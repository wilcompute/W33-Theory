"""Pass 72 Track I: Koide lepton hierarchy verification.

Constructs a W(3,3)-derived toy lepton mass hierarchy from spectral ratios and
evaluates the Koide functional.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main() -> None:
    k, r, s = 12.0, 2.0, -4.0

    m_e = 1.0
    m_mu = (k / abs(s)) ** 2
    m_tau = ((k + abs(s)) / r) ** 2

    sqrt_sum = math.sqrt(m_e) + math.sqrt(m_mu) + math.sqrt(m_tau)
    koide_q = (m_e + m_mu + m_tau) / (sqrt_sum ** 2)
    target = 2.0 / 3.0

    payload = {
        "track": "I",
        "title": "W33 Koide hierarchy verification",
        "spectral_parameters": {"k": k, "r": r, "s": s},
        "toy_masses": {
            "m_e": m_e,
            "m_mu": m_mu,
            "m_tau": m_tau,
        },
        "koide_Q": koide_q,
        "target_2_over_3": target,
        "absolute_error": abs(koide_q - target),
        "relative_error": abs(koide_q - target) / target,
        "reference": "Supplement V (Koide Lepton Hierarchy)"
    }

    Path("w33_pass72_trackI_koide_formula.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
