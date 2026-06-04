"""W(3,3) BREAKTHROUGH 165: macro-tail E6/Phi12 boundary.

BT158 found the inverse-complete Cayley compiler tail:

    tail size       = 151
    admissible      = 143
    forbidden       = 8

BT159 showed the eight forbidden elements generate a 1152-element
F4/24-cell polarization normalizer.  BT161 then identified the 4x4 Q4
layer as an 8+8 parity/octionion bipartition.

This packet splices those threads.  The full 151-element distance-7 tail
has a sharper normalizer boundary:

    outside F4 normalizer = 78 mixed macros, all admissible
    inside F4 normalizer  = 73 anti-polarization macros = Phi_12
                          = 65 admissible + 8 forbidden

So the old "8 bad macros" are not isolated.  They are the octonion-sized
cap of a Phi_12 anti-polarization shell; the complementary shell outside
the normalizer has exact E6 dimension 78 and is entirely q!-restoring.
"""

from __future__ import annotations

from collections import Counter
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
    V,
    bfs_from_maps,
    build_group,
    generator_set,
    mat_order,
    right_maps,
)
from analysis.w33_BREAKTHROUGH_158_macro_tail_sieve import (  # noqa: E402
    P_IH,
    compose_right_map,
    matrix_trace_mod3,
    reconstruct_generator_indices,
)
from analysis.w33_BREAKTHROUGH_159_forbidden_pocket_f4_normalizer import (  # noqa: E402
    F4_WEYL_ORDER,
    closure_generated_by,
    is_anti_diagonal,
    is_block_diagonal,
)


F = 24
PHI3 = 13
PHI12 = 73
DIM_E6 = 78


def polarization_class(matrix: tuple[tuple[int, ...], ...]) -> str:
    if is_block_diagonal(matrix):
        return "block"
    if is_anti_diagonal(matrix):
        return "anti"
    return "mixed"


def _counter_to_json(counter: Counter) -> dict:
    return {str(key): value for key, value in sorted(counter.items())}


