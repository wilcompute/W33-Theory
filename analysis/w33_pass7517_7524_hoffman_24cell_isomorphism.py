#!/usr/bin/env python3
"""Pass7517-7524: direct isomorphism Hoffman-cover stabilizer ~= W(D4):C3.

This upgrades Pass5300 from matching extension data to a generator-level group
isomorphism.  The 24-cell rotation group is built explicitly on the 24 D4 roots;
the actual q=5 Hoffman stabilizer is reconstructed by Pass5300.  A two-generator
word map is checked over all 576 elements.
"""
from __future__ import annotations
import itertools,json,math
from collections import deque,Counter
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass5300_hoffman576_latin_group_bridge import q5_hoffman
OUT=ROOT/'data/PART_W33_PASS7517_7524_HOFFMAN_24CELL_ISOMORPHISM.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
    z=[0]*len(p)
    for i,x in enumerate(p):z[x]=i
    return tuple(z)
def order(p):
    seen=[False]*len(p);o=1
    for i in range(len(p)):
        if seen[i]:continue
        j=i;c=0
        while not seen[j]:seen[j]=True;c+=1;j=p[j]
        if c:o=math.lcm(o,c)
    return o
def powp(p,k):
    if k<0:return powp(inv(p),-k)
    z=tuple(range(len(p)));a=p
    while k:
        if k&1:z=comp(a,z)
        a=comp(a,a);k//=2
    return z
def comm(a,b):return comp(comp(comp(inv(a),inv(b)),a),b)
def sig(a,b):
    bi=inv(b);ab=comp(a,b)
    words=[ab,comp(a,bi),comp(a,comp(b,b)),comp(comp(comp(a,b),a),b),comm(a,b),comp(comp(comp(a,b),a),bi),comp(a,powp(b,3)),comp(comp(comp(comp(a,b),a),b),b),comp(powp(ab,2),b)]
    return (order(a),order(b))+tuple(order(x) for x in words)
def closure(gens,n):
    gg=tuple(gens)+tuple(inv(g) for g in gens);I=tuple(range(n));S={I};dq=deque([I])
    while dq:
        u=dq.popleft()
        for g in gg:
            v=comp(g,u)
            if v not in S:S.add(v);dq.append(v)
    return S
def bfs_iso(a,b,x,y):
    gg=(a,b,inv(a),inv(b));hh=(x,y,inv(x),inv(y));eG=tuple(range(len(a)));eH=tuple(range(len(x)));mp={eG:eH};dq=deque([eG])
    while dq:
        u=dq.popleft();hu=mp[u]
        for g,h in zip(gg,hh):
            v=comp(g,u);hv=comp(h,hu)
            if v in mp:
                if mp[v]!=hv:return None
            else:mp[v]=hv;dq.append(v)
    return mp if len(mp)==576 and len(set(mp.values()))==576 else None

def d4_rotation_group():
    roots=[]
    for i,j in itertools.combinations(range(4),2):
        for a in (-1,1):
            for b in (-1,1):
                v=[0]*4;v[i]=a;v[j]=b;roots.append(tuple(v))
    roots=sorted(set(roots));ri={r:i for i,r in enumerate(roots)};assert len(roots)==24
    mats=[]
    # W(D4): coordinate permutations and even sign flips.
    for p in itertools.permutations(range(4)):
        for signs in itertools.product((-1,1),repeat=4):
            if np.prod(signs)!=1:continue
            M=np.zeros((4,4),dtype=int)
            for i in range(4):M[i,p[i]]=signs[i]
            mats.append(M)
    def perm(M):
        out=[]
        for r in roots:
            y=np.asarray(r)@M.T;out.append(ri[tuple(int(x) for x in y)])
        return tuple(out)
    W={perm(M) for M in mats};assert len(W)==192
    H=np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[-1,1,1,-1]],dtype=int)/2
    tau=perm(H);assert order(tau)==3
    G=PermutationGroup([Permutation(w) for w in list(W)[:8]]+[Permutation(tau)])
    # ensure the selected matrix/permutation set really generates all W(D4):C3
    if G.order()!=576:G=PermutationGroup([Permutation(w) for w in W]+[Permutation(tau)])
    assert G.order()==576
    els=[tuple(g(i) for i in range(24)) for g in G.generate_schreier_sims()]
    # deterministic 2-generator search
    invs=[g for g in els if order(g)==2];sixes=[g for g in els if order(g)==6]
    for a in invs:
        for b in sixes:
            if len(closure((a,b),24))==576:return roots,G,a,b
    raise AssertionError('no 2-generator pair')

def main():
    roots,G,a,b=d4_rotation_group();target=sig(a,b);assert len(closure((a,b),24))==576
    H,_,_,_=q5_hoffman();assert H.order()==576
    hels=[tuple(g(i) for i in range(325)) for g in H.generate_schreier_sims()]
    invs=[g for g in hels if order(g)==2];sixes=[g for g in hels if order(g)==6];witness=None;candidates=0
    for x in invs:
        for y in sixes:
            if sig(x,y)!=target:continue
            candidates+=1;mp=bfs_iso(a,b,x,y)
            if mp is not None:witness=(x,y,mp);break
        if witness:break
    assert witness is not None;_,_,mp=witness
    hist=Counter(order(g) for g in hels);assert hist==Counter({6:272,12:96,4:84,3:80,2:43,1:1})
    out={'schema':'w33.pass7517_7524.hoffman_24cell_isomorphism.v1','status':'PASS','passes':'7517-7524',
      'groups':{'hoffman_cover_stabilizer_order':576,'D4_triality_rotation_order':576,'D4_full_triality_WF4_order':1152},
      '24cell_group':'W(D4):C3','hoffman_Pass5300_structure':'2_+^{1+4}:(S3 x C3)',
      'element_order_census':{str(k):v for k,v in sorted(hist.items())},'two_generator_signature':list(target),
      'matching_H_generator_pairs_tested_before_witness':candidates,'word_map_elements_verified':len(mp),'word_map_bijective':len(set(mp.values()))==576,
      'theorem':'The actual PSp4(5) Hoffman-cover stabilizer reconstructed by Pass5300 is abstractly isomorphic to the orientation-preserving 24-cell group W(D4):C3. The isomorphism is verified on all 576 elements by a common two-generator word map.',
      'latin_boundary':'Pass5300 still stands: this group is not the full order-576 Klein Latin autoparatopy group; its central quotient is the even Latin affine subgroup.',
      'claim_boundary':'Finite group theorem. Equal order alone was not used.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','word_map':576,'signature':target}))
if __name__=='__main__':main()
