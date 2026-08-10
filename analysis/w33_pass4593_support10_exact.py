#!/usr/bin/env python3
"""Pass 4593 -- exact support-10 apartment-code spectrum.

Pass4572 completed labelled support 8 and 9 by direct XOR/popcount.  This pass
closes support 10.  It rebuilds the 40x1620 apartment incidence matrix, emits a
small native C++ fixed-weight XOR/popcount kernel, compiles it with g++, and
splits the support-10 census by the least selected row.  Every 10-subset occurs
exactly once.  Acceptance is the exact C(40,10)=847,660,528 mass checksum plus
the frozen 147-weight spectrum.

This is still not the complete 2^39 code enumerator: supports 11..20 remain.
"""
from __future__ import annotations
import itertools,json,math,subprocess,tempfile
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4593_SUPPORT10_EXACT.json'

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
using namespace std; static uint64_t R[40][26]={ROWS}; static unsigned long long C[1621];
void rec(int start,int need,uint64_t *a){ if(!need){int w=0;for(int j=0;j<26;j++)w+=__builtin_popcountll(a[j]);C[w]++;return;} int mx=40-need; for(int v=start;v<=mx;v++){uint64_t z[26];for(int j=0;j<26;j++)z[j]=a[j]^R[v][j];rec(v+1,need-1,z);}}
int main(int argc,char**argv){int lo=atoi(argv[1]),hi=atoi(argv[2]);uint64_t a[26];for(int f=lo;f<hi;f++){if(39-f<9)continue;for(int j=0;j<26;j++)a[j]=R[f][j];rec(f+1,9,a);}bool q=0;cout<<"{";for(int w=0;w<=1620;w++)if(C[w]){if(q)cout<<",";q=1;cout<<"\\\""<<w<<"\\\":"<<C[w];}cout<<"}\n";}
'''.replace('ROWS',body)

def run():
    *_,H=geometry(); rows=row_words(H)
    with tempfile.TemporaryDirectory() as d:
        p=Path(d);(p/'x.cpp').write_text(source(rows))
        subprocess.run(['g++','-O3','-march=native','-funroll-loops',str(p/'x.cpp'),'-o',str(p/'x')],check=True)
        total=Counter()
        # largest least-element shard (f=0) is separated from the rest.
        for lo,hi in [(0,1),(1,31)]:
            s=subprocess.check_output([str(p/'x'),str(lo),str(hi)],text=True).strip()
            total.update({int(k):int(v) for k,v in json.loads(s).items()})
    return total

def main():
    c=run();assert sum(c.values())==math.comb(40,10)==847660528
    assert len(c)==147 and min(c)==582 and max(c)==1080 and c[582]==2160 and c[1080]==36
    out={'pass':4593,'support':10,'subsets':sum(c.values()),'distinct_weights':len(c),'minimum_weight':min(c),'minimum_count':c[min(c)],'maximum_weight':max(c),'maximum_count':c[max(c)],'spectrum':{str(k):v for k,v in sorted(c.items())},'new_exact_frontier':'complete labelled support spectra are now known through support 10','boundary':'The full [1620,39,162] numerical enumerator remains OPEN; supports 11..20 have not all been accumulated.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='spectrum'},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
