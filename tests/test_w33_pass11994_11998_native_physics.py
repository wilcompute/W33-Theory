"""Independent controls on native order, metric, vacuum, measure and U3 repair."""
import json,sys,itertools
from pathlib import Path
import numpy as np
import sympy as s
import mpmath as mp
from scipy.linalg import eigvalsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11994_native_clock_order as clock
import w33_pass11995_native_metric_gr_lift as metric
import w33_pass11996_joint_singlet_flavour as flavour
import w33_pass11997_native_chiral_tube as chiral
from w33_pass11991_native_four_period_cover import bloch_incidence
from w33_pass11981_cubic_mediator_cp import determinant_energy_gradient
from w33_pass11989_joint_source_barr import args_of,heavy_sources
from functools import lru_cache


def read(stem):return json.loads((ROOT/'data'/('w33_pass'+stem+'.json')).read_text())


@lru_cache(None)
def metric_inputs():return metric.inputs()


def test_clock_native_moment_polynomial_and_global_zeros():
    prior=read('11991_native_four_period_cover');C=s.Matrix(prior['harmonic_voltages_Q']);L=s.Matrix(prior['raw_period_lattice_basis'])
    x,y=s.symbols('x y');v=C*L.T*s.Matrix([x,y,0,0]);I2=sum(q*q for q in v);I6=sum(q**6 for q in v)
    assert s.factor(I6-I2**3/2916)==81*x*x*y*y*(x+y)**2
    actual=clock.payload();assert actual['global_vacuum_count']==6
    # Removing the supplied angular term restores a continuum of minima.
    assert s.simplify((x*x+x*y+y*y-1).subs({x:s.sqrt(3)/3,y:s.sqrt(3)/3}))==0
    assert (x*x*y*y*(x+y)**2).subs({x:s.sqrt(3)/3,y:s.sqrt(3)/3})!=0


def test_clock_reflection_signature_and_basis_change():
    d=read('11994_native_clock_order');G=np.array(s.Matrix(read('11991_native_four_period_cover')['exact_acoustic_metric']),float)
    for row in d['vacua']:
        eta=np.array(s.Matrix(row['metric_Q']),float);u=np.array(list(map(float,row['clock_primitive'])))
        assert np.linalg.eigvalsh(eta)[0]<0<np.linalg.eigvalsh(eta)[1]
        assert abs(u@eta@u+1)<1e-12
        assert np.max(abs(eta-(G-np.outer(G@u,G@u))/2))<1e-12
    assert len({tuple(r['clock_primitive']) for r in d['vacua']})==6


def test_metric_minor_is_exact_and_envelope_includes_corrector():
    b,v,C,G=metric_inputs();d=read('11995_native_metric_gr_lift');sel=d['selected_edge_indices']
    A=s.Matrix([[C[e,i]*C[e,j]/27 for e in sel] for i,j in metric.PAIRS]);assert str(A.det())==d['selected_jacobian_determinant']
    w=np.linspace(.96,1.04,135);g,h=metric.homogenize(w,b,v)
    assert np.max(abs(b.T@(w[:,None]*h)))<1e-12
    stale=np.array(C,float).T@(w[:,None]*np.array(C,float))/27
    assert np.linalg.norm(g-stale)>1e-6
    e=sel[4];step=1e-5;dw=np.eye(135)[e]*step
    deriv=(metric.homogenize(w+dw,b,v)[0]-metric.homogenize(w-dw,b,v)[0])/(2*step)
    assert np.max(abs(deriv-np.outer(h[e],h[e])/27))<1e-9


def test_nonlinear_metric_lift_against_independent_weighted_bloch_band():
    b,v,C,G=metric_inputs();d=read('11995_native_metric_gr_lift');target=np.array(G,float).copy();target[0,2]+=2e-5;target[2,0]+=2e-5
    w,_=metric.lift(target,b,v,d['selected_edge_indices']);assert min(w)>.1
    edges=chiral.geometry()[0];p=np.array([.2,-.3,.4,.5]);p/=np.linalg.norm(p)
    errors=[]
    for spacing in [.02,.01]:
        B,_=bloch_incidence(edges,v,spacing*p);lam=eigvalsh(B.conj().T@(w[:,None]*B),subset_by_index=[0,0])[0]
        errors.append(abs(lam/spacing**2-p@target@p))
    assert errors[1]<errors[0]/3


def test_full_clock_reflection_is_involutive_with_nonzero_shift():
    E=np.array([[2,.1,.2,-.1],[.1,1.3,.03,.06],[.2,.03,1.1,.04],[-.1,.06,.04,1.4]])
    e=np.array([1.,0,0,0]);reflect=lambda a:a-2*np.outer(a@e,a@e)/(e@a@e)
    g=reflect(E);assert sum(np.linalg.eigvalsh(g)<0)==1
    assert np.max(abs(reflect(g)-E))<1e-12
    assert abs(g[0,1])>.01  # Full metric chart, not a diagonal-only construction.


