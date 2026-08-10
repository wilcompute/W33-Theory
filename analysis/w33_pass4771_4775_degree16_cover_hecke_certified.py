#!/usr/bin/env python3
"""Passes 4771/4775 corrected certificate.

The first exploratory verifier correctly found the two subdegree-16 residue
orbitals and the homogeneous 540=|PSp|/48 carrier, but diameter four does not
distinguish the two lifts above the desired base relation.  This certifier uses
three exact fingerprints established by direct comparison with the Pass4752
descended cocycle:

1. the desired subdegree-16 orbital has product of its two four-fixed residue
   involutions of order 3 with seven fixed W33 lines (the other fixes one);
2. its two homogeneous G/K lifts have 1440 and 4320 triangles;
3. the Pass4752 cocycle class is the 4320-triangle lift.

It then freezes its spectra/ranks and constructs the split M2(Q) Hecke block
without importing Pass4753's projector coefficients: the rank-40 projector is
recovered by CRT as the rational spectral projector of the cold adjacency onto
x^2-2x-12.  The resulting exact matrices are checked against the complete
orbital multiplication tensor.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque,defaultdict
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

def gf2_rank(rows):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)
def adjrank(H):
    rows=[]
    for u in sorted(H):
        m=0
        for v in H[u]:m|=1<<v
        rows.append(m)
    return gf2_rank(rows)
def spectrum(H):
    z=np.linalg.eigvalsh(nx.to_numpy_array(H,nodelist=sorted(H),dtype=float))
    return Counter(round(float(x),8) for x in z)
def jspec(C):return {str(k):int(v) for k,v in sorted(C.items())}

def main():
    pts,pidx,lines,A,apartments,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(A[:,C],axis=1)&1):residues.append(tuple(C))
    ridx={r:i for i,r in enumerate(residues)};rm=[sum(1<<x for x in r) for r in residues];assert len(residues)==270
    gens,G,full=build_groups(pts,pidx,lines);assert len(G)==25920 and len(full)==51840
    def act(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    H={g for g in G if act(0,g)==0};assert len(H)==96
    unseen=set(range(270));orbs=[]
    while unseen:
        x=min(unseen);O=sorted({act(x,h) for h in H});orbs.append(O);unseen-=set(O)
    assert sorted(map(len,orbs))==[1,3,6,12,12,12,16,16,24,24,48,96]

    ident=tuple(range(40));four={}
    for g in G:
        if g!=ident and compose(g,g)==ident:
            f=fixed_mask(g)
            if f.bit_count()==4:four[f]=g
    assert len(four)==270 and set(four)==set(rm)
    g0=four[rm[0]]
    candidates16=[]
    for oi,O in enumerate(orbs):
        if len(O)!=16:continue
        r=O[0];prod=compose(g0,four[rm[r]])
        candidates16.append((oi,r,order_perm(prod),fixed_mask(prod).bit_count()))
    desired=[q for q in candidates16 if q[2:]==(3,7)];assert len(desired)==1
    oi,r,_,_=desired[0]

    roots=[h for h in full-G if compose(h,h)==g0 and fixed_mask(h).bit_count()==4];assert len(roots)==2
    hroot=roots[0];K={g for g in G if compose(g,hroot)==compose(hroot,g)};assert len(K)==48 and K<H
    deckel=next(iter(H-K))
    elem={};reps=[]
    for g in sorted(G):
        if g in elem:continue
        C={compose(g,k) for k in K};i=len(reps);reps.append(g)
        for x in C:elem[x]=i
    assert len(reps)==540
    base=[act(0,g) for g in reps];assert Counter(base)==Counter({i:2 for i in range(270)})
    deck=[elem[compose(g,deckel)] for g in reps];assert all(deck[deck[i]]==i and base[deck[i]]==base[i] for i in range(540))

    baseE={tuple(sorted((act(0,x),act(r,x)))) for x in G};assert len(baseE)==2160
    BG=nx.Graph();BG.add_nodes_from(range(270));BG.add_edges_from(baseE);assert nx.is_connected(BG)
    gs=[g for g in G if act(0,g)==r];seeds=sorted({elem[g] for g in gs});assert len(seeds)==2
    lifts=[]
    for seed in seeds:
        q=reps[seed];CE={tuple(sorted((elem[x],elem[compose(x,q)]))) for x in G}
        CG=nx.Graph();CG.add_nodes_from(range(540));CG.add_edges_from(CE)
        assert len(CE)==4320 and set(dict(CG.degree()).values())=={16} and nx.is_connected(CG) and nx.diameter(CG)==4
        proj=Counter(tuple(sorted((base[u],base[v]))) for u,v in CE);assert set(proj)==baseE and set(proj.values())=={2}
        lifts.append((sum(nx.triangles(CG).values())//3,seed,CG))
    assert sorted(t for t,_,_ in lifts)==[1440,4320]
    ctri,seed,CG=next(q for q in lifts if q[0]==4320)
    assert ctri==4320

    bspec=spectrum(BG);cspec=spectrum(CG);sspec=cspec.copy()
    for k,v in bspec.items():sspec[k]-=v
    sspec=Counter({k:v for k,v in sspec.items() if v})
    assert sspec==Counter({8.0:20,4.0:81,-1.0:64,-4.0:105})
    btri=sum(nx.triangles(BG).values())//3;assert btri==2880
    brank=adjrank(BG);crank=adjrank(CG);assert (brank,crank)==(78,226)

    cd,sizes,chars,labels,cmap=character_table(G,gens)
    def covact(i,g):return elem[compose(g,reps[i])]
    pcb=[];pcc=[]
    for _,_,_,g,_ in cd:
        pcb.append(sum(act(i,g)==i for i in range(270)))
        pcc.append(sum(covact(i,g)==i for i in range(540)))
    pcs=[pcc[i]-pcb[i] for i in range(20)]
    def mults(pc):
        mm=[]
        for d,ch in chars:
            z=sum(sizes[i]*pc[i]*np.conjugate(ch[i]) for i in range(20))/25920
            assert abs(z.imag)<1e-5 and abs(z.real-round(z.real))<1e-5;mm.append(int(round(z.real)))
        return {labels[i]:mm[i] for i in range(20) if mm[i]}
    mb,mc,ms=mults(pcb),mults(pcc),mults(pcs)
    assert ms=={'10a':1,'10b':1,'15a':1,'45a':1,'45b':1,'64':1,'81':1}

    out1={'pass':4771,'homogeneous_cover':{'G':'PSp(4,3)','G_order':25920,'H_order':96,'K_order':48,'base':'G/H','cover':'G/K','base_vertices':270,'cover_vertices':540,'fiber_size':2,'deck_quotient':'H/K=C2'},
      'degree16_orbital':{'orbital_index_zero_based':oi,'intrinsic_selector':'product of the two four-fixed residue involutions has order 3 and fixes 7 W33 lines','other_degree16_product_fixed_lines':1,
        'base_edges':2160,'triangles':btri,'adjacency_rank_F2':brank,'cycle_code_dimension':1891,'spectrum':jspec(bspec)},
      'two_homogeneous_lifts':{'triangle_counts':[1440,4320],'Pass4752_cocycle_lift_triangles':4320,'selection':'explicit cohomology comparison fixes the 4320-triangle lift'},
      'cover_graph':{'edges':4320,'degree':16,'diameter':4,'triangles':ctri,'adjacency_rank_F2':crank,'cycle_code_dimension':3781,'spectrum':jspec(cspec),'signed_sheet_spectrum':jspec(sspec)},
      'ordinary_characters':{'base_G_over_H':mb,'cover_G_over_K':mc,'signed_Ind_H_epsilon':ms},
      'theorem':'The descended Pass4752 relation is the unique subdegree-16 residue orbital whose residue-involution product fixes seven W33 lines. Its homogeneous G/K carrier admits two graph lifts; explicit cohomology comparison selects the 4320-triangle lift. The selected cover has exact signed spectrum 8^20+4^81+(-1)^64+(-4)^105 and binary adjacency rank 226.',
      'boundary':'Exact finite homogeneous graph/cohomology/representation theorem. The rejected 1440-triangle lift remains a legitimate different homogeneous double cover.'}
    OUT1.write_text(json.dumps(out1,indent=2,sort_keys=True)+'\n')

    # Orbital multiplication algebra and CRT recovery of the multiplicity-two 20 block.
    oidx={x:k for k,O in enumerate(orbs) for x in O};trans={}
    for g in G:
        x0=act(0,g)
        if x0 not in trans:trans[x0]=g
    def rel(a,b):return oidx[act(b,inv(trans[a]))]
    P=np.zeros((12,12,12),dtype=int)
    for k,O in enumerate(orbs):
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
    one=[Fraction(0)]*12;one[0]=1
    def avec(i):
        v=[Fraction(0)]*12;v[i]=1;return v
    # identify cold and hot relations intrinsically
    cold_idx=next(i for i,O in enumerate(orbs) if len(O)==12 and len(set(residues[0])&set(residues[O[0]]))==2)
    hot_idx=next(i for i,O in enumerate(orbs) if len(O)==3)
    cold=avec(cold_idx);hot=avec(hot_idx)
    def apow(a,n):
        z=one;b=a
        while n:
            if n&1:z=mul(z,b)
            b=mul(b,b);n//=2
        return z
    xx=sp.symbols('x');qpoly=xx**2-2*xx-12;P0=sp.prod(xx-r0 for r0 in [12,8,2,-1,-4,-6])
    invrem=sp.invert(sp.rem(P0,qpoly,domain=sp.QQ),qpoly,domain=sp.QQ);poly=sp.Poly(sp.expand(P0*invrem),xx)
    E=[Fraction(0)]*12
    for (d,),c in poly.terms():
        cc=Fraction(int(c.p),int(c.q));pd=apow(cold,d);E=[a+cc*b for a,b in zip(E,pd)]
    assert mul(E,E)==E and 270*E[0]==40
    F=[x/Fraction(5) for x in mul(E,[hot[i]+2*E[i] for i in range(12)])];assert mul(F,F)==F and 270*F[0]==20
    basis=[F]
    for j in range(12):
        v=mul(avec(j),F);M=sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in row] for row in basis+[v]])
        if M.rank()>len(basis):basis.append(v);break
    assert len(basis)==2
    B=sp.Matrix.hstack(*[sp.Matrix([sp.Rational(x.numerator,x.denominator) for x in v]) for v in basis]);mats=[]
    for i in range(12):
        cols=[]
        for b in basis:
            y=sp.Matrix([sp.Rational(x.numerator,x.denominator) for x in mul(avec(i),b)])
            cols.append(B.gauss_jordan_solve(y)[0])
        mats.append(sp.Matrix.hstack(*cols))
    for i in range(12):
        for j in range(12):
            rhs=sp.zeros(2)
            for k in range(12):rhs+=int(P[i,j,k])*mats[k]
            assert mats[i]*mats[j]==rhs
    def mj(M):return [[str(M[i,j]) for j in range(2)] for i in range(2)]
    M16=mats[oi];cp=sp.factor(M16.charpoly(xx).as_expr());assert sp.expand(cp-(xx**2-4*xx-48))==0
    assert not any(k.startswith('20') for k in ms)
    out5={'pass':4775,'wedderburn':'Q^6 x Q(sqrt(-3)) x M2(Q)','rank40_projector_recovered_by':'CRT projector of cold adjacency onto x^2-2x-12','left_ideal_dimension':2,
      'distinguished_matrices':{'degree16_index':oi,'degree16':mj(M16),'degree16_charpoly':'x^2-4x-48','cold_index':cold_idx,'cold':mj(mats[cold_idx]),'hot_index':hot_idx,'hot':mj(mats[hot_idx])},
      'cover_sheet_comparison':{'signed_sheet_character':ms,'degree20_multiplicity':0,'conclusion':'the degree-16 BASE adjacency acts nontrivially on the unique M2(Q) residue block, but the signed G/K->G/H sheet module contains no degree-20 constituent and therefore lies outside that noncommutative block'},
      'theorem':'The split M2(Q) block is reconstructed intrinsically from the cold radical polynomial and represented on a concrete two-dimensional left ideal. The degree-16 base relation acts by an exact matrix with characteristic polynomial x^2-4x-48, whereas the signed normalizer-cover sheet module has zero degree-20 multiplicity. Thus the base orbital uses the M2 block but the sheet sector itself does not.',
      'boundary':'Exact finite Hecke/Wedderburn/induced-character statement; the 2x2 matrices are algebra coordinates, not physical transfer matrices.'}
    OUT5.write_text(json.dumps(out5,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'4771':out1,'4775':out5},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
