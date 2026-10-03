import { expect, test } from "@playwright/test";

const response = {
  id: "synthetic-answer", status: "ready", language: "en", message: "Synthetic test finding.",
  research_preview: true, notices: ["Synthetic data, not medical evidence."], questions: ["Discuss with your clinician."], safety_url: null,
  claims: [{
    id: "synthetic-claim", source_id: "synthetic-source", text: "Synthetic study result",
    display_language: "en", verification: "source_extract",
    passage: { id: "p", text: "Synthetic study result, not a real medical claim.", locator: "synthetic/table" },
    data: [{ label: "Synthetic count", value: "100", unit: null, passage_id: "p", locator: "synthetic/table" }],
    data_passages: [{ id: "p", text: "Synthetic 100 participants", locator: "synthetic/table" }],
  }],
  sources: [{
    id: "synthetic-source", title: "Synthetic test study", authors: ["Test Researcher"], year: 2020,
    doi: "10.1234/test", pmid: "123", pmcid: "PMC123", url: "https://example.org",
    license: "CC BY", license_url: "https://creativecommons.org/licenses/by/4.0/",
    population: "Synthetic adults", design: "Synthetic design", limitations: ["Not actual evidence."],
    checked_at: "2026-10-03T00:00:00Z", document_hash: "synthetic", copyright_notice: "Synthetic", adaptation_notice: "Test only",
  }],
};

test("adult gate, committed evidence and reset", async ({ page }) => {
  await page.route("**/api/chat", (route) => route.fulfill({ json: response }));
  await page.goto("/");
  const suggestion = page.getByRole("button", { name: /What did diabetes education/ });
  await expect(suggestion).toBeDisabled();
  await page.getByRole("checkbox", { name: /I am 18/ }).check();
  await suggestion.click();
  await expect(page.getByText("Synthetic study result", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: /Inspect evidence/ }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await expect(page.getByText("Synthetic test study")).toBeVisible();
  await expect(page.getByRole("cell", { name: "100", exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Close / Tutup" }).click();
  await page.getByRole("button", { name: /New conversation/ }).click();
  await expect(page.getByText("Synthetic study result", { exact: true })).not.toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBeTruthy();
});

test("Indonesian UI and verbatim reviewed visit summary", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "ID", exact: true }).click();
  await expect(page.locator("html")).toHaveAttribute("lang", "id");
  await page.getByRole("button", { name: /Siapkan kunjungan/ }).click();
  await page.getByLabel("Gejala yang ingin saya diskusikan").fill("User-reported test concern");
  const copy = page.getByRole("button", { name: "Salin ringkasan yang ditinjau" });
  await expect(copy).toBeDisabled();
  await page.getByRole("checkbox", { name: /Saya sudah meninjau/ }).check();
  await expect(copy).toBeEnabled();
  await page.getByText("Pratinjau ringkasan", { exact: true }).click();
  await expect(page.locator("pre")).toContainText("User-reported test concern");
  await page.getByLabel("Gejala yang ingin saya diskusikan").fill("Changed report");
  await expect(copy).toBeDisabled();
});

test("network failure does not appear as a supported answer", async ({ page }) => {
  await page.route("**/api/chat", (route) => route.fulfill({ status: 503, json: { detail: "Unavailable" } }));
  await page.goto("/");
  await page.getByRole("checkbox", { name: /I am 18/ }).check();
  await page.getByRole("button", { name: /What did diabetes education/ }).click();
  await expect(page.getByRole("alert").filter({ hasText: "evidence service" })).toContainText("has not been answered");
  await expect(page.getByRole("button", { name: /Inspect evidence/ })).toHaveCount(0);
});
