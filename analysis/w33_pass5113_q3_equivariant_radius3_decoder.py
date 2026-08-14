#!/usr/bin/env python3
"""Pass5113: q=3 equivariant local-vote decoder, global radius three.

Pass5086 used one arbitrary minimum leader for the unique ambiguous K4 syndrome.
Here the local rule is made S4-equivariant: six nonzero syndromes have a unique
weight-one leader and vote for that apartment; the seventh syndrome has three
tied weight-two leaders and abstains.  The rule is therefore intrinsic under
chart permutations.  Since the apartment automorphism group is transitive, it
suffices to exhaust all triples containing apartment 0.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5113_Q3_EQUIVARIANT_RADIUS3_DECODER.json'
PAIRS=list(itertools.combinations(range(4),2));POS={e:i for i,e in enumerate(PAIRS)}
SYNPAIRS=list(itertools.combinations(range(1,4),2))

def syndrome(mask):
    s=0
    for b,(i,j) in enumerate(SYNPAIRS):
        v=((mask>>POS[(0,i)])&1)^((mask>>POS[(0,j)])&1)^((mask>>POS[(i,j)])&1);s|=v<<b
    return s

def equivariant_leaders():
    by={s:[] for s in range(8)}
    for m in range(64):by[syndrome(m)].append(m)
    out=[];profile=[]
    for s in range(8):
        w=min(x.bit_count() for x in by[s]);mins=[x for x in by[s] if x.bit_count()==w]
        profile.append((w,len(mins)))
        out.append(mins[0] if len(mins)==1 else 0) # abstain on the 3-way weight-2 orbit
    assert profile==[(0,1),(1,1),(1,1),(1,1),(1,1),(1,1),(1,1),(2,3)]
    return out,profile

def main():
    G=build_W(3);n=len(G['apartments']);assert n==1620
    lead,local_profile=equivariant_leaders();coords=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    ach=[[] for _ in range(n)];pairs=set()
    for ci,C in enumerate(coords):
        for pos,a in enumerate(C):ach[a].append((ci,pos))
        for a,b in itertools.combinations(sorted(C),2):
            assert (a,b) not in pairs;pairs.add((a,b))
    assert {len(x) for x in ach}=={4}
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
    # Radius two follows structurally: two errors share at most one chart, so each
    # true coordinate receives 4 votes (disjoint charts) or 3 votes (one shared
    # chart); a false coordinate can receive at most one vote from that shared chart.
    # Exhaust the transitivity-reduced complete radius-three census.
    prof=Counter();fail2=0;first_residual=Counter();tested=0
    for b in range(1,n-1):
        for c in range(b+1,n):
            E=frozenset((0,b,c));corr,mv=sweep(E);R=E^corr
            if not R:
                prof[(0,mv,len(corr),0,0)]+=1
            else:
                first_residual[len(R)]+=1;corr2,mv2=sweep(R);R2=R^corr2
                prof[(len(R),mv,len(corr),len(R2),mv2)]+=1
                if R2:fail2+=1
            tested+=1
    assert tested==math.comb(n-1,2)==1309771 and fail2==0
    assert first_residual==Counter({2:47520,1:450})
    assert prof[(0,4,3,0,0)]==1261761 and prof[(0,3,3,0,0)]==40
    assert prof[(2,4,1,0,3)]==47520 and prof[(1,3,2,0,4)]==450
    out={'pass':5113,'status':'THEOREM_GLOBAL_EQUIVARIANT_RADIUS3_TWO_SWEEPS','q':3,
         'apartments':n,'charts':len(coords),'local_syndrome_minima':local_profile,
         'ambiguous_rule':'abstain on the unique syndrome with three weight-2 leaders',
         'radius2_reason':'two apartments share at most one chart; true votes are >=3 while any false shared-chart vote is <=1',
         'base_fixed_triples_tested':tested,'one_sweep_success':1261761+40,
         'first_sweep_residual_weight2':47520,'first_sweep_residual_weight1':450,
         'second_sweep_failures':fail2,'global_guaranteed_error_weight':3,
         'proof_of_globality':'The decoder is S4-equivariant on every chart and building automorphisms are apartment-transitive, so every weight-3 pattern is equivalent to one in the fixed-apartment census.',
         'boundary':'Guarantee is Hamming weight 3 for this finite hard-decision decoder. No claim is made about radius 4, soft decoding, optical noise, or fault-tolerance thresholds.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
