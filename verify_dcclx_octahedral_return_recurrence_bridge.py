#!/usr/bin/env python3
"""Part DCCLX: octahedral return/recurrence bridge.

Builds on DCCLV-DCCLIX by extracting exact return-probability and recurrence
laws for the same octahedral random walk.

From the exact power law (t>=1)
    P^t = P0 + (-1/2)^t P6,
with diagonal entries P0_ii=1/6 and P6_ii=1/3, we get
    p_t(i,i) = 1/6 + (1/3)(-1/2)^t,  t>=1,
    p_0(i,i)=1.

This verifier also proves mean return time E_i[T_i^+] = 6 (Kac law for uniform
pi_i=1/6) and checks the closed generating function for returns.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccli_octahedral_spectral_projector_semigroup_bridge import build_bridge as build_dccli
from verify_dcclv_octahedral_transition_mixing_bridge import build_bridge as build_dcclv

OUT_PATH = ROOT / "data" / "dcclx_octahedral_return_recurrence_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    stationary_mass: float
    mean_return_time: float
    p1_return: float
    p2_return: float
    p3_return: float
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    dcclv = build_dcclv()
    dccli = build_dccli()

    P = np.array(dcclv["operators"]["P"], dtype=float)
    P0 = np.array(dccli["projectors"]["P0"], dtype=float)
    P6 = np.array(dccli["projectors"]["P6"], dtype=float)

    n = P.shape[0]
    pi = np.ones(n) / n

    # Return probabilities from direct powers and closed form
    direct = []
    closed = []
    for t in range(0, 13):
        Pt = np.linalg.matrix_power(P, t)
        p_ret = float(Pt[0, 0])
        if t == 0:
            p_cl = 1.0
        else:
            p_cl = 1.0 / 6.0 + (1.0 / 3.0) * ((-0.5) ** t)
        direct.append(p_ret)
        closed.append(p_cl)

    # Mean return time by linear system (hitting from non-target states)
    target = 0
    idx = [k for k in range(n) if k != target]
    Q = P[np.ix_(idx, idx)]
    h = np.linalg.solve(np.eye(n - 1) - Q, np.ones(n - 1))
    mean_return_linear = 1.0 + float(np.dot(P[target, idx], h))
    mean_return_kac = 1.0 / pi[target]

    # Return generating function G(z)=sum_{t>=0} p_t z^t
    # Closed form from profile:
    # G(z)=1 + z/(6(1-z)) + (1/3) * [(-z/2)/(1+z/2)]
    z_samples = [0.25, 0.5, 0.8]
    gen_checks = []
    for z in z_samples:
        closed_g = 1.0 + z / (6.0 * (1.0 - z)) + (1.0 / 3.0) * ((-z / 2.0) / (1.0 + z / 2.0))
        partial = 0.0
        for t in range(0, 220):
            partial += direct[t] * (z ** t) if t < len(direct) else float(np.linalg.matrix_power(P, t)[0, 0]) * (z ** t)
        gen_checks.append({
            "z": z,
            "closed_form": closed_g,
            "partial_sum": partial,
            "difference": partial - closed_g,
        })

    identities = {
        "uniform_stationary_mass_is_one_sixth": bool(abs(pi[0] - (1.0 / 6.0)) < 1e-12),
        "p0_return_is_one": bool(abs(direct[0] - 1.0) < 1e-12),
        "closed_return_profile_matches_direct": bool(all(abs(direct[t] - closed[t]) < 1e-12 for t in range(1, 13))),
        "first_return_values_match_profile": bool(
            abs(direct[1] - 0.0) < 1e-12 and abs(direct[2] - 0.25) < 1e-12 and abs(direct[3] - 1.0 / 8.0) < 1e-12
        ),
        "oscillation_around_one_sixth": bool(direct[2] > 1.0 / 6.0 and direct[3] < 1.0 / 6.0 and direct[4] > 1.0 / 6.0),
        "mean_return_linear_equals_kac": bool(abs(mean_return_linear - mean_return_kac) < 1e-10),
        "mean_return_equals_six": bool(abs(mean_return_linear - 6.0) < 1e-10),
        "return_generating_function_matches_closed_form": bool(all(abs(x["difference"]) < 1e-10 for x in gen_checks)),
        "projector_diagonal_constants_hold": bool(np.allclose(np.diag(P0), 1.0 / 6.0, atol=1e-12) and np.allclose(np.diag(P6), 1.0 / 3.0, atol=1e-12)),
    }

    summary = BridgeSummary(
        state_count=n,
        stationary_mass=float(pi[0]),
        mean_return_time=mean_return_linear,
        p1_return=direct[1],
        p2_return=direct[2],
        p3_return=direct[3],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "return_definition": {
            "profile": "p_t(i,i)=1/6 + (1/3)(-1/2)^t for t>=1",
            "kac": "E_i[T_i^+] = 1/pi_i = 6",
            "generating_function": "G(z)=1 + z/(6(1-z)) + (1/3)*((-z/2)/(1+z/2))",
        },
        "return_timeline": [
            {
                "t": t,
                "direct": round(direct[t], 12),
                "closed_form": round(closed[t], 12),
                "difference": round(direct[t] - closed[t], 12),
            }
            for t in range(0, 13)
        ],
        "generating_checks": [
            {
                "z": x["z"],
                "closed_form": round(x["closed_form"], 12),
                "partial_sum": round(x["partial_sum"], 12),
                "difference": round(x["difference"], 12),
            }
            for x in gen_checks
        ],
        "bridge_claim": {
            "exact_layer": (
                "Octahedral closure walk has exact return profile p_t(i,i)=1/6+(1/3)(-1/2)^t (t>=1), exact mean return time 6, and an exact closed return generating function."
            ),
            "conditional_layer": (
                "Interpreting this finite recurrence law as continuum recurrence/Green-resolvent structure requires a scaling-limit theorem."
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
