#!/usr/bin/env python3
"""Pass8233-8240 (outside-box): W(11,3) contains one huge orbit of W33 slices.

Parallel Pass8030-8040 proves that the fixed-point-free order-3 Leech structure
carries W(11,3), while Co0 has no pure Phi_9^4 element giving W33 as the next
cyclotomic quotient.  This pass distinguishes 'no canonical quotient rung' from
'no subgeometry': every nondegenerate symplectic 4-subspace of F3^12 gives a
W(3,3), and Witt transitivity gives a single Sp12(3) orbit with stabilizer
Sp4(3) x Sp8(3).
"""
from __future__ import annotations
import json
from math import prod
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8233_8240_LEECH_W11QUTRIT_W33_SLICE_CENSUS.json'

def sp(n,q):return q**(n*n)*prod(q**(2*i)-1 for i in range(1,n+1)) # Sp(2n,q)
def main():
    a,b,c=sp(6,3),sp(2,3),sp(4,3);N=a//(b*c)
    assert b==51840 and N==2110666092277743
    out={'schema':'w33.pass8233_8240.leech_w11qutrit_w33_slice_census.v1','status':'PASS','passes':'8233-8240','outside_box':True,
      'dependency':'Parallel Pass8030-8040: Leech fixed-point-free order-3 quotient gives W(11,3); no pure Phi_9^4 class exists in Co0',
      'ambient':'W(11,3) = six-qutrit symplectic geometry on F3^12','slice':'W(3,3) on a nondegenerate symplectic F3^4',
      'Sp12_3_order':a,'stabilizer':'Sp4(3) x Sp8(3)','stabilizer_order':b*c,'W33_slices':N,
      'theorem':'The Leech six-qutrit carrier contains exactly 2,110,666,092,277,743 W33 subgeometries, forming one Sp12(3) orbit. Co0 failure of a pure Phi9^4 rung is therefore a failure of canonical cyclotomic descent, not absence of W33 subspaces.',
      'canonicality':'The bare W(11,3) carrier selects no preferred W33 slice; an E8/Leech bridge requires additional lattice or controller data.',
      'claim_boundary':'Exact classical symplectic orbit count; no physical six-qutrit implementation is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','W33_slices':N}))
if __name__=='__main__':main()
