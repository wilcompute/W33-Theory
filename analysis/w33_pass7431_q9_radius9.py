#!/usr/bin/env python3
"""Pass7431: exact q=9 target-48 exclusion at invertible-core deletion radius nine.

Extends Pass7180 by one exact radius.  The same canonical (1,3,5) residual graph,
known 42-state invertible core, blocker-mask filter and greedy-color branch-and-bound
are reused.  No global alpha(W(3,9)) claim is made.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import w33_pass7163_7170_e8_hexagonal_lift as b
import w33_pass7180_q9_local_edit_radius as old
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7431_Q9_RADIUS9.json'

def main():
    Gc,rr=old.residual47();Gi=b.invmat9(Gc);comp=lambda i,j:b.pairv(b.STATES[i],Gi,b.STATES[j])!=0
    C=[x for x in rr if b.rankstate(b.STATES[x])==2];assert len(C)==42
    r1=[i for i,s in enumerate(b.STATES) if b.rankstate(s)==1]
    r2=[i for i,s in enumerate(b.STATES) if b.rankstate(s)==2];out2=[x for x in r2 if x not in C]
    cp={x:i for i,x in enumerate(C)}
    c1={x:frozenset(y for y in C if not comp(x,y)) for x in r1}
    c2={x:frozenset(y for y in C if not comp(x,y)) for x in out2}
    d=9;total=48;need=total-(42-d)
    pool=sorted([x for x in r1 if len(c1[x])<=d]+[x for x in out2 if len(c2[x])<=d]);n=len(pool)
    assert n==469 and need==15
    adj=[0]*n;cm=[]
    for x in pool:
        S=c1[x] if x in c1 else c2[x];m=0
        for y in S:m|=1<<cp[y]
        cm.append(m)
    for i,j in itertools.combinations(range(n),2):
        if comp(pool[i],pool[j]):adj[i]|=1<<j;adj[j]|=1<<i
    nodes=0;witness=None
    def rec(R,P,um):
        nonlocal nodes,witness;nodes+=1
        if len(R)>=need:witness=[pool[i] for i in R];return True
        Q=P;F=0
        while Q:
            bit=Q&-Q;i=bit.bit_length()-1;Q-=bit
            if (um|cm[i]).bit_count()<=d:F|=bit
        P=F
        if len(R)+P.bit_count()<need:return False
        order=[];bounds=[];color=0;U=P
        while U:
            color+=1;Q=U
            while Q:
                bit=Q&-Q;i=bit.bit_length()-1;order.append(i);bounds.append(color);U&=~bit;Q&=~bit;Q&=~adj[i]
        for z in range(len(order)-1,-1,-1):
            i=order[z]
            if len(R)+bounds[z]<need:return False
            bit=1<<i
            if not(P&bit):continue
            nm=um|cm[i]
            if nm.bit_count()<=d and rec(R+[i],P&adj[i],nm):return True
            P&=~bit
        return False
    yes=rec([], (1<<n)-1,0);assert not yes and witness is None
    assert nodes==2535139
    out={'schema':'w33.pass7431.q9_radius9.v1','status':'PASS','anchor_type':'(1,3,5)',
      'known_invertible_core':42,'exact_core_deletions':9,'remaining_core':33,
      'target_residual_clique_size':48,'needed_added_clique':need,'candidate_pool':n,
      'exists':False,'branch_nodes':nodes,
      'theorem':'In the canonical (1,3,5) residual graph, target 48 is impossible after exactly nine deletions from the known 42-state invertible core. Combined with Pass7180, any hypothetical residual 48-clique must delete at least ten of those 42 core states.',
      'boundary':'Local basin theorem only. Radius ten was not closed here; no global 48-clique impossibility and no alpha(W(3,9))=51 claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','radius':9,'nodes':nodes}))
if __name__=='__main__':main()
