#!/usr/bin/env python3
"""Pass9281-9288: central-C3 holonomy on the Leech36 / local-W33 cover.

REHOMED from the superseded Pass9201-9208 label after discovering that another
lane reserved Pass9197-9260 three minutes earlier.

Dependencies:
- Pass8101-8108: one 36-object mixed-Lagrangian component is an
  H27:GL2(3) graph with 12 canonical three-sheet fibres over the affine
  lines of AG(2,3); the sheet kernel is central C3.
- Pass8481-8488: that exact 36-object cover is objectwise/fibrewise the
  36 W33 lines avoiding a fixed W33 point.

This pass orients the central C3, reads every inter-fibre perfect matching as
a ternary translation, and computes the gauge-invariant triangle holonomy.
Holonomy vanishes exactly on concurrent affine-line triples; nonconcurrent
triples carry one of the two nonzero ternary phases.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, defaultdict
from pathlib import Path
import networkx as nx
import numpy as np
from analysis.w33_pass8101_8108_leech_h27_gl23_lagrangian_controller import canon, lagrangians, proj
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9281_9288_LEECH36_HEISENBERG_HOLONOMY.json'

def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))
def affine_direction(T):
    pts=list(T);dirs=set()
    for a,b in itertools.combinations(pts,2):
        d=((a[0]-b[0])%3,(a[1]-b[1])%3)
        if d!=(0,0):dirs.add(canon(d))
    assert len(dirs)==1;return next(iter(dirs))

def main()->int:
    L=lagrangians();A=np.zeros((144,144),dtype=np.uint8)
    for i,j in itertools.combinations(range(144),2):
        if len(L[i]&L[j])==9:A[i,j]=A[j,i]=1
    comps=[sorted(c) for c in nx.connected_components(nx.from_numpy_array(A))]
    assert list(map(len,comps))==[36,36,36,36];C=comps[0];A36=A[np.ix_(C,C)];GX=nx.from_numpy_array(A36)
    fibres=defaultdict(list)
    for loc,g in enumerate(C):fibres[proj(L[g])].append(loc)
    lines=sorted(fibres,key=lambda S:tuple(sorted(S)));F=[frozenset(fibres[S]) for S in lines]
    assert len(F)==12 and set(map(len,F))=={3};fi={f:i for i,f in enumerate(F)}
    traces=[]
    for S in lines:
        T=frozenset((u[2],u[3]) for u in S if (u[0],u[1])!=(0,0));assert len(T)==3;traces.append(T)
    pts=sorted(set().union(*map(set,traces)));assert len(pts)==9
    dirs=[affine_direction(T) for T in traces]
    assert Counter(dirs)==Counter({(0,1):3,(1,0):3,(1,1):3,(1,2):3})
    assert Counter(len(traces[i]&traces[j]) for i,j in itertools.combinations(range(12),2))==Counter({1:54,0:12})
    autos=[tuple(m[i] for i in range(36)) for m in nx.algorithms.isomorphism.GraphMatcher(GX,GX).isomorphisms_iter()]
    assert len(autos)==1296
    base=[tuple(fi[frozenset(p[x] for x in f)] for f in F) for p in autos];e12=tuple(range(12));e36=tuple(range(36))
    ker=[p for p,b in zip(autos,base) if b==e12];assert len(ker)==3
    non=[p for p in ker if p!=e36];assert len(non)==2;k=non[0];k2=compose(k,k);assert compose(k2,k)==e36
    sheet={}
    for f in F:
        a=min(f);orb=[a,k[a],k2[a]];assert set(orb)==set(f)
        for z,v in enumerate(orb):sheet[v]=z
    pair_shift={}
    for i,j in itertools.combinations(range(12),2):
        if len(traces[i]&traces[j])==0:continue
        M=A36[np.ix_(sorted(F[i]),sorted(F[j]))];assert np.all(M.sum(0)==1) and np.all(M.sum(1)==1)
        shifts=set()
        for u in F[i]:
            vs=[v for v in F[j] if A36[u,v]];assert len(vs)==1;shifts.add((sheet[vs[0]]-sheet[u])%3)
        assert len(shifts)==1;pair_shift[(i,j)]=next(iter(shifts))
    assert len(pair_shift)==54
    def shift(i,j):return pair_shift[(i,j)] if i<j else (-pair_shift[(j,i)])%3
    hol=Counter();conc=Counter();bydir=defaultdict(Counter)
    for i,j,e in itertools.combinations(range(12),3):
        if len({dirs[i],dirs[j],dirs[e]})<3:continue
        h=(shift(i,j)+shift(j,e)+shift(e,i))%3;c=len(traces[i]&traces[j]&traces[e])==1
        hol[h]+=1;conc[(c,h)]+=1;bydir[tuple(sorted((dirs[i],dirs[j],dirs[e])))][h]+=1
    assert hol==Counter({0:36,1:36,2:36})
    assert conc==Counter({(True,0):36,(False,1):36,(False,2):36})
    assert all(v[0]==9 and sorted([v[1],v[2]])==[0,18] for v in bydir.values())
    out={'schema':'w33.pass9281_9288.leech36_heisenberg_holonomy.v1','status':'PASS','passes':'9281-9288',
      'base':{'geometry':'AG(2,3) affine-line system','points':9,'lines':12,'parallel_classes':4,'nonparallel_line_pairs':54,'three_direction_triangles':108},
      'cover':{'vertices':36,'sheets_per_line':3,'central_sheet_kernel':'C3','full_automorphism_order':1296,'inter_nonparallel_fibre_edges':'perfect matchings','matching_form':'z -> z + c_ij over F3 after orienting the central C3'},
      'holonomy':{'definition':'h(i,j,k)=c_ij+c_jk+c_ki mod 3','census':{'0':36,'+1':36,'-1':36},'concurrent':{'h=0':36},'nonconcurrent':{'h=+1':36,'h=-1':36},'theorem':'h=0 iff the three affine lines are concurrent','gauge_note':'Independent sheet-origin shifts c_ij -> c_ij+a_j-a_i cancel around triangles. Reversing the chosen generator of central C3 swaps +1 and -1 but preserves zero/nonzero.'},
      'theorem':'The central C3 in the Leech36 H27 cover is an explicit affine-concurrency cocycle: the three-sheet matching holonomy vanishes exactly on concurrent AG(2,3) line triples and is nonzero on every nonconcurrent triple. Via Pass8481 the same cocycle transports objectwise to the 36 W33 lines avoiding a fixed point.',
      'claim_boundary':'Exact finite combinatorial/group-extension theorem. Heisenberg refers to the certified H27 central extension; no physical phase dynamics is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','holonomy':{'0':36,'1':36,'2':36},'criterion':'zero iff concurrent'}));return 0
if __name__=='__main__':raise SystemExit(main())
