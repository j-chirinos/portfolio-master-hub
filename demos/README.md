# Demos interactivas del portafolio

Cada demo es una página estática autocontenida (sin CDN ni `fetch`, CSP `default-src 'none'`) que el hub abre en un
modal con `<iframe sandbox="allow-scripts">`. Todo se procesa en el navegador.

| Carpeta | Repo de origen | Motor JS portado de |
|---|---|---|
| `utility-hub/` | jw-solutions-utility-hub | `web/index.html` (sin fixtures de paridad: la lógica no está separada del DOM) |
| `segubot-validator/` | segubot-ocr-agent | `src/validator.py` |
| `ssot-cleaner/` | ssot-data-normalizer | `src/ssot_normalizer/cleaner.py` |
| `sports-simulator/` | v15-sports-predictor | `src/engine/stochastic_model.py` |

## Pruebas de paridad Python ↔ JS

```bash
node demos/run_parity.mjs
```

Cada demo con motor portado delimita el motor con `// ENGINE-START` / `// ENGINE-END`; `parity_test.mjs` lo extrae y lo
compara con `fixtures.json`, generado por el motor Python real. Para regenerar los fixtures (con el `venv` de cada repo):

```powershell
..\04.v15-sports-predictor\venv\Scripts\python.exe -B demos\tools\gen_sports_fixtures.py
..\02.segubot-ocr-agent\venv\Scripts\python.exe -B demos\tools\gen_receipt_fixtures.py
..\03.ssot-data-normalizer\venv\Scripts\python.exe -B demos\tools\gen_ssot_fixtures.py
```

Si cambia el motor Python, regenera los fixtures, ajusta el port JS y vuelve a ejecutar el runner.
Las fuerzas del simulador también van embebidas en `sports-simulator/index.html` (`var DATA`).

## Diferencias conocidas

- `sports-simulator`: el generador pseudoaleatorio no es el de NumPy; solo el cálculo exacto coincide bit a bit.
- `ssot-cleaner`: fechas soportadas = ISO (AAAA-MM-DD) y D/M/A con `/ . -`; pandas admite más formatos.
