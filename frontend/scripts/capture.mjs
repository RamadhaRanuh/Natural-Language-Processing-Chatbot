// Capture the running client; never substitute synthetic clinical content.
import { chromium } from "@playwright/test";
import { mkdir } from "node:fs/promises";

await mkdir("../docs/screenshots", { recursive: true });
const browser = await chromium.launch();
for (const [name, width, height] of [["phone", 390, 844], ["desktop", 1440, 1000]]) {
  const page = await browser.newPage({ viewport: { width, height } });
  await page.goto("http://127.0.0.1:3000");
  await page.screenshot({ path: "../docs/screenshots/" + name + ".png", fullPage: true });
  await page.close();
}
await browser.close();
