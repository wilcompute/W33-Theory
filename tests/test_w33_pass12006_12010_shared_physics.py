"""Independent controls on shared flavour, colored thresholds, density and SU3 paths."""
import sys,json,itertools
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import null_space,eigh
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12006_vacuum_source_identifiability as vacuum
import w33_pass12007_shared_theta_leptons as flavour
import w33_pass12008_colored_soft_thresholds as soft
import w33_pass12009_native_metric_density as density
import w33_pass12010_nonabelian_native_index as native
from w33_pass11995_native_metric_gr_lift import inputs,lift,homogenize
from w33_pass11991_native_four_period_cover import bloch_incidence,native_geometry

def read(stem):return json.loads((ROOT/'data'/('w33_pass'+stem+'.json')).read_text())

def test_actual_CP_source_and_real_coefficient_map():
    d=vacuum.payload();h=np.array(d['actual_source_h_real'])+1j*np.array(d['actual_source_h_imag']);C=np.array(d['fitted_real_C']);b=flavour.inputs()[3]
    assert np.max(abs(C@h-b))<1e-11 and np.max(abs(C@h.conj()-b.conj()))<1e-11
    assert abs(np.imag(np.vdot(h,h)))<1e-14

def test_positive_auxiliary_square_congruence_without_fitting_eigenvalues():
    rng=np.random.default_rng(36);H=rng.normal(size=(9,9));H=H.T@H;H[0]=0;H[:,0]=0;J=rng.normal(size=(6,9));K=np.diag(np.arange(1,7))
    B=np.block([[H+J.T@K@J,-J.T@K],[-K@J,K]])
    change=np.block([[np.eye(9),np.zeros((9,6))],[J,np.eye(6)]])
    target=np.zeros((15,15));target[:9,:9]=H;target[9:,9:]=K
    assert np.max(abs(change.T@B@change-target))<1e-12
    assert sum(np.linalg.eigvalsh(B)>1e-8)==14

def test_quark_flat_fibre_is_lifted_by_shared_charged_ratios():
    Jq=flavour.jacobian(flavour.FIT,False);J=flavour.jacobian(flavour.FIT);Z=null_space(Jq)
    assert Z.shape==(8,2) and np.linalg.norm(Jq@Z)<1e-10
    assert min(np.linalg.svd(J,compute_uv=False))>.006
    assert min(np.linalg.eigvalsh(Z.T@J[6:].T@J[6:]@Z))>1e-6
    J2=flavour.jacobian(flavour.FIT,step=5e-6)
    assert np.linalg.norm(J-J2)/np.linalg.norm(J)<1e-5

def test_all_ten_charged_comparators_and_common5bar_matching():
    q,e,charged,A=flavour.joint_observables();u,d,eb,b,A=flavour.inputs()
    assert max(abs(q[k]/flavour.DATA[k]-1) for k in q)<1e-7
    assert max(abs(e[k]/flavour.LEPTONS[k]-1) for k in e)<1e-7
    K=np.eye(3)-np.outer(b.conj(),b)/(1+np.vdot(b,b).real)
    assert np.max(abs(A@A-K))<1e-12 and np.max(abs(A-A.conj().T))<1e-12
    assert np.max(abs(charged-A.T@eb.T))<1e-12
    assert np.linalg.norm(charged-eb.T@A)>.001
    # Anindependentabsoluteintersectorcomparatorfails atthe declaredMZscale.
    sb=np.linalg.svd(d@A,compute_uv=False)[0];st=np.linalg.svd(charged,compute_uv=False)[0]
    assert abs((sb/st)/(2.86/1.74624)-1)>.3

