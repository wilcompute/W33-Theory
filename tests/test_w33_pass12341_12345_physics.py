"""Cross-check microscopic response, charges, and the truncated integral."""
from pathlib import Path
import sys
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.sparse import kron,eye,diags,csr_matrix
from scipy.sparse.linalg import eigsh

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12341_12345_physics as core


def test_interacting_response_and_ward_identity():
    x=core.interacting_six_loop_response(2.)
    assert x['hilbert_dimension']==1849
    assert x['sampled_lowest_gap']>.05
    assert x['ground_Ritz_residual']<1e-9
    assert x['combined_gauge_density_ward_residual']<1e-9
    assert x['max_projected_resolvent_residual']<1e-8
    assert x['best_common_cone_relative_residual']>.59
    assert x['static_vs_electric_relative_residual']>.68


def test_interacting_hessian_with_a_second_independent_phase_direction():
    r=core.interacting_six_loop_response(2.)
    _,_,dual,_,edges,K,_,_,_=core.six_loop_operators()
    I=eye(43,format='csr');onsite=diags(2*np.eye(43).reshape(-1),format='csr')
    def energy(t):
        z=K.astype(complex)
        for e,(a,b) in enumerate(edges):
            z[b,a]=-np.exp(1j*t*dual[e,0]);z[a,b]=z[b,a].conjugate()
        M=csr_matrix(z);H=kron(M,I,format='csr')+kron(I,M,format='csr')+onsite
        return float(eigsh(H,k=1,which='SA',tol=1e-12,v0=np.ones(1849),return_eigenvectors=False)[0])
    eps=.001
    fd=(energy(eps)+energy(-eps)-2*energy(0))/eps**2
    assert abs(fd-r['static_hessian'][0][0])<1e-6


def test_free_fock_static_response_is_indefinite_and_electric_positive():
    r=core.six_loop_response(0.,.3)
    assert r['static_eigenvalues'][0]<-.08 and r['static_eigenvalues'][-1]>.04
    assert r['electric_eigenvalues'][0]>.019
    assert r['best_common_cone_relative_residual']>.99
    assert r['finite_difference_absolute_error']<1e-6


def test_projected_16_and_full_27_have_distinct_anomaly_inventories():
    r=core.charge_anomalies()
    sixteen=r['chiral_16'];full=r['complete_27']
    assert [sixteen[k] for k in ('SU5_squared_U1psi','gravitational_U1psi','U1psi_cubed','U1chi_squared_U1psi')]==[4,16,16,80]
    assert sixteen['SU5_cubic']==0
    assert all(v==0 for k,v in full.items() if k!='dimension')


def test_analytic_tau2_integration_against_direct_two_dimensional_quadrature():
    R=.4;x,weights,lo=core.angular_nodes(40);nmax=3;wmax=12;upper=40.
    def integral(t,angle):
        value=0.
        for q,ell,mult in ((0.,0.,-222),(.5,0.,288),(.5,-1/6,-16)):
            n,w=np.meshgrid(np.arange(nmax+1)+q,np.arange(wmax+1),indexing='ij')
            factors=np.where(n==0,1,2)*np.where(w==0,1,2)
            a=np.pi*(n*n/R**2+w*w*R**2+4*ell)
            value+=mult*np.sum(factors*np.exp(-t*a)*np.cos(2*np.pi*angle*n*w))/t**3
        return value
    direct=sum(weight*quad(integral,float(low),upper,args=(float(angle),),epsabs=1e-9)[0]
               for angle,weight,low in zip(x,weights,lo))
    reduced=core.string_potential(R,nmax=nmax,wmax=wmax,nodes=40,upper=upper)[0][0]
    assert abs(direct-reduced)<1e-8


def test_string_slope_and_threshold_log_coefficient():
    R=.55;eps=1e-5
    fd=(core.string_potential(R+eps)[0][0]-core.string_potential(R-eps)[0][0])/(2*eps)
    assert abs(fd-core.string_potential(R)[0][1])<1e-5
    r=sp.sqrt(sp.Rational(3,8))
    assert sp.simplify(32*(sp.pi/(2*r**3))**2-4096*sp.pi**2/27)==0
    a=core.string_audit()
    assert a['min_sampled_slope']>160
    assert abs(a['original_R04_T40']-a['exact_tau2_same_rectangle_T40'])<.02
    assert abs(a['exact_tau2_same_rectangle_T40']-a['exact_tau2_gauss_angular_T40'])>.7
