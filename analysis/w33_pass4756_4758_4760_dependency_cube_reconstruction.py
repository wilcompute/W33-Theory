#!/usr/bin/env python3
"""Passes 4756, 4758, 4760 — dependency shells, 135 cubes, and code reconstruction.

4756: the cold residue graph has 1080 triangles: 540 weight-3 dependency
triangles and 540 nondependency triangles. Every cold edge lies in exactly one
of each. The incidence graph between the two triangle species along cold edges
is 135 disjoint Q3 cubes. The dependency-code weight-4 shell has 3645 words in
PSp orbits 1620+1620+405; A5=29376.

4758 (outside box): each cube uses six residues forming K6-3K2 and their W33
line-support union is a weight-8 H10-dual word. The 135 unions form one PSp
orbit. Their intersection-4 graph is PSp-equivariantly the selected135 graph;
under the compatible Pass4737 residue->selected270 map, the six residues of a
cube are exactly the six selected270 lines through the corresponding selected135
vertex. Thus the dependency geometry reconstructs the 135<->270 incidence.

4760 (outside box): the 135 cube-union words span exactly the 24-dimensional
intersection of the W33 point-star incidence code (rank 25) with H10^perp
(rank 30). Its full weight enumerator is obtained by enumerating its 16-d dual.
The minimum shell has 240 weight-6 words, exactly star_p+star_q for the 240
collinear point pairs.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,defaultdict,deque
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4756_4758_4760_DEPENDENCY_CUBES.json'

def mask(S):return sum(1<<i for i in S)
def pmask(m,p):
    y=0
    for i in range(40):
        if (m>>i)&1:y|=1<<p[i]
    return y

def gf2_basis(vals):
    piv={};out=[]
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;out.append(y);break
    return out

def gf2_reduce(x,basis):
    piv={}
    for b in basis:
        y=int(b)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    y=int(x)
    while y:
        p=y.bit_length()-1
        if p in piv:y^=piv[p]
        else:break
    return y

def gf2_nullspace(rows,n=40):
    R=[int(x) for x in rows if x];rr=0;pivs=[]
    for col in reversed(range(n)):
        k=next((i for i in range(rr,len(R)) if (R[i]>>col)&1),None)
        if k is None:continue
        R[rr],R[k]=R[k],R[rr]
        for i in range(len(R)):
            if i!=rr and ((R[i]>>col)&1):R[i]^=R[rr]
        pivs.append(col);rr+=1
        if rr==len(R):break
    R=R[:rr];free=[c for c in range(n) if c not in set(pivs)];out=[]
    for f in free:
        x=1<<f
        for row,p in zip(R,pivs):
            if (row&x).bit_count()&1:x|=1<<p
        assert all(not ((r&x).bit_count()&1) for r in rows);out.append(x)
    return out

def span(basis):
    S={0}
    for b in basis:S|={x^b for x in list(S)}
    return S

def kraw(n,j,i):
    from math import comb
    return sum((-1)**s*comb(i,s)*comb(n-i,j-s) for s in range(max(0,j-(n-i)),min(j,i)+1))

def build_all():
    pts,pidx,lines,A,apartments,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(A[:,C],axis=1)&1):residues.append(tuple(C))
    rm=[mask(r) for r in residues];ridx={r:i for i,r in enumerate(residues)}
    _,G,_=build_groups(pts,pidx,lines);assert len(G)==25920
    def ar(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]

    cold=nx.Graph();cold.add_nodes_from(range(270))
    for i,j in itertools.combinations(range(270),2):
        if (rm[i]&rm[j]).bit_count()==2:cold.add_edge(i,j)
    assert cold.number_of_edges()==1620 and set(dict(cold.degree()).values())=={12}
    tris=[]
    for a in range(270):
        for b in (x for x in cold[a] if x>a):
            for c in cold[a].keys() & cold[b].keys():
                if c>b:tris.append((a,b,c))
    assert len(tris)==1080
    cir=[t for t in tris if rm[t[0]]^rm[t[1]]^rm[t[2]]==0]
    non=[t for t in tris if rm[t[0]]^rm[t[1]]^rm[t[2]]!=0]
    assert len(cir)==len(non)==540
    ec={};en={}
    for i,t in enumerate(cir):
        for e in itertools.combinations(t,2):ec[tuple(sorted(e))]=i
    for i,t in enumerate(non):
        for e in itertools.combinations(t,2):en[tuple(sorted(e))]=i
    assert set(ec)==set(en)=={tuple(sorted(e)) for e in cold.edges()}
    B=nx.Graph();B.add_nodes_from(range(1080))
    for e in cold.edges():B.add_edge(ec[tuple(sorted(e))],540+en[tuple(sorted(e))])
    comps=[frozenset(C) for C in nx.connected_components(B)]
    assert len(comps)==135 and {len(C) for C in comps}=={8}
    assert all(nx.is_isomorphic(B.subgraph(C),nx.cubical_graph()) for C in comps)

    cube_res=[];unions=[]
    for C in comps:
        R=set()
        for x in C:
            R.update(cir[x] if x<540 else non[x-540])
        assert len(R)==6
        H=cold.subgraph(R);assert H.number_of_edges()==12 and all(d==4 for _,d in H.degree())
        # K6 minus a perfect matching.
        assert len(list(nx.non_edges(H)))==3
        u=0
        for r in R:u|=rm[r]
        assert u.bit_count()==8
        v=np.array([(u>>i)&1 for i in range(40)],dtype=np.uint8)
        assert not np.any((A@v)&1)
        cube_res.append(tuple(sorted(R)));unions.append(u)
    U=sorted(set(unions));assert len(U)==135
    uidx={u:i for i,u in enumerate(U)};u_to_R={u:R for u,R in zip(unions,cube_res)}
    u0=U[0];Hu=[g for g in G if pmask(u0,g)==u0]
    assert len(Hu)==192 and {pmask(u0,g) for g in G}==set(U)

    # Weight-4 dependency shell and PSp orbits.
    pb=defaultdict(list)
    for i,j in itertools.combinations(range(270),2):pb[rm[i]^rm[j]].append((i,j))
    pair_mult=Counter(map(len,pb.values()));assert pair_mult==Counter({1:25650,2:3240,3:135,4:540,6:270})
    D4=set()
    for pairs in pb.values():
        for a,b in itertools.combinations(pairs,2):
            S=frozenset(a+b)
            if len(S)==4:D4.add(tuple(sorted(S)))
    assert len(D4)==3645
    unseen=set(D4);d4orbs=[]
    while unseen:
        S=next(iter(unseen));O={tuple(sorted(ar(i,g) for i in S)) for g in G};assert O<=D4;d4orbs.append(O);unseen-=O
    assert sorted(map(len,d4orbs))==[405,1620,1620]

    # Exact A5 via 2+3 split. Each five-set is seen C(5,2)=10 times.
    hit=0
    for T in itertools.combinations(range(270),3):
        x=rm[T[0]]^rm[T[1]]^rm[T[2]]
        for P2 in pb.get(x,()):
            if set(T).isdisjoint(P2):hit+=1
    assert hit%10==0;A5=hit//10;assert A5==29376

    # selected270 and selected135 reconstruction.
    all40=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(A[:,c]):m|=1<<int(r)
        cols.append(m)
    rep=lambda x:min(int(x),int(x)^all40)
    def fib(ap):
        z=0
        for i in ap:z^=cols[i]
        return rep(z)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not A[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    sel=sorted({aline(ap) for ap in apartments});sing=sorted(set().union(*(set(L) for L in sel)))
    assert len(sel)==270 and len(sing)==135
    sidx={x:i for i,x in enumerate(sing)};selidx={L:i for i,L in enumerate(sel)}
    N=np.zeros((135,270),dtype=np.uint8)
    for j,L in enumerate(sel):
        for x in L:N[sidx[x],j]=1
    As=(N@N.T).astype(int);np.fill_diagonal(As,0);assert set(As.sum(1))=={12}
    Es={tuple(sorted((i,j))) for i,j in itertools.combinations(range(135),2) if As[i,j]}
    def act_sing(i,g):return sidx[rep(pmask(sing[i],g))]
    def act_sel(i,g):return selidx[tuple(sorted(rep(pmask(x,g)) for x in sel[i]))]

    transU={}
    for g in G:
        i=uidx[pmask(u0,g)]
        if i not in transU:transU[i]=g
    fixedS=[i for i in range(135) if all(act_sing(i,h)==i for h in Hu)]
    assert len(fixedS)==3
    EU={tuple(sorted((i,j))) for i,j in itertools.combinations(range(135),2) if (U[i]&U[j]).bit_count()==4}
    phiU=None;baseS=None
    for t in fixedS:
        phi={i:act_sing(t,g) for i,g in transU.items()}
        if {tuple(sorted((phi[i],phi[j]))) for i,j in EU}==Es:phiU=phi;baseS=t;break
    assert phiU is not None and len(set(phiU.values()))==135

    Hline={g for g in G if act_sel(0,g)==0};assert len(Hline)==96
    fixedR=[i for i in range(270) if all(ar(i,h)==i for h in Hline)];assert len(fixedR)==1
    br=fixedR[0];phiR={}
    for g in G:
        a=ar(br,g);b=act_sel(0,g)
        if a in phiR:assert phiR[a]==b
        else:phiR[a]=b
    assert len(phiR)==270
    for ui,u in enumerate(U):
        Rs=u_to_R[u];Ls=[sel[phiR[r]] for r in Rs];common=set(Ls[0])
        for L in Ls[1:]:common&=set(L)
        assert common=={sing[phiU[ui]]}

    # Binary 24-dimensional intersection code.
    stars=[]
    for p in range(40):stars.append(mask(li for li,L in enumerate(lines) if p in L))
    sb=gf2_basis(stars);rb=gf2_basis(rm);ub=gf2_basis(U)
    assert (len(sb),len(rb),len(ub),len(gf2_basis(sb+rb)))==(25,30,24,31)
    assert all(gf2_reduce(u,sb)==0 for u in U)
    assert len(sb)+len(rb)-len(gf2_basis(sb+rb))==24
    dualb=gf2_nullspace(ub,40);assert len(dualb)==16
    Wd=Counter(x.bit_count() for x in span(dualb));assert sum(Wd.values())==2**16
    W={}
    for j in range(41):
        z=sum(c*kraw(40,j,i) for i,c in Wd.items())//(2**16)
        if z:W[j]=z
    assert sum(W.values())==2**24 and W[6]==240 and W[8]==1485
    colpairs=set()
    for p,q in itertools.combinations(range(40),2):
        if any(p in L and q in L for L in lines):colpairs.add(stars[p]^stars[q])
    minwords=[]
    for C in itertools.combinations(range(40),6):
        m=mask(C);v=np.array([(m>>i)&1 for i in range(40)],dtype=np.uint8)
        if not np.any((A@v)&1) and gf2_reduce(m,sb)==0:minwords.append(m)
    assert len(minwords)==240 and set(minwords)==colpairs

    return {'pts':pts,'lines':lines,'A':A,'residues':residues,'rmasks':rm,'G':G,'cold':cold,'circuits':cir,'noncircuits':non,'cube_components':comps,'cube_residues':cube_res,'cube_unions':U,'selected270':sel,'selected135':sing,'selected_incidence':N,'phiU':phiU,'phiR':phiR,
      'summary':{'cold_triangles':1080,'circuits':540,'noncircuits':540,'cube_components':135,'dependency_A4':len(D4),'dependency_A4_orbits':sorted(map(len,d4orbs)),'dependency_A5':A5,'pair_xor_multiplicity':dict(pair_mult),'cube_union_orbit':135,'cube_union_weight':8,'cube_union_stabilizer':192,'binary_intersection_dimension':24,'binary_intersection_enumerator':W,'binary_intersection_dual_enumerator':dict(Wd)}}

def main():
    X=build_all();S=X['summary']
    out={'passes':[4756,4758,4760],
      '4756_dependency_geometry':{'cold_triangles':S['cold_triangles'],'dependency_triangles':S['circuits'],'nondependency_triangles':S['noncircuits'],'edge_triangle_law':'every cold edge lies in exactly one triangle of each species','triangle_incidence_components':'135 Q3 cubes','A4':S['dependency_A4'],'A4_PSp_orbits':S['dependency_A4_orbits'],'A5':S['dependency_A5'],'pair_xor_multiplicity':{str(k):v for k,v in S['pair_xor_multiplicity'].items()}},
      '4758_cube_reconstruction':{'cube_residues':6,'residue_graph_per_cube':'K6 minus 3K2','cube_union_lines':8,'cube_union_words':135,'PSp_orbit':135,'stabilizer_order':192,'union_intersection4_graph_equals_selected135':True,'six_residues_equal_six_incident_selected270_lines':True},
      '4760_binary_intersection_code':{'description':'span(135 cube-union words) = point-star incidence code intersect H10^perp','parameters':'[40,24,6]','weight_enumerator':{str(k):v for k,v in S['binary_intersection_enumerator'].items()},'dual_weight_enumerator':{str(k):v for k,v in S['binary_intersection_dual_enumerator'].items()},'minimum_shell_240':'exactly star_p + star_q for the 240 collinear W33 point pairs','distinguished_weight8_cube_orbit':135},
      'boundary':'All identifications are explicit PSp-equivariant or binary-code equalities. The repeated dimensions 24 and 135 are not used as identification evidence by themselves.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