def macro_tail_e6_phi12_boundary_packet() -> dict:
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
        matrix = elems[elem_index]
        rows.append(
            {
                "index": elem_index,
                "diameter": max(macro_dist),
                "order": mat_order(matrix),
                "trace_mod3": matrix_trace_mod3(matrix),
                "polarization": polarization_class(matrix),
                "word": [labels[gen_index] for gen_index in word_indices],
                "matrix": matrix,
            }
        )

    forbidden_rows = [row for row in rows if row["diameter"] == QFACT + 1]
    forbidden_matrices = [row["matrix"] for row in forbidden_rows]
    normalizer = closure_generated_by(forbidden_matrices)

    for row in rows:
        row["in_f4_normalizer"] = row["matrix"] in normalizer

    class_counts = Counter(row["polarization"] for row in rows)
    class_diameter_counts = Counter(
        (row["polarization"], row["diameter"]) for row in rows
    )
    normalizer_boundary_counts = Counter(
        ("inside" if row["in_f4_normalizer"] else "outside", row["diameter"])
        for row in rows
    )
    inside_rows = [row for row in rows if row["in_f4_normalizer"]]
    outside_rows = [row for row in rows if not row["in_f4_normalizer"]]
    inside_order_distribution = Counter(row["order"] for row in inside_rows)
    outside_order_distribution = Counter(row["order"] for row in outside_rows)
    inside_trace_distribution = Counter(row["trace_mod3"] for row in inside_rows)
    outside_trace_distribution = Counter(row["trace_mod3"] for row in outside_rows)
    normalizer_distance_profile = Counter(symmetric_dist[index[matrix]] for matrix in normalizer)
    normalizer_class_distance_profile = Counter(
        (symmetric_dist[index[matrix]], polarization_class(matrix)) for matrix in normalizer
    )

    tail_summary = [
        {
            "index": row["index"],
            "diameter": row["diameter"],
            "order": row["order"],
            "trace_mod3": row["trace_mod3"],
            "polarization": row["polarization"],
            "in_f4_normalizer": row["in_f4_normalizer"],
            "word": row["word"],
        }
        for row in rows
    ]

    checks = {
        "tail_size_is_151": len(rows) == 151 == 4 * V - Q**2,
        "forbidden_count_is_octonion_dim": len(forbidden_rows) == 2**Q == 8,
        "f4_normalizer_order_is_1152": len(normalizer) == F4_WEYL_ORDER == 1152,
        "tail_intersection_f4_is_phi12": len(inside_rows) == PHI12 == 73,
        "tail_outside_f4_is_dim_e6": len(outside_rows) == DIM_E6 == 78,
        "anti_tail_equals_f4_intersection": all(
            (row["polarization"] == "anti") == row["in_f4_normalizer"] for row in rows
        ),
        "no_block_tail": class_counts.get("block", 0) == 0,
        "mixed_shell_all_admissible": all(row["diameter"] == QFACT for row in outside_rows),
        "anti_shell_splits_65_plus_8": normalizer_boundary_counts == {
            ("outside", QFACT): DIM_E6,
            ("inside", QFACT): V + F + 1,
            ("inside", QFACT + 1): 2**Q,
        },
        "anti_admissible_is_v_plus_f_plus_one": sum(
            1 for row in inside_rows if row["diameter"] == QFACT
        )
        == V + F + 1
        == 65,
        "admissible_total_is_pih_phi3": sum(1 for row in rows if row["diameter"] == QFACT)
        == P_IH * PHI3
        == 143,
        "tail_decomposition_is_e6_plus_65_plus_octonion": len(rows)
        == DIM_E6 + (V + F + 1) + 2**Q,
        "normalizer_tail_is_pure_anti": all(
            polarization_class(matrix) == "anti"
            for matrix in normalizer
            if symmetric_dist[index[matrix]] == QFACT + 1
        ),
        "normalizer_distance_profile_matches": dict(sorted(normalizer_distance_profile.items()))
        == {0: 1, 1: 10, 2: 46, 3: 117, 4: 192, 5: 250, 6: 463, 7: 73},
        "inside_order_distribution_matches": dict(sorted(inside_order_distribution.items()))
        == {2: 5, 4: 6, 6: 32, 8: 6, 12: 24},
        "outside_order_distribution_matches": dict(sorted(outside_order_distribution.items()))
        == {5: 6, 6: 20, 8: 8, 9: 14, 10: 6, 12: 22, 18: 2},
        "inside_trace_distribution_is_phi12_trace_zero": dict(
            sorted(inside_trace_distribution.items())
        )
        == {0: PHI12},
        "outside_trace_distribution_is_28_26_24": dict(
            sorted(outside_trace_distribution.items())
        )
        == {0: 28, 1: 26, 2: F},
        "outside_trace_sectors_sum_to_dim_e6": sum(outside_trace_distribution.values())
        == 28 + 26 + F
        == DIM_E6,
    }

    return {
        "breakthrough": 165,
        "title": "Macro-tail E6/Phi12 boundary",
        "tail_size": len(rows),
        "f4_normalizer_order": len(normalizer),
        "tail_by_polarization": dict(sorted(class_counts.items())),
        "tail_by_polarization_and_diameter": _counter_to_json(class_diameter_counts),
        "tail_by_f4_boundary_and_diameter": _counter_to_json(normalizer_boundary_counts),
        "boundary_decomposition": {
            "outside_f4_normalizer": {
                "count": len(outside_rows),
                "reading": "78 = dim(E6) = q! * Phi_3",
                "all_admissible": True,
            },
            "inside_f4_normalizer": {
                "count": len(inside_rows),
                "reading": "73 = Phi_12 anti-polarization shell",
                "admissible": sum(1 for row in inside_rows if row["diameter"] == QFACT),
                "forbidden": len(forbidden_rows),
                "admissible_reading": "65 = v + f + 1 = 40 + 24 + 1",
                "forbidden_reading": "8 = 2^q = octonion dimension",
            },
        },
        "inside_order_distribution": dict(sorted(inside_order_distribution.items())),
        "outside_order_distribution": dict(sorted(outside_order_distribution.items())),
        "inside_trace_distribution": dict(sorted(inside_trace_distribution.items())),
        "outside_trace_distribution": dict(sorted(outside_trace_distribution.items())),
        "outside_trace_reading": {
            "trace_0": "28 = D4 root count",
            "trace_1": "26 = bosonic string dimension",
            "trace_2": "24 = f",
        },
        "normalizer_distance_profile": dict(sorted(normalizer_distance_profile.items())),
        "normalizer_class_distance_profile": _counter_to_json(normalizer_class_distance_profile),
        "tail_summary": tail_summary,
        "architectural_reading": (
            "The q! compiler-restoring freedom is not merely a 143-element "
            "sieve. The distance-7 tail has an exact normalizer wall: the "
            "78 elements outside the F4/24-cell normalizer are a mixed "
            "E6-dimensional admissible shell, while the 73 elements inside "
            "the normalizer are a Phi_12 anti-polarization shell whose "
            "octonion-sized 8-element cap is precisely the forbidden pocket. "
            "The outside E6 shell further splits by trace into 28+26+24, "
            "matching the D4 root count, bosonic string dimension, and f."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = macro_tail_e6_phi12_boundary_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 165: MACRO-TAIL E6/PHI12 BOUNDARY")
    print("=" * 78)
    print()
    print("TAIL SPLIT:")
    print(f"  tail size                  = {packet['tail_size']}")
    print(f"  by polarization            = {packet['tail_by_polarization']}")
    print(f"  by F4 boundary/diameter    = {packet['tail_by_f4_boundary_and_diameter']}")
    print()
    print("BOUNDARY DECOMPOSITION:")
    for key, value in packet["boundary_decomposition"].items():
        print(f"  {key}:")
        for subkey, subvalue in value.items():
            print(f"    {subkey:<20s} = {subvalue}")
    print()
    print("F4 NORMALIZER DISTANCE PROFILE:")
    print(f"  {packet['normalizer_distance_profile']}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_165_macro_tail_e6_phi12_boundary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")
    print(f"verified {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
