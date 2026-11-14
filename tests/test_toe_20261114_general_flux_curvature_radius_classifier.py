"""Independent exact regressions for the conditional Einstein-frame radius classifier."""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util
import json
import sympy as sp

SRC=Path(__file__).resolve().parents[1]/"analysis"/"toe_20261114_general_flux_curvature_radius_classifier.py"
spec=importlib.util.spec_from_file_location("flux_classifier",SRC)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def test_dimension_and_flux_degree_grid():
    for d in range(3,10):
        for n in range(2,9):
            for p in range(1,n+1):
                z=mod.powers(d,n,p)
                assert z["flux_power"] == -Q(2*p)-Q(2*n,d-2)
                assert z["raw"] + z["weyl"] == z["flux_power"]
                assert z["flux_decay"]>0

def test_t4_p3_reproduces_preexisting_exact_case():
    z=mod.powers(5,4,3)
    assert (z["raw"],z["weyl"],z["flux_power"])==(-2,-Q(20,3),-Q(26,3))

def test_flux_only_derivative_negative():
    R=sp.symbols("R",positive=True)
    for d,n in [(3,2),(5,4),(7,6)]:
        terms=[(p,Q(p,7)) for p in range(1,n+1)]
        V=sum(sp.Rational(A.numerator,A.denominator)*R**(-sp.Rational(mod.powers(d,n,p)["flux_decay"].numerator,mod.powers(d,n,p)["flux_decay"].denominator)) for p,A in terms)
        D=sp.simplify(R*sp.diff(V,R))
        assert all(float(D.subs(R,r))<0 for r in [Q(1,3),1,3,10])

def test_one_flux_curvature_exact_stationary_hessian_and_energy():
    R=sp.symbols("R",positive=True)
    z=mod.one_flux_balance(5,4,3)
    a=sp.Rational(26,3);c=sp.Rational(14,3)
    V=R**(-a)-R**(-c)
    Rstar=(sp.Rational(13,7))**sp.Rational(1,4)
    D=R*sp.diff(V,R)
    H=R*sp.diff(D,R)
    assert sp.simplify(D.subs(R,Rstar))==0
    assert sp.simplify(H.subs(R,Rstar)-a*(a-c)*Rstar**(-a))==0
    assert sp.simplify(V.subs(R,Rstar)+sp.Rational(6,7)*Rstar**(-a))==0
    assert z["radius_power_value"]==Q(13,7)

def test_degree_one_curvature_has_same_power():
    z=mod.one_flux_balance(5,4,1)
    assert z["branch"]=="degenerate_same_radial_scaling"
    assert not z["isolated_stationary"]

def test_multiflux_curvature_uniqueness_and_no_go():
    z=mod.multi_flux_balance(5,4,[(2,1),(3,2)],1)
    assert z["unique"] and z["radially_stable"] and z["vacuum_energy_negative"]
    assert not z["full_background_solution_certified"]
    assert not mod.multi_flux_balance(5,4,[(2,1),(3,2)],0)["exists"]
    assert not mod.multi_flux_balance(5,4,[(1,2),(3,1)],1)["exists"]

def test_certificate_and_scope():
    data=mod.main()
    assert data["torus_T4_flux_only_runaway"]
    assert data["positive_flux_only_no_critical_point"]
    assert "no proof of full moduli stability" in data["scope"]
    assert "No curvature term" in data["topology_guard"]
