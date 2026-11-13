#!/usr/bin/env python3
"""Explicit 28x27 isometric Cartan intertwiner from the repo E6(6)
27 representation into Λ²_0(C8), symplectic traceless USp8 module.

INTERTWINES ONLY FOUR COMMUTING CARTAN GENERATORS. Does NOT yet match
remaining 32 non-Cartan compact generators and cannot serve as an
entire Lie-algebra intertwiner without further proof.
"""
from pathlib import Path
import json,sys,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
OUT=ROOT/"data/toe_20261113_usp8_27_Cartan_isometric_intertwiner.json"

def main():
    prev=json.loads((ROOT/"data/toe_20261113_usp8_27_weight_character_bridge.json").read_text())
    ks=prev["compact_Cartan_indices"]
    had=np.asarray(prev["Hadamard_root_basis_rotation"],dtype=int)
    assert had.shape==(4,4) and np.array_equal(had@had.T,4*np.eye(4,dtype=int))
    _,_,_,_,roots=R.load()
    _,K=R.pack_roots(roots)
    H=[K[i].astype(float) for i in ks]
    coeff=np.array([1,10,100,1000],dtype=float)
    A=sum((z*x for z,x in zip(coeff,H)),np.zeros((27,27),dtype=float))
    evals,Q=np.linalg.eigh(-1j*A)  # Hermitian, real integer frequencies
    weights=[]
    for v in Q.T:
        w=[]
        for hi in H:
            z=np.vdot(v,(-1j*hi)@v)
            assert abs(z.imag)<1e-9 and abs(z.real-round(z.real))<1e-9
            w.append(int(round(z.real)))
        assert abs(np.dot(coeff,w)-np.vdot(v,(-1j*A)@v).real)<1e-8
        weights.append(tuple(w))
    canon=[]
    for w in weights:
        wc=np.dot(had,np.asarray(w,dtype=int))
        assert all(int(t)%2==0 for t in wc)
        canon.append(tuple((wc//2).tolist()))
    assert len(canon)==27 and canon.count((0,0,0,0))==3
    # Standard USp8 highest-weight defining module C8:
    # four vectors weight +eps_i and their symplectic partners -eps_i.
    defining=[tuple(1 if j==i else 0 for j in range(4)) for i in range(4)]
    defining += [tuple(-1 if j==i else 0 for j in range(4)) for i in range(4)]
    pairs=list(itertools.combinations(range(8),2))
    assert len(pairs)==28
    pair_weight=[tuple(defining[i][j]+defining[k][j] for j in range(4)) for i,k in pairs]
    group={}
    for p,w in enumerate(pair_weight):group.setdefault(w,[]).append(p)
    assert len(group[(0,0,0,0)])==4
    zidx=group[(0,0,0,0)]
    # Complete an orthonormal basis for the 4 zero-weight pairs,
    # orthogonal to the invariant symplectic vector Ω ∝ sum_i e_i∧e_-i.
    n=np.zeros((28,1),complex)
    for ix in zidx:n[ix,0]=1/2
    vals=[]
    for q in zidx[:3]:
        v=np.zeros(28,dtype=np.complex128)
        v[q]=1
        v-=n[:,0]*np.vdot(n[:,0],v)
        for w in vals:v-=w*np.vdot(w,v)
        v/=np.linalg.norm(v)
        vals.append(v)
    assert len(vals)==3
    W=np.zeros((28,27),dtype=np.complex128)
    zz=0
    for i,w in enumerate(canon):
        if w==(0,0,0,0):
            W[:,i]=vals[zz];zz+=1
        else:
            assert len(group[w])==1,(w,group.get(w))
            W[group[w][0],i]=1
    assert np.max(abs(W.conj().T@W-np.eye(27)))<1e-10
    assert np.max(abs(n.conj().T@W))<1e-10
    T=W@Q.conj().T
    assert T.shape==(28,27)
    assert np.max(abs(T.conj().T@T-np.eye(27)))<1e-10
    # Original basis coordinates H_i commute with compact USp8 Cartan,
    # represented on each wedge pair by the sum of standard weights
    # rotated back through the Hadamard. Defining weights in original
    # coordinates are 1/2 * w_canonical @ Hadamard.
    allres=[]
    for j,hi in enumerate(H):
        std_diag=[1j*sum(pair_weight[p][k]*had[k,j] for k in range(4))/2
                  for p in range(28)]
        hw=np.diag(std_diag)
        residual=float(np.max(abs(T@hi-hw@T)))
        allres.append(residual)
        assert residual<1e-9,(j,residual)
        assert np.max(abs(hw@n))<1e-10
    # Save an explicit exact-to-numerical matrix with deterministic phase
    # convention from eigh, rounded enough for independent replay.
    result={
      "status":"PASS_EXPLICIT_28_BY_27_CARTAN_ISOMETRIC_INTERTWINER_TO_USP8_LAMBDA2_0",
      "intertwines_four_Cartan_generators":True,
      "intertwines_all_36_compact_generators":False,
      "repo_Cartan_generator_indices":ks,
      "qutrit_root_wts_in_repo_frame":[list(w) for w in weights],
      "weight_dict_to_USp8_standard":[list(w) for w in canon],
      "standard_wedge_pair_indices":[list(p) for p in pairs],
      "standard_zero_weight_pair_indices":zidx,
      "matrix_size":[28,27],
      "matrix_real":np.round(T.real,13).tolist(),
      "matrix_imag":np.round(T.imag,13).tolist(),
      "isometry_max_residual":float(np.max(abs(T.conj().T@T-np.eye(27)))),
      "symplectic_trace_max_residual":float(np.max(abs(n.conj().T@T))),
      "four_Cartan_intertwiner_residuals":allres,
      "scope":"A concrete isometric weight-frame embedding of the E6(6) real 27 into the 27D complex symplectic-traceless exterior-square module, matching all four Cartan actions. It does NOT yet determine the non-Cartan root operators in the defining 8D representation or fix their phases."
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in [
      "status","matrix_size","isometry_max_residual",
      "symplectic_trace_max_residual","four_Cartan_intertwiner_residuals"]},indent=2),flush=True)
    return result
if __name__=="__main__":main()
