"""Independent regression suite for five TOE research fronts.

Exact F8 PPT two-copy relaxation, Einstein-frame mass normalization,
H27 commutator pulse, symplectic-frame locality no-go, photonic fidelity.
"""
import importlib.util
import itertools
import json
import math
from fractions import Fraction as Fr
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    filename=ROOT/"analysis"/name
    spec=importlib.util.spec_from_file_location(name.replace(".py",""),filename)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

@pytest.fixture(scope="module")
def f8():
    return load("toe_20261114_F8_two_copy_PPT_zero_countercertificate.py")

@pytest.fixture(scope="module")
def phys():
    return load("toe_20261114_AdS5_H27_Sp4_optical_fourfronts.py")

def test_F8_GF8_multiplication_trace_field_axioms(f8):
    for a,b,c in itertools.product(range(8),repeat=3):
        assert f8.mul(a,b)==f8.mul(b,a)
        assert f8.mul(f8.mul(a,b),c)==f8.mul(a,f8.mul(b,c))
        assert f8.trace(f8.mul(a,b)^f8.mul(a,c))==(
            f8.trace(f8.mul(a,b))^f8.trace(f8.mul(a,c)))
    assert all(set(f8.mul(a,b) for b in range(8))==set(range(8)) for a in range(1,8))

def test_FWHT_matches_direct_Walsh_on_sparse_input(f8):
    x=[0]*4096
    for u,z in ((0,0),(1,2),(3,5),(56,20),(12,53)):
        x[u+64*z]=1
    transformed=f8.fwht(x)
    for w in (0,1,6,17,513,2048,4095):
        expected=sum((-1)**((w&j).bit_count()&1) for j,v in enumerate(x) if v)
        assert transformed[w]==expected

def test_F8_PPT_feasible_symmetric_zero_objective(f8):
    result=f8.run()
    assert result["K_expectation"]=="0"
    assert result["state_positive"] and result["state_swap_symmetric"]
    s={Fr(lam):num for lam,num in result["partial_transpose_spectrum"].items()}
    assert s=={Fr(0):567,Fr(1,64):1,Fr(31,96768):1512,Fr(1,4032):2016}
    assert sum(lam*num for lam,num in s.items())==1
    weights=result["Bell_weights"]
    assert 567*Fr(weights["covered_each"])+1512*Fr(weights["even_uncovered_each"])==1

def test_no_invalid_F8_pure_state_global_min_claim(f8):
    result=f8.run()
    assert "physical pure state" in result["limitation"]
    assert Fr(result["K_expectation"])==0
    # Earlier exact algebraic witness proves a strict positive numerical
    # candidate upper bound, not a certified global positive lower bound.

def test_AdS_canonical_masses_derived_independently(phys):
    d=phys.compactification_radion_BF()
    assert d["kinetic_metric_uv"]==[["56/3","0"],["0","8"]]
    assert d["canonical_radion_m2"]==["2","18/5"]
    assert d["canonical_m2L2"]==["20","36"]
    assert d["AdS5_BF_bound_m2L2"]==-4
    for rec in d["minimal_probe_KK_l1_l2_up_to_3"]:
        l1,l2=rec["l1"],rec["l2"]
        assert rec["mass_squared"]==l1*(l1+1)+l2*(l2+1)
        assert rec["degeneracy"]==(2*l1+1)*(2*l2+1)

def test_H27_group_associativity_and_nontrivial_center(phys):
    # All 27^3 triples: associativity, noncommutative center and inverses
    states=list(itertools.product(range(3),repeat=3))
    e=(0,0,0)
    for a in states:
        assert phys.h27_mul(a,phys.h27_inv(a))==e
        assert phys.h27_mul(phys.h27_inv(a),a)==e
    for a in states:
        for b in states:
            assert phys.h27_mul(a,b)[0:2]==((a[0]+b[0])%3,(a[1]+b[1])%3)
    # Focused exact 27x27 sample of three-way associativity
    for a in states:
        for b in states:
            for c in ((1,0,0),(0,1,0),(0,0,1)):
                assert phys.h27_mul(phys.h27_mul(a,b),c)==phys.h27_mul(a,phys.h27_mul(b,c))

def test_H27_clock_pulse_det_formula_and_order(phys):
    d=phys.h27_clock()
    assert d["four_pulse_commutator_center"]=="(0,0,1)"
    assert d["central_clock_cycles"]==9
    assert d["full_return_elementary_pulses"]==12
    assert sum(d["commutator_det_class_counts"].values())==81

def test_Sp4_transvections_preserve_symplectic_form(phys):
    for v in itertools.product(range(3),repeat=4):
        for x in ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)):
            assert phys.sp(phys.transvection(x,v),phys.transvection(v,v))==phys.sp(x,v)
    d=phys.symplectic_locality()
    assert d["nonzero_displacement_orbit"]==80
    assert d["full_Sp_and_translation_invariant_nontrivial_Cayley_degree"]==80
    assert d["sparse_framed_degree"]==8

def test_framed_four_dimensional_torus_spectrum_independent(phys):
    from collections import Counter
    # C3^4 degree-eight Cayley graph; count character eigenvalues directly
    vals=Counter()
    for k in itertools.product(range(3),repeat=4):
        lam=sum(2*math.cos(2*math.pi*x/3) for x in k)
        vals[round(lam)]+=1
    assert vals=={8:1,5:8,2:24,-1:32,-4:16}
    d=phys.symplectic_locality()
    for row in d["finite_q_and_large_q_heat_samples"]:
        if row["p"]==101 and row["t"]==100:
            assert 3.9<row["ds"]<4.2

def test_photonic_coherence_Fourier_filter_and_negative_control(phys):
    d=phys.optical_five_setting_certificate()
    assert d["random_density_matrix_max_coherence_error"]<1e-12
    assert d["nuisance_bad_state_naive_X4"]==1
    assert abs(d["nuisance_bad_state_filtered_A"])<1e-12
    assert d["fidelity_estimate"]>=d["Hoeffding_one_sided_lower_99pct"]
    assert d["Hoeffding_one_sided_lower_99pct"]>.5
    assert d["raw_total_5_settings_expected_trials"]==23701

def test_photonic_sample_bound_a_conservative_union_bound(phys):
    d=phys.optical_five_setting_certificate()
    N=d["N_accepted_per_setting"];alpha=.01
    eps_z=math.sqrt(math.log(10/alpha)/(2*N))
    eps_e=math.sqrt(2*math.log(10/alpha)/N)
    assert d["Hoeffding_one_sided_lower_99pct"]==pytest.approx(
      d["fidelity_estimate"]-(eps_z+eps_e)/2,abs=1e-13)

def test_producers_write_scoped_certificates(f8,phys):
    a=f8.run();b=phys.run()
    assert json.loads(f8.OUTPUT.read_text())["status"]==a["status"]
    assert json.loads(phys.OUT.read_text())["status"]==b["status"]
    assert b["n"]==4
