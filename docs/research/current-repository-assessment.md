# Current repository and refactor gaps

Read-only assessment dated 2026-10-02, against repository commit `0ff9d29`. No dependency installation, application startup, or model execution was performed. Findings describe inspected source and local artifacts, not measured runtime behavior.

## Existing foundation

The project separates a Python FastAPI service from a Next.js web interface. PDF loading, Chroma storage, and LlamaIndex retrieval can inform the future ingestion and retrieval modules: [ingestion](../../src/ingest.py), [retrieval](../../src/rag.py), [API](../../src/api.py), and [web interface](../../frontend/src/app/page.tsx).

## Gaps against the user's destination

| Requirement | Inspected baseline | Refactor implication to decide |
| --- | --- | --- |
| Every medical claim has inspectable support | `src/api.py:65` records filename, page, and a short retrieved snippet; `:88` publishes generated text before appending sources at `:93`. There is no claim-to-passage mapping or verification result. | Introduce an evidence contract and publication gate before exposing medical claims. Retrieved sources alone cannot establish support. |
| Display underlying research data | No structured paper identifiers, study population, sample size, outcomes, effect estimates, or uncertainty are returned. | Choose a structured evidence model and numeric validation rules. Do not fabricate missing values. |
| Research papers and labeled authoritative guidance | Dataset contains five Gale medical encyclopedia PDFs. No corpus license/provenance manifest was found. Historical notebook outputs contain a 2002 copyright notice and reproduction restrictions (`Main.ipynb:4314`, `:4317`). | Establish approved sources, permitted reuse, versioning, and retraction handling. Current PDFs are not a research-paper corpus. |
| iPhone application | Responsive web layout exists (`page.tsx:98`, `:145`); no Swift/iOS project or PWA manifest was found. API URL is hardcoded to `http://localhost:8000/chat` (`:47`). | Define a hosted API and native client contract. On a phone, localhost refers to the phone. |
| Follow-up questions and visit preparation | Frontend sends only the latest query (`page.tsx:51`); backend reads only the last message (`src/api.py:47`). History exists in React state. | Decide conversation context, retention, and visit-summary behavior. |
| Reproducible development | Root `.gitignore:7-8` ignores package manifests and lockfiles; frontend manifests are absent. Python dependencies are unpinned. Configured GGUF and Chroma vector database are absent locally. Existing storage directory bypasses index creation (`src/ingest.py:20`, `main.py:10`). | Restore development prerequisites as an implementation stage. Planning does not assume the existing application currently runs. |
| Hosted service readiness | CORS allows all origins (`src/api.py:15`), inference is synchronous within an async endpoint (`:50`), health endpoint only returns an unconditional status (`:36`). No auth, deployment config, evidence evaluation suite, or clinical escalation was found. | Decide deployment boundaries, patient data handling, concurrency, readiness, and validation appropriate to the agreed scope. |

The current web interface uses OpenEvidence's name and advertises peer-reviewed grounding (`page.tsx:165`) that the inspected pipeline does not establish. Future product naming and accuracy wording should describe actual measured capabilities.

Historical notebook output also includes a linguistics textbook (`Main.ipynb:3933`) absent from the current Dataset; those outputs do not prove what is in the current index. The configuration retrieves two chunks (`src/config.py:18`), and retrieval directly feeds synthesis (`src/rag.py:42`).

## Scope confirmed during charting

- Audience: patients and caregivers.
- Role: medical education and doctor-visit preparation.
- Platform: native iPhone client with a hosted evidence service.
- Evidence sources: research papers, plus clearly labeled clinical guidelines and official drug information.
- Languages: English and Indonesian.
- Deliverable now: research and decision map; application implementation follows scope agreement.
- First launch country: Indonesia, explicitly confirmed by the user.

The decision map is [Plan an evidence-supported medical chatbot for iPhone](../../.scratch/medical-evidence-refactor/map.md). Architecture proposals in the research reports remain inputs to human decision tickets, not adopted implementation decisions.
