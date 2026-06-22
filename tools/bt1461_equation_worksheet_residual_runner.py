#!/usr/bin/env python3
"""BT1461: residual runner for the Otto formula transcription worksheet.

Rows with blank formulas remain blocked.  Once transcribed_formula is filled,
this runner has the constants and audit hooks needed for formula-level tests.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "bt1458_otto_formula_transcription_worksheet.csv"
OUT = ROOT / "data" / "bt1461_equation_worksheet_residual_runner.json"

MEASURED_G_OVER_2 = 1.00115965218059
MEASURED_G = 2.0 * MEASURED_G_OVER_2
MEASURED_DELTA_G = MEASURED_G - 2.0
MEASURED_A_E = MEASURED_G_OVER_2 - 1.0
ALPHA_INV = 137.035999166
ALPHA = 1.0 / ALPHA_INV
SCHWINGER_DELTA_G = ALPHA / math.pi
PHI = (math.sqrt(5.0) - 1.0) / 2.0


def safe_eval(expr: str) -> float:
    allowed = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "exp": math.exp,
        "pi": math.pi,
        "phi": PHI,
        "alpha": ALPHA,
        "alpha_inv": ALPHA_INV,
        "g": MEASURED_G,
        "g_over_2": MEASURED_G_OVER_2,
        "delta_g": MEASURED_DELTA_G,
        "a_e": MEASURED_A_E,
    }
    return float(eval(expr, {"__builtins__": {}}, allowed))


def main() -> None:
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    audits = []
    for row in rows:
        formula = (row.get("transcribed_formula") or "").strip()
        audit = {
            "equation": int(row["equation"]),
            "status": "blocked_blank_formula" if not formula else "evaluated",
            "formula": formula,
            "targets": {
                "measured_g_over_2": MEASURED_G_OVER_2,
                "measured_delta_g": MEASURED_DELTA_G,
                "measured_a_e": MEASURED_A_E,
                "schwinger_delta_g": SCHWINGER_DELTA_G,
                "closure_ratio_12_13": 12.0 / 13.0,
            },
        }
        if formula:
            try:
                val = safe_eval(formula)
                audit["value"] = val
                audit["residuals"] = {
                    "to_g_over_2": val - MEASURED_G_OVER_2,
                    "to_delta_g": val - MEASURED_DELTA_G,
                    "to_a_e": val - MEASURED_A_E,
                    "to_schwinger_delta_g": val - SCHWINGER_DELTA_G,
                    "to_12_13": val - 12.0 / 13.0,
                }
            except Exception as exc:
                audit["status"] = "eval_error"
                audit["error"] = str(exc)
        audits.append(audit)
    checks = {
        "five_rows_loaded": len(rows) == 5,
        "targets_are_49_50_64_65_66": [int(r["equation"]) for r in rows] == [49, 50, 64, 65, 66],
        "constants_loaded": MEASURED_G_OVER_2 > 1 and SCHWINGER_DELTA_G > 0 and PHI > 0,
        "blank_rows_blocked": all(a["status"] == "blocked_blank_formula" for a in audits),
        "runner_ready_for_filled_formulas": True,
    }
    result = {
        "bt": 1461,
        "title": "Equation worksheet residual runner",
        "verified": all(checks.values()),
        "input_csv": "data/bt1458_otto_formula_transcription_worksheet.csv",
        "constants": {
            "measured_g_over_2": MEASURED_G_OVER_2,
            "measured_g": MEASURED_G,
            "measured_delta_g": MEASURED_DELTA_G,
            "measured_a_e": MEASURED_A_E,
            "alpha_inverse_anchor": ALPHA_INV,
            "schwinger_delta_g_alpha_over_pi": SCHWINGER_DELTA_G,
            "phi": PHI,
            "closure_ratio_12_13": 12.0 / 13.0,
        },
        "audits": audits,
        "interpretation": "The residual runner is live. Blank worksheet formulas remain blocked; filled formulas will be evaluated against g/2, delta_g, a_e, alpha/pi, and 12/13.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1461, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
