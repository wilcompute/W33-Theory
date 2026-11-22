#!/usr/bin/env python3
"""EXACT sparse 27x81 H27 partial intertwiner in Z[omega]/3.

Each of 27 output rows has nine nonzero coefficients omega^k/3, giving
243 nonzero entries in a 27x81 matrix. Six split-prime certificates
verify TT^dagger=I27 and the x/y^-1 intertwiner relations exactly.
The target is the canonical operator H27 module, not a complete E6
representation or cubic-invariant gauge map.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import toe_20261122_h27_central_fourier_bridge as H
import toe_20261122_witting_minimal_lie_control as W
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_next5_h27_exact_matrix.json'
PRIMES=(7,13,19,31,37,43)

def action_data():
    N,x,y,z,orbit=(getattr(H,'action',None) or H.heisenberg_action)()
    fibers=(getattr(H,'fibers',None) or H.center_fibers)(z,orbit)
    lookup={v:(j,k) for j,f in enumerate(fibers) for k,v in enumerate(f)}
    def monomial(g):return tuple(lookup[int(g(f[0]))] for f in fibers)
    return N,x,y,z,orbit,fibers,lookup,monomial(x),monomial(y**-1)

def apply(A,v):
    out={}
    for j,e in v.items():
        dest,t=A[j]
        assert dest not in out
        out[dest]=(e+t)%3
    return out

def exact_exponent_matrix():
    N,x,y,z,orbit,fibers,lookup,X,Y=action_data()
    unseen=set(range(9));Q=[];seed_orbits=[]
    while unseen:
        j=min(unseen);v={j:0}
        xs=[v]
        for k in (1,2):xs.append(apply(X,xs[-1]))
        assert all(len(q)==1 for q in xs)
        indices=[next(iter(q)) for q in xs]
        assert len(set(indices))==3
        unseen-=set(indices)
        seed_orbits.append(indices)
        base={next(iter(u)):next(iter(u.values())) for u in xs}
        assert apply(X,base)==base  # x eigenvalue 1
        q=base
        for _ in range(3):
            Q.append(q);q=apply(Y,q)
    assert len(Q)==9 and len(unseen)==0
    index={v:j for j,v in enumerate(orbit)}
    exponent=np.full((9,27),-1,dtype=np.int64)
    for row,q in enumerate(Q):
        for fiber,e in q.items():
            for k,vertex in enumerate(fibers[fiber]):
                exponent[row,index[vertex]]=(k-e)%3
    assert np.count_nonzero(exponent>=0)==81
    return exponent,Q,seed_orbits,orbit,x,y,z

def evaluate_mod(exponent,p):
    w=W.primitive_cube_root(p);inv3=pow(3,-1,p)
    T=np.zeros(exponent.shape,dtype=np.int64)
    Td=np.zeros((exponent.shape[1],exponent.shape[0]),dtype=np.int64)
    for a in range(exponent.shape[0]):
        for b in range(exponent.shape[1]):
            e=int(exponent[a,b])
            if e>=0:
                T[a,b]=pow(w,e,p)*inv3%p
                Td[b,a]=pow(w,(-e)%3,p)*inv3%p
    return T,Td,w

def verify():
    expo,Q,seed_orbits,orbit,x,y,z=exact_exponent_matrix()
    n=27;index={v:i for i,v in enumerate(orbit)}
    def pmat(g):
        P=np.zeros((n,n),dtype=np.int64)
        for j,v in enumerate(orbit):P[index[int(g(v))],j]=1
        return P
    Px=pmat(x);Py=pmat(y**-1);Pz=pmat(z)
    assert len(seed_orbits)==3
    # Exact cyclotomic integer arithmetic: omega^0=(1,0), omega=(0,1),
    # omega^2=(-1,-1) in the integral basis 1,omega. Every coefficient
    # of T9 is omega^e/3. All coisometry and equivariance identities are
    # verified as integer-pair equalities, not inferred from floating data.
    roots=((1,0),(0,1),(-1,-1))
    def c(e):return (0,0) if e<0 else roots[e%3]
    for a in range(9):
        for b in range(9):
            sums=[0,0]
            for j in range(27):
                ea,eb=int(expo[a,j]),int(expo[b,j])
                if ea<0 or eb<0:continue
                v=roots[(ea-eb)%3]
                sums[0]+=v[0];sums[1]+=v[1]
            assert tuple(sums)==(9 if a==b else 0,0),(a,b,sums)
    for j,ray in enumerate(orbit):
        ix,iy,iz=[index[int(g(ray))] for g in (x,y**-1,z)]
        for a in range(9):
            e=int(expo[a,j]);ex=int(expo[a,ix]);ey=int(expo[a,iy]);ez=int(expo[a,iz])
            q=a%3;prev=(a//3)*3+(q-1)%3
            assert c(ex)==c(-1 if e<0 else (e+q)%3)
            assert c(ey)==c(int(expo[prev,j]))
            assert c(ez)==c(-1 if e<0 else (e+1)%3)
    checks=[]
    for p in PRIMES:
        T,Td,w=evaluate_mod(expo,p)
        assert np.array_equal(T@Td%p,np.eye(9,dtype=np.int64))
        clock=np.diag([pow(w,q,p) for copy in range(3) for q in range(3)]).astype(np.int64)
        shift=np.kron(np.eye(3,dtype=np.int64),np.array([[0,0,1],[1,0,0],[0,1,0]],dtype=np.int64))
        assert np.array_equal(T@Px%p,clock@T%p)
        assert np.array_equal(T@Py%p,shift@T%p)
        assert np.array_equal(T@Pz%p,w*T%p)
        # Three source regular modules -> nine target Schr triples.
        Tbig=np.kron(np.eye(3,dtype=np.int64),T)%p
        Tbigdag=np.kron(np.eye(3,dtype=np.int64),Td)%p
        assert Tbig.shape==(27,81)
        assert np.array_equal(Tbig@Tbigdag%p,np.eye(27,dtype=np.int64))
        checks.append({'prime':p,'omega':w,'T9_nonzeros':81,'T27x81_nonzeros':243,
                       'coisometry_rank':27,'intertwines_x_y_inverse_z':True})
    return dict(status='PASS_EXACT_SPARSE_WITTING_H27_27X81_INTERTWINER',
      date='2026-11-22',algebraic_field='Z[omega,1/3], omega^2+omega+1=0',
      coefficient_formula='Each nonzero T[row,col]=omega^exponent/3; exponent -1 denotes zero.',
      H27_stabilizer_orbit_seeds=seed_orbits,
      all_9x27_exponents=expo.tolist(),
      full_27x81_sparsity='diag(T9,T9,T9), exactly 243 nonzeros',
      full_operator_target='I9 tensor Z3 and I9 tensor X3 for x and y^-1, scalar central omega',
      six_finite_field_certificates=checks,
      exact_Eisenstein_integer_pair_checks=True,
      exact_pair_basis='omega^0=(1,0), omega=(0,1), omega^2=(-1,-1) in Z[omega]',
      theorem='The explicit sparse 27x81 linear map is a surjective coisometric H27-intertwiner from three copies of the regular 27-ray address module to nine copies of the 3D Schrodinger operator module.',
      proof='Closed-form center Fourier vectors (1/sqrt3) sum_k omega^-k |z^k f> and x eigenvector vectors (1/sqrt3)(e+Xe+X^2 e), shifted by y^-q, give T entries omega^k/3. Coisometry and x/y^-1/center intertwining identities are checked exactly by integer-pair sums in the Z[omega] basis; six modular replicas are redundant independent controls.',
      prior_art='General Fourier decomposition and 27-to-27 obstruction already in repository; this adds a sparse Witting-ray-specific explicit coefficient matrix and exact modular checks.',
      physical_limit='Formal 27 ray-label vectors in C27 are not 27 orthogonal single-photon modes in physical C4; no extension to E6 cubic invariant or gauge interactions is obtained.')

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print('PASS EXACT sparse 27x81 H27 Fourier matrix in Z[omega]/3')

if __name__=='__main__':main()
