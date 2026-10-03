# Sehat Evidence

An evidence-gated adult type 2 diabetes education and doctor-visit preparation pilot: a native iPhone app, a hosted-service backend, and a responsive web client. Indonesia is the first target market; the interface and visit workflow support English and Indonesian.

The complete [specification](spec.md) and [wayfinder map](.scratch/medical-evidence-refactor/map.md) document the decisions. The product focuses on inspectable research, not an unrestricted medical chat response.

## What works

- One typed answer after checking source identity, permitted rights, current metadata, article hash, exact passage location and reported numeric values.
- Per-finding evidence sheets with the original passage, study population/design, results, endpoint/sample context, uncertainty, limitations and original-paper links.
- An optional HTTPS LLM candidate selector whose output is limited to known evidence IDs. It does not receive patient text or generate clinical prose.
- English/Indonesian UI, explicit 18+ confirmations for both users and patients, conservative scope handling and an always-accessible official-help link.
- Editable, user-reviewed visit summaries assembled from the user's entries on the client; no generated diagnoses or urgency scores.
- SwiftUI iPhone/iPad client, reproducible XcodeGen project and native contract/build CI.

## Deliberate limits

This is a development research preview, **not a clinically validated patient service**. Source support does not prove medical truth or individual applicability. Production medical findings remain blocked until genuine clinical review records are supplied. No reviewer identity or approval has been invented.

The initial licensed corpus is small. One study has a correction and is withheld; another has a discrepancy explicitly preserved for review. Unsupported topics decline. Original English passages are shown with labels when a reviewed Indonesian medical translation is unavailable. The app does not claim a full bilingual medical-answer corpus, diagnose, prescribe, alter doses, give routine urgency scores, or provide pediatric/pregnancy advice.

Historical Gale PDFs, notebooks and vector artifacts are not active evidence. They remain historical repository artifacts, with no new rights or clinical trust implied.

See [verification behavior](docs/verification.md), [corpus audit](docs/research/diabetes-corpus-audit.md), and [clinical release requirements](docs/clinical-release.md).

## Run locally

Python 3.11+ and Node 22.13+ are recommended. Dependency manifests and the npm lockfile are tracked.

Windows PowerShell:

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
$env:APP_ENV = "development"
.\.venv\Scripts\python.exe main.py
~~~

macOS/Linux:

~~~sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
APP_ENV=development .venv/bin/python main.py
~~~

In a second terminal:

~~~sh
cd frontend
npm ci
npm run dev
~~~

Open http://localhost:3000. The Next.js server proxies requests to http://127.0.0.1:8000; a phone never uses its own localhost as the hosted backend. Set the server-only EVIDENCE_API_URL to your HTTPS backend for hosted web use.

Start requests with an education-study question. Live verification requires internet access to Europe PMC; a provider failure yields no clinical fallback. The lifestyle example demonstrates unsupported-corpus behavior. No model download, vector database, patient account or API key is required.

APP_ENV defaults to production when not explicitly set; local research previews must be explicitly enabled. Production is intentionally review-gated. Environment examples show optional model configuration. Secrets belong only on the server.

## iPhone

Follow [ios/README.md](ios/README.md) on a Mac with Xcode. Generate the project with XcodeGen, select an iPhone simulator, and set the development server using the app's settings. Real phones and release builds require an HTTPS backend. Core request/response tests and simulator compilation run in CI; device signing and App Store submission use your own Apple credentials.

## API

~~~http
POST /v1/chat
Content-Type: application/json

{
  "messages": [{"role": "user", "content": "What did diabetes education studies find?"}],
  "language": "en",
  "adult_user": true,
  "adult_patient": true,
  "use_model": false
}
~~~

States: ready, insufficient_evidence, blocked_by_scope, safety, review_required. The response contains stable source/claim IDs, supporting passages and numeric data. No raw model tokens stream. GET /health reports corpus and approval/configuration state; it does not certify clinical accuracy or provider uptime. The retired /chat path returns 404.

Requests have bounded body/history sizes and a 35-second overall publication deadline. Responses use no-store caching; user text is not sent to literature services or the optional selector. There is no patient-data database, localStorage, HealthKit, iCloud sync or clinical analytics. Visit sharing uses the user's clipboard/system share destination after review.

## Validation

~~~sh
python -m pytest
cd frontend
npm run typecheck
npm run lint
npm run build
npx playwright install chromium
npm run test:e2e
~~~

Use the virtual environment's Python executable on Windows. Tests cover invented/altered evidence, numeric/unit errors, retractions/corrections, changed XML, review expiry, translation gating, privacy at provider boundaries, ages, scope, safety, errors, phone/desktop layouts and visit editing. Browser data is explicitly synthetic. CI also runs Swift contract tests and unsigned simulator compilation on macOS.

The production container installs the pinned runtime lockfile, runs as a non-root user, disables access logs, and defaults to the clinical review gate:

~~~sh
docker compose up --build
~~~

The compose port binds to localhost. Internet deployment still needs HTTPS, an authentication/abuse-control perimeter, qualified content approval, clinical evaluation and Indonesia-specific privacy/classification review. Source push does not deploy the app.

## Research

- [Medical chatbot landscape](docs/research/medical-chatbot-landscape.md): 13 representative offerings, intended users, evidence/data presentation, iPhone availability, medical workflow, privacy and evaluation limits.
- [Verification and iPhone feasibility](docs/research/evidence-verification-and-ios.md).
- [Adult pilot source readiness](docs/research/adult-pilot-source-readiness.md).
- [Implementation corpus audit](docs/research/diabetes-corpus-audit.md).
- [Safety and bilingual policy](docs/research/safety-and-bilingual-policy.md).

These dated primary-source reports distinguish vendor assertions from measured results. They are a representative comparison, not a claim to have audited every chatbot or demonstrated this project's clinical efficacy.
