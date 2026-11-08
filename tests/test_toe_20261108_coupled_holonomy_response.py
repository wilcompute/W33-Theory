"""Independent derivative, spectral, gauge-profile and bubble controls."""
import importlib.util
import json
from pathlib import Path
import numpy as np
import pytest
from scipy.linalg import eigh
import mpmath as mp

ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("coupled_native_holonomy",ROOT/"analysis/toe_20261108_coupled_holonomy_response.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)

@pytest.fixture(scope="module")
def kernel():return M.ScalarResponse((3,3,3,2),.8)

@pytest.mark.parametrize("nu",[0.,.4,1.2])
def test_scalar_bubble_by_independent_frequency_integral(nu):
    with mp.workdps(35):
        a=mp.mpf('1.3');b=mp.mpf('2.7');n=mp.mpf(str(nu))
        f=lambda t:1/((t*t+a*a)*((t+n)**2+b*b))/(2*mp.pi)
        integral=mp.quad(f,[-mp.inf,-1,0,1,mp.inf])
        closed=(a+b)/(2*a*b*((a+b)**2+n*n))
        assert abs(integral-closed)<mp.mpf('1e-30')

@pytest.mark.parametrize("i,j",[(0,0),(3,3),(0,1),(0,3),(2,3)])
def test_full_four_variable_static_hessian_by_energy_differences(kernel,i,j):
    h=.04;e=np.eye(4);z=np.zeros(4);E=lambda x:M.energy(kernel.sizes,.8,x)
    if i==j:
        v=(-E(2*h*e[i])+16*E(h*e[i])-30*E(z)+16*E(-h*e[i])-E(-2*h*e[i]))/(12*h*h)
    else:
        def mixed(t):
            return (E(t*(e[i]+e[j]))-E(t*(e[i]-e[j]))-E(t*(-e[i]+e[j]))+E(-t*(e[i]+e[j])))/(4*t*t)
        v=(4*mixed(h/2)-mixed(h))/3
    assert v==pytest.approx(kernel.K[i,j],rel=3e-4,abs=8e-9)

def test_previous_single_holonomy_curvature_is_one_Hessian_entry(kernel):
    _,old=M.prior.energy(3,2,.8,0,curvature=True)
    assert kernel.K[3,3]==pytest.approx(old,rel=2e-11,abs=1e-14)

def test_harmonic_and_tree_profiles_static_equal_dynamic_different(kernel):
    tree=M.ScalarResponse((3,3,3,2),.8,profile_mode="tree_without_induced_A0")
    assert np.max(abs(tree.K-kernel.K))<3e-14
    assert np.linalg.norm(tree.Z()-kernel.Z())>1e-5

@pytest.mark.parametrize("s",[0.,.01,.2])
def test_positive_loop_metric_and_strictly_decreasing_kernel(kernel,s):
    G=M.electric_metric(kernel.sizes,.3)
    assert np.linalg.eigvalsh(kernel.Z(s)).min()>0
    assert np.linalg.eigvalsh(kernel.kinetic_at_root(s,.3)-G).min()>0
    assert np.linalg.eigvalsh(kernel.F(s,.3)-kernel.F(s+1e-5,.3)).min()>0

def test_euclidean_frequency_limit_recovers_loop_metric(kernel):
    nu=.001
    finite=(kernel.pi(nu)-kernel.K)/nu**2
    assert np.max(abs(finite-kernel.Z()))<2e-9

@pytest.mark.parametrize("s",[1e-4,.01,.2])
def test_resolvent_moment_error_has_PSD_geometric_bound(kernel,s):
    approx=sum(s**r*z for r,z in enumerate(kernel.moments))
    error=kernel.Z(s)-approx
    ratio=s/(2*kernel.mass)**2
    bound=ratio**3/(1-ratio)*kernel.moments[0]
    assert np.linalg.eigvalsh(error).min()>-1e-17
    assert np.linalg.eigvalsh(bound-error).min()>-1e-17

@pytest.mark.parametrize("g",[.1,.5])
def test_coupled_static_and_dynamic_modes_and_positive_residues(kernel,g):
    r=kernel.modes(g)
    static=np.array(r["static_tree_inertia_squared_frequencies"])
    dynamic=np.array([x["s"] for x in r["dynamic_subthreshold_groups"] for _ in range(x["multiplicity"])])
    assert np.all(dynamic>0) and np.all(dynamic<=static+1e-13)
    assert r["subthreshold_mode_count"]==4
    assert 0<r["theta4_subthreshold_residue_fraction"]<=1+1e-8
    assert all(x["theta4_residue"]>=0 and x["null_residual"]<1e-10 for x in r["dynamic_subthreshold_groups"])
    assert sum(r["static_theta4_weights"])==pytest.approx(1,abs=2e-12)

def test_normal_modes_and_observable_weights_under_coordinate_change(kernel):
    G=M.electric_metric(kernel.sizes);K=kernel.K
    T=np.eye(4);T[0,3]=1.
    a,V=eigh(K,G);b,W=eigh(T.T@K@T,T.T@G@T)
    physical_coordinate=T.T@np.eye(4)[:,3]
    weight_a=V[3]**2/np.linalg.inv(G)[3,3]
    weight_b=(physical_coordinate@W)**2/(physical_coordinate@np.linalg.inv(T.T@G@T)@physical_coordinate)
    assert np.max(abs(a-b))<2e-17
    assert np.max(abs(weight_a-weight_b))<2e-10
    old=K[3,3]*np.linalg.inv(G)[3,3]
    changed=(T.T@K@T)[3,3]*np.linalg.inv(T.T@G@T)[3,3]
    assert abs(old-changed)>1e-6

def test_four_primitive_paths_are_literal_and_independent():
    _,V,a,b,_,_=M.prior.geometry()
    for axis,row in enumerate(M.primitive_paths()):
        v=0;period=np.zeros(4,int)
        for e,s in row["signed_edges"]:
            assert v==(a[e] if s==1 else b[e])
            v=b[e] if s==1 else a[e];period+=s*V[e]
        assert v==0 and period.tolist()==np.eye(4,dtype=int)[axis].tolist()

def test_actual_server_bubbles_and_full_oscillator_bath():
    d=json.loads((ROOT/"data/toe_20261108_coupled_holonomy_server.json").read_text())
    assert d["runtime"]=="Actual functions.exec V8"
    for row in d["bubbles"]:assert row["integral"]==pytest.approx(row["closed"],abs=6e-16)
    b=d["bath"];G=np.array(b["G"]);D=np.array(b["D"]);W=np.array(b["W"]);p=np.array(b["p"])
    full=np.block([[D,W],[W.T,np.diag(p*p)]])
    metric=np.block([[G,np.zeros((2,3))],[np.zeros((3,2)),np.eye(3)]])
    vals,V=eigh(full,metric)
    assert vals.min()>0
    assert np.max(abs(vals[:2]-[r["s"] for r in b["poles"]]))<2e-15
    # Dense generalized eigenvector residues lose more precision than roots.
    # An independent70digit determinant/root calculation gives the same values.
    assert np.max(abs(V[1,:2]**2-[r["second_coordinate_residue"] for r in b["poles"]]))<1e-12
