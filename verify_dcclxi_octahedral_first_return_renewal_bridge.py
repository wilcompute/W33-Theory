#!/usr/bin/env python3
"""Part DCCLXI: octahedral first-return / renewal bridge.

Builds on DCCLX by decomposing return probabilities into first-return events.

Let p_t = P^t(i,i) be return probability and f_t first-return probability.
Renewal identity:
    p_0 = 1,
    p_t = sum_{k=1}^t f_k p_{t-k}   (t>=1).
Generating functions satisfy:
    G(z) = sum_{t>=0} p_t z^t,
    F(z) = sum_{t>=1} f_t z^t,
    G(z) = 1 / (1 - F(z)),
    F(z) = 1 - 1/G(z).

This verifier computes f_t exactly by renewal recursion, checks reconstruction,
and verifies the generating-function identity against DCCLX closed G(z).
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclv_octahedral_transition_mixing_bridge import build_bridge as build_dcclv

OUT_PATH = ROOT / "data" / "dcclxi_octahedral_first_return_renewal_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    f1: float
    f2: float
    f3: float
    first_return_mass: float
    mean_return_from_first_return: float
    all_identities_hold: bool


def compute_return_profile(P: np.ndarray, T: int, start: int = 0) -> list[float]:
    n = P.shape[0]
    mu = np.zeros(n)
    mu[start] = 1.0
    p = [1.0]
    for _ in range(1, T + 1):
        mu = mu @ P
        p.append(float(mu[start]))
    return p


def compute_first_return_from_renewal(p: list[float]) -> list[float]:
    T = len(p) - 1
    f = [0.0] * (T + 1)
    f[0] = 0.0
    for t in range(1, T + 1):
        conv = 0.0
        for k in range(1, t):
            conv += f[k] * p[t - k]
        f[t] = p[t] - conv
    return f


def build_bridge() -> dict[str, Any]:
    dcclv = build_dcclv()
    P = np.array(dcclv["operators"]["P"], dtype=float)
    n = P.shape[0]

    T = 400
    p = compute_return_profile(P, T)
    f = compute_first_return_from_renewal(p)

    # Reconstruction check on finite window
    recon_window = []
    for t in range(1, 81):
        rhs = 0.0
        for k in range(1, t + 1):
            rhs += f[k] * p[t - k]
        recon_window.append({
            "t": t,
            "p_t": p[t],
            "renewal_rhs": rhs,
            "difference": p[t] - rhs,
        })

    # Generating function checks vs DCCLX closed G
    z_samples = [0.25, 0.5, 0.8]
    gen_checks = []
    for z in z_samples:
        G_series = sum(p[t] * (z ** t) for t in range(T + 1))
        F_series = sum(f[t] * (z ** t) for t in range(1, T + 1))
        G_closed = 1.0 + z / (6.0 * (1.0 - z)) + (1.0 / 3.0) * ((-z / 2.0) / (1.0 + z / 2.0))
        F_closed = 1.0 - 1.0 / G_closed
        gen_checks.append(
            {
                "z": z,
                "G_series": G_series,
                "G_closed": G_closed,
                "F_series": F_series,
                "F_closed": F_closed,
                "G_minus_1_over_1_minus_F": G_series - 1.0 / (1.0 - F_series),
            }
        )

    mass = float(sum(f[1:]))
    mean_ret = float(sum(t * f[t] for t in range(1, T + 1)))

    identities = {
        "first_step_return_zero": abs(f[1] - 0.0) < 1e-12,
        "second_step_first_return_is_quarter": abs(f[2] - 0.25) < 1e-12,
        "third_step_first_return_is_eighth": abs(f[3] - 0.125) < 1e-12,
        "renewal_reconstruction_holds_on_window": all(abs(x["difference"]) < 1e-12 for x in recon_window),
        "first_return_probabilities_nonnegative": min(f[1:]) > -1e-12,
        "first_return_total_mass_is_one": abs(mass - 1.0) < 1e-10,
        "mean_return_from_first_return_is_six": abs(mean_ret - 6.0) < 1e-8,
        "generating_function_identity_holds": all(abs(x["G_minus_1_over_1_minus_F"]) < 1e-9 for x in gen_checks),
        "series_matches_closed_forms": all(abs(x["G_series"] - x["G_closed"]) < 1e-9 and abs(x["F_series"] - x["F_closed"]) < 1e-9 for x in gen_checks),
    }

    summary = BridgeSummary(
        state_count=n,
        f1=f[1],
        f2=f[2],
        f3=f[3],
        first_return_mass=mass,
        mean_return_from_first_return=mean_ret,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "renewal_definition": {
            "equation": "p_t = sum_{k=1}^t f_k p_{t-k}",
            "generating": "G = 1/(1-F), F = 1 - 1/G",
            "closed_G": "1 + z/(6(1-z)) + (1/3)*((-z/2)/(1+z/2))",
        },
        "return_profile": [round(x, 12) for x in p[:81]],
        "first_return_profile": [round(x, 12) for x in f[:81]],
        "reconstruction_window": [
            {"t": x["t"], "p_t": round(x["p_t"], 12), "renewal_rhs": round(x["renewal_rhs"], 12), "difference": round(x["difference"], 12)}
            for x in recon_window
        ],
        "generating_checks": [
            {
                "z": x["z"],
                "G_series": round(x["G_series"], 12),
                "G_closed": round(x["G_closed"], 12),
                "F_series": round(x["F_series"], 12),
                "F_closed": round(x["F_closed"], 12),
                "G_minus_1_over_1_minus_F": round(x["G_minus_1_over_1_minus_F"], 12),
            }
            for x in gen_checks
        ],
        "bridge_claim": {
            "exact_layer": (
                "Octahedral closure walk obeys exact renewal decomposition of returns, with first-return mass 1, mean return 6, and exact generating identity G=1/(1-F) matching closed forms."
            ),
            "conditional_layer": (
                "Interpreting this finite renewal law as continuum first-passage renewal structure requires a scaling-limit theorem."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
