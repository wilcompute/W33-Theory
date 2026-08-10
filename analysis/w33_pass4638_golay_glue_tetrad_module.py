#!/usr/bin/env python3
"""Pass 4638 -- the 64 Construction-A glue cosets form the six-tetrad permutation module.

For the paired-axis section C6 <= G24, the quotient G24/C6 has dimension six and
64 elements.  Under the Pass4633 section stabilizer K (order 2160), its induced
linear image has order 720 and kernel order 3.  The same K acts on the six sextet
tetrads through S6 with the same kernel.

Exact intertwiner equations between the quotient module and the binary six-point
permutation module have dimension two.  Among the three nonzero homomorphisms,
two have rank six (isomorphisms) and their sum has rank one.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass4592_paired_axes_simplex_hexacode_golay as p4592
import w33_pass4632_periodic_homology_module_separation as lin
import w33_pass4633_m24_sextet_section_stabilizer as p4633
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4638_GOLAY_GLUE_TETRAD_MODULE.json'

def quotient_action(g,basis,sol):
    cols=[]
    for b in basis[6:]:
        c=sol(p4633.act_word(b,g));assert c is not None;cols.append(c>>6)
    return lin.cols_to_np(cols,6)
def tetrad_action(g,tetrads):
    idx={T:i for i,T in enumerate(tetrads)};cols=[]
    for T in tetrads:cols.append(1<<idx[p4633.act_set(T,g)])
    return lin.cols_to_np(cols,6)
def mkey(M):return bytes(np.asarray(M,dtype=np.uint8).ravel())
def main()->int:
    d=p4633.build();K=d['K'];Kgens=d['Kgens'];G=p4592.golay24();basis=[G[1<<i] for i in range(12)];sol=lin.solver(basis,24)
    assert len(p4592.enum_code(basis[:6]))==64
    Q=[quotient_action(g,basis,sol) for g in Kgens];tetrads=[frozenset(x) for x in d['sextet']];T=[tetrad_action(g,tetrads) for g in Kgens]
    qorder=len({mkey(quotient_action(g,basis,sol)) for g in K});torder=len({mkey(tetrad_action(g,tetrads)) for g in K})
    assert qorder==torder==720 and len(K)//qorder==3
    H=lin.hom_space(Q,T);assert len(H)==2
    maps=[]
    for mask in range(1,1<<len(H)):
        M=np.zeros_like(H[0])
        for i,X in enumerate(H):
            if (mask>>i)&1:M^=X
        maps.append(lin.rank2(M))
    assert sorted(maps)==[1,6,6]
    out={'pass':4638,'section_group_order':len(K),'glue_quotient':{'code_quotient':'G24/C6','dimension':6,'elements':64,'induced_group_order':qorder,'kernel_order':3},'tetrad_module':{'dimension':6,'induced_group_order':torder,'image':'S6','kernel_order':3},'intertwiner_space':{'dimension':2,'ranks_of_three_nonzero_maps':sorted(maps),'full_rank_isomorphisms':2},'theorem':'The six-dimensional Golay glue quotient G24/C6 is K-equivariantly isomorphic to the binary permutation module on the six sextet tetrads. Thus the 64 Construction-A glue cosets carry the sextet tetrad permutation geometry.','boundary':'The isomorphism is for the section stabilizer K. It is not an M24-equivariant splitting of G24, and the two full-rank intertwiners show a residual one-bit ambiguity rather than a unique coordinate identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
