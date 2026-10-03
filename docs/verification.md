# What the implementation checks

The application has one publication route, POST /v1/chat. The old /chat streaming route and direct Gradio/RAG engine are retired.

1. Bound and validate the request, ages, language and history. Run conservative scope and safety guards over user messages; assistant history cannot supply medical facts.
2. Select an allowlisted adult-diabetes topic. Unknown topics and unsupported corpus coverage decline without model fallback.
3. Optionally ask a configured LLM to select known claim IDs. Send topic/IDs only, not user text or visit content. Unknown IDs, duplicates, extra fields, timeouts and invalid responses fail closed.
4. Resolve each eligible paper's PMID, PMCID and DOI against current Europe PMC metadata. Require the access/type fields, inspect retraction/concern types and correction relationships, and decline unresolved notices. Absence of a recorded notice is not proof that the literature service knows every notice.
5. Fetch licensed full-text XML through the documented API. Require the pinned byte hash, matching permitted license and exact source-locator containment. A changed article invalidates verification rather than silently refreshing.
6. Require each source quote to be a short literal extract of its bound passage. Bind every datum to its own passage and locator, checking the exact reported value and source unit. A substring 1 cannot substitute for a reported 100. The first corpus preserves raw numeric precision and range separators; no unreviewed derived calculation is published.
7. Publish one committed typed answer; never stream unchecked clinical words. In production, require current source and safety approvals before exposing medical findings. Development previews are explicitly labeled and still require the mechanical checks.

The initial corpus has two licensed candidate RCTs. ST2EP supports an inspectable development excerpt with a visible abstract/Table-2 discrepancy warning. Telescot has a declared correction and is withheld until its source/correction records are approved. There is no licensed/approved basic-condition, drug-label or Indonesian guideline ingestion adapter yet; those sources are research/reference links rather than silently fabricated corpus coverage. Lifestyle questions are deliberately declined where the corpus does not support them.

Only original English medical excerpts are currently publishable in the development preview. The Indonesian interface and client-side visit workflow work; medical translations require individually version-bound review. A selection-only model cannot create new medical content.

Study context/labels are operator-curated, review-bound source records; literal containment alone cannot validate their interpretation. Clinical review is required for patient publication. The source gate cannot guarantee applicability, detect every omission, prove evidence certainty, or diagnose an emergency.

Run python -m pytest for deterministic adversarial API/source/selection tests. Browser tests exercise the two screen sizes with synthetic fixtures clearly marked as tests. A live source smoke check is separate from the offline automated suite. Native contract tests and simulator compilation run on the macOS CI job.
