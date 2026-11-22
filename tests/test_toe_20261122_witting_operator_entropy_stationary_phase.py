"""Tests that three distinct phase criteria have distinct exact maxima."""
import sys
from pathlib import Path
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261122_witting_operator_entropy_stationary_phase as extrema


def test_distinct_exact_extrema():
    c=extrema.verify()
    assert c["linear_entropy_maximum_a"]=="10/13"
    assert c["linear_entropy_maximum"]=="75/104"
    assert c["spectral_crossing_a"]=="2/3"
    assert c["Shannon_entropy_maximum_a"]=="16/(15+3^(6/5))"
    assert c["Shannon_entropy_maximum_bits"]>2.32


def test_order_and_normalization():
    c=extrema.verify()
    a_entropy=sp.Rational(16)/(15+3**sp.Rational(6,5))
    assert float(sp.Rational(2,3))<float(sp.Rational(10,13))<float(a_entropy)<1
    assert c["entropy_comparison_bits"]["Shannon"]>c["entropy_comparison_bits"]["linear"]
