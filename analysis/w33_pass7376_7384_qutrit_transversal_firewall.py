#!/usr/bin/env python3
"""Pass7376-7384 outside-box: stress-test naive ternary triorthogonality.

C3=[45,14,15]_3 is self-orthogonal and 3-divisible, but neither property by
itself implies a transversal non-Clifford logical gate.  This verifier computes
the cubic coordinate-overlap tensor

    T(u,v,w) = sum_i u_i v_i w_i mod 3

on a deterministic basis of C3.  It is not identically zero.  Therefore the
straight ternary analogue of the usual binary triorthogonality criterion fails
for this basis-independent trilinear form, and no transversal non-Clifford claim
is licensed by the present code data.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from w33_pass4992_4999_common import build_base
import w33_pass7329_7336_char3_e6_defect as m3

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7376_7384_QUTRIT_TRANSVERSAL_FIREWALL.json'

def main():
    b=build_base();N=1-np.asarray(b['M'],dtype=int)
    C=m3.basis([row for row in N.T]);assert len(C)==14
    G=np.asarray(C,dtype=int)%3
    assert np.all((G@G.T)%3==0)
    weights=[]
    for row in G:weights.append(int(np.count_nonzero(row)))
    assert all(w%3==0 for w in weights)
    nonzero=[]
    for i,j,k in itertools.combinations_with_replacement(range(14),3):
        z=int(np.sum(G[i]*G[j]*G[k])%3)
        if z:nonzero.append((i,j,k,z))
    assert nonzero and len(nonzero)==275
    first=nonzero[0]
    # Basis-independence of the obstruction: if the trilinear form were zero on
    # the entire code, it would be zero on every basis triple. One witness on a
    # spanning basis proves the form itself is nonzero.
    out={'schema':'w33.pass7376_7384.qutrit_transversal_firewall.v1','status':'PASS',
      'code':'C3=[45,14,15]_3','self_orthogonal':True,
      'basis_row_weights':weights,'all_basis_row_weights_divisible_by_3':True,
      'cubic_overlap':'T(u,v,w)=sum_i u_i v_i w_i mod 3',
      'nonzero_basis_triples':len(nonzero),'first_nonzero_basis_triple':list(first),
      'conclusion':'The cubic overlap form is nonzero on C3. Naive ternary total-triorthogonality fails; no transversal non-Clifford gate claim follows from the present self-orthogonal/3-divisible code data.',
      'forward_target':'Test a genuine homological/Bockstein refinement criterion on an integral lift of the RN=3Q curved complex instead of importing binary triorthogonality.',
      'boundary':'Negative gate-criterion firewall only; this does not prove that no transversal non-Clifford gate exists by some different mechanism.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','nonzero_triples':len(nonzero),'first':first,'naive_triorthogonality':False}))
if __name__=='__main__':main()
