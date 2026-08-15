#!/usr/bin/env python3
"""Pass5446: notation-safe all-odd footprint double-quotient ladder.

Three prior results must be kept distinct.

Pass5376 (point side): for odd prime powers q,
    ker(F^T)=C_W, rank(F)=g, im(F)=C_F=C_W^perp.
Hence F^T induces an isomorphism
    M/C_W ~= im(F^T),
where M is the point permutation module.  Pass5350 says
    Rad(im F^T)=F^T(M0),
so restriction gives
    M0/C_W ~= Rad(im F^T),
and the quotient by this radical is one-dimensional.

Pass5421/5377 (apartment side): the apartment code C_A ~= H1(Levi)^* maps
surjectively onto C_F with nonzero kernel D_ap=K0 of dimension q^4-g:
    0 -> D_ap=K0 -> H1^* -> C_F -> 0.

Thus Pass5376 kills the EXTRA POINT KERNEL, not the APARTMENT KERNEL.  The two
stages have dimensions
    point transpose: 0 -> (g-1) -> g -> 1 -> 0,
    apartment:       0 -> (q^4-g) -> q^4 -> g -> 0.
This pass freezes that ladder and the notation firewall.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5446_ALLODD_FOOTPRINT_DOUBLE_QUOTIENT_LADDER.json'
ANCHORS=(3,5,7,9,11,13,17,19,23)

def row(q:int)->dict:
    assert q>=3 and q%2==1
    v=(q+1)*(q*q+1);f=q*(q+1)**2//2;g=q*(q*q+1)//2;r=q**4
    cw=1+f
    assert v-cw==g
    return {
      'q':q,'point_module_dim':v,'CW_dim':cw,'CF_dim':g,
      'transpose_image_dim':g,'transpose_radical_dim':g-1,'transpose_nonsingular_quotient_dim':1,
      'H1_dim':r,'apartment_kernel_Dap_K0_dim':r-g}

def main():
    rows={str(q):row(q) for q in ANCHORS}
    q3=rows['3'];assert q3['CF_dim']==15 and q3['apartment_kernel_Dap_K0_dim']==66
    q5=rows['5'];assert q5['CF_dim']==65 and q5['apartment_kernel_Dap_K0_dim']==560
    out={
      'pass':5446,'status':'THEOREM_ALLODD_FOOTPRINT_DOUBLE_QUOTIENT_LADDER',
      'domain':'odd prime powers q',
      'point_side':{
        'Pass5376':'ker(F^T)=C_W and rank(F)=g',
        'isomorphism':'F^T induces M/C_W ~= im(F^T)',
        'Pass5350_radical':'M0/C_W ~= Rad(im F^T)',
        'rank_one_extension':'0 -> M0/C_W -> im(F^T) -> <1> -> 0',
        'dimensions':'0 -> (g-1) -> g -> 1 -> 0'},
      'apartment_side':{
        'Pass5421_5377':'0 -> D_ap=K0 -> H1(Levi)^* -> C_F -> 0',
        'dimensions':'0 -> (q^4-g) -> q^4 -> g -> 0'},
      'firewall':'Pass5376 makes the extra point-kernel quotient ker(F^T)/C_W zero. It does NOT make the apartment kernel D_ap=K0 zero; D_ap has dimension q^4-g.',
      'anchors':rows,
      'boundary':'This is an exact-sequence reconciliation. It does not assert a canonical isomorphism between C_F and Rad(im F^T), which live in different permutation modules and have dimensions g and g-1.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
