"""Actual11996 flavour threshold under radial decoupling, not coefficient tuning.

Linear unitary internal symmetries never forbid HdagH hdagh. A fixed-norm
nonlinear EFT removes its radial mixing; its UV completion remains additional.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
from w33_pass11989_joint_source_barr import args_of
from w33_pass11981_cubic_mediator_cp import determinant_energy_gradient
from w33_pass11952_11955_threshold_vacuum_loop_leptons import b0
ROOT=Path(__file__).resolve().parents[1]


def inputs():
    d=json.loads((ROOT/'data/w33_pass11996_joint_singlet_flavour.json').read_text());x=np.array(d['triplet_coordinates']);tau=float(d['source_value'])
    old=json.loads((ROOT/'data/w33_pass11981_cubic_mediator_cp.json').read_text());prior=next(r for r in old['third_triplet_determinant_probe']['draws'] if r['trial']==3);args=args_of(prior)
    H=np.column_stack([(determinant_energy_gradient(x+2e-5*v,*args,tau=tau)[1]-determinant_energy_gradient(x-2e-5*v,*args,tau=tau)[1])/4e-5 for v in np.eye(18)]);H=(H+H.T)/2
    fit=d['Barr_matching'];m=np.array(fit['real_m']);C=np.array(fit['real_C']);M=np.zeros((4,4),complex);M[:3,:3]=m;M[3,:3]=C@(x[:3]+1j*x[3:6]);M[3,3]=fit['mu']
    Y=np.zeros((19,4,4),complex);Y[0,:3,:3]=m
    for j in range(3):Y[j+1,3,:3]=C[:,j];Y[j+4,3,:3]=1j*C[:,j]
    radial=np.r_[x[:6],np.zeros(12)];radial/=np.linalg.norm(radial)
    return x,H,M,Y,radial


def threshold(K,M,Y,scale=1.):
    ev,O=np.linalg.eigh(K);assert min(ev)>0
    U,m,Vh=np.linalg.svd(M);V=Vh.conj().T;delta=np.zeros((4,4),complex)
    for j,mass2 in enumerate(ev):
        G=np.einsum('i,ijk->jk',O[:,j],Y)
        delta+=G@((V*(m*b0(m*m,mass2,scale)))@U.conj().T)@G/(16*np.pi**2)
    return float(np.trace(np.linalg.solve(M,delta)).imag),float(min(ev))


def payload():
    x,H,M,Y,r=inputs();kappa=.1;v=np.r_[2*kappa*x[:6],np.zeros(12)]
    baseline=np.block([[np.array([[25.]]),v[None,:]],[v[:,None],H+np.outer(v,v)/25]])
    rows=[]
    for mr in [0.,1.,10.,100.,1000.,10000.]:
        K=baseline.copy();K[1:,1:]+=mr*mr*np.outer(r,r)
        theta,minimum=threshold(K,M,Y)
        # CP acts on fields and the mass; vertices keep their real-field
        # derivative convention, including the imaginary field vertices.
        signs=np.r_[1,[(-1 if (i%6)>=3 else 1) for i in range(18)]]
        partner,_=threshold(signs[:,None]*K*signs[None,:],M.conj(),Y)
        assert abs(theta+partner)<2e-10
        rows.append(dict(radial_mass_over_supplied_flavour_scale=mr,theta=theta,CP_partner_theta=partner,minimum_scalar_mass_squared=minimum))
    assert abs(rows[-1]['theta'])<abs(rows[0]['theta'])/100000
    T=null_space(r[None,:]);projection=np.zeros((19,18));projection[0,0]=1;projection[1:,1:]=T
    constrained=projection.T@baseline@projection;vertices=np.einsum('ia,ijk->ajk',projection,Y)
    exact_limit,minimum=threshold(constrained,M,vertices);assert abs(exact_limit)<1e-12
    # General one-loop identity: Hermitian spectral F makes the pure
    # Higgs trace real. Pure flavour vertices only change the Barr B row.
    rng=np.random.default_rng(12001);z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));F=z+z.conj().T
    m=M[:3,:3].real;pureH=Y[0]@F@M.conj().T@Y[0]
    assert abs(np.trace(np.linalg.solve(M,pureH)).imag)<1e-12
    return dict(status='PASS',radial_scan=rows,strict_fixed_norm_theta=exact_limit,
        exact_decoupling_argument='On |h|²=n0, the supplied radial Higgsportal is constant in all angular fields. Scalar eigenstates no longer mix YH with lower-row flavour vertices. For arbitrary real loop spectral F=Fdag, Tr(M^-1 YH F Mdag YH)=Tr(F11 mT m) is real. Every pure-flavour correction changes only B and has zero determinant trace. Therefore this specified one-loop neutral-scalar theta vanishes exactly in the strict constraint EFT.',
        supplied_positive_radial_stiffness='DeltaV=MR² (|h|²-n0)²/(8n0); adds MR² rrT to Hessian, preserves theactualroot and improves stability.',
        internal_symmetry_gate='For every unitarylinear internalrepresentation h->Uh, hdagh is invariant; HdagH hdagh cannot be forbidden by such a symmetry. The repair changes the field manifold/UV dynamics, not an internalcharge assignment.',
        physical_limit='The largeMR/vf hierarchy is supplied. As an elementaryquartic this would become nonperturbative; a nonlinear sigma/composite UV completion and matching of allowed nonradial/higherdimensionportals are required. This is not technicallynatural fullstrongCP protection.',
        scope='Actual11996 neutral-scalar19D threshold channel and its fixed-norm limit, not all72scalar/gauge/gluino/tadpole/twoloop corrections, a fullE6 vacuum or measuredparameterprediction.',
        prior=['11996 actualboundedjointvacuum,realC andportal threshold','11954 B0 neutral-scalar matching','11298/11303/11313 earlier portal andUVbarriers'],
        primary=['https://arxiv.org/abs/2105.09122'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass12001_radial_portal_decoupling.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['radial_scan'][-1]['theta'])
