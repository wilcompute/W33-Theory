#!/usr/bin/env python3
"""Corrected regressions for Passes 1158-1162."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from analysis.w33_pass1158_kernel_residual_1952 import main as p1158, RESIDUAL, factorize
from analysis.w33_pass1160_we6_character_bridge import main as p1160, WE6_IRREP_DIMS
from analysis.w33_pass1161_propagator_determinant_product import main as p1161
from analysis.w33_pass1162_corpus_full_sync import run_invariants


def test_residual_exact_character_decomposition():
    result = p1158()
    assert RESIDUAL == 1952
    assert factorize(RESIDUAL) == {2: 5, 61: 1}
    assert result["commutant_dimension"] == 1109
    assert result["isotypic_species"] == 10


def test_we6_irrep_structure_corrected():
    result = p1160()
    assert len(WE6_IRREP_DIMS) == 25
    assert sum(d**2 for d in WE6_IRREP_DIMS) == 51840
    assert result["orders"]["PSp(4,3)"] == 25920
    assert result["point_permutation_module"] == "1 + 24 + 15"


def test_propagator_determinant_and_ihara():
    result = p1161()
    assert result["constant_term"] == "1"
    assert result["linear_coeff_check"] is True
    assert result["trace_D"] == -40
    assert result["ihara_zeta"]["hashimoto_quadratic_coefficient"] == 11


def test_corpus_sync_all_pass():
    checks, passed, failed = run_invariants()
    assert not failed, f"Failed invariants: {[c['name'] for c in failed]}"
    assert passed == len(checks)
