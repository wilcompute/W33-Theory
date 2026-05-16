#!/usr/bin/env python3
"""Part DCCLXII: octahedral fundamental-matrix / hitting-time bridge.

Builds on DCCLIV and DCCLXI by expressing exact hitting times through the
ergodic-chain fundamental matrix

    Z = (I - P + Pi)^(-1),    Pi = 1 pi^T,

for octahedral random walk transition P with uniform stationary pi.

For all i,j, mean hitting times satisfy

    H_ij = (Z_jj - Z_ij) / pi_j,

and Kemeny's constant satisfies

    K = sum_j pi_j H_ij = trace(Z) - 1,

independent of i.
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

from verify_dccliv_octahedral_commute_hitting_time_bridge import build_bridge as build_dccliv
from verify_dcclv_octahedral_transition_mixing_bridge import build_bridge as build_dcclv

OUT_PATH = ROOT / "data" / "dcclxii_octahedral_fundamental_matrix_hitting_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    kemeny_constant: float
    trace_z_minus_one: float
    adjacent_hitting_time: float
    antipodal_hitting_time: float
    all_identities_hold: bool


def to_list(a: np.ndarray, digits: int = 12) -> list[list[float]]:
    return np.round(a, decimals=digits).tolist()


def hitting_times_from_transition(P: np.ndarray) -> np.ndarray:
    n = P.shape[0]
    H = np.zeros((n, n), dtype=float)
    I = np.eye(n)
    ones = np.ones(n)
    for target in range(n):
        idx = [k for k in range(n) if k != target]
        Q = P[np.ix_(idx, idx)]
        h = np.linalg.solve(I[np.ix_(idx, idx)] - Q, ones[idx])
        for loc, state in enumerate(idx):
            H[state, target] = h[loc]
        H[target, target] = 0.0
    return H


def build_bridge() -> dict[str, Any]:
    dcclv = build_dcclv()
    dccliv = build_dccliv()

    P = np.array(dcclv["operators"]["P"], dtype=float)
    H_ref = np.array(dccliv["operators"]["hitting_times"], dtype=float)
    adjacent_pairs = [tuple(p) for p in dccliv["pair_orbits"]["adjacent_pairs"]]
    antipodal_pairs = [tuple(p) for p in dccliv["pair_orbits"]["antipodal_pairs"]]

    n = P.shape[0]
    pi = np.ones(n) / n
    Pi = np.ones((n, n)) / n
    I = np.eye(n)

    Z = np.linalg.inv(I - P + Pi)

    # Fundamental-matrix hitting formula
    H_fm = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                H_fm[i, j] = 0.0
            else:
                H_fm[i, j] = (Z[j, j] - Z[i, j]) / pi[j]

    H_direct = hitting_times_from_transition(P)

    # Kemeny row constants via weighted hitting sums
    kemeny_rows = np.array([np.dot(pi, H_fm[i, :]) for i in range(n)], dtype=float)
    kemeny = float(kemeny_rows[0])

    adj_hit = np.array([H_fm[i, j] for i, j in adjacent_pairs], dtype=float)
    opp_hit = np.array([H_fm[i, j] for i, j in antipodal_pairs], dtype=float)

    identities = {
        "fundamental_matrix_inverse_identity": np.allclose((I - P + Pi) @ Z, I, atol=1e-12),
        "hitting_formula_matches_direct_solver": np.allclose(H_fm, H_direct, atol=1e-10),
        "hitting_formula_matches_previous_bridge": np.allclose(H_fm, H_ref, atol=1e-10),
        "adjacent_hitting_time_is_5": np.allclose(adj_hit, 5.0, atol=1e-10),
        "antipodal_hitting_time_is_6": np.allclose(opp_hit, 6.0, atol=1e-10),
        "kemeny_independent_of_start": np.allclose(kemeny_rows, kemeny_rows[0], atol=1e-10),
        "kemeny_equals_13_over_3": abs(kemeny - (13.0 / 3.0)) < 1e-10,
        "kemeny_equals_trace_z_minus_one": abs(kemeny - (float(np.trace(Z)) - 1.0)) < 1e-10,
    }

    summary = BridgeSummary(
        state_count=n,
        kemeny_constant=kemeny,
        trace_z_minus_one=float(np.trace(Z) - 1.0),
        adjacent_hitting_time=float(np.mean(adj_hit)),
        antipodal_hitting_time=float(np.mean(opp_hit)),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "fundamental_definition": {
            "Z": "(I - P + Pi)^(-1)",
            "hitting_formula": "H_ij = (Z_jj - Z_ij)/pi_j",
            "kemeny": "K = sum_j pi_j H_ij = trace(Z)-1",
        },
        "operators": {
            "P": to_list(P),
            "Pi": to_list(Pi),
            "Z": to_list(Z),
            "H_fundamental": to_list(H_fm),
            "H_direct": to_list(H_direct),
        },
        "kemeny_rows": [round(x, 12) for x in kemeny_rows.tolist()],
        "bridge_claim": {
            "exact_layer": (
                "Octahedral closure hitting times are exactly represented by the fundamental matrix Z=(I-P+Pi)^(-1), reproducing all pair values and yielding Kemeny constant K=13/3 via both weighted hitting sums and trace(Z)-1."
            ),
            "conditional_layer": (
                "Interpreting this finite fundamental-matrix law as continuum resolvent/hitting geometry requires a scaling limit."
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
