#!/usr/bin/env python3
"""Resolve the local C3 lift obstruction into conjugacy orbits of ASL(2,3).

The certified central extension K -> Q has Q ~= ASL(2,3), with 40 cyclic
order-three subgroups.  The preceding lift-charge audit proves that 16 of those
subgroups lift to C3 x C3 and 24 lift to C9.

This script constructs ASL(2,3)=F_3^2 : SL(2,3) directly and computes the
conjugacy orbits of its cyclic order-three subgroups.  They have sizes 4, 12,
and 24.  Their affine types are respectively:

  * 4 pure translation subgroups (no affine fixed point),
  * 12 nontranslation unipotent subgroups with three affine fixed points,
  * 24 nontranslation unipotent subgroups with no affine fixed point.

Split/nonsplit restriction is invariant under quotient conjugacy.  Because the
certified nonsplit population has size exactly 24, the unique 24-orbit is
exactly the C9 obstruction orbit.  Thus the extension class detects the
fixed-point-free *nontranslation* order-three directions, while both pure
translations and fixed-line unipotents split.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "data/PART_W33_20260830_CLIFFORD_C3_LIFT_CHARGE.json"
OUT = ROOT / "data/PART_W33_20260830_CLIFFORD_C3_ORDER3_ORBITS.json"
P = 3
I = (1, 0, 0, 1)
ZERO = (0, 0)


def mm(A, B):
    a,b,c,d=A; e,f,g,h=B
    return ((a*e+b*g)%P, (a*f+b*h)%P, (c*e+d*g)%P, (c*f+d*h)%P)


def mv(A, v):
    a,b,c,d=A; x,y=v
    return ((a*x+b*y)%P, (c*x+d*y)%P)


def add(u, v): return ((u[0]+v[0])%P, (u[1]+v[1])%P)
def neg(v): return ((-v[0])%P, (-v[1])%P)


def minv(A):
    a,b,c,d=A
    # det(A)=1 in SL(2,3)
    return (d%P, (-b)%P, (-c)%P, a%P)


def mul(g, h):
    A,v=g; B,w=h
    return (mm(A,B), add(v,mv(A,w)))


def inv(g):
    A,v=g; Ai=minv(A)
    return (Ai, neg(mv(Ai,v)))


E=(I,ZERO)


def power(g,n):
    r=E
    for _ in range(n): r=mul(r,g)
    return r


def order(g):
    r=E
    for n in range(1,25):
        r=mul(r,g)
        if r==E: return n
    raise AssertionError("order exceeded 24")


def action(g,x):
    A,v=g
    return add(mv(A,x),v)


def canonical_subgroup(g):
    return frozenset((E,g,power(g,2)))


def main():
    cert=json.loads(IN.read_text())
    assert cert["status"]=="PASS"
    R=cert["order3Restrictions"]
    assert (R["cyclicC3Subgroups"],R["splitC3xC3Preimages"],R["nonsplitC9Preimages"])==(40,16,24)

    SL=[]
    for a,b,c,d in product(range(P),repeat=4):
        if (a*d-b*c)%P==1: SL.append((a,b,c,d))
    assert len(SL)==24
    G=[(A,v) for A in SL for v in product(range(P),repeat=2)]
    assert len(G)==216

    order_dist=Counter(order(g) for g in G)
    assert order_dist==Counter({1:1,2:9,3:80,4:54,6:72})

    subgroups={canonical_subgroup(g) for g in G if order(g)==3}
    assert len(subgroups)==40
    subs=sorted(subgroups,key=lambda H:repr(sorted(H)))
    index={H:i for i,H in enumerate(subs)}
    invs={x:inv(x) for x in G}

    def conj(x,g): return mul(mul(x,g),invs[x])
    def conj_sub(x,H): return frozenset(conj(x,g) for g in H)

    unseen=set(range(len(subs))); orbits=[]
    while unseen:
        i=min(unseen); H=subs[i]
        O={index[conj_sub(x,H)] for x in G}
        unseen-=O; orbits.append(sorted(O))
    assert sorted(map(len,orbits))==[4,12,24]

    affine_points=list(product(range(P),repeat=2))
    orbit_records=[]
    for O in orbits:
        H=subs[O[0]]
        gens=[g for g in H if g!=E]
        g=gens[0]; A,_=g
        fixed=sum(action(g,x)==x for x in affine_points)
        pure_translation=(A==I)
        linear_order=order((A,ZERO))
        if pure_translation:
            kind="pure-translation"
            assert len(O)==4 and fixed==0 and linear_order==1
        elif fixed==3:
            kind="unipotent-with-affine-fixed-line"
            assert len(O)==12 and linear_order==3
        else:
            kind="fixed-point-free-nontranslation-unipotent"
            assert len(O)==24 and fixed==0 and linear_order==3
        orbit_records.append({
            "subgroups":len(O),
            "nonidentityElements":2*len(O),
            "affineType":kind,
            "affineFixedPointsPerNonidentityGenerator":fixed,
            "linearPartOrder":linear_order,
            "pureTranslation":pure_translation,
        })

    orbit_records.sort(key=lambda r:r["subgroups"])
    # The restriction type is conjugacy-invariant.  The only union of complete
    # conjugacy orbits having size 24 is the unique 24-orbit itself.
    for r in orbit_records:
        if r["subgroups"]==24:
            r["extensionRestriction"]="nonsplit C9"
        else:
            r["extensionRestriction"]="split C3 x C3"
    assert sum(r["subgroups"] for r in orbit_records if r["extensionRestriction"]=="nonsplit C9")==24
    assert sum(r["subgroups"] for r in orbit_records if r["extensionRestriction"]=="split C3 x C3")==16

    out={
        "schema":"w33.20260830.clifford-c3-order3-orbits.v1",
        "status":"PASS",
        "inputCertificate":IN.name,
        "quotientModel":{"group":"ASL(2,3) = F3^2 : SL(2,3)","order":216,"orderDistribution":dict(sorted(order_dist.items()))},
        "cyclicOrder3Subgroups":{"total":40,"conjugacyOrbitSizes":[4,12,24],"orbits":orbit_records},
        "obstructionClassification":{
            "splitSubgroups":16,
            "nonsplitSubgroups":24,
            "nonsplitOrbit":"the unique 24-subgroup orbit",
            "geometricType":"fixed-point-free nontranslation unipotent affine C3 directions",
            "statement":"Pure translations (4) and fixed-line unipotents (12) lift to C3 x C3; fixed-point-free nontranslation unipotents (24) lift to C9.",
        },
        "theorem":"The 3/5 local C3 obstruction is one complete Clifford conjugacy orbit: ASL(2,3) has order-three subgroup orbits 4+12+24, and the unique 24-orbit is exactly the nonsplit C9 restriction locus.",
        "boundary":"The affine fixed-point classification is exact in the canonical ASL(2,3) quotient model. Relating these affine directions to optical phase-space coordinates requires an explicit physical coordinate intertwiner.",
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","order3Orbits":[4,12,24],"split":[4,12],"nonsplit":[24]},sort_keys=True))


if __name__=="__main__": main()
