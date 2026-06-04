"""W(3,3) BREAKTHROUGH 158: macro-tail sieve.

BT157 proved that one macro/inverse pair from the inverse-complete
distance-7 tail restores exact q! = 6 compiler depth.  BT158 asks whether
that macro was arbitrary.

It is not arbitrary, but the choice is also not unique:

    distance-7 tail size             = 151 = 4v - q^2
    q!-restoring macros              = 143 = p_Ih * Phi_3 = 11 * 13
    forbidden non-restoring macros   =   8 = 2^q

The eight failures form a binary obstruction pocket inside the tail.  The
admissible 143 macros are the WRF microcode freedom: any one of them can be
packaged as the receipt-bearing macro pair from BT157.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_157_cayley_compiler_macro_depth import (
    CENTERS,
    GROUP_ORDER,
    MU,
    Q,
    QFACT,
    V,
    bfs_from_maps,
    build_group,
    generator_set,
    mat_order,
    right_maps,
)


PHI3 = 13
P_IH = 11


def matrix_trace_mod3(matrix: tuple[tuple[int, ...], ...]) -> int:
    return sum(matrix[i][i] for i in range(4)) % 3


def reconstruct_generator_indices(
    elem_index: int,
    parent: list[int],
    parent_gen: list[int],
) -> list[int]:
    word = []
    cursor = elem_index
    while cursor != 0:
        word.append(parent_gen[cursor])
        cursor = parent[cursor]
    return list(reversed(word))


def compose_right_map(word: list[int], base_maps: list[list[int]], size: int) -> list[int]:
    action = list(range(size))
    for gen_index in word:
        gen_map = base_maps[gen_index]
        action = [gen_map[x] for x in action]
    return action


def macro_tail_sieve_packet() -> dict:
    generators, labels = generator_set(include_inverses=True)
    inverse_gen_index = {}
    for center_index in range(len(CENTERS)):
        inverse_gen_index[2 * center_index] = 2 * center_index + 1
        inverse_gen_index[2 * center_index + 1] = 2 * center_index

    elems, index, parent, parent_gen = build_group(generators)
    base_maps = right_maps(elems, index, generators)
    symmetric_dist = bfs_from_maps(base_maps, len(elems))
    tail = [elem_index for elem_index, dist in enumerate(symmetric_dist) if dist == QFACT + 1]

    rows = []
    for elem_index in tail:
        word_indices = reconstruct_generator_indices(elem_index, parent, parent_gen)
        inverse_word_indices = [inverse_gen_index[gen_index] for gen_index in reversed(word_indices)]
        macro_maps = [
            compose_right_map(word_indices, base_maps, len(elems)),
            compose_right_map(inverse_word_indices, base_maps, len(elems)),
        ]
        macro_dist = bfs_from_maps(base_maps + macro_maps, len(elems))
        macro_distribution = dict(sorted(Counter(macro_dist).items()))
        matrix = elems[elem_index]

        rows.append(
            {
                "index": elem_index,
                "diameter": max(macro_dist),
                "depth_6_count": macro_distribution.get(QFACT, 0),
                "order": mat_order(matrix),
                "trace_mod3": matrix_trace_mod3(matrix),
                "word": [labels[gen_index] for gen_index in word_indices],
                "matrix": [list(row) for row in matrix],
            }
        )

    success_rows = [row for row in rows if row["diameter"] == QFACT]
    failure_rows = [row for row in rows if row["diameter"] == QFACT + 1]
    best_depth = min(row["depth_6_count"] for row in success_rows)
    best_rows = [row for row in success_rows if row["depth_6_count"] == best_depth]

    success_order_dist = dict(sorted(Counter(row["order"] for row in success_rows).items()))
    failure_order_dist = dict(sorted(Counter(row["order"] for row in failure_rows).items()))
    success_trace_dist = dict(sorted(Counter(row["trace_mod3"] for row in success_rows).items()))
    failure_trace_dist = dict(sorted(Counter(row["trace_mod3"] for row in failure_rows).items()))

    checks = {
        "group_size_is_aut_w33": len(elems) == GROUP_ORDER,
        "tail_size_is_4v_minus_q_squared": len(tail) == 4 * V - Q**2 == 151,
        "admissible_macro_count_is_pih_phi3": len(success_rows) == P_IH * PHI3 == 143,
        "forbidden_macro_count_is_two_to_q": len(failure_rows) == 2**Q == 8,
        "admissible_plus_forbidden_is_tail": len(success_rows) + len(failure_rows) == len(tail),
        "all_forbidden_have_trace_zero": failure_trace_dist == {0: 8},
        "forbidden_orders_are_binary_pocket": failure_order_dist == {2: 4, 12: 4},
        "all_order_9_tail_macros_are_admissible": all(
            row["diameter"] == QFACT for row in rows if row["order"] == Q**2
        ),
        "best_macro_count_is_two": len(best_rows) == 2,
        "best_depth_six_count_is_890": best_depth == 890,
        "best_macros_have_order_9_trace_1": all(
            row["order"] == Q**2 and row["trace_mod3"] == 1 for row in best_rows
        ),
        "admissible_order_distribution_matches_audit": success_order_dist
        == {2: 1, 4: 6, 5: 6, 6: 52, 8: 14, 9: 14, 10: 6, 12: 42, 18: 2},
    }

    return {
        "breakthrough": 158,
        "title": "Macro-tail sieve",
        "tail_size": len(tail),
        "admissible_macro_count": len(success_rows),
        "forbidden_macro_count": len(failure_rows),
        "success_order_distribution": success_order_dist,
        "failure_order_distribution": failure_order_dist,
        "success_trace_distribution": success_trace_dist,
        "failure_trace_distribution": failure_trace_dist,
        "best_depth_6_count": best_depth,
        "best_macros": best_rows,
        "forbidden_macros": failure_rows,
        "architectural_reading": (
            "The BT157 macro is a choice from a 143-element admissible microcode "
            "sieve, not a unique accident. The remaining 8 distance-tail elements "
            "are a binary obstruction pocket that preserves diameter 7."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = macro_tail_sieve_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 158: MACRO-TAIL SIEVE")
    print("=" * 78)
    print()
    print("TAIL SIEVE:")
    print(f"  tail size              = {packet['tail_size']} = 4v - q^2")
    print(f"  admissible macros      = {packet['admissible_macro_count']} = p_Ih * Phi_3")
    print(f"  forbidden macros       = {packet['forbidden_macro_count']} = 2^q")
    print()
    print("ORDER DISTRIBUTIONS:")
    print(f"  admissible: {packet['success_order_distribution']}")
    print(f"  forbidden:  {packet['failure_order_distribution']}")
    print()
    print("BEST MACROS:")
    for row in packet["best_macros"]:
        print(f"  index={row['index']} order={row['order']} depth6={row['depth_6_count']} word={' '.join(row['word'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_158_macro_tail_sieve.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")
    print(f"verified {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
