#!/usr/bin/env python3
"""Red-team robustness check for the W33 Weinberg correction alpha input.

The earlier note used alpha_hat(MZ)^(-1)=127.930.  A web audit shows that
standard effective QED alpha(MZ^2) evaluations often quote values closer to
128.94-128.96.  This script tests whether the W33 formula depends fragily on
one alpha convention.

Formula:
    sin2_eff = 3/13 + 1/(11 * alpha_inv)

The result remains inside the PDG effective leptonic weak-mixing uncertainty
for the standard alpha(MZ^2) inputs tested here.
"""
from __future__ import annotations
import json
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    x0 = Fraction(3, 13)
    denom = 11
    pdg_sin2 = 0.23148
    pdg_unc = 0.00012
    alpha_inputs = {
        "prior_hat_alpha_input_127p930": {
            "alpha_inv": 127.930,
            "source_note": "Prior internal hat-alpha convention; not used as the sole external anchor."
        },
        "LEP_Bhabha_running_alpha_128p936": {
            "alpha_inv": 128.936,
            "source_note": "LEP running-alpha summary quotes alpha^{-1}(M_Z^2)=128.936 +/- 0.046."
        },
        "KNT2018_alpha_MZ_128p946": {
            "alpha_inv": 128.946,
            "source_note": "Keshavarzi-Nomura-Teubner data-based evaluation quotes alpha^{-1}(M_Z^2)=128.946 +/- 0.015."
        },
        "older_typical_alpha_MZ_128p962": {
            "alpha_inv": 128.962,
            "source_note": "Representative stronger-theory-assumption value quoted in LEP running-alpha literature."
        },
    }
    rows = {}
    ok = True
    for name, item in alpha_inputs.items():
        a_inv = item["alpha_inv"]
        pred = float(x0) + 1.0/(denom*a_inv)
        resid = pred - pdg_sin2
        sigma = resid/pdg_unc
        rows[name] = {
            "alpha_inverse": a_inv,
            "prediction": pred,
            "residual_vs_0p23148": resid,
            "sigma_using_0p00012": sigma,
            "inside_1sigma": abs(sigma) < 1.0,
            "source_note": item["source_note"],
        }
        ok = ok and abs(sigma) < 1.0
    out = {
        "theorem_name": "W33 Weinberg Alpha-Input Robustness Check",
        "all_checks_passed": ok,
        "summary": {
            "formula": "sin2_eff = 3/13 + 1/(11*alpha_inverse)",
            "tree_generator": "3/13",
            "transport_denominator": 11,
            "comparison_value": pdg_sin2,
            "comparison_uncertainty": pdg_unc,
            "range_of_predictions": [min(v["prediction"] for v in rows.values()), max(v["prediction"] for v in rows.values())],
            "max_abs_sigma": max(abs(v["sigma_using_0p00012"]) for v in rows.values()),
        },
        "rows": rows,
        "interpretation": "The W33 correction is not fragile with respect to the alpha(MZ) convention: using standard alpha^{-1}(M_Z^2) values around 128.94 instead of 127.930 still predicts the effective leptonic weak angle within the quoted PDG-scale uncertainty.",
        "boundary": "The formula still requires a derivation of which alpha scheme is correct for the W33 transport action. Until then, the paper should present this as a robustness window rather than a single exact input."
    }
    path = ROOT / "data" / "w33_weinberg_alpha_input_robustness.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(out["summary"], indent=2, sort_keys=True))
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
