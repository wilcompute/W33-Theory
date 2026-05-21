"""Part MCLXXXV: Q4-tomotope triproduct monodromy lock.

Continuation of MCLXXXI-MCLXXXIV.

New exact statement:
  monodromy M=18432 factors as two independent tri-products:

  M = V_q4 * F_q4 * I_medial = 16 * 24 * 48,
  M = E_tom * T_tom * A_tom  = 12 * 16 * 96.

So the same monodromy packet is fixed both by a router-side
vertex-face-medial volume and a tomotope-side edge-triangle-automorphism
volume.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def q4_tomotope_triproduct_monodromy_lock_packet() -> dict[str, object]:
    mclxxxi = _load(ROOT / "PART_MCLXXXI_Q4_PLAQUETTE_DIRECTED_CHANGE_results.json")
    mclxxxii = _load(ROOT / "PART_MCLXXXII_Q4_TOMOTOPE_REYE_DOUBLE_COVER_results.json")
    mclxxxiii = _load(ROOT / "PART_MCLXXXIII_Q4_TOMOTOPE_MONODROMY_BIQUADRATIC_LOCK_results.json")

    q4_vertices = int(mclxxxi["input_context"]["q4_vertices"])             # 16
    q4_faces = int(mclxxxi["plaquette_formula"]["face_count"])             # 24
    medial_incidences = int(mclxxxii["antipodal_quotient"]["incidences"])  # 48

    tomotope_edges = int(mclxxxii["tomotope_lock"]["edges"])               # 12
    tomotope_triangles = int(mclxxxii["tomotope_lock"]["triangles"])       # 16
    tomotope_automorphism = int(mclxxxii["tomotope_lock"]["automorphism_group_order"])  # 96

    monodromy = int(mclxxxiii["tomotope_packet"]["monodromy_order"])       # 18432

    router_triprod = q4_vertices * q4_faces * medial_incidences
    tomotope_triprod = tomotope_edges * tomotope_triangles * tomotope_automorphism

    checks = {
        "router_triproduct_matches_monodromy": router_triprod == monodromy,
        "tomotope_triproduct_matches_monodromy": tomotope_triprod == monodromy,
        "router_and_tomotope_triproducts_match": router_triprod == tomotope_triprod,
        "router_triproduct_identity": (q4_vertices, q4_faces, medial_incidences) == (16, 24, 48),
        "tomotope_triproduct_identity": (tomotope_edges, tomotope_triangles, tomotope_automorphism) == (12, 16, 96),
        "monodromy_is_18432": monodromy == 18432,
        "monodromy_over_q4_vertices_is_face_medial_sheet": monodromy // q4_vertices == q4_faces * medial_incidences,
        "monodromy_over_tomotope_edges_is_triangle_aut_sheet": monodromy // tomotope_edges == tomotope_triangles * tomotope_automorphism,
        "q4_face_to_tomotope_edge_ratio_is_2": q4_faces == 2 * tomotope_edges,
        "q4_vertex_to_tomotope_triangle_ratio_is_1": q4_vertices == tomotope_triangles,
    }

    return {
        "part": "MCLXXXV",
        "theorem": "Q4-tomotope triproduct monodromy lock",
        "router_packet": {
            "q4_vertices": q4_vertices,
            "q4_faces": q4_faces,
            "medial_incidences": medial_incidences,
            "triproduct": router_triprod,
            "identity": "16*24*48 = 18432",
        },
        "tomotope_packet": {
            "tomotope_edges": tomotope_edges,
            "tomotope_triangles": tomotope_triangles,
            "tomotope_automorphism": tomotope_automorphism,
            "triproduct": tomotope_triprod,
            "identity": "12*16*96 = 18432",
        },
        "lock": {
            "monodromy": monodromy,
            "identity": "18432 = 16*24*48 = 12*16*96",
        },
        "finite_universality_surrogate": {
            "statement": "the same monodromy is fixed by both router-side and tomotope-side tri-volume packets",
            "boundary": "finite incidence/combinatorial lock; not a continuum field equation",
        },
        "claim_boundary": "finite tri-product monodromy law on Q4/tomotope packets",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = q4_tomotope_triproduct_monodromy_lock_packet()
    out_path = ROOT / "PART_MCLXXXV_Q4_TOMOTOPE_TRIPRODUCT_MONODROMY_LOCK_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXXV: Q4-Tomotope Triproduct Monodromy Lock ===")
    print(packet["lock"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
