"""Field-dependent metric test of the native scalar hypersurface bracket.

11301 owns the finite pointwise Leibniz obstruction.11968 owns its tensor
attempt. Here g=a²I is an actual canonical metric slice, Pi_g=0, and the
tested scalar kinetic and momentum maps are specified, not placeholders.
"""
from pathlib import Path
import json
import sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11970_native_wilson_dirac import construction


def data():
    ed,volts,*_=construction()
    old=json.loads((ROOT/'data/w33_pass11956_local_electric_metric.json').read_text())
    h=sp.Matrix(old['harmonic_period_basis']);J=80*h*(h.T*h).inv()
    B=sp.zeros(160,80);C=sp.zeros(160,80)
    for e,(a,b) in enumerate(ed):B[e,a]=-1;B[e,b]=1;C[e,a]=C[e,b]=1
    D=[C.T*sp.diag(*list(J[:,i]))*B/2 for i in range(3)]
    assert all(d+d.T==sp.zeros(80) for d in D)
    return ed,D


def matrices(D,a,N,M):
    w=a**3;g=1/a**2
    KN=sum(d.T@np.diag(N*a)@d for d in D)
    KM=sum(d.T@np.diag(M*a)@d for d in D)
    actual=np.diag(M/w)@KN-np.diag(N/w)@KM
    target=sum(np.diag(g*(N*(d@M)-M*(d@N)))@d for d in D)
    return actual,target


def payload():
    ed,Ds=data();D=[np.asarray(d,float) for d in Ds]
    N=np.zeros(80);M=np.zeros(80);N[ed[0][0]]=1;M[ed[0][1]]=1
    aa=[sp.Rational(2+(v%3),2) for v in range(80)];a=np.array(aa,float)
    actual,target=matrices(D,a,N,M);defect=actual-target
    r,s=map(int,np.unravel_index(np.argmax(abs(defect)),defect.shape))
    exact=0
    for d in Ds:
        exact+=sum((sp.Rational(int(M[r]),1)/aa[r]**3*d[k,r]*int(N[k])*aa[k]*d[k,s]
                   -sp.Rational(int(N[r]),1)/aa[r]**3*d[k,r]*int(M[k])*aa[k]*d[k,s]) for k in range(80))
        exact-=((int(N[r])*sum(d[r,k]*int(M[k]) for k in range(80))-
                 int(M[r])*sum(d[r,k]*int(N[k]) for k in range(80)))/aa[r]**2)*d[r,s]
    assert exact!=0 and abs(float(exact)-defect[r,s])<1e-10
    # Independently differentiate the actual quadratic Hamiltonian in
    # canonical scalar variables, not just the preassembled bracket map.
    rng=np.random.default_rng(11976);q,p=rng.normal(size=(2,80))
    KN=sum(d.T@np.diag(N*a)@d for d in D);KM=sum(d.T@np.diag(M*a)@d for d in D)
    differentiated=float((KN@q)@(M*p/a**3)-(N*p/a**3)@(KM@q))
    assert abs(differentiated-p@actual@q)<1e-9
    U=np.eye(3)[[1,2,0]];Dr=[sum(U[i,j]*D[j] for j in range(3)) for i in range(3)]
    ac,ta=matrices(Dr,a,N,M)
    assert np.max(abs(ac-actual))<1e-10 and np.max(abs(ta-target))<1e-10
    flat=matrices(D,np.ones(80),N,M)
    return dict(status='PASS',native_sites=80,
        canonical_fields='At each vertex: scalar(q,p), positive metric g_ab with six canonical momenta Pi_ab. Evaluate the conformal slice g_ab=a_v² delta_ab and Pi_ab=0; a_v cycles through1,3/2,2.',
        scalar_H='H_phi[N]=1/2 p.T diag(N/a³)p +1/2 sum_i(D_i q).T diag(N a)(D_i q). D_i is the exact11970 normalized native harmonic-current derivative at k0.',
        scalar_M='M_phi_i[v]=p_v (D_i q)_v. Expected hypersurface shift beta_i[v]=a_v^-2[N_v(D_i M)_v-M_v(D_i N)_v].',
        exact_bracket_matrix='A=diag(M/a³) sum_i D_i.T diag(N a)D_i -diag(N/a³)sum_i D_i.T diag(M a)D_i; {H[N],H[M]}=p.T A q.',
        exact_defect_witness=dict(lapse_N_vertex=int(np.argmax(N)),lapse_M_vertex=int(np.argmax(M)),p_vertex=r,q_vertex=s,coefficient=str(exact)),
        max_curved_defect=float(np.max(abs(defect))),max_flat_defect=float(np.max(abs(flat[0]-flat[1]))),
        independent_canonical_bracket=differentiated,
        metric_potential_repair_gate='For standard purely gravitational H_g=kinetic even in Pi plus ANY metric-only potential, dH_g/dPi=0 at Pi=0. The matter H has no Pi. Pure-gravity and mixed metric brackets therefore cannot change this p*q coefficient on that slice. Gravitational M is linear in Pi and vanishes there. Changing only a curvature/potential term cannot repair the tested hypersurface-deformation identity.',
        scope='Scoped failure of these particular native pointwise scalar H/M derivative maps with standard even-momentum gravity additions. Not an all-discrete-gravity no-go, no assertion about other products/coarse constraints/perfect actions or a continuum limit. No nonlinearGR solution.',
        prior=['11301 exact edge bracket and finite derivation theorem','11968 native tensor derivative failure','11970 current normalization'],
        primary='https://arxiv.org/abs/0909.5688')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11976_metric_lapse_bracket.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',d['exact_defect_witness'],d['max_curved_defect'])
