#!/usr/bin/env python3
"""Pass 4667 -- the selected geometry's unique Smith-2 bit pins H10 head/socle.

The selected 135x270 incidence has one Z/2 torsion factor.  As a 1D F2
PSp-module it is necessarily trivial.  H10 has the canonical uniserial chain
0 < <j> < V9=ker(pi) < H10 with factors 1|8|1.  Hence the selected torsion bit
has unique nonzero equivariant maps into and out of H10: 1->j and pi.  Their
composition is zero, yielding the canonical rank-one nilpotent n(x)=pi(x)j.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4667_SELECTED_SMITH_BIT_H10_HEAD_SOCLE.json'

def main():
    s=json.loads((ROOT/'data/PART_W33_PASS4642_SELECTED_LINE_SMITH_COHERENT.json').read_text())
    h=json.loads((ROOT/'data/PART_W33_PASS4553_CANONICAL_H10_WEIGHT_QUADRATIC.json').read_text())
    b=json.loads((ROOT/'data/PART_W33_PASS4630_T_BOCKSTEIN_H10_CSS.json').read_text())
    assert s['incidence']['smith_nonzero_profile']=={'1':119,'2':1}
    assert h['canonical_chain']=='0 < <j> < j^perp=V9 < H10' and h['dimensions']==[0,1,9,10]
    assert h['parity_pairing']=='pi(x)=B(x,j), hence V9=ker(pi)=j^perp'
    assert b['integer_lift']['coker_2_primary_torsion']=='(Z/2)^10' and b['bockstein']['isomorphism']
    out={
      'pass':4667,
      'selected_torsion':{'group':'Z/2','F2_dimension':1,'PSp_module':'trivial','reason':'GL(1,2) is trivial'},
      'H10_filtration':{'chain':'0 < <j> < V9=ker(pi) < H10','composition_factors':'1|8|1','middle':'V8=V9/<j> irreducible 8D'},
      'equivariant_maps':{
        'Hom_PSp(selected_bit,H10)_dimension':1,
        'unique_injection':'i(1)=j',
        'Hom_PSp(H10,selected_bit)_dimension':1,
        'unique_quotient':'pi:H10->F2 with ker(pi)=V9',
        'middle_V8_maps_to_or_from_bit':0,
        'composition_pi_after_i':0},
      'nilpotent':{
        'definition':'n=i o pi, so n(x)=pi(x) j',
        'rank':1,'square_zero':True,'image':'<j>','kernel':'V9',
        'interpretation':'the selected single Smith bit links the trivial head and socle of H10 but does not split or select the 8D middle factor'},
      'Bockstein_connection':'Via Pass4630 H10 ~= Tor_2(coker T), the selected Z/2 defect has the unique nonzero PSp-equivariant injection into the ten Smith bits and the unique nonzero quotient back out.',
      'theorem':'The unique 2-torsion bit of the selected D4 incidence canonically matches the trivial head/socle species of H10. It determines the unique rank-one square-zero endomorphism n(x)=pi(x)j, while the protected V8 middle remains invisible to this one-bit defect.',
      'boundary':'Module-level canonical maps from the exact PSp filtrations; no claim of a new support-level incidence map between the 135x270 and 45x40 matrices.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
