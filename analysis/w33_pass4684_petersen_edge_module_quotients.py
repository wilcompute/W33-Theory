#!/usr/bin/env python3
"""Pass 4684 — representation-theoretic quotient structure of selected270 edges.

The Pass4660 405+1620 edge split is upgraded from a routing observation to a
homogeneous-module theorem.  The 405 shortcut edges are one PSp orbit and map
15-to-1 to the 27 internal Schlaefli objects.  The 1620 base edges are one PSp
orbit and map 12-to-1 to the 135 edges of the internal SRG(27,10,1,5).
Thus the two permutation modules are Ind_H^G(1) carriers with exact equivariant
quotient maps onto the 27-object and 135-edge Schlaefli modules.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import networkx as nx
import numpy as np
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
import sympy as sp
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,perm_group,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
from w33_pass4595_concrete_d4_triality_w33_lifts import max_generators
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4684_PETERSEN_EDGE_MODULE_QUOTIENTS_REGEN.json'

def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def smith(M):
    D=smith_normal_form(sp.Matrix(M.tolist()),domain=ZZ);z=[]
    for i in range(min(D.shape)):
        a=abs(int(D[i,i]));
        if a:z.append(a)
    return {str(k):int(v) for k,v in sorted(Counter(z).items())}

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    j=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]]);V=set(span(B9));rep=lambda x:min(int(x),int(x)^j);q=lambda x:(rep(x).bit_count()//4)&1;polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in {rep(v) for v in V} if x and q(x)==0);sidx={x:i for i,x in enumerate(singular)}
    def fib(ap):
        x=0
        for i in ap:x^=cols[int(i)]
        return rep(x)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(ap) for ap in apartments});selidx={L:i for i,L in enumerate(selected)}
    N=np.zeros((135,270),dtype=np.int64)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    Al=N.T@N-3*np.eye(270,dtype=np.int64);GL=nx.from_numpy_array(Al)
    eb=nx.edge_betweenness_centrality(GL,normalized=False);vmax=max(eb.values());hot=[tuple(sorted(e)) for e,v in eb.items() if abs(v-vmax)<1e-9];cold=[tuple(sorted(e)) for e,v in eb.items() if abs(v-vmax)>=1e-9]
    assert (len(hot),len(cold))==(405,1620)

    MG=max_generators(singular,rep,q,polar);selsets=[set(L) for L in selected];O27=[]
    for X in MG:
        I=frozenset(i for i,L in enumerate(selsets) if L.issubset(X))
        if len(I)==10:O27.append(I)
    assert len(O27)==27 and len(set(O27))==27
    comp={}
    for a,S in enumerate(O27):
        for v in S:assert v not in comp;comp[v]=a
    assert len(comp)==270

    # Hot edges stay inside one component; 15 per component.
    assert all(comp[u]==comp[v] for u,v in hot)
    Hinc=np.zeros((27,405),dtype=np.int64)
    for e,(u,v) in enumerate(hot):Hinc[comp[u],e]=1
    assert set(map(int,Hinc.sum(1)))=={15} and set(map(int,Hinc.sum(0)))=={1}
    assert np.array_equal(Hinc@Hinc.T,15*np.eye(27,dtype=np.int64))

    # Cold edges project 12-to-1 to a 135-edge quotient graph on the 27 components.
    mult=Counter()
    for u,v in cold:mult[tuple(sorted((comp[u],comp[v])))]+=1
    assert Counter(mult.values())==Counter({12:135})
    qedges=sorted(mult);A27=np.zeros((27,27),dtype=np.int64)
    for a,b in qedges:A27[a,b]=A27[b,a]=1
    assert set(map(int,A27.sum(1)))=={10}
    lam=set();mu=set()
    for a,b in itertools.combinations(range(27),2):
        z=int(A27[a]@A27[b]);(lam if A27[a,b] else mu).add(z)
    assert lam=={1} and mu=={5}
    B=np.zeros((27,135),dtype=np.int64)
    for e,(a,b) in enumerate(qedges):B[a,e]=B[b,e]=1
    assert np.array_equal(B@B.T,10*np.eye(27,dtype=np.int64)+A27)
    assert smith(B)=={'1':26,'2':1}

    # PSp orbit/stabilizer certificates.
    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];gens=[];G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    def actv(x,g):return rep(pmask(rep(x),g))
    def acts(i,g):return selidx[tuple(sorted(actv(x,g) for x in selected[i]))]
    def acte(e,g):return tuple(sorted((acts(e[0],g),acts(e[1],g))))
    h0=hot[0];c0=cold[0]
    assert len({acte(h0,g) for g in G})==405 and sum(acte(h0,g)==h0 for g in G)==64
    assert len({acte(c0,g) for g in G})==1620 and sum(acte(c0,g)==c0 for g in G)==16
    C0=O27[0]
    HC=[g for g in G if frozenset(acts(i,g) for i in C0)==C0];assert len(HC)==960
    # A quotient-edge stabilizer has order 25920/135=192.
    assert 25920//135==192 and 25920//27==960

    out={'pass':4684,
      'hot_module':{'edges':405,'PSp_orbit':405,'edge_stabilizer_order':64,'component_quotient':27,'component_stabilizer_order':960,'fiber_size':15,'homogeneous_form':'G/H64 -> G/H960','incidence_gram':'15 I27','kernel_dimension_of_pushforward':378},
      'cold_module':{'edges':1620,'PSp_orbit':1620,'edge_stabilizer_order':16,'quotient_edges':135,'quotient_edge_stabilizer_order':192,'fiber_size':12,'homogeneous_form':'G/H16 -> G/H192','quotient_graph':'SRG(27,10,1,5)','quotient_edge_to_vertex_incidence_smith':'1^26 2^1','kernel_dimension_first_pushforward':1485,'edge_module_to_vertex_module_secondary_kernel':108},
      'vertex_module':{'dimension':27,'A27_eigen_multiplicities':{'10':1,'1':20,'-5':6},'rational_split_dimensions':[1,20,6]},
      'theorem':'The selected270 routing-edge decomposition is an exact PSp-homogeneous bundle over the internal Schlaefli 27: shortcut edges are a 15-fold fiber over vertices, while base edges are a 12-fold fiber over the 135 edges of SRG(27,10,1,5).',
      'boundary':'Exact permutation-module quotient theorem; irreducibility of the large kernels is not asserted.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
