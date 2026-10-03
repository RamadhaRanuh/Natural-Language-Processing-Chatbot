# Which architecture should replace the current retrieve-and-stream pipeline?

Parent: [Plan an evidence-supported medical chatbot for iPhone](../map.md)
Type: grilling
Labels: wayfinder:grilling
Status: resolved
Assignee: codex
Blocked by: 02, 03, 04, 05, 06, 07, 12, 13

## Question

Choose the evidence-source adapters, ingestion provenance, retrieval, draft-and-verify boundary, answer publication protocol, hosted model/provider strategy, and native iPhone API contract. Decide what existing FastAPI and indexing code can be reused, how Next.js fits the final product, and how verified answers are reproduced. Make architecture choices only after the product and evidence boundaries are known.

## Answer

Resolved 2026-10-03 using the user-authorized recommended decision.

Keep FastAPI but replace direct LlamaIndex/GGUF synthesis with EvidenceRepository, exact ClaimVerifier, optional selection-only model, and a single committed JSON answer. Use a versioned curated corpus plus documented Europe PMC metadata/full-text validation, pinned document/record hashes and expiring server-controlled review records. Implement native SwiftUI iOS17+ and a Next.js web review client with a server-only proxy. Retire the unverified legacy streaming/Gradio routes. Ship non-root, production-gated Docker configuration and reproducible Python/npm manifests. No model-specific API secret belongs in a client.

Implementation/specification context: [Medical evidence chatbot specification](../../../spec.md). Clinical release prerequisites are separate from this completed design decision.
