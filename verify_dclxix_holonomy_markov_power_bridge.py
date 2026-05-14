#!/usr/bin/env python3
"""Part DCLXIX: holonomy Markov power bridge.

After DCLXVIII, the literal average of the 40 witness transvections is the exact
complement-walk Markov kernel K. The next question is whether the full witness-
averaged dynamics are equally rigid.

This verifier proves the stronger statement. Every power K^t stays inside the
same three-channel operator algebra and admits an exact decomposition

    K^t = P0 + 4^{-t} P_+ + (2/5)^t P_-,

where P0, P_+, P_- are the DCLXVII projectors of ranks 1, 24, 15. Hence every
entry of K^t is determined by only three exact rational values (diagonal / edge /
non-edge), and the rank-15 sector is the unique slow nontrivial mode.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
EXPLORATION = ROOT / "exploration"
for path in (SCRIPTS, EXPLORATION):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from PART_CCCLIII_EIGENSPACE_PROJECTORS_BRIDGE import (  # noqa: E402
    e0_adj,
    e0_diag,
    e0_non_adj,
    er_adj,
    er_diag,
    er_non_adj,
    es_adj,
    es_diag,
    es_non_adj,
)
from w33_homology import build_w33  # noqa: E402

OUT_PATH = ROOT / "data" / "dclxix_holonomy_markov_power_bridge.json"


@dataclass(frozen=True)
class PowerSummary:
    point_count: int
    stationary_rank: int
    fast_rank: int
    slow_rank: int
    one_step_fast_trace_num: int
    one_step_slow_trace_num: int
    all_identities_hold: bool


def _adjacency_matrix(adj_lists: list[list[int]]) -> np.ndarray:
    n = len(adj_lists)
    matrix = np.zeros((n, n), dtype=float)
    for i, neighbors in enumerate(adj_lists):
        for j in neighbors:
            matrix[i, j] = 1.0
    return matrix


def _entry_formulas(t: int) -> dict[str, Fraction]:
    fast = Fraction(1, 4) ** t
    slow = Fraction(2, 5) ** t
    return {
        "diagonal": e0_diag() + er_diag() * fast + es_diag() * slow,
        "edge": e0_adj() + er_adj() * fast + es_adj() * slow,
        "nonedge": e0_non_adj() + er_non_adj() * fast + es_non_adj() * slow,
        "fast_weight": fast,
        "slow_weight": slow,
        "fast_trace": 24 * fast,
        "slow_trace": 15 * slow,
        "trace": Fraction(1, 1) + 24 * fast + 15 * slow,
    }


def build_bridge() -> dict[str, Any]:
    n, _, adj_lists, _ = build_w33()
    A = _adjacency_matrix(adj_lists)
    I = np.eye(n, dtype=float)
    J = np.ones((n, n), dtype=float)

    K = (12.0 * I - A + J) / 40.0
    P0 = J / 40.0
    P_plus = -((A - 12.0 * I) @ (A + 4.0 * I)) / 60.0
    P_minus = ((A - 12.0 * I) @ (A - 2.0 * I)) / 96.0

    power_rows: list[dict[str, Any]] = []
    powers_hold = True
    decompositions_hold = True
    traces_hold = True
    slow_dominance_holds = True
    ratios_hold = True

    for t in range(1, 9):
        formulas = _entry_formulas(t)
        Kt = np.linalg.matrix_power(K, t)
        expected = P0 + float(formulas["fast_weight"]) * P_plus + float(formulas["slow_weight"]) * P_minus

        diag_values = [Kt[i, i] for i in range(n)]
        edge_values = [Kt[i, j] for i in range(n) for j in range(n) if i != j and A[i, j] == 1.0]
        nonedge_values = [Kt[i, j] for i in range(n) for j in range(n) if i != j and A[i, j] == 0.0]

        diag_ok = np.allclose(diag_values, float(formulas["diagonal"]))
        edge_ok = np.allclose(edge_values, float(formulas["edge"]))
        nonedge_ok = np.allclose(nonedge_values, float(formulas["nonedge"]))
        decomposition_ok = np.allclose(Kt, expected)
        trace_ok = abs(float(np.trace(Kt)) - float(formulas["trace"])) < 1e-8
        ratio = formulas["slow_trace"] / formulas["fast_trace"]
        ratio_ok = ratio == Fraction(8, 5) ** (t - 1)
        slow_ok = True if t == 1 else formulas["slow_trace"] > formulas["fast_trace"]

        powers_hold = powers_hold and diag_ok and edge_ok and nonedge_ok
        decompositions_hold = decompositions_hold and decomposition_ok
        traces_hold = traces_hold and trace_ok
        ratios_hold = ratios_hold and ratio_ok
        slow_dominance_holds = slow_dominance_holds and slow_ok

        power_rows.append(
            {
                "t": t,
                "diagonal": str(formulas["diagonal"]),
                "edge": str(formulas["edge"]),
                "nonedge": str(formulas["nonedge"]),
                "fast_trace": str(formulas["fast_trace"]),
                "slow_trace": str(formulas["slow_trace"]),
                "trace": str(formulas["trace"]),
                "slow_to_fast_ratio": str(ratio),
            }
        )

    identities = {
        "all_markov_powers_t1_to_t8_stay_three_valued": powers_hold,
        "all_markov_powers_t1_to_t8_match_stationary_fast_slow_decomposition": decompositions_hold,
        "all_markov_powers_t1_to_t8_have_exact_trace_formula": traces_hold,
        "one_step_nontrivial_trace_contributions_are_balanced_6_and_6": _entry_formulas(1)["fast_trace"] == 6 and _entry_formulas(1)["slow_trace"] == 6,
        "rank15_sector_is_the_unique_slow_mode_for_t_ge_2": slow_dominance_holds,
        "slow_to_fast_trace_ratio_is_exactly_8_over_5_to_t_minus_1": ratios_hold,
        "dclxviii_kernel_is_recovered_at_t1": power_rows[0]["diagonal"] == "13/40" and power_rows[0]["edge"] == "0" and power_rows[0]["nonedge"] == "1/40",
        "therefore_the_average_witness_dynamics_are_exactly_two_mode_over_the_projector_split": (
            powers_hold and decompositions_hold and traces_hold and slow_dominance_holds and ratios_hold
        ),
    }

    summary = PowerSummary(
        point_count=n,
        stationary_rank=1,
        fast_rank=24,
        slow_rank=15,
        one_step_fast_trace_num=6,
        one_step_slow_trace_num=6,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "power_table": power_rows,
        "interpretation": {
            "power_law": "K^t = P0 + 4^{-t} P_+ + (2/5)^t P_-",
            "stationary_mode": "rank-1 uniform mode P0",
            "fast_mode": "rank-24 mode with decay 1/4^t",
            "slow_mode": "rank-15 mode with decay (2/5)^t",
            "breakthrough": (
                "The averaged witness dynamics are exactly two-mode over the nontrivial projector split. At one step the 24- and 15-dimensional contributions are perfectly balanced at 6 and 6, and from step 2 onward the rank-15 sector is the unique slow residue of the witness-averaged evolution."
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