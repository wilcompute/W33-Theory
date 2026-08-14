#!/usr/bin/env python3
"""Pass5140 (bonkers): exact third-order chamber-star intersection census at q=5.

Pass5134 proves pairwise information is insufficient at leader 18.  This pass
materializes the next required object: for all triples containing a fixed
chamber star, count |S0 cap Si cap Sj| and classify it by the three chamber
pair gallery distances, inferred from the exact q^(4-d) pair-intersection law.
Chamber transitivity makes this a complete rooted orbit census of triple
intersection sizes (though not necessarily a complete orbit classification).
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5140_Q5_TRIPLE_CHAMBER_STAR_CENSUS.json'

def dist_from_inter(q,w):
    for d in range(1,5):
        if w==q**(4-d):return d
    raise AssertionError((q,w))

def main():
    q=5;G=build_W(q);S=chamber_stars(G);n=len(S);base=S[0]
    d0=[0]*n
    for i in range(1,n):d0[i]=dist_from_inter(q,(base&S[i]).bit_count())
    hist=Counter();by_sig=defaultdict(Counter);pair_hist=Counter();positive=0
    for i,j in itertools.combinations(range(1,n),2):
        wij=(S[i]&S[j]).bit_count();dij=dist_from_inter(q,wij)
        sig=tuple(sorted((d0[i],d0[j],dij)))
        t=(base&S[i]&S[j]).bit_count()
        hist[t]+=1;by_sig[sig][t]+=1;pair_hist[sig]+=1
        if t:positive+=1
    assert sum(hist.values())==(n-1)*(n-2)//2
    vals=sorted(hist)
    out={'pass':5140,'status':'EXACT_Q5_ROOTED_TRIPLE_INTERSECTION_CENSUS','q':q,
      'chambers':n,'fixed_base_triples':sum(hist.values()),
      'triple_intersection_histogram':{str(k):hist[k] for k in vals},
      'positive_triples':positive,'intersection_values':vals,
      'by_sorted_gallery_distance_signature':{
        str(sig):{str(k):v for k,v in sorted(H.items())} for sig,H in sorted(by_sig.items())},
      'statement':'For every unordered pair of nonbase chambers, the certificate records the exact number of apartments containing all three chambers, together with the sorted gallery-distance triangle of the three chamber pairs.',
      'connection':'This is the third-order chamber-star data requested by the Pass5134 m=18 wall; it can be inserted into parity inclusion-exclusion / LP constraints beyond pairwise Delsarte.',
      'boundary':'A fixed-base census is complete by chamber transitivity for rooted triples, but distance signature need not equal a full automorphism orbit. This pass does not yet solve the m=18 q5 optimization.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
