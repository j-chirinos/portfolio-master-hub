// Paridad Python <-> JS del pipeline de limpieza. Uso: node parity_test.mjs
// fixtures.json lo genera ssot_normalizer.cleaner.clean (repo ssot-data-normalizer) sobre tablas con casos límite.
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

const dir = new URL(".", import.meta.url);
const html = readFileSync(new URL("index.html", dir), "utf8");
const fixtures = JSON.parse(readFileSync(new URL("fixtures.json", dir), "utf8"));
const src = html.split("// ENGINE-START")[1].split("// ENGINE-END")[0];
const ENGINE = new Function(src.replace(/^[^\n]*\n/, "") + "; return ENGINE;")();

for (const c of fixtures.cases) {
  let got;
  try {
    const r = ENGINE.clean({ columns: c.columns, rows: c.rows }, c.rules, { currentYear: fixtures.current_year });
    got = { columns: r.columns, rows: r.rows, report: r.report };
  } catch (e) {
    assert.equal(e.name, "SchemaError", `${c.name}: error inesperado ${e.stack}`);
    got = { error: e.message };
  }
  assert.deepEqual(got, c.expected, `caso ${c.name}`);
}
console.log(`OK: ${fixtures.cases.length} casos con paridad exacta Python/JS (año de referencia ${fixtures.current_year}).`);
