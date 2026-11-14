"""Regenera demos/sports-simulator/fixtures.json con el motor Python real de 04.v15-sports-predictor.

Uso (con el intérprete del venv del repo 04):
    04.v15-sports-predictor\\venv\\Scripts\\python.exe -B demos\\tools\\gen_sports_fixtures.py
Después, si cambian las fuerzas, actualiza `var DATA = ...` en demos/sports-simulator/index.html.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]  # P004-GitHub_Repositorio-personal
sys.path.insert(0, str(ROOT / "04.v15-sports-predictor"))

from src.engine.stochastic_model import analytic_probabilities, expected_goals, fit_league_model  # noqa: E402
from src.ingestion.data_loader import generate_demo_dataset, normalize_matches  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "sports-simulator" / "fixtures.json"

matches = normalize_matches(generate_demo_dataset(seed=42))
model = fit_league_model(matches)
data = {
    "mu_home": model.mu_home,
    "mu_away": model.mu_away,
    "matches": len(matches),
    "teams": {t: {"attack": s.attack, "defense": s.defense} for t, s in model.strengths.items()},
    "cases": [],
}
for home in model.teams:
    for away in model.teams:
        if home == away:
            continue
        lam_h, lam_a = expected_goals(model, home, away)
        p_h, p_d, p_a = analytic_probabilities(lam_h, lam_a)
        data["cases"].append(
            {"home": home, "away": away, "lam_home": lam_h, "lam_away": lam_a, "p_home": p_h, "p_draw": p_d, "p_away": p_a}
        )
OUT.write_text(json.dumps(data, indent=1), encoding="utf-8", newline="\n")
print(f"{len(data['cases'])} enfrentamientos -> {OUT}")
