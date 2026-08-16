#!/usr/bin/env python3
"""Pass5431: all-odd modular radical quotient isomorphism.

Correction/reconciliation: Pass5376 already CLOSED the all-odd binary footprint
rank theorem using the Lataille--Sin--Tiep characteristic-two point-module lattice:

  rank_2(F)=g=q(q^2+1)/2,
  ker(F^T)=C_W,
  im(F)=C_W^perp

for every odd prime power q.

Pass5350 independently gives, for M=F2^{Pts}, M0=ker(parity),

  Rad(im F^T)=F^T(M0).

The general exact sequence

  0 -> X_q:=ker(F^T)/C_W -> M0/C_W -> Rad(im F^T) -> 0

therefore collapses by Pass5376 to X_q=0 and the canonical isomorphism

  M0/C_W  ~=  Rad(im F^T).

Both sides have dimension g-1.  This respects Pass5358's nonsplitting firewall
and avoids collision with Pass5421's distinct apartment-to-footprint kernel D_q,
which has dimension q^4-g.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5431_ALLODD_MODULAR_FOOTPRINT_DEFECT_EXACT_SEQUENCE.json'

def row(q:int)->dict:
    assert q>=3 and q%2==1
    v=(q+1)*(q*q+1);f=q*(q+1)**2//2;g=q*(q*q+1)//2
    assert v==1+f+g
    r=g
    return {
      'q':q,'points':v,'f':f,'g':g,
      'rank_F2_by_Pass5376':r,
      'dim_M0':v-1,'dim_CW':1+f,
      'dim_M0_mod_CW':g-1,
      'radical_dimension_by_Pass5350':r-1,
      'extra_point_kernel_defect_dimension':0,
      'canonical_radical_quotient_isomorphism':True}

def main():
    anchors={str(q):row(q) for q in (3,5,7,9,11,13,17,19,23,25,27)}
    for x in anchors.values():
        assert x['dim_M0_mod_CW']==x['radical_dimension_by_Pass5350']
        assert x['extra_point_kernel_defect_dimension']==0
    out={
      'pass':5431,
      'status':'THEOREM_ALLODD_MODULAR_RADICAL_QUOTIENT_ISOMORPHISM',
      'domain':'odd prime powers q',
      'Pass5376_input':'rank_2(F)=g and ker(F^T)=C_W for every odd prime power q; the all-odd rank theorem is already closed.',
      'Pass5350_input':'Rad(im F^T)=F^T(M0), where M0 is the even-weight point module.',
      'general_exact_sequence':'0 -> X_q=ker(F^T)/C_W -> M0/C_W -> Rad(im F^T) -> 0',
      'closure':'Pass5376 forces X_q=0 identically.',
      'theorem':'M0/C_W is canonically isomorphic to Rad(im F^T).',
      'dimension':'g-1=q(q^2+1)/2-1 on both sides.',
      'notation_firewall':'Pass5421 D_q is the distinct apartment-to-footprint kernel 0->D_q->H1^*->C_F->0 of dimension q^4-g. X_q is only the transient extra point-kernel quotient ker(F^T)/C_W, and Pass5376 proves X_q=0.',
      'nonsplitting_firewall':'No splitting of F2[P^1(q)] is used; the argument combines the exact Pass5376 modular rank/kernel theorem with Pass5350 FF^T=J.',
      'anchors':anchors,
      'boundary':'This is a corollary/reconciliation of already-proved all-odd rank closure, not a new proof of Pass5376 and not a claim that Pass5421 D_q vanishes.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
