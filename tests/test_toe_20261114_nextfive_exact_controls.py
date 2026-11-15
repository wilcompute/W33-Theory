"""Independent exact and numerical controls of five TOE frontiers."""
import importlib.util
from collections import Counter
from fractions import Fraction as Q
from itertools import product,combinations
import json
import math
from pathlib import Path
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis"/"toe_20261114_nextfive_f8_flux_cursor_frame_optical.py"

@pytest.fixture(scope="module")
def m():
    spec=importlib.util.spec_from_file_location("toe_nov14_new_five",SRC)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def test_integrated_five_fronts_exact_reproducer(m):
    out=m.run()
    assert len(out["results"])==5 and out["n_fronts"]==5
    assert all(d["status"] for d in out["results"].values())
    assert json.loads(m.OUT.read_text())["status"]==out["status"]

def test_F8_4096_Pauli_second_moment_shells(m):
    r=m.f8_ppt_covariance_gap()
    q={name:(Q(v["value"]),v["count"]) for name,v in r["second_moments_multiset"].items()}
    assert q["identity"]==(Q(1),1)
    assert q["covered"]==(Q(0),567)
    assert q["even_uncovered"]==(Q(31,1512),1512)
    assert q["odd_uncovered"]==(Q(1,63),2016)
    assert sum(v[0]*v[1] for v in q.values())==64

def test_F8_PPT_zero_not_necessarily_global_min(m):
    r=m.f8_ppt_covariance_gap()
    assert r["twocopy_symmetric_PPT_K_objective"]==0
    assert r["all_diagonal_Pauli_covariances_nonnegative"]
    assert "not certified" in r["limitation"]

def test_flux_symbolic_stationary_equations(m):
    import sympy as sp
    t=sp.symbols("t",positive=True)
    charges_ratio=t*t*(t+6)/(6*t+1)
    d=sp.factor(sp.diff(charges_ratio,t))
    assert d==3*t*(4*t*t+13*t+4)/(6*t+1)**2
    for x in (sp.Rational(1,17),sp.Rational(1,3),sp.Rational(1),sp.Rational(9,4),sp.Rational(17)):
        r2=sp.factor(5*x/(8*(6*x+1)))
        r1=x*r2
        n1sq=charges_ratio.subs(t,x)
        f1=n1sq/(4*r1*r1);f2=1/(4*r2*r2)
        assert sp.simplify(1/r1-(6*f1-f2)/14)==0
        assert sp.simplify(1/r2-(6*f2-f1)/14)==0
        Lsq=56/(f1+f2)
        assert sp.simplify(Lsq/r1-20/(1+x))==0
        assert sp.simplify(Lsq/r2-20*x/(1+x))==0

def test_flux_radion_mass_matrix_generalized_eigen(m):
    import sympy as sp
    t=sp.symbols("t",positive=True)
    delta=(t-1)/(t+1)
    M=sp.Matrix([[20,-sp.Rational(60,7)*delta],[-20*delta,36]])
    eigs=[28+sgn*8*sp.sqrt(1+sp.Rational(75,28)*delta**2) for sgn in (-1,1)]
    assert sp.simplify(sum(eigs)-sp.trace(M))==0
    assert sp.simplify(eigs[0]*eigs[1]-M.det())==0
    for k in (sp.Rational(1,1000),sp.Rational(1,2),sp.Rational(1),sp.Rational(3),sp.Rational(1000)):
        assert float(eigs[0].subs(t,k))>12
    assert float(eigs[1].subs(t,1))==36

def test_flux_probe_gap_collapses_while_radion_stays_positive(m):
    r=m.flux_branch_charge_theorem()
    xs=r["branch_examples"]
    assert all(x["radion_m2L2"][0]>12 for x in xs)
    assert xs[0]["first_probe_levels_m2L2"]==pytest.approx([20,20],abs=1e-12)
    assert xs[-1]["first_probe_levels_m2L2"][0]<xs[0]["first_probe_levels_m2L2"][0]
    assert r["radion_m2L2_strict_lower_limit"]>12

def test_H27_cursor_symmetry_and_exact_period(m):
    r=m.h27_autonomous_cursor()
    assert r["permutation_sites"]==108
    assert r["cycles_of_length_12"]==9
    assert r["twelve_step_operator"]=="identity"
    assert r["exact_H_log_offdiagonal_nonzero_per_12cycle"]>24

def test_H27_base_permutation_and_center_independent(m):
    base=m.local_module("toe_20261114_AdS5_H27_Sp4_optical_fourfronts.py")
    X=(1,0,0);Y=(0,1,0);Z=(0,0,1)
    assert base.h27_comm(X,Y)==Z
    assert all(base.h27_mul(Z,(a,b,c))==(a,b,(c+1)%3)
               for a,b,c in product(range(3),repeat=3))

def test_frame_all_three_orbitals_and_isotropy(m):
    r=m.w33_frame_correlation_tensor()
    assert r["apartments"]==1620
    assert r["each_displacement_frame_incidence"]==162
    types={x["pair_type"]:(x["cooccurrence"],x["number_of_unordered_nonzero_displacement_pairs"],x["joint_probability"])
           for x in r["frame_pair_count_types"]}
    assert types=={
      "opposite":(162,40,"1/10"),
      "symplectic_orthogonal":(27,960,"1/60"),
      "symplectic_nonorthogonal":(6,2160,"1/270")
    }
    assert r["nonconstant_Fourier_mode_variance"]=="729/100"

def test_averaged_frame_graph_erases_locality(m):
    r=m.w33_frame_correlation_tensor()
    assert r["uniform_averaged_adjacency"]=="(J-I)/10, nonlocal complete weighted graph"
    assert r["single_frame_adjacency_spectrum"]=={"8":1,"5":8,"2":24,"-1":32,"-4":16}
    assert sum(int(x)*mult for x,mult in r["single_frame_adjacency_spectrum"].items())==0

def test_detector_allocation_is_better_than_uniform(m):
    r=m.optical_optimal_detector_budget()
    n=r["Hoeffding_allocated_accepted_shots"]
    assert n["Z"]>n["each_equatorial"]
    assert r["raw_optimal_expected_launches"]<r["raw_equal_allocation_expected_launches"]
    assert r["Hoeffding_actual_statistical_width"]<=r["statistical_fidelity_halfwidth_target"]
    assert r["model_conditional_fidelity_lower_99pct"]>.5

def test_detector_worst_case_bias_from_first_principles(m):
    r=m.optical_optimal_detector_budget()
    lam=Q(1,100); dz=Q(5,1000);de=Q(1,100)
    expected=Q(1,2)*lam+4*Q(1,8)*(2*lam)+Q(1,2)*dz+4*Q(1,8)*de
    assert expected==Q(9,400)
    assert r["worst_case_adversarial_fidelity_bias"]=="9/400"

def test_detector_negative_control_not_falsely_positive(m):
    r=m.optical_optimal_detector_budget()
    assert r["negative_control_filtered_false_GHZ"]==0

def test_against_parallel_F8_exact_witness_caveat(m):
    r=m.f8_ppt_covariance_gap()
    candidate=(47-32*math.cos(2*math.pi/9))/9
    assert 2<candidate<3
    assert r["twocopy_symmetric_PPT_K_objective"]==0
    assert "No new global c8 bound" in r["limitation"]
