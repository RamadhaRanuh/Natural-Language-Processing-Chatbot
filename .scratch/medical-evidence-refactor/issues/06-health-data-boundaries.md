# What patient data may the app collect, retain, and send to services?

Parent: [Plan an evidence-supported medical chatbot for iPhone](../map.md)
Type: grilling
Labels: wayfinder:grilling
Status: resolved
Assignee: codex
Blocked by: 03, 05

## Question

Decide whether accounts, saved conversations, patient context, uploaded records, or Apple Health access belong in the first release. Agree retention, deletion, hosting, provider data handling, and whether clinical text is excluded from telemetry. Evaluate options against the selected launch country and medical role; do not assume health-data integrations are necessary for chat.

## Answer

Resolved 2026-10-03 using the user-authorized recommended decision.

Use session-only conversation state and client-side, user-reviewed visit forms. No accounts, saved health conversations, record uploads, HealthKit or iCloud storage in this version. Provider searches and model selection receive public topic/identifiers only. No clinical request bodies in logs/analytics; no-store responses, restricted CORS, bounded inputs, timeouts and HTTPS outside local development. Sharing occurs only through a user-confirmed clipboard/system sheet. Internet hosting requires a real identity/abuse-control perimeter and country-specific controller/processor review.

Implementation/specification context: [Medical evidence chatbot specification](../../../spec.md). Clinical release prerequisites are separate from this completed design decision.
