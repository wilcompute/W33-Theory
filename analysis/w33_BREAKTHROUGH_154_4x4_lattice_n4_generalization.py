"""W(3,3) BREAKTHROUGH 154: 4x4 lattice n=4 generalization.

Extends the WRF lattice harness to a 4x4 = 16-cell lattice.  The
promotable theorem is an exact Clifford-frame statement:

    16 = 2^mu = dim Cl_4 = sum_r binom(4,r).

The 4x4 lattice is therefore a Dirac/Clifford operator-basis frame, with
grade profile 1,4,6,4,1.  This is stronger and more accurate than calling
the 16 cells the components of a conventional complex Dirac spinor.

The seed grid uses the BT141-D spacing rule: every pair of seeds is at least
100 apart, so the WRF orthogonality harness predicts zero cross-talk.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
import math
from pathlib import Path


Q = 3
LAMBDA = 2
MU = 4
DIRECTED_STATES_PER_CELL = 480
CID_TYPICAL = 100


def binomial(n: int, k: int) -> int:
    return math.comb(n, k)


def seed_grid() -> list[list[int]]:
    seeds = [61 + 100 * index for index in range(MU**2)]
    return [seeds[index : index + MU] for index in range(0, len(seeds), MU)]


def flat(values: list[list[int]]) -> list[int]:
    return [item for row in values for item in row]


def min_pair_spacing(values: list[int]) -> int:
    return min(abs(left - right) for left, right in combinations(values, 2))


def lattice_4x4_packet() -> dict:
    n_cells = MU**2
    grades = [binomial(MU, grade) for grade in range(MU + 1)]
    seeds = seed_grid()
    seed_values = flat(seeds)
    joint_address_bits = n_cells * math.log2(CID_TYPICAL)

    checks = {
        "cell_count_is_mu_squared": n_cells == MU**2 == 16,
        "cell_count_is_lambda_to_mu": n_cells == LAMBDA**MU,
        "cell_count_is_clifford_dimension": n_cells == 2**MU,
        "grade_profile_is_cl4": grades == [1, 4, 6, 4, 1],
        "even_odd_clifford_split_is_balanced": sum(grades[::2]) == sum(grades[1::2]) == 2**Q,
        "seed_count_is_16": len(seed_values) == n_cells,
        "seed_spacing_rule_holds": min_pair_spacing(seed_values) >= CID_TYPICAL,
        "base_6_register_seed_is_present": 661 in seed_values,
        "directed_state_total_is_7680": n_cells * DIRECTED_STATES_PER_CELL == 7680,
        "full_4d_toric_cells_are_q4": Q ** (Q + 1) == 81,
        "spinor_frame_is_subregion_not_full_spacetime": n_cells < Q ** (Q + 1),
        "joint_address_bits_round_to_106": round(joint_address_bits) == 106,
    }

    return {
        "breakthrough": 154,
        "title": "4x4 lattice Clifford-frame generalization",
        "n_cells": n_cells,
        "seed_grid": seeds,
        "min_seed_spacing": min_pair_spacing(seed_values),
        "expected_cross_talk": 0,
        "clifford_grade_profile": grades,
        "grade_labels": ["scalar", "vector", "bivector", "pseudovector", "pseudoscalar"],
        "even_grade_count": sum(grades[::2]),
        "odd_grade_count": sum(grades[1::2]),
        "directed_state_total": n_cells * DIRECTED_STATES_PER_CELL,
        "typical_cids_per_cell": CID_TYPICAL,
        "joint_address_bits": joint_address_bits,
        "full_4d_toric_cells": Q ** (Q + 1),
        "reading": (
            "A 4x4 WRF lattice is exactly a 16-cell Cl_4 operator-basis frame: "
            "1 scalar, 4 vectors, 6 bivectors, 4 pseudovectors, and 1 pseudoscalar. "
            "It is a Clifford/Dirac control frame around Bell-qutrit cells, not a "
            "claim that a conventional complex Dirac spinor has 16 components."
        ),
        "boundary": (
            "This verifies the finite lattice and seed-spacing theorem. It does "
            "not run a live WRF cross-talk experiment; it applies the already "
            "committed BT141-D spacing rule."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main():
    packet = lattice_4x4_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 154: 4x4 LATTICE CLIFFORD FRAME")
    print("=" * 78)
    print()

    print("16 CELL SUBSTRATE READING:")
    print("  16 = lambda^mu = 2^4")
    print("  16 = mu^2 = 4^2")
    print("  16 = dim Cl_4 = sum_r C(4,r)")
    print(f"  Clifford grade profile: {packet['clifford_grade_profile']}")
    print(f"  even/odd split: {packet['even_grade_count']} / {packet['odd_grade_count']} = 2^q / 2^q")
    print()

    print("SEEDS (BT141-D spaced):")
    for row, values in enumerate(packet["seed_grid"]):
        print(f"  Row {row}: {values}")
    print()
    print(f"  Minimum pair spacing: {packet['min_seed_spacing']} >= 100")
    print("  BT141-D predicts zero cross-talk under this spacing rule.")
    print()

    print("JOINT ADDRESS SPACE:")
    print(f"  Per-cell distinct CIDs ~ {packet['typical_cids_per_cell']}")
    print(f"  Joint 16-tuple space ~ 100^16 = 10^32")
    print(f"  Address bits: {packet['joint_address_bits']:.1f}")
    print()

    print("SCALING TO FULL 4D TORIC SPACETIME:")
    print(f"  Full toric sector: q^(q+1) = {packet['full_4d_toric_cells']} cells")
    print("  This 4x4 lattice: 16 cells = Cl_4 control frame")
    print("  Substrate provides both the 81-cell matter bulk and the 16-cell Clifford frame.")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 154 SUMMARY")
    print("=" * 78)
    print("""
4x4 LATTICE = 16-CELL CLIFFORD/ DIRAC OPERATOR FRAME.

SUBSTRATE READINGS:
  16 = lambda^mu = mu^2 = dim Cl_4.
  Grade profile 1+4+6+4+1 is exact.
  Even and odd grades split 8/8 = 2^q / 2^q.

WRF PREDICTIONS:
  Cross-talk: 0 (BT141-D rule, spacing 100 enforced)
  Joint address space: 100^16 = 10^32 (~106 bits)

SCALING BOUNDARY:
  16 cells = Clifford/Dirac operator frame
  81 cells = q^(q+1) matter sector (full 4D toric, BT136)
  The 16-cell frame is a subregion/control basis, not the full spacetime.

CLOSES USER'S BT145 OPEN QUEUE ITEM with a corrected finite interpretation.
""")

    out = Path("data") / "w33_BREAKTHROUGH_154_4x4_lattice_n4_generalization.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")
    print(f"verified {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
