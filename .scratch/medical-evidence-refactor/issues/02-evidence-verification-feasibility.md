# What can claim-level medical evidence verification reliably establish?

Parent: [Plan an evidence-supported medical chatbot for iPhone](../map.md)
Type: research
Labels: wayfinder:research
Status: resolved
Assignee: evidence_verification
Blocked by: none

## Question

Which authoritative paper APIs, licensed full-text sources, evidence extraction methods, verification gates, and evaluation practices can support a medical answer with inspectable passages and study data? Establish the limits of citations, source entailment, clinical applicability, numeric validation, retractions, conflicting findings, and streaming. Investigate hosted-service and native-iPhone feasibility against current official documentation, and identify intended-use and jurisdiction-dependent constraints without selecting the user's scope.

## Comments

- Research started 2026-10-02. Artifact target: `docs/research/evidence-verification-and-ios.md`; branch: `research/evidence-verification-and-ios`.

## Answer

Resolved 2026-10-02 after review of [Medical evidence verification and native iPhone feasibility](../../../docs/research/evidence-verification-and-ios.md). Research snapshot: branch `research/evidence-verification-and-ios`, report-only commit `1b405b8`.

Source support can be checked against identifiable passages and reported numeric facts. It does not establish clinical truth, study certainty, or applicability to an individual. A defensible proposed pipeline separates evidence identity/rights/status, structured extraction, atomic claims, passage and numeric checks, and final publication. Recheck rendered English/Indonesian statements so translation cannot introduce unsupported claims. Release clinical text after checking; show only neutral progress before publication.

Show reported study design, population, outcome-specific denominators, intervention/comparator, time horizon, results and confidence intervals when accessible. Preserve absent fields as absent; raw participant data is a different asset and must not be implied. Abstract-only access limits what can be supported. Guidelines and drug information need their own source category, jurisdiction, version, and status.

Current supported PubMed/PMC/Europe PMC/Crossref routes can provide literature, identity and update inputs, subject to source rights and schema validation. The legacy PMC OA Web Service was discontinued August 25, 2026; choose current datasets/OAI-PMH routes instead. Missing notices do not prove a source is current or unretracted.

Native SwiftUI plus a hosted typed API is feasible; Mac/macOS build access is needed for native compilation and device validation. HealthKit is optional. Indonesia-specific feature classification, patient-data handling, authority selection, and clinical validation thresholds remain open decisions. The report includes primary references, proposed module seams, provenance/numeric fields, and evaluation metrics; none constitutes a validated deployed implementation.
