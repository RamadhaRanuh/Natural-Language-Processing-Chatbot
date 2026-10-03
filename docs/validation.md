# Implementation validation

Checked on 2026-10-03 on Windows, Python 3.12.7 and Node 22.12.0. Node 22.13+ is recommended for the complete development dependency tree.

- Backend: 43 tests passed. One upstream Starlette TestClient deprecation warning remains; no test failures.
- Web: TypeScript, ESLint and the production Next.js build passed.
- Browser: six Playwright tests passed across 390-pixel phone and desktop viewports. Evidence fixtures are explicitly synthetic; these tests do not establish clinical validity.
- Production UI smoke: no browser console/page errors or horizontal overflow at phone width. [Phone](screenshots/phone.png) and [desktop](screenshots/desktop.png) captures show the running production client.
- Live web-to-backend-to-Europe-PMC check: an education-study request returned HTTP 200, one source-bound finding and ten reported data items. Indonesian UI preserved the explicitly labeled original English excerpt. The corrected telemonitoring paper was withheld.
- Production configuration check: unapproved medical findings returned review_required with no claims, and health reported clinical_release_ready=false.
- Wayfinder: thirteen resolved decision tickets; local artifact links and dependency graph checked.
- Dependency audit: npm reported zero vulnerabilities at delivery time. This is a dated dependency check, not a guarantee about future advisories.

Native Swift tests, unsigned iPhone simulator compilation and the container build are checked in [GitHub Actions](https://github.com/RamadhaRanuh/Natural-Language-Processing-Chatbot/actions/workflows/ci.yml). Windows cannot run Xcode; the local Docker Desktop daemon was unavailable. Platform results are recorded by CI rather than inferred from source inspection.

The checks validate implementation behavior, not clinical efficacy, the completeness of emergency detection, or patient applicability. No clinician or bilingual medical approvals were created. See [clinical release prerequisites](clinical-release.md).
