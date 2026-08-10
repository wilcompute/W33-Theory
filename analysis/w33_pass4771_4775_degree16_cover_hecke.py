#!/usr/bin/env python3
"""Passes 4771 and 4775 — the degree-16 residue orbital, its 540 cover, and M2 Hecke block.

Reconstruct the 270 involution residues and H=Stab(r0), |H|=96.  Reconstruct
K=C_PSp(h), |K|=48, from the Pass4738 outer order-four root.  Enumerate G/K
literally (540 cosets), project to G/H (270 residues), and test the two degree-16
H-suborbits.  The Pass4752 cover is selected by the frozen invariants: a connected
16-regular 540-vertex two-cover with 4320 edges and diameter four.

Then decompose both the base and signed sheet permutation characters.  Finally
rebuild Pass4753's 12-dimensional orbital algebra and represent its split M2(Q)
block on the two-dimensional left ideal A*e.  This gives explicit rational 2x2
matrices for every orbital relation, including the degree-16 cover base relation.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque
from fractions import Fraction
from pathlib import Path
import networkx as nx
import numpy as np
import sympy as sp
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups
from w33_pass4745_invariant_h1_character import character_table

ROOT=Path(__file__).resolve().parents[1]
OUT1=ROOT/'data/PART_W33_PASS4771_DEGREE16_NORMALIZER_COVER.json'
OUT5=ROOT/'data/PART_W33_PASS4775_RESIDUE_M2_HECKE_TRANSFER.json'

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def fixed_mask(p):return sum(1<<i for i,j in enumerate(p) if i==j)
def order_perm(p):
    seen=set();o=1
    for i in range(len(p)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=p[j]
        o=math.lcm(o,n)
    return o

def rank2_rows(rows,n):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def adj_rank2(G):
    n=G.number_of_nodes();rows=[]
    for u in range(n):
        m=0
        for v in G[u]:m|=1<<v
        rows.append(m)
    return rank2_rows(rows,n)

def spec_counter(G):
    A=nx.to_numpy_array(G,nodelist=range(G.number_of_nodes()),dtype=float)
    vals=np.linalg.eigvalsh(A);return Counter(round(float(x),8) for x in vals)

def dictspec(C):return {str(k):int(v) for k,v in sorted(C.items())}

def main():
    pts,pidx,lines,Astar,apartments,_,_=geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(Astar[:,C],axis=1)&1):residues.append(tuple(C))
    assert len(residues)==270;ridx={r:i for i,r in enumerate(residues)}
    gens,G,full=build_groups(pts,pidx,lines);assert len(G)==25920 and len(full)==51840
    def act(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    H={g for g in G if act(0,g)==0};assert len(H)==96
    unseen=set(range(270));orbs=[]
    while unseen:
        x=min(unseen);O=sorted({act(x,h) for h in H});orbs.append(O);unseen-=set(O)
    subdegrees=[len(O) for O in orbs];assert subdegrees==[1,12,16,48,16,6,24,96,12,12,24,3]

    ident=tuple(range(40));rmask=sum(1<<x for x in residues[0])
    invol=[g for g in G if g!=ident and compose(g,g)==ident and fixed_mask(g)==rmask]
    assert len(invol)==1;gi=invol[0]
    roots=[h for h in full-G if compose(h,h)==gi and fixed_mask(h).bit_count()==4]
    assert len(roots)==2;hroot=roots[0]
    K={g for g in G if compose(g,hroot)==compose(hroot,g)};assert len(K)==48 and K<H
    deckel=next(iter(H-K))

    # Enumerate right cosets gK; left G acts by x:gK -> (xg)K.
    elem_to_coset={};reps=[]
    for g in sorted(G):
        if g in elem_to_coset:continue
        C={compose(g,k) for k in K};idx=len(reps);reps.append(g)
        for x in C:elem_to_coset[x]=idx
    assert len(reps)==540 and len(elem_to_coset)==25920
    base_of=[act(0,g) for g in reps]
    assert Counter(base_of.values())==Counter({i:2 for i in range(270)})
    deck=[elem_to_coset[compose(g,deckel)] for g in reps]
    assert all(deck[deck[i]]==i and deck[i]!=i and base_of[deck[i]]==base_of[i] for i in range(540))

    candidates=[]
    for oi,O in enumerate(orbs):
        if len(O)!=16:continue
        r=O[0]
        gs=[g for g in G if act(0,g)==r]
        lift_seeds=sorted({elem_to_coset[g] for g in gs});assert len(lift_seeds)==2
        baseE={tuple(sorted((act(0,x),act(r,x)))) for x in G};assert len(baseE)==2160
        for seed in lift_seeds:
            gseed=reps[seed]
            CE={tuple(sorted((elem_to_coset[x],elem_to_coset[compose(x,gseed)]))) for x in G}
            CG=nx.Graph();CG.add_nodes_from(range(540));CG.add_edges_from(CE)
            if len(CE)!=4320 or set(dict(CG.degree()).values())!={16}:continue
            proj=Counter(tuple(sorted((base_of[u],base_of[v]))) for u,v in CE)
            if set(proj)!=baseE or set(proj.values())!={2}:continue
            conn=nx.is_connected(CG);diam=nx.diameter(CG) if conn else None
            candidates.append((oi,seed,baseE,CG,diam))
    good=[x for x in candidates if x[4]==4]
    assert good
    # Frozen Pass4752 gives a single descended homogeneous cover invariant class;
    # if both sheet seeds generate the same edge set they are the same candidate.
    uniq={frozenset(x[3].edges()):x for x in good}
    assert len(uniq)==1
    oi,seed,baseE,CG,diam=next(iter(uniq.values()))
    BG=nx.Graph();BG.add_nodes_from(range(270));BG.add_edges_from(baseE)
    assert nx.is_connected(BG) and set(dict(BG.degree()).values())=={16}
    assert nx.is_connected(CG) and diam==4

    bspec=spec_counter(BG);cspec=spec_counter(CG);sspec=cspec.copy()
    for k,v in bspec.items():sspec[k]-=v
    sspec=Counter({k:v for k,v in sspec.items() if v})
    btri=sum(nx.triangles(BG).values())//3;ctri=sum(nx.triangles(CG).values())//3

    # Ordinary character decomposition of base, cover and signed sheet sector.
    cd,sizes,chars,labels,cmap=character_table(G,gens)
    def cov_act(i,g):return elem_to_coset[compose(g,reps[i])]
    pcb=[];pcc=[]
    for _,_,_,g,_ in cd:
        pcb.append(sum(act(i,g)==i for i in range(270)))
        pcc.append(sum(cov_act(i,g)==i for i in range(540)))
    pcs=[pcc[i]-pcb[i] for i in range(20)]
    def mults(pc):
        mm=[]
        for d,ch in chars:
            z=sum(sizes[i]*pc[i]*np.conjugate(ch[i]) for i in range(20))/25920
            assert abs(z.imag)<1e-5 and abs(z.real-round(z.real))<1e-5;mm.append(int(round(z.real)))
        return {labels[i]:mm[i] for i in range(20) if mm[i]}
    mb,mc,ms=mults(pcb),mults(pcc),mults(pcs)

    out1={'pass':4771,'homogeneous_cover':{'G':'PSp(4,3)','G_order':25920,'H_order':96,'K_order':48,
        'base':'G/H','cover':'G/K','base_vertices':270,'cover_vertices':540,'fiber_size':2,'deck_quotient':'H/K=C2'},
      'degree16_orbital':{'orbital_index_zero_based':oi,'subdegree':16,'base_edges':2160,'base_connected':True,
        'base_triangles':btri,'base_adjacency_rank_F2':adj_rank2(BG),'base_cycle_code_dimension':2160-270+1,
        'base_spectrum':dictspec(bspec)},
      'cover_graph':{'edges':4320,'degree':16,'diameter':diam,'triangles':ctri,'adjacency_rank_F2':adj_rank2(CG),
        'cycle_code_dimension':4320-540+1,'spectrum':dictspec(cspec),'signed_sheet_spectrum':dictspec(sspec)},
      'ordinary_characters':{'base_G_over_H':mb,'cover_G_over_K':mc,'signed_Ind_H_epsilon':ms},
      'theorem':'The Pass4752 degree-16 relation is identified as a specific rank-12 residue orbital and its 540-vertex double cover is reconstructed purely as the homogeneous graph on PSp/K above PSp/H. Exact spectra, binary adjacency ranks, cycle-code dimensions and the signed sheet permutation character are frozen.',
      'boundary':'Exact finite homogeneous graph/representation theorem. The signed sheet sector is a finite induced representation, not a physical gauge field.'}
    OUT1.write_text(json.dumps(out1,indent=2,sort_keys=True)+'\n')

    # Pass4775: rebuild the orbital multiplication tensor and explicit M2(Q) representation.
    H0=list(H);unseen=set(range(270));orbs2=[]
    while unseen:
        x=min(unseen);O=sorted({act(x,h) for h in H0});orbs2.append(O);unseen-=set(O)
    oidx={x:k for k,O in enumerate(orbs2) for x in O};trans={}
    for g in G:
        x=act(0,g)
        if x not in trans:trans[x]=g
    def rel(a,b):return oidx[act(b,inv(trans[a]))]
    P=np.zeros((12,12,12),dtype=int)
    for k,O in enumerate(orbs2):
        y=O[0]
        for z in range(270):P[rel(0,z),rel(z,y),k]+=1
    def mul(a,b):
        out=[Fraction(0)]*12
        for i,ai in enumerate(a):
            if not ai:continue
            for j,bj in enumerate(b):
                if not bj:continue
                for k in range(12):
                    if P[i,j,k]:out[k]+=ai*bj*int(P[i,j,k])
        return out
    E40=[Fraction(4,27),Fraction(1,81),Fraction(1,54),Fraction(-11,324),Fraction(1,36),Fraction(-1,324),Fraction(1,81),Fraction(0),Fraction(1,81),Fraction(7,81),Fraction(0),Fraction(2,81)]
    A11=[Fraction(0)]*12;A11[11]=1
    F20=[x/Fraction(5) for x in mul(E40,[A11[i]+2*E40[i] for i in range(12)])]
    assert mul(F20,F20)==F20
    e=F20
    basis=[e]
    for j in range(12):
        Aj=[Fraction(int(i==j)) for i in range(12)];v=mul(Aj,e)
        if sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in q] for q in basis+[v]]).rank()>len(basis):
            basis.append(v);break
    assert len(basis)==2
    B=sp.Matrix.hstack(*[sp.Matrix([sp.Rational(x.numerator,x.denominator) for x in v]) for v in basis])
    mats=[]
    for i in range(12):
        Ai=[Fraction(int(k==i)) for k in range(12)];colsM=[]
        for b in basis:
            y=sp.Matrix([sp.Rational(x.numerator,x.denominator) for x in mul(Ai,b)])
            sol=B.gauss_jordan_solve(y)[0];colsM.append(sol)
        M=sp.Matrix.hstack(*colsM);mats.append(M)
    for i in range(12):
        for j in range(12):
            lhs=mats[i]*mats[j];rhs=sp.zeros(2)
            for k in range(12):rhs+=int(P[i,j,k])*mats[k]
            assert lhs==rhs
    def mjson(M):return [[str(M[i,j]) for j in range(2)] for i in range(2)]
    selectedM=mats[oi];cold_idx=next(i for i,O in enumerate(orbs2) if len(O)==12 and len(set(residues[0])&set(residues[O[0]]))==2)
    hot_idx=next(i for i,O in enumerate(orbs2) if len(O)==3)
    x=sp.symbols('x');cp=sp.factor(selectedM.charpoly(x).as_expr())
    scalar=selectedM[0,1]==0 and selectedM[1,0]==0 and selectedM[0,0]==selectedM[1,1]
    signed20=sum(v for k,v in ms.items() if k.startswith('20'))
    out5={'pass':4775,'wedderburn':'Q^6 x Q(sqrt(-3)) x M2(Q)','left_ideal_dimension':2,
      'orbital_M2_matrices':{str(i):mjson(M) for i,M in enumerate(mats)},
      'distinguished_relations':{'degree16_index':oi,'degree16_matrix':mjson(selectedM),'degree16_charpoly':str(cp),'degree16_is_scalar_on_M2':scalar,
        'cold_index':cold_idx,'cold_matrix':mjson(mats[cold_idx]),'hot_index':hot_idx,'hot_matrix':mjson(mats[hot_idx])},
      'cover_comparison':{'signed_sheet_degree20_total_multiplicity':signed20,
        'interpretation':'The base degree-16 adjacency has an explicit 2x2 image in the unique noncommutative residue block. The signed G/K->G/H sheet module is compared separately by its exact induced-character decomposition; overlap is reported rather than inferred from the common carrier.'},
      'theorem':'A concrete two-dimensional left ideal of the split M2(Q) Wedderburn block supplies exact rational 2x2 matrices for all twelve residue orbitals. Thus the degree-16 base relation has an explicit Hecke/Morita transfer matrix; the homogeneous cover sheet sector is independently tested against the same degree-20 constituent by character decomposition.',
      'boundary':'Exact finite semisimple-algebra/induced-module statement. M2 transfer matrices are representation coordinates, not physical transfer matrices.'}
    OUT5.write_text(json.dumps(out5,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'4771':out1,'4775':out5},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
