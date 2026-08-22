#!/usr/bin/env python3
"""Pass7490: exact q=9 target-48 decision at one deletion radius d>=9.

Extends Pass7180.  A hypothetical residual 48-clique at exact deletion radius d from
the known 42-state invertible core must choose d+6 outside-core states whose pairwise
compatibilities form a clique and whose union of core-conflict masks has size at most d.
The search below enforces both constraints exactly with bitset branch-and-bound.
"""
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
import w33_pass7163_7170_e8_hexagonal_lift as b
import w33_pass7180_q9_local_edit_radius as old
ROOT=Path(__file__).resolve().parents[1]

def decide(d:int):
    Gc,rr=old.residual47();Gi=b.invmat9(Gc);comp=lambda i,j:b.pairv(b.STATES[i],Gi,b.STATES[j])!=0
    core=[x for x in rr if b.rankstate(b.STATES[x])==2];assert len(core)==42
    pos={x:i for i,x in enumerate(core)}
    pool=[];mask=[]
    for x in range(512):
        if x in pos:continue
        m=0
        for y in core:
            if not comp(x,y):m|=1<<pos[y]
        if m.bit_count()<=d:pool.append(x);mask.append(m)
    n=len(pool);need=d+6
    adj=[0]*n
    for i,j in itertools.combinations(range(n),2):
        if comp(pool[i],pool[j]):adj[i]|=1<<j;adj[j]|=1<<i
    # Search ordering by core-conflict count then descending compatibility degree.
    perm=sorted(range(n),key=lambda i:(mask[i].bit_count(),-adj[i].bit_count(),pool[i]));rev={x:i for i,x in enumerate(perm)}
    P0=[pool[i] for i in perm];M0=[mask[i] for i in perm];A=[0]*n
    for ni,oi in enumerate(perm):
        z=0;q=adj[oi]
        while q:
            bit=q&-q;j=bit.bit_length()-1;q-=bit;z|=1<<rev[j]
        A[ni]=z
    nodes=0;wit=None;wmask=0
    def rec(R,P,um):
        nonlocal nodes,wit,wmask;nodes+=1
        if len(R)>=need:
            wit=[P0[i] for i in R[:need]];wmask=um;return True
        # Enforce deletion budget on every remaining candidate.
        Q=P;F=0
        while Q:
            bit=Q&-Q;i=bit.bit_length()-1;Q-=bit
            if (um|M0[i]).bit_count()<=d:F|=bit
        P=F
        if len(R)+P.bit_count()<need:return False
        # Greedy coloring clique upper bound.
        order=[];bound=[];color=0;U=P
        while U:
            color+=1;Q=U
            while Q:
                bit=Q&-Q;i=bit.bit_length()-1
                order.append(i);bound.append(color);U&=~bit;Q&=~bit;Q&=~A[i]
        for k in range(len(order)-1,-1,-1):
            if len(R)+bound[k]<need:return False
            i=order[k];bit=1<<i
            if not(P&bit):continue
            nm=um|M0[i]
            if nm.bit_count()<=d and rec(R+[i],P&A[i],nm):return True
            P&=~bit
        return False
    yes=rec([], (1<<n)-1,0)
    deleted=[core[i] for i in range(42) if (wmask>>i)&1] if yes else None
    return {'deletions':d,'needed_additions':need,'candidate_pool':n,'target48_exists':yes,'search_nodes':nodes,'added_witness':wit,'deleted_core_states_used':deleted,
      'theorem_if_unsat':f'No residual 48-clique exists at exact deletion radius {d} from the known 42-state invertible core.',
      'boundary':'Local theorem in canonical anchor type (1,3,5). Even UNSAT at many radii is not by itself a global alpha(W(3,9)) proof.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--d',type=int,required=True);ap.add_argument('--out');a=ap.parse_args();assert 9<=a.d<=36
    z=decide(a.d);p=Path(a.out) if a.out else ROOT/f'data/PART_W33_PASS7490_Q9_TARGET48_D{a.d}.json';p.write_text(json.dumps({'schema':'w33.pass7490.q9_radius_target48.v1','status':'PASS',**z},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','d':a.d,'candidate_pool':z['candidate_pool'],'nodes':z['search_nodes'],'target48_exists':z['target48_exists']}))
if __name__=='__main__':main()
