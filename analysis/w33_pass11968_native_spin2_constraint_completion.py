"""Native harmonic-current derivative spin-two constraint attempt.

Exact rational bracket witness, and a constructed nonlocal first-class linear
completion. No nonlinear Einstein action or helicity identification inferred.
"""
from pathlib import Path
import json
import sys
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep

PAIRS=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]


def constraints(D):
    n=D[0].shape[0];zero=np.zeros((n,n))
    lap=sum(x@x for x in D)
    H=np.hstack([lap-D[i]@D[i] if i==j else -(D[i]@D[j]+D[j]@D[i]) for i,j in PAIRS])
    blocks=[]
    for k in range(3):
        blocks.append(np.hstack([D[k] if i==j==k else D[j]/2 if i!=j and i==k else D[i]/2 if i!=j and j==k else zero for i,j in PAIRS]))
    return H,np.vstack(blocks)


def row_projector(M):
    _,s,V=np.linalg.svd(M,full_matrices=False)
    keep=s>max(s[0],1)*1e-10
    basis=V[keep]
    return basis.T@basis,int(sum(keep))


def payload():
    edges,volts,*_=prep();n=80
    B=np.zeros((160,n),dtype=int);C=np.zeros_like(B)
    for e,(a,b) in enumerate(edges):B[e,a]=-1;B[e,b]=1;C[e,a]=C[e,b]=1
    br=sp.Matrix(B[:,1:]); V=sp.Matrix(volts)
    currents=V-br*(br.T*br).inv(method='DM')*br.T*V
    assert sp.Matrix(B).T*currents==sp.zeros(n,3)
    Ds=[sp.SparseMatrix(sp.Matrix(C).T*sp.diag(*list(currents[:,i]))*sp.Matrix(B)/2) for i in range(3)]
    assert all(d+d.T==sp.zeros(n) for d in Ds)
    D=[np.asarray(d,float) for d in Ds]
    H,M=constraints(D);bracket=H@M.T
    index=np.unravel_index(np.argmax(abs(bracket)),bracket.shape)
    row,column=map(int,index);i,site=divmod(column,n)
    lap=sum((d*d for d in Ds),sp.zeros(n))
    hs=[lap-Ds[a]*Ds[a] if a==b else -(Ds[a]*Ds[b]+Ds[b]*Ds[a]) for a,b in PAIRS]
    ms=[Ds[i] if a==b==i else Ds[b]/2 if a!=b and a==i else Ds[a]/2 if a!=b and b==i else sp.zeros(n) for a,b in PAIRS]
    exact=sum(hs[a][row,k]*ms[a][site,k] for a in range(6) for k in range(n))
    assert exact!=0 and abs(float(exact)-bracket[index])<1e-14
    # Canonical q=(h11,h22,h33,h12,h13,h23), p=(pi11,pi22,pi33,2pi12,2pi13,2pi23).
    # Replace H by its row projection orthogonal to momentum rows.
    PM,rankM=row_projector(M);HC=H@(np.eye(6*n)-PM)
    PH,rankH=row_projector(HC)
    Q=np.eye(6*n)-PM-PH
    closure=float(np.max(abs(HC@M.T)))
    idem=float(np.max(abs(Q@Q-Q)))
    assert closure<1e-12 and idem<1e-10
    qrank=6*n-rankM-rankH
    assert int(round(np.trace(Q)))==qrank
    # A compatible positive quadratic Hamiltonian can now be named explicitly.
    K=np.kron(np.eye(6),B.T@B)
    Kphysical=Q@K@Q
    eq_constraints=float(max(np.max(abs(HC@Q)),np.max(abs(M@Kphysical))))
    assert eq_constraints<1e-10
    rng=np.random.default_rng(11968);q=rng.normal(size=6*n);p=rng.normal(size=6*n)
    def energy(q,p):return float((p@Q@p+q@Kphysical@q)/2)
    a=rng.normal(size=3*n);b=rng.normal(size=n)
    gauge_change=abs(energy(q+M.T@a,p-HC.T@b)-energy(q,p))
    assert gauge_change<1e-9
    offsite=np.kron(np.ones((6,6)),(np.eye(n)+(abs(B).T@abs(B))==0).astype(int))
    nonlocal_fraction=float(np.linalg.norm(Q*offsite)/np.linalg.norm(Q))
    assert nonlocal_fraction>0
    return dict(status='PASS',native_dimensions={'vertices':n,'links':160,'symmetric_tensor_configuration':480},
                derivative='D_i=C.T diag(j_i) B/2, C unsigned endpoint incidence, j_i weighted-uniform harmonic projection of the three native unit voltages; B.T j_i=0 makes D_i antisymmetric.',
                derivative_commutator_norms=[float(np.linalg.norm(D[a]@D[b]-D[b]@D[a])) for a,b in ((0,1),(0,2),(1,2))],
                naive_linear_constraints='H=sum_i D_i² Tr(h)-sum_ij sym(D_i D_j)h_ij; M_i=sum_j D_j pi_ij',
                exact_poisson_witness={'H_vertex':row,'M_component':i,'M_vertex':site,'bracket':str(exact)},
                naive_max_bracket=float(np.max(abs(bracket))),
                completion='P_M=orthogonal projector onto row(M); Hc=H(I-P_M); P_H=row projector of Hc; Q=I-P_M-P_H. Constraints Hc q=0,M p=0 commute exactly because Hc M.T=0. Hamiltonian=(p.T Q p+q.T Q (I6 tensor B.T B) Q q)/2 is gauge invariant.',
                momentum_rank=rankM,completed_H_rank=rankH,physical_configuration=qrank,
                completed_constraint_bracket_max=closure,physical_projector_idempotence=idem,
                Hamiltonian_constraint_flow_residual=eq_constraints,finite_gauge_energy_change=gauge_change,
                offsite_projector_norm_fraction=nonlocal_fraction,
                scope='A new specified native derivative attempt and explicitly projected finite linear canonical completion. The projection is nonlocal and an added choice. Physical configuration count is not a helicity-two proof. No nonlinear hypersurface-deformation algebra, dynamically curved spacetime, coupling to stress energy or continuum gravitational limit.',
                prior=['11955 continuum Fierz-Pauli positive control','11301 native scalar lapse obstruction','11306 parametrized multi-clock closure; different completion'],
                primary='https://arxiv.org/abs/1304.5983')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11968_native_spin2_constraint_completion.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',d['exact_poisson_witness'],d['momentum_rank'],d['completed_H_rank'],d['physical_configuration'],flush=True)
