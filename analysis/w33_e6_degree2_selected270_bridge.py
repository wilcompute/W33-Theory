#!/usr/bin/env python3
"""Canonical bridge: W33 selected 270 lines <-> degree-2 W(E6) involutions.

Rebuilds the Pass-4659 selected 135_6-270_3 geometry and its intrinsic 36
minimum-code supports.  The 27x36 E6 incidence matrix R makes the 36 supports
into the double-six carrier.  Two double-sixes are called syzygetic when their
27-line supports meet in four lines; there are 270 such pairs.

For every selected 3-point line L, exactly 12 of the 36 code supports meet L
in two points.  For every syzygetic pair {D1,D2}, exactly 12 double-sixes are
nonadjacent to both D1 and D2 in the syzygetic SRG(36,15,6,6).  These 270
12-subsets coincide bijectively.  Hence the selected 270-set is canonically,
PSp(4,3)-equivariantly the 270 syzygetic pairs, equivalently the degree-2
involution class of W(E6).
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,nullspace2
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
from w33_pass4595_concrete_d4_triality_w33_lifts import max_generators
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_e6_degree2_selected270_bridge.json'

def main(write=True):
    _,_,_,_,_,Astar,_,apartments,_=build_geometry(); Astar=np.asarray(Astar,dtype=np.uint8)
    j=(1<<40)-1; cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]): m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i,k in itertools.combinations(range(40),2) if Astar[i,k]])
    V=set(span(B9)); rep=lambda x:min(int(x),int(x)^j); q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in {rep(v) for v in V} if x and q(x)==0); assert len(singular)==135
    def ap_fiber(ap):
        x=0
        for i in ap:x^=cols[i]
        return rep(x)
    def ap_line(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]; assert len(opp)==2
        s=rep(cols[opp[0][0]]^cols[opp[0][1]]); t=rep(cols[opp[1][0]]^cols[opp[1][1]])
        return tuple(sorted((s,t,ap_fiber(ap))))
    selected=sorted({ap_line(a) for a in apartments}); assert len(selected)==270
    sidx={x:i for i,x in enumerate(singular)}; N=np.zeros((135,270),dtype=np.uint8)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    B=nullspace2(N.T); assert len(B)==16
    bm=[]
    for b in B:
        m=0
        for i,z in enumerate(b):
            if int(z):m|=1<<i
        bm.append(m)
    words=[0]
    for b in bm:words += [x^b for x in words]
    minimum=sorted(w for w in words if w.bit_count()==30); assert len(minimum)==36
    supports=[{singular[i] for i in range(135) if (w>>i)&1} for w in minimum]
    MG=max_generators(singular,rep,q,polar)
    O27=sorted([X for X in MG if sum(set(L).issubset(X) for L in selected)==10],key=lambda X:tuple(sorted(X))); assert len(O27)==27
    R=np.zeros((27,36),dtype=np.uint8)
    for i,X in enumerate(O27):
        S=set(X)-{0}
        for a,U in enumerate(supports):
            z=len(S&U); assert z in (0,6)
            if z==0:R[i,a]=1
    pair_census=Counter(); syz=np.zeros((36,36),dtype=np.uint8); syz_pairs=[]
    for a,b in itertools.combinations(range(36),2):
        z=int(np.dot(R[:,a],R[:,b])); pair_census[z]+=1
        if z==4:syz[a,b]=syz[b,a]=1; syz_pairs.append((a,b))
    assert pair_census==Counter({6:360,4:270}) and set(map(int,syz.sum(1)))=={15}
    line_sig=[]
    for L in selected:
        H=frozenset(a for a,U in enumerate(supports) if len(set(L)&U)==2)
        assert len(H)==12; line_sig.append(H)
    pair_sig=[]
    for a,b in syz_pairs:
        H=frozenset(c for c in range(36) if c not in (a,b) and not syz[a,c] and not syz[b,c])
        assert len(H)==12; pair_sig.append(H)
    assert len(set(line_sig))==270 and len(set(pair_sig))==270 and set(line_sig)==set(pair_sig)
    out={
      'schema':'w33.e6_degree2_selected270_bridge.v1','status':'PASS',
      'headline':'The selected 270 lines of the intrinsic 135_6-270_3 geometry are canonically the 270 syzygetic double-six pairs, hence the degree-2 involution carrier of W(E6).',
      'selected_geometry':{'points':135,'lines':270,'line_size':3,'line_stabilizer_order_prior':96},
      'double_six_carrier':{'count':36,'syzygetic_graph':'SRG(36,15,6,6)','pair_intersection_census_on_27_lines':{'4':270,'6':360}},
      'canonical_signature':{'selected_line':'12 double-sixes meeting the selected line in two singular points','syzygetic_pair':'12 double-sixes nonadjacent to both endpoints','distinct_selected_signatures':270,'distinct_pair_signatures':270,'signature_sets_equal':True},
      'consequence':'PSp-equivariant bijection selected270 <-> syzygetic-pair270 <-> W(E6) degree-2 involutions; stabilizer order 25920/270=96.',
      'boundary':'Exact finite G-set theorem. No physical involution or gauge field is inferred.'}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out
if __name__=='__main__':main(True)
