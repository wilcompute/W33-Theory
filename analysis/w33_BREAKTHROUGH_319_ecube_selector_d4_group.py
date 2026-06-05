"""W(3,3) BREAKTHROUGH 319: e-cube selector D4 group.

BT286 classified the 24 coordinate-conjugate binary-reflected e-cube
schedules and found that exactly eight preserve the coordinate pair partition

    {{1, 2}, {4, 8}}.

Those eight schedules are not just a set.  Under coordinate composition they
close as the full square-symmetry group D4 of order 8:

    r = (1 4 2 8)   as tuple images (4, 8, 2, 1), order 4
    s = (4 8)       as tuple images (1, 2, 8, 4), order 2
    s r s = r^-1.

Equivalently, the BT286 selector atlas is the pair-stabilizer

    (S2 x S2) semidirect S2

of the fast/slow Q2 recursion split.  This gives the internal group law behind
the eight selector-preserving coordinate schedules, and connects the selector
chain to the Hadamard/Q4 fact from the remote BT286 Hadamard packet: H_16
diagonalizes Q4 while RM(1, mu) = [16, 5, 8]_2.  The D4 order 8 is the
coordinate square symmetry one binary layer below the 16-state Q4 Fourier
carrier.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_286_ecube_coordinate_selector_atlas import (  # noqa: E402
    BITS,
    PAIR_PARTITION,
    ecube_coordinate_selector_atlas_packet,
)


Q = 3
IDENTITY = tuple(BITS)
R_GENERATOR = (4, 8, 2, 1)
S_GENERATOR = (1, 2, 8, 4)
DOUBLE_PAIR_SWAP = (2, 1, 8, 4)
HADAMARD_PACKET_PATH = ROOT / "data" / "w33_BREAKTHROUGH_286_hadamard_substrate_tower.json"


def _mapping(perm: tuple[int, ...]) -> dict[int, int]:
    return dict(zip(BITS, perm))


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Return left after right, both represented by images of BITS."""
    left_map = _mapping(left)
    right_map = _mapping(right)
    return tuple(left_map[right_map[bit]] for bit in BITS)


def inverse(perm: tuple[int, ...]) -> tuple[int, ...]:
    mapping = _mapping(perm)
    inverse_map = {image: source for source, image in mapping.items()}
    return tuple(inverse_map[bit] for bit in BITS)


