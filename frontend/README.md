# Web client

This mobile-first Next.js client complements the native iPhone app. It uses the same committed-answer contract and server-side proxy; no model key is shipped to the browser.

Run npm ci and npm run dev after starting the backend as described in the root README. EVIDENCE_API_URL is a server-only setting and defaults to the local Python service. A hosted backend must use HTTPS.

The app keeps conversation and visit form state in memory. Reset clears both, and changing a visit field clears its review acknowledgement. Clinical translations are not inferred from the interface language: unreviewed research remains visibly labeled in the original English.

Commands: npm run typecheck, npm run lint, npm run build, npm run test:e2e. The phone and desktop browser tests use synthetic source fixtures; they are not medical evaluation results.