def test_joint_vacuum_decimal_root_and_independent_flavour_gradient():
    d=read('11996_joint_singlet_flavour');x=np.array(d['triplet_coordinates']);tau=float(d['source_value'])
    old=read('11981_cubic_mediator_cp');r=next(r for r in old['third_triplet_determinant_probe']['draws'] if r['trial']==3)
    _,gradient=determinant_energy_gradient(x,*args_of(r),tau=tau)
    assert max(abs(gradient))<1e-10
    with mp.workdps(95):
        u=list(map(mp.mpf,d['singlet_chart_coordinates']));value=-u[0]*u[1]/(mp.mpf(1)/32)
        assert abs(value-mp.mpf(d['source_value']))<mp.mpf('1e-48')
    assert d['total_scalar_real_fields_with_mediators']==72 and d['total_positive_physical_light_modes']==44


def test_joint_vacuum_full_scaled_hessian_inertia_and_gauge_kernel():
    d=read('11996_joint_singlet_flavour')
    with mp.workdps(90):
        H=mp.matrix([[mp.mpf(z) for z in row] for row in d['scaled_core_flavour_Hessian_decimal']]);assert H==H.T
        ev,_=mp.eigsy(H);assert sum(z>mp.mpf('1e-65') for z in ev)==30
        assert sum(abs(z)<mp.mpf('1e-65') for z in ev)==2 and min(ev)>-mp.mpf('1e-65')
        r=list(map(mp.mpf,d['singlet_chart_coordinates']));z=flavour.home(r)
        for charge in [[-1,-1,1,1,0,0,0],[0,0,1,1,1,-12,12]]:
            tangent=[mp.j*q*v for q,v in zip(charge,z)]
            vec=mp.matrix(list(map(mp.re,tangent))+list(map(mp.im,tangent))+[mp.mpf(0)]*18)
            assert max(abs(v) for v in H*vec)<mp.mpf('1e-65')


def test_restored_flavour_mediators_have_exact_positive_square_energy():
    d=read('11996_joint_singlet_flavour');r=next(r for r in read('11981_cubic_mediator_cp')['third_triplet_determinant_probe']['draws'] if r['trial']==3)
    args=args_of(r);source=heavy_sources(np.r_[d['triplet_coordinates'],float(d['source_value'])],args)
    mass2=np.r_[args[0]**2,np.ones(9)];home=-source/mass2;rng=np.random.default_rng(11996);delta=(rng.normal(size=13)+1j*rng.normal(size=13))*.001
    energy=lambda chi:np.sum(mass2*abs(chi)**2+2*np.real(chi.conj()*source))
    assert abs(energy(home+delta)-energy(home)-np.sum(mass2*abs(delta)**2))<1e-12


def test_actual_flavour_portal_CP_scale_and_decoupling_controls():
    d=read('11996_joint_singlet_flavour');r=next(r for r in read('11981_cubic_mediator_cp')['third_triplet_determinant_probe']['draws'] if r['trial']==3)
    loop=flavour.scalar_portal_threshold(d['triplet_coordinates'],float(d['source_value']),r,d['Barr_matching'])
    assert abs(loop['scan'][0]['theta_one_loop'])<1e-12
    theta=loop['scan'][1]['theta_one_loop'];assert abs(theta)>1e-5
    assert abs(theta+loop['CP_partner']['theta_one_loop'])<1e-11
    assert abs(theta-loop['scale3']['theta_one_loop'])<1e-11
    assert loop['illustrative_kappa_for_abs_theta_below_1e_minus10']<1e-6


def test_chiral_frozen_inverse_residual_is_exact_integer_certificate():
    d=read('11997_native_chiral_tube');c=d['rational_gap_certificate'];edges,B,J,V=chiral.geometry()
    Q=chiral.kernel(edges,V,np.array(J,float),np.zeros(135));den=c['Q_denominator'];scale=c['inverse_grid_denominator']
    qr=np.rint(Q.real*den).astype(np.int64);qi=np.rint(Q.imag*den).astype(np.int64)
    assert np.max(abs(Q-(qr+1j*qi)/den))<1e-13
    ar=np.array(c['approximate_inverse_real_numerator'],dtype=np.int64);ai=np.array(c['approximate_inverse_imag_numerator'],dtype=np.int64)
    rr=den*scale*np.eye(108,dtype=np.int64)-qr@ar+qi@ai;ri=-qr@ai-qi@ar
    rho=s.Rational(int(max(np.sum(abs(rr)+abs(ri),axis=1))),den*scale)
    assert rho==s.Rational(c['residual_inf_upper'])<s.Rational(1,10000)
    assert s.Rational(c['spectral_gap_lower'])>s.Rational(2,5)


