#!/usr/bin/env python3
"""Optimize ten-setting W33/Q8 tomography conditioning with unitary Givens steps.

Maintain eight published Bell contexts; optimize exactly two generic nine-mode
projective bases with deterministic stochastic Riemannian coordinate search.
No unique/global optimality claim.
"""
import json,math,sys,hashlib
from pathlib import Path
import numpy as np
from w33_20261109_q8_ten_context_tomography import select,projection_design

def givens_left(U,i,j,theta,phase):
    c,s=math.cos(theta),math.sin(theta)
    z=np.exp(1j*phase)
    V=U.copy()
    V[i,:]=c*U[i,:]-z*s*U[j,:]
    V[j,:]=z.conjugate()*s*U[i,:]+c*U[j,:]
    return V

def metrics(bell,op,U,V):
    m=np.vstack([bell,projection_design(U,op),projection_design(V,op)])
    eig=np.linalg.eigvalsh(m.T@m)
    return float(math.sqrt(eig[-1]/eig[0])),float(math.sqrt(eig[0])),float(math.sqrt(eig[-1]))

def main(path=None,return_components=False):
    seed=20261109228
    base,(B,U,V,op,_)=select(return_components=True)
    bell=projection_design(B,op)
    rng=np.random.default_rng(seed)
    start=metrics(bell,op,U,V)
    best=start[0]
    histories=[]
    improvements=0
    # random coordinate descent over a sequence of nine-mode Givens stages;
    # evaluated with the actual 90x80 measurement map, not just its local block.
    for scale,steps in ((.42,400),(.18,400),(.075,400),(.025,400)):
        gains=0
        for q in range(steps):
            which=int(rng.integers(0,2))
            i,j=sorted(rng.choice(9,size=2,replace=False))
            theta=rng.normal(0,scale)
            phi=float(rng.uniform(0,2*np.pi))
            altered=givens_left(U if which==0 else V,i,j,theta,phi)
            x,y=(altered,V) if which==0 else (U,altered)
            cond,_,_=metrics(bell,op,x,y)
            if cond<best:
                best=cond
                U,V=x,y
                gains+=1
                improvements+=1
        histories.append({"step_scale":scale,"trials":steps,
                          "accepted":gains,"achieved_cond":best})
    final=metrics(bell,op,U,V)
    assert final[0]<start[0]
    M=np.vstack([bell,projection_design(U,op),projection_design(V,op)])
    pinv=np.linalg.pinv(M,rcond=1e-14)
    rng2=np.random.default_rng(seed+7)
    errors=[]
    for rank in (1,2,3,5,9):
        for _ in range(12):
            X=rng2.normal(size=(9,rank))+1j*rng2.normal(size=(9,rank))
            rho=X@X.conj().T;rho/=np.trace(rho)
            p=np.concatenate([np.einsum("ij,ik,kj->j",E.conj(),rho,E).real
                              for E in [B[:,9*k:9*(k+1)] for k in range(8)]+[U,V]])
            w=pinv@(p-1/9)
            restored=np.eye(9)/9+np.einsum("k,kij->ij",w,op)
            errors.append(float(np.max(abs(restored-rho))))
    assert max(errors)<4e-12
    out={
        "status":"PASS_W33_Q8_TEN_SETTING_CONDITIONING_REFINED",
        "baseline_condition":start[0],
        "refined_condition":final[0],
        "relative_improvement":float(1-final[0]/start[0]),
        "baseline_min_singular":start[2],
        "refined_min_singular":final[2],
        "refined_max_singular":final[1],
        "settings":10,"rank":80,
        "total_candidate_rotations":sum(x["trials"] for x in histories),
        "accepted_improvements":improvements,
        "schedule":histories,
        "seed":seed,
        "refined_2bases_sha256":hashlib.sha256(np.ascontiguousarray(np.stack([U,V])).tobytes()).hexdigest(),
        "max_mixed_reconstruction_error":max(errors),
        "synthesizability":"Both are 9x9 unitaries: each can be compiled with 36 adjacent complex Givens and 9 phases; no physical photonic loss model implemented here",
        "claim_scope":"Best among a deterministic local stochastic search only, not proof of globally optimal near-tight tomography."
    }
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS refined 10-context",json.dumps({
        k:out[k] for k in ("baseline_condition","refined_condition",
                         "relative_improvement","accepted_improvements",
                         "max_mixed_reconstruction_error")}))
    if return_components:
        return out,(B,U,V,op)
    return out
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
