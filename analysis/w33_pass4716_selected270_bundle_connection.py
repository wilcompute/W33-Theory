#!/usr/bin/env python3
"""Pass 4716 — reconstruct selected270 from a finite graph-bundle connection.

The selected135 graph is a connected three-sheet cover of the 45-point
GQ(4,2) point graph.  Each base edge carries a perfect matching of its two
three-point packets, hence an S3 connection.  Every one of the 270 base
triangles has transposition holonomy; its unique fixed sheet reconstructs one
selected singular line.  Their intersection graph is exactly selected270.

The 27 GQ lines become the 27 Petersen fibers of selected270.  Across adjacent
fibers the 12 base edges split as three K2,2 blocks indexed by the three
internal coordinates of their shared 45-packet.  This gives an explicit finite
connection law for rebuilding the full router from its quotient data.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4716_SELECTED270_BUNDLE_CONNECTION_REGEN.json'

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def invperm(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def orderperm(p):
    seen=set();o=1
    import math
    for i in range(len(p)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=p[j]
        o=math.lcm(o,n)
    return o

def build_bundle():
    _,_,_,_,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8);apartments=sorted(tuple(map(int,a)) for a in apartments)
    j=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]])
    rep=lambda x:min(int(x),int(x)^j)
    def fib(ap):
        z=0
        for i in ap:z^=cols[i]
        return rep(z)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(a) for a in apartments});sing=sorted(set().union(*(set(L) for L in selected)));sidx={x:i for i,x in enumerate(sing)}
    N=np.zeros((135,270),dtype=np.int64)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    Ap=N@N.T-6*np.eye(135,dtype=np.int64);Al=N.T@N-3*np.eye(270,dtype=np.int64)

    # The 45 packets can be recovered directly from apartment fibers: the three
    # singular fibers with the same 16-line support form one packet.
    fibers=defaultdict(list)
    for ap in apartments:fibers[fib(ap)].append(ap)
    support_to_s=defaultdict(list)
    for s,F in fibers.items():support_to_s[frozenset().union(*(set(ap) for ap in F))].append(s)
    packets=sorted((tuple(sorted(sidx[x] for x in S)) for S in support_to_s.values()))
    assert len(packets)==45 and Counter(i for T in packets for i in T)==Counter({i:1 for i in range(135)})
    packet_of={x:p for p,T in enumerate(packets) for x in T}

    # Base graph and the perfect-matching connection.
    G45=nx.Graph();G45.add_nodes_from(range(45));sig={}
    for p,q in itertools.combinations(range(45),2):
        E=[(i,j) for i,x in enumerate(packets[p]) for j,y in enumerate(packets[q]) if Ap[x,y]]
        if E:
            assert len(E)==3 and Counter(i for i,j in E)==Counter({0:1,1:1,2:1}) and Counter(j for i,j in E)==Counter({0:1,1:1,2:1})
            G45.add_edge(p,q);s=tuple(next(j for ii,j in E if ii==i) for i in range(3));sig[(p,q)]=s;sig[(q,p)]=invperm(s)
    assert set(dict(G45.degree()).values())=={12} and nx.is_connected(G45)

    projected=[]
    for L in selected:
        T=tuple(sorted(packet_of[sidx[x]] for x in L));assert len(set(T))==3;projected.append(T)
    assert len(set(projected))==270
    def hol(T):
        a,b,c=sorted(T);return compose(sig[(c,a)],compose(sig[(b,c)],sig[(a,b)]))
    hc=Counter();recovered=[]
    for T in projected:
        a,b,c=sorted(T);h=hol(T);hc[h]+=1;assert orderperm(h)==2
        fixed=[i for i in range(3) if h[i]==i];assert len(fixed)==1
        ia=fixed[0];ib=sig[(a,b)][ia];ic=sig[(b,c)][ib]
        recovered.append(tuple(sorted((packets[a][ia],packets[b][ib],packets[c][ic]))))
    original=[tuple(sorted(sidx[x] for x in L)) for L in selected]
    assert recovered==original
    R=np.zeros((135,270),dtype=np.int64)
    for c,T in enumerate(recovered):R[list(T),c]=1
    assert np.array_equal(R,N) and np.array_equal(R.T@R-3*np.eye(270,dtype=np.int64),Al)

    # Gauge the S3 connection on a spanning tree.
    parent={0:None};gauge={0:(0,1,2)};Q=deque([0])
    while Q:
        p=Q.popleft()
        for q in sorted(G45[p]):
            if q in parent:continue
            parent[q]=p;gauge[q]=compose(sig[(p,q)],gauge[p]);Q.append(q)
    tree={tuple(sorted((v,parent[v]))) for v in parent if parent[v] is not None}
    cot=Counter()
    for p,q in sorted(G45.edges()):
        if (p,q) in tree:continue
        z=compose(invperm(gauge[q]),compose(sig[(p,q)],gauge[p]));cot[z]+=1
    assert cot==Counter({(0,1,2):64,(1,0,2):54,(0,2,1):54,(2,1,0):54})

    # Reconstruct 27 GQ lines as maximal K5s and classify selected270 fibers.
    K5=sorted((frozenset(c) for c in nx.find_cliques(G45) if len(c)==5),key=lambda S:tuple(sorted(S)));assert len(K5)==27
    owner=[]
    for T in projected:
        h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])
    assert Counter(owner)==Counter({i:10 for i in range(27)})
    hot=[];cold=[]
    for u in range(270):
        for v in range(u+1,270):
            if Al[u,v]:(hot if owner[u]==owner[v] else cold).append((u,v))
    assert (len(hot),len(cold))==(405,1620)
    H=nx.Graph();H.add_nodes_from(range(270));H.add_edges_from(hot)
    C=[frozenset(c) for c in nx.connected_components(H)];assert len(C)==27 and all(len(c)==10 and nx.is_isomorphic(H.subgraph(c),nx.petersen_graph()) for c in C)

    # Exact cross-fiber law: adjacent quotient lines share one packet.  The 12
    # cold edges are 3 disjoint K2,2 blocks, one per singular coordinate there.
    laws=Counter()
    for a,b in itertools.combinations(range(27),2):
        common=K5[a]&K5[b]
        cross=[(u,v) for u,v in cold if {owner[u],owner[v]}=={a,b}]
        if common:
            assert len(common)==1 and len(cross)==12;p=next(iter(common))
            groups=defaultdict(list)
            for u,v in cross:
                if owner[u]!=a:u,v=v,u
                cu=next(x for x in recovered[u] if packet_of[x]==p);cv=next(x for x in recovered[v] if packet_of[x]==p);assert cu==cv;groups[cu].append((u,v))
            assert sorted(map(len,groups.values()))==[4,4,4]
            for E in groups.values():
                U={u for u,v in E};Vv={v for u,v in E};assert len(U)==len(Vv)==2 and len(E)==4
            laws['3 K2,2']+=1
        else:assert len(cross)==0
    assert laws==Counter({'3 K2,2':135})

    return {'packets':packets,'projected':projected,'G45':G45,'sig':sig,'cot':cot,'holonomy':hc,'K5':K5,'hot':hot,'cold':cold,'laws':laws,'Al':Al}

def main():
    X=build_bundle();out={'pass':4716,
      'selected135_cover':{'base':'SRG(45,12,3,3) = GQ(4,2) point graph','base_vertices':45,'lift_vertices':135,'sheets':3,'connection_group':'S3','spanning_tree_gauged_cotree_voltage_census':{str(k):v for k,v in X['cot'].items()}},
      'triangle_holonomy':{'base_triangles':270,'all_order':2,'transposition_census':{str(k):v for k,v in X['holonomy'].items()},'unique_fixed_sheet_reconstructs_selected_line':True},
      'selected270_reconstruction':{'vertices':270,'intersection_graph_recovered_exactly':True,'Petersen_fibers':27,'vertices_per_fiber':10,'hot_edges':405,'cold_edges':1620},
      'interfiber_connection':{'quotient_edges':135,'cold_edges_per_quotient_edge':12,'law':'3 disjoint K2,2 indexed by the three singular coordinates of the shared packet'},
      'theorem':'The selected135 graph is a connected nonregular S3 three-cover of the GQ(4,2) point graph. Every base triangle has transposition holonomy and its unique fixed sheet reconstructs one selected singular line; their intersection graph is selected270. The 27 Petersen fibers are coupled across each quotient edge by three coordinate-preserving K2,2 blocks.',
      'boundary':'Exact finite graph-cover/bundle theorem; selected270 is not claimed to be a regular 10-sheet cover of the 27 quotient.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
