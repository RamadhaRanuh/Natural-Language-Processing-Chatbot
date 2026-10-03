# What evaluation evidence is required before the patient pilot?

Parent: [Plan an evidence-supported medical chatbot for iPhone](../map.md)
Type: grilling
Labels: wayfinder:grilling
Status: resolved
Assignee: codex
Blocked by: 02, 03, 04, 05, 12, 13

## Question

Agree topic coverage, clinician-reviewed reference questions, claim-support precision and coverage, numeric accuracy, citation validity, applicability, abstention, and escalation checks. Establish sample sizes, acceptance thresholds, reviewers, latency expectations, and pilot boundaries. No numeric performance guarantee is selected without measurement or a human decision.

## Answer

Resolved 2026-10-03 using the user-authorized recommended decision.

Use deterministic adversarial integration tests for source identity, retractions/corrections, changed XML, exact passage/data checks, expiry/translation gates, scopes, input constraints and model privacy. Add phone/desktop browser interaction checks, Swift contract tests and unsigned simulator build CI. Before patient release, require qualified adjudication of at least 200 held-out English and 200 Indonesian cases, full support coverage, no observed numeric/citation or unauthorized-treatment errors, and explicit acceptance of residual risk. Test counts are not clinical validation or zero-risk proof. Detailed reviewer/evaluation requirements are in docs/clinical-release.md.

Implementation/specification context: [Medical evidence chatbot specification](../../../spec.md). Clinical release prerequisites are separate from this completed design decision.
