from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "PART_W33_PASS4721_4724_SUPPORT12_INVOLUTION_SQUARE_ROOT_COVER.json"


def D():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_4721_support12_disjointness_triangles():
    d = D()["4721_support12_disjointness"]
    assert d["vertices"] == 1620
    assert d["degree"] == 2
    assert d["components"] == 540
    assert d["component_graph"] == "K3"
    assert d["triangle_union_lines"] == 36
    assert d["residual_lines"] == 4
    assert d["distinct_residues"] == 270
    assert d["triangles_per_residue"] == 2


def test_4722_old_270_frontier_is_resolved():
    d = D()["4722_involution_resolution"]
    assert d["PSp_order"] == 25920
    assert d["inner_involutions_total"] == 315
    assert d["fixed_line_census"] == {"4": 270, "16": 45}
    assert d["residues_equal_four_fixed_line_sets"] is True
    assert d["unique_involution_per_residue"] is True
    assert d["residue_stabilizer_order_PSp"] == 96
    assert "point positions" in d["old_pass1830_erratum"]
    assert "line indices" in d["old_pass1830_erratum"]


def test_4723_square_root_double_cover_and_outer_boundary():
    d = D()["4723_square_root_double_cover"]
    assert d["PGSp_order"] == 51840
    assert d["outer_square_roots_per_representative_involution"] == 8
    assert d["four_fixed_line_square_roots"] == 2
    assert d["four_fixed_roots_are_inverse_pair"] is True
    assert d["triangle_orbit_PSp"] == d["outer_order4_orbit_PSp"] == 540
    assert d["triangle_stabilizer_order_PSp"] == d["root_centralizer_order_PSp"] == 48
    assert d["inner_stabilizers_equal"] is True
    assert d["full_PGSp_triangle_stabilizer"] == d["full_PGSp_root_centralizer"] == 96
    assert d["full_extensions_equal"] is False
    assert d["full_extensions_intersection_order"] == 48


def test_4724_residual_incidence_factorization():
    d = D()["4724_residual_incidence"]
    assert (d["blocks"], d["block_size"], d["replication_per_line"]) == (270, 4, 27)
    assert d["skew_line_pairs"] == 540
    assert d["residues_per_skew_pair"] == 3
    assert d["residues_per_meeting_pair"] == 0
    assert d["gram_identity"] == "B B^T = 27 I + 3 (J-I-A_*)"
    assert d["real_gram_spectrum"] == {"108": 1, "18": 24, "36": 15}
    assert d["real_rank"] == 40
    assert d["binary_residue_span_rank"] == 30
    assert d["involution_fixed_support12_thickenings"] == 24
    assert d["involution_fixed_disjointness_triangles"] == 8
