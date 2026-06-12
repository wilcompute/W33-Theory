#!/usr/bin/env python3
"""
BT839 - Grunbaum-Coxeter operation Euler/flag audit.

The source note contains 16 tables:

  base: 11-cell, 57-cell, tomotope partial a, tomotope partial b
  operations: rectified/truncated/expanded/omnitruncated for
              11-cell, 57-cell, and tomotope partial b

BT839 transcribes the rank-class counts and audits the arithmetic.  The
unexpected invariant is that all base tables have Euler 0, while every
Wythoff operation table carries a fixed negative Euler charge:

  11-cell operations      chi = -11
  57-cell operations      chi = -57
  tomotope operations     chi = -4

The omnitruncated vertices are the full flag carriers for the two regular
GC polytopes (660 and 3420) and the half-flag carrier for the tomotope (96),
whose doubled packet is the verified BT814 192-flag runtime ABI.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open() as f:
        return json.load(f)


def totals(rank_classes: list[list[int]]) -> list[int]:
    return [sum(row) for row in rank_classes]


def euler(rank_classes: list[list[int]]) -> int:
    t = totals(rank_classes)
    return t[0] - t[1] + t[2] - t[3]


BASE = {
    "11_cell": {
        "rank_classes": [[11], [55], [55], [11]],
        "vertex_figure": [10, 15, 6],
        "cell": [6, 15, 10],
        "prime": 11,
    },
    "57_cell": {
        "rank_classes": [[57], [171], [171], [57]],
        "vertex_figure": [6, 15, 10],
        "cell": [10, 15, 6],
        "prime": 19,
    },
    "tomotope_partial_a": {
        "rank_classes": [[8], [24], [32], [8, 8]],
        "vertex_figure": [6, 12, 4, 3],
        "cell": [[4, 6, 4], [3, 6, 4]],
    },
    "tomotope_partial_b": {
        "rank_classes": [[4], [12], [16], [4, 4]],
        "vertex_figure": [6, 12, 4, 3],
        "cell": [[4, 6, 4], [3, 6, 4]],
    },
}


OPERATIONS = {
    "11_cell": {
        "rectified": [[55], [165], [55, 66], [11, 11]],
        "truncated": [[110], [55, 165], [55, 66], [11, 11]],
        "expanded": [[66], [165, 165], [110, 165, 110], [11, 55, 55, 11]],
        "omnitruncated": [
            [660],
            [330, 330, 330, 330],
            [110, 165, 165, 66, 165, 110],
            [11, 55, 55, 11],
        ],
    },
    "57_cell": {
        "rectified": [[171], [855], [171, 570], [57, 57]],
        "truncated": [[342], [171, 855], [171, 570], [57, 57]],
        "expanded": [[570], [855, 855], [342, 855, 342], [57, 171, 171, 57]],
        "omnitruncated": [
            [3420],
            [1710, 1710, 1710, 1710],
            [342, 855, 855, 570, 855, 342],
            [57, 171, 171, 57],
        ],
    },
    "tomotope_partial_b": {
        "rectified": [[12], [48], [16, 16, 12], [4, 4, 4]],
        "truncated": [[24], [12, 48], [16, 16, 12], [4, 4, 4]],
        "expanded": [[48], [48, 48, 48], [16, 24, 24, 16, 12, 24], [4, 4, 12, 4]],
        "omnitruncated": [
            [96],
            [48, 48, 48, 48],
            [16, 24, 24, 16, 12, 24],
            [4, 4, 12, 4],
        ],
    },
}


def psl2_order(p: int) -> int:
    return p * (p * p - 1) // 2


def main() -> None:
    bt814 = load_json("data/bt814_tomotope_middle_layer_from_residual_tetrahedra.json")
    bt831 = load_json("data/bt831_tomotope_minimal_cover_architecture.json")
    bt837 = load_json("data/bt837_schedule_library_geometry.json")
    k, g, mu, f, n_eff = 12, 15, 4, 24, 55

    base_rows = {}
    for name, table in BASE.items():
        base_rows[name] = {
            "rank_totals": totals(table["rank_classes"]),
            "euler": euler(table["rank_classes"]),
            "rank_classes": table["rank_classes"],
        }

    operation_rows = {}
    for family, ops in OPERATIONS.items():
        operation_rows[family] = {}
        for opname, classes in ops.items():
            operation_rows[family][opname] = {
                "rank_totals": totals(classes),
                "euler": euler(classes),
                "rank_classes": classes,
            }

    euler_charge = {
        family: sorted({row["euler"] for row in ops.values()})
        for family, ops in operation_rows.items()
    }

    flag_bridge = {
        "11_cell": {
            "omnitruncated_vertices": operation_rows["11_cell"]["omnitruncated"]["rank_totals"][0],
            "psl2_order": psl2_order(11),
            "substrate_identity": k * n_eff,
            "cell_automorphism_product": 11 * 60,
            "cell_type": "hemi-icosahedron",
            "vertex_figure_type": "hemi-dodecahedron",
        },
        "57_cell": {
            "omnitruncated_vertices": operation_rows["57_cell"]["omnitruncated"]["rank_totals"][0],
            "psl2_order": psl2_order(19),
            "substrate_identity": k * g * 19,
            "cell_automorphism_product": 57 * 60,
            "w33_petersen_home_flags": bt837["t3"]["total_flags"],
            "petersen_home_plus_sentinel_sheet": bt837["t3"]["total_flags"] + k * g,
            "cell_type": "hemi-dodecahedron",
            "vertex_figure_type": "hemi-icosahedron",
        },
        "tomotope_partial_b": {
            "omnitruncated_vertices": operation_rows["tomotope_partial_b"]["omnitruncated"]["rank_totals"][0],
            "bt814_full_flags": bt814["f_vector_from_transversal_tetrahedra"]["flags_if_each_block_has_2x2_fiber"],
            "doubled_omnitruncated": 2 * operation_rows["tomotope_partial_b"]["omnitruncated"]["rank_totals"][0],
            "bt831_W3_order": next(row["Wk_order"] for row in bt831["cover_indices_tested"] if row["k"] == 3),
            "W3_from_flags": 2 * operation_rows["tomotope_partial_b"]["omnitruncated"]["rank_totals"][0] * 3**3,
            "cellular_family": "24-cell/toroidal tomotope middle-layer bridge",
        },
    }

    regular_polychoron_bridge = {
        "primary_pairing": {
            "11_cell_to_600_cell": {
                "reason": "icosahedral/hemi-icosahedral local structure; 600-cell vertices form 2I, whose projective quotient is A5",
                "direct_cell_match": False,
                "vertex_or_symmetry_match": True,
                "score": 2,
            },
            "tomotope_to_24_cell": {
                "reason": "24-cell/D4/24-stabilizer layer already appears as the tomotope runtime lift f=24",
                "direct_cell_match": False,
                "runtime_stabilizer_match": True,
                "score": 2,
            },
            "57_cell_to_120_cell": {
                "reason": "57-cell cells are hemi-dodecahedra and the 120-cell cells are dodecahedra",
                "direct_cell_match": True,
                "vertex_or_symmetry_match": True,
                "score": 3,
            },
        },
        "alternate_pairing": {
            "11_cell_to_120_cell": {
                "reason": "11-cell vertex figure is hemi-dodecahedron, so it has a weaker dual/vertex-figure dodecahedral hook",
                "direct_cell_match": False,
                "vertex_or_symmetry_match": True,
                "score": 1,
            },
            "57_cell_to_600_cell": {
                "reason": "57-cell vertex figure is hemi-icosahedron, so it has a weaker dual/vertex-figure icosahedral hook",
                "direct_cell_match": False,
                "vertex_or_symmetry_match": True,
                "score": 1,
            },
        },
        "regular_polychoron_counts": {
            "600_cell": {"vertices": 120, "edges": 720, "faces": 1200, "cells": 600},
            "24_cell": {"vertices": 24, "edges": 96, "faces": 96, "cells": 24},
            "120_cell": {"vertices": 600, "edges": 1200, "faces": 720, "cells": 120},
        },
        "boundary": "The 11/57 pairing is not asserted as an embedding of full regular polychora; it is a cell/vertex-figure/symmetry alignment.",
    }

    checks = {
        "all_base_tables_have_euler_zero": all(row["euler"] == 0 for row in base_rows.values()),
        "partial_a_is_double_partial_b": (
            base_rows["tomotope_partial_a"]["rank_totals"]
            == [2 * x for x in base_rows["tomotope_partial_b"]["rank_totals"]]
        ),
        "eleven_and_fiftyseven_swap_cell_and_vertex_figure": (
            BASE["11_cell"]["vertex_figure"] == BASE["57_cell"]["cell"]
            and BASE["11_cell"]["cell"] == BASE["57_cell"]["vertex_figure"]
        ),
        "operation_euler_charges_are_constant": (
            euler_charge == {
                "11_cell": [-11],
                "57_cell": [-57],
                "tomotope_partial_b": [-4],
            }
        ),
        "rectified_vertices_equal_base_edges": all(
            operation_rows[family]["rectified"]["rank_totals"][0] == base_rows[family]["rank_totals"][1]
            for family in ("11_cell", "57_cell", "tomotope_partial_b")
        ),
        "truncated_vertices_equal_twice_base_edges": all(
            operation_rows[family]["truncated"]["rank_totals"][0] == 2 * base_rows[family]["rank_totals"][1]
            for family in ("11_cell", "57_cell", "tomotope_partial_b")
        ),
        "expanded_11_uses_11_hemi_icosahedra": (
            operation_rows["11_cell"]["expanded"]["rank_totals"][0] == 11 * BASE["11_cell"]["cell"][0]
        ),
        "expanded_57_uses_57_hemi_dodecahedra": (
            operation_rows["57_cell"]["expanded"]["rank_totals"][0] == 57 * BASE["57_cell"]["cell"][0]
        ),
        "expanded_tomotope_is_bt814_packet": (
            operation_rows["tomotope_partial_b"]["expanded"]["rank_totals"][0]
            == bt814["f_vector_from_transversal_tetrahedra"]["middle_blocks"]
        ),
        "omnitruncated_11_is_psl2_11_and_k_neff": (
            flag_bridge["11_cell"]["omnitruncated_vertices"]
            == flag_bridge["11_cell"]["psl2_order"]
            == flag_bridge["11_cell"]["substrate_identity"]
            == flag_bridge["11_cell"]["cell_automorphism_product"]
        ),
        "omnitruncated_57_is_psl2_19_and_k_g_19": (
            flag_bridge["57_cell"]["omnitruncated_vertices"]
            == flag_bridge["57_cell"]["psl2_order"]
            == flag_bridge["57_cell"]["substrate_identity"]
            == flag_bridge["57_cell"]["cell_automorphism_product"]
        ),
        "w33_petersen_flags_complete_to_57_flags_by_kg": (
            flag_bridge["57_cell"]["petersen_home_plus_sentinel_sheet"]
            == flag_bridge["57_cell"]["omnitruncated_vertices"]
        ),
        "tomotope_omni_is_half_bt814_flags": (
            flag_bridge["tomotope_partial_b"]["doubled_omnitruncated"]
            == flag_bridge["tomotope_partial_b"]["bt814_full_flags"]
        ),
        "tomotope_W3_order_is_cover_lifted_full_flags": (
            flag_bridge["tomotope_partial_b"]["bt831_W3_order"]
            == flag_bridge["tomotope_partial_b"]["W3_from_flags"]
        ),
        "primary_pairing_scores_above_swapped": (
            regular_polychoron_bridge["primary_pairing"]["11_cell_to_600_cell"]["score"]
            + regular_polychoron_bridge["primary_pairing"]["57_cell_to_120_cell"]["score"]
            > regular_polychoron_bridge["alternate_pairing"]["11_cell_to_120_cell"]["score"]
            + regular_polychoron_bridge["alternate_pairing"]["57_cell_to_600_cell"]["score"]
        ),
        "twenty_four_cell_count_hits_runtime_lift": (
            regular_polychoron_bridge["regular_polychoron_counts"]["24_cell"]["vertices"] == f
            and regular_polychoron_bridge["regular_polychoron_counts"]["24_cell"]["edges"]
            == operation_rows["tomotope_partial_b"]["omnitruncated"]["rank_totals"][0]
        ),
        "one_twenty_cell_and_six_hundred_cell_are_dual_count_swap": (
            regular_polychoron_bridge["regular_polychoron_counts"]["120_cell"]["vertices"]
            == regular_polychoron_bridge["regular_polychoron_counts"]["600_cell"]["cells"]
            and regular_polychoron_bridge["regular_polychoron_counts"]["120_cell"]["cells"]
            == regular_polychoron_bridge["regular_polychoron_counts"]["600_cell"]["vertices"]
        ),
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT839 check failed: {name}")

    out = {
        "theorem": "BT839 Grunbaum-Coxeter operation Euler/flag audit",
        "base_tables": base_rows,
        "operation_tables": operation_rows,
        "euler_charge": euler_charge,
        "flag_bridge": flag_bridge,
        "regular_polychoron_bridge": regular_polychoron_bridge,
        "interpretation": {
            "base_tables": "all four base GC/tomotope tables are Euler-neutral; tomotope partial a is exactly the double cover of partial b",
            "operation_tables": "Wythoff operations turn neutrality into fixed charges -11, -57, and -4",
            "eleven_cell": "the 11-cell full flag count 660 is PSL(2,11), 11*A5, and k*N_eff",
            "fiftyseven_cell": "the 57-cell full flag count 3420 is PSL(2,19), 57*A5, and k*g*19; W33's 3240 Petersen homes need exactly k*g=180 sentinel slots to complete it",
            "tomotope": "the tomotope omnitruncation has 96 half-flags; doubling gives BT814's 192 full flags and cover-lifting gives BT831's W_k order",
            "regular_polychora": "the best-supported orientation is 11-cell -> 600-cell, tomotope -> 24-cell, 57-cell -> 120-cell, with 11/57 kept as a scored alignment rather than a full embedding claim",
        },
        "checks": checks,
    }
    path = ROOT / "data" / "bt839_gc_operation_euler_flag_audit.json"
    with path.open("w") as fjson:
        json.dump(out, fjson, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
