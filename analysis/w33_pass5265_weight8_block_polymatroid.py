#!/usr/bin/env python3
"""Pass5265 (outside-box): the weight-8 dual support carries an exact K0 block polymatroid.

Pass5262 proves d_block(K0)=25 by showing that on one weight-8 footprint-dual
support D the K0 projection rank is unchanged when any one of the eight blocks
is deleted.  Here we compute the entire rank profile on all subsets of D.

The induced P-block graph on D is K8 minus the perfect matching
  (119,188),(124,317),(183,209),(302,318).
For subset sizes >=3 the K0 projection rank is controlled by the number m of
complete opposite pairs in the subset.  The exact profile is frozen below.
The triple split is especially clean: the 32 triangles of K8-4K2 have rank71,
while the 24 triples containing an opposite pair have rank72.  Thus the local
rank defect already reconstructs the dual-support matching geometry without
being told the graph.

This is a block-polymatroid theorem, not a new binary-code distance claim beyond
Pass5262.  It gives a compact local object to generalize when searching for an
all-odd-q block-distance proof.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment,atoms,atom_L_syndromes

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5265_WEIGHT8_BLOCK_POLYMATROID.json'
D=(119,124,183,188,209,302,317,318)
MATCH={(119,188),(124,317),(183,209),(302,318)}
MATCH={tuple(sorted(e)) for e in MATCH}

def rank_ints(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def indep(rows):
    piv={};ans=[]
    for i,x in enumerate(rows):
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;ans.append(i);break
    return ans

def null_deps(cols):
    piv={};deps=[]
    for i,x in enumerate(cols):
        c=1<<i
        while x:
            p=x.bit_length()-1
            if p in piv:y,d=piv[p];x^=y;c^=d
            else:piv[p]=(x,c);break
        if not x:deps.append(c)
    return deps,len(piv)

def main():
    G=build_W(5);acid,nc=p_component_assignment(G);AA,meta,_=atoms(G,acid);syn,_=atom_L_syndromes(G,AA)
    byc=defaultdict(list)
    for u,m in enumerate(meta):byc[m[3]].append(u)
    cols=[]
    for c in range(325):
        U=byc[c]; rows=[]
        for u in U:
            z=0
            for a in AA[u]:z|=1<<a
            rows.append(z)
        I=indep(rows);assert len(I)==25
        B=[U[i] for i in I];a=B[0]
        cols.extend(syn[u]^syn[a] for u in B[1:])
    deps,r=null_deps(cols);assert r==7240 and len(deps)==560
    def pr(S):
        mask=0
        for c in S:mask|=((1<<24)-1)<<(24*c)
        return rank_ints([x&mask for x in deps])
    prof=defaultdict(Counter);raw={}
    for k in range(1,9):
        C=Counter()
        for S in itertools.combinations(D,k):
            m=sum(tuple(sorted(e)) in MATCH for e in itertools.combinations(S,2))
            C[(m,pr(S))]+=1
        prof[k]=C;raw[str(k)]={f'm{m}_r{r}':n for (m,r),n in sorted(C.items())}
    want={
      '1':{'m0_r24':8},
      '2':{'m0_r48':24,'m1_r48':4},
      '3':{'m0_r71':32,'m1_r72':24},
      '4':{'m0_r91':16,'m1_r94':48,'m2_r95':6},
      '5':{'m1_r111':32,'m2_r114':24},
      '6':{'m2_r126':24,'m3_r129':4},
      '7':{'m3_r134':8},
      '8':{'m4_r134':1}}
    assert raw==want
    out={'pass':5265,'status':'THEOREM_Q5_WEIGHT8_K0_BLOCK_POLYMATROID',
      'seed_support':list(D),'opposite_matching':[list(x) for x in sorted(MATCH)],
      'subset_projection_rank_profile':raw,
      'reconstruction':'At k=3, rank71 occurs exactly on the 32 triangles of K8 minus 4K2; rank72 occurs exactly on the 24 triples containing one opposite pair.',
      'connection':'The no-singleton rank equality r(D)=r(D\\{j})=134 used in Pass5262 is the top layer of this local polymatroid.',
      'boundary':'Exact q5 local rank theorem; no all-q polymatroid formula is asserted.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
