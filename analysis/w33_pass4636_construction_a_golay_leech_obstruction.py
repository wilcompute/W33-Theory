#!/usr/bin/env python3
"""Pass 4636 -- exact Construction-A gluing of the paired-axis Golay section.

For a binary code C <= F2^24 define
  L(C)=(1/sqrt(2)){x in Z^24 : x mod 2 in C}.
The paired-axis section C6 is the six-generator [18,6,8] code zero-padded to 24
coordinates; the full code is the extended binary Golay G24.

The determinant formula is det L(C)=2^(24-2 dim C).  Hence det L(C6)=2^12,
while det L(G24)=1 and [L(G24):L(C6)]=|G24/C6|=64.  Both codes have no weight-4
word, so the only norm-2 vectors in either Construction-A lattice are the 48
coordinate roots +/-sqrt(2)e_i.  Thus the 64-coset glue reaches the rooted
A1^24 Niemeier lattice, not the rootless Leech lattice.  Reaching Leech requires
an additional neighbor/shift (holy-construction) step not supplied by C6.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import w33_pass4592_paired_axes_simplex_hexacode_golay as p4592
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4636_CONSTRUCTION_A_GOLAY_LEECH_OBSTRUCTION.json'

def rank_bits(rows,n=24):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)
def main()->int:
    G=p4592.golay24();basis=[G[1<<i] for i in range(12)];C6=p4592.enum_code(basis[:6]);Gset=set(G)
    assert len(C6)==64 and len(Gset)==4096 and C6<=Gset
    assert rank_bits(basis[:6])==6 and rank_bits(basis)==12
    W6=Counter(x.bit_count() for x in C6);WG=Counter(x.bit_count() for x in Gset)
    assert W6==Counter({8:45,12:18,0:1})
    assert WG==Counter({12:2576,8:759,16:759,0:1,24:1})
    assert all(w%4==0 for w in W6) and all(w%4==0 for w in WG)
    det6=2**(24-2*6);detG=2**(24-2*12);index=2**(12-6)
    assert (det6,detG,index)==(4096,1,64) and det6==index**2*detG
    # norm 2 means x.x=4 before scaling.  Besides +/-2e_i, the only possibility
    # is four odd coordinates, which would require a weight-4 codeword.
    roots6=48 if W6.get(4,0)==0 else None;rootsG=48 if WG.get(4,0)==0 else None
    assert roots6==rootsG==48
    out={'pass':4636,'codes':{'C6':{'dimension':6,'weight_enumerator':dict(W6)},'G24':{'dimension':12,'weight_enumerator':dict(WG)},'quotient_G24_over_C6':64},'construction_A':{'definition':'(1/sqrt(2)){x in Z^24: x mod 2 in C}','det_L_C6':det6,'det_L_G24':detG,'index_LG24_over_LC6':index,'norm2_roots_LC6':roots6,'norm2_roots_LG24':rootsG},'theorem':'The paired-axis C6 lattice is an index-64 sublattice of the full Golay Construction-A lattice. Adding all 64 G24/C6 glue cosets makes the lattice unimodular but preserves 48 A1 coordinate roots, so the endpoint is the A1^24 Niemeier lattice rather than Leech.','Leech_obstruction':'Leech is rootless (minimum norm 4); these Construction-A lattices contain 48 norm-2 roots. A further neighbor/shift/holy-construction step is required.','boundary':'Exact code/glue/determinant/root obstruction. No direct C6-to-Leech isometry is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
