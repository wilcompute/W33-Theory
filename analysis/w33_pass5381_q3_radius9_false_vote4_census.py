#!/usr/bin/env python3
"""Pass5381: exact q=3 global eventual radius-nine theorem for the provenance decoder.

Pass5263 proves global eventual radius eight.  Fix a false candidate z by
apartment transitivity.  Its four incident charts are disjoint outside z, so a
false candidate has vote V<=4.  If z survives max-vote -> max-singleton
provenance at vote V, every true error has at least 5-V spoiled incident charts.

Weight nine is closed sector by sector.

V=1.  A surviving false candidate would require a 9-variable stopping set in the
(4,6)-regular apartment/chart incidence hypergraph.  An exact fixed-coordinate
MILP is infeasible.

V=2.  One exact MILP simultaneously enforces total weight nine, z absent, exactly
two z-voting incident charts, and at least three spoiled charts for every selected
true error.  It is infeasible.

V=3.  The complete rooted completion census has local z-neighbor weights
6,7,8,9 with counts 32,256,832,1536.  The spoiled>=2 condition leaves no
survivors at local weight 7,8,9 and exactly 32 rooted candidates at local weight6.
Every one of those 32 clears under the actual decoder with trace 9->10->1->0.

V=4.  The only z-voting local masks avoiding z are
  weight2: {1,2}, {3,4}
  weight3: {1,4,5}, {2,3,5}.
Thus the full rooted sector is 64 local 3+2+2+2 patterns plus the 16 radius-eight
poison echoes with one of 1599 outsiders: 25648 cases.  All clear.  The dominant
trace is 9->8->9->1->0.

Therefore every weight-nine error either makes a nonempty true-only correction and
falls into the certified radius-eight basin, or belongs to one of the explicitly
classified false-survivor sectors and self-heals.  The global eventual guaranteed
radius is nine.  The monotone true-only radius remains sharply seven because the
radius-eight echo family still makes a false first correction.
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
OUT=ROOT/'data/PART_W33_PASS5381_Q3_RADIUS9_FALSE_VOTE4_CENSUS.json'
PAIRS=list(itertools.combinations(range(4),2));LEAD=[0,8,16,1,32,2,4,0]

def syn(m):
    return (((m>>0&1)^(m>>1&1)^(m>>3&1)))|((((m>>0&1)^(m>>2&1)^(m>>4&1)))<<1)|((((m>>1&1)^(m>>2&1)^(m>>5&1)))<<2)

def build():
    G=build_W(3);charts=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    ach=[[] for _ in G['apartments']]
    for ci,C in enumerate(charts):
        for p,a in enumerate(C):ach[a].append((ci,p))
    adj=[set() for _ in G['apartments']]
    for C in charts:
        for a in C:adj[a].update(x for x in C if x!=a)
    assert len(charts)==1080 and {len(x) for x in ach}=={4} and {len(x) for x in adj}=={20}
    return G,charts,ach,adj

def sweep(errs,charts,ach,adj):
    touched={}
    for a in errs:
        for ci,p in ach[a]:touched[ci]=touched.get(ci,0)^(1<<p)
    vote={};sing={}
    for ci,m in touched.items():
        lm=LEAD[syn(m)]
        if not lm:continue
        p=(lm&-lm).bit_length()-1;a=charts[ci][p]
        vote[a]=vote.get(a,0)+1
        if m.bit_count()==1 and ((m>>p)&1):sing[a]=sing.get(a,0)+1
    if not vote:return tuple()
    mv=max(vote.values());M=[a for a,v in vote.items() if v==mv]
    ms=max(sing.get(a,0) for a in M);F=[a for a in M if sing.get(a,0)==ms]
    deg={a:sum(b in adj[a] for b in F if b!=a) for a in F};md=min(deg.values())
    return tuple(sorted(a for a in F if deg[a]==md))

def decode(E,charts,ach,adj,limit=12):
    E=set(E);seen=set();trace=[len(E)]
    for step in range(limit+1):
        if not E:return {'status':'clear','sweeps':step,'trace':trace}
        key=tuple(sorted(E))
        if key in seen:return {'status':'cycle','sweeps':step,'trace':trace,'state':list(key)}
        seen.add(key);corr=sweep(E,charts,ach,adj)
        if not corr:return {'status':'stuck','sweeps':step,'trace':trace,'state':list(key)}
        E.symmetric_difference_update(corr);trace.append(len(E))
    return {'status':'limit','sweeps':limit,'trace':trace,'state':sorted(E)}

def stopping9_infeasible(charts):
    n=1620;m=len(charts);off=n;N=n+m;rr=[];cc=[];dd=[];lo=[];hi=[];r=0
    for ci,C in enumerate(charts):
        for a in C:rr.append(r);cc.append(a);dd.append(1)
        rr.append(r);cc.append(off+ci);dd.append(-2);lo.append(0);hi.append(np.inf);r+=1
        for a in C:rr.append(r);cc.append(a);dd.append(1)
        rr.append(r);cc.append(off+ci);dd.append(-6);lo.append(-np.inf);hi.append(0);r+=1
    for a in range(n):rr.append(r);cc.append(a);dd.append(1)
    lo.append(9);hi.append(9);r+=1
    rr.append(r);cc.append(0);dd.append(1);lo.append(1);hi.append(1);r+=1
    A=sparse.csr_matrix((dd,(rr,cc)),shape=(r,N))
    res=milp(np.zeros(N),integrality=np.ones(N),bounds=Bounds(np.zeros(N),np.ones(N)),
      constraints=LinearConstraint(A,np.array(lo),np.array(hi)),options={'presolve':True})
    assert res.status==2,res.message

def false_v2_milp_infeasible(charts,ach,z=0):
    n=1620;m=len(charts);inc=[ci for ci,_ in ach[z]];others=[charts[ci][1:] for ci in inc]
    # x_a: errors; w_ci: chart occupancy >=2; h_{q,mask}: exact local mask for each z-chart.
    x0=0;w0=n;h0=n+m;N=h0+4*32
    rr=[];cc=[];dd=[];lo=[];hi=[];r=0
    # exact w <-> occupancy>=2 for chart size6
    for ci,C in enumerate(charts):
        for a in C:rr.append(r);cc.append(x0+a);dd.append(1)
        rr.append(r);cc.append(w0+ci);dd.append(-2);lo.append(0);hi.append(np.inf);r+=1
        for a in C:rr.append(r);cc.append(x0+a);dd.append(1)
        rr.append(r);cc.append(w0+ci);dd.append(-5);lo.append(-np.inf);hi.append(1);r+=1
    # selected true error => at least3 spoiled charts
    for a in range(n):
        for ci,_ in ach[a]:rr.append(r);cc.append(w0+ci);dd.append(1)
        rr.append(r);cc.append(x0+a);dd.append(-3);lo.append(0);hi.append(np.inf);r+=1
    # weight9 and false center absent
    for a in range(n):rr.append(r);cc.append(x0+a);dd.append(1)
    lo.append(9);hi.append(9);r+=1
    rr.append(r);cc.append(x0+z);dd.append(1);lo.append(0);hi.append(0);r+=1
    # one-hot local masks, linked exactly to each of the five noncenter coordinates
    def vote0(mask5):
        m=sum(((mask5>>(p-1))&1)<<p for p in range(1,6));return int((LEAD[syn(m)]&1)!=0)
    for q in range(4):
        for mask in range(32):rr.append(r);cc.append(h0+32*q+mask);dd.append(1)
        lo.append(1);hi.append(1);r+=1
        for j,a in enumerate(others[q]):
            rr.append(r);cc.append(x0+a);dd.append(1)
            for mask in range(32):
                if (mask>>j)&1:rr.append(r);cc.append(h0+32*q+mask);dd.append(-1)
            lo.append(0);hi.append(0);r+=1
    for q in range(4):
        for mask in range(32):
            if vote0(mask):rr.append(r);cc.append(h0+32*q+mask);dd.append(1)
    lo.append(2);hi.append(2);r+=1
    A=sparse.csr_matrix((dd,(rr,cc)),shape=(r,N))
    res=milp(np.zeros(N),integrality=np.ones(N),bounds=Bounds(np.zeros(N),np.ones(N)),
      constraints=LinearConstraint(A,np.array(lo),np.array(hi)),options={'presolve':True})
    assert res.status==2,res.message

def main():
    G,charts,ach,adj=build();z=0;inc=ach[z];assert len(inc)==4 and {p for _,p in inc}=={0}
    others=[charts[ci][1:] for ci,_ in inc];N20=set().union(*map(set,others));outside=[a for a in range(1620) if a!=z and a not in N20]
    assert len(N20)==20 and len(outside)==1599
    ndir=[]
    for a in range(1620):
        d={}
        for bit,(ci,p) in enumerate(ach[a]):
            for u in charts[ci]:
                if u!=a:d[u]=bit
        assert len(d)==20;ndir.append(d)
    def mask_to(a,S):
        m=0
        for u in S:
            if u in ndir[a]:m|=1<<ndir[a][u]
        return m
    def spoil_ok(E,s):return all(mask_to(a,E-{a}).bit_count()>=s for a in E)
    def vote0(mask5):
        m=sum(((mask5>>(p-1))&1)<<p for p in range(1,6));return (LEAD[syn(m)]&1)!=0

    stopping9_infeasible(charts);false_v2_milp_infeasible(charts,ach,z)

    local={v:{w:[] for w in range(10)} for v in (3,4)}
    for ms in itertools.product(range(32),repeat=4):
        w=sum(x.bit_count() for x in ms)
        if w>9:continue
        v=sum(vote0(x) for x in ms)
        if v in local:
            E=set()
            for q,x in enumerate(ms):
                for j,a in enumerate(others[q]):
                    if (x>>j)&1:E.add(a)
            local[v][w].append(frozenset(E))
    assert [len(local[3][w]) for w in (6,7,8,9)]==[32,256,832,1536]

    v3={'local9':0,'eight_plus_one':0,'seven_plus_two':0,'six_plus_three_survivors':0};v3sur=[]
    for Lf in local[3][9]:
        L=set(Lf);v3['local9']+=1;assert not spoil_ok(L,2)
    for Lf in local[3][8]:
        L=set(Lf)
        for u in outside:
            v3['eight_plus_one']+=1
            if mask_to(u,L) and spoil_ok(L|{u},2):raise AssertionError('V3 w8+1 survivor')
    for Lf in local[3][7]:
        L=set(Lf);cand=sorted({u for a in L for u in adj[a] if u in outside})
        for i,u in enumerate(cand):
            for v in cand[i+1:]:
                v3['seven_plus_two']+=1
                if spoil_ok(L|{u,v},2):raise AssertionError('V3 w7+2 survivor')
    # Complete w6+3 search via required-new-direction neighborhoods.
    outset=set(outside)
    for Lf in local[3][6]:
        L=set(Lf);base={u:mask_to(u,L) for u in outside};b1=[u for u,m in base.items() if m.bit_count()==1];b2=[u for u,m in base.items() if m.bit_count()>=2];bp=b1+b2
        pairs=set()
        for i,u in enumerate(bp):
            for v in bp[i+1:]:pairs.add((u,v))
        for u in outside:
            for v in adj[u]&outset:
                if u<v:pairs.add((u,v))
        for u,v in pairs:
            def dirs(a,b):
                m=base[a]
                if b in ndir[a]:m|=1<<ndir[a][b]
                return m
            du,dv=dirs(u,v),dirs(v,u)
            if du.bit_count()==0 or dv.bit_count()==0:continue
            needu=du.bit_count()<2;needv=dv.bit_count()<2
            if needu and needv:cand=(adj[u]&adj[v]&outset)
            elif needu:cand=(adj[u]&outset)
            elif needv:cand=(adj[v]&outset)
            else:cand=set(b2)|(adj[u]&outset)|(adj[v]&outset)
            for w in cand:
                if w in (u,v):continue
                E=L|{u,v,w}
                if len(E)==9 and spoil_ok(E,2):v3sur.append(frozenset(E))
    v3sur=sorted(set(v3sur),key=lambda S:tuple(sorted(S)));v3['six_plus_three_survivors']=len(v3sur);assert len(v3sur)==32
    v3tr=Counter()
    for E in v3sur:
        R=decode(E,charts,ach,adj);assert R['status']=='clear';v3tr[tuple(R['trace'])]+=1
    assert v3tr==Counter({(9,10,1,0):32})

    # V4 complete rooted census.
    two=[(1,2),(3,4)];three=[(1,4,5),(2,3,5)];cases=[];kind=[]
    for heavy in range(4):
        for choices in itertools.product(range(2),repeat=4):
            E=set()
            for q in range(4):
                pat=three[choices[q]] if q==heavy else two[choices[q]];E.update(others[q][p-1] for p in pat)
            cases.append(frozenset(E));kind.append('local_3+2+2+2')
    base=[]
    for choices in itertools.product(range(2),repeat=4):
        E=set()
        for q in range(4):E.update(others[q][p-1] for p in two[choices[q]])
        base.append(frozenset(E))
    for B in base:
        for u in outside:cases.append(B|{u});kind.append('echo_plus_outsider')
    assert len(cases)==25648 and len(set(cases))==25648
    status=Counter();traces=Counter();maxsw=0
    for E in cases:
        R=decode(E,charts,ach,adj);status[R['status']]+=1;traces[tuple(R['trace'])]+=1;maxsw=max(maxsw,R['sweeps'])
    assert status==Counter({'clear':25648})
    expected={(9,8,9,1,0):23856,(9,10,8,7,1,0):1536,(9,10,8,4,0):192,(9,10,4,0):64};assert dict(traces)==expected

    out={'pass':5381,'status':'COMPUTATIONAL_THEOREM_Q3_GLOBAL_EVENTUAL_RADIUS9',
      'false_vote1':'impossible: exact weight-9 stopping-set MILP is infeasible',
      'false_vote2':'impossible: exact weight-9, vote-2, spoiled>=3 MILP is infeasible',
      'false_vote3':{'local_counts':{'6':32,'7':256,'8':832,'9':1536},'rooted_survivors_per_false_center':32,'survivor_trace':'9->10->1->0'},
      'false_vote4':{'rooted_cases_per_false_center':25648,'all_clear':True,'max_sweeps_observed':maxsw,'trace_histogram':{'/'.join(map(str,k)):v for k,v in expected.items()}},
      'decoder_conclusion':'Every weight-9 error either makes a nonempty true-only first correction and falls into the certified radius-8 basin, or belongs to a classified V=3/V=4 false-survivor family and self-heals.',
      'guaranteed_eventual_radius':9,'guaranteed_monotone_true_only_radius':7,
      'boundary':'Computational theorem. V1/V2 use exact MILP; V3/V4 use exhaustive rooted completion censuses plus full deterministic decoder simulation. Radius10 is open.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
