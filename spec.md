# Medical evidence chatbot — implementation specification

Status: approved implementation direction through the user's delegated recommendations on 2026-10-03.

## Product and scope

Build an iPhone application backed by a hosted Python service, with a responsive web client for development and accessibility checks. The first pilot serves adult type 2 diabetes education and doctor-visit preparation in Indonesia, in English and Indonesian. Both users and patients must be 18 or older. It does not diagnose, prescribe, change medication doses, provide pregnancy/pediatric advice, or issue routine urgency scores.

The user authorizes using recommended answers for remaining wayfinder decisions, finishing this specification, implementing it, and committing/pushing with the user as the sole author. This supersedes the previous planning-only scope and live interview requirement. It does not constitute clinician approval, clinical validation, consent to process patient records with external models, or authorization to release a medical device.

## Evidence promise

Every published medical proposition must link to an identified, current, permitted source and a precise supporting passage. Show the original source, passage locator, study population/design, reported results, denominator/timeframe and uncertainty where available. Missing data remains missing. Guidelines and official drug information are separately labeled and never represented as papers.

Source support, evidence certainty, and personal applicability are separate. A citation is not proof of truth. The application must not advertise 100% clinical accuracy.

For this implementation, the deterministic publication gate accepts only original-source extracts or explicitly reviewed bilingual claims tied to original passages. An optional LLM may select candidate claim IDs from the corpus; it cannot invent new medical prose, numbers, citations, translations, or instructions. Invalid model output fails closed. No API key is needed for the default evidence-selector path. The model receives only a selected biomedical topic and public evidence metadata; symptoms and conversation text are not sent to it.

Indonesian interface text and visit preparation work immediately. Original research passages remain in their original language, visibly labeled. An Indonesian medical translation may be published only when its exact source/version/text hash has a dated, unexpired review record. Unreviewed translations are withheld rather than misrepresented as verified.

## Evidence corpus and freshness

Use a small, versioned JSON corpus of permitted primary research, with stable source/claim IDs, DOI/PMID/PMCID, license URI, exact source excerpts, locators, data values, and checksums. Do not ingest the legacy Gale PDFs. Each numeric datum has its own supporting passage and locator; retrieved similarity never proves support.

Resolve source identity, retraction/correction state and metadata through documented Europe PMC APIs at query time, with a short shared public-metadata cache. Unknown/unavailable/stale status, identity mismatch, retraction, or unresolved correction blocks the affected source. A correction requires an explicit review record tied to the source version. Production never trusts a client-supplied source or review flag.

Offline demonstration is explicitly labeled, contains no clinical accuracy promise, and cannot be mistaken for fresh literature checking. Tests use synthetic fixtures; source assertions in tests do not authorize production sources.

Rights, bibliographic checks and excerpt containment are mechanical gates. Clinical context, omission risks, source suitability and language clarity require qualified review and evaluation before public patient use. A review manifest defaults to unapproved; health/readiness reports disclose that state. Production is the startup default. Source approvals bind complete source records; safety approvals bind patterns, help links and bilingual fixed messages. Both require dated, unexpired records.

## Conversation and publication

POST /v1/chat accepts bounded conversation history, selected language, age confirmations and optional use of the external candidate selector. Return one typed committed answer. No unverified medical tokens stream to clients. States are ready, insufficient_evidence, blocked_by_scope, safety, and review_required. Sources and claims have stable IDs; clients display the same typed contract.

Answer scope is selected from a small auditable set of adult diabetes education topics, such as lifestyle-study findings and long-term outcomes. Queries outside the corpus decline with a scope explanation. Questions requiring personal diagnosis, targets, dosing, pregnancy advice or pediatric care are not turned into treatment recommendations. Previous assistant text cannot establish a clinical fact or source.

Simple bilingual scope/safety matching is a conservative interaction guard, not a diagnostic classifier or validated emergency detector. Approved safety criteria may interrupt normal answers; until clinical content and triggers are approved, show a clearly identified general service-limitation notice, link to official help, and report review_required. Never claim that lack of a trigger means the user is safe.

## Visit preparation and privacy

