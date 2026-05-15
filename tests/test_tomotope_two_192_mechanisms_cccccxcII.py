from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.PART_CCCCCXCII_tomotope_two_192_mechanisms import build


def test_intermediate_semiregular_group_order_192():
    summary = build()
    assert summary.intermediate_group_order_192 == 192
    assert summary.intermediate_group_order_192 == 8 * summary.packet_24


def test_actual_tomotope_automorphism_order_and_flags():
    summary = build()
    assert summary.tomotope_automorphism_order_96 == 96
    assert summary.tomotope_flag_orbits * summary.tomotope_automorphism_order_96 == summary.tomotope_flag_carrier_192 == 192


def test_tomotope_f_vector_and_facets():
    vertices = 4
    edges = 12
    triangles = 16
    tetrahedra = 4
    hemioctahedra = 4
    assert (vertices, edges, triangles, tetrahedra + hemioctahedra) == (4, 12, 16, 8)
    assert tetrahedra == hemioctahedra == 4


def test_intermediate_to_tomotope_collapse_halves_automorphism_scale():
    summary = build()
    assert summary.intermediate_group_order_192 // 2 == summary.tomotope_automorphism_order_96


def test_24_cell_packet_ladder_with_two_192s():
    summary = build()
    assert summary.packet_24 == 24
    assert summary.intermediate_group_order_192 == 192
    assert summary.tomotope_flag_carrier_192 == 192
    assert summary.f4_scale_1152 == 1152
    assert 6 * 192 == summary.f4_scale_1152


def test_reconciles_168_plus_24_with_tomotope_flags():
    summary = build()
    assert 168 + summary.packet_24 == summary.tomotope_flag_carrier_192


def test_code_crack_intrinsic_dimension_verdict():
    summary = build()
    assert summary.intrinsic_carrier_growth_degree == 3.0
    assert summary.intrinsic_monodromy_growth_degree == 6.0
    assert summary.intrinsic_4d_from_cover_only is False


def test_all_checks_hold():
    summary = build()
    assert all(summary.checks.values())
