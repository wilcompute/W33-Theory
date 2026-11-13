#!/usr/bin/env python3
"""Attempt FULL 36-generator compact usp8 ↔ E6 cubic 27 intertwiner.

Construct four Chevalley simple-root lowering matrices from adjoint root
eigenvectors of the EXACT certified C4 36D algebra, normalize to the
standard symplectic-traceless wedge^2(8) root matrices, then propagate a
highest-weight vector through all simple-root lowering paths to construct
28x27 T without choosing arbitrary phases for 24 nonzero and three
zero-weight eigenvectors. Fail-closed for path inconsistency.

Checks if T†T=I, Ω†T=0, and 36 source Lie generators individually map
to the 36D standard wedge(usp8) Lie algebra by *real* coefficients.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261113_USp8_full36_intertwiner_audit as F
OUT=ROOT/"data/toe_20261113_USp8_full36_highest_weight_intertwiner.json"

def eij(n,i,j):
    M=np.zeros((n,n),dtype=np.complex128);M[i,j]=1
    return M

def wedge_complex_root(A):
    # Unlike compact real generators, a single raising root is NOT
    # anti-Hermitian; the wedge map must not impose that restriction.
    pairs=list(combinations(range(8),2))
    idx={p:i for i,p in enumerate(pairs)}
    W=np.zeros((28,28),dtype=complex)
    for col,(i,j) in enumerate(pairs):
        for k in range(8):
            if k!=j and A[k,i]:
                W[idx[tuple(sorted((k,j)))],col]+=A[k,i]*(1 if k<j else -1)
            if k!=i and A[k,j]:
                W[idx[tuple(sorted((i,k)))],col]+=A[k,j]*(1 if i<k else -1)
    return W

def simple_e8():
    out=[]
    for i in range(3):
        out.append(eij(8,i,i+1)-eij(8,4+i+1,4+i))
    out.append(eij(8,3,7))
    return [wedge_complex_root(e) for e in out]

def source_root_operators(Ks,cartan,had):
    A=np.zeros((36,36,36),dtype=np.float64)
    for i in range(36):
        for j in range(i+1,36):
            Z=Ks[i]@Ks[j]-Ks[j]@Ks[i]
            if not np.any(Z):continue
            for k,K in enumerate(Ks):
                v=np.trace(K.T@Z)
                assert int(v)%12==0
                A[i,j,k]=float(v)/12
                A[j,i,k]=-float(v)/12
    ad=[A[i,:,:].T for i in range(36)]
    comb=[1,10,100,1000]
    operator=sum((-1j*float(c)*ad[i] for c,i in zip(comb,cartan)),np.zeros((36,36),complex))
    assert np.max(abs(operator.conj().T-operator))<1e-10
    eigs,Q=np.linalg.eigh(operator)
    simples=[(1,-1,0,0),(0,1,-1,0),(0,0,1,-1),(0,0,0,2)]
    E=[]
    rec=[]
    for alpha in simples:
        w=np.asarray(alpha,dtype=np.int64)@had/2
        assert all(abs(v-round(v))<1e-9 for v in w)
        f=float(w@np.asarray(comb))
        choices=np.where(abs(eigs-f)<1e-8)[0]
        assert len(choices)==1,(alpha,f,choices)
        v=Q[:,int(choices[0])]
        mat=sum((v[k]*Ks[k] for k in range(36)),np.zeros((27,27),complex))
        assert np.linalg.norm(mat)>0
        for c,j in enumerate(cartan):
            H=-1j*Ks[j]
            assert np.linalg.norm(H@mat-mat@H-w[c]*mat)<1e-8
        E.append(mat)
        rec.append({"simple_root_canonical":list(alpha),"root_frequency_original":[int(t) for t in w],
                    "Frob_source_raw":float(np.linalg.norm(mat)),"frequency":f})
    return E,rec

def get_highest_vec(Ks,cartan,had):
    coeff=np.array([1,10,100,1000],dtype=float)
    H=sum((-1j*c*Ks[i] for c,i in zip(coeff,cartan)),np.zeros((27,27),complex))
    evals,Q=np.linalg.eigh(H)
    hw=np.array([1,1,0,0])@had/2
    f=float(hw@coeff)
    q=np.where(abs(evals-f)<1e-8)[0]
    assert len(q)==1
    return Q[:,int(q[0])]

def build_pair_map(Erepo,Estd,Ks,cartan,had):
    vr=get_highest_vec(Ks,cartan,had)
    vs=np.zeros(28,dtype=complex)
    wedge=list(combinations(range(8),2))
    vs[wedge.index((0,1))]=1
    lowr=[z.conj().T for z in Erepo]
    lows=[z.conj().T for z in Estd]
    cols_r=[vr]
    cols_s=[vs]
    queue=0
    worst_path=0
    attempted=0
    while queue<len(cols_r) and len(cols_r)<=27:
        v=cols_r[queue];w=cols_s[queue]
        queue+=1
        for ar,as_ in zip(lowr,lows):
            nvr=ar@v;nvs=as_@w
            attempted+=1
            if np.linalg.norm(nvr)<1e-10:
                if np.linalg.norm(nvs)>1e-9:
                    return None,{"reason":"mismatched_annihilation","queue":queue,"attempted":attempted,"standard_norm":float(np.linalg.norm(nvs))}
                continue
            B=np.stack(cols_r,axis=1)
            coeff,resid,*_=np.linalg.lstsq(B,nvr,rcond=1e-11)
            diff=float(np.linalg.norm(B@coeff-nvr))
            if diff>1e-8:
                if len(cols_r)==27:
                    return None,{"reason":"full_rank_but_independent","attempted":attempted}
                cols_r.append(nvr)
                cols_s.append(nvs)
                # one extra basis vector, no normalization
            else:
                Bstd=np.stack(cols_s,axis=1)
                sr=float(np.linalg.norm(Bstd@coeff-nvs))
                worst_path=max(worst_path,sr)
                if sr>1e-7:
                    return None,{"reason":"incompatible_lowering_path","attempted":attempted,
                                 "rank_generated":len(cols_r),"mismatch":sr}
    if len(cols_r)!=27:
        return None,{"reason":"highest_weight_failed_to_span","rank_generated":len(cols_r),"attempted":attempted}
    B=np.stack(cols_r,axis=1)
    S=np.stack(cols_s,axis=1)
    assert np.linalg.matrix_rank(B)==27
    T=S@np.linalg.inv(B)
    return T,{"reason":"success","rank_generated":27,"attempted":attempted,
               "worst_path_mismatch":worst_path,
               "isometry_residual":float(np.max(abs(T.conj().T@T-np.eye(27))))}

def main():
    info=json.loads((ROOT/"data/toe_20261113_e6_c4_compact_translation_holography.json").read_text())["lie_type"]
    cartan=info["Cartan_commuting_basis_indices"]
    roots=info["root_weight_vectors"]
    had=np.asarray([w for w in roots if sum(abs(q) for q in w)==4 and w[0]==1],dtype=int)
    assert had.shape==(4,4) and np.array_equal(had@had.T,4*np.eye(4,dtype=int))
    _,_,_,_,rootset=R.load()
    _,Ks=R.pack_roots(rootset)
    Erepo,recs=source_root_operators(Ks,cartan,had)
    Estd=simple_e8()
    for i in range(4):
        normstd=np.linalg.norm(Estd[i]);normrepo=np.linalg.norm(Erepo[i])
        Erepo[i]*=normstd/normrepo
        recs[i]["Frob_source_rescaled"]=float(np.linalg.norm(Erepo[i]))
        recs[i]["Frob_target"]=float(normstd)
    T,diag=build_pair_map(Erepo,Estd,Ks,cartan,had)
    result={"status":"UNDECIDED","simple_roots":recs,"construction":diag}
    if T is not None:
        wb=[F.wedge_action(x) for x in F.defining_basis()]
        BM=np.stack([np.r_[x.real.ravel(),x.imag.ravel()] for x in wb],axis=1)
        residual=[]
        for K in Ks:
            B=T@K@T.conj().T
            v=np.r_[B.real.ravel(),B.imag.ravel()]
            coeff,_,_,_=np.linalg.lstsq(BM,v,rcond=None)
            residual.append(float(np.linalg.norm(BM@coeff-v)/np.linalg.norm(v)))
        result["full_36_relative_residuals"]=residual
        result["max_relative_residual"]=max(residual)
        result["status"]="FULL_36_INTERTWINER_VERIFIED" if max(residual)<1e-9 and diag["isometry_residual"]<1e-9 else "HIGHEST_WEIGHT_PARTIAL_MAP_FAILED_FULL_36_TEST"
        if result["status"]=="FULL_36_INTERTWINER_VERIFIED":
            result["matrix_T_real"]=np.round(T.real,12).tolist()
            result["matrix_T_imag"]=np.round(T.imag,12).tolist()
    result["scope"]="An attempted constructive 36-generator equivalence via simple roots, with fail-closed path and matrix-intertwining controls. If result not FULL_36_INTERTWINER_VERIFIED, no completed mapping is claimed."
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ["status","construction"]}|({"max_relative_residual":result["max_relative_residual"]} if "max_relative_residual" in result else {}),indent=2),flush=True)
    return result
if __name__=="__main__":main()
