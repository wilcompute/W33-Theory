#!/usr/bin/env python3
"""W33 controlled-phase nonlocal optimality modulo local one-register phases.

Known W33 binary adjacency 2-rank=16: prior repository Pass 88 and
2026-08-29 adjacency sentinel extension. New hardware connection:
double-centering the phase incidence matrix gives exact rank 14.
This is the minimal number of independent binary bilinear cross-register
coupling terms if one-body diagonal phase tables are supplied for free.
Local tables and reversible address-flag compute/uncompute STILL COST HARDWARE.
"""
import hashlib,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_photonic_five_fronts_GF2_phase_causal_break_20261023 import adjacency

def rank_factor(m):
    m=np.asarray(m,dtype=np.uint8)
    assert set(np.unique(m)).issubset({0,1})
    nr,nc=m.shape
    rows=[sum(int(m[i,j])<<j for j in range(nc)) for i in range(nr)]
    selected=[]
    echelon={}
    for initial in rows:
        x=initial;coeff=0
        while x:
            k=x.bit_length()-1
            if k in echelon:
                reduced,rep=echelon[k];x^=reduced;coeff^=rep
            else:
                q=len(selected);selected.append(initial)
                echelon[k]=(x,coeff^(1<<q))
                break
    r=len(selected)
    left=np.zeros((nr,r),dtype=np.uint8)
    right=np.zeros((nc,r),dtype=np.uint8)
    for i,initial in enumerate(rows):
        x=initial;coeff=0
        while x:
            k=x.bit_length()-1
            red,rep=echelon[k]
            x^=red;coeff^=rep
        for q in range(r):left[i,q]=(coeff>>q)&1
    for q,bits in enumerate(selected):
        for j in range(nc):right[j,q]=(bits>>j)&1
    assert np.array_equal((left.astype(int)@right.T.astype(int))%2,m)
    return left,right

def centered(a,base=0):
    x=np.asarray(a,dtype=np.uint8)
    return x^x[:,base,None]^x[base,None,:]^int(x[base,base])

def certificate():
    A=adjacency()
    left16,right16=rank_factor(A)
    assert left16.shape==(40,16)
    B=centered(A)
    left14,right14=rank_factor(B)
    assert left14.shape==(40,14)
    localL=A[:,0].copy()
    localR=A[0,:].copy()
    reconstructed=((left14.astype(int)@right14.T.astype(int))%2).astype(np.uint8)^localL[:,None]^localR[None,:]
    assert np.array_equal(reconstructed,A)
    # Strict lower bound under arbitrary local single-register +/-1 phases:
    # double-centering kills u(i),v(j),global; B=double_center(A)
    # = P (A+u 1^T+1 v^T+g11^T) Q where P,Q are binary row/column maps;
    # rank(B) <= rank(any compensated interaction matrix).
    assert np.all(B[:,0]==0) and np.all(B[0,:]==0)
    for base in range(40):
        assert rank_factor(centered(A,base))[0].shape[1]==14
    rng=np.random.default_rng(20261023)
    for _ in range(32):
        u=rng.integers(0,2,40,dtype=np.uint8)
        v=rng.integers(0,2,40,dtype=np.uint8)
        compensated=A^u[:,None]^v[None,:]
        assert np.array_equal(centered(compensated),B)
        assert rank_factor(compensated)[0].shape[1]>=14
    return {'schema':'w33.phase_oracle.mod_local_gauge_rank14.v1',
      'preexisting_W33_Gf2_adjacency_rank':16,
      'W33_rank16_prior_repo_paths':['analysis/w33_pass88_smith_group.py','analysis/w33_20260829_adjacency_sentinel_extension.py'],
      'new_optimal_cross_register_couplings':14,
      'left_local_phase_flags_from_A_column0':localL.astype(int).tolist(),
      'right_local_phase_flags_from_A_row0':localR.astype(int).tolist(),
      'left_cross_bit_lookup_40x14':left14.astype(int).tolist(),
      'right_cross_bit_lookup_40x14':right14.astype(int).tolist(),
      'all_1600_phase_pairs_checked':1600,
      'basepoints_checked':40,'random_local_compensations_checked':32,
      'exact_identity':'A[a,b] = A[a,0] XOR A[0,b] XOR XOR_{k=1..14}(L[a,k] AND R[b,k]); A[0,0]=0',
      'proof_of_lower_bound':'C=A+u*1^T+1*v^T+g*J; double_center(C)=B=double_center(A), with double_center(C)=P*C*Q over F2 and rank(P*C*Q)<=rank(C). rank_F2(B)=14. The choice C=B attains 14.',
      'physical_resource_count':'14 logical cross-register parity products + two single-register diagonal phase lookup tables + compute/uncompute of 28 Boolean address flags; no foundry hardware costs established',
      'interpretation':'Exact gate specification optimal only for binary bilinear parity-product cross couplings with unrestricted local diagonal phase lookup, not universal optical mesh or minimal MZI count.'}

if __name__=='__main__':
    c=certificate()
    c['sha256']=hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    p=ROOT/'data/w33_phase_oracle_mod_local_gauge_rank14_20261023.json'
    p.write_text(json.dumps(c,indent=2,sort_keys=True)+'\n')
    print('PASS 40 basepoints and 1600 phases; W33 rank16 -> nonlocal gauge rank14, optimal')
