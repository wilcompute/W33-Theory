#!/usr/bin/env python3
"""Pass5159: all-q four-chamber apartment-intersection law.

Pass5140 gives the complete triple-star law.  Four distinct chamber edges can
occur in one apartment C8 in exactly seven dihedral distance patterns.  Six of
those patterns already determine the entire C8 and therefore have one common
apartment.  The remaining pattern consists of four consecutive C8 edges; after
its length-four gallery is fixed, one generalized-quadrangle projection choice
remains, giving q common apartments.

A complete rooted census at q=2,3,4,5 (including GF(4)) verifies every signature
and multiplicity and checks there is no hidden split of a six-distance signature.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5159_ALLQ_FOUR_CHAMBER_INTERSECTION_CENSUS.json'
PATH4=(1,1,1,2,2,3)
UNIT_SIGS={
 (1,1,2,2,3,4),(1,1,2,3,3,4),(1,1,3,3,4,4),
 (1,2,2,3,3,3),(1,2,2,3,3,4),(2,2,2,2,4,4)
}


def pair_dist(q,S,a,b):
    w=(S[a]&S[b]).bit_count()
    for d in range(1,5):
        if w==q**(4-d):return d
    raise AssertionError((q,a,b,w))


def anchor(q):
    G=build_W(q);S=chamber_stars(G);base=0
    containing=[tuple(sorted(es)) for es in G['apt_edges'] if base in es]
    assert len(containing)==q**4
    counts=Counter()
    for es in containing:
        rest=[x for x in es if x!=base]
        for abc in itertools.combinations(rest,3):counts[(base,)+tuple(sorted(abc))]+=1
    by_sig=defaultdict(Counter);hist=Counter()
    for Q,c in counts.items():
        sig=tuple(sorted(pair_dist(q,S,a,b) for a,b in itertools.combinations(Q,2)))
        by_sig[sig][c]+=1;hist[c]+=1
    assert set(by_sig)==UNIT_SIGS|{PATH4}
    assert by_sig[PATH4]==Counter({q:4*q**3})
    expected_counts={
      (1,1,2,2,3,4):8*q**4,
      (1,1,2,3,3,4):8*q**4,
      (1,1,3,3,4,4):2*q**4,
      (1,2,2,3,3,3):4*q**4,
      (1,2,2,3,3,4):8*q**4,
      (2,2,2,2,4,4):q**4}
    for sig,c in expected_counts.items():assert by_sig[sig]==Counter({1:c})
    assert not any(len(H)>1 for H in by_sig.values())
    assert hist[q]==4*q**3 and hist[1]==31*q**4
    return {
      'q':q,'chambers':len(G['flags']),'apartments_through_base':len(containing),
      'rooted_nonzero_quadruples':len(counts),
      'common_apartment_histogram':{str(k):v for k,v in sorted(hist.items())},
      'distance_signature_classes':len(by_sig),
      'distance_signature_nonconstant_classes':{},
      'distance_signature_table':{str(sig):{str(k):v for k,v in sorted(H.items())} for sig,H in sorted(by_sig.items())}}


def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={
      'pass':5159,'status':'THEOREM_ALL_Q_FOUR_CHAMBER_STAR_INTERSECTION_LAW',
      'law':{
        str(PATH4):'q',
        '(1,1,2,2,3,4)':'1','(1,1,2,3,3,4)':'1','(1,1,3,3,4,4)':'1',
        '(1,2,2,3,3,3)':'1','(1,2,2,3,3,4)':'1','(2,2,2,2,4,4)':'1',
        'all_other_six_distance_signatures':'0'},
      'geometric_proof':'An apartment is an induced C8 in the Levi graph. Up to dihedral symmetry, four distinct cycle edges have exactly seven sorted six-distance signatures. Six patterns contain enough alternating point-line incidence data to determine the full C8 uniquely. The consecutive-four-edge pattern (1,1,1,2,2,3) leaves one generalized-quadrangle projection choice; exactly q completions avoid the already fixed incidence, giving q apartments. Any other six-distance signature cannot embed in C8.',
      'rooted_multiplicities':{
        str(PATH4):'4 q^3 quadruples, each with q common apartments',
        '(1,1,2,2,3,4)':'8 q^4','(1,1,2,3,3,4)':'8 q^4','(1,1,3,3,4,4)':'2 q^4',
        '(1,2,2,3,3,3)':'4 q^4','(1,2,2,3,3,4)':'8 q^4','(2,2,2,2,4,4)':'q^4'},
      'anchors':A,
      'connection':'This is the exact fourth-order chamber-star coefficient beyond Pass5140. It can be inserted into degree-four parity minorants without re-enumerating apartments.',
      'boundary':'The law is all-q, but no q5 minimum-distance theorem follows automatically; a fourth-order parity attack still needs a lower bound on how many selected chamber quadruples realize the nonzero signatures.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
