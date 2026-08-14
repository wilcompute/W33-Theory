#!/usr/bin/env python3
"""Pass5159: rooted four-chamber apartment-intersection census for q=2,3,4,5.

Pass5140 gives the complete triple-star law.  This producer computes the next
coefficient directly from apartments, but only through one base chamber; chamber
transitivity makes that sufficient for rooted quadruples.  It deliberately does
not assume that the six pairwise gallery distances classify a quadruple orbit:
if one distance signature has multiple common-apartment counts, the certificate
records that failure instead of collapsing it.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5159_ALLQ_FOUR_CHAMBER_INTERSECTION_CENSUS.json'


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
        for abc in itertools.combinations(rest,3):
            counts[(base,)+tuple(sorted(abc))]+=1
    # Every nonzero rooted quadruple is generated once from each common apartment.
    by_sig=defaultdict(Counter);hist=Counter()
    for Q,c in counts.items():
        ds=[]
        for a,b in itertools.combinations(Q,2):ds.append(pair_dist(q,S,a,b))
        sig=tuple(sorted(ds));by_sig[sig][c]+=1;hist[c]+=1
    nonconstant={str(sig):{str(k):v for k,v in sorted(H.items())}
                 for sig,H in sorted(by_sig.items()) if len(H)>1}
    return {
      'q':q,'chambers':len(G['flags']),'apartments_through_base':len(containing),
      'rooted_nonzero_quadruples':len(counts),
      'common_apartment_histogram':{str(k):v for k,v in sorted(hist.items())},
      'distance_signature_classes':len(by_sig),
      'distance_signature_nonconstant_classes':nonconstant,
      'distance_signature_table':{
        str(sig):{str(k):v for k,v in sorted(H.items())} for sig,H in sorted(by_sig.items())}
    }


def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={
      'pass':5159,'status':'EXACT_ROOTED_FOUR_CHAMBER_INTERSECTION_CENSUS',
      'anchors':A,
      'statement':'For q=2,3,4,5 this file exhausts every chamber quadruple containing a fixed base chamber that occurs in at least one apartment and records its exact common-apartment count and six-distance signature.',
      'promotion_rule':'An all-q distance-signature law may be promoted only if the signature classes are constant in all anchors and a separate C8/generalized-quadrangle completion proof is supplied.',
      'boundary':'This producer is an exact finite census, not by itself an all-q theorem and not a q5 distance proof.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
