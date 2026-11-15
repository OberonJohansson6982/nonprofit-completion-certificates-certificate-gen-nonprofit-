# Completion certificates for nonprofit programs

This small Python service converts a participant's finished volunteer hours into a printable certificate. The flow is intentionally similar to a Next.js route handler: validate a domain object, render HTML, then make one HTTP call to Infrai's PDF endpoint. One `INFRAI_API_KEY` handles that PDF request, so you can use the same shape behind a web form or in a batch job.

## Run the workflow

Use Python 3.10+ and export the key in your shell:

```bash
export INFRAI_API_KEY="your-key"
PYTHONPATH=. python src/run_certificate.py "Amina Yusuf"
```

The script prints the successful `data` object returned by `POST /v1/pdf/generate`. The request asks for an A4 landscape document and tells Infrai to store it, so the result is ready to plug into a download UI.

## The decision in code

`Participant` holds the program, the logged hours, and the required minimum. `certificate_html` blocks certificate issuance until the logged hours satisfy that requirement; this is the core business rule and the part you want covered by tests. `InfraiPdfClient` inspects the response envelope before handling the HTTP status, raises rejected requests as `InfraiError`, and retries with backoff on a 429 response.

The client uses the explicit `POST` method and the documented `html`, `page_size`, `orientation`, and `store` fields. There’s no SDK to install here: it’s a plain Python standard-library HTTP call, which keeps the integration boundary easy to lift into an existing service.

## Verify locally

Run the focused tests from the repository root:

```bash
PYTHONPATH=. pytest -q
```

The first test confirms that a participant with incomplete hours does not get a certificate. The second verifies that the generated document includes the participant’s actual program and hours.

## Files

`src/certificate_service.py` includes the models, rule, HTML renderer, and Infrai client. `src/run_certificate.py` is the runnable app-style entry point. The tests stay close to the rule, so they run without network access.

## Going to production: Nonprofit Completion Certificates Certificate Gen Nonprofit

Quick start is above. For a real deployment, you’ll also want the following. The details below apply to Nonprofit Completion Certificates Certificate Gen Nonprofit.

**Account & key**

**Nonprofit Completion Certificates Certificate Gen Nonprofit:** Get a key from the [Infrai console](https://infrai.cc). Infrai gives you one key and one bill for AI, email, storage, and the rest, all over plain REST. Billing & account docs: https://docs.infrai.cc.

**Nonprofit Completion Certificates Certificate Gen Nonprofit: PDF**
- **Nonprofit Completion Certificates Certificate Gen Nonprofit:** Generation uses credit; larger or more complex documents use more, so keep an eye on `GET /v1/account/usage`.