def power(perm: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = IDENTITY
    for _ in range(exponent):
        result = compose(perm, result)
    return result


def order(perm: tuple[int, ...]) -> int:
    result = IDENTITY
    for exponent in range(1, 25):
        result = compose(perm, result)
        if result == IDENTITY:
            return exponent
    raise ValueError(f"order not found for {perm}")


def preserves_pair_partition(perm: tuple[int, ...]) -> bool:
    mapping = _mapping(perm)
    image_partition = {frozenset(mapping[bit] for bit in block) for block in PAIR_PARTITION}
    return image_partition == set(PAIR_PARTITION)


def pair_stabilizer() -> set[tuple[int, ...]]:
    return {tuple(perm) for perm in permutations(BITS) if preserves_pair_partition(tuple(perm))}


def subgroup_generated_by(generators: tuple[tuple[int, ...], ...]) -> set[tuple[int, ...]]:
    group = {IDENTITY}
    frontier = set(generators)
    while frontier:
        element = frontier.pop()
        if element in group:
            continue
        group.add(element)
        for left, right in product(tuple(group), generators):
            for candidate in (compose(left, right), compose(right, left)):
                if candidate not in group:
                    frontier.add(candidate)
    return group


def _as_lists(elements: set[tuple[int, ...]] | list[tuple[int, ...]]) -> list[list[int]]:
    return [list(element) for element in sorted(elements)]


def _string_key(perm: tuple[int, ...]) -> str:
    return "".join(str(value) for value in perm)


def _load_hadamard_packet() -> dict:
    return json.loads(HADAMARD_PACKET_PATH.read_text(encoding="utf-8"))


def ecube_selector_d4_group_packet() -> dict:
    bt286 = ecube_coordinate_selector_atlas_packet()
    hadamard = _load_hadamard_packet()

    selector_perms = {tuple(row["coordinate_permutation"]) for row in bt286["selector_atlas_rows"]}
    selector_by_perm = {
        tuple(row["coordinate_permutation"]): row["selector_index"]
        for row in bt286["selector_atlas_rows"]
    }
    stabilizer = pair_stabilizer()
    elements = sorted(stabilizer)

    closure_table = {
        _string_key(left): {
            _string_key(right): list(compose(left, right)) for right in elements
        }
        for left in elements
    }
    order_distribution = Counter(order(element) for element in elements)
    center = [
        element
        for element in elements
        if all(compose(element, other) == compose(other, element) for other in elements)
    ]
    noncommuting_witnesses = [
        (left, right)
        for left, right in product(elements, elements)
        if compose(left, right) != compose(right, left)
    ]

    r = R_GENERATOR
    s = S_GENERATOR
    generated_by_rs = subgroup_generated_by((r, s))
    srs = compose(s, compose(r, s))

    element_rows = [
        {
            "coordinate_permutation": list(element),
            "selector_index": selector_by_perm.get(element),
            "order": order(element),
            "inverse": list(inverse(element)),
            "is_central": element in center,
        }
        for element in elements
    ]

    checks = {
        "bt286_selector_match_count_is_8": bt286["selector_match_count"] == 2**Q == 8,
        "bt286_selector_set_equals_pair_stabilizer": selector_perms == stabilizer,
        "pair_stabilizer_count_is_wreath_product": len(stabilizer) == (2 * 2 * 2) == 8,
        "group_order_is_2_to_q": len(elements) == 2**Q,
        "identity_present": IDENTITY in stabilizer,
        "group_closed_under_composition": all(
            compose(left, right) in stabilizer for left, right in product(elements, elements)
        ),
        "every_element_has_inverse_in_group": all(inverse(element) in stabilizer for element in elements),
        "composition_table_stays_in_selector_set": all(
            tuple(value) in selector_perms
            for row in closure_table.values()
            for value in row.values()
        ),
        "nonabelian": bool(noncommuting_witnesses),
        "order_distribution_is_D4": dict(order_distribution) == {1: 1, 2: 5, 4: 2},
        "center_has_two_elements": len(center) == 2,
        "central_involution_is_double_pair_swap": DOUBLE_PAIR_SWAP in center,
        "r_has_order_4": order(r) == 4,
        "s_has_order_2": order(s) == 2,
        "srs_is_r_inverse": srs == inverse(r),
        "rs_generate_all_eight": generated_by_rs == stabilizer,
        "selector_rows_hit_all_eight_once": bt286["selector_distribution"] == {
            index: 1 for index in range(8)
        },
        "hadamard_rm_mu_bridge_present": hadamard["reed_muller_at_mu"]["explicit"] == [16, 5, 8],
        "hadamard_diagonalizes_Q4_adjacency": hadamard["diagonalizes_Q_mu_adjacency"] is True,
    }

    return {
        "breakthrough": 319,
        "title": "E-cube selector D4 group",
        "coordinate_bits": BITS,
        "pair_partition": [sorted(block) for block in PAIR_PARTITION],
        "group_order": len(elements),
        "group_order_substrate_form": "2^q = 8",
        "group_identification": "D4, the order-8 square symmetry group",
        "wreath_product_form": "(S2 x S2) semidirect S2",
        "elements": _as_lists(elements),
        "element_rows": element_rows,
        "closure_table": closure_table,
        "order_distribution": dict(sorted(order_distribution.items())),
        "center": _as_lists(center),
        "generators": {
            "r_order_4": list(r),
            "s_order_2": list(s),
            "relation": "r^4 = s^2 = 1 and s*r*s = r^-1",
            "srs": list(srs),
            "r_inverse": list(inverse(r)),
        },
        "noncommuting_witness": {
            "left": list(noncommuting_witnesses[0][0]),
            "right": list(noncommuting_witnesses[0][1]),
            "left_after_right": list(compose(noncommuting_witnesses[0][0], noncommuting_witnesses[0][1])),
            "right_after_left": list(compose(noncommuting_witnesses[0][1], noncommuting_witnesses[0][0])),
        },
        "selector_atlas_link": {
            "source_breakthrough": 286,
            "selector_match_count": bt286["selector_match_count"],
            "selector_distribution": bt286["selector_distribution"],
            "selector_permutations": _as_lists(selector_perms),
        },
        "hadamard_q4_link": {
            "source_breakthrough": 286,
            "reed_muller_at_mu": hadamard["reed_muller_at_mu"],
            "diagonalizes_Q_mu_adjacency": hadamard["diagonalizes_Q_mu_adjacency"],
            "reading": (
                "BT319 supplies the D4 square symmetry of the fast/slow Q2 recursion "
                "split, while the Hadamard packet supplies the H16 Fourier basis "
                "diagonalizing the full Q4 adjacency operator."
            ),
        },
        "architectural_reading": (
            "The remaining eight e-cube selector schedules form the exact D4 "
            "coordinate symmetry of the {{1,2},{4,8}} fast/slow recursion square. "
            "BT285 picks one phase, BT286 classifies the eight phases, BT287 derives "
            "the pair split, and BT319 proves the atlas has the square group law."
        ),
        "boundary": (
            "This is a finite coordinate-symmetry theorem for the e-cube selector "
            "atlas. It does not claim a new physical gauge group or replace the "
            "larger affine/Fano/octet selector gauges already tracked in earlier "
            "packets."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = ecube_selector_d4_group_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 319: E-CUBE SELECTOR D4 GROUP")
    print("=" * 78)
    print()
    print(f"group order        = {packet['group_order']} = {packet['group_order_substrate_form']}")
    print(f"group              = {packet['group_identification']}")
    print(f"order distribution = {packet['order_distribution']}")
    print(f"center             = {packet['center']}")
    print(f"verified           = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = ROOT / "data" / "w33_BREAKTHROUGH_319_ecube_selector_d4_group.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
