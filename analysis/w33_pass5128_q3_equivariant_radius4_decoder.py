#!/usr/bin/env python3
"""Pass5128: global q=3 equivariant decoder guarantee through weight four."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5128_Q3_EQUIVARIANT_RADIUS4_DECODER.json'
PAIRS=list(itertools.combinations(range(4),2));POS={e:i for i,e in enumerate(PAIRS)}
SYNPAIRS=list(itertools.combinations(range(1,4),2))

def syndrome(mask):
    s=0
    for b,(i,j) in enumerate(SYNPAIRS):
        v=((mask>>POS[(0,i)])&1)^((mask>>POS[(0,j)])&1)^((mask>>POS[(i,j)])&1);s|=v<<b
    return s

def leaders():
    by={s:[] for s in range(8)}
    for m in range(64):by[syndrome(m)].append(m)
    out=[]
    for s in range(8):
        w=min(x.bit_count() for x in by[s]);z=[x for x in by[s] if x.bit_count()==w]
        out.append(z[0] if len(z)==1 else 0)
    return out

def connected_sets(adj,root,k):
    L={frozenset((root,))}
    for size in range(1,k):
        N=set()
        for S in L:
            B=set()
            for v in S:B|=adj[v]
            for u in B-S:N.add(frozenset(set(S)|{u}))
        L=N
    return L

def main():
    G=build_W(3);n=len(G['apartments']);lead=leaders();coords=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    ach=[[] for _ in range(n)];adj=[set() for _ in range(n)]
    for ci,C in enumerate(coords):
        for pos,a in enumerate(C):ach[a].append((ci,pos))
        for a,b in itertools.combinations(C,2):adj[a].add(b);adj[b].add(a)
    assert {len(x) for x in adj}=={20}
    def sweep(err):
        masks={}
        for a in err:
            for ci,pos in ach[a]:masks[ci]=masks.get(ci,0)^(1<<pos)
        votes={}
        for ci,m in masks.items():
            lm=lead[syndrome(m)]
            if lm:
                pos=lm.bit_length()-1;a=coords[ci][pos];votes[a]=votes.get(a,0)+1
        if not votes:return frozenset(),0
        mv=max(votes.values());return frozenset(a for a,v in votes.items() if v==mv),mv
    counts={};profiles={}
    for k in range(1,5):
        SS=connected_sets(adj,0,k);counts[str(k)]=len(SS);P=Counter()
        for E0 in SS:
            E=E0;steps=0
            while E:
                corr,mv=sweep(E);assert corr and corr<=E
                P[(len(E),len(corr),mv)]+=1;E=E^corr;steps+=1;assert steps<=2 if k>=3 else steps<=1
        profiles[str(k)]={str(x):v for x,v in sorted(P.items())}
    assert counts=={'1':1,'2':20,'3':490,'4':13269}
    out={'pass':5128,'status':'THEOREM_GLOBAL_EQUIVARIANT_RADIUS4_THREE_SWEEPS',
         'q':3,'chart_sharing_degree':20,'fixed_base_connected_component_counts':counts,
         'connected_census_profiles':profiles,
         'monotonicity':'For every connected error component of size <=4, every max-vote correction is a subset of the true component; no false apartment is introduced.',
         'component_proof':'Different chart-sharing components occur in no common chart. Global max-vote selection therefore acts on one or more component-local true corrections. For weight four the only partitions are 4, 3+1, 2+2, 2+1+1, 1+1+1+1; the 3+1 case is the unique one needing up to three sweeps.',
         'global_guaranteed_error_weight':4,'global_sweep_bound':3,
         'boundary':'Finite hard-decision Hamming guarantee only. Weight five is handled separately by Pass5131; no optical-noise or fault-tolerance threshold is inferred.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
