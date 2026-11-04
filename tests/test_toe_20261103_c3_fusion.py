"""Regression checks for C3-equivariant apartment basis and frame fusion."""
from pathlib import Path
import importlib.util
import math
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
def load(fname):
    sp=importlib.util.spec_from_file_location(fname,ROOT/"analysis"/fname)
    x=importlib.util.module_from_spec(sp);sp.loader.exec_module(x)
    return x

@pytest.fixture(scope="module")
def c3():
    return load("toe_20261103_c3_symmetry_selector.py").certificate(seed=2,save=False)

@pytest.fixture(scope="module")
def fusion():
    return load("toe_20261103_c3_tightframe_fusion.py").run()

def test_c3_projective_character(c3):
    assert (c3["transvection_fixed_points"],c3["transvection_fixed_lines"],
            c3["transvection_fixed_flags"],c3["cycle_character_trace"])==(13,4,16,0)
    assert c3["apartment_orbits"]==540 and c3["chosen_orbits"]==27

def test_c3_exact_basis_and_symmetry(c3):
    assert c3["C3_H_invariant"] and c3["cut_leakage_exact_zero"]
    assert c3["cycle_GF2_rank"]==81 and c3["max_flag_load"]==6
    assert c3["chosen_cycles"]==81 and c3["edge_hoppings"]==1985

def test_fusion_exact_finite_certificate(fusion):
    assert fusion["status"].startswith("PASS_EXACT")
    assert fusion["constituent_seeds"]==[5,9,18]
    assert fusion["C3_symmetry_verified_exact"]
    assert fusion["cycle_cut_leakage_zero_exact"]
    assert fusion["three_frames_cycle_count"]==243
    assert fusion["fused_hopping_pairs"]==4320
    assert fusion["max_offdiag_neighbors"]==72

def test_fusion_conditioning_and_flux(fusion):
    assert math.isclose(fusion["three_C3_fused"]["condition"],6.9978021402123485,rel_tol=1e-9)
    assert fusion["conditioning_gain_from_seed33"]>181
    assert fusion["pi_flux_triangles"]==13066
    assert fusion["signed_triangles"]==29418
    assert fusion["fused_flag_load_max"]<=18
