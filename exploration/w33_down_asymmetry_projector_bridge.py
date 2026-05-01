"""Projector/closure-count explanation of the real up/down asymmetry.

The canonical real dressings in the paper packet are

    up   : 3/37 = q/(v-q),
    down : 1/14 = 1/(2 Phi_6).

Their difference looks arbitrary at first glance, but it has an exact count
decomposition:

    1/14 - 3/37 = -5/(14*37) = -(mu+1)/(2 Phi_6 * (v-q)).

This module ties that ``5`` back to the actual right-handed projector packet
and to the slot-independent closure labels. The saved l6/V4 summaries already
show that the canonical closure matrix is

    [[AB, I, A],
     [AB, I, A],
     [ A, B, 0]]

so it contains exactly

    3 copies of A,
    5 non-A nonzero labels {AB, AB, I, I, B}.

For the down-side clean channel Hbar_2, the exact V4 projector theorem gives

    (++): rank 4   (inactive support),
    (-+): rank 1   (the singled down state d_c_1),
    (+-): rank 3   (the active triplet d_c_2,d_c_3,e_c),
    (--): rank 0.

So the real up/down asymmetry admits one exact operator-side reading:

    - the up real dressing uses the triality-triplet count 3 over the cyclic
      shell v-q = 37;
    - the down real dressing differs from that by an exact (4+1)-correction
      over dim(G2) * (v-q), where 4+1 is the Hbar_2 inactive-plus-singled packet.

So the same exact ``3`` vs ``5`` split appears in two independent native
descriptions:

    - closure labels: 3 copies of A versus 5 complementary nonzero labels;
    - projectors: 3 active-triplet states versus 4+1 inactive-plus-singled.

This does not by itself prove the full dynamical selection principle, but it is
the first exact operator-count explanation of why the two real dressings are
different.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

try:
    from exploration.w33_bridge_inputs import load_bridge_json
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from w33_bridge_inputs import load_bridge_json


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_down_asymmetry_projector_bridge_summary.json"
PROJECTOR_SUMMARY_PATH = DATA_DIR / "w33_l6_v4_projector_bridge_summary.json"
CLOSURE_SUMMARY_PATH = DATA_DIR / "w33_l6_v4_closure_selection_bridge_summary.json"


Q = Fraction(3, 1)
V = Fraction(40, 1)
PHI6 = Fraction(7, 1)
MU = Fraction(4, 1)

UP_REAL = Q / (V - Q)
DOWN_REAL = Fraction(1, 1) / (2 * PHI6)
REAL_DIFFERENCE = DOWN_REAL - UP_REAL
PROJECTOR_CORRECTION = -(MU + 1) / ((2 * PHI6) * (V - Q))


def _frac(value: Fraction) -> str:
    return str(value)


def _load_json(path: Path) -> dict[str, Any]:
    return load_bridge_json(path.name, path.parent)


def _count_labels(matrix: list[list[str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in matrix:
        for label in row:
            counts[label] = counts.get(label, 0) + 1
    return counts


def build_summary() -> dict[str, Any]:
    projector = _load_json(PROJECTOR_SUMMARY_PATH)
    closure = _load_json(CLOSURE_SUMMARY_PATH)

    hbar2 = projector["slot_profiles"]["Hbar_2"]["projectors"]
    inactive_rank = hbar2["++"]["rank"]
    singled_rank = hbar2["-+"]["rank"]
    triplet_rank = hbar2["+-"]["rank"]
    closure_matrix = closure["slot_profiles"]["Hbar_2"]["canonical_label_matrix"]
    label_counts = _count_labels(closure_matrix)
    a_count = label_counts.get("A", 0)
    non_a_nonzero_count = sum(
        count for label, count in label_counts.items() if label not in {"A", "0"}
    )

    return {
        "canonical_real_dressings": {
            "up": _frac(UP_REAL),
            "down": _frac(DOWN_REAL),
            "difference": _frac(REAL_DIFFERENCE),
        },
        "count_dictionary": {
            "q": _frac(Q),
            "v_minus_q": _frac(V - Q),
            "dim_g2": _frac(2 * PHI6),
            "mu_plus_1": _frac(MU + 1),
        },
        "closure_label_matrix": {
            "matrix": closure_matrix,
            "label_counts": label_counts,
            "a_count": a_count,
            "non_a_nonzero_count": non_a_nonzero_count,
            "non_a_nonzero_labels": [
                label
                for row in closure_matrix
                for label in row
                if label not in {"A", "0"}
            ],
        },
        "hbar2_projector_ranks": {
            "inactive_plus_plus_rank": inactive_rank,
            "singled_minus_plus_rank": singled_rank,
            "active_triplet_plus_minus_rank": triplet_rank,
            "vanishing_minus_minus_rank": hbar2["--"]["rank"],
        },
        "derived_identity": {
            "up_equals_triality_triplet_over_cyclic_shell": _frac(
                Fraction(triplet_rank, 1) / (V - Q)
            ),
            "up_equals_a_label_count_over_cyclic_shell": _frac(
                Fraction(a_count, 1) / (V - Q)
            ),
            "down_minus_up_equals_minus_inactive_plus_singled_over_dim_g2_times_cyclic_shell": _frac(
                -Fraction(inactive_rank + singled_rank, 1) / ((2 * PHI6) * (V - Q))
            ),
            "down_minus_up_equals_minus_non_a_nonzero_label_count_over_dim_g2_times_cyclic_shell": _frac(
                -Fraction(non_a_nonzero_count, 1) / ((2 * PHI6) * (V - Q))
            ),
            "projector_correction_exact_formula": _frac(PROJECTOR_CORRECTION),
        },
        "down_asymmetry_projector_theorem": {
            "up_real_dressing_is_exactly_triality_triplet_over_cyclic_shell": (
                UP_REAL == Fraction(triplet_rank, 1) / (V - Q)
            ),
            "up_real_dressing_is_exactly_a_label_count_over_cyclic_shell": (
                UP_REAL == Fraction(a_count, 1) / (V - Q)
            ),
            "down_minus_up_is_exactly_minus_mu_plus_one_over_dim_g2_times_cyclic_shell": (
                REAL_DIFFERENCE == PROJECTOR_CORRECTION
            ),
            "the_mu_plus_one_correction_equals_the_hbar2_inactive_plus_singled_rank_4_plus_1": (
                inactive_rank + singled_rank == int(MU + 1)
            ),
            "the_mu_plus_one_correction_equals_the_non_a_nonzero_label_count": (
                non_a_nonzero_count == int(MU + 1)
            ),
            "the_triality_triplet_count_equals_the_a_label_count": (
                a_count == triplet_rank
            ),
            "the_real_up_down_asymmetry_has_an_exact_operator_count_reading": (
                UP_REAL == Fraction(triplet_rank, 1) / (V - Q)
                and REAL_DIFFERENCE
                == -Fraction(inactive_rank + singled_rank, 1) / ((2 * PHI6) * (V - Q))
                and a_count == triplet_rank
                and non_a_nonzero_count == inactive_rank + singled_rank
            ),
        },
        "interpretation": (
            "The real up/down asymmetry is no longer a loose rational mismatch. "
            "Upstairs, the numerator 3 is simultaneously the triality-triplet "
            "projector rank and the number of A labels in the slot-independent "
            "closure matrix, all over the cyclic shell 37. Downstairs, the shift "
            "from 3/37 to 1/14 is exactly a -(4+1)/(14*37) correction, and that "
            "same 4+1 is both the Hbar_2 inactive-plus-singled projector packet "
            "and the five complementary non-A nonzero closure labels {AB,AB,I,I,B}."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["down_asymmetry_projector_theorem"], indent=2))


if __name__ == "__main__":
    main()
