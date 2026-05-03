"""
Tests for Part CCXLVIII — Swampland Conjectures Bridge
Expected: 27 checks, Verified=True
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))

import pytest
from PART_CCXLVIII_SWAMPLAND_WGC_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    wgc_trivial_mult, wgc_tower_plus, wgc_tower_minus, wgc_tower_sum, wgc_total_species,
    dc_duality_frames, dc_lattice_dim, dc_moduli_count,
    species_D, species_scale_exp, species_N,
    no_global_sym_rank, total_generators,
    cobordism_maxdim,
    checks, Verified,
)


def test_all_checks_pass():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


def test_verified_true():
    assert Verified is True


def test_check_count():
    assert len(checks) == 27


def test_srg_params():
    assert Q == 3
    assert V == 40
    assert K == 12
    assert LAM == 2
    assert MU == 4


def test_wgc_tower():
    # WGC tower: trivial=1, M_LAM, M_NEG; sum = V = 40
    assert wgc_trivial_mult == 1
    assert wgc_tower_plus == M_LAM
    assert wgc_tower_minus == M_NEG
    assert wgc_tower_sum == V
    assert wgc_tower_sum == 1 + M_LAM + M_NEG


def test_wgc_species_count():
    assert wgc_total_species == V


def test_distance_conjecture():
    # DC lattice dimension = 24 = K*LAM; moduli count = 20 = V//LAM
    assert dc_lattice_dim == K * LAM
    assert dc_moduli_count == V // LAM


def test_species_scale():
    assert species_D == K // LAM      # 6
    assert species_scale_exp == MU    # 4


def test_no_global_symmetry():
    assert no_global_sym_rank == K
    assert total_generators == EDGES
