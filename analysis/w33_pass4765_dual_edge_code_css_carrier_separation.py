#!/usr/bin/env python3
"""Pass 4765 -- the new [240,200,4] code lives on the dual line-edge carrier, not the point-edge CSS carrier.

Both W33 point collinearity and its line-intersection dual have 240 graph edges,
but q=3 is not self-dual.  We test the stronger representation question directly.
Under the canonical PSp(4,3) action, the stabilizer of one line-graph edge has no
fixed point-graph edge at all.  Hence there is no equivariant coordinate bijection
between the two 240-sets.  Twisting the point action by the PGSp outer involution
does not repair this.

Thus Pass4761's even-cycle code is an exact dual-GQ graph code and must not be
silently identified with the existing W33 point-edge CSS/Hodge carrier.  The two
240 counts are a controlled non-identification.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,perm_group,transvection_matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4765_DUAL_EDGE_CODE_CSS_CARRIER_SEPARATION.json'

def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def inv(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def rank2(M):
    piv={}
    for row in np.asarray(M,dtype=np.uint8):
        x=0
        for j,b in enumerate(row):
            if int(b)&1:x|=1<<j
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def main()->int:
    pts,pidx,lines,lidx,_,Aline,_,apartments,_=build_geometry();Aline=np.asarray(Aline,dtype=np.uint8)
    # Point graph from the line incidence; line graph is Aline.
    Apoint=np.zeros((40,40),dtype=np.uint8)
    through=[set() for _ in range(40)]
    for li,L in enumerate(lines):
        for p in L:through[p].add(li)
    for p,q in itertools.combinations(range(40),2):
        if through[p]&through[q]:Apoint[p,q]=Apoint[q,p]=1
    assert set(map(int,Apoint.sum(axis=1)))==set(map(int,Aline.sum(axis=1)))=={12}
    assert (rank2(Apoint),rank2(Aline))==(16,10)
    pedges=[(i,j) for i,j in itertools.combinations(range(40),2) if Apoint[i,j]]
    ledges=[(i,j) for i,j in itertools.combinations(range(40),2) if Aline[i,j]]
    assert len(pedges)==len(ledges)==240

    cand=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[];PSp={tuple(range(40))}
    for p in cand:
        trial=perm_group(gens+[p])
        if len(trial)>len(PSp):gens.append(p);PSp=trial
        if len(PSp)==25920:break
    assert len(PSp)==25920
    outer=build_line_perm(np.diag([1,2,1,2])%3,pts,pidx,lines,lidx);outi=inv(outer)

    # Recover the point action from the action on the four-line stars.
    stars=[frozenset(through[p]) for p in range(40)];sidx={S:i for i,S in enumerate(stars)}
    def pp(g):return tuple(sidx[frozenset(g[l] for l in stars[p])] for p in range(40))
    def ae(e,g):return tuple(sorted((g[e[0]],g[e[1]])))
    def ape(e,g):
        h=pp(g);return tuple(sorted((h[e[0]],h[e[1]])))
    e0=ledges[0];St=[g for g in PSp if ae(e0,g)==e0];assert len(St)==108

    def orbit_sizes(items,action,group):
        unseen=set(items);out=[]
        while unseen:
            x=min(unseen);O={action(x,g) for g in group};out.append(len(O));unseen-=O
        return sorted(out)
    own=orbit_sizes(ledges,ae,St);other=orbit_sizes(pedges,ape,St)
    assert own==[1,1,2,2,18,18,18,18,27,27,54,54]
    assert other==[6,6,6,6,54,54,54,54]
    assert not any(all(ape(e,g)==e for g in St) for e in pedges)

    Tw=[compose(compose(outer,g),outi) for g in St]
    twisted=orbit_sizes(pedges,ape,Tw);assert twisted==[6,6,6,6,54,54,54,54]
    assert not any(all(ape(e,g)==e for g in Tw) for e in pedges)

    out={'pass':4765,'carriers':{'point_graph_edges':240,'dual_line_graph_edges':240,'point_adjacency_rank_F2':16,'dual_line_adjacency_rank_F2':10},
      'line_edge_stabilizer':{'order':108,'suborbits_on_line_edges':own,'suborbits_on_point_edges':other,'fixed_point_edges':0},
      'outer_twist':{'point_edge_suborbits':twisted,'fixed_point_edges':0,'repairs_equivariant_bijection':False},
      'code_boundary':{'Pass4761':'[240,200,4]_2 even-cycle code on dual line graph','existing_edge_CSS_Hodge':'240 point-collinearity edges','canonical_PSp_coordinate_identification':False},
      'theorem':'The two 240-edge carriers are inequivalent under the canonical PSp action: a line-edge stabilizer fixes no point edge, and the PGSp outer twist does not change that obstruction. Pass4761 is therefore a dual-line graph code, not the point-edge CSS code in disguise.',
      'boundary':'Exact G-set separation. Abstract code equivalences that ignore the canonical group action are not classified here.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
