#!/usr/bin/env python3
"""Pass 4681 — the dual weight-132 shell is the protected/E6 45 carrier.

Rebuild the selected [135,16,30]_2 code.  A weight-132 dual word has a
3-coordinate complement.  Instead of enumerating the 2^119 dual, solve the
16 primal orthogonality constraints on triples.  Exactly 45 triples occur.
They partition all 135 coordinates and equal, object-for-object, the three
singular fibers attached to each protected 16-line support from Pass4585/4624.

The 270 dual weight-three selected lines meet each complement packet in at most
one coordinate.  Projecting their three coordinates to the 45 packets gives
270 distinct triples; packet-pairs occur with multiplicity three and their
pair graph is SRG(45,12,3,3), the complement of the protected 45 graph.
PSp is transitive on the packets with stabilizer 576; PGSp remains transitive
with stabilizer 1152.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,nullspace2,perm_group,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4681_DUAL132_PROTECTED45_REGEN.json'

def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8);apartments=sorted(tuple(map(int,a)) for a in apartments)
    j=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]]);V=set(span(B9));rep=lambda x:min(int(x),int(x)^j)
    def fib(ap):
        x=0
        for i in ap:x^=cols[i]
        return rep(x)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(a) for a in apartments});sing=sorted(set().union(*(set(L) for L in selected)));sidx={x:i for i,x in enumerate(sing)}
    N=np.zeros((135,270),dtype=np.uint8)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    B=nullspace2(N.T);assert len(B)==16

    # Complement T of a dual weight-132 word obeys <1+1_T,b>=0 for each primal basis b.
    sig=[]
    for i in range(135):
        z=0
        for r,b in enumerate(B):
            if int(b[i]):z|=1<<r
        sig.append(z)
    parity=0
    for r,b in enumerate(B):
        if int(b.sum())&1:parity|=1<<r
    bysig=defaultdict(list)
    for i,z in enumerate(sig):bysig[z].append(i)
    triples=set()
    for i in range(135):
        for k in range(i+1,135):
            need=parity^sig[i]^sig[k]
            for l in bysig.get(need,()):
                if l>k:triples.add((i,k,l))
    triples=sorted(triples);assert len(triples)==45
    assert Counter(i for T in triples for i in T)==Counter({i:1 for i in range(135)})
    assert Counter(len(set(a)&set(b)) for a,b in itertools.combinations(triples,2))==Counter({0:990})

    # The old protected supports group the same 135 singular fibers into triples.
    fibers=defaultdict(list)
    for ap in apartments:fibers[fib(ap)].append(ap)
    support_to_s=defaultdict(list)
    for s,F in fibers.items():support_to_s[frozenset().union(*(set(ap) for ap in F))].append(s)
    protected=sorted(tuple(sorted(sidx[x] for x in S)) for S in support_to_s.values())
    assert len(protected)==45 and triples==protected

    # Dual-minimum selected lines project to a 45-point triple system.
    packet={i:t for t,T in enumerate(triples) for i in T}
    projected=[]
    for L in selected:
        h=tuple(sorted(packet[sidx[x]] for x in L));assert len(set(h))==3;projected.append(h)
    assert len(set(projected))==270
    pairmult=Counter()
    for h in projected:
        for a,b in itertools.combinations(h,2):pairmult[(a,b)]+=1
    assert Counter(pairmult.values())==Counter({3:270})
    A=np.zeros((45,45),dtype=np.int64)
    for a,b in pairmult:A[a,b]=A[b,a]=1
    assert set(map(int,A.sum(1)))=={12}
    lam=set();mu=set()
    for a,b in itertools.combinations(range(45),2):
        c=int(A[a]@A[b]);(lam if A[a,b] else mu).add(c)
    assert lam==mu=={3}

    # PSp/PGSp orbit and stabilizers.
    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];gens=[];G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    def actv(x,g):return rep(pmask(rep(x),g))
    def actT(T,g):return frozenset(sidx[actv(sing[i],g)] for i in T)
    T0=frozenset(triples[0]);packetset=set(map(frozenset,triples))
    orbit={actT(T0,g) for g in G};stab=sum(actT(T0,g)==T0 for g in G)
    assert orbit==packetset and stab==576
    outer=build_line_perm(np.diag([1,2,1,2])%3,pts,pidx,lines,lidx);PG=set(G)|{tuple(outer[g[i]] for i in range(40)) for g in G}
    assert len(PG)==51840
    porbit={actT(T0,g) for g in PG};pstab=sum(actT(T0,g)==T0 for g in PG)
    assert porbit==packetset and pstab==1152

    out={'pass':4681,
      'dual_weight132':{'words':45,'complement_size':3,'complement_triples':45,'partition_135':'45 x 3','pairwise_complement_intersection':0},
      'protected45_intertwiner':{'literal_triple_equality_with_Pass4585_4624_singular_fiber_packets':True,'PSp_orbit_size':45,'PSp_stabilizer_order':576,'PGSp_orbit_size':45,'PGSp_stabilizer_order':1152},
      'incidence_with_dual_weight3':{'selected_lines':270,'packet_intersection_per_selected_line':'three distinct packets','projected_triples':270,'packet_pair_multiplicity':3,'pair_graph':'SRG(45,12,3,3)','identification':'complement of protected SRG(45,32,22,24)'},
      'theorem':'The 45 weight-132 words of C^perp have disjoint 3-coordinate complements that are literally the protected singular-fiber packets. The dual minimum shell projects through those packets to SRG(45,12,3,3), giving a second code-internal realization of the protected/E6 45 carrier.',
      'boundary':'Exact binary-code/hypergraph/G-set theorem only.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
