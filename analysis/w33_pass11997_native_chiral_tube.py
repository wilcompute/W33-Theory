"""A globally periodic gauge-orbit tube frame with an exact finite gap bound.

This is a gauge-covariant finite-cell section, built using a spanning tree.
It is NOT a spatially local Luscher measure or all-sector chiral continuum.
11429 owns Stiefel-chart method;11443/11462 own earlier global-measure caveats.
"""
import json,itertools
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import eigh
from w33_pass11991_native_four_period_cover import native_geometry,bloch_incidence,gamma4
ROOT=Path(__file__).resolve().parents[1]
CHARGES=[1,-4,2,-3,6,0];MULTIPLICITIES=[6,3,3,2,1,1]


def geometry():
    _,edges,B,*_=native_geometry();d=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text())
    C=s.Matrix(d['harmonic_voltages_Q']);current=27*C*(C.T*C).inv();V=np.array(d['primitive_integer_edge_voltages'],float)
    return edges,B,current,V


def kernel(edges,V,current,phases):
    B,C=bloch_incidence(edges,V,np.zeros(4),phases);g,g5=gamma4();G5=np.kron(g5,np.eye(27))
    derivatives=[C.conj().T@(current[:,i,None]*B) for i in range(4)]
    return G5@(sum(np.kron(a,b) for a,b in zip(g,derivatives))+np.kron(np.eye(4),B.conj().T@B-.5*np.eye(27)))


def rational_gap_certificate(B,current):
    A=s.zeros(135,27)
    # B is the signed vertex-by-edge incidence.
    for e in range(135):
        for v in range(27):A[e,v]=abs(B[v,e])/2
    X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
    gamma=[s.kronecker_product(X,X),s.kronecker_product(X,Y),s.kronecker_product(X,Z),s.kronecker_product(Z,s.eye(2))];g5=gamma[0]*gamma[1]*gamma[2]*gamma[3]
    derivative=[A.T*s.diag(*current[:,i])*B.T for i in range(4)]
    Q=s.kronecker_product(g5,s.eye(27))*(sum((s.kronecker_product(g,x) for g,x in zip(gamma,derivative)),s.zeros(108))+s.kronecker_product(s.eye(4),B*B.T-s.eye(27)/2))
    Q=Q.applyfunc(s.expand)
    assert Q==Q.conjugate().T
    den=int(s.ilcm(*[s.denom(z) for x in Q for z in (s.re(x),s.im(x))]));qr=np.array(s.re(Q)*den,dtype=np.int64);qi=np.array(s.im(Q)*den,dtype=np.int64)
    approximate=np.linalg.inv(np.array(Q,complex));scale=10**8
    ar=np.rint(approximate.real*scale).astype(np.int64);ai=np.rint(approximate.imag*scale).astype(np.int64)
    # Every following integer operation is exact: prove no int64 overflow.
    bound=4*108*max(1,int(abs(qr).max()),int(abs(qi).max()))*max(1,int(abs(ar).max()),int(abs(ai).max()))
    assert bound<2**63
    rr=den*scale*np.eye(108,dtype=np.int64)-qr@ar+qi@ai;ri=-qr@ai-qi@ar
    residual=int(max(np.sum(abs(rr)+abs(ri),axis=1)));anorm=int(max(np.sum(abs(ar)+abs(ai),axis=1)))
    assert residual<den*scale
    inverse_bound=s.Rational(anorm*den,den*scale-residual)
    # Since Q^-1 is Hermitian its spectral norm <= its infinity norm.
    return dict(Q_denominator=den,inverse_grid_denominator=scale,approximate_inverse_real_numerator=ar.tolist(),approximate_inverse_imag_numerator=ai.tolist(),
        residual_inf_upper=str(s.Rational(residual,den*scale)),inverse_inf_upper=str(inverse_bound),spectral_gap_lower=str(1/inverse_bound),int64_product_upper=bound),float(1/inverse_bound)


def frame(P,E):
    gram=E.conj().T@P@E;ev,U=eigh(gram);assert ev[0]>.5
    F=P@E@(U/np.sqrt(ev))@U.conj().T
    assert np.max(abs(F.conj().T@F-np.eye(F.shape[1])))<1e-10
    return F,float(ev[0])


def tree_gauge(edges,phases):
    # Unique rooted tree gauge; phases are used numerically here. The
    # periodic definition is products of U1 links along root paths.
    theta=np.zeros(27);seen={0};queue=[0];tree=[]
    for a in queue:
        for e,(u,v) in enumerate(edges):
            if u==a and v not in seen:theta[v]=theta[a]-phases[e];seen.add(v);queue.append(v);tree.append(e)
            if v==a and u not in seen:theta[u]=theta[a]+phases[e];seen.add(u);queue.append(u);tree.append(e)
    fixed=phases+np.array([theta[b]-theta[a] for a,b in edges])
    return fixed,theta,tree


