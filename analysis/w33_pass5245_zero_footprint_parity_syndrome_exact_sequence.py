#!/usr/bin/env python3
"""Pass5245: exact parity/syndrome sequence for the q=5 zero-footprint residual.

Let V_P be the direct sum of the 325 q=5 P-component tensor codes.  Each
component has dimension25, hence dim V_P=8125.  Component parity is one nonzero
linear functional per coordinate-disjoint component, so

  pi: V_P -> F2^325

is onto and its even-block kernel E has dimension 325*24=7800.

Let L be the connected-L compatibility map.  Pass5220 gives rank(L|V_P)=7500
and ker L = apartment code C_A of dimension625.  Pass5201 identifies the
component-parity image of C_A with the footprint code C_F, now [325,65,25] by
Pass5238.  Therefore the zero-footprint apartment residual

  K0 = C_A cap E

has dimension625-65=560.  Rank-nullity on E gives rank(L|E)=7800-560=7240.
Thus the quotient of the full L-syndrome image by the even-block L image has
dimension 7500-7240=260, and the induced map F2^325 -> that quotient has kernel
exactly C_F.  Hence there is a canonical exact sequence

  0 -> C_F -> F2^325 -> Im(L|V_P)/Im(L|E) -> 0.

Equivalently the dual of the quotient is C_F^perp, explaining why the 260
sparse footprint checks are exactly the parity information missing from the
even-block connected-L image.

Pass5244 proves every strict q=5 apartment word below625 lies in K0 and uses at
most15 nonzero P blocks.  Therefore the full q=5 d=625 theorem is now
_equivalent_, on the strict side, to the block-distance statement d_block(K0)>=16.
The equality side is already closed by Pass5238.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5245_ZERO_FOOTPRINT_PARITY_SYNDROME_EXACT_SEQUENCE.json'

def main():
    comps=325;local_dim=25;even_local=24
    VP=comps*local_dim;E=comps*even_local
    Lrank=7500;CA=625;CF=65;K0=CA-CF
    LE=E-K0;Q=Lrank-LE
    assert (VP,E,Lrank,CA,CF,K0,LE,Q)==(8125,7800,7500,625,65,560,7240,260)
    assert VP-Lrank==CA and E-LE==K0 and 325-CF==Q
    out={'pass':5245,'status':'THEOREM_Q5_ZERO_FOOTPRINT_PARITY_SYNDROME_EXACT_SEQUENCE',
      'P_side_space':{'blocks':325,'local_dimension':25,'dimension':VP},
      'even_block_space':{'local_dimension':24,'dimension':E},
      'connected_L_rank_full':Lrank,
      'apartment_code_dimension':CA,
      'footprint_code':'C_F=[325,65,25]_2','footprint_dimension':CF,
      'zero_footprint_residual_dimension':K0,
      'connected_L_rank_on_even_block_space':LE,
      'syndrome_quotient_dimension':Q,
      'exact_sequence':'0 -> C_F -> F2^325 -> Im(L|V_P)/Im(L|E) -> 0',
      'dual_identification':'The dual of the 260-dimensional syndrome quotient is naturally C_F^perp, matching the 260 independent sparse footprint parity checks of Pass5231.',
      'strict_block_reduction':'Pass5244: every q5 apartment-code word of weight<625 belongs to K0 and has at most15 nonzero P blocks.',
      'new_closure_target':'Prove block-distance d_block(K0)>=16. This alone eliminates every strict sub625 word; Pass5238 has already classified the weight625 shell as chamber stars.',
      'boundary':'The block-distance-16 statement is a sharply isolated target, not proved in this pass. Thus the full q5 apartment-code distance theorem remains open on the strict side.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
