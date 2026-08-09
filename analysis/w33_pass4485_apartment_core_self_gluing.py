#!/usr/bin/env python3
"""Pass 4485 -- the apartment radical reuses the Pass-176 irreducible 8-core.

Let M=F_2^40 be the W33 line permutation module and A*=N^T N mod 2.  Put
K=ker A*, I=im A*, R=ker N, U=R cap I, J=<1>.  Pass 4481 gives

    dim(J,U,I,K,M) = (1,9,10,30,40).

Pass 176 already owns the protected fixed-line reduction onto the route-hull
8-space U/J, including its plus-type quadratic structure.  The new statement
here is apartment-side: because A*^2=0 and A* induces M/K ~= I, the same owned
U/J that is the middle factor of protected H10=1|8|1 also sits inside the
29-dimensional apartment radical K/J.

Thus the *same quotient space U/J*, not merely another 8-dimensional module,
appears on both sides of the new apartment extension:

    radical side:    U/J  <  K/J,
    protected side:  M/K --Abar~--> I, whose middle factor is U/J.

The verifier checks the diagram and action matrices.  The protected U/J bridge
itself remains Pass-176 ownership; Pass 4485 adds its occurrence inside the
apartment radical.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_pass158_chiral_trade_lattice_two_480s import build_group, build_w33, w33_lines
from w33_pass161_gq42_ihara_inheritance import small_generating_set
from w33_pass187_f2_layer_sandwich import subquotient_action_matrices, exhaustive_cyclic_irreducible
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2, rref_rows
from w33_pass4481_apartment_radical_module_filtration import inter, contains

ROOT=Path(__file__).resolve().parents[1]
def rank2(M): return len(rref_rows(np.asarray(M,dtype=np.uint8)))
def same(A,B):
    A=rref_rows(A);B=rref_rows(B)
    return len(A)==len(B) and contains(A,B) and contains(B,A)
def main():
    points,A,symp=build_w33(); lines=w33_lines(A); N=np.zeros((40,40),dtype=np.uint8)
    for li,L in enumerate(lines): N[list(L),li]=1
    Ast=(N.T@N)%2; J=np.ones((1,40),dtype=np.uint8)
    K=rref_rows(nullspace_mod2(Ast)); I=rref_rows(Ast); R=rref_rows(nullspace_mod2(N)); U=inter(R,I)
    checks={
      'dims_1_9_10_30_40':(len(J),len(U),len(I),len(K),40)==(1,9,10,30,40),
      'Astar_square_zero':not np.any((Ast@Ast)%2),'I_in_K':contains(K,I),'J_in_U':contains(U,J),'U_in_I':contains(I,U),'U_in_K':contains(K,U),
      'Abar_kernel_K':same(rref_rows(nullspace_mod2(Ast)),K),'Abar_image_I':same(rref_rows(Ast),I),'protected_dim10':40-len(K)==10,
      'middle_same_literal_UmodJ':len(U)-len(J)==8,'radical_dim29':len(K)-len(J)==29}
    _,group=build_group(points,symp); pg=small_generating_set(group); idx={frozenset(L):i for i,L in enumerate(lines)}
    lg=[tuple(idx[frozenset(g[p] for p in L)] for L in lines) for g in pg]
    a8,d8=subquotient_action_matrices(U,J,lg); ir8,orbits=exhaustive_cyclic_irreducible(a8,d8)
    atop,dt=subquotient_action_matrices(I,U,lg)
    checks.update({'UmodJ_dim8_irreducible':d8==8 and ir8,'IoverU_trivial1':dt==1 and all(int(x[0,0])==1 for x in atop)})
    for gi,g in enumerate(lg):
        P=np.zeros((40,40),dtype=np.uint8)
        for i,j in enumerate(g): P[j,i]=1
        checks[f'Astar_equivariant_gen{gi}']=np.array_equal((P@Ast)%2,(Ast@P)%2)
    assert all(checks.values()),checks
    out={'pass':4485,'theorem':'W33 apartment-radical reuse of the Pass-176 eight-core theorem',
      'diagram':{'apartment_code':'M/J (39)','radical':'K/J (29)','protected':'M/K (10)','incidence_isomorphism':'Abar: M/K -> I=im(A*)','protected_filtration':'J < U < I gives 1|8|1','repeated_core':'the Pass-176 U/J (8) protected core also occurs as an apartment-radical submodule'},
      'core':{'dimension':8,'irreducible':True,'vector_orbits':orbits,'literal_space':'U/J'},
      'prior_owner':'Pass 176 owns the protected f^perp/<f> -> route-hull U/J quadratic isometry; Pass 4485 adds its occurrence inside the apartment radical.',
      'boundary':'Exact apartment-side self-gluing only. Pass 176 already owns the protected route-hull U/J quadratic eight-core. No semisimple splitting, hardware duplication, E8 dynamics, or four-qubit machine is inferred.',
      'checks':{'passed':sum(checks.values()),'total':len(checks)}}
    p=ROOT/'data/PART_W33_PASS4485_APARTMENT_CORE_SELF_GLUING.json'; p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())