# How should patients inspect claims and study data on iPhone?

Parent: [Plan an evidence-supported medical chatbot for iPhone](../map.md)
Type: grilling
Labels: wayfinder:grilling
Status: resolved
Assignee: codex
Blocked by: 03, 04, 05

## Question

Use a disposable prototype with the user to decide the answer and evidence-card experience: readable summary, per-claim links, supporting passage, study population, measured results and uncertainty, disagreements, and insufficient evidence. Decide accessibility and language behavior. The prototype is for feedback and does not implement the production refactor.

## Answer

Resolved 2026-10-03 using the user-authorized recommended decision.

Select the recommended mobile experience: short attributed findings, a per-finding evidence button, a sheet for source passages, study design/population, reported data, uncertainty, limitations and original links. Keep support, certainty and applicability distinct. Include editable user-reported visit preparation, language controls, explicit age gate, always-available official help, reset and readable error/insufficiency states. The user explicitly delegated recommended decisions, so a live disposable-prototype interview is replaced by this design decision; the implemented web client and phone/desktop interaction checks make it reviewable. Native uses Dynamic Type/system SwiftUI controls.

Implementation/specification context: [Medical evidence chatbot specification](../../../spec.md). Clinical release prerequisites are separate from this completed design decision.
