#!/usr/bin/env python3
"""Pass 4492 -- the 23D cocycle support extends the Pass-176 route hull by the Pass-201 sentinel code.

Pass 4491 identified the fixed-line extension-cocycle support as

    W/J,  W = K intersect R^perp,

of dimension 23, with profile 8|1|14.  Here R=ker N is the line route code,
R^perp=rowspace(N), K=ker(N^T N), and J=<1> on line coordinates.

This pass resolves the 23 structurally.  Let C=ker N^T be the point sentinel
code from Pass 201.  Then incidence N restricts to an exact sequence

    0 -> U -> W --N--> C -> 0,

where U=R intersect R^perp is precisely the Pass-176 route hull.  Exact ranks:

    dim U=9, dim W=24, dim C=15.

The image N(W) equals all of C, and ker(N|_W)=U.  Since J<=U, quotienting gives

    0 -> U/J (8) -> W/J (23) -> C (15) -> 0.

Pass 176 owns U/J and Pass 201 owns C=[40,15,8].  The point sentinel C contains
its fixed all-ones line and C/<1> is the irreducible 14-factor from Pass 187,
so the cocycle-support profile is literally

    8 | (1 | 14).

New content: W/J is the exact incidence extension welding these two older code
objects, and it is the support required by the nonsplitting fixed-line cocycle.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_pass158_chiral_trade_lattice_two_480s import build_group,build_w33,w33_lines
from w33_pass161_gq42_ihara_inheritance import small_generating_set
from w33_pass187_f2_layer_sandwich import subquotient_action_matrices,exhaustive_cyclic_irreducible
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2,rref_rows
from w33_pass4481_apartment_radical_module_filtration import inter,contains

ROOT=Path(__file__).resolve().parents[1]
def rank2(M):return len(rref_rows(np.asarray(M,dtype=np.uint8)))
def same(A,B):
    A=rref_rows(A);B=rref_rows(B)
    return len(A)==len(B) and contains(A,B) and contains(B,A)
def main():
    points,A,symp=build_w33();lines=w33_lines(A);N=np.zeros((40,40),dtype=np.uint8)
    for li,L in enumerate(lines):N[list(L),li]=1
    Ast=(N.T@N)%2;R=rref_rows(nullspace_mod2(N));Rp=rref_rows(N);K=rref_rows(nullspace_mod2(Ast));I=rref_rows(Ast)
    U_route=inter(R,Rp);U_alt=inter(R,I);W=inter(K,Rp);C=rref_rows(nullspace_mod2(N.T));Jline=np.ones((1,40),dtype=np.uint8);Jpoint=np.ones((1,40),dtype=np.uint8)
    imageW=rref_rows((N@W.T).T);kerW=inter(W,R)
    checks={'dims_U_W_C':(len(U_route),len(W),len(C))==(9,24,15),'U_route_equals_RcapI':same(U_route,U_alt),
      'image_NW_is_C':same(imageW,C),'kernel_N_on_W_is_U':same(kerW,U_route),'Jline_in_U':contains(U_route,Jline),
      'Jpoint_in_C':contains(C,Jpoint),'quotient_dims_8_23_15':(len(U_route)-1,len(W)-1,len(C))==(8,23,15)}
    # Verify the owned irreducible 14 quotient C/<j> with point action.
    _,group=build_group(points,symp);gens=small_generating_set(group)
    a14,d14=subquotient_action_matrices(C,Jpoint,gens);ir14,orbits14=exhaustive_cyclic_irreducible(a14,d14)
    checks['C_over_j_irreducible14']=d14==14 and ir14
    assert all(checks.values()),checks
    out={'pass':4492,'theorem':'W33 cocycle-support route-hull/sentinel extension theorem',
      'ambient_exact_sequence':'0 -> U(route hull,9) -> W=K intersect R^perp (24) --N--> C(sentinel,15) -> 0',
      'quotient_exact_sequence':'0 -> U/J (8) -> W/J (23) -> C (15) -> 0',
      'support_profile':'8 | (1 | 14)','map':'point-line incidence N','kernel':'U=R intersect R^perp = Pass-176 route hull','image':'C=ker N^T = Pass-201 [40,15,8] sentinel code',
      'owners':{'U/J':'Pass 176','sentinel_C':'Pass 201','C_over_fixed_line_14_factor':'Pass 187','W/J_as_cocycle_support':'Pass 4491'},
      'new_content':'The Pass-4491 23D obstruction support is the incidence extension welding the owned route-hull 8-core to the owned sentinel 15-code.',
      'C_over_j_vector_orbits':orbits14,
      'boundary':'Exact code/module extension only; no physical coupling, energy transfer, or error-channel interpretation is inferred.',
      'checks':{'passed':sum(checks.values()),'total':len(checks)}}
    p=ROOT/'data/PART_W33_PASS4492_COCYCLE_SUPPORT_ROUTE_SENTINEL_EXTENSION.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())