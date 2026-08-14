#!/usr/bin/env python3
"""Pass5076: exact q=4 chamber-star shell through three generators."""
import json,time
from collections import Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS5076_Q4_LOW_GENERATOR_SHELL.json'

def main():
    G=build_W(4);S=chamber_stars(G);n=len(S);assert n==425
    ph=Counter();pairmin=10**9
    for i in range(n):
        for j in range(i+1,n):
            w=(S[i]^S[j]).bit_count();ph[w]+=1;pairmin=min(pairmin,w)
    th=Counter();trimin=10**9;triarg=None;t0=time.time()
    for i in range(n-2):
        for j in range(i+1,n-1):
            z=S[i]^S[j]
            for k in range(j+1,n):
                w=(z^S[k]).bit_count();th[w]+=1
                if w<trimin:trimin=w;triarg=(i,j,k)
    out={'pass':5076,'status':'PASS_EXACT_LOW_GENERATOR_SHELL','q':4,'code':[13600,256,256],
         'one_generator_weight':256,'two_generator_min':pairmin,'two_generator_hist':dict(sorted(ph.items())),
         'three_generator_min':trimin,'three_generator_min_example':triarg,'three_generator_hist':dict(sorted(th.items())),
         'elapsed_seconds':time.time()-t0,
         'consequence':'Any non-chamber-star weight-256 word, if one exists, has no representation using <=3 distinct chamber-star generators.',
         'boundary':'Not a complete shell classification because the 425 stars have a 169-dimensional dependency kernel.'}
    assert pairmin==trimin==384
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
