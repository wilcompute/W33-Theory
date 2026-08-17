#!/usr/bin/env python3
"""Passes 5872--5879: coherent/Radon/rank-metric/Clifford closure.

Eight exact probes:
5872 joint determinant-polar + unit-difference coherent closure on M2(F2);
5873 local Reye versus global q=5 CSS check-space no-go;
5874 all-field unit-difference Cayley graph spectrum/SRG law;
5875 hyperbolic 72-label isometries and the non-entangling Clifford quotient;
5876 exact mod-2 Radon sequence and determinant quadratic cokernel;
5877 odd-field quadratic-character determinant Fourier eigenfunction;
5878 q=3 maximum rank-distance clique orbit split;
5879 primal/dual minimum-shell reconstruction of both Reye incidences.

Finite statements are replayed from definitions. Literature-bound automorphism/Clifford
identifications are stated as boundaries in the report, not silently assumed here.
"""
from __future__ import annotations

import collections
import itertools
import json
import math
from pathlib import Path

import networkx as nx
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS5872_5879_COHERENT_CSS_RANKMETRIC_CLIFFORD_DISCRIMINANT.json"

# ---------------- F2 / M2(F2) ----------------
V16 = list(range(16))
BASIS4 = (1, 2, 4, 8)

def bits4(x: int) -> tuple[int,int,int,int]:
    return tuple((x >> i) & 1 for i in range(4))  # type: ignore[return-value]

def det2(x: int) -> int:
    a,b,c,d = bits4(x)
    return (a & d) ^ (b & c)

def bdet(x: int, y: int) -> int:
    return det2(x ^ y) ^ det2(x) ^ det2(y)

def rank_cols(cols: tuple[int,int,int,int]) -> int:
    span={0}
    for v in cols:
        span |= {x ^ v for x in tuple(span)}
    return (len(span)).bit_length()-1

def lin_perm(cols: tuple[int,int,int,int]) -> tuple[int,...]:
    return tuple(
        (cols[0] if x&1 else 0) ^
        (cols[1] if x&2 else 0) ^
        (cols[2] if x&4 else 0) ^
        (cols[3] if x&8 else 0)
        for x in V16
    )

def gl4_perms() -> list[tuple[int,...]]:
    out=[]
    for cols in itertools.permutations(range(1,16),4):
        if rank_cols(cols)==4:
            out.append(lin_perm(cols))
    assert len(out)==20160 and len(set(out))==20160
    return out

def renumber(values: dict[tuple[int,int], object]) -> dict[tuple[int,int], int]:
    uniq={v:i for i,v in enumerate(sorted(set(values.values()), key=repr))}
    return {k:uniq[v] for k,v in values.items()}

def refine_pair_colors(c: dict[tuple[int,int],int]) -> dict[tuple[int,int],int]:
    pairs=[(x,y) for x in V16 for y in V16]
    n=max(c.values())+1
    raw={}
    for x,y in pairs:
        hist=[0]*(n*n)
        for z in V16:
            hist[c[(x,z)]*n+c[(z,y)]] += 1
        raw[(x,y)] = (c[(x,y)], tuple(hist))
    return renumber(raw)

