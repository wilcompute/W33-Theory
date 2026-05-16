#!/usr/bin/env python3
"""Part DCCLV: octahedral transition-mixing bridge.

Builds on DCCLI-DCCLIV by deriving an exact modal formula for powers of the
simple random-walk transition operator on the octahedral phase space.

With Laplacian-spectrum projectors (P0, P4, P6) and transition matrix
    P = I - L/4,
its eigenvalues are {1, 0, 0, 0, -1/2, -1/2}. Hence for t >= 1,
    P^t = P0 + (-1/2)^t P6,
since the P4 component is annihilated after one step.

This gives an exact convergence law to the uniform stationary distribution.
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

from verify_dccli_octahedral_spectral_projector_semigroup_bridge import build_bridge as build_dccli

OUT_PATH = ROOT / "data" / "dcclv_octahedral_transition_mixing_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    vertex_count: int
    stationary_mass_per_vertex: float
    second_abs_eigenvalue: float
    first_step_tv_distance: float
    mixing_ratio: float
    all_identities_hold: bool


def as_matrix(a: list[list[float]]) -> np.ndarray:
    return np.array(a, dtype=float)


def to_list(a: np.ndarray, digits: int = 12) -> list[list[float]]:
    return np.round(a, decimals=digits).tolist()


def build_bridge() -> dict[str, Any]:
    dccli = build_dccli()
    P0 = as_matrix(dccli["projectors"]["P0"])
    P4 = as_matrix(dccli["projectors"]["P4"])
    P6 = as_matrix(dccli["projectors"]["P6"])

    n = P0.shape[0]
    I = np.eye(n)
    L = 4 * P4 + 6 * P6
    P = I - 0.25 * L

    evals = np.linalg.eigvals(P)
    evals = np.real_if_close(evals, tol=1e-10).astype(float)
    evals_sorted = np.sort(evals)[::-1]

    powers_direct = {}
    powers_modal = {}
    for t in range(0, 9):
        direct = np.linalg.matrix_power(P, t)
        if t == 0:
            modal = I
        else:
            modal = P0 + ((-0.5) ** t) * P6
        powers_direct[str(t)] = direct
        powers_modal[str(t)] = modal

    pi = np.ones(n) / n
    tv_by_start = {}
    for t in range(1, 9):
        M = powers_direct[str(t)]
        tvs = []
        for i in range(n):
            row = M[i, :]
            tv = 0.5 * float(np.sum(np.abs(row - pi)))
            tvs.append(tv)
        tv_by_start[str(t)] = tvs

    mean_tv = {k: float(np.mean(v)) for k, v in tv_by_start.items()}
    ratio = {str(t): mean_tv[str(t + 1)] / mean_tv[str(t)] for t in range(1, 8)}

    # exact geometric constant from t=1 onward
    c = mean_tv["1"] * 2.0
    closed_form_tv = {str(t): c * (0.5 ** t) for t in range(1, 9)}

    identities = {
        "transition_rows_sum_to_one": np.allclose(P.sum(axis=1), 1.0, atol=1e-12),
        "stationary_distribution_is_uniform": np.allclose(pi @ P, pi, atol=1e-12),
        "transition_spectrum_is_1_0_0_0_-half_-half": np.allclose(np.sort(evals), np.array([-0.5, -0.5, 0.0, 0.0, 0.0, 1.0]), atol=1e-10),
        "power_modal_formula_holds_for_t_ge_1": all(
            np.allclose(powers_direct[str(t)], powers_modal[str(t)], atol=1e-10)
            for t in range(1, 9)
        ),
        "p4_mode_is_annihilated_after_one_step": np.allclose(P @ P4, 0, atol=1e-12),
        "total_variation_is_vertex_symmetric": all(
            np.allclose(vals, vals[0], atol=1e-10) for vals in tv_by_start.values()
        ),
        "tv_distance_decays_by_exact_factor_half": all(
            abs(ratio[str(t)] - 0.5) < 1e-8 for t in range(1, 8)
        ),
        "tv_distance_matches_closed_form": all(
            abs(mean_tv[str(t)] - closed_form_tv[str(t)]) < 1e-8 for t in range(1, 9)
        ),
    }

    summary = BridgeSummary(
        vertex_count=n,
        stationary_mass_per_vertex=1.0 / n,
        second_abs_eigenvalue=0.5,
        first_step_tv_distance=mean_tv["1"],
        mixing_ratio=0.5,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "transition_definition": {
            "operator": "P = I - L/4",
            "spectrum": "{1,0,0,0,-1/2,-1/2}",
            "power_formula": "P^t = P0 + (-1/2)^t P6 for t>=1",
            "stationary_distribution": "uniform on 6 vertices",
        },
        "operators": {
            "P": to_list(P),
            "P0": to_list(P0),
            "P4": to_list(P4),
            "P6": to_list(P6),
        },
        "power_checks": {
            str(t): {
                "direct": to_list(powers_direct[str(t)]),
                "modal": to_list(powers_modal[str(t)]),
            }
            for t in range(0, 9)
        },
        "mixing_profile": {
            "tv_by_start": {k: [round(x, 12) for x in v] for k, v in tv_by_start.items()},
            "mean_tv": {k: round(v, 12) for k, v in mean_tv.items()},
            "ratio": {k: round(v, 12) for k, v in ratio.items()},
            "closed_form": {k: round(v, 12) for k, v in closed_form_tv.items()},
        },
        "bridge_claim": {
            "exact_layer": (
                "Octahedral closure random-walk powers obey exact modal law P^t=P0+(-1/2)^tP6 (t>=1), forcing vertex-symmetric total-variation decay by an exact factor 1/2 per step."
            ),
            "conditional_layer": (
                "Interpreting this finite mixing law as continuum relaxation requires a scaling-limit theorem."
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
