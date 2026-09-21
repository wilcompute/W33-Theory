#!/usr/bin/env python3
"""Objectwise realization of the 33, 48 and 32 sectors of the FI x parity Z6.

The E6 minuscule 27 is reconstructed as an exact Weyl orbit in Dynkin-label
coordinates.  Its Qpsi charges are 16_1 + 10_-2 + 1_4.  Its root-difference
graph is the Schlaefli graph SRG(27,16,10,8), and an anchored graph isomorphism
maps it to W33's independent cubic-line carrier.

Consequences:
  * each nonzero Z3 grade is 27 x 3, so the 16 odd frames give 48=16x3;
    the 10+1 even frames give 33=30+3;
  * the unique 1_4 weight differs from each of the 16_1 weights by an actual
    E6 root of Qpsi=-3.  These 16 roots and their negatives give the grade-zero
    matter-odd 32=16+16bar objectwise as (far frame, root orientation +/-).
"""
from __future__ import annotations
import importlib.util, json, sys
from collections import Counter, deque
from fractions import Fraction as F
from pathlib import Path
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_z6_objectwise_33_48_32_carrier.json"
A=((2,-1,0,0,0,0),(-1,2,-1,0,0,0),(0,-1,2,-1,-1,0),
   (0,0,-1,2,0,0),(0,0,-1,0,2,-1),(0,0,0,0,-1,2))
QPSI=(4,5,6,3,4,2)

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path); assert spec and spec.loader
    m=importlib.util.module_from_spec(spec); sys.modules[name]=m; spec.loader.exec_module(m); return m

def refl(mu,i):
    return tuple(mu[j]-mu[i]*A[j][i] for j in range(6))

def orbit(start):
    seen={start}; q=deque([start])
    while q:
        x=q.popleft()
        for i in range(6):
            y=refl(x,i)
            if y not in seen: seen.add(y); q.append(y)
    return sorted(seen)

def qpsi(w): return sum(QPSI[i]*w[i] for i in range(6))

def main(write=True):
    old=load(ROOT/"analysis/w33_pass7081_7096_e8_z3_z4_z12_common_refinement.py","inv_z6obj")
    common=load(ROOT/"analysis/w33_pass4992_4999_common.py","common_z6obj")
    W=orbit((1,0,0,0,0,0)); assert len(W)==27
    charges=[qpsi(w) for w in W]
    assert Counter(charges)==Counter({1:16,-2:10,4:1})
    sidx=charges.index(4); singlet=W[sidx]

    # Enumerate the 72 E6 roots in Dynkin-label coordinates from one simple root.
    simple0=tuple(A[i][0] for i in range(6))
    roots=set(orbit(simple0)); assert len(roots)==72

    WG=nx.Graph(); WG.add_nodes_from(range(27))
    for i in range(27):
        for j in range(i+1,27):
            d=tuple(W[i][k]-W[j][k] for k in range(6))
            if d in roots or tuple(-x for x in d) in roots: WG.add_edge(i,j)
    assert set(dict(WG.degree()).values())=={16} and WG.number_of_edges()==216

    base=common.build_base(); meet=base["G27"]; sch=nx.complement(meet)
    assert set(dict(sch.degree()).values())=={16}
    nx.set_node_attributes(WG,{i:(i==sidx) for i in WG},"anchor")
    nx.set_node_attributes(sch,{i:(i==0) for i in sch},"anchor")
    GM=nx.algorithms.isomorphism.GraphMatcher(WG,sch,node_match=lambda a,b:a["anchor"]==b["anchor"])
    iso=next(GM.isomorphisms_iter())
    assert iso[sidx]==0
    near=set(meet.neighbors(0)); far=set(range(27))-{0}-near
    assert len(near)==10 and len(far)==16
    assert {iso[i] for i,c in enumerate(charges) if c==-2}==near
    assert {iso[i] for i,c in enumerate(charges) if c==1}==far

    # The 16 odd grade-zero roots are literal differences from the 1_4 weight.
    odd_roots=[]
    for i,w in enumerate(W):
        if charges[i]!=1: continue
        d=tuple(w[k]-singlet[k] for k in range(6))
        assert d in roots
        odd_roots.append((i,d))
    assert len(odd_roots)==len({d for _,d in odd_roots})==16
    root32={(iso[i],sgn) for i,_ in odd_roots for sgn in (-1,1)}
    assert len(root32)==32

    triplet=(0,1,2)
    grade1_even={(iso[i],a) for i,c in enumerate(charges) if c%2==0 for a in triplet}
    grade1_odd ={(iso[i],a) for i,c in enumerate(charges) if c%2!=0 for a in triplet}
    assert len(grade1_even)==33 and len(grade1_odd)==48
    assert len({x for x in grade1_even if x[0]==0})==3
    assert len({x for x in grade1_even if x[0] in near})==30

    parent=json.loads((ROOT/"data/w33_physical_fi_matter_parity_z6_quotient.json").read_text())
    assert parent["Z6"]["dimensions"]==[54,48,33,32,33,48]

    out={
      "schema":"w33.z6_objectwise_33_48_32_carrier.v1",
      "status":"PASS_OBJECTWISE_Z6_33_48_32_CARRIER",
      "headline":"The FI x matter-parity Z6 sectors 48,33,32 now have explicit carriers. In each nonzero Z3 sector, the anchored 27-weight/27-cubic-line isomorphism gives 48=16 matter-odd far frames x 3 family weights and 33=(10 meeting frames + reference frame) x3 =30+3. In grade zero, each of the 16 odd minuscule weights differs from the unique 1_4 weight by a genuine E6 root; those roots and their negatives give 32=16+16bar as far-frame x root-orientation channels.",
      "weight_to_cubic_line":{str(i):iso[i] for i in range(27)},
      "reference_weight_index":sidx,
      "reference_cubic_line":0,
      "Qpsi_histogram":{"1":16,"-2":10,"4":1},
      "nonzero_Z3_sector":{
        "even_33":{"objects":33,"decomposition":"(10 x 3) + (1 x 3) = 30+3"},
        "odd_48":{"objects":48,"decomposition":"16 x 3"}},
      "grade_zero_odd_32":{
        "objects":32,"decomposition":"16_-3 + 16bar_+3",
        "predicate":"for each far frame/minuscule 16 weight w, w - w_(1_4) is an E6 root; include both root orientations"},
      "root_channels":[{"weight_index":i,"cubic_line":iso[i],"root_dynkin_labels":list(d),
                        "Qpsi_root":-3,"negative_Qpsi_root":3} for i,d in odd_roots],
      "boundary":"The graph isomorphism is an anchored coordinate gauge; different stabilizer choices relabel the 10 and 16 without changing the theorem. This does not assign observed generations or masses.",
      "checks":{"27_weight_graph_is_Schlaefli":True,"anchored_cubic_isomorphism":True,
                "48_is_16x3":True,"33_is_30plus3":True,"32_is_oriented_16_root_channels":True}}
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("status","nonzero_Z3_sector","grade_zero_odd_32")},indent=2))
    return out
if __name__=="__main__": main(True)
