#!/usr/bin/env python3
"""Export the deterministic q=3 chart-sharing graph and chart coordinates for Pass5176."""
from __future__ import annotations
import itertools,sys
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W

PAIRS=list(itertools.combinations(range(4),2))

def main(path='/tmp/w33_pass5176_q3_graph.txt'):
    G=build_W(3);coords=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    n=len(G['apartments']);adj=[set() for _ in range(n)]
    for C in coords:
        for a,b in itertools.combinations(C,2):adj[a].add(b);adj[b].add(a)
    assert n==1620 and len(coords)==1080 and {len(A) for A in adj}=={20}
    p=Path(path)
    with p.open('w') as f:
        f.write(f'{n} {len(coords)}\n')
        for A in adj:f.write(' '.join(map(str,sorted(A)))+'\n')
        for C in coords:f.write(' '.join(map(str,C))+'\n')
    print(p)

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else '/tmp/w33_pass5176_q3_graph.txt')
