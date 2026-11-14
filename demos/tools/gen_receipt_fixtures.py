"""Regenera demos/segubot-validator/fixtures.json con el validador Python real de 02.segubot-ocr-agent.

Uso (con el intérprete del venv del repo 02):
    02.segubot-ocr-agent\\venv\\Scripts\\python.exe -B demos\\tools\\gen_receipt_fixtures.py
Las fechas de los textos deben ser claramente pasadas (<= 2025) o 2999: no dependen del día de ejecución.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "02.segubot-ocr-agent"))

from src.validator import parse_amount_string, validate_receipt  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "segubot-validator" / "fixtures.json"

AMOUNTS = ["1.234,56", "1,234.56", "1.234.567,89", "150,00", "25.50", "1.234", "500", "", "0,00", "0012,5", "1,5", "12.345,6", "1.2.3", "9999999999,99"]
TEXTS = [
    "BANESCO\nComprobante de transferencia\nFecha: 15/03/2025\nMonto: Bs. 1.234,56\nNro. de Referencia: 0012345678",
    "Banco Mercantil C.A.\nPago Móvil BDV\nFecha 05.11.2024\nImporte 150,00 Bs\nOperación #123456789",
    "Zelle payment\n2025-03-15 14:22\nTotal: $ 25.00\nConfirmación: 55667788",
    "Binance Pay\n15-03-25\nMonto transferido: 1,234.56 USD\nRef. 987654",
    "texto ilegible sin datos",
    "Fecha: 01/01/2999\nMonto: 10,00\nRef: 123456",
    "Fecha: 29/02/2025\nMonto: 10,00\nRef: 123456",
    "Fecha: 29/02/2024\nMonto: 10,00\nRef: 123456",
    "Fecha: 00/01/2025 y 0000-01-01 y 12/12/0000\nMonto: 10,00\nRef: 123456",
    "Monto: 0,00 Total: 50,00\nFecha: 10/10/2020\nReferencia 12 Ref 4455667",
    "Transferencia por Bs. 2.500,75 exitosa 20/01/2023 Nro de operación 000456789012 Banco de Venezuela",
    "BNC Banco Nacional de Crédito\nTotal a pagar: VES 3.000\n2022-12-31\nComprobante No. 77889900",
    "PROVINCIAL BBVA\nVALOR: USD 1,000.50\n31/12/22\nREF NRO: 123456789012345678901",
    "Mercantil\nMONTO Bs 500\n7/3/2021\nCONFIRMACIÓN: #00991122",
    "Monto: -50,00\nBs 75,5\n2020-02-30 11/11/2011\nOperación 4321",
] + [f"Monto: {a}\nFecha: 01/02/2020\nRef: 111222" for a in AMOUNTS]

cases = [{"text": t, "expected": validate_receipt(t).to_dict()} for t in TEXTS]
parse = []
for a in AMOUNTS:
    value = parse_amount_string(a)
    parse.append({"raw": a, "expected": str(value) if value is not None else None})
OUT.write_text(json.dumps({"cases": cases, "parse_amount": parse}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(f"{len(cases)} comprobantes, {len(parse)} montos -> {OUT}")
