#!/usr/bin/env python3
"""Seven symplectic hyperbolic pairs behind the locally gauged W33 oracle.

B=double_center(W33 adjacency) is symmetric and zero-diagonal over F2,
hence alternating, rank14. Construct B=sum_{k=1}^7
 (x_k*y_k^T + y_k*x_k^T), a canonical symplectic-type factorization
(not a canonical choice of individual basis vectors).
"""
import json,hashlib,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_phase_oracle_mod_local_gauge_rank14_20261023 import centered,rank_factor
from w33_photonic_five_fronts_GF2_phase_causal_break_20261023 import adjacency

def pairs_from_alternating(M):
    R=np.array(M,dtype=np.uint8).copy()
    assert np.array_equal(R,R.T) and not np.any(np.diag(R))
    pairs=[]
    while R.any():
        i,j=next((i,j) for i in range(R.shape[0]) for j in range(i+1,R.shape[1]) if R[i,j])
        x=R[:,i].copy();y=R[:,j].copy()
        assert np.dot(x.astype(int),np.eye(len(x),dtype=int)[:,j])==1
        correction=(x[:,None]*y[None,:])^(y[:,None]*x[None,:])
        R^=correction
        assert not np.any(R[i,:]) and not np.any(R[j,:])
        pairs.append((x,y))
    return pairs

def certificate():
    A=adjacency()
    B=centered(A)
    p=pairs_from_alternating(B)
    assert len(p)==7
    M=np.zeros((40,40),dtype=np.uint8)
    for x,y in p:M^=(x[:,None]*y[None,:])^(y[:,None]*x[None,:])
    assert np.array_equal(M,B)
    local1=A[:,0];local2=A[0,:]
    assert np.array_equal(M^local1[:,None]^local2[None,:],A)
    return {'schema':'w33.phase_oracle.7_symplectic_pairs.v1',
      'W33_binary_A_rank':16,'locally_gauged_alternating_rank':14,
      'symplectic_hyperbolic_pair_count':7,
      'two_cross_parity_terms_per_pair':2,'total_cross_parity_terms':14,
      'first_local_sign_table':local1.astype(int).tolist(),
      'second_local_sign_table':local2.astype(int).tolist(),
      'seven_pairs':[
          {'index':i,'x_flag_40':x.astype(int).tolist(),'y_flag_40':y.astype(int).tolist()}
          for i,(x,y) in enumerate(p)],
      'all_1600_compiled_phases_exact':True,
      'proof':'B=A+A[:,0]1^T+1A[0,:] is alternating rank14. Repeatedly peel x*y^T+y*x^T where x=B[:,i],y=B[:,j],B[i,j]=1, decreasing rank by 2 until zero. Restore two local phase tables.',
      'prior_art':'Finite field alternating form decomposition is standard. A has 2-rank 16 in existing repository Pass88/2026-08-29. New deliverable is a seven-pair exact W33 phase-oracle compiler certificate.',
      'optical_limits':'Seven pairs are algebraic logical controls, NOT seven MZIs or seven optical entangling devices. Boolean decoding and physical coherent two-address CZ phases need implementation.'}
if __name__=='__main__':
    x=certificate()
    x['sha256']=hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    p=ROOT/'data/w33_phase_oracle_seven_symplectic_pairs_20261023.json'
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
    print('PASS W33 seven hyperbolic pairs, 14 cross terms + local phase tables, all 1600 addresses')
