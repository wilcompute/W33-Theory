#!/usr/bin/env python3
"""Pass5084: q=4 four-star shell and complete minimum dependency shell.

Every four-star subset can be moved so one member is star 0.  Enumerating all
C(424,3) remaining triples therefore meets every four-star orbit.  The only
weight-256 outputs are other chamber stars; adjoining that target gives a
five-star zero relation.  The two such relations through a fixed chamber are
exactly its point-panel and line-panel relations.  Transitivity then gives all
170=85+85 weight-five kernel words.  Pass5076 and this census exclude kernel
weights <=4, so the 169-dimensional chamber-generator kernel has distance 5.
"""
from collections import Counter
import itertools,json,math
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5084_Q4_FOUR_STAR_SHELL.json'

def main():
    G=build_W(4);stars=chamber_stars(G);assert len(stars)==425 and all(z.bit_count()==256 for z in stars)
    star_index={z:i for i,z in enumerate(stars)};assert len(star_index)==425
    base=stars[0];h=Counter();mn=10**9;arg=None;tested=0;minimum_targets=Counter();minimum_reps=[];fixed_deps=set()
    for i,j,k in itertools.combinations(range(1,len(stars)),3):
        z=base^stars[i]^stars[j]^stars[k];w=z.bit_count();h[w]+=1;tested+=1
        if w<mn:mn=w;arg=[0,i,j,k]
        if w==256:
            target=star_index.get(z,-1);minimum_targets[target]+=1
            if target>=0:fixed_deps.add(frozenset((0,i,j,k,target)))
            if len(minimum_reps)<20:minimum_reps.append({'summands':[0,i,j,k],'target_chamber_star':target})
    assert tested==math.comb(424,3) and mn==256
    assert -1 not in minimum_targets and sum(minimum_targets.values())==h[256]==8 and len(fixed_deps)==2
    # The geometric panel relations: five chambers/flags incident to each point or line.
    point_panels={frozenset(i for i,(p,l) in enumerate(G['flags']) if p==p0) for p0 in range(len(G['pts']))}
    line_panels={frozenset(i for i,(p,l) in enumerate(G['flags']) if l==l0) for l0 in range(len(G['lines']))}
    panels=point_panels|line_panels;assert len(panels)==170 and set(map(len,panels))=={5}
    through0={P for P in panels if 0 in P};assert fixed_deps==through0 and len(through0)==2
    for P in panels:
        z=0
        for i in P:z^=stars[i]
        assert z==0
    out={'pass':5084,'status':'THEOREM_Q4_FOUR_STAR_AND_KERNEL_SHELL','q':4,'stars':425,'generator_rank':256,'generator_kernel_dimension':169,
         'fixed_star':0,'representatives_tested':tested,'minimum_four_star_weight':mn,'minimum_witness':arg,
         'weight_histogram':dict(sorted(h.items())),'weight256_four_star_representatives':h[256],'weight256_nonstar_targets':0,
         'minimum_target_histogram':{str(k):v for k,v in sorted(minimum_targets.items())},'minimum_examples':minimum_reps,
         'five_star_dependencies_through_fixed_chamber':len(fixed_deps),'global_weight5_dependencies':170,
         'dependency_identification':'85 point panels + 85 line panels','generator_kernel_minimum_distance':5,
         'consequence':'Every four-star weight-256 representative is itself a chamber star. Any exotic q=4 minimum codeword requires at least five distinct chamber stars in every literal representation; separately, the chamber-generator dependency code has complete minimum shell equal to the 170 panel relations.',
         'boundary':'This does not classify arbitrary q=4 weight-256 codewords beyond the <=4-star representation wall.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