def payload():
    edges,B,J,V=geometry();certificate,gap=rational_gap_certificate(B,J);jf=np.array(J,float)
    q0=kernel(edges,V,jf,np.zeros(135));ev,E=eigh(q0);E0=E[:,ev>0];assert E0.shape==(108,54)
    assert sum(q*m for q,m in zip(CHARGES,MULTIPLICITIES))==sum(q**3*m for q,m in zip(CHARGES,MULTIPLICITIES))==0
    costs=np.array([float(1+sum(abs(J[e,i]) for i in range(4))/2) for e in range(135)])
    _,_,tree=tree_gauge(edges,np.zeros(135));chords=[i for i in range(135) if i not in tree]
    rng=np.random.default_rng(11997);physical=np.zeros(135);physical[chords]=rng.normal(size=len(chords));physical*=gap/(128*6*np.dot(costs,abs(physical)))
    theta=rng.uniform(-40*np.pi,40*np.pi,27);theta[0]=0
    actual=physical+np.array([theta[b]-theta[a] for a,b in edges]);fixed,t,_=tree_gauge(edges,actual)
    assert max(abs(fixed-physical))<1e-12
    rows=[];frames=[]
    for charge,mult in zip(CHARGES,MULTIPLICITIES):
        Q=kernel(edges,V,jf,charge*physical);ev,U=eigh(Q);E=U[:,ev>0];P=E@E.conj().T;F,mineig=frame(P,E0)
        T=np.kron(np.eye(4),np.diag(np.exp(1j*charge*t)));Factual=T@F
        ev0,U0=eigh(kernel(edges,V,jf,charge*actual));Pactual=U0[:,ev0>0]@U0[:,ev0>0].conj().T
        covariance=float(np.max(abs(Pactual-Factual@Factual.conj().T)));assert covariance<1e-10
        # Large2pi site windings must preserve the global frame, not just P.
        wind=np.zeros(27);wind[3]=2*np.pi; _,tw,_=tree_gauge(edges,actual+np.array([wind[b]-wind[a] for a,b in edges]))
        Fwind=np.kron(np.eye(4),np.diag(np.exp(1j*charge*tw)))@F
        periodicity=float(np.max(abs(Fwind-Factual)));assert periodicity<1e-10
        budget=float(np.dot(costs,abs(charge*physical)));assert budget<gap/16
        rows.append(dict(charge=charge,multiplicity=mult,Wilson_gap=float(min(abs(ev))),gap_perturbation_budget=budget,
            overlap_chart_Gram_min=mineig,gauge_covariant_frame_error=covariance,large_gauge_periodicity_error=periodicity))
        frames.append((P,F))
    # Three independent reference frames over one common physical patch.
    Ps,Fs=frames[0];refs=[E0,frame(Ps,E0)[0]]
    ph2=physical*.7;ev2,u2=eigh(kernel(edges,V,jf,ph2));refs.append(u2[:,ev2>0])
    ff=[frame(Ps,R)[0] for R in refs];T01=ff[0].conj().T@ff[1];T12=ff[1].conj().T@ff[2];T20=ff[2].conj().T@ff[0]
    cocycle=float(np.max(abs(T01@T12@T20-np.eye(54))));assert cocycle<1e-10
    return dict(status='PASS',native_finite_cell_vertices=27,spinor_dimension=108,modified_Weyl_rank=54,rational_gap_certificate=certificate,
        perturbation_theorem='For phase-fixed link fields with sum_e c_e |q a_e| < g0/16, c_e=1+sum_i |J_ei|/2, ||Q(a)-Q0||2<=that sum. Exact inverse residual gives g0>0; gap>=15g0/16. Davis-Kahan gives ||P-P0||<2/15, so E0^dag P E0> (1-(2/15)^2) I. The Stiefel frame therefore exists throughout this finite weak-field tube.',
        charges=rows,rooted_tree_edge_indices=tree,physical_weak_field_phases=physical.tolist(),
        global_frame='F(U)=T_tree(U) P(U_fixed) E0 [E0^dag P(U_fixed) E0]^-1/2. Rooted tree products are periodic under2pi windings and transform covariantly under the complete rootedU1 gauge group. Arbitrarily large gauge phases are allowed, while gauge-fixed physical cycles remain small.',
        exact_charge_anomaly_moments={'linear':0,'cubic':0},three_patch_transition_cocycle_error=cocycle,
        locality_obstruction='The rooted tree frame depends on products along possibly distant tree paths. This explicitly constructs a NONLOCAL finite-cell gauge fixing. A global section on this tube is not a spatially local gauge-invariant fermion measure, and anomaly cancellation does not demand zero Berry curvature.',
        global_scope='All rooted gauge orbits over the specified contractible weak-cycle domain in the27vertex finite quotient. Not all physical gauge configurations, nonzero topological sectors, all Blochmomenta, full nonAbelian fields, an interacting chiral continuum or derivedthreefamilies.',
        prior=['11991 actualnative4cover/GWkernel','11429 Stiefelcharts and nonflat anomalyfree measure curvature','11443 gaugeorbitcocycle is insufficient for local global measure','11462 admissibleflux determinant-line patch','11984 suppliedchiralSU5 template'],
        primary=['https://arxiv.org/abs/hep-lat/9811032','https://arxiv.org/abs/hep-lat/9909150'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11997_native_chiral_tube.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['rational_gap_certificate']['spectral_gap_lower'])
