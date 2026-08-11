#!/usr/bin/env python3
"""Pass 4828 — exact parametric hot/cold phase diagrams for six outage cases.

For a fixed failure case, PSp-failure-stabilizer reduction gives edge orbits and
ordered-pair commodity orbits exactly as in Pass4820. Give every surviving cold
edge capacity 1 and every surviving hot edge capacity rho>0. The metric dual has
objective

    A(y) + rho B(y),

so the optimum throughput is the lower envelope of affine rational lines. An
adaptive exact oracle discovers all envelope lines: solve at seed rho values,
construct the finite lower envelope, query every segment and breakpoint, and add
any newly exposed dual line until closure. Each oracle call reconstructs matching
rational primal/dual certificates and checks exact shortest-path separation.
"""
from __future__ import annotations
import itertools,json,math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import networkx as nx
import numpy as np
from scipy.optimize import linprog
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4828_PARAMETRIC_OUTAGE_FLOW.json'

def path_sig(path,er,r):
    z=[0]*r
    for u,v in zip(path,path[1:]):z[er[tuple(sorted((u,v)))]]+=1
    return tuple(z)

def build_case(D,B,F,node_remove):
    Gp=D['G'];res=D['residues'];phi=D['phiR'];ridx={r:i for i,r in enumerate(res)};invphi={v:k for k,v in phi.items()}
    def ar(i,g):return ridx[tuple(sorted(g[x] for x in res[i]))]
    def av(v,g):return phi[ar(invphi[v],g)]
    hot={tuple(sorted(e)) for e in B['hot']};cold={tuple(sorted(e)) for e in B['cold']};allE=hot|cold
    K5=B['K5'];owner=[]
    for T in B['projected']:
        h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])
    fibers=[set(i for i,a in enumerate(owner) if a==f) for f in range(27)]
    def fp(g):return tuple(owner[av(min(fibers[f]),g)] for f in range(27))
    FF=set(F);H=[g for g in Gp if {fp(g)[f] for f in FF}==FF]
    rem=set().union(*(fibers[f] for f in FF)) if node_remove else set();V=sorted(set(range(270))-rem);E=set(allE)
    if node_remove:E={e for e in E if not (set(e)&rem)}
    else:E={e for e in E if not (e in hot and owner[e[0]] in FF)}
    acts=[tuple(av(i,g) for i in range(270)) for g in H]
    unseen=set(E);EO=[]
    while unseen:
        u,v=next(iter(unseen));O={tuple(sorted((a[u],a[v]))) for a in acts};EO.append(O);unseen-=O
    er={e:i for i,O in enumerate(EO) for e in O};etype=[]
    for O in EO:
        e=next(iter(O));etype.append('hot' if e in hot else 'cold');assert all((x in hot)==(etype[-1]=='hot') for x in O)
    unseen={(u,v) for u in V for v in V if u!=v};PO=[]
    while unseen:
        s,t=next(iter(unseen));O={(a[s],a[t]) for a in acts};PO.append(O);unseen-=O
    reps=[next(iter(O)) for O in PO];G=nx.Graph();G.add_nodes_from(V);G.add_edges_from(E)
    bys=defaultdict(list)
    for k,(s,t) in enumerate(reps):bys[s].append((k,t))
    return {'F':tuple(F),'node_remove':node_remove,'H':H,'V':V,'E':E,'EO':EO,'er':er,'etype':etype,'PO':PO,'reps':reps,'G':G,'bys':bys}

