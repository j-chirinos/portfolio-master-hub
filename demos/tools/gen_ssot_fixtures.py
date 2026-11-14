"""Regenera demos/ssot-cleaner/fixtures.json con el pipeline Python real de 03.ssot-data-normalizer.

Uso (con el intérprete del venv del repo 03):
    03.ssot-data-normalizer\\venv\\Scripts\\python.exe -B demos\\tools\\gen_ssot_fixtures.py
Las fechas de 2 dígitos dependen del año actual (ventana de ±50 años de dateutil): el año de ejecución
se guarda en `current_year` y el test JS lo usa como referencia.
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "03.ssot-data-normalizer" / "src"))

import pandas as pd  # noqa: E402
from ssot_normalizer.cleaner import ColumnRule, Schema, SchemaError, clean  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "ssot-cleaner" / "fixtures.json"


def rule(name: str, dtype: str, required: bool = False, key: bool = False, case: str = "keep", aliases: list[str] | None = None) -> dict[str, Any]:
    return {"name": name, "dtype": dtype, "required": required, "key": key, "case": case, "aliases": aliases or []}


def run(columns: list[str], rows: list[list[Any]], rules: list[dict[str, Any]]) -> dict[str, Any]:
    df = pd.DataFrame(rows, columns=columns, dtype="object") if rows else pd.DataFrame({c: [] for c in columns}, dtype="object")
    try:
        schema = Schema(columns=tuple(ColumnRule(r["name"], r["dtype"], r["required"], r["key"], r["case"], tuple(r["aliases"])) for r in rules))
        out, report = clean(df, schema)
    except SchemaError as exc:
        return {"error": str(exc)}
    data: list[list[Any]] = []
    for _, row in out.iterrows():
        values: list[Any] = []
        for r in rules:
            v = row[r["name"]]
            if v is pd.NA or (not isinstance(v, str) and pd.isna(v)):
                values.append(None)
            elif r["dtype"] == "date":
                values.append(v.strftime("%Y-%m-%d"))
            elif r["dtype"] == "int":
                values.append(int(v))
            elif r["dtype"] == "float":
                values.append(float(v))
            elif r["dtype"] == "bool":
                values.append(bool(v))
            else:
                values.append(str(v))
        data.append(values)
    return {"columns": [r["name"] for r in rules], "rows": data, "report": report.to_dict()}


cases: list[dict[str, Any]] = []


def add(name: str, columns: list[str], rows: list[list[Any]], rules: list[dict[str, Any]]) -> None:
    cases.append({"name": name, "columns": columns, "rows": rows, "rules": rules, "expected": run(columns, rows, rules)})


demo_rules = [
    rule("id", "int", True, True), rule("name", "string", True, False, "title", ["Nombre Completo"]),
    rule("amount", "float", aliases=["Monto (Bs)"]), rule("date", "date", aliases=["Fecha"]), rule("active", "bool", aliases=["Activo"]),
]
demo_rows = [
    ["1", "  juan   pérez ", "Bs. 1.234,56", "15/03/2025", "Sí", "x"], ["2", "MARÍA lópez", "1,234.56", "2025-03-15", "no", "x"],
    ["3", "N/A", "$25", "5-4-25", "si", "x"], ["4", "carlos o'neil", "abc", "31/02/2025", "maybe", "x"],
    ["2", "duplicada maría", "10", "01/01/2024", "1", "x"], ["3.5", "ana", "1.234", "x", "falso", "x"],
    ["2.0", "luis", "", "", "", ""], ["", "sin id", "5", "01/01/2024", "true", ""], ["7", "-", "-", "S/D", "N/D", "x"],
]
add("readme_demo", ["ID", "Nombre Completo", "Monto (Bs)", "Fecha", "Activo", "Observaciones"], demo_rows, demo_rules)
add("sin_clave_dedupe_filas", ["a", "b"], [["x", "1"], ["x", "1"], ["y", "2"], ["x", "1"]], [rule("a", "string"), rule("b", "int")])
add("case_upper_lower_keep", ["u", "l", "k"], [["abc Def", "ABC dEf", "aBc dEf"], ["n/a", "NULL", "  s/d "]],
    [rule("u", "string", case="upper"), rule("l", "string", case="lower"), rule("k", "string")])
add("opcional_ausente", ["id"], [["1"], ["2"]], [rule("id", "int", True, True), rule("extra", "string"), rule("when", "date")])
add("tipos_nativos", ["id", "v", "ok", "name"], [[1, 2.5, True, "a"], [2, None, False, None], [3, "7,5", 1, 5], [None, 1, 0, "z"]],
    [rule("id", "int", True, True), rule("v", "float"), rule("ok", "bool"), rule("name", "string", case="title")])
add("alias_acentos", ["Número de Teléfono", "  PAÍS  "], [["0414", "ve"], ["0424", "co"]],
    [rule("telefono", "string", aliases=["Número de Teléfono"]), rule("pais", "string", case="upper", aliases=["País"])])
add("fechas_dmy", ["d"], [["01/02/2024 10:30"], ["1.2.2024"], ["13/01/2024"], ["01/13/2024"], ["31-12-99"], ["15/06/45"], ["15/06/69"],
    ["2024-02-29"], ["2023-02-29"], ["32/01/2024"], ["13/13/2024"], ["2024-01-05T08:00:00"]], [rule("d", "date")])
add("numeros", ["n", "i"], [["Bs. 1.234.567,89", "1.000"], ["1,5", "1,000"], ["-12,5", "+7"], ["12.345,6", "1e3"], ["1.2.3", "3,0"],
    ["$ 0,50", "12abc"], ["  ", "-"], ["5.", "007"]], [rule("n", "float"), rule("i", "int")])
add("vacio", ["a"], [], [rule("a", "string")])
add("err_faltan_obligatorias", ["x"], [["1"]], [rule("id", "int", True)])
add("err_duplicado_destino", ["ID", "id"], [["1", "2"]], [rule("id", "int")])
add("err_alias_duplicados", ["Nombre", "Nombre Completo"], [["a", "b"]], [rule("name", "string", aliases=["Nombre", "Nombre Completo"])])
add("err_esquema_duplicado", ["a"], [["1"]], [rule("a", "string"), rule("a", "int")])

OUT.write_text(json.dumps({"cases": cases, "current_year": datetime.date.today().year}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(f"{len(cases)} casos -> {OUT}")