Provide an editable client-side form for patient-reported symptoms, timing, concerns, current prescribed medicines and clinician questions. Generate a summary using those entries verbatim, not inferred clinical findings. Users preview and confirm before copying/sharing. Saved visit text, accounts, record uploads and HealthKit are outside the first implementation.

Server requests are processed in memory and not retained; responses use no-store caching. Do not log question bodies, model prompts or visit content. Disable access logs in documented production startup. External literature searches contain topic terms/identifiers, never patient identifiers. No clinical text in analytics or push notifications. Browser/native state disappears on reset/termination; OS clipboard/share destinations are under user control.

Use bounded request sizes/history, per-request timeouts, restricted CORS, HTTPS for non-local endpoints and environment-only model secrets. No shared application secret belongs in an iPhone binary. Public internet deployment still needs a real authentication/rate-limit perimeter, controller/processor review and local legal classification; localhost development is supported without fabricating those approvals.

## Clients

Web: independent project identity, mobile-first layout, bilingual controls, explicit adult confirmations, short answer cards, tap-to-inspect evidence, source/data sheets, unknown/stale/provider-failure states, editable visit sheet and reset. Avoid third-party font downloads and external analytics.

iPhone: native SwiftUI iOS 17+ application using URLSession, the same typed API, adult confirmations, topic suggestions, evidence/detail sheets and an editable visit summary. Configure an HTTPS backend in the app; permit localhost HTTP only in DEBUG simulator builds. No HealthKit or iCloud health-data persistence. Use Dynamic Type, VoiceOver labels and system controls. Include an XcodeGen project and macOS CI build with signing disabled; App Store/device signing remains an external credential step.

## Architecture

- src/contracts.py: public and corpus models; bounded input validation.
- src/evidence.py: corpus/provenance validation, public metadata resolution and freshness.
- src/verification.py: exact passage, numeric and reviewed-translation publication checks.
- src/service.py: scope, topic selection, optional model selection, answer assembly.
- src/api.py: FastAPI transport, health/readiness and JSON chat.
- src/safety.py: separately versioned interaction guards and review status.
- data/evidence/: source and claim corpus plus explicit unapproved clinical-review manifest.
- frontend/: reproducible Next.js client with same-origin server proxy.
- ios/: SwiftUI app, typed models, transport and XcodeGen project.

Retire the executable legacy retrieve-and-stream/Gradio routes so they cannot bypass the publication gate. Preserve historical PDFs/notebooks as unapproved artifacts outside the active runtime.

## Validation and acceptance

Meaningful backend tests must cover real API requests, invalid ages/history, no unverified or invented citations, missing/mismatched numbers and context, retracted/corrected/stale/unavailable metadata, unresolved source identity, prompt-injection/model-selected unknown IDs, missing clinical approval, unreviewed Indonesian translations, bilingual scope/safety handling, no patient text in provider/model calls, and explicit corpus insufficiency.

Web checks: TypeScript, ESLint, production build, browser checks at phone and desktop widths for adult gate, answer/evidence sheets, visit edit/copy, errors, language switch and reset. Native CI: macOS Swift tests for decoding and request policy, generated project, simulator compilation without signing. Report any check that cannot run; do not describe unbuilt native source as device-tested.

The implementation is a working evidence-gated development pilot, not a clinically released product. Production medical answers require a genuine clinical approval manifest and reviewed translations. A demo/review-required state is a supported product state, not permission to silently disable checks.

Before public patient release, qualified reviewers must adjudicate held-out English/Indonesian cases, omissions, numeric accuracy, source support, applicability, refusals and safety errors. Measured release thresholds, source rights, Indonesia classification and operational ownership must be approved by accountable humans. Document these as release prerequisites, not fabricated completed tasks.

## Delivery

Restore tracked dependency manifests and lockfiles, provide local and Docker startup, environment examples and a README describing the real behavior. Include dated comparative research and resolved wayfinder decision tickets, model/corpus limitations and verification instructions. Commit the complete reviewed implementation with the user's configured name/email as sole author, no co-author trailers, then push to origin. A push authorizes source publication; deployment/App Store submission is not part of this request.
