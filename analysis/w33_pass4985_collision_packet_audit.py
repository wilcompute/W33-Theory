#!/usr/bin/env python3
"""Pass4985: exact audit of the collided/corrected Pass4968-4972 packet."""
from __future__ import annotations
import json,cmath
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4985_COLLISION_PACKET_AUDIT.json'
def main():
 # Ihara roots follow from the frozen W33 spectrum 12,2^24,-4^15 and k-1=11.
 r2=((1+1j*(10**0.5))/11,(1-1j*(10**0.5))/11)
 rm4=((-2+1j*(7**0.5))/11,(-2-1j*(7**0.5))/11)
 assert all(abs(abs(z)-1/(11**0.5))<1e-12 for z in r2+rm4)
 # Frozen Pass88 exact critical group structure.
 order=(10**8)*40*(160**14)
 assert order==(2**81)*(5**23)
 out={
  'pass':4985,
  'audited_commit':'f9db42c7fe192690b824a307df7fe27abadbd483',
  'survives':[
   'W(3,3)=srg(40,12,2,4)','spectrum 12^1,2^24,(-4)^15','PSp(4,3) connected collineation subgroup has order25920','Ramanujan bound holds','Pass4971 retraction of the srg(33) Fano-deletion story'],
  'corrections':{
   'Pass4968':'PSp(4,3) is the connected/index-two subgroup used by the symplectic action, not the full 51840 similitude extension. The 27 nonneighbors of a fixed W33 point are points of the same 40-point carrier; the asserted identification with 27 PG(3,3) lines not through a point is withdrawn.',
   'Pass4969':'A graph automorphism commutes with adjacency, hence preserves the distinct 24- and 15-dimensional eigenspaces; it cannot interchange them. The finite PGSp/PSp outer sign is not, by itself, physical CPT.',
   'Pass4970':'Roots of 1-2u+11u^2 are (1+-i sqrt(10))/11, and roots of 1+4u+11u^2 are (-2+-i sqrt(7))/11. The previous sqrt(43),sqrt(107) fields and class-number interpretation are withdrawn.',
   'Pass4972':'The spanning-tree/critical-group order 2^81*5^23 survives, but the exact frozen critical group is (Z/10)^8 + Z/40 + (Z/160)^14. The ad-hoc invariant-factor/hypercharge-denominator paragraph is withdrawn.'},
  'ihara_nontrivial_root_fields':['Q(i sqrt(10))','Q(i sqrt(7))'],
  'critical_group':{'structure':'(Z/10)^8 (+) Z/40 (+) (Z/160)^14','order_factored':'2^81*5^23'},
  'boundary':'The equality v2(|Krit|)=81 is exact arithmetic. Interpreting it as a physical encoding of the bulk logical dimension requires an independent mechanism and is not promoted here.',
  'theorem':'The corrected 4968-4972 packet repaired the 33-vertex error but retained three independent mistakes: eigenspace interchange/CPT, Ihara discriminants, and critical-group invariant factors. Pass4985 supersedes those claims while preserving the valid 40-vertex spectrum and Ramanujan statements.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
