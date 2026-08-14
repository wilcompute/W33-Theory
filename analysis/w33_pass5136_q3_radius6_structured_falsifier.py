#!/usr/bin/env python3
"""Pass5136: exact structured attack on q=3 decoder radius six.

A false apartment z can first tie the true-error vote ceiling at total weight 6:
choose three of the four charts through z and, in each chart, choose a 2-error
mask whose unique local leader is z.  These 2+2+2 errors are disjoint because
charts through z meet only in z.  We exhaust this minimal centered motif and
run the actual global max-vote decoder.  A single witness is enough to falsify
the radius-six guarantee.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5136_Q3_RADIUS6_STRUCTURED_FALSIFIER.json'
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
        w=min(x.bit_count() for x in B[s]);z=[x for x in B[s] if x.bit_count()==w]
        out.append(z[0] if len(z)==1 else 0)
    return out

def main():
    G=build_W(3);n=len(G['apartments']);lead=leaders();coords=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    ach=[[] for _ in range(n)]
    for ci,C in enumerate(coords):
        for pos,a in enumerate(C):ach[a].append((ci,pos))
    assert all(len(x)==4 for x in ach)
    def sweep(E):
        masks={}
        for a in E:
            for ci,pos in ach[a]:masks[ci]=masks.get(ci,0)^(1<<pos)
        votes={}
        for ci,m in masks.items():
            lm=lead[syndrome(m)]
            if lm:
                p=lm.bit_length()-1;a=coords[ci][p];votes[a]=votes.get(a,0)+1
        if not votes:return frozenset(),0,{}
        z=max(votes.values());return frozenset(a for a,v in votes.items() if v==z),z,votes
    center=0;inc=ach[center];local_options=[]
    for ci,cpos in inc:
        opts=[]
        other=[p for p in range(6) if p!=cpos]
        for a,b in itertools.combinations(other,2):
            m=(1<<a)|(1<<b)
            if lead[syndrome(m)]==(1<<cpos):opts.append((coords[ci][a],coords[ci][b]))
        assert len(opts)==2;local_options.append((ci,cpos,opts))
    tested=0;witness=None
    for chosen in itertools.combinations(range(4),3):
        for choices in itertools.product((0,1),repeat=3):
            E=set()
            charts=[]
            for t,j in enumerate(chosen):
                ci,cpos,opts=local_options[j];E.update(opts[choices[t]]);charts.append(ci)
            if len(E)!=6:continue
            tested+=1;corr,v,votes=sweep(frozenset(E))
            if center in corr and center not in E:
                witness={'errors':sorted(E),'center_false_apartment':center,'centered_charts':charts,
                         'max_vote':v,'correction_set':sorted(corr),
                         'true_corrections':[a for a in sorted(corr) if a in E],
                         'false_corrections':[a for a in sorted(corr) if a not in E],
                         'center_vote':votes.get(center,0)}
                break
        if witness:break
    assert tested>0
    status='COUNTEREXAMPLE_RADIUS6' if witness else 'NO_COUNTEREXAMPLE_IN_MINIMAL_CENTERED_MOTIF'
    out={'pass':5136,'status':status,'q':3,'structured_candidates_tested':tested,
         'minimal_false_vote_mechanism':'three charts through a false center, two errors per chart, each local 2-error syndrome voting for the center',
         'witness':witness,
         'conclusion':('The equivariant decoder is not globally radius six: the displayed six-error word makes a false apartment tie for the global maximum and therefore the max-vote correction introduces a false bit.' if witness else 'The minimal centered 2+2+2 false-vote motif does not falsify radius six; a broader connected-six search remains required.'),
         'boundary':'This concerns the specific hard-decision decoder only. It says nothing about ML distance or the apartment code distance.'}
    if witness:assert witness['false_corrections']
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
