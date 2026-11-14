// Paridad Python <-> JS del motor del simulador. Uso: node parity_test.mjs
// fixtures.json lo genera el motor Python (src/engine/stochastic_model.py) con el dataset demo (semilla 42).
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

const dir = new URL(".", import.meta.url);
const html = readFileSync(new URL("index.html", dir), "utf8");
const fixtures = JSON.parse(readFileSync(new URL("fixtures.json", dir), "utf8"));
const engineSrc = html.split("// ENGINE-START")[1].split("// ENGINE-END")[0];
const ENGINE = new Function(engineSrc.replace(/^[^\n]*\n/, "") + "; return ENGINE;")();
const model = { mu_home: fixtures.mu_home, mu_away: fixtures.mu_away, teams: fixtures.teams };
const TOL = 1e-12;
const close = (a, b, msg) => assert.ok(Math.abs(a - b) <= TOL, `${msg}: ${a} vs ${b}`);

for (const c of fixtures.cases) {
  const [lh, la] = ENGINE.expectedGoals(model, c.home, c.away);
  close(lh, c.lam_home, `lam_home ${c.home}-${c.away}`);
  close(la, c.lam_away, `lam_away ${c.home}-${c.away}`);
  const [ph, pd, pa] = ENGINE.analytic(lh, la);
  close(ph, c.p_home, "p_home"); close(pd, c.p_draw, "p_draw"); close(pa, c.p_away, "p_away");
}

const first = fixtures.cases[0];
const a = ENGINE.simulate(model, first.home, first.away, 200000, 42);
const b = ENGINE.simulate(model, first.home, first.away, 200000, 42);
assert.deepEqual(a.matrix, b.matrix, "misma semilla => misma simulación");
close(a.pHome + a.pDraw + a.pAway, 1, "probabilidades suman 1");
close(a.matrix.reduce((x, y) => x + y, 0), 1, "matriz suma 1");
for (const [sim, ex, k] of [[a.pHome, first.p_home, "home"], [a.pDraw, first.p_draw, "draw"], [a.pAway, first.p_away, "away"]]) {
  assert.ok(Math.abs(sim - ex) < 0.01, `simulado vs exacto (${k}): ${sim} vs ${ex}`);
}
assert.throws(() => ENGINE.simulate(model, first.home, first.home, 1000, 1), /distintos/);
assert.throws(() => ENGINE.simulate(model, first.home, first.away, 10, 1), /rango/);
console.log(`OK: ${fixtures.cases.length} enfrentamientos con paridad exacta (tol ${TOL}) + simulación determinista y consistente.`);
