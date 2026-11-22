#!/usr/bin/env python3
"""Exact cyclotomic full two-D Hessian macro compiler, not a sampled search.

All 648 Hessian matrices lie in Mat_4((1/3)Z[omega]); the phase flip D does
as well. Therefore every H D N D N matrix has entries (a+b omega)/243,
with integer coefficients. A pair-int16 key is EXACT, not floating-point or
single-prime hashing. All 472392 words are examined.
"""
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.stats import unitary_group
import toe_20261122_witting_one_phase_three_fixed as W
import toe_20261122_next5_hessian_coset_compiler as C
import toe_20261122_h27_central_fourier_bridge as H27
import toe_20261122_next5_compiler_photonics as O
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_further_two_D_exact.json'

def sumz(vals):
    x=W.Z
    for y in vals:x=W.add(x,y)
    return x

def mulq(A,B):
    return tuple(tuple(sumz(W.mul(A[i][k],B[k][j]) for k in range(4))
                       for j in range(4)) for i in range(4))

def exact_H_and_D(words):
    I=tuple(tuple(W.O if i==j else W.Z for j in range(4)) for i in range(4))
    rays=W.all_rays()
    def g(k):
        return tuple(tuple(W.reflect(rays[k],tuple(I[i][j] for i in range(4)))[r]
                           for j in range(4)) for r in range(4))
    ga={l:g(j) for l,j in [('a',5),('b',26),('c',33)]}
    for k in ('a','b','c'):ga[k.upper()]=mulq(ga[k],ga[k])
    mats={'':I}
    for word,_ in words:
        if word:mats[word]=mulq(mats[word[:-1]],ga[word[-1]])
    assert len(mats)==648
    D=tuple(tuple(W.add(I[i][j],W.scale(W.mul(rays[36][i],W.conj(rays[36][j])),F(-2,3)))
                       for j in range(4)) for i in range(4))
    def three(A):
        arr=np.zeros((4,4,2),dtype=np.int64)
        for i in range(4):
            for j in range(4):
                a,b=A[i][j]
                assert (3*a).denominator==(3*b).denominator==1
                arr[i,j,:]=(int(3*a),int(3*b))
        return arr
    return np.stack([three(mats[word]) for word,_ in words]),three(D)

def mulz(A,B):
    a,b=A[...,0],A[...,1]
    c,d=B[...,0],B[...,1]
    bd=np.matmul(b,d)
    return np.stack((np.matmul(a,c)-bd,np.matmul(a,d)+np.matmul(b,c)-bd),axis=-1)

def exact_census():
    words=C.hessian_words()
    group,_,_,_,_=H27.heisenberg_action()
    nset={tuple(int(g(i)) for i in range(40)) for g in group.generate_schreier_sims()}
    word_idx={q:i for i,(_,q) in enumerate(words)}
    normal_idx=[word_idx[p] for p in sorted(nset)]
    assert len(normal_idx)==27
    H,D=exact_H_and_D(words);N=H[normal_idx]
    assert H.shape==(648,4,4,2) and N.shape==(27,4,4,2)
    S1=set();S2=set();largest=0
    for hmat in H:
        HD=mulz(hmat,D)
        HDN=mulz(HD,N)              # denominator 27
        for row in HDN:
            S1.add(row.astype('<i2').tobytes())
        HDND=mulz(HDN,D)
        HDNDN=mulz(HDND[:,None,:,:,:],N[None,:,:,:,:]) # denominator 243
        largest=max(largest,int(np.max(np.abs(HDNDN))))
        assert largest<32768
        for row in HDNDN.reshape(729,4,4,2).astype('<i2'):
            S2.add(row.tobytes())
    assert len(S1)==17496 and len(S2)==385560,(len(S1),len(S2))
    # H belongs to two-D words by inserting D^2=I.
    assert all((hmat*81).astype('<i2').tobytes() in S2 for hmat in H)
    digest=hashlib.sha256(b''.join(sorted(S2))).hexdigest()
    assert digest=='e50c2d9c40d10e05a63b807f938a05443178b79c6963061c25ed4834f93bde42'
    return words,normal_idx,dict(H_group_order=648,normal_H27_order=27,
       first_D_stage_unique_matrices=len(S1),second_D_stage_raw_words=648*27*27,
       second_D_stage_exact_unique_matrices=len(S2),
       same_word_collision_excess=648*27*27-len(S2),
       H_inside_two_D=True,common_cyclotomic_denominator_second_stage=243,
       largest_exact_integer_coefficient=largest,
       exact_second_stage_matrix_set_sha256=digest)

def bench(words,normal_idx):
    G=O.gates();I=np.eye(4,dtype=complex)
    H=[]
    for word,_ in words:
        mat=I
        for ch in word:mat=mat@G[ch]
        H.append(mat)
    H=np.stack(H);N=H[normal_idx];D=G['d']
    rng=np.random.default_rng(20261122)
    targets=[unitary_group.rvs(4,random_state=rng) for _ in range(3)]
    best1=[(-1.,None) for _ in targets];best2=[(-1.,None) for _ in targets]
    for i,hmat in enumerate(H):
        HD=hmat@D
        HDN=HD@N
        val2=(HDN@D)[:,None,:,:]@N[None,:,:,:]
        for j,U in enumerate(targets):
            tr1=np.abs(np.einsum('ij,kji->k',U.conj().T,HDN,optimize=True))/4
            k1=int(np.argmax(tr1));v1=float(tr1[k1])
            if v1>best1[j][0]:best1[j]=(v1,(i,k1))
            tr2=np.abs(np.einsum('ij,abji->ab',U.conj().T,val2,optimize=True))/4
            k2,l2=np.unravel_index(int(np.argmax(tr2)),tr2.shape);v2=float(tr2[k2,l2])
            if v2>best2[j][0]:best2[j]=(v2,(i,k2,l2))
    result=[]
    for j in range(3):
        s1=(2-2*best1[j][0])**.5;s2=(2-2*best2[j][0])**.5
        assert s2<=s1+1e-12
        i,k,l=best2[j][1]
        word=words[i][0]+'d'+words[normal_idx[k]][0]+'d'+words[normal_idx[l]][0]
        result.append(dict(haar_target_seed=20261122,target_index=j,
            one_D_best_projective_Frobenius=s1,
            two_D_best_projective_Frobenius=s2,
            two_D_compiled_word=word,primitive_length=len(word),
            process_infidelity=1-best2[j][0]**2))
    return result

def verify():
    words,n,exact=exact_census();results=bench(words,n)
    return dict(status='PASS_EXACT_TWO_D_HESSIAN_COMPILER_385560',date='2026-11-22',
      exact_cyclotomic_enumeration=exact,
      benchmark_results=results,
      theorem='The set H D H D H = H D N D N has exactly 385560 distinct complex 4x4 matrices; raw 648*27^2=472392 candidate words contain 86832 duplicates. Each entry lies in (1/243)Z[omega].',
      scope='Exact cardinality of the specified two-D word family and exhaustive three-target numerical optimization within it, NOT global finite-depth optimality nor experimentally efficient photonic compilation.',
      prior_work='Previous report certified H=D subgroup double coset |HDH|=17496 and H=H27 semidirect SL(2,3), which this computation builds upon.')

def main():
    out=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],out['exact_cyclotomic_enumeration'])
    print([z['two_D_best_projective_Frobenius'] for z in out['benchmark_results']])
if __name__=='__main__':main()
