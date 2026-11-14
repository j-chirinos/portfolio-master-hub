// Paridad Python <-> JS del validador de comprobantes. Uso: node parity_test.mjs
// fixtures.json lo genera src/validator.py (repo segubot-ocr-agent) sobre un conjunto de textos y montos.
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

const dir = new URL(".", import.meta.url);
const html = readFileSync(new URL("index.html", dir), "utf8");
const fixtures = JSON.parse(readFileSync(new URL("fixtures.json", dir), "utf8"));
const src = html.split("// ENGINE-START")[1].split("// ENGINE-END")[0];
const ENGINE = new Function(src.replace(/^[^\n]*\n/, "") + "; return ENGINE;")();
const TODAY = { y: 2026, m: 11, d: 14 }; // las fechas de los fixtures son claramente pasadas (<=2025) o 2999

for (const { raw, expected } of fixtures.parse_amount) {
  assert.equal(ENGINE.parseAmountString(raw), expected, `parse_amount_string(${JSON.stringify(raw)})`);
}
for (const { text, expected } of fixtures.cases) {
  const got = ENGINE.validateReceipt(text, TODAY);
  const actual = { amount: got.amount, date: got.date, reference: got.reference, bank: got.bank, is_valid: got.is_valid, errors: got.errors };
  assert.deepEqual(actual, expected, `texto: ${JSON.stringify(text)}`);
}
console.log(`OK: ${fixtures.cases.length} comprobantes y ${fixtures.parse_amount.length} montos con paridad exacta Python/JS.`);
