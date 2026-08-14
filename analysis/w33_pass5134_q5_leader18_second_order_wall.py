#!/usr/bin/env python3
"""Pass5134: exact q=5 m=18 cut-gauge second-order frontier.

We certify the sharp universal adjacent-pair cap 27 for an 18-edge
cut-minimal leader (bipartite, max degree 3, girth at least 8), then run the
same exact chamber-scheme Delsarte program as Pass5126.  The resulting
Bonferroni bound is only 320, proving that the pair-only route is exhausted at
m=18 and that any further q5 distance progress needs third-order information.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5134_Q5_LEADER18_SECOND_ORDER_WALL.json'

def degree_sequences(m):
    out=[]
    for n3 in range(m//3+1):
      for n2 in range((m-3*n3)//2+1):
        n1=m-3*n3-2*n2
        if n1>=0:
          s=(3,)*n3+(2,)*n2+(1,)*n1
          if s:out.append(s)
    return out

def wedges(s):return sum(d*(d-1)//2 for d in s)

def realize(L,R):
    L=tuple(sorted(L,reverse=True));R=tuple(sorted(R,reverse=True));nr=len(R)
    memo=set();chosen=[];suf=[0]*(len(L)+1)
    for i in range(len(L)-1,-1,-1):suf[i]=suf[i+1]+L[i]
    def rec(i,rem,padj):
        if i==len(L):return tuple(chosen) if all(x==0 for x in rem) else None
        key=(i,rem,padj)
        if key in memo:return None
        memo.add(key);d=L[i];avail=[j for j,x in enumerate(rem) if x]
        if len(avail)<d:return None
        for C in itertools.combinations(avail,d):
            if any(((padj[a]>>b)&1) or (padj[a]&padj[b]) for a,b in itertools.combinations(C,2)):continue
            rr=list(rem)
            for a in C:rr[a]-=1
            if sum(rr)!=suf[i+1] or any(x>len(L)-i-1 for x in rr):continue
            pp=list(padj)
            for a,b in itertools.combinations(C,2):pp[a]|=1<<b;pp[b]|=1<<a
            chosen.append(C);z=rec(i+1,tuple(rr),tuple(pp))
            if z is not None:return z
            chosen.pop()
        return None
    return rec(0,R,tuple([0]*nr))

def delsarte_ok(m,n1,n2,n3,n4):
    if 625*m-250*n1+50*n2-10*n3+2*n4<0:return False
    if 25*m+20*n1-10*n2-4*n3+2*n4<0:return False
    R=25*m+20*n1+4*n3-2*n4;C=5*n1+4*n2-n3
    return R>=0 and R*R>=10*C*C

def optimize(m,cap):
    total=math.comb(m,2);best=(-1,None);feasible=0
    for n1 in range(cap+1):
      rem=total-n1
      for n2 in range(rem+1):
        for n3 in range(rem-n2+1):
          n4=rem-n2-n3
          if not delsarte_ok(m,n1,n2,n3,n4):continue
          feasible+=1;ov=125*n1+25*n2+5*n3+n4
          if ov>best[0]:best=(ov,(n1,n2,n3,n4))
    return best[0],best[1],feasible,m*625-2*best[0]

def main():
    m=18;S=degree_sequences(m)
    high=[(wedges(L)+wedges(R),L,R) for L in S for R in S if wedges(L)+wedges(R)>27]
    assert len(S)==37 and len(high)==63
    assert all(realize(L,R) is None for _,L,R in high)
    eqL=(3,3,3,3,3,3);eqR=(3,3,2,2,2,1,1,1,1,1,1)
    assert wedges(eqL)+wedges(eqR)==27 and realize(eqL,eqR) is not None
    ov,dist,feas,lb=optimize(m,27)
    assert (ov,dist,lb)==(5465,(27,73,53,0),320)
    out={'pass':5134,'status':'THEOREM_EXACT_SECOND_ORDER_WALL_AT_Q5_LEADER18','q':5,
      'leader_size':18,'degree_sequences':37,'profiles_above_wedge27_rejected':63,
      'sharp_adjacent_pair_cap':27,'sharp_profile':{'left':list(eqL),'right':list(eqR)},
      'delsarte':{'max_pair_overlap':ov,'distance_pair_counts':list(dist),'integer_points':feas,'bonferroni_weight_lower_bound':lb},
      'conclusion':'The universal girth-8/subcubic pair cap is exactly 27, but pairwise Delsarte+Bonferroni only gives wt>=320 at m=18. Thus the second-order leader method that closed m<=17 cannot by itself close m=18.',
      'next_required_order':'third-order chamber-star intersections / triple moments',
      'boundary':'This is a rigorous diagnostic theorem, not a q5 distance improvement. Strict counterexamples are still known only to require leader >=18.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
