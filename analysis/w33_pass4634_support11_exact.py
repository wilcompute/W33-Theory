#!/usr/bin/env python3
"""Pass 4634 -- exact labelled support-11 apartment-code spectrum.

This advances Pass4593 by evaluating every C(40,11)=2,311,801,440 eleven-row
coefficient subset.  A native XOR/popcount kernel is split by least selected row
and executed in parallel.  The result is checked against the frozen 153-weight
certificate.  Supports 12..20 remain open, so this is not a full enumerator claim.
"""
from __future__ import annotations
import json,math,subprocess,tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4634_SUPPORT11_EXACT.json'

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
void rec(int start,int need,uint64_t *a){if(!need){int w=0;for(int j=0;j<26;j++)w+=__builtin_popcountll(a[j]);C[w]++;return;}int mx=40-need;for(int v=start;v<=mx;v++){uint64_t z[26];for(int j=0;j<26;j++)z[j]=a[j]^R[v][j];rec(v+1,need-1,z);}}
int main(int argc,char**argv){int lo=atoi(argv[1]),hi=atoi(argv[2]);uint64_t a[26];for(int f=lo;f<hi;f++){if(39-f<10)continue;for(int j=0;j<26;j++)a[j]=R[f][j];rec(f+1,10,a);}bool q=0;cout<<"{";for(int w=0;w<=1620;w++)if(C[w]){if(q)cout<<",";q=1;cout<<"\\\""<<w<<"\\\":"<<C[w];}cout<<"}\n";}
'''.replace('ROWS',body)

def run():
    *_,H=geometry();rows=row_words(H)
    with tempfile.TemporaryDirectory() as d:
        p=Path(d);(p/'x.cpp').write_text(source(rows));subprocess.run(['g++','-O3','-march=native','-funroll-loops',str(p/'x.cpp'),'-o',str(p/'x')],check=True)
        ranges=[(0,1),(1,2),(2,4),(4,7),(7,11),(11,16),(16,22),(22,30)]
        def shard(r):
            s=subprocess.check_output([str(p/'x'),str(r[0]),str(r[1])],text=True).strip();return Counter({int(k):int(v) for k,v in json.loads(s).items()})
        with ThreadPoolExecutor(max_workers=len(ranges)) as ex:parts=list(ex.map(shard,ranges))
    total=Counter()
    for c in parts:total.update(c)
    return total

def main()->int:
    frozen=json.loads(OUT.read_text()) if OUT.exists() else None
    c=run();assert sum(c.values())==math.comb(40,11)==2311801440
    assert len(c)==153 and min(c)==614 and c[614]==12960 and max(c)==1026 and c[1026]==1080
    if frozen and 'spectrum' in frozen:assert {str(k):v for k,v in sorted(c.items())}==frozen['spectrum']
    out={'pass':4634,'support':11,'subsets':sum(c.values()),'distinct_weights':len(c),'minimum_weight':min(c),'minimum_count':c[min(c)],'maximum_weight':max(c),'maximum_count':c[max(c)],'spectrum':{str(k):v for k,v in sorted(c.items())},'new_exact_frontier':'complete labelled support spectra are now known through support 11','boundary':'The full [1620,39,162] numerical enumerator remains OPEN; supports 12..20 have not all been accumulated.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='spectrum'},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
