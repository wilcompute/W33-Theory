#!/usr/bin/env python3
"""BT1438: g-2 audit calculator for Otto's Moebius-ball electron claim.

The SCIRP HTML exposes the rounded claim g_e = 2.002319 and states that
Equations (49)/(50) give golden-mean representations, but the equation bodies
are image-rendered/omitted in the scraped text.  This calculator therefore
audits only the visible rounded claim, Schwinger's alpha/pi baseline for
Delta g, and formula slots that require manual equation transcription.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1438_gminus2_otto_audit.json"


def main() -> None:
    # Fan, Myers, Sukra, Gabrielse 2023: g/2 = 1.00115965218059(13).
    g_over_2_exp = 1.00115965218059
    g_exp = 2.0 * g_over_2_exp
    delta_g_exp = g_exp - 2.0
    a_exp = delta_g_exp / 2.0

    # Visible rounded claim in Otto abstract.
    otto_g_visible = 2.002319
    otto_delta_g_visible = otto_g_visible - 2.0
    otto_a_visible = otto_delta_g_visible / 2.0

    # Alpha value quoted from the 2023 electron magnetic moment paper's inferred alpha^-1.
    alpha_inv_fan2023 = 137.035999166
    alpha = 1.0 / alpha_inv_fan2023
    schwinger_delta_g = alpha / math.pi
    schwinger_a = alpha / (2.0 * math.pi)

    rows = [
        {
            "model": "Otto visible rounded abstract claim",
            "g": otto_g_visible,
            "delta_g": otto_delta_g_visible,
            "a": otto_a_visible,
            "g_residual": otto_g_visible - g_exp,
            "delta_g_residual": otto_delta_g_visible - delta_g_exp,
            "a_residual": otto_a_visible - a_exp,
            "status": "auditable rounded claim, not a formula derivation",
        },
        {
            "model": "Schwinger one-loop baseline alpha/pi for Delta g",
            "g": 2.0 + schwinger_delta_g,
            "delta_g": schwinger_delta_g,
            "a": schwinger_a,
            "g_residual": schwinger_delta_g - delta_g_exp,
            "delta_g_residual": schwinger_delta_g - delta_g_exp,
            "a_residual": schwinger_a - a_exp,
            "status": "QED leading-order baseline, not Otto-specific",
        },
        {
            "model": "Otto Eq.49 golden-mean representation",
            "g": None,
            "delta_g": None,
            "a": None,
            "g_residual": None,
            "delta_g_residual": None,
            "a_residual": None,
            "status": "requires manual transcription from equation image/PDF",
        },
        {
            "model": "Otto Eq.50 series-expansion representation",
            "g": None,
            "delta_g": None,
            "a": None,
            "g_residual": None,
            "delta_g_residual": None,
            "a_residual": None,
            "status": "requires manual transcription from equation image/PDF",
        },
    ]
    checks = {
        "experimental_g_matches_fan2023_precision_anchor": abs(g_exp - 2.00231930436118) < 1e-14,
        "otto_visible_g_is_rounded": abs(otto_g_visible - 2.002319) < 1e-15,
        "otto_visible_residual_is_about_3e_minus7": abs((otto_g_visible - g_exp) + 3.0436118026e-7) < 1e-16,
        "schwinger_delta_g_is_alpha_over_pi": abs(schwinger_delta_g - alpha / math.pi) < 1e-18,
        "formula_slots_marked_not_transcribed": rows[2]["g"] is None and rows[3]["g"] is None,
    }
    result = {
        "bt": 1438,
        "title": "g-2 audit calculator for Otto Moebius-ball electron claim",
        "verified": all(checks.values()),
        "experimental_anchor": {
            "source": "Fan-Myers-Sukra-Gabrielse 2023 electron magnetic moment measurement",
            "g_over_2": g_over_2_exp,
            "g": g_exp,
            "delta_g": delta_g_exp,
            "a_e": a_exp,
            "alpha_inverse_inferred": alpha_inv_fan2023,
        },
        "audit_rows": rows,
        "decision": "The visible rounded claim is close at 3.04e-7 in g, but equations (49)/(50) must be transcribed before Otto-specific formula accuracy can be credited.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1438, "verified": result["verified"], "otto_g_residual": rows[0]["g_residual"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
