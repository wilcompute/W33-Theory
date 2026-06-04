"""W(3,3) BREAKTHROUGH 166: optimal macro receipt pair.

BT165 split the distance-7 macro tail across the F4 normalizer boundary:

    78 outside-F4 mixed macros, all admissible
    73 inside-F4 anti macros = 65 admissible + 8 forbidden

BT166 asks which admissible macros are best, not merely valid.  The answer is
again boundary-clean:

    the unique optimal pair is outside F4, mixed, trace 1, order 9,
    and the two optimal macros are mutual inverses.

So the receipt-bearing macro from BT157 is not arbitrary.  The canonical
q!-restoring macro pair lives in the E6-dimensional outside-normalizer shell,
inside its trace-1/order-9 sector.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_157_cayley_compiler_macro_depth import (  # noqa: E402
    CENTERS,
    Q,
    QFACT,
    bfs_from_maps,
    build_group,
    generator_set,
    mat_id,
    mat_mul,
    mat_order,
    right_maps,
)
from analysis.w33_BREAKTHROUGH_158_macro_tail_sieve import (  # noqa: E402
    compose_right_map,
    matrix_trace_mod3,
    reconstruct_generator_indices,
)
from analysis.w33_BREAKTHROUGH_159_forbidden_pocket_f4_normalizer import (  # noqa: E402
    closure_generated_by,
)
from analysis.w33_BREAKTHROUGH_165_macro_tail_e6_phi12_boundary import (  # noqa: E402
    DIM_E6,
    polarization_class,
)


def _counter_to_json(counter: Counter) -> dict:
    return {str(key): value for key, value in sorted(counter.items())}


def _profile(values: list[int]) -> dict:
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "sum": sum(values),
        "average_fraction": f"{sum(values)}/{len(values)}",
    }


def optimal_macro_e6_trace1_receipt_packet() -> dict:
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
        inverse_word_indices = [
            inverse_gen_index[gen_index] for gen_index in reversed(word_indices)
        ]
        macro_maps = [
            compose_right_map(word_indices, base_maps, len(elems)),
            compose_right_map(inverse_word_indices, base_maps, len(elems)),
        ]
        macro_dist = bfs_from_maps(base_maps + macro_maps, len(elems))
        macro_distribution = Counter(macro_dist)
        matrix = elems[elem_index]
        rows.append(
            {
                "index": elem_index,
                "matrix": matrix,
                "diameter": max(macro_dist),
                "depth_6_count": macro_distribution[QFACT],
                "order": mat_order(matrix),
                "trace_mod3": matrix_trace_mod3(matrix),
                "polarization": polarization_class(matrix),
                "word": [labels[gen_index] for gen_index in word_indices],
            }
        )

    forbidden_rows = [row for row in rows if row["diameter"] == QFACT + 1]
    normalizer = closure_generated_by([row["matrix"] for row in forbidden_rows])
    for row in rows:
        row["boundary"] = "inside" if row["matrix"] in normalizer else "outside"

    admissible_rows = [row for row in rows if row["diameter"] == QFACT]
    best_depth = min(row["depth_6_count"] for row in admissible_rows)
    best_rows = [row for row in admissible_rows if row["depth_6_count"] == best_depth]
    outside_trace1_rows = [
        row for row in admissible_rows if row["boundary"] == "outside" and row["trace_mod3"] == 1
    ]
    outside_trace1_order9_rows = [
        row for row in outside_trace1_rows if row["order"] == Q**2
    ]

    by_boundary_trace = defaultdict(list)
    by_boundary_order = defaultdict(list)
    for row in admissible_rows:
        by_boundary_trace[(row["boundary"], row["trace_mod3"])].append(row["depth_6_count"])
        by_boundary_order[(row["boundary"], row["order"])].append(row["depth_6_count"])

    best_pair_inverse = (
        len(best_rows) == 2
        and mat_mul(best_rows[0]["matrix"], best_rows[1]["matrix"]) == mat_id()
        and mat_mul(best_rows[1]["matrix"], best_rows[0]["matrix"]) == mat_id()
    )

    best_summary = [
        {
            "index": row["index"],
            "boundary": row["boundary"],
            "polarization": row["polarization"],
            "trace_mod3": row["trace_mod3"],
            "order": row["order"],
            "depth_6_count": row["depth_6_count"],
            "word": row["word"],
        }
        for row in best_rows
    ]

    outside_trace1_depth_distribution = Counter(
        row["depth_6_count"] for row in outside_trace1_rows
    )
    outside_trace1_order9_depth_distribution = Counter(
        row["depth_6_count"] for row in outside_trace1_order9_rows
    )

    checks = {
        "admissible_count_is_143": len(admissible_rows) == 143,
        "outside_admissible_count_is_dim_e6": sum(
            1 for row in admissible_rows if row["boundary"] == "outside"
        )
        == DIM_E6
        == 78,
        "best_depth_is_890": best_depth == 890,
        "best_count_is_unique_inverse_pair": len(best_rows) == 2 and best_pair_inverse,
        "best_indices_are_stable": [row["index"] for row in best_rows] == [51706, 51765],
        "best_pair_is_outside_f4": all(row["boundary"] == "outside" for row in best_rows),
        "best_pair_is_mixed": all(row["polarization"] == "mixed" for row in best_rows),
        "best_pair_is_trace1": all(row["trace_mod3"] == 1 for row in best_rows),
        "best_pair_is_order9": all(row["order"] == Q**2 == 9 for row in best_rows),
        "outside_trace1_count_is_26": len(outside_trace1_rows) == 26,
        "outside_trace1_order9_count_is_14": len(outside_trace1_order9_rows) == 14,
        "outside_trace1_depths_are_inverse_paired": all(
            count == 2 for count in outside_trace1_depth_distribution.values()
        ),
        "outside_trace1_order9_depth_profile_matches": dict(
            sorted(outside_trace1_order9_depth_distribution.items())
        )
        == {890: 2, 1217: 2, 1448: 2, 1572: 2, 1915: 2, 2360: 2, 3375: 2},
        "inside_min_is_worse_than_best": min(
            row["depth_6_count"] for row in admissible_rows if row["boundary"] == "inside"
        )
        > best_depth,
        "outside_trace0_min_is_worse_than_best": min(
            row["depth_6_count"]
            for row in admissible_rows
            if row["boundary"] == "outside" and row["trace_mod3"] == 0
        )
        > best_depth,
        "outside_trace2_min_is_worse_than_best": min(
            row["depth_6_count"]
            for row in admissible_rows
            if row["boundary"] == "outside" and row["trace_mod3"] == 2
        )
        > best_depth,
    }

    return {
        "breakthrough": 166,
        "title": "Optimal macro E6 trace-1 receipt pair",
        "admissible_count": len(admissible_rows),
        "best_depth_6_count": best_depth,
        "best_macros": best_summary,
        "best_pair_inverse": best_pair_inverse,
        "outside_trace1_count": len(outside_trace1_rows),
        "outside_trace1_order9_count": len(outside_trace1_order9_rows),
        "outside_trace1_depth_distribution": dict(sorted(outside_trace1_depth_distribution.items())),
        "outside_trace1_order9_depth_distribution": dict(
            sorted(outside_trace1_order9_depth_distribution.items())
        ),
        "quality_by_boundary_trace": {
            str(key): _profile(values) for key, values in sorted(by_boundary_trace.items())
        },
        "quality_by_boundary_order": {
            str(key): _profile(values) for key, values in sorted(by_boundary_order.items())
        },
        "architectural_reading": (
            "The canonical q!-restoring macro receipt is the unique inverse "
            "pair minimizing the depth-6 shell. Both optimal macros are outside "
            "the F4/24-cell normalizer, mixed rather than anti-polarization, "
            "trace 1 mod 3, and order 9. Thus the compiler's best receipt "
            "comes from the E6-dimensional outside shell, not the Phi_12 "
            "normalizer shell."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = optimal_macro_e6_trace1_receipt_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 166: OPTIMAL MACRO E6 TRACE-1 RECEIPT")
    print("=" * 78)
    print()
    print("OPTIMAL MACROS:")
    for row in packet["best_macros"]:
        print(
            "  index={index} boundary={boundary} polarization={polarization} "
            "trace={trace_mod3} order={order} depth6={depth_6_count} word={word}".format(
                **{**row, "word": " ".join(row["word"])}
            )
        )
    print()
    print(f"best pair inverse       = {packet['best_pair_inverse']}")
    print(f"outside trace-1 count   = {packet['outside_trace1_count']}")
    print(f"outside trace-1 order-9 = {packet['outside_trace1_order9_count']}")
    print()
    print("OUTSIDE TRACE-1 ORDER-9 DEPTH PROFILE:")
    print(f"  {packet['outside_trace1_order9_depth_distribution']}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_166_optimal_macro_e6_trace1_receipt.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")
    print(f"verified {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