def oracle(C,rho):
    rho=Fraction(rho);EO=C['EO'];PO=C['PO'];er=C['er'];etype=C['etype'];G=C['G'];bys=C['bys'];r=len(EO);K=len(PO)
    paths=[set() for _ in range(K)]
    for s,kt in bys.items():
        P=nx.single_source_shortest_path(G,s)
        for k,t in kt:paths[k].add(path_sig(P[t],er,r))
    it=0
    while True:
        n=r+K;c=np.zeros(n)
        for i,O in enumerate(EO):c[i]=len(O)*(float(rho) if etype[i]=='hot' else 1.0)
        Au=[];bu=[];row=np.zeros(n);row[r:]=[-len(O) for O in PO];Au.append(row);bu.append(-1.)
        for k,PS in enumerate(paths):
            for sg in PS:
                row=np.zeros(n);row[:r]=-np.array(sg,float);row[r+k]=1;Au.append(row);bu.append(0.)
        dual=linprog(c,A_ub=np.array(Au),b_ub=np.array(bu),bounds=[(0,None)]*n,method='highs');assert dual.success
        y=dual.x[:r];dd=dual.x[r:]
        for e in G.edges():G.edges[e]['weight']=y[er[tuple(sorted(e))]]
        adds=0
        for s,kt in bys.items():
            dist,P=nx.single_source_dijkstra(G,s,weight='weight')
            for k,t in kt:
                if dd[k]>dist[t]+1e-9:
                    sg=path_sig(P[t],er,r)
                    if sg not in paths[k]:paths[k].add(sg);adds+=1
        it+=1
        if not adds:break
        assert it<60
    # finite matching primal with capacities 1/rho by type
    plist=[list(P) for P in paths];off=[];tot=0
    for P in plist:off.append(tot);tot+=len(P)
    nv=tot+1;zidx=tot;cp=np.zeros(nv);cp[zidx]=1
    Aeq=np.zeros((K,nv));beq=np.ones(K)
    for k,P in enumerate(plist):Aeq[k,off[k]:off[k]+len(P)]=1
    Aup=np.zeros((r,nv))
    for rr,O in enumerate(EO):
        for k,P in enumerate(plist):
            coef=len(PO[k])/len(O)
            for j,sg in enumerate(P):Aup[rr,off[k]+j]=coef*sg[rr]
        cap=float(rho) if etype[rr]=='hot' else 1.0;Aup[rr,zidx]=-cap
    primal=linprog(cp,A_ub=Aup,b_ub=np.zeros(r),A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*nv,method='highs');assert primal.success
    q=lambda x:Fraction(float(x)).limit_denominator(10**9)
    yr=[q(x) for x in dual.x[:r]];dr=[q(x) for x in dual.x[r:]];xr=[q(x) for x in primal.x[:-1]];z=q(primal.fun)
    A=sum(Fraction(len(EO[i]))*yr[i] for i in range(r) if etype[i]=='cold')
    Bc=sum(Fraction(len(EO[i]))*yr[i] for i in range(r) if etype[i]=='hot')
    lam=A+rho*Bc;assert lam==q(dual.fun) and z==1/lam
    assert sum(Fraction(len(PO[k]))*dr[k] for k in range(K))==1
    # exact shortest-path dual separation
    L=1
    for x in yr:L=math.lcm(L,x.denominator)
    for e in G.edges():G.edges[e]['iw']=int(yr[er[tuple(sorted(e))]]*L)
    for s,kt in bys.items():
        dist=nx.single_source_dijkstra_path_length(G,s,weight='iw')
        for k,t in kt:assert dr[k]<=Fraction(dist[t],L)
    for k,P in enumerate(plist):assert sum(xr[off[k]+j] for j in range(len(P)))==1
    loads=[]
    for rr,O in enumerate(EO):
        zload=Fraction(0)
        for k,P in enumerate(plist):
            coef=Fraction(len(PO[k]),len(O))
            for j,sg in enumerate(P):zload+=coef*sg[rr]*xr[off[k]+j]
        cap=rho if etype[rr]=='hot' else Fraction(1);loads.append(zload/cap if cap else Fraction(0) if zload==0 else Fraction(10**30))
    assert max(loads)==z
    return {'rho':rho,'line':(A,Bc),'lambda':lam,'iterations':it,'paths':sum(map(len,paths))}

def envelope(lines):
    lines=sorted(set(lines));xs={Fraction(0)}
    for (A,B),(C,D) in itertools.combinations(lines,2):
        if B!=D:
            x=Fraction(C-A,B-D)
            if x>=0:xs.add(x)
    xs=sorted(xs);pieces=[]
    bounds=xs+[None]
    for i,left in enumerate(bounds):
        if left is None:break
        right=bounds[i+1] if i+1<len(bounds) else None
        t=(left+right)/2 if right is not None else left+max(Fraction(1),left+1)
        vals=[(A+B*t,(A,B)) for A,B in lines];m=min(v for v,L in vals);best=min(L for v,L in vals if v==m)
        if pieces and pieces[-1][2]==best:pieces[-1]=(pieces[-1][0],right,best)
        else:pieces.append((left,right,best))
    # Keep only actual lower-envelope pieces; zero-width break intervals naturally vanish later.
    return pieces

