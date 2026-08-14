#!/usr/bin/env python3
"""Pass5084: exact q=4 four-chamber-star shell modulo chamber transitivity.

Every four-star subset can be moved so one member is star 0.  Enumerating all
C(424,3) remaining triples therefore meets every four-star orbit and determines
the global minimum over literal four-star sums.  It is not a complete code-shell
classification because the 425 chamber generators have a 169-dimensional kernel.
"""
from collections import Counter
import itertools,json,math
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5084_Q4_FOUR_STAR_SHELL.json'

def main():
    G=build_W(4);stars=chamber_stars(G);assert len(stars)==425 and all(z.bit_count()==256 for z in stars)
    base=stars[0];h=Counter();mn=10**9;arg=None;tested=0
    for i,j,k in itertools.combinations(range(1,len(stars)),3):
        w=(base^stars[i]^stars[j]^stars[k]).bit_count();h[w]+=1;tested+=1
        if w<mn:mn=w;arg=[0,i,j,k]
    assert tested==math.comb(424,3)
    out={'pass':5084,'status':'PASS','q':4,'stars':425,'fixed_star':0,'representatives_tested':tested,
         'minimum_four_star_weight':mn,'minimum_witness':arg,'weight_histogram':dict(sorted(h.items())),
         'minimum_256_found':mn==256,
         'consequence':('A weight-256 word may have a four-star representation.' if mn==256 else 'No weight-256 word has a representation by four distinct chamber stars; combined with Pass5076 any exotic minimum needs at least five distinct stars in every literal representation.'),
         'boundary':'Orbit-complete for exactly four distinct chamber-star summands only; not a complete q=4 minimum-shell classification.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
