// Ejecuta las pruebas de paridad Python <-> JS de todas las demos. Uso: node demos/run_parity.mjs
// Cada demo con motor portado (marcadores ENGINE-START/ENGINE-END) trae fixtures.json (generado por el motor
// Python real, ver demos/tools/) y parity_test.mjs. Código de salida != 0 si alguna falla.
import { spawnSync } from "node:child_process";
import { existsSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const demos = path.dirname(fileURLToPath(import.meta.url));
const suites = readdirSync(demos, { withFileTypes: true })
  .filter((d) => d.isDirectory() && existsSync(path.join(demos, d.name, "parity_test.mjs")))
  .map((d) => d.name)
  .sort();

if (!suites.length) { console.error("No se encontró ninguna prueba de paridad."); process.exit(1); }

let failed = 0;
for (const name of suites) {
  const run = spawnSync(process.execPath, [path.join(demos, name, "parity_test.mjs")], { encoding: "utf8" });
  const ok = run.status === 0;
  if (!ok) { failed++; }
  console.log(`${ok ? "✅" : "❌"} ${name}: ${(run.stdout || "").trim() || (run.stderr || "").trim().split("\n").slice(0, 6).join("\n")}`);
}
console.log(failed ? `\n${failed} de ${suites.length} suites fallaron.` : `\nTodas las suites de paridad pasan (${suites.length}).`);
process.exit(failed ? 1 : 0);
