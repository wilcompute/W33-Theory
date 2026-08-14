#!/usr/bin/env python3
"""Pass5127: q=5 coarea/heavy-chart defect quantization at weight 625."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5127_Q5_COAREA_DEFECT_QUANTIZATION.json'

def solutions(maxh=40):
    rows=[]
    for h8 in range(maxh+1):
      for h9 in range(maxh+1):
        d=3*h8+4*h9
        if d%5==0 and d<=1250:
            A=250-d//5
            if A>=h8+h9:rows.append((d//5,h8,h9,A))
    return sorted(rows)

def main():
    R=solutions();heavy=[r for r in R if r[1]+r[2]>0]
    mind=min(r[0] for r in heavy);mins=[r for r in heavy if r[0]==mind]
    assert mind==2 and mins==[(2,2,1,248)]
    out={'pass':5127,'status':'THEOREM_Q5_MINIMUM_COAREA_DEFECT_QUANTIZATION',
         'q':5,'word_weight':625,
         'coarea_identity':'For each chart type P or L separately, sum local cut weights = 2 wt = 1250.',
         'local_K6_cut_weights':[5,8,9],
         'equation':'5 A_type + 3 h8 + 4 h9 = 1250, equivalently 5(250-A_type)=3h8+4h9.',
         'congruence':'3 h8 + 4 h9 == 0 mod 5.',
         'smallest_nonzero_defect':{'active_chart_deficit':2,'h8':2,'h9':1,'A_type':248,'heavy_charts':3},
         'consequence':'Any weight-625 nonstar word, which by the minimum-cut rigidity theorem must contain a heavy K6 chart, actually contains at least three heavy charts in one point/line type and has total active-chart count <=498 rather than the star value 500.',
         'boundary':'This quantizes the exotic equality shell but does not rule it out; q5 d=625 remains open for leader >=18.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
