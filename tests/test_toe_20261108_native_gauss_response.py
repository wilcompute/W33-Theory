"""Direct temporal integrals, full native Ward and constrained mode controls."""
import importlib.util
import json
from pathlib import Path
import numpy as np
import pytest
import mpmath as mp
from scipy.linalg import eigh

ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("native_full_gauss",ROOT/"analysis/toe_20261108_native_gauss_response.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)

@pytest.fixture(scope="module")
def response():return M.FullResponse((2,2,2,2),.8)

@pytest.mark.parametrize("nu",[0.,.4,1.2])
@pytest.mark.parametrize("power",[0,1,2])
def test_independent_temporal_frequency_integrals(nu,power):
    with mp.workdps(35):
        a=mp.mpf('1.3');b=mp.mpf('2.7');v=mp.mpf(str(nu));p=a+b
        f=lambda t:(2*t+v)**power/((t*t+a*a)*((t+v)**2+b*b))/(2*mp.pi)
        direct=mp.quad(f,[-mp.inf,-1,0,1,mp.inf])
        values=[p,(b-a)*v,p*(4*a*b+v*v)]
        exact=values[power]/(2*a*b*(p*p+v*v))
        assert abs(direct-exact)<mp.mpf('1e-29')

def test_full_native_dimension_and_exact_chain_constraints(response):
    B,V,_,_,H,C,L,Q,F,T=M.zero_momentum_geometry((2,2,2,2))
    assert F.shape==(105,135) and T.shape==(135,135)
    assert C.shape==(135,105) and Q.shape==(27,26)
    assert not (F@B).any() and not (F@V).any()
    assert np.max(abs(Q.T@np.ones(27)))<2e-15
    assert np.max(abs(Q.T@Q-np.eye(26)))<2e-15
    assert response.static_gauge_residual<1e-12

def test_temporal_vertices_verify_ward_independently(response):
    assert response.commutator_residual<1e-12
    for r in response.ward_controls:
        assert r["full161by161_Ward_residual"]<1e-14
        assert r["direct_mixed_vs_spatial_max"]<1e-14
        assert r["direct_density_vs_spatial_max"]<1e-14
        assert r["uniform_charge_density_response"]<1e-25

def test_omitted_temporal_seagull_is_detected(response):
    for r in response.ward_controls:
        assert r["direct_contact_minus_bubble_agreement"]<1e-13
        assert r["omitted_temporal_contact_Ward_residual"]>1e-4

def test_static_harmonic_block_matches_prior_fullband(response):
    old=M.old.ScalarResponse((2,2,2,2),.8)
    assert np.max(abs(old.K-response.K[:4,:4]))<2e-14

def test_positive_gauss_loop_metric_is_below_clamped_loop_metric(response):
    E=response.tree_electric+response.moments[0]
    reduced=M.schur(E,109)
    base=response.tree_electric[:109,:109]
    assert np.linalg.eigvalsh(reduced-base).min()>-2e-12
    assert np.linalg.eigvalsh(E[:109,:109]-reduced).min()>-2e-12

@pytest.mark.parametrize("s",[0.,.001])
def test_temporal_elimination_repairs_tree_profile_change(response,s):
    r=response.profile_invariance(s,.5)
    assert r["Gauss_reduced_profile_error"]<2e-11
    assert r["clamped_profile_change"]>1
    assert r["zero_static_gauge_block_error"]<1e-14

def test_temporal_basis_change_does_not_change_reduced_response(response):
    O=np.linalg.qr(np.random.default_rng(44).normal(size=(26,26)))[0]
    S=np.eye(135);S[109:,109:]=O
    E=response.tree_electric+response.Zmoment(.001)
    assert np.max(abs(M.schur(E,109)-M.schur(S.T@E@S,109)))<2e-12

def test_optical_coordinate_change_is_not_a_magnetic_action_change(response):
    response.use_magnetic("basis105")
    A=response.physical(.0001)
    S=np.eye(109);S[4,5]=.2
    assert np.max(abs(M.schur(A,4)-M.schur(S.T@A@S,4)))<2e-12
    before=M.schur(A,4);response.use_magnetic("all1287")
    after=M.schur(response.physical(.0001),4)
    assert np.linalg.norm(after-before)>1e-12

def test_all_short_faces_preserve_controller_basis_rows_do_not():
    full,d=M.magnetic_prescriptions()
    assert full.shape==(135,135)
    assert d["all_face_count"]==1287 and d["selected_basis_count"]==105
    assert d["all_faces_H27_exact_max_error"]==0
    assert d["selected_basis_H27_exact_max_error"]>0
    assert d["selected_basis_broken_controller_count"]==26

def test_adding_face_rows_is_a_positive_hessian_change():
    full,_=M.magnetic_prescriptions()
    F=M.zero_momentum_geometry((2,2,2,2))[-2]
    assert np.linalg.eigvalsh(full-F.T@F).min()>-2e-12

@pytest.mark.parametrize("g",[.5,1.])
def test_gauss_optical_poles_ordering_and_unexpanded_residues(response,g):
    results={}
    for name in ("basis105","all1287"):
        response.use_magnetic(name);r=response.modes(g)
        full=np.array(r["full_gauss_and_optical_squared_frequencies"])
        gauss=np.array(r["gauss_but_optical_clamped_squared_frequencies"])
        fixed=np.array(r["clamped_temporal_and_optical_squared_frequencies"])
        assert np.all(full>0) and np.all(full<=gauss+2e-13)
        assert np.all(fixed<=gauss+2e-13)
        assert sum(z["multiplicity"] for z in r["full_low_groups"])==4
        assert all(z["theta4_residue"]>=0 and z["unexpanded_low_kernel_residual"]<2e-10 for z in r["full_low_groups"])
        results[name]=full
    assert np.all(results["basis105"]<=results["all1287"]+2e-13)
    assert abs(results["all1287"][0]-results["all1287"][1])<2e-13
    assert abs(results["basis105"][0]-results["basis105"][1])>1e-11

def test_full_constrained_equations_reconstruct_low_schur_mode(response):
    response.use_magnetic("all1287")
    r=response.modes(.5);s=r["full_gauss_and_optical_squared_frequencies"][0]
    P=response.physical(s,.5,exact=True)
    _,U=eigh(M.schur(P,4));h=U[:,0]
    spatial=np.r_[h,-np.linalg.solve(P[4:,4:],P[4:,:4]@h)]
    E=response.tree_electric/.5**2+response.Zexact(float(s))
    A0=-np.sqrt(s)*np.linalg.solve(E[109:,109:],E[109:,:109]@spatial)
    K=response.K[:109,:109]+response.tree_magnetic[:109,:109]/.5**2
    full=np.block([[K-s*E[:109,:109],-np.sqrt(s)*E[:109,109:]],
                   [np.sqrt(s)*E[109:,:109],E[109:,109:]]])
    assert np.linalg.norm(full@np.r_[spatial,A0])<3e-10

def test_exact_reduced_slope_by_finite_difference(response):
    response.use_magnetic("basis105")
    s=.0002;eps=1e-6
    finite=-(response.low(s+eps,exact=True)-response.low(s-eps,exact=True))/(2*eps)
    analytic=response.slope_low(s)
    assert np.max(abs(finite-analytic))<2e-7
    assert np.linalg.eigvalsh(analytic).min()>0

def test_actual_server_temporal_integrals_and_nested_complex_schur():
    d=json.loads((ROOT/"data/toe_20261108_native_gauss_server.json").read_text())
    assert d["runtime"]=="Actual functions.exec V8"
    for r in d["integrals"]:
        assert np.max(abs(np.array(r["quadrature"])-r["closed"]))<5e-15
        assert r["density_contact"]-r["closed"][2]==pytest.approx(r["density_after_contact"],abs=1e-15)
    E=np.array(d["toy"]["E"]);K=np.diag(d["toy"]["K"])
    for r in d["toy"]["cases"]:
        nu=r["nu"]
        W=np.block([[K+nu*nu*E[:3,:3],1j*nu*E[:3,3:]],
                    [-1j*nu*E[3:,:3],E[3:,3:]]])
        independent=1/np.linalg.inv(W)[0,0]
        assert independent.imag==pytest.approx(0,abs=1e-14)
        assert independent.real==pytest.approx(r["low_kernel"],abs=2e-15)
        assert r["profile_reduced_error"]<1e-14
