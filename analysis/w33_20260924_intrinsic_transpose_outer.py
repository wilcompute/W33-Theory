#!/usr/bin/env python3
"""Intrinsic qutrit-transpose construction of the E6 outer involution.

In the canonical W33 center-quad coordinates (z1,z2,x1,x2), transposition of
two-qutrit Pauli monomials sends x -> -x and fixes z, i.e.
diag(1,1,-1,-1).  This script transports that anti-symplectic similitude
through the 90-center-quad -> 45-point GQ(4,2) quotient and compares it with
BT171/172's formerly GAP-imported outer involution.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
OUT = ROOT / "data/w33_20260924_intrinsic_transpose_outer.json"

from exploration.w33_center_quad_gq42_e6_bridge import (
    w33_points, center_quads, center_quad_pairing, quotient_points,
    _normalize_projective, symplectic_form,
)

def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inverse_perm(p):
    out = [0]*len(p)
    for i,j in enumerate(p):
        out[j] = i
    return tuple(out)


def cycles(p):
    seen=set(); out=[]
    for s in range(len(p)):
        if s in seen:
            continue
        c=[]; x=s
        while x not in seen:
            seen.add(x); c.append(x); x=p[x]
        out.append(tuple(c))
    return out


def point_perm_from_matrix(M):
    pts = w33_points()
    pidx = {p:i for i,p in enumerate(pts)}
    out=[]
    for v in pts:
        w=tuple(sum(M[i][j]*v[j] for j in range(4))%3 for i in range(4))
        out.append(pidx[_normalize_projective(w)])
    return tuple(out)
def quotient_perm_from_point_perm(pp):
    quads=center_quads()
    qidx={frozenset(q):i for i,q in enumerate(quads)}
    quad_perm=[]
    for q in quads:
        quad_perm.append(qidx[frozenset(pp[v] for v in q)])

    qpoints=quotient_points()
    pair_to_id={tuple(sorted(qp.quad_pair)):qp.point_id for qp in qpoints}
    out=[]
    for qp in qpoints:
        pair=tuple(sorted(quad_perm[q] for q in qp.quad_pair))
        out.append(pair_to_id[pair])
    return tuple(out)


def transvection_point_perm(v):
    pts=w33_points()
    pidx={p:i for i,p in enumerate(pts)}
    out=[]
    for x in pts:
        a=symplectic_form(x,v)
        y=tuple((x[i]+a*v[i])%3 for i in range(4))
        out.append(pidx[_normalize_projective(y)])
    return tuple(out)
def generate_inner_quotient_group():
    pts=w33_points()
    qgens=[quotient_perm_from_point_perm(transvection_point_perm(v)) for v in pts]
    ident=tuple(range(45))
    group={ident}
    todo=deque([ident])
    while todo:
        g=todo.popleft()
        for h in qgens:
            y=compose(h,g)
            if y not in group:
                group.add(y); todo.append(y)
    assert len(group)==25920
    return group


def transported_bt172_to_centerquad():
    cross=json.loads((ROOT/"data/w33_BREAKTHROUGH_169_gap_f4_centerquad_crosswalk.json").read_text())
    bt=json.loads((ROOT/"data/w33_BREAKTHROUGH_172_outer_involution_temporal_qutrit.json").read_text())
    m=cross["point_mapping_f4_to_centerquad"]
    outer=bt["outer_permutation_zero_based"]
    out=[0]*45
    for i in range(45):
        out[m[i]]=m[outer[i]]
    return tuple(out)
def find_conjugator(group, source, target):
    sinv=inverse_perm(source)
    for h in group:
        hi=inverse_perm(h)
        if compose(compose(h,source),hi)==target:
            return h
    return None


def fixed_support_signature(p):
    fixed=[i for i,x in enumerate(p) if i==x]
    return {
        "fixed":fixed,
        "count":len(fixed),
        "cycle_hist":dict(Counter(map(len,cycles(p)))),
    }


def main():
    # Pauli transpose in (z1,z2,x1,x2) coordinates.
    T=((1,0,0,0),(0,1,0,0),(0,0,2,0),(0,0,0,2))
    pp=point_perm_from_matrix(T)
    intrinsic=quotient_perm_from_point_perm(pp)
    target=transported_bt172_to_centerquad()

    assert compose(pp,pp)==tuple(range(40))
    assert compose(intrinsic,intrinsic)==tuple(range(45))
    assert fixed_support_signature(intrinsic)["cycle_hist"]=={1:7,2:19}
    assert fixed_support_signature(target)["cycle_hist"]=={1:7,2:19}

    inner=generate_inner_quotient_group()
    conj=find_conjugator(inner,intrinsic,target)
    assert conj is not None
    # Verify anti-symplectic multiplier -1 directly on all vectors.
    pts=w33_points()
    anti=True
    for a in pts:
        for b in pts:
            Ta=tuple(sum(T[i][j]*a[j] for j in range(4))%3 for i in range(4))
            Tb=tuple(sum(T[i][j]*b[j] for j in range(4))%3 for i in range(4))
            anti &= symplectic_form(Ta,Tb)==(-symplectic_form(a,b))%3
    assert anti

    out={
        "schema":"w33.20260924.intrinsic_transpose_outer.v1",
        "status":"PASS_INTRINSIC_QUTRIT_TRANSPOSE_IS_BT172_OUTER_CLASS",
        "pauli_convention":{
            "coordinates":"(z1,z2,x1,x2)",
            "monomial":"X1^x1 Z1^z1 tensor X2^x2 Z2^z2",
            "transpose_projective_action":"(z1,z2,x1,x2)->(z1,z2,-x1,-x2)",
            "matrix_mod3":[list(r) for r in T],
        },
        "w33_action":{
            "anti_symplectic_multiplier":2,
            "squares_to_identity":True,
            "point_cycle_histogram":dict(Counter(map(len,cycles(pp)))),
            "fixed_w33_points":[i for i,x in enumerate(pp) if i==x],
        },
        "centerquad_45_action":{
            "intrinsic_cycle_histogram":fixed_support_signature(intrinsic)["cycle_hist"],
            "intrinsic_fixed_points":fixed_support_signature(intrinsic)["fixed"],
            "bt172_transported_cycle_histogram":fixed_support_signature(target)["cycle_hist"],
            "bt172_transported_fixed_points":fixed_support_signature(target)["fixed"],
            "exactly_equal_in_frozen_crosswalk_gauge":intrinsic==target,
            "PSp_conjugate":True,
            "inner_conjugator_zero_based":list(conj),
        },
        "theorem":(
            "Ordinary transpose of the two-qutrit Pauli algebra induces the canonical "
            "W33 anti-symplectic similitude diag(1,1,-1,-1). On the intrinsic "
            "center-quad GQ(4,2) quotient its order-two permutation has cycle shape "
            "1^7 2^19 and is conjugate under the inner PSp(4,3) quotient action to "
            "the BT171/172 full-W(E6) outer involution. Thus BT172's temporal "
            "reversal class has an intrinsic qutrit-transpose construction."
        ),
        "boundary":(
            "The conjugator depends on the noncanonical BT169 labeling crosswalk. "
            "This proves equality of the outer conjugacy class, not a canonical "
            "point-by-point identification without a chosen quotient gauge."
        ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":out["status"],
        "w33_point_cycles":out["w33_action"]["point_cycle_histogram"],
        "q45_cycles":out["centerquad_45_action"]["intrinsic_cycle_histogram"],
        "equal_in_gauge":out["centerquad_45_action"]["exactly_equal_in_frozen_crosswalk_gauge"],
        "PSp_conjugate":True,
    },indent=2))


if __name__=="__main__":
    main()
