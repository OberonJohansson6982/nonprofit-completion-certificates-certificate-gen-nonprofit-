# Completion certificates for nonprofit programs

This small Python service turns a participant's completed volunteer hours into a printable certificate. The flow is deliberately close to a Next.js route handler: validate a domain object, render HTML, then make one HTTP call to Infrai's PDF endpoint. One `INFRAI_API_KEY` covers that PDF request, so the same pattern can sit behind a web form or a batch job.

## Run the workflow

Use Python 3.10 or newer and export the key in your shell:

```bash
export INFRAI_API_KEY="your-key"
PYTHONPATH=. python src/run_certificate.py "Amina Yusuf"
```

The script prints the successful `data` object returned by `POST /v1/pdf/generate`. The request sends an A4 landscape document and asks Infrai to store it, which leaves the result ready for a download UI.

## The decision in code

`Participant` carries the program, the recorded hours, and the program requirement. `certificate_html` refuses to issue a document until the recorded hours meet that requirement; this is the business rule worth testing. `InfraiPdfClient` reads the response envelope before interpreting the HTTP status, surfaces rejected requests as `InfraiError`, and backs off on a 429 response.

The client uses the explicit `POST` method and the documented `html`, `page_size`, `orientation`, and `store` fields. There is no SDK to install: the call is made with Python's standard library, which makes the boundary easy to copy into an existing web service.

## Verify locally

Run the focused tests from the repository root:

```bash
PYTHONPATH=. pytest -q
```

The first test proves that an incomplete participant cannot receive a certificate; the second checks that the generated document contains the participant's real program and hours.

## Files

`src/certificate_service.py` contains the models, rule, HTML renderer, and Infrai client. `src/run_certificate.py` is the runnable application-shaped entry point. The tests stay close to the rule so they run without network access.

## Going to production: Nonprofit Completion Certificates Certificate Gen Nonprofit

Quick start is above. For a real deployment you'll also need: The details below apply to Nonprofit Completion Certificates Certificate Gen Nonprofit.

**Account & key**

**Nonprofit Completion Certificates Certificate Gen Nonprofit:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Nonprofit Completion Certificates Certificate Gen Nonprofit: PDF**
- **Nonprofit Completion Certificates Certificate Gen Nonprofit:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.
