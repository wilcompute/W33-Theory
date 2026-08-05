#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import pytest

from analysis.bt3458_3471_face_tower_brauer_tomotope import build_certificate

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/PART_BT3458_BT3471_FACE_TOWER_BRAUER_TOMOTOPE_results.json"


@pytest.fixture(scope="module")
def certificate():
    return build_certificate()


def test_all_exact_checks_pass(certificate):
    assert certificate["status"] == "PASS"
    assert len(certificate["checks"]) == 12
    assert all(certificate["checks"].values())


def test_face_tower_recovers_w33(certificate):
    tower = certificate["sections"]["association_scheme_and_face_tower"]
    assert tower["face_action"]["degree"] == 240
    assert tower["face_action"]["antipodal_pairs"] == 120
    assert tower["pair_scheme"]["valency_two_relation_components"] == [40, 3]
    assert tower["quotient"]["srg"] == [40, 12, 2, 4]
    assert tower["quotient"]["matching_triangle_holonomy"] == {
        "identity": 1080,
        "transposition": 2160,
        "three_cycle": 0,
    }


def test_characteristic_three_loewy_data(certificate):
    modular = certificate["sections"]["characteristic_three_descent"]
    assert modular["pair_module"]["endomorphism_radical_dimensions_J_J2_J3"] == [4, 1, 0]
    assert modular["pair_module"]["endomorphism_loewy_layers"] == [1, 3, 1]
    assert modular["antisymmetric_module"]["decomposition_dimensions"] == [81, 39]
    assert modular["antisymmetric_module"]["rank_39_endomorphism_ring"] == "F3[epsilon]/(epsilon^2)"


def test_m4_and_tomotope_boundaries(certificate):
    m4 = certificate["sections"]["full_M4_amplitude_compiler"]
    assert m4["algebra_dimensions"] == {
        "S4_transposition_group_algebra_image": 10,
        "plus_null_conic_dual_sign": 16,
        "target_full_M4": 16,
    }
    tomotope = certificate["sections"]["tomotope_product_code"]
    assert tomotope["product_code_falsifier"]["maximum_projective_triples_in_one_dual_coset"] == 4
    assert tomotope["oriented_tetrahedron_incidence"]["configuration"] == [12, 4, 16, 3]


def test_frozen_semantic_surface(certificate):
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert frozen["status"] == "PASS"
    assert frozen["checks"] == certificate["checks"]
    assert frozen["sections"]["association_scheme_and_face_tower"]["pair_scheme"] == certificate["sections"]["association_scheme_and_face_tower"]["pair_scheme"]
    assert frozen["sections"]["characteristic_three_descent"] == certificate["sections"]["characteristic_three_descent"]
    assert frozen["sections"]["tomotope_product_code"] == certificate["sections"]["tomotope_product_code"]


def test_hardware_sources_present():
    formal = (ROOT / "rtl/w33_five_channel_formal_rom.v").read_text(encoding="utf-8")
    testbench = (ROOT / "rtl/tb_w33_pass3458_3471_order3.v").read_text(encoding="utf-8")
    assert "module w33_five_channel_symbol_rom" in formal
    assert "module w33_mod3_order3_formal" in formal
    assert "PASS literal_equivalence=200 order3_cases=1944" in testbench
