#!/usr/bin/env python3
"""Pass 4519 -- the corrected splitting flag is the Sylow-3 normalizer/Borel.

Pass 4503 shows every maximal subgroup type of PSp(4,3) retains the apartment
extension obstruction, while a canonical incident point-line flag stabilizer H
of order 162 splits it.  The shared order with the standard Sylow-3 normalizer
is not used as an identification: this pass proves equality inside the exact
25920-element permutation action.

For the canonical flag stabilizer H:

  * |H| = 162;
  * its unique Sylow-3 subgroup P has order 81 (index two in H);
  * N_G(P) computed in the full PSp(4,3) action has order 162;
  * N_G(P) = H as explicit permutation sets.

Thus the verified splitting gauge is the chamber/Borel subgroup, equivalently
the full normalizer of a Sylow-3 subgroup in this action.  Together with Pass
4509, restriction to this Borel kills the complete two-dimensional radical H1
obstruction.
"""
from __future__ import annotations

import json
from math import gcd
from pathlib import Path
import numpy as np

from w33_apartment_section_core import (
    build_geometry, build_line_perm, compose, line_perm_from_point_perm,
    perm_group, point_perm_from_matrix, small_generating_set,
    transvection_matrix,
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4519_FLAG_BOREL_SYLOW3_NORMALIZER.json'


def inverse_perm(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)


def perm_order(p):
    seen=[False]*len(p);order=1
    for i in range(len(p)):
        if seen[i]:continue
        j=i;n=0
        while not seen[j]:
            seen[j]=True;j=p[j];n+=1
        if n:
            order=order*n//gcd(order,n)
    return order


def conjugate(g,h):
    return compose(compose(g,h),inverse_perm(g))


def main()->int:
    pts,pidx,lines,lidx,*_=build_geometry()
    matrices=[transvection_matrix(v) for v in pts]
    point_trans=[point_perm_from_matrix(M,pts,pidx) for M in matrices]
    line_trans=[build_line_perm(M,pts,pidx,lines,lidx) for M in matrices]

    selected=[];full_line={tuple(range(40))}
    for i,p in enumerate(line_trans):
        trial=perm_group([line_trans[j] for j in selected]+[p],40)
        if len(trial)>len(full_line):selected.append(i);full_line=trial
        if len(full_line)==25920:break
    assert len(full_line)==25920
    full_point=perm_group([point_trans[i] for i in selected],40)
    assert len(full_point)==25920

    fp,fl=min((p,li) for li,L in enumerate(lines) for p in L)
    flag_point={
        g for g in full_point
        if g[fp]==fp and line_perm_from_point_perm(g,lines,lidx)[fl]==fl
    }
    H={line_perm_from_point_perm(g,lines,lidx) for g in flag_point}
    assert len(H)==162

    # Since a Sylow-3 subgroup has index 2 in H, it is unique/normal.  In a
    # quotient H/P ~= C2 every element outside P has even order, so P is exactly
    # the odd-order elements of H.
    orders={g:perm_order(g) for g in H}
    P={g for g,o in orders.items() if o%2==1}
    assert len(P)==81
    assert perm_group(small_generating_set(P,40),40)==P
    pgens=small_generating_set(P,40)

    normalizer=set()
    for g in full_line:
        if all(conjugate(g,p) in P for p in pgens):
            normalizer.add(g)
    assert len(normalizer)==162
    assert normalizer==H

    p_order_hist={}
    for g in P:
        o=perm_order(g);p_order_hist[o]=p_order_hist.get(o,0)+1
    h_order_hist={}
    for g in H:
        o=perm_order(g);h_order_hist[o]=h_order_hist.get(o,0)+1

    c4509=json.loads((ROOT/'data/PART_W33_PASS4509_COHOMOLOGY_RESTRICTION_BARCODE.json').read_text())
    flag_barcode=c4509['barcode']['incident_flag_162']
    assert flag_barcode['restriction_kernel_dimension']==2
    assert len(flag_barcode['killed_nonzero_classes'])==3

    out={
      'pass':4519,
      'theorem':'the canonical incident-flag splitting subgroup is exactly the Sylow-3 normalizer/Borel of PSp(4,3)',
      'group_order':25920,
      'flag':{'point':fp,'line':fl,'order':len(H),'index':25920//len(H)},
      'sylow3':{'order':len(P),'index_in_flag':len(H)//len(P),'generators_used':len(pgens),'element_order_histogram':{str(k):v for k,v in sorted(p_order_hist.items())}},
      'normalizer':{'order':len(normalizer),'equals_flag_stabilizer':normalizer==H,'element_order_histogram':{str(k):v for k,v in sorted(h_order_hist.items())}},
      'cohomology_restriction':{'radical_H1_dimension':2,'restriction_kernel_dimension':flag_barcode['restriction_kernel_dimension'],'all_three_nonzero_classes_killed':len(flag_barcode['killed_nonzero_classes'])==3},
      'structural_reading':'The corrected symmetry-breaking threshold is a chamber/Borel gauge: fixing an incident point-line flag selects the Sylow-3 normalizer and annihilates both radical obstruction bits.',
      'boundary':'This is an exact finite-group/building identification. Borel/chamber locality is not by itself a physical gauge field, spacetime locality, or hardware subgroup implementation.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
