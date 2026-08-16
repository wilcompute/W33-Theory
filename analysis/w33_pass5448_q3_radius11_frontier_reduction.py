#!/usr/bin/env python3
"""Pass5448: exact q=3 radius-eleven frontier reduction.

Pass5430 proves global eventual radius10.  Fix a false candidate z.  As before
V<=4 and a true error needs at least 5-V spoiled incident charts for z to survive
max-vote/max-singleton provenance.

This pass does NOT close radius11.  It proves:
- V=1: exact weight11 stopping-set MILP infeasible.
- V=2: exact weight11 false-center/spoiled>=3 MILP infeasible.
- V=3: local weights6..11 occur 32,256,832,1536,1856,1536 times.  One outsider
  supplies at most two new local chart directions.  Therefore local weights>=8
  cannot survive at total weight11.  Only weight6+5 outsiders and weight7+4
  outsiders remain. Exact MILPs exhibit necessary survivors in both branches;
  the returned witnesses self-heal under the actual decoder.
- V=4: the raw rooted count is
    16*C(1599,3)+64*C(1599,2)+96*1599+64 = 10,963,673,616.
  Requiring every outsider to be adjacent in the chart-sharing graph to the core
  or another outsider leaves exactly35,218,336 necessary cases.  The count is
  obtained analytically from the outside graph and the 16/64/96/64 local cores.
  An exact MILP returns a necessary V4 witness, which also self-heals.

The remaining radius11 task is exhaustive decoding/classification of the two V3
branches and the 35,218,336 pruned V4 cases.
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
OUT=ROOT/'data/PART_W33_PASS5448_Q3_RADIUS11_FRONTIER_REDUCTION.json'
PAIRS=list(itertools.combinations(range(4),2));LEAD=[0,8,16,1,32,2,4,0]

def syn(m):
    return (((m>>0&1)^(m>>1&1)^(m>>3&1)))|((((m>>0&1)^(m>>2&1)^(m>>4&1)))<<1)|((((m>>1&1)^(m>>2&1)^(m>>5&1)))<<2)

def build():
    G=build_W(3);charts=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    ach=[[] for _ in G['apartments']];adj=[set() for _ in G['apartments']]
    for ci,C in enumerate(charts):
        for p,a in enumerate(C):ach[a].append((ci,p))
        for a in C:adj[a].update(x for x in C if x!=a)
    return charts,ach,adj

def sweep(E,charts,ach,adj):
    touched={}
    for a in E:
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

def decode(E,charts,ach,adj,limit=30):
    E=set(E);seen=set();trace=[len(E)]
    for _ in range(limit+1):
        if not E:return ('clear',trace)
        key=tuple(sorted(E))
        if key in seen:return ('cycle',trace)
        seen.add(key);corr=sweep(E,charts,ach,adj)
        if not corr:return ('stuck',trace)
        E.symmetric_difference_update(corr);trace.append(len(E))
    return ('limit',trace)

def exact_false_sector_milp(charts,ach,weight,V,spoil,local_weight=None):
    n=1620;m=len(charts);z=0;inc=[ci for ci,_ in ach[z]];others=[charts[ci][1:] for ci in inc]
    N20=set().union(*map(set,others));x0=0;w0=n;h0=n+m;NV=h0+4*32
    rr=[];cc=[];dd=[];lo=[];hi=[];r=0
    for ci,C in enumerate(charts):
        for a in C:rr.append(r);cc.append(a);dd.append(1)
        rr.append(r);cc.append(w0+ci);dd.append(-2);lo.append(0);hi.append(np.inf);r+=1
        for a in C:rr.append(r);cc.append(a);dd.append(1)
        rr.append(r);cc.append(w0+ci);dd.append(-5);lo.append(-np.inf);hi.append(1);r+=1
    for a in range(n):
        for ci,_ in ach[a]:rr.append(r);cc.append(w0+ci);dd.append(1)
        rr.append(r);cc.append(a);dd.append(-spoil);lo.append(0);hi.append(np.inf);r+=1
    for a in range(n):rr.append(r);cc.append(a);dd.append(1)
    lo.append(weight);hi.append(weight);r+=1
    rr.append(r);cc.append(z);dd.append(1);lo.append(0);hi.append(0);r+=1
    if local_weight is not None:
        for a in N20:rr.append(r);cc.append(a);dd.append(1)
        lo.append(local_weight);hi.append(local_weight);r+=1
    def vote0(mask5):
        mm=sum(((mask5>>(p-1))&1)<<p for p in range(1,6));return int((LEAD[syn(mm)]&1)!=0)
    for q in range(4):
        for mask in range(32):rr.append(r);cc.append(h0+32*q+mask);dd.append(1)
        lo.append(1);hi.append(1);r+=1
        for j,a in enumerate(others[q]):
            rr.append(r);cc.append(a);dd.append(1)
            for mask in range(32):
                if (mask>>j)&1:rr.append(r);cc.append(h0+32*q+mask);dd.append(-1)
            lo.append(0);hi.append(0);r+=1
    for q in range(4):
        for mask in range(32):
            if vote0(mask):rr.append(r);cc.append(h0+32*q+mask);dd.append(1)
    lo.append(V);hi.append(V);r+=1
    A=sparse.csr_matrix((dd,(rr,cc)),shape=(r,NV))
    res=milp(np.zeros(NV),integrality=np.ones(NV),bounds=Bounds(np.zeros(NV),np.ones(NV)),
      constraints=LinearConstraint(A,np.array(lo),np.array(hi)),options={'presolve':True})
    if res.status==2:return None
    assert res.status==0,res.message
    return set(np.flatnonzero(res.x[:n]>.5))

def stopping11_infeasible(charts):
    n=1620;m=len(charts);off=n;NV=n+m;rr=[];cc=[];dd=[];lo=[];hi=[];r=0
    for ci,C in enumerate(charts):
        for a in C:rr.append(r);cc.append(a);dd.append(1)
        rr.append(r);cc.append(off+ci);dd.append(-2);lo.append(0);hi.append(np.inf);r+=1
        for a in C:rr.append(r);cc.append(a);dd.append(1)
        rr.append(r);cc.append(off+ci);dd.append(-6);lo.append(-np.inf);hi.append(0);r+=1
    for a in range(n):rr.append(r);cc.append(a);dd.append(1)
    lo.append(11);hi.append(11);r+=1
    rr.append(r);cc.append(0);dd.append(1);lo.append(1);hi.append(1);r+=1
    A=sparse.csr_matrix((dd,(rr,cc)),shape=(r,NV))
    res=milp(np.zeros(NV),integrality=np.ones(NV),bounds=Bounds(np.zeros(NV),np.ones(NV)),
      constraints=LinearConstraint(A,np.array(lo),np.array(hi)),options={'presolve':True})
    assert res.status==2,res.message

def main():
    charts,ach,adj=build();z=0;inc=ach[z];assert {p for _,p in inc}=={0};others=[charts[ci][1:] for ci,_ in inc]
    N20=set().union(*map(set,others));outside=set(range(1620))-{z}-N20;assert len(outside)==1599
    ndir=[]
    for a in range(1620):
        d={}
        for bit,(ci,p) in enumerate(ach[a]):
            for u in charts[ci]:
                if u!=a:d[u]=bit
        ndir.append(d)
    def mask_to(a,S):
        m=0
        for u in S:
            b=ndir[a].get(u)
            if b is not None:m|=1<<b
        return m
    def vote0(mask5):
        mm=sum(((mask5>>(p-1))&1)<<p for p in range(1,6));return (LEAD[syn(mm)]&1)!=0

    stopping11_infeasible(charts)
    assert exact_false_sector_milp(charts,ach,11,2,3) is None

    local3=defaultdict(list)
    for ms in itertools.product(range(32),repeat=4):
        w=sum(x.bit_count() for x in ms)
        if w>11 or sum(vote0(x) for x in ms)!=3:continue
        E=set()
        for q,x in enumerate(ms):
            for j,a in enumerate(others[q]):
                if (x>>j)&1:E.add(a)
        local3[w].append(frozenset(E))
    counts=[len(local3[w]) for w in range(6,12)];assert counts==[32,256,832,1536,1856,1536]
    deficits={}
    for w in range(6,12):
        h=Counter()
        for core in local3[w]:
            L=set(core);h[sum(max(0,2-mask_to(a,L-{a}).bit_count()) for a in L)]+=1
        deficits[str(w)]={str(k):v for k,v in sorted(h.items())}
    assert min(map(int,deficits['8']))>2*(11-8)
    assert min(map(int,deficits['9']))>2*(11-9)
    assert min(map(int,deficits['10']))>2*(11-10)
    assert min(map(int,deficits['11']))>0
    v3w6=exact_false_sector_milp(charts,ach,11,3,2,6);v3w7=exact_false_sector_milp(charts,ach,11,3,2,7)
    assert v3w6 is not None and v3w7 is not None
    d6=decode(v3w6,charts,ach,adj);d7=decode(v3w7,charts,ach,adj);assert d6[0]==d7[0]=='clear'

    two=[(1,2),(3,4)];three=[(1,4,5),(2,3,5)]
    def cores(h):
        out=[]
        for Ht in itertools.combinations(range(4),h):
            H=set(Ht)
            for ch in itertools.product(range(2),repeat=4):
                E=set()
                for q in range(4):
                    pat=three[ch[q]] if q in H else two[ch[q]]
                    E.update(others[q][p-1] for p in pat)
                out.append(frozenset(E))
        return out
    c8,c9,c10,c11=(cores(h) for h in range(4));assert list(map(len,(c8,c9,c10,c11)))==[16,64,96,64]
    outside_edges=[(u,v) for u in sorted(outside) for v in adj[u] if v in outside and u<v];Eout=len(outside_edges);assert Eout==15840
    def valid3_count(core):
        A=set().union(*(adj[a]&outside for a in core));B=outside-A;a=len(A)
        c0=math.comb(a,3)
        c1=sum(math.comb(a,2)-math.comb(a-len(adj[b]&A),2) for b in B)
        Bedges=[(u,v) for u in B for v in adj[u]&B if u<v]
        total_common=sum(math.comb(len(adj[x]&B),2) for x in A)
        edge_common=sum(len(adj[u]&adj[v]&A) for u,v in Bedges)
        c2=len(Bedges)*a+total_common-edge_common
        wedge=sum(math.comb(len(adj[b]&B),2) for b in B)
        tri3=sum(len(adj[u]&adj[v]&B) for u,v in Bedges);assert tri3%3==0
        tri=tri3//3;c3=wedge-2*tri
        return (a,c0,c1,c2,c3,c0+c1+c2+c3,len(Bedges),tri)
    p8=Counter(valid3_count(c) for c in c8)
    assert p8==Counter({(104,182104,143746,1479768,219619,2025237,14168,17902):8,(112,227920,169102,1578536,216567,2192125,14032,17670):8})
    def valid2_count(core):
        A=set().union(*(adj[a]&outside for a in core));eA=sum(1 for u,v in outside_edges if u in A and v in A)
        return (len(A),math.comb(len(A),2)+Eout-eA,eA)
    p9=Counter(valid2_count(c) for c in c9)
    assert p9==Counter({(121,22787,313):16,(123,23027,316):16,(117,22317,309):8,(125,23273,317):8,(119,22551,310):8,(127,23523,318):8})
    p10=Counter(len(set().union(*(adj[a]&outside for a in c))) for c in c10)
    assert p10==Counter({138:48,134:32,133:16})
    n8=sum(k[5]*v for k,v in p8.items());n9=sum(k[1]*v for k,v in p9.items());n10=sum(k*v for k,v in p10.items());n11=len(c11)
    assert (n8,n9,n10,n11,n8+n9+n10+n11)==(33738896,1466336,13040,64,35218336)
    raw=16*math.comb(1599,3)+64*math.comb(1599,2)+96*1599+64;assert raw==10963673616
    v4wit=exact_false_sector_milp(charts,ach,11,4,1);assert v4wit is not None
    d4=decode(v4wit,charts,ach,adj);assert d4[0]=='clear'

    out={
      'pass':5448,'status':'THEOREM_Q3_RADIUS11_EXACT_FRONTIER_REDUCTION_NOT_CLOSURE',
      'V1':'weight11 stopping-set MILP infeasible',
      'V2':'weight11 false-center/spoiled>=3 MILP infeasible',
      'V3':{'local_counts_w6_to_w11':counts,'direction_deficit_histograms':deficits,
        'surviving_local_weights':[6,7],
        'weight6_MILP_witness':sorted(v3w6),'weight6_witness_trace':d6[1],
        'weight7_MILP_witness':sorted(v3w7),'weight7_witness_trace':d7[1]},
      'V4':{'raw_rooted_count':raw,'necessary_pruned_counts':{'8local_plus3':n8,'9local_plus2':n9,'10local_plus1':n10,'11local':n11,'total':n8+n9+n10+n11},
        'local8_three_outsider_profile':{str(k):v for k,v in p8.items()},
        'local9_two_outsider_profile':{str(k):v for k,v in p9.items()},
        'local10_one_outsider_profile':{str(k):v for k,v in p10.items()},
        'MILP_witness':sorted(v4wit),'witness_trace':d4[1]},
      'conclusion':'V1 and V2 are closed. V3 is reduced to two explicit local-weight branches. V4 is reduced from10.96B raw rooted cases to35,218,336 necessary cases. Representative necessary survivors in every remaining branch self-heal.',
      'boundary':'Global eventual radius11 is NOT proved. Exhaustive completion/decoding of V3 weights6,7 and all35,218,336 pruned V4 cases remains open.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
