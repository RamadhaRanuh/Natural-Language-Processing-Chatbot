# What evidence promise should every medical answer make?

Parent: [Plan an evidence-supported medical chatbot for iPhone](../map.md)
Type: grilling
Labels: wayfinder:grilling
Status: resolved
Assignee: codex
Blocked by: 02, 03

## Question

Agree what counts as a medical claim; whether research papers alone or labeled guidelines and official drug information are admissible; what passage, numeric data, population, uncertainty, and access-level information the user sees; and when the system withholds a claim. Distinguish evidence support from clinical truth and individual applicability. Decide how approved safety language is sourced. Establish the public promise without asserting perfect verification.

Include mixed questions that contain both supportable and unsupported medical propositions: decide whether and how to present a partial answer without implying support for the remainder. Keep patient-reported visit-summary statements separate from medical claims added by the system.

## Comments

- User accepts research papers plus clearly labeled clinical guidelines and official drug information, confirmed during charting on 2026-10-02. Do not revisit this source-type choice without new evidence or a requested change. Claim coverage, evidence display, and withholding rules still need resolution.

## Answer

Resolved 2026-10-03 using the user-authorized recommended decision.

Every medical proposition must have source-linked support. Use short original-language extracts, exact passage/data locators, rights and freshness checks, and source-bound human review for clinical publication; never promise medical truth or personal applicability. Mixed/unsupported requests abstain rather than silently adding model prose. The optional LLM selects existing claim IDs only. Guidelines/drug information remain separately labeled references until their adapters/corpus are reviewed. Unreviewed Indonesian medical translations are withheld.

Implementation/specification context: [Medical evidence chatbot specification](../../../spec.md). Clinical release prerequisites are separate from this completed design decision.
