#!/usr/bin/env python3
"""Pass5077: q=5 exact pair shell plus bounded multistar distance falsifier."""
import random,json
from collections import Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS5077_Q5_DISTANCE_SEARCH.json'

def main():
    G=build_W(5);stars=chamber_stars(G);n=len(stars);assert n==936 and all(z.bit_count()==625 for z in stars)
    h=Counter();mn=10**9
    for i in range(n):
        for j in range(i+1,n):
            w=(stars[i]^stars[j]).bit_count();h[w]+=1;mn=min(mn,w)
    rng=random.Random(5077);best=625;bestset=[0];starts=200
    for s in range(starts):
        if s==0:curset={0};cur=stars[0]
        else:
            k=rng.randint(2,12);curset=set(rng.sample(range(n),k));cur=0
            for i in curset:cur^=stars[i]
        for _ in range(1200):
            i=rng.randrange(n);nxt=cur^stars[i];w=nxt.bit_count();cw=cur.bit_count()
            if w and (w<cw or rng.random()<0.002):
                cur=nxt
                if i in curset:curset.remove(i)
                else:curset.add(i)
                if w<best:best=w;bestset=sorted(curset)
            if best<625:break
        if best<625:break
    out={'pass':5077,'status':'PASS_BOUNDED_Q5_SEARCH','code_from_5066':[73125,625],
         'candidate_upper_bound':625,'exact_two_star_minimum':mn,'exact_two_star_weight_hist':dict(sorted(h.items())),
         'pair_intersections':[625-w//2 for w in sorted(h)],
         'heuristic_starts':starts,'heuristic_steps_per_start':1200,'best_nonzero_weight_found':best,'best_generator_count':len(bestset),
         'falsified_d_q4':best<625,'boundary':'No q=5 minimum-distance proof: exact <=2-star shell plus bounded seeded local descent only.'}
    assert mn==1000 and best==625
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
