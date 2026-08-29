#!/usr/bin/env python3
"""Construct the central-C3 three-sheeted bridge to the 216 qutrit Clifford.

The previous no-go proves that K/Z, where K is a 648 point stabilizer and
Z=Z(K)=C3, cannot act directly on the 216 sentinel five-circuits because Z
moves every circuit.  This audit asks the constructive next question: quotient
the circuit set by that free deck action.

Result: Z has 72 three-element circuit orbits.  K/Z has order 216 and acts
faithfully on those 72 fibres, split into two 36-orbits distinguished by whether
a five-circuit has 0 or 2 minimum supports through the distinguished W33 point.
The two quotient stabilizers are S3 and C6.  The central extension is nonsplit,
so any section carries a genuinely nontrivial C3-valued extension cocycle.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import w33_20260829_216_clifford_torsor_nogo as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260829_CLIFFORD_C3_CIRCUIT_COVER.json"


def perm_order(p):
    seen=set(); out=1
    for i in range(len(p)):
        if i in seen: continue
        j=i; n=0
        while j not in seen:
            seen.add(j); n+=1; j=p[j]
        out=math.lcm(out,n)
    return out


def orbit_partition(G, n):
    rem=set(range(n)); out=[]
    while rem:
        s=min(rem); O={g[s] for g in G}
        out.append(sorted(O)); rem-=O
    return sorted(out, key=lambda O:(-len(O),O))


def main():
    pts, idx, _, N = base.geometry()
    supports, masks = base.supports_from_N(N)

    circuits=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C: w ^= masks[i]
        if w==0: circuits.append(C)
    assert len(circuits)==216
    cidx={C:i for i,C in enumerate(circuits)}

    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*base.form(x,v)%3
                y=base.norm(tuple((x[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)}
    gens45=[tuple(si[frozenset(p[x] for x in S)] for S in supports) for p in gens40]
    chosen=(18,62,77,10)
    Gpaired=base.closure_paired([gens40[i] for i in chosen],[gens45[i] for i in chosen])
    assert len(Gpaired)==25920

    K={p45 for p40,p45 in Gpaired if p40[0]==0}
    assert len(K)==648

    def act_circuit(i,g):
        return cidx[tuple(sorted(g[x] for x in circuits[i]))]

    # Recover Z(K)=C3.
    kgens=base.deterministic_generators(K,45)
    Z=[z for z in K if all(base.compose(z,g)==base.compose(g,z) for g in kgens)]
    assert len(Z)==3
    e45=tuple(range(45))
    assert Counter(perm_order(z) for z in Z)==Counter({1:1,3:2})
    z=next(x for x in Z if x!=e45)

    # The central deck action is free on all 216 circuits.
    zperm=tuple(act_circuit(i,z) for i in range(216))
    zfibres=[]; seen=set()
    for i in range(216):
        if i in seen: continue
        O=[]; j=i
        while j not in seen:
            seen.add(j); O.append(j); j=zperm[j]
        zfibres.append(tuple(sorted(O)))
    assert len(zfibres)==72 and {len(O) for O in zfibres}=={3}
    fibre_of={x:i for i,O in enumerate(zfibres) for x in O}

    # Quotient action K/Z on the 72 deck fibres.
    def quotient_perm(g):
        return tuple(fibre_of[act_circuit(O[0],g)] for O in zfibres)
    Q={quotient_perm(g) for g in K}
    assert len(Q)==216                         # kernel is exactly Z

    q_orbits=orbit_partition(Q,72)
    assert [len(O) for O in q_orbits]==[36,36]

    orbit_records=[]
    for O in q_orbits:
        incidence_counts=set()
        for fi in O:
            C=circuits[zfibres[fi][0]]
            incidence_counts.add(sum(0 in supports[j] for j in C))
        assert len(incidence_counts)==1
        r=next(iter(incidence_counts))
        assert r in (0,2)
        seed=O[0]
        stab=[g for g in Q if g[seed]==seed]
        assert len(stab)==6
        orders=Counter(perm_order(g) for g in stab)
        if orders==Counter({1:1,2:3,3:2}):
            stabilizer="S3"
        elif orders==Counter({1:1,2:1,3:2,6:2}):
            stabilizer="C6"
        else:
            raise AssertionError(orders)
        orbit_records.append({"circuitSupportsThroughDistinguishedPoint":r,
                              "fibres":36,"circuitStates":108,
                              "quotientStabilizer":stabilizer})
    orbit_records.sort(key=lambda x:x["circuitSupportsThroughDistinguishedPoint"])
    assert orbit_records==[
        {"circuitSupportsThroughDistinguishedPoint":0,"fibres":36,"circuitStates":108,"quotientStabilizer":"S3"},
        {"circuitSupportsThroughDistinguishedPoint":2,"fibres":36,"circuitStates":108,"quotientStabilizer":"C6"},
    ]

    # K itself has the corresponding two 108-state circuit orbits.
    K216={tuple(act_circuit(i,g) for i in range(216)) for g in K}
    assert [len(O) for O in orbit_partition(K216,216)]==[108,108]

    # The extension 1 -> C3 -> K -> Q -> 1 is nonsplit.  The derived subgroup
    # has order 216 and already contains Z.  A complement would be an index-3
    # normal subgroup giving a map K->C3 nontrivial on Z, impossible because
    # every abelian quotient kills [K,K].
    Kderived=base.derived_subgroup(K,45)
    assert len(Kderived)==216
    assert set(Z).issubset(Kderived)

    # Explicit cocycle witness: classify orders of all three lifts of every
    # quotient element.  Forty-eight order-3 quotient elements have only
    # order-9 lifts, so no homomorphic section exists.
    lifts=defaultdict(list)
    for g in K: lifts[quotient_perm(g)].append(g)
    assert len(lifts)==216 and {len(v) for v in lifts.values()}=={3}
    lift_patterns=Counter()
    for q, pre in lifts.items():
        lift_patterns[(perm_order(q),tuple(sorted(perm_order(g) for g in pre)))] += 1
    expected_patterns=Counter({
        (1,(1,3,3)):1,
        (2,(2,6,6)):9,
        (3,(3,3,3)):32,
        (3,(9,9,9)):48,
        (4,(4,12,12)):54,
        (6,(6,6,6)):72,
    })
    assert lift_patterns==expected_patterns

    out={
      "schema":"w33.20260829.clifford-c3-circuit-cover.v1","status":"PASS",
      "centralExtension":{"K":"W33 point stabilizer","orderK":648,"center":"C3","orderQuotient":216,
        "quotient":"projective one-qutrit Clifford / Hessian ASL(2,3)","split":False,
        "derivedSubgroupOrder":216,"centerContainedInDerived":True},
      "threeSheetedCover":{"circuitStates":216,"deckGroup":"C3","deckFibres":72,"fibreSize":3,
        "centerActsFreely":True},
      "quotientAction":{"degree":72,"faithful":True,"orbitSizes":[36,36],"orbits":orbit_records},
      "cocycleWitness":{"statement":"the nonsplit central extension defines a nonzero C3-valued extension class for every set-theoretic section",
        "order3QuotientElementsWithOnlyOrder9Lifts":48,
        "liftOrderPatterns":[{"quotientOrder":qo,"liftOrders":list(lo),"elements":n}
          for (qo,lo),n in sorted(expected_patterns.items())]},
      "boundary":"The Clifford quotient acts canonically on the 72 central circuit fibres, not on the 216 circuits themselves. The three-sheeted lift is exact; it is not a regular 216-state Clifford torsor."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","cover":"216 -> 72","quotient":216,"orbits":[36,36],"nonsplit":True,"order3To9":48}))


if __name__=="__main__": main()
