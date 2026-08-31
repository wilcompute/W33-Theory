#!/usr/bin/env python3
"""Exact classification of the W(3,3) 2-ovoid and sentinel-circuit 216-sets.

Holotrade independently certifies exactly 432 point-set size-20 m-ovoids of
W(3,3), i.e. 2-ovoids.  Complementation pairs these into 216 unoriented
hemisystems.  The W33 sentinel shell independently has 216 five-circuits.

Equal cardinality and abstract S5 stabilizers strongly suggest the two 216-sets
might be PSp(4,3)-equivariantly identical.  The first version of this audit
explicitly tested that hypothesis and failed because the hemisystem-pair S5
fixes no sentinel five-circuit.  This version turns that failure into a theorem:
it computes both S5 actions, their orbit partitions on the opposite 216-set,
and the corresponding oriented A5 stabilizers.

What remains true and is certified here:
  * 432 two-ovoids form one PSp(4,3)/A5 orbit;
  * complementation gives 216 pairs with S5 stabilizer;
  * 216 sentinel five-circuits form a distinct PSp(4,3)/S5 orbit type;
  * the two S5 subgroups are nonconjugate in PSp(4,3), despite having the same
    abstract element-order profile and index 216.

Boundary: this is a finite G-set classification, not a Clifford or physical
identification.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import w33_20260829_216_clifford_torsor_nogo as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260831_HEMISYSTEM_CIRCUIT_BRIDGE.json"
T0 = frozenset([0,1,2,3,5,7,8,9,15,16,17,20,24,26,27,28,33,34,36,39])
ALL40 = frozenset(range(40))


def canon_pair(T):
    C = ALL40 - T
    a, b = tuple(sorted(T)), tuple(sorted(C))
    return (a, b) if a < b else (b, a)


def parts(H, n, action):
    rem=set(range(n)); out=[]
    while rem:
        s=min(rem); O={action(g,s) for g in H}; out.append(sorted(O)); rem-=O
    return sorted(out,key=lambda O:(-len(O),O))


def main():
    pts, idx, lines, N = base.geometry()
    supports, masks = base.supports_from_N(N)
    nbr=[set() for _ in range(40)]
    for L in lines:
        for a in L: nbr[a].update(x for x in L if x!=a)
    assert {len(nbr[x]) for x in range(40)}=={12}
    assert {len(nbr[x]&T0) for x in T0}=={4}
    assert {len(nbr[x]&T0) for x in ALL40-T0}=={8}

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

    def image_set(p,T): return frozenset(p[x] for x in T)

    # Oriented two-ovoid orbit and A5 stabilizer.
    orbit432={image_set(p40,T0) for p40,_ in Gpaired}
    assert len(orbit432)==432
    assert all({len(nbr[x]&T) for x in T}=={4} and {len(nbr[x]&T) for x in ALL40-T}=={8} for T in orbit432)
    stab_T=[(p40,p45) for p40,p45 in Gpaired if image_set(p40,T0)==T0]
    assert len(stab_T)==60
    order_A=Counter(base.porder(p40) for p40,_ in stab_T)
    assert order_A==Counter({1:1,2:15,3:20,5:24})

    # Unoriented complement-pair orbit and S5 stabilizer.
    pair_list=sorted({canon_pair(T) for T in orbit432})
    pair_idx={P:i for i,P in enumerate(pair_list)}
    assert len(pair_list)==216
    P0=canon_pair(T0)
    stab_pair=[(p40,p45) for p40,p45 in Gpaired if image_set(p40,T0) in (T0,ALL40-T0)]
    assert len(stab_pair)==120
    order_HP=Counter(base.porder(p40) for p40,_ in stab_pair)
    assert order_HP==Counter({1:1,2:25,3:20,4:30,5:24,6:20})

    # Sentinel five-circuits and one circuit S5 stabilizer.
    circuits=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C: w^=masks[i]
        if w==0: circuits.append(C)
    assert len(circuits)==216
    cidx={C:i for i,C in enumerate(circuits)}
    C0=circuits[0]; C0s=set(C0)
    stab_circuit=[(p40,p45) for p40,p45 in Gpaired if {p45[x] for x in C0s}==C0s]
    assert len(stab_circuit)==120
    order_HC=Counter(base.porder(p40) for p40,_ in stab_circuit)
    assert order_HC==order_HP

    Hpair45=[p45 for _,p45 in stab_pair]
    Hpair40=[p40 for p40,_ in stab_pair]
    Hcirc45=[p45 for _,p45 in stab_circuit]
    Hcirc40=[p40 for p40,_ in stab_circuit]

    def act_circuit(g45,i):
        return cidx[tuple(sorted(g45[x] for x in circuits[i]))]
    def act_pair(g40,i):
        A=frozenset(pair_list[i][0])
        return pair_idx[canon_pair(image_set(g40,A))]

    pairS5_on_circuits=parts(Hpair45,216,act_circuit)
    circS5_on_pairs=parts(Hcirc40,216,act_pair)
    fixed_circuits=sum(len(O)==1 for O in pairS5_on_circuits)
    fixed_pairs=sum(len(O)==1 for O in circS5_on_pairs)
    assert fixed_circuits==0 and fixed_pairs==0

    # Since both stabilizers have order 120, conjugacy would imply one fixes a
    # point of the other's G/H action.  Zero fixed points is therefore an exact
    # nonconjugacy certificate.
    s5_conjugate=False

    # Native 45- and 40-point orbit fingerprints.
    pairS5_45=parts(Hpair45,45,lambda g,i:g[i])
    circS5_45=parts(Hcirc45,45,lambda g,i:g[i])
    pairS5_40=parts(Hpair40,40,lambda g,i:g[i])
    circS5_40=parts(Hcirc40,40,lambda g,i:g[i])

    # A5 in the circuit S5 is its derived subgroup.  Compare its action with
    # the oriented-hemisystem A5 without presuming conjugacy.
    Ac45=base.derived_subgroup(set(Hcirc45),45)
    assert len(Ac45)==60
    # recover the paired 40 permutations whose 45 action lies in Ac45
    Ac_pairs=[(p40,p45) for p40,p45 in Gpaired if p45 in Ac45]
    assert len(Ac_pairs)==60
    Ac40=[p40 for p40,_ in Ac_pairs]
    Ahemi45=[p45 for _,p45 in stab_T]
    Ahemi40=[p40 for p40,_ in stab_T]

    Ahemi_on_circuits=parts(Ahemi45,216,act_circuit)
    Acirc_on_oriented=[]
    # action on the 432 oriented two-ovoids
    olist=sorted(tuple(sorted(T)) for T in orbit432); oidx={T:i for i,T in enumerate(olist)}
    def act_ovoid(g40,i): return oidx[tuple(sorted(image_set(g40,frozenset(olist[i]))))]
    Acirc_on_oriented=parts(Ac40,432,act_ovoid)
    Ahemi_fixed_circuits=sum(len(O)==1 for O in Ahemi_on_circuits)
    Acirc_fixed_ovoids=sum(len(O)==1 for O in Acirc_on_oriented)
    # Same-order A5s are conjugate iff either fixes a point in the other's G/A5 action.
    a5_conjugate=(Ahemi_fixed_circuits>0 or Acirc_fixed_ovoids>0)  # diagnostic relation to circuit-derived A5 action

    # Direct stabilizer intersections at the chosen representatives.
    interS5_45=set(Hpair45)&set(Hcirc45)
    interA5_45=set(Ahemi45)&set(Ac45)

    # Intersection histogram of all 45 sentinel supports with an oriented half.
    support_hist=Counter(len(S&T0) for S in supports)

    out={
      "schema":"w33.20260831.hemisystem-circuit-bridge.v2",
      "status":"PASS",
      "twoOvoids":{"orbitSize":432,"stabilizerOrder":60,"stabilizerType":"A5",
        "stabilizerElementOrders":dict(sorted(order_A.items())),
        "A5PointOrbits40":sorted(map(len,parts(Ahemi40,40,lambda g,i:g[i]))),
        "supportIntersectionHistogram45":dict(sorted(support_hist.items()))},
      "hemisystemPairs":{"count":216,"stabilizerOrder":120,"stabilizerType":"S5",
        "stabilizerElementOrders":dict(sorted(order_HP.items())),
        "orbitsOn45":sorted(map(len,pairS5_45)),"orbitsOn40":sorted(map(len,pairS5_40))},
      "sentinelCircuits":{"count":216,"stabilizerOrder":120,"stabilizerType":"S5",
        "stabilizerElementOrders":dict(sorted(order_HC.items())),
        "orbitsOn45":sorted(map(len,circS5_45)),"orbitsOn40":sorted(map(len,circS5_40))},
      "crossActions":{
        "hemisystemS5On216Circuits":sorted(map(len,pairS5_on_circuits),reverse=True),
        "circuitS5On216HemisystemPairs":sorted(map(len,circS5_on_pairs),reverse=True),
        "hemisystemS5FixedCircuits":fixed_circuits,"circuitS5FixedPairs":fixed_pairs,
        "S5ConjugateInPSp":s5_conjugate,
        "chosenS5IntersectionOrder":len(interS5_45)},
      "A5CrossDiagnostic":{
        "hemisystemA5FixedCircuits":Ahemi_fixed_circuits,
        "circuitDerivedA5FixedOrientedTwoOvoids":Acirc_fixed_ovoids,
        "conjugacyWitnessDetected":a5_conjugate,
        "chosenA5IntersectionOrder":len(interA5_45),
        "hemisystemA5CircuitOrbitSizes":sorted(map(len,Ahemi_on_circuits),reverse=True),
        "circuitA5OrientedOvoidOrbitSizes":sorted(map(len,Acirc_on_oriented),reverse=True)},
      "theorem":"The 432 W33 two-ovoids form a PSp(4,3)/A5 orbit and complement to a 216-point PSp(4,3)/S5 orbit. The sentinel five-circuits form another 216-point PSp(4,3)/S5 orbit, but the two S5 stabilizers are nonconjugate: each has zero fixed points on the other's 216-set. Equal counts and abstract stabilizer type therefore do not define an equivariant bridge.",
      "boundary":"This is an exact finite G-set no-go. It leaves open non-equivariant correspondences and other geometric relations between the two 216-sets."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","twoOvoidOrbit":432,"A5":60,"pairs":216,"S5":120,
      "pairS5OnCircuits":out["crossActions"]["hemisystemS5On216Circuits"],
      "circuitS5OnPairs":out["crossActions"]["circuitS5On216HemisystemPairs"],
      "S5conjugate":False,"S5intersection":len(interS5_45),
      "A5fixedCross":[Ahemi_fixed_circuits,Acirc_fixed_ovoids],"A5intersection":len(interA5_45),
      "pair45":out["hemisystemPairs"]["orbitsOn45"],"circ45":out["sentinelCircuits"]["orbitsOn45"],
      "supportHist":dict(sorted(support_hist.items()))},sort_keys=True))

if __name__=="__main__": main()
