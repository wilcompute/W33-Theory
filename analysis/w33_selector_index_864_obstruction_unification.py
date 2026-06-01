"""Part MMCCCLXIX: selector index 864 obstruction unification.

Several independent selector computations keep returning the same integer:

* the negative-polar selector symmetry has |O^-(6,2)| / |A5| = 864;
* the draft golden selector has 864 ordered nonlocal quadrangle failures;
* the signed local affine search has 2*|AGL(2,3)| = 864 candidates.

This verifier promotes only the exact finite statements.  It does not claim a
canonical bijection between the three 864-element sets.  The new theorem is the
bounded bridge: the flatness obstruction is numerically the same size as the
missing index from the raw A5 torsor to the W(E6)/negative-polar selector, and
also the same size as the signed AGL(2,3) local search shell.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_clifford_antipodal_a5_selector_group import (  # noqa: E402
    clifford_antipodal_permutations,
    permutation_order,
)
from analysis.w33_golden_selector_z20_cochain_lift import (  # noqa: E402
    golden_selector_z20_cochain_lift_packet,
)
from analysis.w33_spread_negative_polar_selector_signature import (  # noqa: E402
    o_minus_6_2_order,
)


OUTPUT_PATH = ROOT / "PART_MMCCCLXIX_SELECTOR_INDEX_864_OBSTRUCTION_UNIFICATION_results.json"

Q = 3
V = 40
K = 12
MU = 4
G_NEG = 15
E8_ROOTS = 240


def gl_2_order(q: int) -> int:
    """Order of GL(2,q): choose two independent columns."""

    return (q**2 - 1) * (q**2 - q)


def agl_2_order(q: int) -> int:
    """Order of AGL(2,q) = translations by F_q^2 semidirect GL(2,q)."""

    return q**2 * gl_2_order(q)


def a5_torsor_order_profile() -> dict[str, int]:
    permutations = set(clifford_antipodal_permutations().values())
    return {str(order): int(count) for order, count in sorted(Counter(permutation_order(p) for p in permutations).items())}


def selector_index_864_obstruction_unification_packet() -> dict[str, Any]:
    a5_order = len(set(clifford_antipodal_permutations().values()))
    a5_profile = a5_torsor_order_profile()
    negative_polar_order = o_minus_6_2_order()
    negative_polar_over_a5 = negative_polar_order // a5_order
    agl_order = agl_2_order(Q)
    signed_agl_order = 2 * agl_order
    obstruction_unit = 2 ** (MU + 1) * Q**3

    golden = golden_selector_z20_cochain_lift_packet()
    draft = golden["draft_obstruction"]
    cochain = golden["cochain_system"]
    z20 = golden["z20_lift"]
    ordered_failures = int(draft["ordered_violations"])
    ordered_quadrangles = int(draft["ordered_quadrangles"])
    unique_failures = int(cochain["unique_failures"])

    checks = {
        "raw_clifford_selector_is_a5_order_60": a5_order == 60 and a5_profile == {"1": 1, "2": 15, "3": 20, "5": 24},
        "negative_polar_selector_order_is_we6": negative_polar_order == 51840,
        "negative_polar_over_a5_index_is_864": negative_polar_over_a5 == 864,
        "agl_2_3_order_is_432": agl_order == 432,
        "signed_agl_2_3_shell_is_864": signed_agl_order == 864,
        "golden_ordered_failures_are_864": ordered_failures == 864,
        "golden_unique_failures_are_108": unique_failures == 108,
        "ordered_failures_are_8_unique_failures": ordered_failures == 2**Q * unique_failures,
        "ordered_quadrangles_are_g_times_864": ordered_quadrangles == G_NEG * ordered_failures == V * K * Q**3,
        "obstruction_unit_is_2_mu_plus_1_q3": obstruction_unit == ordered_failures,
        "transport_edges_are_two_e8_root_shells": int(draft["directed_transport_edges"]) == 2 * E8_ROOTS,
        "z20_lift_removes_all_ordered_failures": int(z20["corrected_ordered_failures"]) == 0,
    }

    return {
        "part": "MMCCCLXIX",
        "theorem": "Selector index 864 obstruction unification",
        "input_packets": [
            "MDCLXXXIII Clifford antipodal A5 selector group",
            "MDCLXXXIV W33 spread negative-polar selector signature",
            "MCCXLVI golden selector Z20 cochain lift",
            "MMCCCLXVIII diagonal-A5 orbital selector no-go",
        ],
        "group_index": {
            "a5_order": a5_order,
            "a5_order_profile": a5_profile,
            "negative_polar_order": negative_polar_order,
            "negative_polar_over_a5": negative_polar_over_a5,
            "formula": "|O^-(6,2)|/|A5| = 51840/60 = 864",
        },
        "affine_search_shell": {
            "gl_2_3_order": gl_2_order(Q),
            "agl_2_3_order": agl_order,
            "signed_agl_2_3_order": signed_agl_order,
            "formula": "2*|AGL(2,3)| = 2*3^2*(3^2-1)*(3^2-3) = 864",
        },
        "golden_obstruction": {
            "ordered_quadrangles": ordered_quadrangles,
            "ordered_failures": ordered_failures,
            "unique_failures": unique_failures,
            "ordered_failures_over_unique_failures": ordered_failures // unique_failures,
            "total_over_failures": ordered_quadrangles // ordered_failures,
            "formula": "864 = 2^(mu+1)*q^3 = 32*27; 12960 = g*864",
        },
        "unified_864": {
            "negative_polar_index": negative_polar_over_a5,
            "signed_agl_shell": signed_agl_order,
            "golden_ordered_failures": ordered_failures,
            "substrate_decomposition": "2^(mu+1)*q^3 = 2^5*3^3",
            "unique_failure_core": "864/2^q = 108 = mu*q^3",
        },
        "reading": (
            "The raw A5 selector is exactly one 60-element torsor. The W33 spread "
            "selector lives in the 51840-element negative-polar/W(E6) symmetry, "
            "so the missing selector index is 864. Independently, the draft "
            "golden selector has exactly 864 ordered nonlocal quadrangle "
            "failures, and the local signed affine shell has exactly 864 "
            "candidates. The obstruction size is therefore not just a selector "
            "bug count: it is the exact coset-size required to pass from A5 to "
            "the W(E6) negative-polar selector scale."
        ),
        "claim_boundary": (
            "This proves equality of three exact 864-element counts and their "
            "substrate decomposition. It does not yet construct a canonical "
            "bijection from failed ordered quadrangles to O^-(6,2)/A5 cosets or "
            "to signed AGL(2,3) candidates. That bijection is the next selector "
            "target."
        ),
        "next_target": (
            "Build a canonical transport map whose fibers send the 108 unique "
            "golden failures, with their 8 orientations, onto the 864 cosets of "
            "the raw A5 torsor inside the negative-polar selector symmetry."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = selector_index_864_obstruction_unification_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MMCCCLXIX: Selector Index 864 Obstruction Unification ===")
    print("group index:", packet["group_index"])
    print("affine shell:", packet["affine_search_shell"])
    print("golden obstruction:", packet["golden_obstruction"])
    print("verified:", packet["n_verified"], "/", len(packet["checks"]))


if __name__ == "__main__":
    main()
