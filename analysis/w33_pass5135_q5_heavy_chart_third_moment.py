#!/usr/bin/env python3
"""Pass5135: third local moment of the q=5 weight-625 heavy-chart shell.

For a local K6 cut with bipartition size s, selected apartments are edges of
K_{s,6-s}.  In the local theta line graph, the number of selected triangles is
sum_v C(deg(v),3), giving 10,8,6 for local weights 5,8,9.  Combining this with
Pass5127's coarea equation quantizes the third-moment defect of an exotic
minimum shell.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5135_Q5_HEAVY_CHART_THIRD_MOMENT.json'

def local(s):
    r=6-s;w=s*r
    tri=s*math.comb(r,3)+r*math.comb(s,3)
    return w,tri

def main():
    loc={s:local(s) for s in (1,2,3)}
    assert loc=={1:(5,10),2:(8,8),3:(9,6)}
    sols=[]
    for h8 in range(20):
      for h9 in range(20):
        if h8==h9==0:continue
        defect=3*h8+4*h9
        if defect%5:continue
        A=250-defect//5
        T=10*(A-h8-h9)+8*h8+6*h9
        D=2500-T
        sols.append((D,h8,h9,A,T))
    sols.sort()
    assert sols[0]==(28,2,1,248,2472)
    out={'pass':5135,'status':'THEOREM_Q5_MINIMUM_SHELL_THIRD_MOMENT_QUANTIZATION',
      'q':5,'weight':625,
      'local_cut_types':{'weight5':{'partition':'1+5','theta_star_triangles':10},'weight8':{'partition':'2+4','theta_star_triangles':8},'weight9':{'partition':'3+3','theta_star_triangles':6}},
      'coarea_equation':'5 A_type + 3 h8 + 4 h9 = 1250',
      'third_moment_formula':'T_type = 10 A_type - 2 h8 - 4 h9 = 2500 - 8 h8 - 12 h9',
      'minimal_nonzero_defect':{'h8':2,'h9':1,'active_charts_type':248,'third_moment':2472,'defect_from_chamber_star_type':28},
      'conclusion':'Any exotic q5 weight-625 shell has, on at least one point/line chart type, a third local theta-triangle moment defect of at least 28; the unique smallest defect is the Pass5127 profile (h8,h9)=(2,1).',
      'boundary':'This is a necessary moment constraint. It does not yet prove that the (2,1) profile is globally impossible.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