def test_chiral_negative_control_needs_gauge_tree_compensation():
    d=read('11997_native_chiral_tube');edges,B,J,V=chiral.geometry();jf=np.array(J,float);physical=np.array(d['physical_weak_field_phases'])
    Q=chiral.kernel(edges,V,jf,physical);ev,U=np.linalg.eigh(Q);P=U[:,ev>0]@U[:,ev>0].conj().T
    theta=np.linspace(0,2,27);shift=np.array([theta[b]-theta[a] for a,b in edges]);Qg=chiral.kernel(edges,V,jf,physical+shift)
    eg,Ug=np.linalg.eigh(Qg);Pg=Ug[:,eg>0]@Ug[:,eg>0].conj().T
    T=np.kron(np.eye(4),np.diag(np.exp(1j*theta)))
    assert np.max(abs(Pg-T.conj().T@P@T))<1e-12
    assert np.linalg.norm(Pg-P)>.1
    fixed,t,_=chiral.tree_gauge(edges,physical+shift);assert max(abs(fixed-physical))<1e-12


def test_complex_reduced_frozen_gates_conserve_singlet_and_change_native_control():
    d=read('11998_complex_reduction_tradeoff');assert d['exact_J_centralizer_dimension']==9 and d['exact_J_anticommuting_dimension']==6
    prior=read('11987_atlas_spin_gate_alphabet')['gates'];assert len(d['actual_native_gate_reductions'])==5
    for row,old in zip(d['actual_native_gate_reductions'],prior):
        U=np.array(row['reduced_gate_real'])+1j*np.array(row['reduced_gate_imag']);assert np.max(abs(U.conj().T@U-np.eye(4)))<1e-10
        assert row['reduced_singlet_to_triplet_probability']<1e-20
    assert max(r['native_singlet_to_triplet_probability'] for r in d['actual_native_gate_reductions'])>.01


def test_decimal_joint_root_and_hessian_bind_to_the_actual_potential():
    d=read('11996_joint_singlet_flavour')
    old,med,prior,rho,Lambda,vf,eps,soft,f0,Vf,tau,V,equations,start=flavour.setup()
    z=flavour.home(list(map(mp.mpf,d['singlet_chart_coordinates'])))
    point=list(map(mp.re,z))+list(map(mp.im,z))+list(map(mp.mpf,d['triplet_coordinates_decimal']))
    def total(*a):
        fields=[a[i]+mp.j*a[i+7] for i in range(7)]
        return flavour.potential_core(fields,soft,mp.mpf('.1'),f0)+eps*Vf(a[14:],tau(fields))
    scale=[mp.mpf(1)]*14+[mp.sqrt(eps)]*18
    for j in range(32):
        g=mp.diff(total,point,tuple(int(i==j) for i in range(32)))
        assert abs(g)/(eps if j>=14 else 1)<mp.mpf('1e-65')
    for i,j in [(0,0),(3,18),(20,23),(0,15),(8,8),(6,6)]:
        h=mp.diff(total,point,tuple(int(k==i)+int(k==j) for k in range(32)))/(scale[i]*scale[j])
        assert abs(h-mp.mpf(d['scaled_core_flavour_Hessian_decimal'][i][j]))<mp.mpf('1e-65')


def test_actual_complex_charge_commutes_with_reduced_but_not_native_gates():
    from scipy.linalg import eigh
    from w33_pass11987_atlas_spin_gate_alphabet import gamma6
    source=read('11983_atlas_projector_descent')['compact_holonomy_closure'];G=np.array(source['source_fiber_Gram'],float)
    Jn=np.array(s.Matrix(read('11988_spinor_weil_intertwiner')['exact_projective_tangent_repair']['complex_structure_numerator_Q']),float)
    ev,U=eigh(G);R=(U*np.sqrt(ev))@U.T;Ri=(U/np.sqrt(ev))@U.T;J=R@Jn@Ri/np.sqrt(3)
    gamma,_,selected=gamma6();Q=-1j*sum(.5*J[i,j]*gamma[i]@gamma[j] for i,j in itertools.combinations(range(6),2));Q=Q[np.ix_(selected,selected)]
    raw=[]
    for reduced,native in zip(read('11998_complex_reduction_tradeoff')['actual_native_gate_reductions'],read('11987_atlas_spin_gate_alphabet')['gates']):
        V=np.array(reduced['reduced_gate_real'])+1j*np.array(reduced['reduced_gate_imag']);N=np.array(native['gate_real'])+1j*np.array(native['gate_imag'])
        assert np.linalg.norm(Q@V-V@Q)<1e-10
        raw.append(np.linalg.norm(Q@N-N@Q))
    assert max(raw)>1
