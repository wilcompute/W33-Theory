#!/usr/bin/env python3
"""Pass5164 (bonkers): close q=5 leader 24 by rejecting the only P4=96 equality profiles.

Pass5163 closes m=23.  For m=24, deletion gives W<=41; W=41 would force
endpoint-degree sum >=5, but every degree profile has leaves, so W<=40.  Pair +
N_112 + selected-four-edge-path cubic correction closes W<=39.  At W=40 the
local-type relaxation has three degree profiles; one has P4>=100 and closes.
The only remaining equality profiles have P4=96:
  (n1,n2,n3)=(4,4,12) and (7,1,13).
This producer proves both impossible in a girth-eight bipartite selected Levi
graph, hence actual P4>=97 and the W=40 cubic bound becomes 629>625.
"""
from __future__ import annotations
import itertools,json,math
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import optimize
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import (
    local_patterns,profiles,p4_relaxed,centered_wedge_floor,ceil_frac)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5164_Q5_CUBIC_LEADER25_GIRTH_REJECTION.json'


def compositions(n,k,p=()):
    if k==1:
        yield p+(n,);return
    for i in range(n+1):yield from compositions(n-i,k-1,p+(i,))


def equality_pattern_solutions(profile,minsum,target):
    data={}
    for d,n in zip((1,2,3),profile):
        pats=local_patterns(d,minsum);rows=[]
        for cnts in compositions(n,len(pats)):
            st=[0,0,0];cost=0
            for cnt,(pat,pc) in zip(cnts,pats):
                cost+=cnt*pc
                for j in range(3):st[j]+=cnt*pat[j]
            rows.append((tuple(st),cost,cnts))
        data[d]=(pats,rows)
    out=[]
    for s1,c1,x1 in data[1][1]:
      for s2,c2,x2 in data[2][1]:
        if s1[1]!=s2[0]:continue
        for s3,c3,x3 in data[3][1]:
          if c1+c2+c3!=target:continue
          if s1[2]!=s3[0] or s2[2]!=s3[1]:continue
          if s1[0]%2 or s2[1]%2 or s3[2]%2:continue
          out.append((s1,s2,s3,x1,x2,x3))
    return data,out


def realize_girth8(L,R):
    """Exact simple bipartite C4/C6-free realization search."""
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
            # repeated right pair -> C4; a previous common neighbor of a,b -> C6
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


def profile_A_impossible():
    # Equality DP forces the degree-3 induced graph H to be 2-regular on 12
    # vertices. Girth>=8 implies H=C12. Four external degree-2 vertices join
    # eight H vertices in pairs. Each such 2-edge chord must join antipodes of
    # C12, otherwise one of the two chord+arc cycles has length <8. Four chosen
    # antipodal pairs project to four vertices of C6; two are adjacent because
    # alpha(C6)=3, and those two chords plus two cycle edges form a C6.
    return {'H':'C12','external_degree2_chords':4,'forced_chord_distance':6,
            'quotient_antipodal_graph':'C6','independence_number':3,
            'required_independent_vertices':4,'impossible':True}


def profile_B_impossible():
    # Equality DP: induced H on the 13 degree-3 vertices has degree sequence
    # 3^4 2^9 and 15 edges. Bipartition degree sums are 15, forcing side
    # sequences (3,2,2,2,2,2,2) and (3,3,3,2,2,2), up to swap. Exact C4/C6-free
    # realization search rejects that unique degree split.
    L=(3,2,2,2,2,2,2);R=(3,3,3,2,2,2)
    z=realize_girth8(L,R)
    assert z is None
    return {'left_degrees':list(L),'right_degrees':list(R),'C4_C6_free_realization':False,'impossible':True}


def main():
    m=24
    # W=41: deletion to m=23 cap38 forces d(u)+d(v)>=5, so no leaves. But all
    # algebraic degree profiles at W=41 have n1>0.
    assert profiles(m,41)==[(2,5,12),(5,2,13)]
    cap=40
    pair={}
    for W in range(32,41):
        ov,dist,feas,lb=optimize(m,W);pair[str(W)]={'distance_counts':list(dist),'pair_weight_lower_bound':lb}
    assert [pair[str(W)]['pair_weight_lower_bound'] for W in range(32,41)]==[1040,736,432,96,-208,-512,-816,-1120,-1424]

    # Reproduce W40 relaxed equality structure.
    rows=[]
    for p in profiles(m,40):
        v,st=p4_relaxed(*p,4);rows.append((p,v,st))
    assert [(p,v) for p,v,_ in rows]==[((1,7,11),100),((4,4,12),96),((7,1,13),96)]
    for p in ((4,4,12),(7,1,13)):
        _,sol=equality_pattern_solutions(p,4,96);assert len(sol)==1

    A=profile_A_impossible();B=profile_B_impossible()
    actual_p4=97
    n112=centered_wedge_floor(m,40)-3*(40//3);assert n112==57
    mass=25*n112+10*actual_p4
    bound=Fraction(pair['40']['pair_weight_lower_bound'])+Fraction(6,7)*mass
    assert ceil_frac(bound)==629

    # W<=39 is already safe with relaxed DP; record exact lower bounds.
    branch={}
    for W in range(33,40):
        ps=profiles(m,W);minsum=max(0,W-36)
        vals=[]
        for p in ps:
            v,_=p4_relaxed(*p,minsum)
            if v is not None:vals.append(v)
        p4=min(vals) if vals else 0
        n112w=centered_wedge_floor(m,W)-3*(W//3)
        massw=25*n112w+10*p4
        bw=Fraction(pair[str(W)]['pair_weight_lower_bound'])+Fraction(6,7)*massw
        branch[str(W)]={'P4_lower':p4,'N112_lower':n112w,'integer_weight_lower_bound':ceil_frac(bw)}
    assert min(v['integer_weight_lower_bound'] for v in branch.values())>=693

    out={'pass':5164,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_25',
      'q':5,'leader_size_closed':24,'target_distance':625,'adjacent_pair_cap':cap,
      'W40_relaxed_profiles':[{'degree_counts':list(p),'P4_relaxed_lower':v} for p,v,_ in rows],
      'P4_96_profile_A_rejection':A,'P4_96_profile_B_rejection':B,
      'actual_W40_P4_lower':actual_p4,'W40_N112_lower':n112,
      'W40_triple_mass_lower':mass,'W40_integer_weight_lower_bound':ceil_frac(bound),
      'lower_W_branches':branch,
      'conclusion':'The only two local-type patterns that could attain P4=96 at W=40 are incompatible with Levi girth eight. Thus actual P4>=97, giving weight>=629 in the final W40 sector. Every q5 word of weight <625 therefore has minimum chamber leader at least 25.',
      'boundary':'This closes leader 24 only. The q5/all-q apartment-code distance theorem remains open for leaders >=25 and the weight-625 equality shell remains unclassified.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