def test_real_Majorana_with_same_complex_source_and_Takagi_control():
    obs,d=flavour.neutrino();oc,dc=flavour.neutrino(conjugate=True)
    assert max(abs(obs/flavour.NEUTRINO_TARGET-1))<1e-7
    n=np.array(d['real_bare_Majorana']);assert min(np.linalg.eigvalsh(n))>0
    _,_,_,A=flavour.joint_observables();nu=A.T@n@A;U,sv,Vh=np.linalg.svd(nu);right=Vh.conj().T
    diagonal=right.T@nu@right
    assert np.max(abs(diagonal-np.diag(np.diag(diagonal))))<1e-12
    assert abs(dc['J']+d['J'])<1e-12 and max(abs(oc-obs))<1e-12
    # Fourconstraints onfiveMajorana shapeparameters leavea localfree direction.
    p=flavour.NEUTRINO_FIT;h=1e-5
    J=np.column_stack([(np.log(flavour.neutrino(p+h*v)[0])-np.log(flavour.neutrino(p-h*v)[0]))/(2*h) for v in np.eye(5)])
    assert np.linalg.matrix_rank(J,tol=1e-6)==4

def test_aligned_colored_threshold_for_actual_and_new_complex_mass():
    rng=np.random.default_rng(22)
    M=soft.full_mass();r=soft.threshold(M)
    assert abs(r['theta_quark'])<1e-11 and abs(r['theta_gluino'])<1e-11
    # Independentmatrix testsSVDalignment beyondthe fittedBarrpattern.
    z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));M=z+3*np.eye(4)
    r=soft.threshold(M);assert abs(r['theta_colored_sum'])<1e-11

def test_colored_misalignment_CP_and_no_decoupling_by_common_scaling():
    M=soft.full_mass();r=soft.threshold(M,.01);c=soft.threshold(M.conj(),.01)
    assert abs(r['theta_colored_sum'])>1e-10
    assert abs(r['theta_colored_sum']+c['theta_colored_sum'])<1e-12
    r3=soft.threshold(3*M,.03,mg=2.1,a=.9,soft2=36)
    assert abs(r3['theta_colored_sum']-r['theta_colored_sum'])<1e-12

def test_aligned_upper_block_can_be_nonzero_but_generic_leak_changes_phase():
    M=soft.full_mass();m=M[:3,:3];b=M[3,:3];r=.001
    M[:3,3]=r*m@b.conj();assert np.linalg.norm(M[:3,3])>1e-4
    expected=np.linalg.det(m)*(1-r*np.vdot(b,b).real)
    assert expected>0 and abs(np.linalg.det(M)/expected-1)<1e-11
    M[:3,3]+=1e-6*np.array([.3,-.4,.2]);assert abs(np.angle(np.linalg.det(M)))>1e-7

def test_metric_density_non_diagonal_and_dimension_dependence():
    H=np.array([[2,.2,.1,0],[.2,3,.3,.1],[.1,.3,2,.2],[0,.1,.2,4]])
    M,G=density.geometric(H);assert abs(M-1/np.sqrt(np.linalg.det(G)))<1e-12
    assert np.max(abs(M*G-H))<1e-12
    a=np.array([[2,.2,0],[.2,3,.1],[0,.1,4.]])
    mass,g=density.geometric(a,3);assert abs(mass-np.linalg.det(a))<1e-12

def test_actual_native_generalized_Bloch_metric_with_capacity():
    b,v,C,H0=inputs();H0=np.array(H0,float);target=H0.copy();target[0,2]+=1e-5;target[2,0]+=1e-5
    selected=read('11995_native_metric_gr_lift')['selected_edge_indices'];w,_=lift(target,b,v,selected);M,G=density.geometric(target)
    edges=native_geometry()[1];direction=np.array([.3,-.2,.4,.1]);expected=direction@G@direction;errors=[]
    for spacing in [.02,.01]:
        B,_=bloch_incidence(edges,v,spacing*direction);ev=np.linalg.eigvalsh(B.conj().T@(w[:,None]*B)/M)
        errors.append(abs(ev[0]/spacing**2-expected))
    assert errors[1]<errors[0]/3

