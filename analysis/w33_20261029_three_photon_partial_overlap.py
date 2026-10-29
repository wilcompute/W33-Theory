#!/usr/bin/env python3
"""Rigorous W33/dual three-photon discrimination for uniform partial overlap s.

U=(2J-5(I+A))/15. For three pure internal photon states having real
pairwise overlap s in [0,1], three-distinct-input/output probability is
(c0+c2*s*s+c3*s*s*s)/15**6. All 512 possible {-3,2} scattering
numerator patterns are audited with the six S3 permutations.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import json
from w33_20261029_three_photon_dual_discriminator import two_graphs

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261029_three_photon_partial_overlap.json"
PERMS=tuple(permutations(range(3)))
DENOM=15**6

def coefficients(pattern):
    h=tuple(-3 if pattern >> i & 1 else 2 for i in range(9))
    p=tuple(h[t[0]]*h[3+t[1]]*h[6+t[2]] for t in PERMS)
    c=[0,0,0]
    for i,a in enumerate(PERMS):
        for j,b in enumerate(PERMS):
            mismatch=sum(a[k]!=b[k] for k in range(3))
            assert mismatch in (0,2,3)
            c[{0:0,2:1,3:2}[mismatch]]+=p[i]*p[j]
    assert sum(c)==sum(p)**2
    return tuple(c)

def independent_triples(M):
    rows=[sum(int(M[i,j])<<j for j in range(40)) for i in range(40)]
    hist=Counter()
    witness=None
    for a,b,c in combinations(range(40),3):
        if rows[a]>>b&1 or rows[a]>>c&1 or rows[b]>>c&1:
            continue
        common=rows[a]&rows[b]&rows[c]
        k=common.bit_count()
        hist[k]+=1
        if witness is None and k>=3:
            output=tuple(j for j in range(40) if common>>j&1)[:3]
            assert len(output)==3 and all(rows[x]>>y&1 for x in (a,b,c) for y in output)
            witness=((a,b,c),output)
    return dict(hist),witness

def main():
    A,B=two_graphs()
    w33,_=independent_triples(A)
    dual,no_witness=independent_triples(B)
    assert w33=={1:2880,4:360}
    assert dual=={0:1080,2:2160} and no_witness is None
    # SAME physical input ports: the first W33-independent triple is not
    # necessarily independent in the dual's fixed line-mode ordering.
    # Select one that is independent in BOTH graphs and has four
    # common point-graph neighbors. This avoids an invalid comparison.
    witness=None
    for abc in combinations(range(40),3):
        if any(A[i,j] or B[i,j] for i,j in combinations(abc,2)):
            continue
        common=[k for k in range(40) if all(A[i,k] for i in abc)]
        if len(common)==4:
            witness=(abc,tuple(common[:3]))
            break
    assert witness is not None and not (set(witness[0])&set(witness[1]))
    assert all(not A[i,j] and not B[i,j] for i,j in combinations(witness[0],2))
    patterns=[coefficients(m) for m in range(512)]
    w=patterns[-1]
    assert w==(4374,13122,8748)
    # A 3x3 all-minus-three pattern requires THREE outputs which are
    # all common neighbors of the THREE independent inputs. Dual forbids.
    bound=tuple(max(v[k] for v in patterns[:-1]) for k in range(3))
    assert bound==(3564,5832,3888)
    margin=tuple(w[i]-bound[i] for i in range(3))
    assert margin==(810,7290,4860) and min(margin)>0
    data={
      "status":"PASS","model":"Three photon pure internal states with equal real pairwise overlap s in [0,1], detector insensitive to internal state",
      "unitary":"U=(2J-5(I+A))/15 at t=pi/2",
      "all_3x3_signed_patterns":512,
      "W33_independent_triple_common_neighbor_histogram":{str(k):v for k,v in w33.items()},
      "dual_independent_triple_common_neighbor_histogram":{str(k):v for k,v in dual.items()},
      "W33_witness_input":list(witness[0]),
      "identical_input_ports_independent_in_both_graphs":True,
      "W33_witness_output":list(witness[1]),
      "W33_witness_coefficient_tuple":list(w),
      "dual_universal_upper_coefficient_tuple":list(bound),
      "guaranteed_strict_gap_coefficient_tuple":list(margin),
      "probability_denominator":DENOM,
      "guaranteed_probability_gap_at_s0":margin[0]/DENOM,
      "guaranteed_probability_gap_at_s1":sum(margin)/DENOM,
      "theorem":"For every s in [0,1], W33 has an event P=(4374+13122*s^2+8748*s^3)/15^6 exceeding ALL independent-input, distinct-output dual events bounded by (3564+5832*s^2+3888*s^3)/15^6.",
      "scope":"Calibrated ideal conventional quantum optics; no loss/dark counts/partial-number-resolution modeling; no beyond-QM or TOE prediction."
    }
    OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf8")
    print("PASS",w,bound,margin,"input/output",witness)
    return data
if __name__=="__main__":
    main()
