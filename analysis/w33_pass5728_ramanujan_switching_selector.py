#!/usr/bin/env python3
"""Pass5728: quotient matching signings by complement switching and test invariant rho selector."""
from __future__ import annotations
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass5683_balanced_ramanujan_levi_lifts as p5683
import w33_pass5693_explicit_ramanujan_levels23 as p5693
import w33_pass5706_ramanujan_levels45_and_color_gauge as p5706
OUT=ROOT/'data/PART_W33_PASS5728_RAMANUJAN_SWITCHING_INVARIANT_SELECTOR.json'

def main():
 E0=p5683.levi();E=p5693.lift_edges(E0,80,set(p5683.NEG));n=160;levels=[]
 for _ in range(4):
  best,rows=p5706.best(E,n)
  vals=sorted(float(r) for r,_a,_b,_neg in rows)
  assert len(vals)==6
  classes=[]
  for i in range(0,6,2):
   assert abs(vals[i]-vals[i+1])<1e-7
   classes.append((vals[i]+vals[i+1])/2)
  assert classes[0]+1e-7<classes[1] and classes[1]+1e-7<classes[2]
  levels.append({'parent_vertices':n,'switching_class_signed_radii':classes,'unique_minimum':classes[0],
                 'gap_to_second':classes[1]-classes[0],'min_is_ramanujan':classes[0]<2*math.sqrt(3)})
  E=p5693.lift_edges(E,n,best[3]);n*=2
 out={'pass':5728,'status':'SPECTRAL_RADIUS_IS_LABEL_INDEPENDENT_UNIQUE_SELECTOR_ON_EACH_KNOWN_THREE_CLASS_CANDIDATE_SET__ALL_LEVEL_CANONICITY_STILL_OPEN',
  'quotient':'six 2-of-4 matching labels -> three complement-switching classes',
  'intrinsic_invariant':'rho(A_sigma), invariant under vertex switching and graph automorphism',
  'known_levels':levels,
  'result':'At parents 160,320,640,1280 the three quotient-class radii are strictly ordered. Thus argmin rho is unique and independent of the 01/02/03 class names, removing the raw color gauge for the one-step choice.',
  'remaining_recursion_obstruction':'The three candidates themselves come from a deterministic perfect-matching factorization of a labeled parent. No theorem yet proves that this candidate triple is canonical under the full parent automorphism group or that global minimization over intrinsic balanced switching classes lands in it. This is an invariant one-step selector, not an infinite recursion theorem.',
  'physics_boundary':'Internal expander-cover spectrum only; no spacetime/RG claim.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
