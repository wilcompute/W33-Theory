#!/usr/bin/env python3
"""Pass7180: exact q=9 local target-48 exclusion through five invertible-core deletions."""
from __future__ import annotations
import itertools,json
from pathlib import Path
import w33_pass7163_7170_e8_hexagonal_lift as b
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7180_Q9_LOCAL_EDIT_RADIUS.json'
S9=[22,24,78,80,88,95,141,144,149,177,182,189,190,191,200,213,214,230,234,258,271,276,288,331,336,364,368,376,397,403,449,450,478,480,539,561,570,580,588,622,651,655,658,741,750,753,756,780,784,801,814]

def residual47():
    P=sorted({b.norm9(v) for v in itertools.product(range(9),repeat=4) if any(v)});W=[P[i] for i in S9];A=[0,1,2,5]
    Gold=[[b.B9(W[i],W[j]) for j in A] for i in A];Gc=b.canonical_G((1,3,5));sol=[]
    for perm in itertools.permutations(range(4)):
      for d1,d2,d3 in itertools.product(range(1,9),repeat=3):
        ds=(1,d1,d2,d3);lhs=b.gm(ds[0],b.gm(ds[1],Gold[perm[0]][perm[1]]));c=b.gm(lhs,b.INV[Gc[0][1]])
        if all(b.gm(ds[i],b.gm(ds[j],Gold[perm[i]][perm[j]]))==b.gm(c,Gc[i][j]) for i in range(4) for j in range(4)):sol.append((perm,ds,c))
    assert len(sol)==4;perm,ds,c=sol[0];idx={r:i for i,r in enumerate(b.STATES)};rr=[]
    for i in range(51):
        if i in A:continue
        old=[b.B9(W[i],W[a]) for a in A];new=[b.gm(ds[j],old[perm[j]]) for j in range(4)];z=b.INV[new[0]]
        rr.append(idx[tuple(b.gm(z,x) for x in new)])
    assert len(rr)==47 and len(set(rr))==47
    return Gc,rr

def main():
    Gc,rr=residual47();Gi=b.invmat9(Gc);comp=lambda i,j:b.pairv(b.STATES[i],Gi,b.STATES[j])!=0
    C=[x for x in rr if b.rankstate(b.STATES[x])==2];B=[x for x in rr if b.rankstate(b.STATES[x])==1]
    assert len(C)==42 and len(B)==5
    r1=[i for i,s in enumerate(b.STATES) if b.rankstate(s)==1];r2=[i for i,s in enumerate(b.STATES) if b.rankstate(s)==2];out2=[x for x in r2 if x not in C]
    c1={x:frozenset(y for y in C if not comp(x,y)) for x in r1};c2={x:frozenset(y for y in C if not comp(x,y)) for x in out2};cp={x:i for i,x in enumerate(C)}
    def exists(d,total):
        need=total-(42-d);pool=sorted([x for x in r1 if len(c1[x])<=d]+[x for x in out2 if len(c2[x])<=d]);n=len(pool)
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
        yes=rec([], (1<<n)-1,0)
        return {'deletions':d,'total_target':total,'needed_added_clique':need,'candidate_pool':n,'exists':yes,'nodes':nodes,'witness':witness}
    exact={0:47,1:46,2:47,3:46,4:46,5:46};cert=[]
    for d,m in exact.items():
        lo=exists(d,m);up=exists(d,m+1);assert lo['exists'] and not up['exists'];cert.append({'d':d,'maximum_total':m,'lower':lo,'upper':up})
    # The original core has exactly the known five universally compatible rank-one states.
    universal=[x for x in r1 if not c1[x]];assert set(universal)==set(B)
    out={'schema':'w33.pass7180.q9_local_edit_radius.v1','status':'PASS','anchor_type':'(1,3,5)',
      'known_47_split':{'invertible':42,'rank1':5},'invertible_core':C,'rank1_completion':B,
      'universally_compatible_rank1_states':universal,
      'exact_maximum_total_after_exact_core_deletions':{str(k):v for k,v in exact.items()},'certificates':cert,
      'theorem':'For exactly d=0,1,2,3,4,5 deletions from the known 42-state invertible core, followed by arbitrary compatible additions from every other normalized residual state, the exact maxima are 47,46,47,46,46,46. Thus target 48 is impossible through deletion radius five.',
      'boundary':'Local theorem in the canonical (1,3,5) anchor graph only. It does not prove the global 48-clique impossibility or alpha(W(3,9))=51.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','maxima':out['exact_maximum_total_after_exact_core_deletions']}))
if __name__=='__main__':main()
