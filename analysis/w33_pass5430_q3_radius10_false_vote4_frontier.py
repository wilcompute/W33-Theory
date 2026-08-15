#!/usr/bin/env python3
"""Pass5430: exact q=3 global eventual radius-ten theorem.

Pass5381 proves global eventual radius nine.  Fix a false candidate z by
apartment transitivity.  Its four incident charts are disjoint outside z, so a
false candidate has vote V<=4.  If z survives max-vote -> max-singleton
provenance at vote V, every true error has at least 5-V spoiled incident charts.

Weight ten closes sector by sector.

V=1: a surviving false candidate would require a 10-variable stopping set in the
(4,6)-regular apartment/chart incidence hypergraph.  The exact fixed-coordinate
MILP is infeasible.

V=2: an exact MILP enforces weight ten, z absent, exactly two z-voting incident
charts, and >=3 spoiled charts at every selected true error.  It is infeasible.

V=3: the complete local z-neighbor census has weights 6..10 with counts
32,256,832,1536,1856.  Every outside coordinate can supply a new chart direction
to at most two local errors.  The local direction deficits are respectively
6; >=7; >=8; >=9; >=10, so only local weight six plus four outsiders can survive
the necessary spoiled>=2 condition.  Exact completion gives 1296 rooted cases;
all 1296 clear under the actual deterministic decoder.

V=4: raw shapes number 20,544,048.  An outsider must share a chart with another
true error or its four singleton votes eliminate z.  This exact prune leaves
341,664 two-outsider echoes, 7,808 one-outsider 3+2+2+2 cases, and 96 local
3+3+2+2 cases: 349,568 total.  All clear under the actual decoder.

Therefore every weight-ten error either makes a nonempty true-only first
correction and falls to the certified radius-nine basin, or lies in one of the
classified false-survivor sectors and self-heals.  The global eventual guaranteed
radius is ten.  The monotone true-only radius remains sharply seven.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy import sparse
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5430_Q3_GLOBAL_EVENTUAL_RADIUS10.json'
PAIRS=list(itertools.combinations(range(4),2));LEAD=[0,8,16,1,32,2,4,0]

def syn(m):
    return (((m>>0&1)^(m>>1&1)^(m>>3&1)))|((((m>>0&1)^(m>>2&1)^(m>>4&1)))<<1)|((((m>>1&1)^(m>>2&1)^(m>>5&1)))<<2)

def build():
    G=build_W(3);charts=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    ach=[[] for _ in G['apartments']];adj=[set() for _ in G['apartments']]
    for ci,C in enumerate(charts):
        for p,a in enumerate(C):ach[a].append((ci,p))
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

def decode(E,charts,ach,adj,limit=20):
    E=set(E);seen=set();trace=[len(E)]
    for step in range(limit+1):
        if not E:return {'status':'clear','sweeps':step,'trace':trace}
        key=tuple(sorted(E))
        if key in seen:return {'status':'cycle','sweeps':step,'trace':trace,'state':list(key)}
        seen.add(key);corr=sweep(E,charts,ach,adj)
        if not corr:return {'status':'stuck','sweeps':step,'trace':trace,'state':list(key)}
        E.symmetric_difference_update(corr);trace.append(len(E))
    return {'status':'limit','sweeps':limit,'trace':trace,'state':sorted(E)}

def stopping10_infeasible(charts):
    n=1620;m=len(charts);off=n;N=n+m;rr=[];cc=[];dd=[];lo=[];hi=[];r=0
    for ci,C in enumerate(charts):
        for a in C:rr.append(r);cc.append(a);dd.append(1)
        rr.append(r);cc.append(off+ci);dd.append(-2);lo.append(0);hi.append(np.inf);r+=1
        for a in C:rr.append(r);cc.append(a);dd.append(1)
        rr.append(r);cc.append(off+ci);dd.append(-6);lo.append(-np.inf);hi.append(0);r+=1
    for a in range(n):rr.append(r);cc.append(a);dd.append(1)
    lo.append(10);hi.append(10);r+=1
    rr.append(r);cc.append(0);dd.append(1);lo.append(1);hi.append(1);r+=1
    A=sparse.csr_matrix((dd,(rr,cc)),shape=(r,N))
    res=milp(np.zeros(N),integrality=np.ones(N),bounds=Bounds(np.zeros(N),np.ones(N)),
      constraints=LinearConstraint(A,np.array(lo),np.array(hi)),options={'presolve':True})
    assert res.status==2,res.message

def false_v2_infeasible(charts,ach,z=0):
    n=1620;m=len(charts);inc=[ci for ci,_ in ach[z]];others=[charts[ci][1:] for ci in inc]
    x0=0;w0=n;h0=n+m;N=h0+4*32;rr=[];cc=[];dd=[];lo=[];hi=[];r=0
    for ci,C in enumerate(charts):
        for a in C:rr.append(r);cc.append(x0+a);dd.append(1)
        rr.append(r);cc.append(w0+ci);dd.append(-2);lo.append(0);hi.append(np.inf);r+=1
        for a in C:rr.append(r);cc.append(x0+a);dd.append(1)
        rr.append(r);cc.append(w0+ci);dd.append(-5);lo.append(-np.inf);hi.append(1);r+=1
    for a in range(n):
        for ci,_ in ach[a]:rr.append(r);cc.append(w0+ci);dd.append(1)
        rr.append(r);cc.append(x0+a);dd.append(-3);lo.append(0);hi.append(np.inf);r+=1
    for a in range(n):rr.append(r);cc.append(x0+a);dd.append(1)
    lo.append(10);hi.append(10);r+=1
    rr.append(r);cc.append(x0+z);dd.append(1);lo.append(0);hi.append(0);r+=1
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
    others=[charts[ci][1:] for ci,_ in inc];N20=set().union(*map(set,others));outside=set(range(1620))-{z}-N20
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
            b=ndir[a].get(u)
            if b is not None:m|=1<<b
        return m
    def spoil_ok(E,s):return all(mask_to(a,E-{a}).bit_count()>=s for a in E)
    def vote0(mask5):
        m=sum(((mask5>>(p-1))&1)<<p for p in range(1,6));return (LEAD[syn(m)]&1)!=0

    stopping10_infeasible(charts);false_v2_infeasible(charts,ach,z)

    # V=3 local census.
    local3=defaultdict(list)
    for ms in itertools.product(range(32),repeat=4):
        w=sum(x.bit_count() for x in ms)
        if w>10:continue
        if sum(vote0(x) for x in ms)!=3:continue
        E=set()
        for q,x in enumerate(ms):
            for j,a in enumerate(others[q]):
                if (x>>j)&1:E.add(a)
        local3[w].append(frozenset(E))
    assert [len(local3[w]) for w in (6,7,8,9,10)]==[32,256,832,1536,1856]
    deficit_profiles={}
    for w in (6,7,8,9,10):
        h=Counter()
        for core in local3[w]:
            L=set(core);h[sum(max(0,2-mask_to(a,L-{a}).bit_count()) for a in L)]+=1
        deficit_profiles[str(w)]={str(k):v for k,v in sorted(h.items())}
    assert deficit_profiles=={'6':{'6':32},'7':{'7':96,'8':160},'8':{'8':352,'9':480},'9':{'9':1056,'10':480},'10':{'10':1696,'11':160}}

    # For every local V3 core, one outsider can add a new direction to at most two core errors.
    contrib_cap=0
    v3_status=Counter();v3_traces=Counter();v3_solution_profile=Counter();v3_total=0
    for core in local3[6]:
        L=set(core);base={a:mask_to(a,L-{a}) for a in L};contrib={}
        for u in outside:
            items=[]
            for a in L:
                b=ndir[a].get(u)
                if b is not None and not ((base[a]>>b)&1):items.append((a,b))
            if items:contrib[u]=tuple(items);contrib_cap=max(contrib_cap,len(items))
        dbl=[u for u,it in contrib.items() if len(it)==2];sng=[u for u,it in contrib.items() if len(it)==1];zero=[u for u in outside if u not in contrib]
        sols=set()
        # No zero-contribution outsider: at least two doubles are needed to cover six deficits with four outsiders.
        for nd in range(2,min(4,len(dbl))+1):
            for D in itertools.combinations(dbl,nd):
                for S in itertools.combinations(sng,4-nd):
                    O=D+S;E=L|set(O)
                    if spoil_ok(E,2):sols.add(tuple(sorted(O)))
        # One zero-contribution outsider: the other three must all be doubles and already cover all six core deficits.
        for D in itertools.combinations(dbl,3):
            LD=L|set(D)
            if not all(mask_to(a,LD-{a}).bit_count()>=2 for a in L):continue
            for u in zero:
                E=LD|{u}
                if spoil_ok(E,2):sols.add(tuple(sorted(D+(u,))))
        v3_solution_profile[len(sols)]+=1;v3_total+=len(sols)
        for O in sols:
            R=decode(L|set(O),charts,ach,adj);v3_status[R['status']]+=1;v3_traces[tuple(R['trace'])]+=1
    assert contrib_cap==2
    assert v3_solution_profile==Counter({8:12,32:8,58:4,0:4,178:4})
    assert v3_total==1296 and v3_status==Counter({'clear':1296})
    # For w>=7 the minimum core-direction deficit exceeds 2*(10-w), so no necessary survivor exists.
    assert min(map(int,deficit_profiles['7']))>2*3
    assert min(map(int,deficit_profiles['8']))>2*2
    assert min(map(int,deficit_profiles['9']))>2*1
    assert min(map(int,deficit_profiles['10']))>0

    # V=4 complete necessary-survivor census.
    two=[(1,2),(3,4)];three=[(1,4,5),(2,3,5)]
    cores8=[];cores9=[];cores10=[]
    for choices in itertools.product(range(2),repeat=4):
        E=set()
        for q in range(4):E.update(others[q][p-1] for p in two[choices[q]])
        cores8.append(frozenset(E))
    for heavy in range(4):
        for choices in itertools.product(range(2),repeat=4):
            E=set()
            for q in range(4):
                pat=three[choices[q]] if q==heavy else two[choices[q]];E.update(others[q][p-1] for p in pat)
            cores9.append(frozenset(E))
    for heavies in itertools.combinations(range(4),2):
        for choices in itertools.product(range(2),repeat=4):
            E=set()
            for q in range(4):
                pat=three[choices[q]] if q in heavies else two[choices[q]];E.update(others[q][p-1] for p in pat)
            cores10.append(frozenset(E))
    assert (len(cores8),len(cores9),len(cores10))==(16,64,96)
    outside_edges=[(u,v) for u in sorted(outside) for v in adj[u] if v in outside and u<v];assert len(outside_edges)==15840
    v4_status=Counter();v4_traces=Counter();n82=0;n91=0;n100=0;Nprof=Counter();EAprof=Counter()
    for core in cores8:
        A=set().union(*(adj[a]&outside for a in core));pairs=set(itertools.combinations(sorted(A),2));eA=0
        for e in outside_edges:
            if e[0] in A and e[1] in A:eA+=1
            pairs.add(e)
        Nprof[(len(A),len(pairs))]+=1;EAprof[(len(A),eA)]+=1
        for u,v in pairs:
            n82+=1;R=decode(set(core)|{u,v},charts,ach,adj);v4_status[R['status']]+=1;v4_traces[tuple(R['trace'])]+=1
    assert Nprof==Counter({(104,20928):8,(112,21780):8}) and EAprof==Counter({(104,268):8,(112,276):8})
    for core in cores9:
        A=set().union(*(adj[a]&outside for a in core));n91+=len(A)
        for u in A:
            R=decode(set(core)|{u},charts,ach,adj);v4_status[R['status']]+=1;v4_traces[tuple(R['trace'])]+=1
    for core in cores10:
        n100+=1;R=decode(core,charts,ach,adj);v4_status[R['status']]+=1;v4_traces[tuple(R['trace'])]+=1
    assert (n82,n91,n100)==(341664,7808,96)
    assert v4_status==Counter({'clear':349568})
    raw=16*math.comb(1599,2)+64*1599+96;assert raw==20544048

    out={
      'pass':5430,'status':'COMPUTATIONAL_THEOREM_Q3_GLOBAL_EVENTUAL_RADIUS10',
      'prior':'Pass5381 proves global eventual radius9.',
      'V1':'Exact fixed-coordinate weight10 stopping-set MILP infeasible.',
      'V2':'Exact false-center V=2, spoiled>=3 MILP infeasible.',
      'V3':{'local_counts_w6_to_w10':[32,256,832,1536,1856],'deficit_profiles':deficit_profiles,'new_core_direction_cap_per_outsider':2,'necessary_survivors':v3_total,'solution_count_profile':{str(k):v for k,v in sorted(v3_solution_profile.items())},'decoder_status':dict(v3_status),'trace_histogram':{str(k):v for k,v in v3_traces.items()}},
      'V4':{'raw_rooted_count':raw,'necessary_pruned_counts':{'8local_plus2':n82,'9local_plus1':n91,'10local':n100,'total':n82+n91+n100},'decoder_status':dict(v4_status),'trace_histogram':{str(k):v for k,v in v4_traces.items()}},
      'decoder_conclusion':'Every weight10 error either makes a nonempty true-only first correction and falls into the certified radius9 basin, or belongs to an exhaustively classified false-survivor sector that clears under the actual decoder.',
      'guaranteed_eventual_radius':10,'guaranteed_monotone_true_only_radius':7,
      'boundary':'Computational theorem for the deterministic q3 provenance decoder. Radius11 remains open; the monotone guarantee remains7 because radius8 echoes make false first corrections.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
