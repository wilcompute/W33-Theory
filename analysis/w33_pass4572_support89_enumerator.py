#!/usr/bin/env python3
"""Pass 4572 -- execute the W33 apartment enumerator through full supports 8 and 9.

Pass4520 exhaustively evaluated labelled coefficient supports through m=7. Pass4546
then supplied an exact symmetry-orbit engine but intentionally did not claim its
10,789,604-orbit full run had executed.

This pass advances the *executed* numerical frontier without relying on nauty. It
builds the forty 1620-bit apartment-incidence rows from the canonical W33 geometry,
generates an optimized fixed-weight C++ XOR/popcount kernel, and exhausts every
labelled coefficient subset at supports 8 and 9. Consecutive lexicographic
combinations update only the changed suffix of the 1620-bit XOR word.

Exact evaluated mass:
  C(40,8) =  76,904,685 subsets,
  C(40,9) = 273,438,880 subsets,
  total    = 350,343,565 newly evaluated labelled subsets.

The resulting complete support-8 and support-9 weight spectra are frozen in the
Pass4572 JSON certificate. The complete [1620,39] enumerator remains OPEN because
supports 10..20 have not all been accumulated and the 2^39 checksum has not run.
"""
from __future__ import annotations

import json,subprocess,tempfile
from pathlib import Path

from w33_pass4495_4502_distance_prism_reconstruction import geometry

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4572_SUPPORT89_ENUMERATOR.json'


def row_chunks():
    pts,pidx,lines,A,apartments,apmasks,H=geometry();assert H.shape==(40,1620)
    rows=[]
    for i in range(40):
        ch=[0]*26
        for j,b in enumerate(H[i]):
            if b:ch[j//64]|=1<<(j%64)
        assert sum(x.bit_count() for x in ch)==162;rows.append(ch)
    return rows


def cpp_source(rows):
    R=',\n'.join('{'+','.join(f'0x{x:016x}ULL' for x in row)+'}' for row in rows)
    return f'''#include <bits/stdc++.h>\nusing namespace std;\nstatic const unsigned long long R[40][26]={{\n{R}\n}};\nint main(int argc,char**argv){{\n int m=atoi(argv[1]); map<int,unsigned long long> cnt; unsigned long long total=0;\n vector<int> c(m); for(int i=0;i<m;i++)c[i]=i; unsigned long long w[26]={{0}};\n for(int a=0;a<m;a++)for(int k=0;k<26;k++)w[k]^=R[c[a]][k];\n while(true){{\n   int wt=0; for(int k=0;k<26;k++)wt+=__builtin_popcountll(w[k]); cnt[wt]++; total++;\n   int i=m-1; while(i>=0 && c[i]==40-m+i)i--; if(i<0)break;\n   for(int j=i;j<m;j++)for(int k=0;k<26;k++)w[k]^=R[c[j]][k];\n   c[i]++; for(int j=i+1;j<m;j++)c[j]=c[j-1]+1;\n   for(int j=i;j<m;j++)for(int k=0;k<26;k++)w[k]^=R[c[j]][k];\n }}\n cerr<<"total "<<total<<"\\n"; for(auto &kv:cnt)cout<<kv.first<<" "<<kv.second<<"\\n";\n}}\n'''


def run_support(exe,m):
    p=subprocess.run([str(exe),str(m)],check=True,text=True,capture_output=True)
    spec={}
    for line in p.stdout.splitlines():
        if line.strip():
            w,n=map(int,line.split());spec[w]=n
    return spec


def main()->int:
    rows=row_chunks()
    with tempfile.TemporaryDirectory(prefix='w33_pass4572_') as td:
        td=Path(td);src=td/'census.cpp';exe=td/'census';src.write_text(cpp_source(rows),encoding='utf-8')
        subprocess.run(['g++','-O3','-march=native',str(src),'-o',str(exe)],check=True)
        s8=run_support(exe,8);s9=run_support(exe,9)
    assert sum(s8.values())==76904685 and (min(s8),max(s8))==(528,960) and s8[528]==540 and s8[960]==1755
    assert sum(s9.values())==273438880 and (min(s9),max(s9))==(582,1026) and s9[582]==4320 and s9[1026]==360
    out={
      'pass':4572,'status':'EXACT_SUPPORT_8_9_COMPLETE_FULL_ENUMERATOR_OPEN',
      'prior_frontier':'Pass4520 exact labeled support census ended at support 7',
      'new_exact_labeled_subsets':sum(s8.values())+sum(s9.values()),
      'support8':{'subsets':sum(s8.values()),'weights':len(s8),'minimum_weight':min(s8),'maximum_weight':max(s8),
                  'spectrum':{str(k):v for k,v in s8.items()}},
      'support9':{'subsets':sum(s9.values()),'weights':len(s9),'minimum_weight':min(s9),'maximum_weight':max(s9),
                  'spectrum':{str(k):v for k,v in s9.items()}},
      'full_enumerator':'OPEN: support 10..20 orbit/weight accumulation remains',
      'boundary':'Exact labeled support spectra, not the full [1620,39] numerical enumerator. No 2^39 checksum is claimed.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('support8','support9')},indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
