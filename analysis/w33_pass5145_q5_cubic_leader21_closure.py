#!/usr/bin/env python3
"""Pass5145: cubic q=5 closure of chamber leader 20.

Pass5142 closed leaders 18 and 19. Deleting an edge from a 20-edge selected
Levi graph leaves a 19-edge graph, whose adjacent-pair/wedge count is <=29.
Averaging deletion decrements gives n1<=32. The n1=32 case forces endpoint
degree sum >=5 on every edge; only three degree-profile pairs survive, and an
exact C4/C6-free realization search rejects all three. Thus n1<=31, sharply.

The Pass5140 triple law plus the Pass5142 cubic parity minorant then closes the
remaining n1=29,30,31 branches. At n1=31 the deletion constraint forces every
degree-one Levi endpoint to meet degree three, improving N_112 to 44.
"""
from __future__ import annotations
import itertools,json,math
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import optimize

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5145_Q5_CUBIC_LEADER21_CLOSURE.json'


def realize_constrained(L,R,min_dsum):
    L=tuple(sorted(L,reverse=True));R=tuple(sorted(R,reverse=True));nr=len(R)
    memo=set();chosen=[];suf=[0]*(len(L)+1)
    for i in range(len(L)-1,-1,-1):suf[i]=suf[i+1]+L[i]
    def rec(i,rem,padj):
        if i==len(L):return tuple(chosen) if all(x==0 for x in rem) else None
        key=(i,rem,padj)
        if key in memo:return None
        memo.add(key);d=L[i]
        avail=[j for j,x in enumerate(rem) if x and L[i]+R[j]>=min_dsum]
        if len(avail)<d:return None
        for C in itertools.combinations(avail,d):
            if any(((padj[a]>>b)&1) or (padj[a]&padj[b]) for a,b in itertools.combinations(C,2)):continue
            rr=list(rem)
            for a in C:rr[a]-=1
            if sum(rr)!=suf[i+1] or any(x>len(L)-i-1 for x in rr):continue
            ok=True
            for j,x in enumerate(rr):
                if x and x>sum(1 for ii in range(i+1,len(L)) if L[ii]+R[j]>=min_dsum):
                    ok=False;break
            if not ok:continue
            pp=list(padj)
            for a,b in itertools.combinations(C,2):pp[a]|=1<<b;pp[b]|=1<<a
            chosen.append(C);z=rec(i+1,tuple(rr),tuple(pp))
            if z is not None:return z
            chosen.pop()
        return None
    return rec(0,R,tuple([0]*nr))


def wedges(s):return sum(math.comb(d,2) for d in s)


def girth8_ok(L,R,rows):
    # Pair-graph test: repeated right pairs are C4s; a triangle assembled from
    # three DIFFERENT left stars is a C6.  Check all pairs of one star against
    # the previous pair graph before inserting that star, so the intrinsic
    # triangle of a degree-three star is not falsely flagged as a 6-cycle.
    pair_seen=set();adjR=[set() for _ in R]
    for C in rows:
        pairs=list(itertools.combinations(C,2))
        for a,b in pairs:
            if (a,b) in pair_seen:return False
            if adjR[a]&adjR[b]:return False
        for a,b in pairs:
            pair_seen.add((a,b));adjR[a].add(b);adjR[b].add(a)
    return True


def sharp_cap31():
    raw=Fraction(29*20,18);assert raw<33
    candidates=[
      ((3,3,2,2,2,2,2,2,2),(3,3,3,3,3,3,2)),
      ((3,3,3,3,2,2,2,2),(3,3,3,3,2,2,2,2)),
      ((3,3,3,3,3,3,2),(3,3,2,2,2,2,2,2,2)),
    ]
    rejected=[]
    for L,R in candidates:
        assert sum(L)==sum(R)==20 and wedges(L)+wedges(R)==32
        z=realize_constrained(L,R,5);rejected.append(z is None)
    assert all(rejected)
    L=(3,3,2,2,2,2,2,2,2);R=(3,3,3,3,3,3,1,1)
    rows=((0,1,6),(0,2,7),(0,3),(1,4),(1,5),(2,4),(2,5),(3,4),(3,5))
    assert tuple(map(len,rows))==L
    degR=[0]*len(R)
    for C in rows:
        for j in C:degR[j]+=1
    assert tuple(degR)==R and girth8_ok(L,R,rows)
    assert wedges(L)+wedges(R)==31
    return {'deletion_average_upper':str(raw),'wedge32_candidate_profiles':3,
            'wedge32_exact_rejections':3,'sharp_cap':31,
            'sharp31_left_degrees':list(L),'sharp31_right_degrees':list(R)}


def min_centered_wedges(m,e):
    a,r=divmod(2*e,m)
    return (m-r)*math.comb(a,2)+r*math.comb(a+1,2)


def ceil_frac(x):return (x.numerator+x.denominator-1)//x.denominator


def main():
    cap=sharp_cap31();pair={}
    for c in (28,29,30,31):
        ov,dist,feas,lb=optimize(20,c)
        pair[str(c)]={'max_pair_overlap':ov,'distance_counts':list(dist),'pair_weight_lower_bound':lb}
    assert [pair[str(c)]['pair_weight_lower_bound'] for c in (28,29,30,31)]==[712,376,72,-232]
    branches={'n1<=28':{'lower_bound':712}}
    for n1,pb in ((29,376),(30,72)):
        W=min_centered_wedges(20,n1);N112=W-3*(n1//3)
        bound=Fraction(pb,1)+Fraction(6,7)*25*N112
        branches[f'n1={n1}']={'pair_bound':pb,'linegraph_wedges_lower':W,
          'N112_lower':N112,'S3_lower':25*N112,'integer_weight_lower_bound':ceil_frac(bound)}
    N112=44;pb=-232;bound=Fraction(pb,1)+Fraction(6,7)*25*N112
    branches['n1=31']={'pair_bound':pb,'forced_degree1_attachment':'1--3 only',
      'N112_lower':N112,'S3_lower':25*N112,'integer_weight_lower_bound':ceil_frac(bound)}
    assert branches['n1=29']['N112_lower']==29 and branches['n1=29']['integer_weight_lower_bound']==998
    assert branches['n1=30']['N112_lower']==30 and branches['n1=30']['integer_weight_lower_bound']==715
    assert branches['n1=31']['integer_weight_lower_bound']==711
    out={'pass':5145,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_21',
      'q':5,'target_distance':625,'leader_size_closed':20,'adjacent_pair_cap':cap,
      'pair_relaxations':pair,'branches':branches,'uniform_leader20_weight_lower_bound':711,
      'conclusion':'Pass5142 forced every strict q5 counterexample to leader >=20. This pass proves every leader-20 word has weight >=711, so every q5 word of weight <625 has minimum chamber leader at least 21.',
      'boundary':'The full q5 distance theorem remains open. Leaders >=21 and the weight-625 equality shell are not classified here.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
