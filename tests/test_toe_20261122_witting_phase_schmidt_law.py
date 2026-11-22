"""Parameterized exact Witting Schmidt-spectrum regression."""
import sys
from pathlib import Path
import sympy as sp

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261122_witting_phase_schmidt_law as phase


def test_symbolic_all_phases():
    d=phase.verify()
    assert d["status"]=="PASS_EXACT_ALL_PHASES"
    assert d["squared_operator_schmidt_spectrum"]==(
        ["16-15a","9a"]+["a"]*6+["0"]*8)
    assert d["fidelity_k2"]=="F_avg <= 1-4a/17"
    assert d["crossing"]=="a=2/3, cos(theta)=-1/3; dominant squared values 6 and 6"


def test_phase_specializations():
    a=sp.symbols("a",real=True)
    assert (16-15*a).subs(a,sp.Rational(1,2)) == sp.Rational(17,2)
    assert (9*a).subs(a,sp.Rational(1,2)) == sp.Rational(9,2)
    assert sp.simplify(1-4*a/17).subs(a,sp.Rational(1,2))==sp.Rational(15,17)
    assert sp.solve(16-15*a-9*a,a)==[sp.Rational(2,3)]
