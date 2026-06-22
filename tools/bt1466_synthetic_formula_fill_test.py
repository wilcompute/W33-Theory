#!/usr/bin/env python3
"""BT1466: synthetic filled worksheet proving formula-parser classification."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_OUT = ROOT / "data" / "bt1466_synthetic_formula_fill.csv"
JSON_OUT = ROOT / "data" / "bt1466_synthetic_formula_fill_test.json"

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
    "Phi": 1.0 / PHI,
    "phi": PHI,
    "phi5": PHI**5,
    "delta_g": DELTA_G,
    "a_e": A_E,
    "Schwinger": SCHWINGER,
    "ratio_12_13": RATIO_12_13,
    "g_over_2": G_OVER_2,
    "sqrt": math.sqrt,
    "pi": math.pi,
}
TARGETS = {
    "g_over_2": G_OVER_2,
    "delta_g": DELTA_G,
    "a_e": A_E,
    "Schwinger": SCHWINGER,
    "ratio_12_13": RATIO_12_13,
}


def eval_expr(expr: str) -> float:
    return float(eval(expr, {"__builtins__": {}}, ALIASES))


def nearest(value: float) -> tuple[str, float]:
    name = min(TARGETS, key=lambda k: abs(value - TARGETS[k]))
    return name, abs(value - TARGETS[name])


def main() -> None:
    rows = [
        {"equation": 49, "transcribed_formula": "g_over_2", "expected_target": "g_over_2"},
        {"equation": 50, "transcribed_formula": "a_e", "expected_target": "a_e"},
        {"equation": 64, "transcribed_formula": "delta_g", "expected_target": "delta_g"},
        {"equation": 65, "transcribed_formula": "ratio_12_13", "expected_target": "ratio_12_13"},
        {"equation": 66, "transcribed_formula": "Schwinger", "expected_target": "Schwinger"},
        {"equation": 1454, "transcribed_formula": "4-phi**2", "expected_target": "none_quartic_coefficient"},
    ]
    for row in rows:
        value = eval_expr(row["transcribed_formula"])
        target, residual = nearest(value)
        row["value"] = value
        row["nearest_target"] = target
        row["nearest_abs_residual"] = residual
        row["classified_correctly"] = row["expected_target"] == target or row["expected_target"] == "none_quartic_coefficient"
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    checks = {
        "synthetic_rows_written": CSV_OUT.exists() and len(rows) == 6,
        "equation_targets_classify_correctly": all(r["classified_correctly"] for r in rows[:5]),
        "ratio_alias_hits_ratio_target": rows[3]["nearest_target"] == "ratio_12_13" and rows[3]["nearest_abs_residual"] == 0.0,
        "schwinger_alias_hits_schwinger_target": rows[4]["nearest_target"] == "Schwinger" and rows[4]["nearest_abs_residual"] == 0.0,
        "quartic_demo_evaluates": rows[5]["value"] > 3.6 and rows[5]["value"] < 3.7,
    }
    result = {
        "bt": 1466,
        "title": "Synthetic formula fill classification test",
        "verified": all(checks.values()),
        "synthetic_csv": "data/bt1466_synthetic_formula_fill.csv",
        "rows": rows,
        "interpretation": "The formula parser's target-classification logic is verified on synthetic filled rows before any Otto equation body is transcribed.",
        "checks": checks,
    }
    JSON_OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1466, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
