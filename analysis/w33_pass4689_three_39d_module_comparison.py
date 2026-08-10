#!/usr/bin/env python3
"""Pass 4689 -- compare the three dimension-39 carriers exactly over F2.

The cross-shell differential of Pass4639 is

    D0 = [[0,R],[R^T,0]],

so its homology splits canonically as H27 direct-sum H36.  This pass compares
that 39-dimensional periodic/cross-shell module with the 39-dimensional
apartment coefficient module.  The apartment incidence map has kernel exactly
<1>, so the apartment code is the point permutation quotient F2^40/<1>.

The result is a clean separation: the Hom space in each direction has dimension
2.  All three nonzero maps Hcross -> Cap have rank 14; all three nonzero maps
Cap -> Hcross have rank 1.  Hence the equal dimensions do not give an
isomorphism.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass4632_periodic_homology_module_separation as p

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4689_THREE_39D_MODULE_COMPARISON.json'

def direct_sum(A,B):
    M=np.zeros((A.shape[0]+B.shape[0],A.shape[1]+B.shape[1]),dtype=np.uint8)
    M[:A.shape[0],:A.shape[1]]=A;M[A.shape[0]:,A.shape[1]:]=B
    return M

def all_nonzero_ranks(H):
    if not H:return []
    out=[]
    for mask in range(1,1<<len(H)):
        M=np.zeros_like(H[0])
        for i,A in enumerate(H):
            if (mask>>i)&1:M^=A
        out.append(p.rank2(M))
    return sorted(out)

def build_periodic_actions(ggens):
    sing=[x for x in range(1,64) if not p.q(x)];anis=[x for x in range(1,64) if p.q(x)]
    si={x:i for i,x in enumerate(sing)};ai={x:i for i,x in enumerate(anis)}
    R=np.array([[p.B(s,a) for a in anis] for s in sing],dtype=np.uint8)
    sperms=[[si[p.mat_apply(g,x)] for x in sing] for g in ggens]
    aperms=[[ai[p.mat_apply(g,x)] for x in anis] for g in ggens]
    rowR=p.basis([sum(int(R[i,j])<<j for j in range(36) if R[i,j]) for i in range(27)],36)
    kerR=p.nullspace([sum(int(R[i,j])<<j for j in range(36) if R[i,j]) for i in range(27)],36)
    colR=p.basis([sum(int(R[i,j])<<i for i in range(27) if R[i,j]) for j in range(36)],27)
    kerRt=p.nullspace([sum(int(R[i,j])<<i for i in range(27) if R[i,j]) for j in range(36)],27)
    H36=p.subquotient_actions(kerR,rowR,aperms,36)
    H27=p.subquotient_actions(kerRt,colR,sperms,27)
    H39=[direct_sum(a,b) for a,b in zip(H27,H36)]
    return R,H27,H36,H39

def build_apartment_coefficient_module(fullgens,ggens):
    full=p.closure(fullgens);I=np.eye(6,dtype=np.uint8);Z=np.zeros((6,6),dtype=np.uint8)
    oriented=[M for M in full if np.array_equal((M@M+M+I)%2,Z)];assert len(oriented)==80
    pairs={tuple(sorted((p.mkey(J),p.mkey((J@J)%2)))) for J in oriented};pairs=sorted(pairs);assert len(pairs)==40
    pidx={P:i for i,P in enumerate(pairs)}
    def pairperm(g):
        gi=p.inv6(g);out=[]
        for a,b in pairs:
            J=np.frombuffer(a,dtype=np.uint8).reshape(6,6);K=p.mmul(p.mmul(g,J),gi);K2=(K@K)%2
            out.append(pidx[tuple(sorted((p.mkey(K),p.mkey(K2))))])
        return out
    perms=[pairperm(g) for g in ggens]
    one=(1<<40)-1;ambient=[one]
    for i in range(40):
        if p.rank(ambient+[1<<i],40)>len(ambient):ambient.append(1<<i)
    assert len(ambient)==40
    return p.quotient_actions(ambient,1,perms,40)

def main()->int:
    fullgens=p.small_full_generators();ggens=p.derived_generators(fullgens)
    assert len(p.closure(ggens))==25920
    R,H27,H36,Hcross=build_periodic_actions(ggens)
    assert Hcross[0].shape==(39,39)
    Cap=build_apartment_coefficient_module(fullgens,ggens);assert Cap[0].shape==(39,39)
    fwd=p.hom_space(Hcross,Cap);rev=p.hom_space(Cap,Hcross)
    rf=all_nonzero_ranks(fwd);rr=all_nonzero_ranks(rev)
    assert len(fwd)==len(rev)==2
    assert rf==[14,14,14] and rr==[1,1,1]
    out={
      'pass':4689,
      'group':'PSp(4,3)',
      'canonical_cross_shell_split':{
        'D0_block_form':'[[0,R],[R^T,0]]',
        'Hcross':'H27 direct-sum H36',
        'dimensions':[15,24,39],
        'status':'canonical shell decomposition, not a dimension inference'},
      'apartment_code_module':{
        'dimension':39,
        'coefficient_model':'F2^40/<all-ones>',
        'reason':'the 40 apartment incidence rows have rank 39 and their unique coefficient relation is the all-ones vector'},
      'equivariant_comparison':{
        'Hom_Hcross_to_Cap_dimension':len(fwd),
        'ranks_of_three_nonzero_maps_Hcross_to_Cap':rf,
        'Hom_Cap_to_Hcross_dimension':len(rev),
        'ranks_of_three_nonzero_maps_Cap_to_Hcross':rr},
      'theorem':'The 39D cross-shell homology is canonically H27 plus H36, but it is not isomorphic to the 39D apartment code.  The two-dimensional Hom spaces contain only rank-14 maps forward and rank-1 maps backward.',
      'boundary':'Exact F2 PSp(4,3)-module theorem.  The common dimension 39 is explicitly rejected as an apartment/periodic identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
