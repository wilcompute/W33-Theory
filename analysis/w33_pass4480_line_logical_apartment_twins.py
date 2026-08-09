#!/usr/bin/env python3
"""Pass 4480 -- line-logical / apartment-generator twin theorem.

Renumbering note: this result was first pushed under Pass 4474, but the earlier
reservation d300fa184fa5665fd539f39b2d6ab4b23c08a39d owns 4472--4479.  The
current canonical number is 4480.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles
from w33_pass4469_apartment_css_h10_intertwiner import complement_to, in_span, nullspace_mod2, rref_rows
from w33_pass4470_apartment_h10_quadratic_fixed_layer import q_half_weight, solve_mod2

ROOT=Path(__file__).resolve().parents[1]

def rank2(M):
    from w33_pass4463_apartment_parity_tomography import rank_mod2
    return rank_mod2(np.asarray(M,dtype=np.uint8))

def keymod(v,C):
    r=np.asarray(v,dtype=np.uint8).copy()
    for b in rref_rows(C):
        p=int(np.flatnonzero(b)[0])
        if r[p]: r^=b
    return tuple(map(int,r))

def main():
    _,lines,A,N0,edge_line=geometry(); N=(N0%2).astype(np.uint8); Ast=(N.T@N)%2
    aps=[frozenset(edge_line[e] for e in c) for c in simple_four_cycles(A)]
    H=np.zeros((40,len(aps)),dtype=np.uint8)
    for j,S in enumerate(aps): H[list(S),j]=1
    C=rref_rows(nullspace_mod2(N.T)); K=nullspace_mod2(Ast); Q=complement_to(K,40)
    xb=np.asarray([(N@b)%2 for b in Q],dtype=np.uint8); gb=np.asarray([(H.T@b)%2 for b in Q],dtype=np.uint8)
    G=(Q@Ast@Q.T)%2
    defect=np.asarray([q_half_weight(gb[i])^q_half_weight(xb[i]) for i in range(10)],dtype=np.uint8)
    fc=solve_mod2(G,defect); f=(fc@xb)%2
    g=H.copy(); x=N.T.copy(); shifted=x^f
    checks={
      'forty_lines':len(lines)==40,
      'apartment_weight_162':all(int(v.sum())==162 for v in g),
      'logical_weight_4':all(int(v.sum())==4 for v in x),
      'forty_distinct_H10_classes':len({keymod(v,C) for v in x})==40,
      'line_classes_span_H10':rank2(np.vstack((C,x)))==25,
      'same_W33_polar_gram':np.array_equal((g@g.T)%2,Ast) and np.array_equal((x@x.T)%2,Ast),
      'apartment_lines_q1':all(q_half_weight(v)==1 for v in g),
      'logical_lines_q0':all(q_half_weight(v)==0 for v in x),
      'fixed_f_isotropic':q_half_weight(f)==0,
      'fixed_f_pairs_one_with_all_lines':bool(np.all((x@f)%2==1)),
      'shifted_q1':all(q_half_weight(v)==1 for v in shifted),
      'shifted_same_W33_gram':np.array_equal((shifted@shifted.T)%2,Ast),
      'raw_shifted_disjoint':{keymod(v,C) for v in x}.isdisjoint({keymod(v,C) for v in shifted}),
    }
    universal=[]
    for m in range(1<<10):
        c=np.array([(m>>i)&1 for i in range(10)],dtype=np.uint8); v=(c@xb)%2
        if np.all((x@v)%2==1): universal.append(m)
    checks['fixed_f_unique_universal_pairing_class']=len(universal)==1 and universal[0]==sum(int(b)<<i for i,b in enumerate(fc))
    assert all(checks.values()),checks
    out={
      'pass':4480,'theorem':'W33 line-logical / apartment-generator singular-anisotropic twin theorem',
      'single_line':{'apartment_weight':162,'logical_weight':4,'classes':40,'pairing_graph':'dual W33'},
      'quadratic_twin':{'raw_logical_q':0,'apartment_q':1,'shifted_q':1,'fixed_class_unique':True,'raw_shifted_disjoint':True},
      'owners':{'minimum_logical_lines':'Pass 201','fixed_H10_layer':'Pass 187','bridge':'Pass 4469','quadratic_defect':'Pass 4470'},
      'boundary':'Finite O+(10,2) label-space statement only; not a second physical code, particle doubling, or implemented gate.',
      'checks':{'passed':sum(checks.values()),'total':len(checks)} }
    p=ROOT/'data/PART_W33_PASS4480_LINE_LOGICAL_APARTMENT_TWINS.json'; p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
