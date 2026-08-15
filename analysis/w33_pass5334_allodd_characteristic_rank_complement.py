#!/usr/bin/env python3
"""Pass5334: characteristic-zero/binary rank-complement law for footprint incidence.

Pass5267 gives, for odd q,

    F F^T = (q^2-1)I + (q-1)A_W + J,

with W(3,q) point multiplicities 1,f,g where
f=q(q+1)^2/2 and g=q(q^2+1)/2.  Hence over characteristic zero
rank(F)=1+f and nullity(point->carrier map)=g.  Pass5288/5293 give
rank_2(F)<=g and show that equality is equivalent to K0=D_q.

Therefore the all-odd binary-rank conjecture can be restated as an exact
rank-complement swap:

    rank_2(F) = nullity_Q(F) = g,
    nullity_2(F) = rank_Q(F) = 1+f.

The first equality is open in general but verified at q=3,5,7,9,11,13.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5334_ALLODD_CHARACTERISTIC_RANK_COMPLEMENT.json'

def row(q):
    v=(q+1)*(q*q+1);f=q*(q+1)**2//2;g=q*(q*q+1)//2
    assert v==1+f+g
    lam0=2*q*q*(q+1);lamr=2*q*(q-1);lams=0
    return {'q':q,'v':v,'f':f,'g':g,'rank_Q':1+f,'nullity_Q':g,
            'Gram_spectrum':{str(lam0):1,str(lamr):f,'0':g}}

def main():
    anchors={3:15,5:65,7:175,9:369,11:671,13:1105}
    rows={str(q):row(q) for q in (3,5,7,9,11,13)}
    for q,r in anchors.items():
        assert r==rows[str(q)]['g']
        assert rows[str(q)]['v']-r==rows[str(q)]['rank_Q']
    # q=5 explicit characteristic flip from the exact Gram law.
    q5=rows['5'];assert (q5['rank_Q'],q5['nullity_Q'],anchors[5],q5['v']-anchors[5])==(91,65,65,91)
    out={'pass':5334,'status':'THEOREM_ALLODD_CHARACTERISTIC_ZERO_RANK_COMPLEMENT_AND_BINARY_SWAP_TARGET',
      'all_odd_exact':'rank_Q(F)=1+f and nullity_Q(F)=g for f=q(q+1)^2/2, g=q(q^2+1)/2.',
      'binary_upper_bound':'rank_2(F)<=g.',
      'equivalent_binary_target':'rank_2(F)=g iff nullity_2(F)=1+f iff K0=D_q.',
      'rank_complement_form':'Conjecturally rank_2(F)=nullity_Q(F)=g and nullity_2(F)=rank_Q(F)=1+f.',
      'anchors_rank2_equals_g':{f'q{q}':r for q,r in anchors.items()},
      'q5_characteristic_flip':{'rank_Q':91,'nullity_Q':65,'rank_F2':65,'nullity_F2':91},
      'anchors':rows,
      'boundary':'The characteristic-zero rank/nullity formula is all odd q. The characteristic-2 swap is verified only at the displayed anchors; its all-odd statement is exactly the still-open K0=D_q generation theorem.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
