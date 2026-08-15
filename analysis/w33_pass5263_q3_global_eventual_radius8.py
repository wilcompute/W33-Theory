#!/usr/bin/env python3
"""Pass5263: orbit-free global eventual radius-eight theorem for the q=3 decoder.

Pass5215 certifies global radius seven.  Pass5254 found 25,920 weight-eight
'echo' errors for which the provenance stage makes a false first correction,
but every echo self-heals 8->9->1->0.  This pass proves those are the ONLY
weight-eight errors for which a false candidate can survive provenance.

Fix a false candidate z by apartment transitivity.  Its four incident charts are
disjoint outside z.  A chart can vote for z while z is not an error only when it
contains 2 or 3 errors; for each local position there are exactly two 2-error
and two 3-error masks that do so.  Thus a false candidate has vote V<=4.

A false candidate has singleton-provenance score zero.  If it survives the
max-vote then max-singleton rule with vote V, every true error must have at most
V-1 singleton incident charts, equivalently at least 5-V 'spoiled' charts that
contain another error.

V=1: this would be an 8-variable stopping set in the (4,6)-regular
apartment/chart incidence hypergraph.  An exact fixed-coordinate binary MILP is
infeasible, so no such set exists.  This also proves every weight-eight error
has at least one singleton chart, hence the provenance candidate set is nonempty.

V=2: enumerate the local z-neighbor patterns by local weight l.  Counts are
l=4..8: 24,288,1488,4512,9288.  Exhaustive completion under the necessary
'spoiled>=3' condition leaves no candidate: l=8 has zero; l=7 scans 442,368
possible relevant outsiders; l=6 scans 21,064 filtered pairs; l=5 scans 287,826
safely-pruned relevant triples; for l=4, half the 24 patterns have outsider
local-adjacency at most one and are impossible, while the other 12 force the
unique four double-neighbor outsiders and all 12 forced quadruples fail.

V=3: local weights are l=6,7,8 with 32,256,832 patterns.  The necessary
'spoiled>=2' condition leaves none: all 832 local l=8 patterns fail; all
256*1599=409,344 l=7+1 completions fail; and all 111,744 relevant l=6+2 pairs
fail.

V=4: four voting charts cost at least 8 errors, hence exactly two in each chart.
Each chart has exactly two poison pairs, so precisely 2^4=16 echoes occur per z,
16*1620=25,920 globally.  Pass5254 already certifies all of them self-heal.

Therefore for every weight-eight error, either provenance corrects a nonempty
subset of true errors, leaving <=7 errors for Pass5215, or it is an echo and
self-heals.  The decoder has global eventual guaranteed radius eight.  The
monotone true-only guarantee remains sharply seven.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy import sparse
from analysis.w33_pass5074_gauge_active_chart_tester import build_W

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5263_Q3_GLOBAL_EVENTUAL_RADIUS8.json'
PAIRS=list(itertools.combinations(range(4),2))
LEAD=[0,8,16,1,32,2,4,0]

def syn(m):
    return (((m>>0&1)^(m>>1&1)^(m>>3&1)))|((((m>>0&1)^(m>>2&1)^(m>>4&1)))<<1)|((((m>>1&1)^(m>>2&1)^(m>>5&1)))<<2)

def build():
    G=build_W(3); charts=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    ach=[[] for _ in G['apartments']]
    for ci,C in enumerate(charts):
        for p,a in enumerate(C):ach[a].append((ci,p))
    assert len(charts)==1080 and {len(x) for x in ach}=={4}
    return G,charts,ach

def stopping8_infeasible(charts,ach):
    n=1620;m=len(charts);offy=n;N=n+m
    rr=[];cc=[];dd=[];lo=[];hi=[];r=0
    for ci,C in enumerate(charts):
        # If chart is used (y=1), it contains at least 2 and at most 6 errors;
        # if y=0 it contains zero. Thus singleton intersections are forbidden.
        for a in C:rr.append(r);cc.append(a);dd.append(1)
        rr.append(r);cc.append(offy+ci);dd.append(-2);lo.append(0);hi.append(np.inf);r+=1
        for a in C:rr.append(r);cc.append(a);dd.append(1)
        rr.append(r);cc.append(offy+ci);dd.append(-6);lo.append(-np.inf);hi.append(0);r+=1
    for a in range(n):rr.append(r);cc.append(a);dd.append(1)
    lo.append(8);hi.append(8);r+=1
    rr.append(r);cc.append(0);dd.append(1);lo.append(1);hi.append(1);r+=1
    A=sparse.csr_matrix((dd,(rr,cc)),shape=(r,N))
    res=milp(np.zeros(N),integrality=np.ones(N),bounds=Bounds(np.zeros(N),np.ones(N)),
      constraints=LinearConstraint(A,np.array(lo),np.array(hi)),options={'presolve':True})
    assert res.status==2,res.message
    return True

def main():
    G,charts,ach=build();z=0
    inc=ach[z];assert len(inc)==4
    # The deterministic chart ordering places z at local position zero here.
    assert {p for _,p in inc}=={0}
    others=[charts[ci][1:] for ci,_ in inc]
    N20=set().union(*map(set,others));assert len(N20)==20
    outside=[a for a in range(1620) if a!=z and a not in N20]

    ndir=[];adj=[]
    for a in range(1620):
        d={};A=set()
        for bit,(ci,p) in enumerate(ach[a]):
            for u in charts[ci]:
                if u!=a:d[u]=bit;A.add(u)
        assert len(d)==20;ndir.append(d);adj.append(A)
    def mask_to(a,S):
        m=0
        for u in S:
            b=ndir[a].get(u)
            if b is not None:m|=1<<b
        return m
    def vote0(m5):
        m=sum(((m5>>(p-1))&1)<<p for p in range(1,6))
        return LEAD[syn(m)]==1

    # Complete local pattern census around z.
    local={v:{w:[] for w in range(9)} for v in (2,3,4)}
    counts=Counter()
    for ms in itertools.product(range(32),repeat=4):
        w=sum(x.bit_count() for x in ms)
        if w>8:continue
        v=sum(vote0(x) for x in ms);counts[(v,w)]+=1
        if v in local:
            E=set()
            for q,x in enumerate(ms):
                for j,a in enumerate(others[q]):
                    if (x>>j)&1:E.add(a)
            assert len(E)==w
            local[v][w].append(frozenset(E))
    assert [len(local[2][w]) for w in range(4,9)]==[24,288,1488,4512,9288]
    assert [len(local[3][w]) for w in range(6,9)]==[32,256,832]
    assert len(local[4][8])==16

    # V=3 necessary condition: every true error has at least two spoiled charts.
    v3={'local8':0,'seven_plus_one_scanned':0,'six_plus_two_pairs_scanned':0}
    for Lf in local[3][8]:
        L=set(Lf)
        assert any(mask_to(a,L-{a}).bit_count()<2 for a in L)
        v3['local8']+=1
    for Lf in local[3][7]:
        L=set(Lf)
        for u in outside:
            E=L|{u};v3['seven_plus_one_scanned']+=1
            assert any(mask_to(a,E-{a}).bit_count()<2 for a in E)
    for Lf in local[3][6]:
        L=set(Lf);cand=sorted({u for a in L for u in adj[a] if u in outside})
        for i,u in enumerate(cand):
            for v in cand[i+1:]:
                E=L|{u,v};v3['six_plus_two_pairs_scanned']+=1
                assert any(mask_to(a,E-{a}).bit_count()<2 for a in E)
    assert v3=={'local8':832,'seven_plus_one_scanned':409344,'six_plus_two_pairs_scanned':111744}

    # V=2: every true error must have at least three spoiled charts.
    v2={'local8':0,'seven_plus_one_relevant':0,'six_plus_two_pairs':0,'five_plus_three_relevant':0,'four_plus_four_forced':0}
    for Lf in local[2][8]:
        L=set(Lf);v2['local8']+=1
        assert any(mask_to(a,L-{a}).bit_count()<3 for a in L)
    for Lf in local[2][7]:
        L=set(Lf);pool={u for a in L for u in adj[a] if u in outside}
        for u in pool:
            v2['seven_plus_one_relevant']+=1
            if mask_to(u,L).bit_count()>=3:
                E=L|{u};assert any(mask_to(a,E-{a}).bit_count()<3 for a in E)
    for Lf in local[2][6]:
        L=set(Lf);pool={u for a in L for u in adj[a] if u in outside}
        cand=[u for u in pool if mask_to(u,L).bit_count()>=2]
        for i,u in enumerate(cand):
            for v in cand[i+1:]:
                v2['six_plus_two_pairs']+=1;E=L|{u,v}
                assert any(mask_to(a,E-{a}).bit_count()<3 for a in E)
    for Lf in local[2][5]:
        L=set(Lf);pool=sorted({u for a in L for u in adj[a] if u in outside})
        cand=[u for u in pool if mask_to(u,L)]
        base={u:mask_to(u,L) for u in cand}
        for i,u in enumerate(cand):
            for j in range(i+1,len(cand)):
                v=cand[j];mu=base[u]|((1<<ndir[u][v]) if v in ndir[u] else 0);mv=base[v]|((1<<ndir[v][u]) if u in ndir[v] else 0)
                if mu.bit_count()<2 or mv.bit_count()<2:continue
                for k in range(j+1,len(cand)):
                    w=cand[k];v2['five_plus_three_relevant']+=1;E=L|{u,v,w}
                    if all(mask_to(a,E-{a}).bit_count()>=3 for a in E):raise AssertionError('V2 survivor')
    for Lf in local[2][4]:
        L=set(Lf);base=[mask_to(a,L-{a}).bit_count() for a in L];assert base==[1]*4 or sorted(base)==[1]*4
        cnt={u:sum(a in adj[u] for a in L) for u in outside};mx=max(cnt.values())
        if mx<=1:continue
        dbl=[u for u,c in cnt.items() if c==2];assert len(dbl)==4
        v2['four_plus_four_forced']+=1;E=L|set(dbl)
        assert any(mask_to(a,E-{a}).bit_count()<3 for a in E)
    assert v2['local8']==9288 and v2['seven_plus_one_relevant']==442368 and v2['six_plus_two_pairs']==21064 and v2['five_plus_three_relevant']==287826 and v2['four_plus_four_forced']==12

    stopping8_infeasible(charts,ach)
    out={'pass':5263,'status':'COMPUTATIONAL_THEOREM_Q3_GLOBAL_EVENTUAL_RADIUS8',
      'weight8_stopping_set':'infeasible after fixing one apartment by transitivity',
      'false_vote1':'impossible: would require an 8-variable stopping set',
      'false_vote2':{'local_pattern_counts':{'4':24,'5':288,'6':1488,'7':4512,'8':9288},'completion_certificate':v2,'survivors':0},
      'false_vote3':{'local_pattern_counts':{'6':32,'7':256,'8':832},'completion_certificate':v3,'survivors':0},
      'false_vote4':'exactly 16 poison-pair echoes per false center = 25920 globally; Pass5254 certifies 8->9->1->0.',
      'decoder_conclusion':'Every weight-8 error either makes a nonempty true-only first correction and falls into the certified radius-7 basin, or is an echo and self-heals.',
      'guaranteed_eventual_radius':8,'guaranteed_monotone_true_only_radius':7,
      'boundary':'Computational theorem: the stopping-set infeasibility uses exact MILP; V=2,3 use exhaustive finite completion censuses. Radius nine is open.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
