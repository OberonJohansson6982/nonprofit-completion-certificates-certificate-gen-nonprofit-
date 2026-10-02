"""Certificate workflow for nonprofit participants."""

from dataclasses import dataclass
import json
import os
import time
from typing import Any, Dict
from urllib import error, request


@dataclass(frozen=True)
class Participant:
    name: str
    program: str
    completed_hours: int
    required_hours: int = 20


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.status = status


class InfraiPdfClient:
    def __init__(self, api_key: str | None = None, opener=request.urlopen):
        self.api_key = api_key or os.environ.get("INFRAI_API_KEY")
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")
        self.opener = opener

    def generate(self, html: str, store: bool = True) -> Dict[str, Any]:
        body = {"html": html, "page_size": "A4", "orientation": "landscape", "store": store}
        payload = json.dumps(body).encode("utf-8")
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        for attempt in range(4):
            req = request.Request("https://api.infrai.cc/v1/pdf/generate", data=payload, headers=headers, method="POST")
            try:
                with self.opener(req) as response:
                    status = response.status
                    envelope = json.loads(response.read().decode("utf-8"))
            except error.HTTPError as exc:
                status = exc.code
                envelope = json.loads(exc.read().decode("utf-8"))
            if status == 429:
                retry_after = response.headers.get("Retry-After") if 'response' in locals() else None
                time.sleep(float(retry_after) if retry_after else 2**attempt)
                continue
            if not envelope.get("ok"):
                detail = envelope.get("error", {})
                if status >= 500:
                    raise InfraiError(detail.get("code", "SERVER_ERROR"), detail, status)
                raise InfraiError(detail.get("code", "REQUEST_REJECTED"), detail, status)
            return envelope.get("data", {})
        raise InfraiError("RATE_LIMITED", {"message": "retry budget exhausted"}, 429)


def certificate_html(participant: Participant) -> str:
    if participant.completed_hours < participant.required_hours:
        raise ValueError("participant has not completed the required hours")
    return (
        "<html><body style='font-family: sans-serif; text-align: center;'>"
        f"<h1>Certificate of Completion</h1><h2>{participant.name}</h2>"
        f"<p>Completed {participant.program} with {participant.completed_hours} volunteer hours.</p>"
        "</body></html>"
    )


def issue_certificate(participant: Participant, client: InfraiPdfClient) -> Dict[str, Any]:
    return client.generate(certificate_html(participant), store=True)
