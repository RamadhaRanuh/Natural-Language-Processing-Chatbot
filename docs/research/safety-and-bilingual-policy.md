# Safety and bilingual publication policy: Indonesia adult diabetes education pilot

Checked 2026-10-03 against primary sources. Scope: adults, patient/caregiver education and doctor-visit preparation in Indonesia. This report supplies implementation recommendations and **unapproved draft wording**. Research, user authorization, or a code configuration switch does not constitute clinical approval.

## Official authority inputs

| Input | What was verified | Practical limit |
| --- | --- | --- |
| Indonesian emergency route | Kemenkes's 5 October 2024 announcement identifies **119** as the medical emergency number, accessible across districts/cities, including through SATUSEHAT Mobile. It describes forwarding calls to the nearest hospital in areas without a PSC. [Official announcement](https://www.kemkes.go.id/id/akses-darurat-medis-119-kini-bisa-melalui-satusehat-mobile). | This is published routing information, not an operational test, guaranteed pickup time, universal ambulance availability, or an API/dispatch integration contract. Do not promise the chatbot has called, located, or dispatched help. |
| Current local clinical guideline | JDIH lists **HK.01.07/MENKES/302/2026**, adult type 2 diabetes PNPK, as in force; adoption date 17 April 2026. Kemenkes's public publication page is dated 19 August 2026. [Legal record](https://jdih.kemkes.go.id/documents/keputusan-menteri-kesehatan-nomor-hk0107menkes3022026), [ministry publication](https://www.kemkes.go.id/id/pnpk-tatalaksana-diabetes-melitus-tipe-2-dewasa). | Use the 2026 document for current local review rather than assuming old 2020 materials remain the right corpus. It is clinical guidance aimed at clinical services, not an endorsement of this chatbot or authorization to reproduce dosing algorithms to patients. |
| Acute diabetes complications | The 2026 PNPK discusses emergency referral and acute complications, including hypoglycemia with reduced consciousness and serious hyperglycemic complications (printed pp. 16, 71–72). [Official guideline PDF](https://keslan.kemkes.go.id/unduhan/fileunduhan1777518085_672976.pdf). | The document contains professional treatment instructions; a general excerpt pipeline must not expose those as self-treatment recommendations. Clinical review must select patient-appropriate educational material. |
| Plain-language severe symptoms | NIDDK describes seizures and loss of consciousness as severe low-glucose symptoms needing immediate treatment. Its diabetes symptom page describes difficulty breathing, fainting, abdominal pain/nausea/vomiting among possible ketoacidosis symptoms. [Hypoglycemia](https://www.niddk.nih.gov/health-information/diabetes/overview/preventing-problems/low-blood-glucose-hypoglycemia), [diabetes symptoms](https://www.niddk.nih.gov/health-information/diabetes/overview/symptoms-causes). | These are US official education sources, not Indonesian emergency routing instructions. Never copy their US emergency number into the Indonesia product. Symptoms are neither a diagnosis nor a complete screening checklist. |

No verified public 119 dispatch API was established. The pilot should link to the official route and offer a user-initiated ordinary phone action. Actual iPhone dialing behavior, SIM/connectivity limitations, and local route reachability need testing; do not infer them from ministry publicity. The ministry article was retrieved through the web search result; direct page opens timed out, so preserve the source URL and recheck its availability before release.

## Fixed safety notice and review gate

Recommend a persistent, readily available safety notice rather than relying on an LLM to detect danger in every message. The following is **proposed app-authored wording**, not a quotation from an authority, a clinician-approved translation, or a finished clinical protocol:

**English draft:** “This service provides education and helps you prepare for a doctor visit. It cannot determine whether you are having an emergency. If you or the person you care for has lost consciousness, is having a seizure, or is struggling to breathe, seek emergency medical help now. In Indonesia, call 119. Do not wait for a chatbot response.”

**Indonesian draft:** “Layanan ini memberikan informasi edukasi dan membantu Anda menyiapkan kunjungan ke dokter. Layanan ini tidak dapat menentukan apakah Anda sedang mengalami keadaan darurat. Jika Anda atau orang yang Anda rawat tidak sadarkan diri, mengalami kejang, atau kesulitan bernapas, segera cari pertolongan medis darurat. Di Indonesia, hubungi 119. Jangan menunggu jawaban chatbot.”

The severe-sign wording is a conservative draft informed by the official education sources above. It must be reviewed for clinical appropriateness, Indonesian clarity, the action requested, and regional service availability before patient release. Avoid numerical emergency thresholds, medication doses, oral-treatment instructions, diagnosis labels inferred from symptoms, or a complete “safe/not safe” checklist in this fixed notice.

Recommended acknowledgement labels, also unapproved drafts: **“I understand this service is for education and visit preparation.”** / **“Saya memahami bahwa layanan ini untuk edukasi dan persiapan kunjungan ke dokter.”** Keep the emergency contact action visible before and after acknowledgement. The acknowledgement records understanding; it is not clinical consent, a waiver, a risk score, or evidence that symptoms are safe.

Store the notices in a versioned safety-content bundle with source URLs, source-check date, exact text hashes, language, reviewer identity/qualification, review date, scope, expiry/recheck date, and signed review record. Default to `review_required`; missing, expired, mismatched, or unsigned review records block patient-facing pilot enablement. A developer may prepare and test the draft in internal/demo mode, but must not silently change the status to `approved`. Changes in either language invalidate that language's review, and source changes trigger re-review.

User-selected emergency help may display the fixed notice and route without LLM generation once the bundle is approved. Keyword matching can route obvious phrases for internal tests, but it must not be described as reliable clinical screening or used to reassure users when nothing matches. Patient launch still requires clinician-reviewed routing behavior and testing. No automatic call or claim of help dispatch is recommended.

## Truthful bilingual evidence policy

**Recommendation:** when independent semantic verification is unavailable, disable generated medical paraphrases in **both** languages. A free model, a second prompt to the same model, temperature zero, source identifiers, and a syntactically valid JSON response do not establish semantic correctness. WHO identifies inaccurate/incomplete output and automation bias among generative-health AI risks. [WHO guidance announcement](https://www.who.int/news/item/18-01-2024-who-releases-ai-ethics-and-governance-guidance-for-large-multi-modal-models). This fail-closed policy is an engineering choice; WHO does not prescribe this exact pipeline.

| Mode | Allowed display | Publication condition |
| --- | --- | --- |
| Original-language evidence card | A bounded, exact source excerpt, attribution, access level, population/outcome context and reported values. | Rights eligibility, immutable document version/hash, literal span verification, numeric checks, and an approved patient-education excerpt/topic policy. Exact matching proves extraction fidelity only; use the label **“Source excerpt”**, not “clinically verified answer.” |
| Indonesian card from Indonesian source | The original Indonesian excerpt, clearly identified as original source wording. | Same checks and patient-appropriateness review; do not equate language match with clinical approval. |
| Reviewed translation | Translation tied to the precise original excerpt and its hash. | A recorded qualified bilingual review of meaning, qualifiers, numbers, units, negation, population and uncertainty; always allow viewing the original. Use **“Reviewed translation”**, specifying who reviewed it where appropriate, without claiming authority endorsement. |
| Unreviewed model translation/paraphrase | No clinical translation or paraphrase in the patient answer. | Return fixed UI text: translation is unavailable; offer the original-language source and a clinician-discussion option. The label “AI translation” alone is insufficient for the verified product contract. |
| Generated draft for internal tooling | Draft claims, translations, search terms or formatting suggestions. | Never sent to clinical text, audio, notifications, accessible previews or saved patient answers. Independent semantic verification and final publication gates are required before this mode can become patient-facing. |

English sources therefore remain English when Indonesian translation is unavailable. Indonesian interface text can explain this limitation without translating the medical claim. Offer Indonesian-language sources when available; never substitute an unrelated local passage merely to satisfy a language preference. Source excerpts must not be concatenated into a new inference or personalized recommendation. No eligible excerpt means `insufficient_evidence`, not uncited fallback generation. Unreviewed treatment/dose excerpts stay outside the educational allowlist even when the original source is genuine.

A small pilot can implement useful retrieval and attributed evidence cards without an LLM. This is the recommended baseline if the requested free LLM has no demonstrated independent verifier. It should present **findings reported by sources**, with context and limitations, rather than claim to answer any clinical question accurately. Attributed excerpt mode does not eliminate communication risk or the clinical release gate.

## Necessary checks before patient release

- Clinician approval of the adult-diabetes scope, patient-appropriate excerpt policy, fixed safety notice, routing boundaries and escalation actions.
- Qualified English/Indonesian review of fixed clinical content and each publishable translation; verify numerical and qualifier fidelity separately.
- Tests showing an unapproved/expired safety bundle, unavailable verifier, unsupported translation, or altered source span cannot publish clinical text.
- Review current local source status and permissions; confirm 119 contact presentation on supported iPhones and do not invent response/ambulance guarantees.
- Test emergency-help access without successful model, retrieval, login or acknowledgement completion; test that absent keyword matches never create reassurance.

This report approves no clinical content, verifies no individual patient's condition, and establishes no regulator or ministry endorsement.