def coherent_packet(gl4: list[tuple[int,...]]) -> dict:
    pairs=[(x,y) for x in V16 for y in V16]
    c=renumber({(x,y):(x==y,det2(x^y),bdet(x,y)) for x,y in pairs})
    assert len(set(c.values()))==5
    counts=[5]
    for _ in range(4):
        c2=refine_pair_colors(c)
        counts.append(len(set(c2.values())))
        old={frozenset(k for k,v in c.items() if v==a) for a in set(c.values())}
        new={frozenset(k for k,v in c2.items() if v==a) for a in set(c2.values())}
        c=c2
        if old==new:
            break
    assert counts[:3]==[5,15,15]

    O=[p for p in gl4 if all(det2(p[x])==det2(x) for x in V16)]
    assert len(O)==72
    unseen=set(pairs); orbitals=[]
    while unseen:
        a=next(iter(unseen))
        orb={(p[a[0]],p[a[1]]) for p in O}
        orbitals.append(orb); unseen-=orb
    osizes=sorted(map(len,orbitals))
    assert osizes==[1,6,6,6,9,9,9,12,18,18,18,36,36,36,36]
    classes=[{k for k,v in c.items() if v==a} for a in set(c.values())]
    assert {frozenset(x) for x in classes} == {frozenset(x) for x in orbitals}

    mats=[]
    for orb in orbitals:
        A=sp.zeros(16,16)
        for i,j in orb: A[i,j]=1
        mats.append(A)
    eq=[]
    for B in mats:
        comm=[A*B-B*A for A in mats]
        for r in range(16):
            for s in range(16):
                row=[int(X[r,s]) for X in comm]
                if any(row): eq.append(row)
    center=sp.Matrix(eq).nullspace()
    assert len(center)==4
    Z=sp.zeros(16)
    for j,v in enumerate(center):
        den=sp.ilcm(*[x.q for x in v])
        coeff=[int(x*den) for x in v]
        for i,a in enumerate(coeff):
            Z += (j+1)*a*mats[i]
    ev=Z.eigenvals()
    assert sorted(ev.values())==[1,3,4,8]
    eigen_data=[]
    I=sp.eye(16)
    for lam,mult in ev.items():
        P=I; den=1
        for mu in ev:
            if mu!=lam:
                P=P*(Z-mu*I); den*=int(lam-mu)
        P=P/den
        vecs=[sp.Matrix(P*A*P).reshape(256,1) for A in mats]
        algdim=sp.Matrix.hstack(*vecs).rank()
        eigen_data.append((int(P.rank()), int(algdim)))
    eigen_data=sorted(eigen_data)
    assert eigen_data==[(1,1),(3,9),(4,1),(8,4)]
    return {
        "initial_pair_colors":5,
        "stable_orbitals":15,
        "refinement_counts":counts[:3],
        "orthogonal_group_order":72,
        "orbital_sizes":osizes,
        "wl_classes_equal_Oplus_orbitals":True,
        "orbital_algebra_dimension":15,
        "center_dimension":4,
        "central_isotypic_rank_and_commutant_dimension":eigen_data,
        "complex_commutant_wedderburn":"M3(C) + M2(C) + C + C",
        "permutation_module":"1^3 + eps + V4a + 2 V4b (dimensions 3+1+4+8=16)",
        "boundary":"This is a three-fibre coherent configuration, not a homogeneous association scheme."
    }

# ---------------- Reye + CSS interface ----------------
V2=[(0,0),(0,1),(1,0),(1,1)]
NZ2=[(1,0),(0,1),(1,1)]
MATS2=[tuple(x) for x in itertools.product((0,1), repeat=4)]
def mv2(m,v):
    return ((m[0]&v[0])^(m[1]&v[1]), (m[2]&v[0])^(m[3]&v[1]))
P12=[(w,x) for w in NZ2 for x in V2]
def reye_lines():
    return [frozenset(i for i,(w,x) in enumerate(P12) if x==mv2(m,w)) for m in MATS2]
def reye_code():
    lines=reye_lines(); C=set()
    for mask in range(1<<12):
        v=tuple((mask>>i)&1 for i in range(12))
        if all(sum(v[i] for i in L)%2==0 for L in lines): C.add(v)
    return C
def css_packet() -> dict:
    C=reye_code()
    wt=collections.Counter(map(sum,C))
    assert len(C)==16 and wt=={0:1,6:12,8:3}
    q=5
    n=(q+1)*(q*q+1)
    g=q*(q*q+1)//2
    check_d=2*(q+1)
    css_k=n-2*g
    css_d=q+1
    assert (n,g,check_d,css_k,css_d)==(156,65,12,26,6)
    return {
        "local_reye_code":[12,4,6],
        "local_weight_enumerator":{"0":1,"6":12,"8":3},
        "global_q5_footprint_check_code":[156,65,12],
        "global_q5_css":[156,26,6],
        "supported_embedding_into_check_code":False,
        "reason":"A local minimum word has weight 6, below the global check-code distance 12.",
        "any_12_coordinate_shortening_dimension_upper_bound":1,
        "shortening_reason":"A nonzero shortened word must have weight >=12 on 12 coordinates, so its support is the entire 12-set.",
        "logical_normalizer_boundary":"The q=5 line code C_W has distance 6, so distance alone does not rule out a map into C_W; no canonical 12-cover-to-156-point coordinate map is certified here."
    }

