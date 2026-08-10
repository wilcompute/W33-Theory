#!/usr/bin/env python3
"""Pass 4693 -- exact support-12 apartment-code spectrum using coefficient transitivity.

Let A_w be the number of 12-subsets of the 40 apartment-code generators whose
XOR has weight w.  Aut(C)=PGSp(4,3) is transitive on the 40 generator positions.
If B_w counts only such subsets containing generator 0, double counting
incidences (S,i) gives

    12 A_w = 40 B_w, hence A_w = (10/3) B_w.

Therefore the exact support-12 shell requires only C(39,11)=1,676,056,044
fixed-point subsets, fewer than the already completed support-11 census.  A
native in-place XOR/popcount kernel exhausts that fixed-point shell.  Every B_w
is divisible by three; rescaling gives total C(40,12)=5,586,853,480, with 151
distinct weights, minimum 608 (1620 subsets), maximum 990 (4320 subsets).
"""
from __future__ import annotations
import json,math,subprocess,tempfile
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4693_SUPPORT12_TRANSITIVITY_EXACT.json'

def row_words(H):
    out=[]
    for i in range(40):
        a=[]
        for b in range(26):
            x=0
            for k in range(64):
                j=64*b+k
                if j<1620 and H[i,j]:x|=1<<k
            a.append(x)
        out.append(a)
    return out

def source(rows):
    body=',\n'.join('  {'+','.join(str(x)+'ULL' for x in r)+'}' for r in rows)
    return r'''#include <bits/stdc++.h>
using namespace std; static uint64_t R[40][26]={ROWS}; static unsigned long long C[1621]; static uint64_t a[26];
inline void xr(int v){for(int j=0;j<26;j++)a[j]^=R[v][j];}
void rec(int start,int need){if(!need){int w=0;for(int j=0;j<26;j++)w+=__builtin_popcountll(a[j]);C[w]++;return;}int mx=40-need;for(int v=start;v<=mx;v++){xr(v);rec(v+1,need-1);xr(v);}}
int main(){for(int j=0;j<26;j++)a[j]=R[0][j];rec(1,11);bool q=0;cout<<"{";for(int w=0;w<=1620;w++)if(C[w]){if(q)cout<<",";q=1;cout<<"\\\""<<w<<"\\\":"<<C[w];}cout<<"}\n";}
'''.replace('ROWS',body)

def run_fixed_point():
    *_,H=geometry();rows=row_words(H)
    with tempfile.TemporaryDirectory() as d:
        p=Path(d);(p/'x.cpp').write_text(source(rows),encoding='utf-8')
        subprocess.run(['g++','-O3','-march=native','-funroll-loops',str(p/'x.cpp'),'-o',str(p/'x')],check=True)
        s=subprocess.check_output([str(p/'x')],text=True).strip()
    return Counter({int(k):int(v) for k,v in json.loads(s).items()})

def main()->int:
    B=run_fixed_point();assert sum(B.values())==math.comb(39,11)==1676056044
    assert all(v%3==0 for v in B.values())
    A=Counter({w:(v//3)*10 for w,v in B.items()})
    assert sum(A.values())==math.comb(40,12)==5586853480
    assert len(A)==151 and min(A)==608 and max(A)==990 and A[608]==1620 and A[990]==4320
    out={'pass':4693,'support':12,'transitivity_reduction':{'group':'Aut(C)=PGSp(4,3)','coefficient_positions':40,'fixed_position':0,'identity':'12 A_w = 40 B_w','scale':'A_w=(10/3)B_w','fixed_point_subsets':sum(B.values()),'all_fixed_point_counts_divisible_by_3':True},'subsets':sum(A.values()),'distinct_weights':len(A),'minimum_weight':min(A),'minimum_count':A[min(A)],'maximum_weight':max(A),'maximum_count':A[max(A)],'spectrum':{str(k):v for k,v in sorted(A.items())},'new_exact_frontier':'complete labelled support spectra are now known through support 12','theorem':'Coefficient transitivity reduces the exact support-12 census from C(40,12) to C(39,11) fixed-point subsets.  Exhaustive native XOR/popcount accumulation and the 12A=40B double count give the complete 151-weight support-12 spectrum with exact total 5,586,853,480.','boundary':'The full [1620,39,162] numerical enumerator remains OPEN; supports 13..20 have not all been accumulated.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='spectrum'},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
