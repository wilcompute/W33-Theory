#!/usr/bin/env python3
"""Pass5080: q=2 complete enumerator and Fourier-gauge extremal certificate."""
import json
from collections import Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS5080_FOURIER_GAUGE_Q2.json'

def independent(rows):
    piv={};keep=[]
    for i,r0 in enumerate(rows):
        r=r0
        while r:
            p=r.bit_length()-1
            if p in piv:r^=piv[p]
            else:piv[p]=r;keep.append(i);break
    return keep

def main():
    G=build_W(2);stars=chamber_stars(G);K=independent(stars);assert len(K)==16;B=[stars[i] for i in K]
    h=Counter({0:1});cur=0
    for t in range(1,1<<16):
        g=t^(t>>1);pg=(t-1)^((t-1)>>1);flip=(g^pg).bit_length()-1;cur^=B[flip];h[cur.bit_count()]+=1
    assert h[16]==45 and len(set(stars))==45
    out={'pass':5080,'status':'PASS','q2_code':[90,16,16],'weight_enumerator':dict(sorted(h.items())),
         'minimum_words':h[16],'chamber_stars':45,'nonstar_minimum_words':h[16]-45,
         'apartment_measure_edge_fourier':'1-16/45=29/45',
         'distance_fourier_equivalence':'wt(c_y)=N_A*(1-muhat(y))/2; d=q^4 iff max_nontrivial muhat <= 1-16/((q+1)^2(q^2+1))'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