def test_fixed_capacity_extra_scalar_heat_term_independent_quadrature():
    eps=.12
    I=(2*np.pi)**3*quad(lambda x:np.exp(-2*eps*np.cos(x))*(eps*np.sin(x))**2,0,2*np.pi,epsabs=1e-12)[0]
    a2=(2*np.pi)**3*quad(lambda x:-np.exp(-2*eps*np.cos(x))*(-eps*np.cos(x)+(eps*np.sin(x))**2),0,2*np.pi,epsabs=1e-12)[0]
    assert abs(a2+3*I)<1e-10
    d=read('12009_native_metric_density')['conformal_fixed_capacity'];assert abs(d['integrated_R_over6']-I)<1e-10

def test_noncommuting_native_links_gauge_covariance_and_unitarity():
    rng=np.random.default_rng(60010);C=np.array([[native.su3(rng) for _ in range(4)] for _ in range(2)]);gauge=np.array([[native.su3(rng) for _ in range(27)] for _ in range(2)])
    _,S,L,edges=native.compile_native(C,np.array([1,2,1,1]));_,T,Lg,_=native.compile_native(C,np.array([1,2,1,1]),gauge)
    G=np.zeros((162,162),complex)
    for c in range(2):
        for a in range(27):G[3*(27*c+a):3*(27*c+a+1),3*(27*c+a):3*(27*c+a+1)]=gauge[c,a]
    for x,y in zip(S,T):assert np.max(abs(y-G.conj().T@x@G))<1e-11 and np.linalg.norm(x@x.conj().T-np.eye(162))<1e-10
    assert np.max(abs(Lg-G.conj().T@L@G))<1e-11
    assert max(abs(np.linalg.det(x)-1) for x in edges.reshape(-1,3,3))<1e-11

def test_SU3_flux_bundle_determinant_and_index_orientation():
    pp,U,Q=native.flux_links();assert Q==1
    assert np.max(abs(np.linalg.det(U)-1))<1e-12
    a=native.flux_index();b=native.flux_index(True)
    assert a['total_overlap_index']==-1 and b['total_overlap_index']==1
    assert a['minimum_color_kernel_gap']>.3

def test_actual_overlap_GW_projector_and_optical_index_zero():
    pp,U,Q=native.flux_links();D,G5=native.wilson(native.coarse_shifts(U,pp,color=0));e,V=eigh(G5@D);sign=(V*np.sign(e))@V.conj().T;O=np.eye(len(D))+G5@sign
    assert np.linalg.norm(G5@O+O@G5-O@G5@O)<1e-10
    P=(np.eye(len(D))+sign)/2;assert np.linalg.norm(P@P-P)<1e-10
    heavy=np.linalg.eigvalsh(G5@(D+4*np.eye(len(D))));assert abs(sum(np.sign(heavy)))==0 and min(abs(heavy))>=3-1e-12

def test_SM_inventory_anomaly_cancellation_and_missing_lepton_control():
    charges=[(6,1),(3,-4),(3,2),(2,-3),(1,6),(1,0)]
    assert sum(d*q for d,q in charges)==sum(d*q**3 for d,q in charges)==0
    assert 2-1-1==2*1-4+2==3*1-3==0
    assert 3*sum(d for d,q in charges)==48 and (3*(3+1))%2==0
    assert sum(d*q for d,q in charges if (d,q)!=(2,-3))!=0


def test_densitized_GL4_action_and_natural_scale_gate():
    H=np.array([[2,.2,.1,0],[.2,3,.3,.1],[.1,.3,2,.2],[0,.1,.2,4]])
    T=np.array([[2,1,0,0],[0,1,1,0],[0,0,1,1],[0,0,0,1.]])
    Ti=np.linalg.inv(T);jac=abs(np.linalg.det(T));M,G=density.geometric(H)
    Mp,Gp=density.geometric(jac*Ti@H@Ti.T)
    assert abs(Mp-jac*M)<1e-11 and np.max(abs(Gp-Ti@G@Ti.T))<1e-12
    for scale in [.3,2.,5.]:
        Ms,Gs=density.geometric(scale*H)
        assert abs(Ms-scale**2*M)<1e-10 and np.max(abs(Gs-G/scale))<1e-12
