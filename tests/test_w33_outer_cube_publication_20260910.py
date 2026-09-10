from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_outer_cube_observer_bridge_v2 import build_result  # noqa: E402
from w33_stabilizer96_cube_central_cover import build_result as build_cover  # noqa: E402
from w33_publish_september_2026_frontier import BEGIN, END, render_section  # noqa: E402


def test_outer_fixed_residue_is_explicit_cube_and_welds_to_observer_chart() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    fixed = data["outer_fixed_cube"]
    assert len(fixed["fixed_point_ids"]) == 8
    assert fixed["W33_collinearity_edges_on_fixed_points"] == 16
    assert len(fixed["complement_Q3_edges"]) == 12
    assert len(fixed["Q3_square_faces"]) == 6
    assert fixed["graph_identity"] == "complement(W33[Fix(D)]) = K4,4 - perfect_matching ~= Q3"

    q = data["spread_orbit_quotient"]
    assert q["spread_orbit_count"] == 20
    assert q["spread_orbit_size_histogram"] == {"1": 4, "2": 16}
    assert len(q["fixed_spread_K4_edges"]) == 6
    assert len(q["swapped_orbit_internal_edges"]) == 6
    assert q["four_intersection_edge_orbits"] == 141
    assert q["edge_orbit_size_histogram"] == {"1": 12, "2": 129}
    assert q["fixed_edge_types"] == {
        "edge_between_fixed_spreads": 6,
        "loop_from_exchanged_spreads": 6,
    }
    assert q["quotient_loop_count"] == 6
    assert q["lifted_edge_mass"] == 270

    observer = data["observer_affine_cube"]
    assert len(observer["stochastic_macrostates"]) == 8
    assert set(observer["stochastic_macrostates"]) == {
        f"1{a}{b}{c}" for a in (0, 1) for b in (0, 1) for c in (0, 1)
    }
    assert len(observer["observer_Q3_edges"]) == 12
    assert data["Q4_facet_weld"]["facet_vertex_count"] == 8
    assert data["Q4_facet_weld"]["facet_edge_count"] == 12


def test_stabilizer96_is_nonsplit_central_cover_of_cube_symmetry() -> None:
    data = build_cover()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    cube = data["cube_automorphism_group"]
    assert cube["order"] == 48
    assert cube["center_order"] == 2
    assert cube["derived_order"] == 12
    assert cube["direct_product"].endswith("C2 x S4")
    cover = data["Heawood_stabilizer_cover"]
    assert cover["H_order"] == 96
    assert cover["quotient_order"] == 48
    assert cover["quotient"] == "H/Z(H) ~= C2 x S4 ~= Aut(Q3)"
    assert cover["splitting"] == "NON-SPLIT"
    cocycle = data["extension_cocycle"]
    assert cocycle["cocycle_triples_checked"] == 48 ** 3
    assert cocycle["nontriviality_witness"]["alpha_g_h"] == 1
    assert cocycle["nontriviality_witness"]["alpha_h_g"] == 0


def test_publication_renderer_and_docs_index_anchor() -> None:
    section = render_section()
    assert BEGIN in section and END in section
    assert "New cubical bridge" in section
    assert "12 + 129×2" in section
    assert "D8 ×_C2 S4" in section
    assert "AG(3,2) ≅ F2^3" in section
    assert "non-split central double cover" in section

    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert docs.count(BEGIN) == 1
    assert docs.count(END) == 1
    assert 'id="heawood-schubert-observer-20260910"' in docs
    assert "Cube/observer bridge JSON" in docs
    assert "central-cover cocycle" in docs


def test_holonet_publication_insert_is_wired() -> None:
    wrapper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    insert = ROOT / "analysis" / "BT20260910_heawood_schubert_observer_insert.tex"
    assert insert.is_file()
    assert r"\input{analysis/BT20260910_heawood_schubert_observer_insert}" in wrapper
