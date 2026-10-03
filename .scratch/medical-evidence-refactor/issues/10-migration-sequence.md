# What implementation sequence reaches the agreed patient pilot?

Parent: [Plan an evidence-supported medical chatbot for iPhone](../map.md)
Type: grilling
Labels: wayfinder:grilling
Status: resolved
Assignee: codex
Blocked by: 08, 09

## Question

Given the selected architecture and validation bar, agree the implementation stages, concrete deliverables, development environment needs including Mac/Xcode access, and pilot completion criteria. Produce the handoff specification for the actual refactor and identify any remaining fog. Implementation is a later effort unless the user changes the destination.

## Answer

Resolved 2026-10-03 using the user-authorized recommended decision.

Implement the specified contracts and evidence gate, curated candidate corpus, bilingual web/visit workflow, native iPhone project, deployment scaffolding and tests. Restore tracked manifests; remove tracked bytecode and retire unsafe routes. Validate locally and through macOS CI, then commit the complete change with the user as sole author and push to origin. This execution direction supersedes the earlier planning-only destination. Clinical release, signing/App Store submission, real reviewer appointments and privacy/classification approval are explicit external prerequisites, not fabricated deliverables.

Implementation/specification context: [Medical evidence chatbot specification](../../../spec.md). Clinical release prerequisites are separate from this completed design decision.
