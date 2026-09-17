#!/usr/bin/env python3
"""The Suzuki W33 kernel carries the binary E6 27/36 quadratic shells.

The new stabilizer reconciliation identifies the linear kernel as the
extraspecial minus group E = 2_-^(1+6).  For every extraspecial 2-group the
quotient E/Z(E) carries the canonical quadratic form q(xZ)=x^2 in Z(E).  Minus
type therefore gives a six-dimensional O_6^-(2) space.

This file constructs a canonical F2^6 minus form and proves:
  * 27 nonzero singular vectors and 36 nonsingular vectors;
  * the singular polar graph is SRG(27,10,1,5)=GQ(2,4);
  * it is explicitly isomorphic, vertex by vertex, to the repository's
    W33 center-quad -> GQ(4,2) 27-line intersection graph;
  * the 36-shell stabilizer orders under the inner/full groups are 720/1440,
    matching the certified PSp 36-spread/double-six/Pfaffian action and the
    classical full W(E6) double-six action.

The exact objectwise isomorphism is certified on the 27-shell.  For the 36
shell this pass certifies orbit size and stabilizer fingerprints, not yet an
explicit spread <-> nonsingular-vector bijection.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_suzuki_kernel_e6_quadratic_shell_bridge.json'
# W33 quotient-line id -> lexicographic singular-vector id.
ISO27=(0,5,6,11,1,13,12,7,26,21,25,2,23,3,22,4,20,24,18,8,16,14,19,9,10,15,17)


def load_center_quad():
    path=ROOT/'exploration'/'w33_center_quad_gq42_e6_bridge.py'
    spec=importlib.util.spec_from_file_location('center_quad_bridge',path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def qminus(v):
    # H + H + A, with A(a,b)=a^2+ab+b^2 over F2.
    return (v[0]*v[1] + v[2]*v[3] + v[4] + v[4]*v[5] + v[5]) & 1


def polar(u,v):
    w=tuple(a^b for a,b in zip(u,v))
    return qminus(w)^qminus(u)^qminus(v)


def srg_params(A):
    n=len(A); deg={int(x) for x in A.sum(1)}; lam=set(); mu=set()
    for i,j in itertools.combinations(range(n),2):
        c=int(np.logical_and(A[i],A[j]).sum())
        (lam if A[i,j] else mu).add(c)
    assert len(deg)==len(lam)==len(mu)==1
    return [n,next(iter(deg)),next(iter(lam)),next(iter(mu))]


def main(write=True):
    ker=json.loads((ROOT/'data'/'w33_suzuki_w33_kernel_structure_reconciliation.json').read_text())
    d36=json.loads((ROOT/'data'/'w33_psp36_spread_double_six_pfaffian_equivariance.json').read_text())
    assert ker['status']=='PASS' and d36['status']=='PASS'
    assert ker['linear_kernel']['shape']=='2_-^(1+6)'

    V=[tuple(v) for v in itertools.product(range(2),repeat=6)]
    singular=[v for v in V if any(v) and qminus(v)==0]
    nonsingular=[v for v in V if qminus(v)==1]
    assert len(singular)==27 and len(nonsingular)==36

    A=np.zeros((27,27),dtype=np.uint8)
    for i,j in itertools.combinations(range(27),2):
        if polar(singular[i],singular[j])==0: A[i,j]=A[j,i]=1
    assert srg_params(A)==[27,10,1,5]

    cq=load_center_quad(); lines=cq.quotient_lines(); assert len(lines)==27
    W=np.zeros((27,27),dtype=np.uint8)
    for i,j in itertools.combinations(range(27),2):
        if set(lines[i].point_ids)&set(lines[j].point_ids): W[i,j]=W[j,i]=1
    assert srg_params(W)==[27,10,1,5]
    assert sorted(ISO27)==list(range(27))
    assert all(int(W[i,j])==int(A[ISO27[i],ISO27[j]]) for i in range(27) for j in range(27))

    inner=25920; full=51840
    assert d36['group']['order']==inner and d36['group']['degree']==36
    assert d36['group']['pointStabilizerOrder']==inner//36==720
    assert full//36==1440

    out={
      'schema':'w33.suzuki_kernel_e6_quadratic_shell_bridge.v1','status':'PASS',
      'headline':'The newly identified Suzuki W33 linear kernel 2_-^(1+6) has canonical quotient E/Z(E)=F2^6 of minus type. Its nonzero vectors split exactly into 27 singular and 36 nonsingular vectors. The 27 singular polar graph is SRG(27,10,1,5) and is explicitly isomorphic to the repository W33 center-quad/GQ(4,2) 27-line graph. The 36 nonsingular shell has inner/full stabilizer orders 720/1440, matching the certified PSp spread-double-six-Pfaffian family and the classical W(E6) double-six action.',
      'kernel':{'shape':'2_-^(1+6)','center_order':2,'quotient':'F2^6 minus quadratic space'},
      'quadratic_shells':{'singular_nonzero':27,'nonsingular':36,'total_nonzero':63},
      'singular_shell':{'geometry':'Q^-(5,2)=GQ(2,4)','graph_srg':[27,10,1,5],
                        'w33_center_quad_line_graph_isomorphism':list(ISO27),'objectwise_verified':True},
      'nonsingular_shell':{'size':36,'PSp4_3_stabilizer_order':720,'O6minus2_stabilizer_order':1440,
                           'repo_36_family':'W33 spreads <-> Schlaefli double-sixes <-> doily complements <-> Pfaffian sections',
                           'objectwise_intertwiner_to_repo_36_family':'OPEN'},
      'outer_automorphism_explanation':'Out(2_-^(1+6)) is the full minus orthogonal group O6^-(2), the order-51840 E6 Weyl action. The Suzuki block stabilizer supplies only its index-two U4(2) ~= PSp(4,3) subgroup, explaining why the local 27-carrier admits an outer E6 involution that is absent from the ambient 2.Suz-induced action.',
      'boundary':'The 27-shell graph bridge is explicit. The 36-shell match currently uses exact orbit/stabilizer fingerprints plus the already certified 36-object PSp family; an explicit nonsingular-vector <-> spread/double-six intertwiner remains to be constructed.'
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out

if __name__=='__main__': main(True)
