#!/usr/bin/env python3
"""Exact phase-signature pigeonhole obstruction + constructive 4-bit search.
Prior art: 2026-11-03 numerical rank sweep and 216-port POVM.
"""
from pathlib import Path
import sys,math,json
import numpy as np
from scipy.linalg import eigvalsh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_five_deeper_fronts import route_frame
from w33_20261103_three_setting_ic_povm import embed_effects

def blind_bound(n,b,m):
    # Signature of each input mode is (mask[1] mod 2^(b-1),...).
    # If two signatures agree, each relative phase in every setting is 0 or pi;
    # real receiver effects cannot see i(|j><k|-|k><j|).
    slots=2**((b-1)*(m-1))
    a,r=divmod(n,slots)
    blind=(slots-r)*a*(a-1)//2+r*a*(a+1)//2
    return {'bits':b,'settings':m,'modes':n,'signature_capacity':slots,
            'forced_blind_imaginary_pairs':blind,
            'hermitian_rank_upper_bound':n*n-blind,
            'full_IC_excluded_by_collision':blind>0}

def sample_unique_masks(rng,b,n):
    h=2**(b-1)
    chosen=rng.choice(h*h,size=n,replace=False)
    rng.shuffle(chosen)
    a=chosen//h; bb=chosen%h
    flip=rng.integers(0,2,size=(2,n))
    a=a+h*flip[0];bb=bb+h*flip[1]
    return a.astype(int),bb.astype(int)

def evaluate(F0,V,a,b,bits):
    h=2**bits
    D1=np.diag(np.exp(2j*np.pi*a/h))
    D2=np.diag(np.exp(2j*np.pi*b/h))
    X=np.vstack((F0,embed_effects(V,D1),embed_effects(V,D2)))
    Gram=X.T@X
    ev=eigvalsh(Gram,subset_by_index=[0,0],check_finite=False)[0]
    # Largest eigenvalue 1/3 from three scalar identity columns.
    # Check norm upper bound <= 1/3 from previous exact frame.
    assert abs((Gram@np.r_[np.ones(24),np.zeros(552)])[0]-1/3)<1e-9
    return float(ev),X

def main():
    theory={str(b):blind_bound(24,b,3) for b in (1,2,3,4,5,6)}
    assert theory['2']['forced_blind_imaginary_pairs']==60
    assert theory['3']['forced_blind_imaginary_pairs']==8
    assert theory['4']['forced_blind_imaginary_pairs']==0
    assert blind_bound(24,2,5)['forced_blind_imaginary_pairs']>0
    assert blind_bound(24,2,6)['forced_blind_imaginary_pairs']==0
    Z,_=route_frame()
    w,Q=np.linalg.eigh((Z.T@Z).astype(float))
    V=Z@Q[:,16:]/math.sqrt(360)
    for j in range(24):
        if V[np.argmax(abs(V[:,j])),j]<0:V[:,j]*=-1
    F0=embed_effects(V,np.eye(24,dtype=complex))
    rng=np.random.default_rng(20261102)
    tests=[];best=None
    for j in range(45):
        a,b=sample_unique_masks(rng,4,24)
        min_eig,_=evaluate(F0,V,a,b,4)
        if best is None or min_eig>best['min_eigenvalue']:
            best={'bits':4,'trial':j,'min_eigenvalue':min_eig,'phase_mask_1':a.tolist(),
                   'phase_mask_2':b.tolist(),'condition_estimate':float(math.sqrt((1/3)/min_eig)) if min_eig>0 else None}
            print('BEST4',j,min_eig,best['condition_estimate'],flush=True)
        tests.append({'trial':j,'min_eigenvalue':min_eig})
    assert best['min_eigenvalue']>1e-10,'No full-rank four-bit candidate in designed sample'
    a=np.array(best['phase_mask_1']);b=np.array(best['phase_mask_2'])
    minimum,X=evaluate(F0,V,a,b,4)
    eigs=np.linalg.eigvalsh(X.T@X)
    rank=int(np.count_nonzero(eigs>1e-10))
    assert rank==576
    nshots_001=int(math.ceil(1/(216*minimum*.01**2)))
    result={'status':'PASS_EXACT_SIGNATURE_NO_GO_AND_NUMERIC_4BIT_WITNESS',
            'theorem':'For a real rank-one POVM with n input modes, m settings including an all-zero reference, and b-bit phase masks, modes share modulo-2^(b-1) signatures in at most 2^((b-1)(m-1)) classes. Every pair in a class has an undetectable imaginary Hermitian coherence. Minimum blindness is sum binomial(group sizes,2), balanced by pigeonhole.',
            'rigorous_upper_bounds':theory,
            'four_bit_search_count':len(tests),
            'candidate_winners':sum(x['min_eigenvalue']>1e-10 for x in tests),
            'four_bit_min_eigenvalue_trials':tests,
            'constructive_four_bit_candidate':best,
            'four_bit_hermitian_rank':rank,
            'four_bit_full_rank_numeric_tolerance':1e-10,
            'minimum_detected_photons_per_setting_for_0p01_weak_axis_CRB':nshots_001,
            'measurement_basis':'24 orthonormal input modes from the existing 216x40 sign matrix positive-eigenspace eigendecomposition. This phase coordinate system is basis-dependent; calibrate before hardware.',
            'scope':'Combinatorial non-IC obstruction exact independent of detector geometry; full rank of a four-bit numerical candidate computed double precision; finite detector loss and gain not yet included.'}
    p=ROOT/'data/w33_20261102_phase_signature_no_go_4bit.json'
    p.write_text(json.dumps(result,indent=2)+'\n')
    print('FINAL',json.dumps({'rigorous_bounds':theory,'best':best,'rank':rank,'samples':len(tests),'shots01':nshots_001})[:4300],flush=True)
    return result
if __name__=='__main__':main()
