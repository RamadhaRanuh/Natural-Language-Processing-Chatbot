# Who approves and maintains the pilot's safety interruptions?

Parent: [Plan an evidence-supported medical chatbot for iPhone](../map.md)
Type: grilling
Labels: wayfinder:grilling
Status: resolved
Assignee: codex
Blocked by: 03, 04, 05

## Question

For the approved safety-interruption path, decide who is accountable for clinical approval, the reviewed criteria and content format, verified Indonesia-specific care resources, and maintenance/version ownership. Define how this path differs from excluded routine urgency scoring and what to do when context or local resource availability is uncertain. Define which safety decisions require qualified clinical review and what evidence of approval must exist before a patient pilot. The agent must not invent clinical thresholds or assume emergency detection is reliable. Measured safety performance and release thresholds belong in the validation ticket.

## Answer

Resolved 2026-10-03 using the user-authorized recommended decision.

The project owner is accountable for appointing a qualified adult-diabetes clinician and English/Indonesian medical-language reviewer before public patient use. No named reviewer or clinical signoff is invented. Source, translation and safety records are hash-bound, dated and expiring, controlled on the server. Safety review binds routing criteria and fixed bilingual messages; local help routes need operational review. Generic service-limitation/help access stays available without retrieval, model or age confirmation. Keyword matching is a limited guard, never a validated diagnosis/urgency detector; clinical thresholds are not fabricated. Public release requirements are captured in docs/clinical-release.md.

Implementation/specification context: [Medical evidence chatbot specification](../../../spec.md). Clinical release prerequisites are separate from this completed design decision.

Research asset: [Safety and bilingual policy](../../../docs/research/safety-and-bilingual-policy.md).
