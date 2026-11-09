#!/usr/bin/env python3
"""12-setting W33 correlation plus local-qutrit MUB informational completion.

Eight Bell Q8 contexts span all 64 correlations; four matched product MUB
settings resolve the 16 invisible local Bloch directions. This is known
finite MUB tomography used as an explicit W33 physical protocol check.
"""
import json,sys
from pathlib import Path
import numpy as np
from w33_20261109_q8_correlation_five import (
    frames,frame_map,probabilities,tensor_recovered
)

def single_qutrit_H():
    H=[]
    for i in range(3):
        for j in range(i+1,3):
            x=np.zeros((3,3),complex);x[i,j]=x[j,i]=1/np.sqrt(2);H.append(x)
            y=np.zeros((3,3),complex);y[i,j]=-1j/np.sqrt(2);y[j,i]=1j/np.sqrt(2);H.append(y)
    H += [np.diag([1,-1,0])/np.sqrt(2),np.diag([1,1,-2])/np.sqrt(6)]
    return np.array(H)

def product_mub():
    w=np.exp(2j*np.pi/3)
    F=np.array([[w**(i*j) for j in range(3)] for i in range(3)])/np.sqrt(3)
    P=np.diag([1,1,w])
    U=[np.eye(3),F,P@F,P@P@F]
    cross=max(float(np.max(abs(abs(U[i].conj().T@U[j])**2-1/3)))
              for i in range(4) for j in range(i+1,4))
    assert cross<5e-13
    return U,cross

def reconstruct(Eb,A,U,ops,rho):
    pe=probabilities(Eb,rho)
    T=tensor_recovered(A,pe)
    pprod=np.array([probabilities(np.kron(B,B),rho).reshape(3,3) for B in U])
    marginal_A=np.array([p.sum(axis=1) for p in pprod])
    marginal_B=np.array([p.sum(axis=0) for p in pprod])
    # Single-qutrit MUB tomography identity: sum_{settings,outcomes} p P = rho + I3.
    rA=-np.eye(3,dtype=complex)
    rB=-np.eye(3,dtype=complex)
    for basis,pa,pb in zip(U,marginal_A,marginal_B):
        for j in range(3):
            Pj=np.outer(basis[:,j],basis[:,j].conj())
            rA+=pa[j]*Pj
            rB+=pb[j]*Pj
    H=[h.reshape(3,3) for h in ops]
    out=np.eye(9,dtype=complex)/9
    for j in range(8):
        out+=np.trace(rA@H[j])*np.kron(H[j],np.eye(3))/3
        out+=np.trace(rB@H[j])*np.kron(np.eye(3),H[j])/3
        for k in range(8):
            out+=T[j,k]*np.kron(H[j],H[k])
    return out,rA,rB,pe,pprod

def main(path=None):
    _,fam=frames()
    U,mub_error=product_mub()
    H=single_qutrit_H()
    op_corr=np.array([np.kron(x,y) for x in H for y in H])
    op_A=np.array([np.kron(x,np.eye(3))/np.sqrt(3) for x in H])
    op_B=np.array([np.kron(np.eye(3),x)/np.sqrt(3) for x in H])
    allops=np.concatenate([op_corr,op_A,op_B])
    assert allops.shape==(80,9,9)
    Eb=fam[0]
    A=frame_map(Eb,op_corr)
    bell=np.array([np.einsum("i,kij,j->k",e.conj(),allops,e).real for e in Eb.T])
    prod=np.array([np.einsum("i,kij,j->k",e.conj(),allops,e).real
                   for basis in U for e in np.kron(basis,basis).T])
    rankB=np.linalg.matrix_rank(bell,tol=1e-10)
    rankP=np.linalg.matrix_rank(prod,tol=1e-10)
    total=np.vstack((bell,prod))
    rankCombined=np.linalg.matrix_rank(total,tol=1e-10)
    assert rankB==64 and rankCombined==80
    svals=np.linalg.svd(total,compute_uv=False)
    # At least 4 matched product settings needed to capture 2 local generators
    # from each local qutrit per product setting.
    for q in range(1,4):
        short=np.vstack((bell,prod[:9*q]))
        assert np.linalg.matrix_rank(short,tol=1e-10)<80

    rng=np.random.default_rng(20261109)
    tests=[]
    for rank in (1,2,3,5,9):
        for _ in range(12):
            x=rng.normal(size=(9,rank))+1j*rng.normal(size=(9,rank))
            rho=x@x.conj().T
            rho/=np.trace(rho)
            r,a,b,pe,pp=reconstruct(Eb,A,U,H,rho)
            targetA=np.einsum('ibjb->ij',rho.reshape(3,3,3,3))
            targetB=np.einsum('aiaj->ij',rho.reshape(3,3,3,3))
            err=float(np.max(abs(r-rho)))
            errA=float(np.max(abs(a-targetA)))
            errB=float(np.max(abs(b-targetB)))
            tests.append((err,errA,errB))
            assert max(err,errA,errB)<5e-12
    # Maximal indistinguishability under all 24 Bell contexts:
    r0=np.eye(9)/9
    r1=np.kron(np.diag([1,0,0]),np.eye(3)/3)
    bmatch=max(float(np.max(abs(probabilities(E,r0)-probabilities(E,r1))))
               for E in fam)
    p_diff=max(float(np.max(abs(probabilities(np.kron(B,B),r0)-probabilities(np.kron(B,B),r1))))
               for B in U)
    assert bmatch<5e-13 and p_diff>0.1
    out={
      "status":"PASS_12SETTING_FULL_TWO_QUTRIT_TOMOGRAPHY_WITH_Q8_CORRELATION_FRAME",
      "bell_settings":8,"bell_outcomes":72,"bell_rank":int(rankB),
      "product_settings":4,"product_outcomes":36,"product_rank":int(rankP),
      "combined_rank":int(rankCombined),"all_traceless_density_parameters":80,
      "local_generators_added":16,
      "product_MUB_overlap_error":mub_error,
      "smallest_combined_singular_value":float(min(svals)),
      "largest_combined_singular_value":float(max(svals)),
      "combined_condition_number":float(max(svals)/min(svals)),
      "max_reconstruction_error":max(x[0] for x in tests),
      "max_marginal_reconstruction_error":max(max(x[1:]) for x in tests),
      "random_density_controls":len(tests),
      "bell_only_indistinguishable_max_error":bmatch,
      "product_setting_discrimination_max_difference":p_diff,
      "explicit_pair":["I9/9","|0><0| tensor I3/3"],
      "minimum_four_matched_product_settings_in_this_protocol":True,
      "not_global_minimum_number_of_arbitrary_projective_settings":True,
      "reconstruction":"rho=I9/9+sum_ab T_ab Ha⊗Hb+(1/3)sum_a tr(rhoA Ha)Ha⊗I+(1/3)sum_b tr(rhoB Hb)I⊗Hb",
      "scope":"This is informationally complete with ideal calibrated projective settings. Standard complete qutrit MUB marginal tomography, not an original general theorem or a physical chip."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS 12-settings",json.dumps({
        "rank":int(rankCombined),"cond":out["combined_condition_number"],
        "error":out["max_reconstruction_error"],"random_tests":len(tests)}))
    return out
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
