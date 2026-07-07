"""Pass 72 Track H: CKM matrix numerical reconstruction from W(3,3) spectral parameters.

This is a falsifiability-oriented spectral proxy computation that outputs the
three CKM angles and CP phase together with the implied |Vus|, |Vub|, |Vcb|.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main() -> None:
    k, r, s = 12.0, 2.0, -4.0
    spreads = 27
    families = 3
    per_family = 9

    sin_theta_12 = math.sqrt(r / k)
    theta_12 = math.degrees(math.asin(sin_theta_12))

    sin_theta_13 = 1.0 / (spreads - families)
    theta_13 = math.degrees(math.asin(sin_theta_13))

    sin_theta_23 = math.sqrt(per_family / spreads) / 8.0
    theta_23 = math.degrees(math.asin(sin_theta_23))

    delta_cp = -math.degrees(math.atan2(abs(s), k + r))

    Vus = sin_theta_12
    Vub = sin_theta_13
    Vcb = sin_theta_23

    pdg = {
        "Vus": 0.2245,
        "Vub": 0.00382,
        "Vcb": 0.0411,
    }

    payload = {
        "track": "H",
        "title": "W33 CKM spectral reconstruction",
        "spectral_parameters": {"k": k, "r": r, "s": s},
        "spread_decomposition": {"total_spreads": spreads, "families": families, "per_family": per_family},
        "angles_deg": {
            "theta_12": theta_12,
            "theta_13": theta_13,
            "theta_23": theta_23,
            "delta_CP": delta_cp,
        },
        "ckm_moduli": {
            "Vus": Vus,
            "Vub": Vub,
            "Vcb": Vcb,
        },
        "pdg_2024": pdg,
        "absolute_errors": {
            "Vus": abs(Vus - pdg["Vus"]),
            "Vub": abs(Vub - pdg["Vub"]),
            "Vcb": abs(Vcb - pdg["Vcb"]),
        },
        "reference": "BREAKTHROUGH_BT692_CKM_ANGLES.md",
        "falsifiability": "Direct comparison against PDG moduli; large deviations reject the proxy mapping."
    }

    Path("w33_pass72_trackH_ckm_matrix.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
