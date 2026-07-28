#!/usr/bin/env python3
"""Corrected regressions for Passes 1168-1172."""
import pathlib, sys
from math import comb
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from analysis.w33_pass1168_sym3_decomposition import main as p1168
from analysis.w33_pass1169_sp43_432_orbit_source import main as p1169
from analysis.w33_pass1170_meataxe_kernel_plan import main as p1170
from analysis.w33_pass1171_needs_tag_fix import main as p1171, ERRATUM
from analysis.w33_pass1172_ihara_zeta_degree20 import main as p1172


def test_sym3_dimension_and_scope_barrier():
    r=p1168(); assert r["total_dimension"]==comb(42,3)==11480
    assert "does not identify" in r["rejected_claim"]


def test_432_extension_types_not_conflated():
    r=p1169(); assert r["groups"]["PSp(4,3)"]["order"]==25920
    assert r["groups"]["Sp(4,3)"]["order"]==51840
    assert r["groups"]["W(E6)"]["order"]==51840
    assert r["coset_sizes"]["W(E6)/S5"]==r["coset_sizes"]["PSp(4,3)/A5"]==432
    assert "intersection" in r["required_unfinished_check"]


def test_meataxe_semisimple_not_absolute_claim():
    r=p1170(); assert r["kernel_dimension"]==2195
    assert r["modular_validation"]["semisimple"] is True
    assert "does not guarantee" in r["modular_validation"]["field_warning"]


def test_erratum_module_not_orbit():
    r=p1171(); assert r["all_tags_present"] is True
    assert ERRATUM["object_type"]=="W(E6)-module, not orbit"


def test_ihara_degree20_corrected():
    r=p1172(); assert r["hashimoto_quadratic_coefficient"]==11
    assert r["inverse_coefficients_degree_0_to_20"][0]==1
    assert r["closed_nonbacktracking_traces_n_1_to_20"][2]==960
    assert r["ramanujan"] is True
