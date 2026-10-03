# What medical role belongs in the patient first release?

Parent: [Plan an evidence-supported medical chatbot for iPhone](../map.md)
Type: grilling
Labels: wayfinder:grilling
Status: resolved
Assignee: codex
Blocked by: 11

## Question

Within the confirmed medical-education and doctor-visit-preparation role, define the first topic coverage, supported patient population, handling of user-reported symptoms, allowed visit-preparation outputs, and scope/escalation boundaries. Use the landscape findings when relevant. Personalized diagnosis and treatment recommendations remain outside the agreed first release; do not reopen that choice without a requested change.

## Comments

- User selected medical education and doctor-visit preparation during charting on 2026-10-02. This fixes the broad role. The ticket remains open to define concrete allowed workflows, medical capability boundaries, and escalation behavior together in a decision session.
- Claimed by Codex on 2026-10-02 for a live grilling/domain-modeling session. Existing audience, market, languages, platform, and accepted source categories remain settled.
- Interview round one asks: focused versus broad topic coverage (and which topics); adult-only versus family/pediatric scope; whether symptom descriptions may be organized for a visit without inferring diagnosis or urgency. Recommendations are proposals, not answers supplied on the user's behalf. Later questions about concrete visit outputs and safety handling depend on these answers.
- Round one response: the user accepted all three recommendations. Confirmed: one-condition pilot (specific condition not selected); adults and caregivers of adults; symptom descriptions may be organized into a user-reviewed visit summary without assigning a diagnosis or urgency score.
- Round two responses: the user chose an editable symptom/concern summary plus questions for the doctor, keeping patient-reported information separate from evidence-based explanations. For diagnosis or medication/dose-change requests, explain the scope boundary, offer supported general information, and help formulate a doctor question; do not issue a personalized diagnosis or medication instruction.
- The topic choice is waiting on a narrow source-readiness check for type 2 diabetes and hypertension. Emergency-interruption behavior has been asked separately and remains pending. No clinical trigger thresholds or emergency contact instructions have been selected.
- Source-readiness research is now resolved. Its provisional recommendation is adult type 2 diabetes; the user still chooses the condition. Remaining interview items: condition choice; explicit minimum age and specialized/pregnancy-advice boundary; emergency-interruption behavior. Clinical trigger rules, safety wording and local contacts are review work rather than medical facts for the user to invent.
- Final scope response on 2026-10-02: the user accepted adult type 2 diabetes, both users and patients aged 18 or older, pregnancy-specific medical advice outside the pilot, and clinician-approved safety interruptions with Indonesia-specific guidance. This completes the live scope exchange.

## Answer

Resolved 2026-10-02 through the user's explicit acceptance across the interview rounds.

### Agreed first-release role

The pilot provides adult type 2 diabetes education and doctor-visit preparation for patients and caregivers. Both app users and the patient whose care is discussed must be 18 or older. Indonesia, English/Indonesian answers, native iPhone plus hosted service, and the previously accepted source categories remain the standing project constraints in the map.

### Allowed workflow

1. A user asks a general adult type 2 diabetes question or supplies symptoms and concerns for a visit.
2. The app provides supported general explanations within that education scope. The detailed evidence-display and withholding contract will be decided separately.
3. For visit preparation, the app organizes reported symptoms, their timing, concerns, and questions for a clinician into an editable summary. The user reviews and corrects it. Patient-reported information remains distinct from added medical explanations; summarizing a symptom does not establish its clinical truth.
4. If asked for a diagnosis or a medication/dose change, explain the education boundary, offer supported general information where appropriate, and help formulate a doctor question. Do not provide a personalized diagnosis or medication instruction.
5. When clinician-approved safety criteria apply, interrupt normal education with clinician-approved, Indonesia-specific safety guidance. This approved safety path does not authorize routine symptom-based urgency scoring. Its actual triggers, wording, local resources, and approval process must be reviewed before deployment; this decision does not claim reliable emergency detection.

### Boundaries

The pilot does not provide personalized diagnosis or treatment recommendations, medication/dose changes, routine urgency scores, pediatric advice, or pregnancy-specific medical advice. It may help organize reported concerns and clinician questions without supplying those excluded conclusions. General medical coverage beyond adult type 2 diabetes is outside this first pilot. A request outside the topic should receive a scope explanation and clinician-question help without expanding medical claims beyond the approved topic.

### Decisions deliberately left to their own tickets

Evidence coverage and abstention rules, local authorities and translations, accounts/retention/export, model/API choices, release metrics and clinical validation remain separate. This ticket does not establish source licenses, corpus completeness, clinical efficacy, legal readiness, or an approved safety policy.

The selected topic makes a focused source-corpus audit specifiable. The accepted safety path also makes its clinical approval and maintenance responsibilities specifiable. These are new dependent tickets; their details do not belong in this role decision.
