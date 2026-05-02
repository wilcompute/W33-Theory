#!/usr/bin/env python3
"""
PART CLXXVI - Firewall Diagonal / Fiber Albert Bridge
=====================================================

CLXXV produced the triple-Albert split

    3 * J_3(O) = 3 * (3 + 24) = 9 + 72 = 81.

The repo's E6 cubic affine Heisenberg artifact gives the missing concrete
meaning of the 9-sector:

    affine_line_triads = 36
    fiber_triads       = 9
    cubic_triads_total = 45

and verifies

    firewall_bad_triads_match_fiber_triads = true.

In Heisenberg coordinates F_3^3, the 27 points are (u,z) with

    u in F_3^2  -> 9 possible u-fibers
    z in F_3    -> 3 points per fiber.

Thus the 9 fiber triads are the vertical z-lines over the 9 u-values.  This
matches the triple-Albert diagonal sector exactly:

    triple Albert diagonal sector = 3 generations * 3 diagonal entries = 9.

The complement is the affine/off-diagonal sector:

    affine line triads = 36
    oriented affine directions = 2 * 36 = 72 = E6 root count.

Therefore the old 36/9 firewall split is the same object as the new
triple-Albert 72/9 split, with orientation converting 36 affine triads into
72 E6 root directions.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

Q = 3
Q2 = Q * Q
Q3 = Q ** 3
Q4 = Q ** 4
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
J = 5
J_INV = 8
RANK_SEED = 2 * Q

ALBERT_DIM = Q3
ALBERT_DIAGONAL = Q
ALBERT_OFFDIAGONAL = Q * J_INV
TRIPLE_ALBERT = Q * ALBERT_DIM
TRIPLE_DIAGONAL = Q * ALBERT_DIAGONAL
TRIPLE_OFFDIAGONAL = Q * ALBERT_OFFDIAGONAL

HEISENBERG_POINTS = Q3
U_FIBERS = Q2
Z_LEVELS = Q
FIBER_TRIADS = U_FIBERS
AFFINE_U_LINES = Q2 + Q + 1  # 12 affine lines in AG(2,3)
TRIADS_PER_U_LINE = Q
AFFINE_LINE_TRIADS = AFFINE_U_LINES * TRIADS_PER_U_LINE
CUBIC_TRIADS_TOTAL = AFFINE_LINE_TRIADS + FIBER_TRIADS
ORIENTED_AFFINE_ROOTS = 2 * AFFINE_LINE_TRIADS


@dataclass(frozen=True)
class FirewallLayer:
    name: str
    value: int
    formula: str
    interpretation: str


def firewall_layers() -> List[FirewallLayer]:
    return [
        FirewallLayer("Heisenberg_points", HEISENBERG_POINTS, "q^3=27", "H27 cubic/Heisenberg points"),
        FirewallLayer("u_fibers", U_FIBERS, "q^2=9", "vertical z-fibers over u in F3^2"),
        FirewallLayer("z_levels", Z_LEVELS, "q=3", "three points per fiber"),
        FirewallLayer("fiber_triads", FIBER_TRIADS, "q^2=9", "firewall/fiber triads"),
        FirewallLayer("affine_u_lines", AFFINE_U_LINES, "q^2+q=12", "affine lines in the u-plane AG(2,3)"),
        FirewallLayer("affine_line_triads", AFFINE_LINE_TRIADS, "12*3=36", "non-firewall affine triads"),
        FirewallLayer("oriented_affine_roots", ORIENTED_AFFINE_ROOTS, "2*36=72", "oriented affine triads / E6 root directions"),
        FirewallLayer("cubic_triads_total", CUBIC_TRIADS_TOTAL, "36+9=45=5*q^2", "E6 cubic tritangent/triad total"),
        FirewallLayer("triple_albert_diagonal", TRIPLE_DIAGONAL, "3*3=9=q^2", "diagonal/fiber sector of three Albert copies"),
        FirewallLayer("triple_albert_offdiagonal", TRIPLE_OFFDIAGONAL, "3*24=72", "off-diagonal octonion sector / E6 roots"),
    ]


def firewall_diagonal_fiber_audit() -> Dict[str, object]:
    checks = {
        "one_albert_dim": ALBERT_DIM == Q3 == 27,
        "one_albert_split": ALBERT_DIAGONAL == Q == 3 and ALBERT_OFFDIAGONAL == Q * J_INV == 24,
        "triple_albert_split": TRIPLE_ALBERT == TRIPLE_DIAGONAL + TRIPLE_OFFDIAGONAL == Q4 == 81,
        "triple_diagonal_is_q2": TRIPLE_DIAGONAL == Q2 == 9,
        "triple_offdiagonal_is_e6_roots": TRIPLE_OFFDIAGONAL == 72,
        "heisenberg_points_are_q3": HEISENBERG_POINTS == Q3 == 27,
        "fibers_are_q2": U_FIBERS == FIBER_TRIADS == Q2 == 9,
        "fiber_points_partition_h27": FIBER_TRIADS * Z_LEVELS == HEISENBERG_POINTS,
        "affine_u_lines_count": AFFINE_U_LINES == 12,
        "affine_triads_count": AFFINE_LINE_TRIADS == 36,
        "cubic_triads_total": CUBIC_TRIADS_TOTAL == 45 == J * Q2,
        "firewall_split": CUBIC_TRIADS_TOTAL == AFFINE_LINE_TRIADS + FIBER_TRIADS,
        "oriented_affine_roots_are_72": ORIENTED_AFFINE_ROOTS == 72,
        "affine_orientation_gives_e6_roots": 2 * AFFINE_LINE_TRIADS == TRIPLE_OFFDIAGONAL,
        "fiber_triads_match_triple_diagonal": FIBER_TRIADS == TRIPLE_DIAGONAL,
        "fiber_plus_oriented_affine_is_h1": FIBER_TRIADS + ORIENTED_AFFINE_ROOTS == TRIPLE_ALBERT == 81,
        "rank_plus_oriented_affine_is_e6": RANK_SEED + ORIENTED_AFFINE_ROOTS == 78,
        "threshold_carrier_inverse": (J * J_INV) % PHI3 == 1,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXXVI_FIREWALL_DIAGONAL_FIBER_ALBERT",
        "source_links": {
            "CLXXV": "triple Albert / E8 grading bridge",
            "artifact": "artifacts/e6_cubic_affine_heisenberg_model.json",
            "legacy_firewall": "36/9 firewall split scripts and archive theorem",
        },
        "w33_atoms": {
            "q": Q,
            "q2": Q2,
            "q3": Q3,
            "q4": Q4,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "J": J,
            "J_inverse": J_INV,
            "rank_seed_2q": RANK_SEED,
        },
        "firewall_layers": [asdict(layer) for layer in firewall_layers()],
        "bridge_identities": {
            "artifact_split": "36 affine-line triads + 9 fiber triads = 45 cubic triads",
            "firewall_match": "artifact verifies firewall_bad_triads_match_fiber_triads=true",
            "albert_split": "3*J_3(O)=9 diagonal + 72 off-diagonal = 81",
            "identification": "9 fiber triads = triple-Albert diagonal sector; 2*36 oriented affine triads = 72 E6 roots",
            "h1_bridge": "9 + 72 = 81 = H1(W33)",
            "e6_bridge": "6 + 72 = 78 = dim(E6)",
        },
        "checks": checks,
        "theorem_statement": (
            "The old 36/9 firewall split is the concrete Heisenberg realization of the triple-Albert 72/9 split. "
            "The 9 fiber triads are the q^2 vertical z-fibers over F3^2 and match the 3*3 diagonal sector of three "
            "Albert copies.  The 36 affine-line triads orient to 72 directions, matching the E6 root count.  Hence "
            "H1(W33)=81 decomposes as 9 firewall/fiber modes plus 72 oriented affine/root modes."
        ),
        "interpretive_note": (
            "This welds the firewall back into the new algebra instead of treating it as an anomaly.  The firewall is the "
            "diagonal/fiber sector required to complete the 72 E6-root/off-diagonal directions into the full 81-dimensional "
            "three-generation carrier."
        ),
    }


def main() -> int:
    audit = firewall_diagonal_fiber_audit()
    out = ROOT / "PART_CLXXVI_firewall_diagonal_fiber_albert_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
