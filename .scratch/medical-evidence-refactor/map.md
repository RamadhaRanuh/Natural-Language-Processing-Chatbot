# Plan an evidence-supported medical chatbot for iPhone

Labels: wayfinder:map
Status: resolved

## Destination

Finish a researched specification and implement a reviewable adult type 2 diabetes education/visit-preparation development pilot: native iPhone client, hosted evidence publication service, web review client, validation, and a comprehensive sole-user-author commit pushed to origin. Public clinical deployment and App Store submission are outside this source-delivery effort.

## Notes

- Confirmed by the user on 2026-10-02: patients and caregivers are the first audience; native iPhone with a hosted service is the target; this effort delivers research and planning before implementation.
- Confirmed first-release role: medical education and preparation for a doctor visit. Confirmed languages: English and Indonesian. Confirmed first launch market: Indonesia.
- Central requirement: medical details must have inspectable evidence and show the underlying study data. The user accepts research papers plus clearly labeled clinical guidelines and official drug information. The precise claim coverage, display rules, and verification/abstention contract remain to be settled.
- Use wayfinder, grilling, domain-modeling, and research. Grilling tickets resolve through conversation with the user. Research uses primary sources and distinguishes vendor claims from independent evaluations.
- Tracker: local Markdown, following `C:/Users/Rama Ranuh/.codex/skills/setup-matt-pocock-skills/issue-tracker-local.md`. Child tickets live in `issues/`; dependencies use `Blocked by:`. Open unassigned tickets whose blockers are resolved form the frontier.
- Research artifacts live in `docs/research/`, with throwaway `research/*` branches as context snapshots. Do not switch the working branch while researching.
- Competitive research is a representative market landscape, not an assertion that every medical chatbot has been examined. Availability and evidence are dated 2026-10-02.
- Execution override on 2026-10-03: the user explicitly requests the completed spec, implementation, commit and push, and directs grilling to use recommendations. This supersedes the earlier planning-only scope, live approval/prototype exchange and one-decision-per-session limits for this effort. Record delegated decisions transparently; do not fabricate clinical approvals.
- Canonical implementation specification: [Medical evidence chatbot](../../spec.md). Native/build and medical-release prerequisites remain honest and explicit.
- All thirteen decisions are resolved. The implementation and local checks are recorded in [Implementation validation](../../docs/validation.md); native/container results are tracked by the repository CI workflow. Clinical release remains outside this source-delivery map.
- Read-only baseline assessment: [Current repository and refactor gaps](../../docs/research/current-repository-assessment.md). Missing manifests/model/vector database mean the existing app was not run; the assessment does not assert runtime correctness.
- User answers confirmed before map creation are standing preferences above, not artificially resolved decision tickets.

## Decisions so far

<!-- One gist and named link per resolved decision; detail lives in its ticket. -->

- [Which medical chatbot capabilities should shape this patient product?](issues/01-medical-chatbot-landscape.md): Thirteen offerings reveal overlapping citation features; test patient-readable, auditable evidence and bilingual visit preparation as the proposed advantage.
- [What can claim-level medical evidence verification reliably establish?](issues/02-evidence-verification-feasibility.md): Passage and numeric support require explicit publication checks; evidence support, certainty, and patient applicability remain distinct.
- [Which adult education topic has suitable sources for the Indonesia pilot?](issues/11-adult-pilot-source-readiness.md): Both candidates have updated Indonesian guidance; source readiness favors type 2 diabetes, with coverage and reuse rights still needing a full audit.
- [What medical role belongs in the patient first release?](issues/03-first-release-medical-role.md): Adult type 2 diabetes education and reviewed visit summaries for users/patients aged 18+, with approved safety interruptions and defined medical boundaries.

- [What evidence promise should every medical answer make?](issues/04-evidence-promise.md): Source-bound publication; original excerpts or reviewed translations; unsupported content withheld.
- [How should the Indonesia launch handle local guidance and bilingual evidence?](issues/05-launch-country-and-language.md): Indonesia-specific references and bilingual UI; medical translations require review.
- [What patient data may the app collect, retain, and send to services?](issues/06-health-data-boundaries.md): Session-only health information; no patient text to literature/model services.
- [How should patients inspect claims and study data on iPhone?](issues/07-iphone-evidence-experience.md): Per-finding evidence sheets plus an editable, reviewed visit summary.
- [Which permitted sources cover the adult type 2 diabetes pilot?](issues/12-diabetes-evidence-corpus.md): Two licensed candidates; discrepancies/corrections retained and patient approval absent.
- [Who approves and maintains the pilot's safety interruptions?](issues/13-clinical-safety-approval.md): Owner appoints qualified reviewers; version-bound clinical approvals remain required before release.
- [Which architecture should replace the current retrieve-and-stream pipeline?](issues/08-refactor-architecture.md): FastAPI publication gate, curated evidence and native SwiftUI sharing a typed API.
- [What evaluation evidence is required before the patient pilot?](issues/09-validation-and-release-bar.md): Adversarial API/browser/native checks; separate qualified clinical release assessment.
- [What implementation sequence reaches the agreed patient pilot?](issues/10-migration-sequence.md): Implement and validate the development pilot, then publish a sole-user-author commit.

## Not yet specified

None within the agreed source-delivery specification. Clinical reviewer appointments, rights/coverage expansion, country-specific public-release approval and App Store/device signing are explicit predeployment work in [Clinical release prerequisites](../../docs/clinical-release.md), not unresolved implementation choices.

## Out of scope

- Public clinical deployment and App Store submission; source implementation and push are authorized by the 2026-10-03 execution override.
- Claiming perfect accuracy, clinical validation, or guaranteed App Store acceptance from retrieval or citations.
- Exhaustive coverage of every medical chatbot or private vendor feature.
- Personalized diagnosis or treatment recommendations in the first release; the user selected education and appointment preparation.
- [Broader medical coverage, pediatric advice, pregnancy-specific advice, and routine symptom-based urgency scoring](issues/03-first-release-medical-role.md) are beyond the agreed adult type 2 diabetes pilot; later expansion requires a separate scope decision.
