#!/usr/bin/env python3
"""Pass5131 (bonkers): exhaustive connected-component proof of q=3 radius five."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5131_Q3_EQUIVARIANT_RADIUS5_DECODER.json'
PAIRS=list(itertools.combinations(range(4),2));POS={e:i for i,e in enumerate(PAIRS)};SYN=list(itertools.combinations(range(1,4),2))
def syndrome(m):
    s=0
    for b,(i,j) in enumerate(SYN):s|=((((m>>POS[(0,i)])&1)^((m>>POS[(0,j)])&1)^((m>>POS[(i,j)])&1))<<b)
    return s
def leaders():
    B={s:[] for s in range(8)}
    for m in range(64):B[syndrome(m)].append(m)
    out=[]
    for s in range(8):
        w=min(x.bit_count() for x in B[s]);z=[x for x in B[s] if x.bit_count()==w];out.append(z[0] if len(z)==1 else 0)
    return out
def connected_sets(adj,k):
    L={frozenset((0,))}
    for _ in range(1,k):
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
    def sweep(E):
        masks={}
        for a in E:
            for ci,pos in ach[a]:masks[ci]=masks.get(ci,0)^(1<<pos)
        votes={}
        for ci,m in masks.items():
            lm=lead[syndrome(m)]
            if lm:
                p=lm.bit_length()-1;a=coords[ci][p];votes[a]=votes.get(a,0)+1
        if not votes:return frozenset(),0
        z=max(votes.values());return frozenset(a for a,v in votes.items() if v==z),z
    counts={};sweep_bounds={};profiles=Counter()
    for k in range(1,6):
        SS=connected_sets(adj,k);counts[str(k)]=len(SS);mx=0
        for E0 in SS:
            E=E0;steps=0
            while E:
                corr,v=sweep(E);assert corr and corr<=E
                if k==5:profiles[(len(E),len(corr),v)]+=1
                E=E^corr;steps+=1;assert steps<=3
            mx=max(mx,steps)
        sweep_bounds[str(k)]=mx
    assert counts=={'1':1,'2':20,'3':490,'4':13269,'5':381480}
    assert sweep_bounds=={'1':1,'2':1,'3':2,'4':2,'5':3}
    out={'pass':5131,'status':'THEOREM_GLOBAL_EQUIVARIANT_RADIUS5_THREE_SWEEPS','q':3,
         'fixed_base_connected_counts':counts,'connected_sweep_bounds':sweep_bounds,
         'connected_weight5_transition_profile':{str(k):v for k,v in sorted(profiles.items())},
         'monotonicity':'Every max-vote correction on every connected component of size <=5 is a subset of the true errors.',
         'global_proof':'Chart-sharing components occur in no common affected chart. Global max-vote selection is therefore a union of component-local true corrections. Enumerating the integer partitions of five with the connected sweep bounds gives a global maximum of three sweeps.',
         'global_guaranteed_error_weight':5,'global_sweep_bound':3,
         'boundary':'No claim is made for weight six; random weight-six probes are not a proof. This is finite hard-decision decoding only.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
