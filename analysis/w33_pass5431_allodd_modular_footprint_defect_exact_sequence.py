#!/usr/bin/env python3
"""Pass5431: characteristic-2 exact sequence for the all-odd footprint-rank defect.

This reduction deliberately respects Pass5358's nonsplitting firewall.
Let M=F2^{Pts(W(3,q))}, M0=ker(parity), F^T:M->F2^{P-components},
K=ker(F^T), and C_W the binary W-line code.  Pass5350 gives K<=M0 and
C_W<=K.  It also identifies Rad(im F^T)=F^T(M0).

Therefore restriction to M0 induces the exact sequence

  0 -> K/C_W -> M0/C_W -> Rad(im F^T) -> 0.

Writing r=rank_2(F), f=q(q+1)^2/2, g=q(q^2+1)/2 and
v=(q+1)(q^2+1)=1+f+g,

  dim(M0/C_W)=g-1,
  dim Rad(im F^T)=r-1,
  dim(K/C_W)=g-r.

Thus the entire all-odd theorem is equivalent to vanishing of one intrinsic
modular defect module D_q=K/C_W.  No characteristic-zero splitting is used.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5431_ALLODD_MODULAR_FOOTPRINT_DEFECT_EXACT_SEQUENCE.json'
ANCHOR_RANKS={3:15,5:65,7:175,9:369,11:671,13:1105}

def row(q:int,r:int|None=None)->dict:
    assert q%2==1
    v=(q+1)*(q*q+1);f=q*(q+1)**2//2;g=q*(q*q+1)//2
    assert v==1+f+g
    rec={'q':q,'points':v,'f':f,'g':g,'dim_M0':v-1,'dim_CW':1+f,'dim_M0_mod_CW':g-1}
    if r is not None:
        defect=g-r
        rec.update(rank_F2=r,radical_dimension=r-1,defect_dimension=defect)
        assert (g-1)-(r-1)==defect
    return rec

def main():
    anchors={str(q):row(q,r) for q,r in ANCHOR_RANKS.items()}
    assert all(x['defect_dimension']==0 for x in anchors.values())
    symbolic={str(q):row(q) for q in (15,17,19,21,23,25,27)}
    out={
      'pass':5431,'status':'THEOREM_ALLODD_MODULAR_FOOTPRINT_DEFECT_EXACT_SEQUENCE',
      'domain':'odd prime powers q; formulas themselves require only odd q where the cited W-line-code inclusion holds.',
      'exact_sequence':'0 -> D_q=ker(F^T)/C_W -> M0/C_W -> Rad(im F^T) -> 0',
      'definitions':{'M0':'even-weight point module','C_W':'binary W-line code','D_q':'intrinsic extra-kernel/defect module'},
      'dimensions':{'dim(M0/C_W)':'g-1','dim Rad(im F^T)':'rank_2(F)-1','dim D_q':'g-rank_2(F)'},
      'equivalence':'rank_2(F)=g iff D_q=0 iff ker(F^T)=C_W.',
      'nonsplitting_firewall':'The proof uses only kernels, quotients, and Pass5350 FF^T=J. It does not split F2[P^1(q)] or reduce the characteristic-zero Steinberg/pair decomposition modulo 2.',
      'verified_zero_defect_anchors':anchors,
      'symbolic_rows':symbolic,
      'boundary':'This concentrates the open all-odd rank theorem into vanishing of D_q; it does not prove D_q=0 for arbitrary odd q.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
