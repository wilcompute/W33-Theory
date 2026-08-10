#!/usr/bin/env python3
"""Pass 4601 -- lift Pass4571's factor proof into one explicit S186 composition series.

Pass4571 closed the Jordan-Hoelder multiset of S186 but did not freeze an ordered
series. This pass reruns the same deterministic submodule witnesses and records
the preimage dimensions. The resulting exact composition series is
  0 < 14 < 54 < 60 < 74 < 80 < 120 < 126 < 134 < 140 < 146 < 186
with simple factors
  14,40,6,14,6,40,6,8,6,6,40.
Every factor's simplicity is already independently certified by Pass4571's
exhaustive 6/8/14 spins or full-degree irreducible 40D group-algebra witness.

This is an extension skeleton, not the complete unlabeled Loewy/submodule lattice:
alternative incomparable submodules and all Ext classes are not enumerated here.
"""
from __future__ import annotations
import json
from pathlib import Path
import w33_pass4571_dual_middle_module_composition as p4571
import w33_pass4544_dual_middle_module_lattice as p4544
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4601_S186_COMPOSITION_SERIES_SKELETON.json'

def main():
    S186g,Q64=p4571.locate_frontier();assert len(S186g[0])==186
    # visible S120
    B120=next(p4544.cyclic(1<<i,S186g) for i in range(186) if len(p4544.cyclic(1<<i,S186g))==120)
    S120=list(p4544.canonical(B120,186));S120g,_=p4544.restrict_to_subspace(S186g,S120,186);Q66,_=p4544.quotient_gens(S186g,S120,186)
    # S120 branch: 14 | (40 | 6 | 14) | 6 | 40 in deterministic witness order.
    A14=p4571.dual_annihilator_proper(S120g,120);assert A14 and A14[0]==14
    Q106,_=p4544.quotient_gens(S120g,A14[1],120)
    h106=p4571.hidden_proper(Q106,106,457101,{60});assert h106;S60=list(h106[1])
    S60g,_=p4544.restrict_to_subspace(Q106,S60,106);Q46u,_=p4544.quotient_gens(Q106,S60,106)
    h60=p4571.hidden_proper(S60g,60,457102,{40});assert h60;S40=list(h60[1])
    Q20,_=p4544.quotient_gens(S60g,S40,60);a6v=p4571.dual_annihilator_proper(Q20,20);assert a6v and a6v[0]==6
    Q14,_=p4544.quotient_gens(Q20,a6v[1],20);assert p4571.terminal_simple(Q14,14,0)
    a6u=p4571.dual_annihilator_proper(Q46u,46);assert a6u and a6u[0]==6
    Q40u,_=p4544.quotient_gens(Q46u,a6u[1],46);assert p4571.terminal_simple(Q40u,40,457112)
    # Q66 branch: 6 | 8 | 6 | 6 | 40.
    a6=p4571.dual_annihilator_proper(Q66,66);assert a6 and a6[0]==6;Q60,_=p4544.quotient_gens(Q66,a6[1],66)
    h8=p4571.hidden_proper(Q60,60,457103,{8});assert h8;B8=list(h8[1]);Q52,_=p4544.quotient_gens(Q60,B8,60)
    a6b=p4571.dual_annihilator_proper(Q52,52);assert a6b and a6b[0]==6;Q46,_=p4544.quotient_gens(Q52,a6b[1],52)
    a6c=p4571.dual_annihilator_proper(Q46,46);assert a6c and a6c[0]==6;Q40,_=p4544.quotient_gens(Q46,a6c[1],46)
    assert p4571.terminal_simple(Q40,40,457113)
    dims=[0,14,54,60,74,80,120,126,134,140,146,186]
    fac=[b-a for a,b in zip(dims,dims[1:])];assert fac==[14,40,6,14,6,40,6,8,6,6,40]
    old=json.loads((ROOT/'data/PART_W33_PASS4571_DUAL_MIDDLE_MODULE_COMPOSITION.json').read_text())
    assert old['S186']['composition_factors']=={'40':3,'14':2,'8':1,'6':5}
    out={'pass':4601,'module':'S186','composition_series_dimensions':dims,'ordered_simple_factor_dimensions':fac,'factor_multiset':{'40':3,'14':2,'8':1,'6':5},'status':'EXPLICIT_COMPOSITION_SERIES_CLOSED','remaining_loewy_frontier':'classify all incomparable submodules, radical/socle layers and extension classes; this pass does not claim the complete unlabeled submodule lattice','boundary':'Exact deterministic composition series, not a claim that the displayed chain is the unique composition series.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
