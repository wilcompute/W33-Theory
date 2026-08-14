#!/usr/bin/env python3
"""Pass5126: exact q=5 m=17 cut-gauge/Delsarte closure.

A cut-minimal chamber leader in the q=5 Levi graph is a bipartite graph of
maximum degree three and girth at least eight.  We exhaust all ordered left/right
degree-sequence pairs with 17 edges whose wedge count exceeds 25 and prove that
none has a simple C4/C6-free realization.  Wedge 25 is realizable.  The exact
q=5 chamber-scheme Delsarte optimization at this cap then gives apartment weight
at least 625, raising the strict counterexample leader wall from 17 to 18.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5126_Q5_LEADER18_EXACT.json'

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
    memo=set();chosen=[]
    def rec(i,rem,padj):
        if i==len(L):return tuple(chosen) if all(x==0 for x in rem) else None
        key=(i,rem,padj)
        if key in memo:return None
        memo.add(key);d=L[i];avail=[j for j,x in enumerate(rem) if x]
        if len(avail)<d:return None
        for C in itertools.combinations(avail,d):
            ok=True
            for a,b in itertools.combinations(C,2):
                # Prior right-distance 1 gives a C4; distance 2 gives a C6.
                if ((padj[a]>>b)&1) or (padj[a]&padj[b]):ok=False;break
            if not ok:continue
            rr=list(rem)
            for a in C:rr[a]-=1
            if sum(rr)!=sum(L[i+1:]) or any(x>len(L)-i-1 for x in rr):continue
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
    S=degree_sequences(17);high=[];eq=[]
    for L in S:
      for R in S:
        w=wedges(L)+wedges(R)
        if w>25:high.append((w,L,R))
        elif w==25:
            z=realize(L,R)
            if z is not None:eq.append((L,R,z))
    assert len(high)==51 and all(realize(L,R) is None for _,L,R in high)
    assert len(eq)==12
    ov,dist,feas,lb=optimize(17,25)
    assert (ov,dist,lb)==(5000,(25,66,45,0),625)
    out={'pass':5126,'status':'THEOREM_Q5_COUNTEREXAMPLE_LEADER_AT_LEAST_18',
         'q':5,'target_distance':625,'leader_size_closed':17,
         'degree_sequences':len(S),'ordered_profiles_above_wedge25_rejected':len(high),
         'sharp_wedge_cap':25,'ordered_degree_profiles_realizing_wedge25':len(eq),
         'delsarte':{'max_pair_overlap':ov,'distance_pair_counts':list(dist),
                     'integer_points':feas,'weight_lower_bound':lb},
         'conclusion':'Pass5118 covered leaders through 16. Every cut-minimal 17-edge leader has at most 25 adjacent chamber pairs, and exact Delsarte positivity then gives wt>=625. Hence any q5 word with wt<625 has minimum chamber leader at least 18.',
         'equality_boundary':'At leader 17 the second-order bound can equal 625 at distance distribution (25,66,45,0); this pass does not classify actual weight-625 equality words.',
         'boundary':'The q5 distance theorem remains open for leaders >=18.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