def discover(C):
    seen={};seed=[Fraction(0),Fraction(1,4),Fraction(1),Fraction(4),Fraction(16),Fraction(64)]
    def ask(x):
        if x not in seen:seen[x]=oracle(C,x)
        return seen[x]
    for x in seed:ask(x)
    while not any(v['line'][1]==0 for v in seen.values()):
        x=max(seen)*2;ask(x);assert x<4096
    lines=set(v['line'] for v in seen.values())
    for _round in range(20):
        changed=False;P=envelope(lines)
        tests=set()
        for left,right,L in P:
            if right is None:tests.add(left+max(Fraction(1),left+1))
            elif right>left:tests.add((left+right)/2);tests.add(right)
        for x in sorted(tests):
            o=ask(x)
            if o['line'] not in lines:lines.add(o['line']);changed=True
        if not changed:break
    assert not changed
    # ordered active lines and exact transition breakpoints
    P=envelope(lines);active=[]
    for left,right,L in P:
        if right is not None and right==left:continue
        if active and active[-1]==L:continue
        active.append(L)
    br=[]
    for (A,B),(C,D) in zip(active,active[1:]):
        assert B!=D;x=Fraction(C-A,B-D);assert x>0;br.append(x)
    # Validate one point in every final region plus each breakpoint.
    bounds=[Fraction(0)]+br+[None]
    for i,L in enumerate(active):
        left=bounds[i];right=bounds[i+1]
        t=(left+right)/2 if right is not None else left+max(Fraction(1),left+1)
        o=ask(t);assert o['line']==L and o['lambda']==L[0]+L[1]*t
        if right is not None:
            o=ask(right);assert o['lambda']==min(A+B*right for A,B in active)
    return active,br,seen

def fs(x):return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'
def main():
    D=build_all();B=build_bundle();K5=B['K5'];qG=nx.Graph();qG.add_nodes_from(range(27))
    for a,b in itertools.combinations(range(27),2):
        if K5[a]&K5[b]:qG.add_edge(a,b)
    adj=next(iter(qG.edges()));non=next((a,b) for a,b in itertools.combinations(range(27),2) if not qG.has_edge(a,b))
    specs=[('one_hot',(0,),False),('two_hot_adjacent',adj,False),('two_hot_nonadjacent',non,False),('one_vertex_fiber_removed',(0,),True),('two_vertex_adjacent_removed',adj,True),('two_vertex_nonadjacent_removed',non,True)]
    cases={};intact={Fraction(63,155),Fraction(111,137),Fraction(239,105)}
    for name,F,nr in specs:
        C=build_case(D,B,F,nr);active,br,seen=discover(C)
        pieces=[]
        for i,(A,Bc) in enumerate(active):
            lo=Fraction(0) if i==0 else br[i-1];hi=None if i==len(active)-1 else br[i]
            pieces.append({'rho_low':fs(lo),'rho_high':None if hi is None else fs(hi),'lambda':f'{fs(A)} + ({fs(Bc)})*rho','A':fs(A),'B':fs(Bc)})
        one=oracle(C,Fraction(1));cases[name]={'failed_fibers':list(F),'node_removal':nr,'failure_stabilizer_order':len(C['H']),'edge_orbits':len(C['EO']),'ordered_pair_orbits':len(C['PO']),'breakpoints':[fs(x) for x in br],'pieces':pieces,'lambda_at_rho1':fs(one['lambda']),'shares_intact_breakpoint':[fs(x) for x in br if x in intact],'oracle_calls':len(seen)}
    out={'pass':4828,'capacity_model':'cold edge capacity 1, surviving hot edge capacity rho>0; unit ordered-pair demand among surviving vertices','cases':cases,
      'intact_breakpoints':['63/155','111/137','239/105'],
      'theorem':'Each of the six symmetry-broken outage throughput functions is the exact lower envelope of finitely many rational affine dual metrics A+B rho. Adaptive stabilizer-reduced primal/dual separation discovers and certifies every active line and breakpoint without assuming the intact-router phase structure survives failure.',
      'boundary':'Exact splittable fractional multicommodity flow. No queueing, unsplittable routing, latency or measured hardware performance is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
