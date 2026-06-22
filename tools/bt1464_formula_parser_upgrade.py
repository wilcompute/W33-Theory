#!/usr/bin/env python3
"""BT1464: upgraded formula parser for transcribed Otto worksheet rows."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "bt1458_otto_formula_transcription_worksheet.csv"
OUT = ROOT / "data" / "bt1464_formula_parser_upgrade.json"

PHI = (math.sqrt(5.0) - 1.0) / 2.0
ALPHA_INV = 137.035999166
ALPHA = 1.0 / ALPHA_INV
G_OVER_2 = 1.00115965218059
G = 2.0 * G_OVER_2
DELTA_G = G - 2.0
A_E = G_OVER_2 - 1.0
SCHWINGER = ALPHA / math.pi
RATIO_12_13 = 12.0 / 13.0

ALIASES = {
    "phi": PHI,
    "Phi": 1.0 / PHI,
    "phi5": PHI**5,
    "Phi5": (1.0 / PHI) ** 5,
    "alpha": ALPHA,
    "alpha_inv": ALPHA_INV,
    "g": G,
    "g_over_2": G_OVER_2,
    "delta_g": DELTA_G,
    "Delta_g": DELTA_G,
    "a_e": A_E,
    "Schwinger": SCHWINGER,
    "ratio_12_13": RATIO_12_13,
    "sqrt": math.sqrt,
    "pi": math.pi,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "exp": math.exp,
    "pow": pow,
    "abs": abs,
}
TARGETS = {
    "g_over_2": G_OVER_2,
    "delta_g": DELTA_G,
    "a_e": A_E,
    "Schwinger": SCHWINGER,
    "ratio_12_13": RATIO_12_13,
}


def evaluate(expr: str) -> float:
    return float(eval(expr, {"__builtins__": {}}, ALIASES))


def classify(value: float) -> dict[str, float | str]:
    residuals = {name: abs(value - target) for name, target in TARGETS.items()}
    nearest = min(residuals, key=residuals.get)
    return {"nearest_target": nearest, "nearest_abs_residual": residuals[nearest], "residuals": residuals}


def main() -> None:
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    demo_exprs = {
        "ratio_alias": "ratio_12_13",
        "schwinger_alias": "Schwinger",
        "quartic_coefficient": "4-phi**2",
        "quartic_square": "(4-phi**2)**2",
        "delta_g_alias": "delta_g",
    }
    demos = {}
    for name, expr in demo_exprs.items():
        value = evaluate(expr)
        demos[name] = {"expr": expr, "value": value, **classify(value)}
    parsed_rows = []
    for row in rows:
        expr = (row.get("transcribed_formula") or "").strip()
        parsed = {"equation": int(row["equation"]), "status": "blocked_blank_formula", "expr": expr}
        if expr:
            try:
                value = evaluate(expr)
                parsed.update({"status": "evaluated", "value": value, **classify(value)})
            except Exception as exc:
                parsed.update({"status": "eval_error", "error": str(exc)})
        parsed_rows.append(parsed)
    checks = {
        "aliases_include_requested_symbols": all(k in ALIASES for k in ["Phi", "phi5", "delta_g", "a_e", "Schwinger", "ratio_12_13"]),
        "demo_ratio_classifies_to_ratio": demos["ratio_alias"]["nearest_target"] == "ratio_12_13",
        "demo_schwinger_classifies_to_schwinger": demos["schwinger_alias"]["nearest_target"] == "Schwinger",
        "demo_delta_g_classifies_to_delta_g": demos["delta_g_alias"]["nearest_target"] == "delta_g",
        "worksheet_rows_loaded": [int(r["equation"]) for r in rows] == [49, 50, 64, 65, 66],
        "blank_rows_still_blocked": all(r["status"] == "blocked_blank_formula" for r in parsed_rows),
    }
    result = {
        "bt": 1464,
        "title": "Formula parser upgrade",
        "verified": all(checks.values()),
        "aliases": {k: v for k, v in ALIASES.items() if isinstance(v, (int, float))},
        "targets": TARGETS,
        "demo_evaluations": demos,
        "parsed_rows": parsed_rows,
        "interpretation": "Worksheet formulas may now use aliases Phi, phi5, delta_g, a_e, Schwinger, and ratio_12_13; evaluated rows are auto-classified by nearest target.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1464, "verified": result["verified"], "aliases": len(result["aliases"])}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
