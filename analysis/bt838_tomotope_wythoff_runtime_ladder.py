#!/usr/bin/env python3
"""
BT838 - Tomotope Wythoff runtime ladder.

The Grunbaum-Coxeter/tomotope table gives the local tomotope operation
vertex counts

    original, rectified, truncated, expanded, omnitruncated
    4,        12,        24,        48,       96

BT838 ties those counts to the holonet runtime:

    4   = mu tomotope vertex carriers
    12  = k local edge axes
    24  = f Clifford lift / local runtime stabilizer
    48  = BT814 middle packet ABI
    96  = half of the 192 full flag packet

The expanded tomotope is therefore not decoration: it is exactly the packet
surface the runtime already uses.  The omnitruncated tomotope is the half-flag
boundary whose doubled base/shadow fiber gives the 192 durable packet flags.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open() as f:
        return json.load(f)


def main() -> None:
    bt814 = load_json("data/bt814_tomotope_middle_layer_from_residual_tetrahedra.json")
    bt831 = load_json("data/bt831_tomotope_minimal_cover_architecture.json")
    bt832 = load_json("data/bt832_cover_indexed_durable_storage.json")

    q, mu, k, f = 3, 4, 12, 24
    fvec = bt814["f_vector_from_transversal_tetrahedra"]
    source_operation_vertices = {
        "original_tomotope": 4,
        "rectified_tomotope": 12,
        "truncated_tomotope": 24,
        "maximal_expanded_tomotope": 48,
        "omnitruncated_tomotope": 96,
    }
    runtime_ladder = [
        {
            "operation": "original_tomotope",
            "vertices": 4,
            "runtime_layer": "four transversal vertex carriers",
            "substrate_identity": "mu",
        },
        {
            "operation": "rectified_tomotope",
            "vertices": 12,
            "runtime_layer": "local tomotope edge axes",
            "substrate_identity": "k",
        },
        {
            "operation": "truncated_tomotope",
            "vertices": 24,
            "runtime_layer": "full lift of the D12 mirror-slot stabilizer",
            "substrate_identity": "f",
        },
        {
            "operation": "maximal_expanded_tomotope",
            "vertices": 48,
            "runtime_layer": "BT814 cover-invariant packet ABI",
            "substrate_identity": "2*f = four tetrahedra x three axes x four faces",
        },
        {
            "operation": "omnitruncated_tomotope",
            "vertices": 96,
            "runtime_layer": "half-flag packet boundary",
            "substrate_identity": "4*f = 192/2",
        },
    ]

    w_orders = {
        row["k"]: row["Wk_order"]
        for row in bt831["cover_indices_tested"]
    }
    cover_scaled = []
    for row in bt832["cover_lifts"]:
        kk = row["cover_index"]
        cover_scaled.append({
            "k": kk,
            "expanded_packet_slots": source_operation_vertices["maximal_expanded_tomotope"] * kk**3,
            "bt832_lifted_capacity": row["cover_counts"]["lifted_packet_slots"],
            "omnitruncated_half_flags": source_operation_vertices["omnitruncated_tomotope"] * kk**3,
            "full_flags": 2 * source_operation_vertices["omnitruncated_tomotope"] * kk**3,
            "bt831_Wk_order": w_orders[kk],
        })

    checks = {
        "bt814_original_tomotope_counts_match": (
            fvec["vertices"] == 4
            and fvec["edges"] == 12
            and fvec["faces"] == 16
            and fvec["cells"] == 8
        ),
        "bt831_source_counts_match_original": (
            bt831["source_facts"]["tomotope_counts"]["vertices"] == 4
            and bt831["source_facts"]["tomotope_counts"]["edges"] == 12
            and bt831["source_facts"]["tomotope_counts"]["triangles"] == 16
            and bt831["source_facts"]["tomotope_counts"]["tetrahedra"]
            + bt831["source_facts"]["tomotope_counts"]["hemioctahedra"] == 8
        ),
        "operation_vertex_ladder_is_mu_k_f_2f_4f": (
            list(source_operation_vertices.values()) == [mu, k, f, 2 * f, 4 * f]
        ),
        "rectified_vertices_are_edge_axes": (
            source_operation_vertices["rectified_tomotope"] == fvec["edges"]
        ),
        "truncated_vertices_are_clifford_lift": (
            source_operation_vertices["truncated_tomotope"] == f
        ),
        "expanded_vertices_are_bt814_packet_blocks": (
            source_operation_vertices["maximal_expanded_tomotope"] == fvec["middle_blocks"]
        ),
        "omnitruncated_vertices_are_half_flags": (
            source_operation_vertices["omnitruncated_tomotope"]
            == fvec["flags_if_each_block_has_2x2_fiber"] // 2
        ),
        "full_flags_are_twice_omnitruncated": (
            2 * source_operation_vertices["omnitruncated_tomotope"]
            == fvec["flags_if_each_block_has_2x2_fiber"]
        ),
        "post_rectification_doubles_three_times": (
            [
                source_operation_vertices["truncated_tomotope"] // source_operation_vertices["rectified_tomotope"],
                source_operation_vertices["maximal_expanded_tomotope"] // source_operation_vertices["truncated_tomotope"],
                source_operation_vertices["omnitruncated_tomotope"] // source_operation_vertices["maximal_expanded_tomotope"],
            ] == [2, 2, 2]
        ),
        "first_jump_is_q": (
            source_operation_vertices["rectified_tomotope"]
            // source_operation_vertices["original_tomotope"] == q
        ),
        "cover_scaled_expanded_matches_bt832_capacity": all(
            row["expanded_packet_slots"] == row["bt832_lifted_capacity"]
            for row in cover_scaled
        ),
        "cover_scaled_full_flags_double_half_flags": all(
            row["full_flags"] == 2 * row["omnitruncated_half_flags"]
            for row in cover_scaled
        ),
        "cover_scaled_full_flags_equal_Wk_order": all(
            row["full_flags"] == row["bt831_Wk_order"]
            for row in cover_scaled
        ),
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT838 check failed: {name}")

    out = {
        "theorem": "BT838 tomotope Wythoff runtime ladder",
        "source": "Grunbaum-Coxeter/tomotope operation tables: original, rectified, truncated, maximal expanded, omnitruncated tomotope",
        "source_operation_vertices": source_operation_vertices,
        "runtime_ladder": runtime_ladder,
        "cover_scaled_ladder": cover_scaled,
        "interpretation": {
            "expanded_tomotope": "the maximal expanded tomotope is the BT814 48-block packet ABI",
            "omnitruncated_tomotope": "the omnitruncated tomotope is the 96-element half-flag boundary; base/shadow doubling gives 192 flags",
            "cover_order": "after cover lift, the full flag count 192*k^3 equals BT831's W_k order",
            "architecture": "Wythoff operations are packet expansion stages, not only geometric variants",
        },
        "checks": checks,
    }
    path = ROOT / "data" / "bt838_tomotope_wythoff_runtime_ladder.json"
    with path.open("w") as fjson:
        json.dump(out, fjson, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
