# Diabetes pilot corpus: rights and provenance audit

Checked 2026-10-03. The bundled `data/evidence/pilot.json` contains **two unreviewed candidate fixtures**, not a clinically approved patient corpus. No medical reviewer or Indonesian translator has approved them. These studies concern care interventions; they do not validate this chatbot. Do not silently convert their results into personalized treatment guidance.

## Sources selected

| Candidate | Primary publication | API identifier | License checked |
| --- | --- | --- | --- |
| ST2EP | [Debussche et al., 2018](https://doi.org/10.1371/journal.pone.0191262) | PMID 29357380; PMC5777645 | CC BY 4.0; explicit license link inside XML permissions |
| Telescot | [Wild et al., 2016](https://doi.org/10.1371/journal.pmed.1002098) | PMID 27458809; PMC4961438 | XML declares CC Attribution; publisher's license link resolves to CC BY 4.0 |

Both are original adult type 2 diabetes randomized trials. Numerical samples, endpoints, estimates, confidence intervals, and exact source locators are in the JSON instead of repeated here. Source passages preserve selected XML text; table cells use visible separators. They are licensed supporting material. The single visible claim excerpt per study is under 25 words and is literally contained in its referenced passage. Titles, authors, primary links and license links must travel with any rendered evidence card; normalized/extracted data must be identified as adapted from the article. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) permits commercial redistribution and adaptation subject to attribution and its other terms. This finding applies to the checked article material, not every linked image, third-party work or raw patient dataset.

## Publication status and blocking issues

The search API returned `isOpenAccess: Y`, `inEPMC: Y`, and `Randomized Controlled Trial` in `pubTypeList.pubType` for both. The ST2EP core record returned no `commentCorrectionList`; neither checked record declared a retraction publication type. These are observations at this date, not proof against later notices.

**ST2EP:** an abstract confidence limit has an inconsistent sign. The fixture's signed within-arm limits come from Table 2, and the standardized effect comes from the Results paragraph. These are distinct measures and must not be combined into an invented between-arm confidence interval. Medical review must address the discrepancy. The endpoint denominators differ from enrollment and are preserved separately.

**Telescot:** both the [publisher page](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002098) and API declare [a correction](https://doi.org/10.1371/journal.pmed.1002163), PMID 27760145 / PMC5070826. The correction, inspected in publisher text and licensed fullTextXML, replaces a duplicated supplementary adverse-events file. Its existence must be visible, and any adverse-events answer must use the corrected supplement. The primary-result table and prose also disagree on the p-value; the fixture does not expose that p-value as a structured result. Review is pending. A publication checker that rejects all declared corrections should decline this candidate rather than remove the warning.

Sources remain candidates even though their redistribution licenses were inspected. Rights access, passage support and clinical applicability are separate checks. English excerpts are unmodified; Indonesian claim strings are `null`, so the app must withhold Indonesian medical claims until their meaning has been checked.

## Documented API and observed wire shape

Use the [Europe PMC Articles REST API](https://europepmc.org/RestfulWebService), with access boundaries described on its [developer page](https://europepmc.org/developers). Full XML was downloaded through the documented service, not scraped from the main archive.

```text
GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A10.1371%2Fjournal.pone.0191262&format=json&resultType=core
GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5777645/fullTextXML
GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4961438/fullTextXML
GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5070826/fullTextXML
```

Observed JSON nesting (selected fields, not a fabricated whole response):

```json
{
  "resultList": {
    "result": [{
      "id": "29357380",
      "source": "MED",
      "pmcid": "PMC5777645",
      "doi": "10.1371/journal.pone.0191262",
      "firstPublicationDate": "2018-01-22",
      "isOpenAccess": "Y",
      "inEPMC": "Y",
      "pubTypeList": {"pubType": ["Research Support, Non-U.S. Gov't", "research-article", "Randomized Controlled Trial", "Journal Article"]}
    }]
  }
}
```

Telescot's `commentCorrectionList.commentCorrection[]` includes an `Erratum in` item with `id: 27760145` and `source: MED`; the correction record reciprocally declares `Erratum for`. Absence of this optional field must not crash a parser. Query each source identifier with `EXT_ID:<pmid> AND SRC:MED`; do not confuse the API `source` field with a full-text PMCID.

Each fixture's `document_hash` is SHA-256 of the downloaded XML bytes, and `publication_status.full_text_url` names that exact endpoint. Supporting `locator` values refer to this document version, using section IDs, paragraph indexes or table paths. A later XML revision should invalidate cached verification until the version and locators are checked again. Numeric units retain their reported meaning: changes in HbA1c expressed in percent are percentage-point changes; mmol/mol remains mmol/mol. Confidence intervals belong to their named measures and populations.

## Initial release boundary

This is enough for retrieval/parser/evidence-card demonstrations and refusal-path tests. It is insufficient for broad diabetes education coverage, personalized advice or a production bilingual answer service. The present fixtures deliberately retain publication problems so the verification gate can demonstrate withholding. Add sources for basic condition explanations and visit questions with individually documented rights; obtain medical and bilingual reviews before enabling patient answers. No approvals or reviewer identities should be filled by an automated process.