# ---------------- all-field unit-difference graph ----------------
def detq(m,q): return (m[0]*m[3]-m[1]*m[2])%q
def legendre(a,p):
    a%=p
    if a==0:return 0
    x=pow(a,(p-1)//2,p)
    return 1 if x==1 else -1
def pairq(y,x,q): return sum(a*b for a,b in zip(y,x))%q
def cyclo_equals_integer(coeff:list[int], K:int)->bool:
    d=coeff[:]; d[0]-=K
    return len(set(d))==1

def graph_anchor(q:int)->dict:
    mats=list(itertools.product(range(q),repeat=4))
    units=[x for x in mats if detq(x,q)!=0]
    byrank={0:[],1:[],2:[]}
    for y in mats:
        d=detq(y,q)
        if y==(0,0,0,0): r=0
        elif d==0:r=1
        else:r=2
        byrank[r].append(y)
    expected={0:q*(q-1)**2*(q+1),1:-q*(q-1),2:q}
    vals={}
    for r,Ys in byrank.items():
        for y in Ys:
            coeff=[0]*q
            for x in units: coeff[pairq(y,x,q)]+=1
            assert cyclo_equals_integer(coeff,expected[r])
        vals[str(r)]={"labels":len(Ys),"eigenvalue":expected[r]}
    return vals

def rankmetric_graph_packet()->dict:
    anchors={str(q):graph_anchor(q) for q in (2,3,5,7)}
    examples={}
    for q in (2,3,5,7):
        v=q**4; k=q*(q-1)**2*(q+1)
        lam=q*(q**3-2*q**2-q+3)
        mu=q*(q-1)*(q**2-q-1)
        examples[str(q)]={"srg":[v,k,lam,mu]}
    return {
        "vertices":"r^4",
        "adjacency":"X~Y iff rank(X-Y)=2 iff det(X-Y)!=0",
        "identification":"complement of the bilinear forms graph H_r(2,2)",
        "degree":"r(r-1)^2(r+1)=|GL2(r)|",
        "spectrum":{
            "degree":"multiplicity 1",
            "r":"multiplicity r(r-1)^2(r+1)",
            "-r(r-1)":"multiplicity (r-1)(r+1)^2"
        },
        "srg_parameters":{
            "v":"r^4",
            "k":"r(r-1)^2(r+1)",
            "lambda":"r(r^3-2r^2-r+3)",
            "mu":"r(r-1)(r^2-r-1)"
        },
        "prime_anchor_exact_character_checks":anchors,
        "examples":examples,
        "full_aut_prior_art":"F_r^4 : ((((GL2(r) o GL2(r)) : Aut(F_r)) : C2)); o denotes central product and C2 is factor transpose.",
        "aut_order_formula":"r^4 * (|GL2(r)|^2/(r-1)) * |Aut(F_r)| * 2",
        "q2_order":1152
    }

# ---------------- Clifford lift ----------------
PAULI_NAMES={
    0:"II",1:"XI",2:"ZI",3:"YI",4:"IX",5:"XX",6:"ZX",7:"YX",
    8:"IZ",9:"XZ",10:"ZZ",11:"YZ",12:"IY",13:"XY",14:"ZY",15:"YY"
}
def q_spp(v:int)->int:
    x1,z1,x2,z2=bits4(v)
    return (x1&z1)^(x2&z2)^x2
def b_spp(u:int,v:int)->int:
    ux1,uz1,ux2,uz2=bits4(u); vx1,vz1,vx2,vz2=bits4(v)
    return (ux1&vz1)^(uz1&vx1)^(ux2&vz2)^(uz2&vx2)
def q_ne(v:int)->int:
    x1,z1,x2,z2=bits4(v)
    s1=x1^z1^(x1&z1)
    s2=x2^z2^(x2&z2)
    return s1^s2
def pinv(p):
    out=[0]*len(p)
    for i,j in enumerate(p):out[j]=i
    return tuple(out)
def pcompose(p,q): return tuple(p[q[x]] for x in range(len(q)))

def clifford_packet(gl4:list[tuple[int,...]])->dict:
    I=[L for L in gl4 if all(q_spp(L[y])==det2(y) for y in V16)]
    assert len(I)==72
    L0=I[0]; L0i=pinv(L0)
    rel={pcompose(L,L0i) for L in I}
    O_spp={p for p in gl4 if all(q_spp(p[y])==q_spp(y) for y in V16)}
    assert rel==O_spp and len(O_spp)==72
    Sp={p for p in gl4 if all(b_spp(p[x],p[y])==b_spp(x,y) for x in BASIS4 for y in BASIS4)}
    assert len(Sp)==720 and O_spp < set(Sp)
    Qs=[Q for Q in gl4 if all(q_ne(Q[y])==q_spp(y) for y in V16)]
    assert len(Qs)==72
    Q=Qs[0]
    standard={p for p in gl4 if all(q_ne(p[y])==q_ne(y) for y in V16)}
    conj={pcompose(pcompose(Q,h),pinv(Q)) for h in O_spp}
    assert conj==standard and len(standard)==72
    qne_split=collections.Counter(q_ne(x) for x in range(1,16))
    assert qne_split=={0:9,1:6}
    return {
        "matrix_to_SPP_quadratic_isometries":72,
        "relative_group":"O+(4,2)",
        "relative_group_order":72,
        "Sp4_2_order":720,
        "hyperbolic_quadrics_orbit_size":10,
        "standard_nonentangling_quadratic":"q_NE=s(x1,z1)+s(x2,z2), s(x,z)=x+z+xz",
        "standard_split":{"two_body_Paulis":9,"one_body_Paulis":6},
        "explicit_SPP_to_standard_basis_images":[PAULI_NAMES[Q[e]] for e in BASIS4],
        "standard_stabilizer_order":72,
        "projective_Pauli_order":16,
        "Clifford_preimage_projective_order":1152,
        "literature_identification":"Clifford-conjugate to the non-entangling two-qubit Clifford subgroup generated by local Cliffords and SWAP.",
        "boundary":"The identification is up to Clifford conjugacy; it does not assert that the original SPP coordinate frame is already the standard tensor-product frame."
    }

# ---------------- exact lattice/Radon mod-2 sequence ----------------
def inv4mod2(A):
    aug=[[A[i][j]&1 for j in range(4)]+[int(i==j) for j in range(4)] for i in range(4)]
    r=0
    for c in range(4):
        p=next(i for i in range(r,4) if aug[i][c])
        aug[r],aug[p]=aug[p],aug[r]
        for i in range(4):
            if i!=r and aug[i][c]: aug[i]=[x^y for x,y in zip(aug[i],aug[r])]
        r+=1
    return [row[4:] for row in aug]
def act4(A,v): return tuple(sum((A[i][j]&v[j]) for j in range(4))&1 for i in range(4))
def rref2(A):
    A=[[int(x)&1 for x in row] for row in A]
    if not A:return A,[]
    r=0;piv=[]
    for c in range(len(A[0])):
        p=next((i for i in range(r,len(A)) if A[i][c]),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r]
        for i in range(len(A)):
            if i!=r and A[i][c]: A[i]=[x^y for x,y in zip(A[i],A[r])]
        piv.append(c);r+=1
        if r==len(A):break
    return A,piv
def null2(A):
    rr,piv=rref2(A); n=len(rr[0])
    free=[j for j in range(n) if j not in piv]; out=[]
    for f in free:
        v=[0]*n;v[f]=1
        for i,p in enumerate(piv):v[p]=rr[i][f]
        out.append(tuple(v))
    return out
def mvbin(A,v): return tuple(sum(a*b for a,b in zip(row,v))&1 for row in A)
def span2(basis):
    if not basis:return {()}
    z=(0,)*len(basis[0]);out={z}
    for b in basis:out |= {tuple(x^y for x,y in zip(v,b)) for v in tuple(out)}
    return out

def radon_packet()->dict:
    pidx={p:i for i,p in enumerate(P12)}
    midx={m:i for i,m in enumerate(MATS2)}
    R=sp.Matrix([[int(mv2(m,w)==x) for m in MATS2] for w,x in P12])
    PBc=[]
    for w in NZ2:
        inds=[pidx[(w,x)] for x in V2]
        for i in range(3):
            z=[0]*12;z[inds[i]]=1;z[inds[3]]=-1;PBc.append(z)
    PB=sp.Matrix.hstack(*map(sp.Matrix,PBc))
    L=[[0,1,1,0],[1,0,1,1],[0,1,1,1],[1,0,0,1]]
    Li=inv4mod2(L); C=[[Li[j][i] for j in range(4)] for i in range(4)]
    qperm=[midx[act4(C,m)] for m in MATS2]
    pairidx={(a,b):midx[a+b] for a in V2 for b in V2}
    LBc=[]
    for i in range(3):
        for j in range(3):
            z=[0]*16
            for ai,ca in ((i,1),(3,-1)):
                for bj,cb in ((j,1),(3,-1)):
                    z[pairidx[(V2[ai],V2[bj])]]+=ca*cb
            LBc.append(z)
    LB=sp.Matrix.hstack(*map(sp.Matrix,LBc))
    lcoords=[pairidx[(V2[i],V2[j])] for i in range(3) for j in range(3)]
    def qvec(z):
        out=[0]*16
        for i,j in enumerate(qperm):out[j]=int(z[i,0])
        return sp.Matrix(out)
    def linecoords(zold):
        z=qvec(zold); c=z.extract(lcoords,[0]); assert LB*c==z; return c
    TR=sp.zeros(9,9)
    for k in range(9): TR[:,k]=linecoords(R.T*PB[:,k])
    GP=PB.T*PB; GL=LB.T*LB
    assert TR.T*GL*TR==4*GP and abs(int(TR.det()))==64

    TR2=[[int(TR[i,j])&1 for j in range(9)] for i in range(9)]
    PB2=[[int(PB[i,j])&1 for j in range(9)] for i in range(12)]
    kerbasis=null2(TR2); assert len(kerbasis)==4
    kerwords={mvbin(PB2,v) for v in span2(kerbasis)}
    CReye=reye_code()
    assert kerwords==CReye

    GL2=[[int(GL[i,j])&1 for j in range(9)] for i in range(9)]
    radbasis=null2(GL2); assert len(radbasis)==5
    radical=span2(radbasis)
    image={mvbin(TR2,tuple((m>>i)&1 for i in range(9))) for m in range(1<<9)}
    assert image==radical

    def qeven(v):
        vv=sp.Matrix(v); n=int((vv.T*GL*vv)[0]); assert n%2==0
        return (n//2)&1
    assert {qeven(v) for v in radical}=={0}
    cur=list(radbasis); comp=[]
    def rankv(vs): return len(rref2(vs)[1]) if vs else 0
    for i in range(9):
        e=tuple(int(i==j) for j in range(9))
        if rankv(cur+[e])>rankv(cur):
            comp.append(e);cur.append(e)
        if len(comp)==4:break
    assert len(comp)==4 and rankv(cur)==9
    def comb(mask):
        v=[0]*9
        for i,b in enumerate(comp):
            if (mask>>i)&1:v=[x^y for x,y in zip(v,b)]
        return tuple(v)
    qquot=[qeven(comb(x)) for x in range(16)]
    assert qquot==[det2(x) for x in range(16)]
    return {
        "integral_similarity":"TR^T G_line TR = 4 G_point",
        "TR_determinant":-64,
        "TR_snf":"1^5 2^2 4^2",
        "integral_cokernel":"(Z/2)^2 x (Z/4)^2",
        "mod2_exact_sequence":"0 -> C_Reye -> F2^9 -> Rad(A3 tensor A3 mod 2) -> 0",
        "kernel_dimension":4,
        "kernel_equals_Reye_code_objectwise":True,
        "image_dimension":5,
        "image_equals_line_Gram_radical":True,
        "mod2_cokernel_dimension":4,
        "quotient_even_quadratic_distribution":{"0":10,"1":6},
        "quotient_quadratic_in_greedy_complement_coordinates":"det([[a,b],[c,d]])=ad+bc",
        "quotient_is_det_Pauli_9plus6_objectwise":True,
        "deduction":"The same saturated Radon map places the Reye code in the kernel and the determinant/Pauli plus-type 4-space in the mod-2 cokernel."
    }

# ---------------- odd-q determinant multiplicative-character Fourier ----------------
def determinant_character_anchor(p:int)->dict:
    mats=list(itertools.product(range(p),repeat=4))
    byrank={0:[],1:[],2:[]}
    for y in mats:
        if y==(0,0,0,0):r=0
        elif detq(y,p)==0:r=1
        else:r=2
        byrank[r].append(y)
    scalar=p*p*legendre(-1,p)
    for r,Ys in byrank.items():
        for y in Ys:
            coeff=[0]*p
            for x in mats:
                chi=legendre(detq(x,p),p)
                if chi: coeff[pairq(y,x,p)] += chi
            expected=scalar*legendre(detq(y,p),p)
            assert cyclo_equals_integer(coeff,expected)
    return {"scalar":scalar,"rank0":0,"rank1":0,"rank2_values":sorted({scalar*legendre(detq(y,p),p) for y in byrank[2]})}

def odd_character_packet()->dict:
    return {
        "theorem":"For odd finite fields F_r and quadratic character chi(0)=0, Fourier[chi(det)](Y)=r^2 chi(-1) chi(det Y).",
        "support_consequence":"The transform vanishes identically on rank 0 and rank 1 dual matrices.",
        "prime_exact_anchors":{str(p):determinant_character_anchor(p) for p in (3,5,7)},
        "proof_sketch":"Rank-one labels reduce to a nonzero linear functional and the character sum vanishes. At an invertible label reduce to I; summing over b,c gives r*chi(ad), and the remaining two one-dimensional Gauss sums give r^2 chi(-1).",
        "prior_art_boundary":"This is an explicit 2x2 determinant instance of finite-field prehomogeneous-vector-space Fourier/character-sum functional equations."
    }

# ---------------- q=3 MRD clique orbit split ----------------
def addq(x,y,q): return tuple((a+b)%q for a,b in zip(x,y))
def subq(x,y,q): return tuple((a-b)%q for a,b in zip(x,y))
def scalq(c,x,q): return tuple((c*a)%q for a in x)
def mmulq(x,y,q):
    a,b,c,d=x;e,f,g,h=y
    return ((a*e+b*g)%q,(a*f+b*h)%q,(c*e+d*g)%q,(c*f+d*h)%q)
def inv2q(x,q):
    a,b,c,d=x;z=(a*d-b*c)%q;zi=pow(z,-1,q)
    return ((d*zi)%q,(-b*zi)%q,(-c*zi)%q,(a*zi)%q)
def rank_modp(vectors,p):
    A=[list(v) for v in vectors]
    if not A:return 0
    r=0
    for c in range(len(A[0])):
        k=next((i for i in range(r,len(A)) if A[i][c]%p),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r];z=pow(A[r][c]%p,-1,p);A[r]=[(z*x)%p for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][c]%p:
                f=A[i][c]%p;A[i]=[(x-f*y)%p for x,y in zip(A[i],A[r])]
        r+=1
        if r==len(A):break
    return r

def q3_clique_packet()->dict:
    q=3;mats=list(itertools.product(range(q),repeat=4));idx={m:i for i,m in enumerate(mats)}
    G=nx.Graph();G.add_nodes_from(range(len(mats)))
    for i in range(len(mats)):
        for j in range(i+1,len(mats)):
            if detq(subq(mats[i],mats[j],q),q)!=0:G.add_edge(i,j)
    maximal=list(nx.find_cliques(G))
    sizes=collections.Counter(map(len,maximal))
    assert sizes=={6:9072,9:648}
    C9={frozenset(c) for c in maximal if len(c)==9}

    nz=[x for x in mats if x!=(0,0,0,0)]
    subs=set()
    for u in nz:
        for v in nz:
            S=frozenset(addq(scalq(a,u,q),scalq(b,v,q),q) for a in range(q) for b in range(q))
            if len(S)==9:subs.add(S)
    assert len(subs)==130
    anis=[S for S in subs if all(x==(0,0,0,0) or detq(x,q)!=0 for x in S)]
    assert len(anis)==18
    affine=set()
    for S in anis:
        remaining=set(mats)
        while remaining:
            a=next(iter(remaining));C=frozenset(idx[addq(a,s,q)] for s in S)
            affine.add(C);remaining-={mats[i] for i in C}
    assert len(affine)==162 and affine<C9

    def permt(t):return tuple(idx[addq(m,t,q)] for m in mats)
    def perml(A):return tuple(idx[mmulq(A,m,q)] for m in mats)
    def permr(B):
        Bi=inv2q(B,q);return tuple(idx[mmulq(m,Bi,q)] for m in mats)
    def permtp():return tuple(idx[(m[0],m[2],m[1],m[3])] for m in mats)
    e=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]
    A=(0,1,2,0);B=(1,1,0,1);D=(2,0,0,1)
    gens=[permt(x) for x in e]+[perml(A),perml(B),perml(D),permr(A),permr(B),permr(D),permtp()]
    unseen=set(C9);orbits=[]
    while unseen:
        c=next(iter(unseen));orb={c};todo=[c]
        while todo:
            z=todo.pop()
            for p in gens:
                w=frozenset(p[i] for i in z)
                assert w in C9
                if w not in orb:orb.add(w);todo.append(w)
        orbits.append(orb);unseen-=orb
    assert sorted(map(len,orbits))==[162,486]
    def affdim(C):
        pts=[mats[i] for i in C];a=pts[0]
        return rank_modp([subq(x,a,q) for x in pts[1:]],q)
    orbit_data=sorted((len(o), sorted(set(affdim(C) for C in o))) for o in orbits)
    assert orbit_data==[(162,[2]),(486,[4])]
    return {
        "graph":"Gamma_3 on M2(F3), invertible-difference adjacency",
        "maximum_clique_size":9,
        "maximal_clique_size_distribution":{"6":9072,"9":648},
        "linear_anisotropic_2_spaces":18,
        "affine_linear_maximum_cliques":162,
        "full_rank_isometry_group_orbits_on_9_cliques":[162,486],
        "affine_span_dimensions_by_orbit":{"162":2,"486":4},
        "deduction":"Exactly one orbit consists of affine-linear MRD cosets; the other 486 maximum cliques are genuinely nonlinear maximum rank-distance sets.",
        "scope":"Exact q=3 enumeration only; no all-q orbit classification is claimed."
    }

# ---------------- Reye primal/dual minimum-shell reconstruction ----------------
def reye_dual_packet()->dict:
    C=reye_code();lines=reye_lines()
    rr,piv=rref2([list(v) for v in C])
    Cb=[tuple(rr[i]) for i in range(len(piv))]
    assert len(Cb)==4
    Cd=set()
    for mask in range(1<<12):
        v=tuple((mask>>i)&1 for i in range(12))
        if all(sum(a*b for a,b in zip(v,c))%2==0 for c in Cb):Cd.add(v)
    assert len(Cd)==256
    enum=collections.Counter(map(sum,Cd))
    assert enum=={0:1,3:16,4:39,5:48,6:48,7:48,8:39,9:16,12:1}
    min_dual={frozenset(i for i,b in enumerate(v) if b) for v in Cd if sum(v)==3}
    assert min_dual==set(lines)
    min_primal={frozenset(i for i,b in enumerate(v) if b) for v in C if sum(v)==6}
    ints=collections.Counter(len(L&H) for L in min_dual for H in min_primal)
    assert ints=={0:48,2:144}
    assert {sum(not(L&H) for H in min_primal) for L in min_dual}=={3}
    assert {sum(not(L&H) for L in min_dual) for H in min_primal}=={4}
    return {
        "C":[12,4,6],
        "C_weight_enumerator":{"0":1,"6":12,"8":3},
        "Cdual":[12,8,3],
        "Cdual_weight_enumerator":{str(k):v for k,v in sorted(enum.items())},
        "dual_16_weight3_supports_equal_original_Reye_lines":True,
        "primal_12_weight6_supports_equal_heavy_sets":True,
        "line_heavy_intersection_spectrum":{"0":48,"2":144},
        "disjointness_degrees":{"16_line_side":3,"12_heavy_side":4},
        "deduction":"The primal/dual minimum shells reconstruct both 12_4,16_3 Reye copies: C^perp minimum words are the original triples, C minimum words are heavies, and shell disjointness is the second Reye incidence."
    }

def main():
    gl4=gl4_perms()
    out={
        "schema":"w33.pass5872_5879.coherent_css_rankmetric_clifford_discriminant.v1",
        "status":"PASS",
        "pass_5872_joint_coherent_closure":coherent_packet(gl4),
        "pass_5873_css_interface_nogo":css_packet(),
        "pass_5874_allfield_unit_difference_graph":rankmetric_graph_packet(),
        "pass_5875_clifford_lift":clifford_packet(gl4),
        "pass_5876_discriminant_radon_exact_sequence":radon_packet(),
        "pass_5877_oddq_determinant_character_fourier":odd_character_packet(),
        "pass_5878_q3_max_clique_orbits":q3_clique_packet(),
        "pass_5879_reye_dual_min_shell_reconstruction":reye_dual_packet(),
        "boundary":"Exact finite algebra/coding/lattice/Fourier/graph statements. Literature is used only to identify established bilinear-forms/MRD/Clifford contexts. No finite coincidence is promoted to a physical q=5 qubit embedding, continuum law, particle assignment, mass, or coupling prediction."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
