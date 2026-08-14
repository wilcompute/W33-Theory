#!/usr/bin/env python3
"""Pass5148 (outside box): two root statistics govern derivative volume and memory depth."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5148_ROOT_VOLUME_DEPTH_CALCULUS.json'

def main():
    rows=[]
    for typ,heights in [('A2',[1,1,2]),('C2',[1,1,2,3]),('G2',[1,1,2,3,4,5])]:
        N=len(heights);H=sum(heights)
        rows.append({'type':typ,'positive_root_heights':heights,'N_positive_roots':N,'height_sum':H,
                     'big_cell_volume':'q^%d'%N,'formal_root_derivative':'%d q^%d'%(N,N-1),
                     'safe_Jennings_top_degree':'(p-1)*%d'%H})
    assert [(r['N_positive_roots'],r['height_sum']) for r in rows]==[(3,4),(4,7),(6,16)]
    out={'pass':5148,'status':'THEOREM_ROOT_VOLUME_DEPTH_TWO_STATISTICS',
         'rows':rows,
         'volume_law':'N=|Phi+| controls |U(q)|=q^N and the total first root-coset count N q^(N-1).',
         'depth_law':'H=sum_{alpha>0} ht(alpha) controls the top Jennings degree (p-1)H in the p>h safe range.',
         'C2_user_derivative':'For C2, N=4 gives q^4 -> 4q^3, while H=7 gives the independent augmentation-depth scale 7(p-1).',
         'synthesis':'The derivative count and memory filtration are two distinct statistics of the same positive-root poset: cardinality versus total height.',
         'boundary':'This is finite Lie algebra/group-algebra structure. It is not a continuous derivative in field size and not a claim about physical clock latency.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
