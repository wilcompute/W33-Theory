#!/usr/bin/env python3
"""Pass8301-8308: the 64 W33 leaves that meet the embedded Q+(3,3) residue in a line.

Dependencies:
- Pass7465/7501 common E8/A2/2240-leaf reconstruction;
- Pass7949 explicit Q+(3,3)=PG(1,3)xPG(1,3) embedding through 16 current A2 radicals.

This pass classifies the induced 64-leaf distance-one graph and the faithful action
of the projective E8 set-stabilizer of the 16-point subquadric.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
from sympy import Matrix, symbols, factor
from sympy.combinatorics import Permutation,PermutationGroup
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
OUT=ROOT/'data/PART_W33_PASS8301_8308_QPLUS33_64LEAF_RESIDUE.json'
T=np.array([[0,1,2,0],[1,0,0,1],[1,1,1,2],[1,2,2,2]],dtype=np.int8)%3

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:
            s=1 if x==1 else 2
            return tuple((s*y)%3 for y in v)
    raise ValueError('zero')
def qdet(x):return (x[0]*x[3]-x[1]*x[2])%3
def pkey(g,n):return tuple(int(g(i)) for i in range(n))

def main():
    R,A2,ag,J,base,leaves,lgens,parity=E.build()
    radicals=[]
    for S in A2:
        vals=set()
        for i,j in itertools.combinations(sorted(S),2):
            if E.dot(R[i],R[j])==-4:
                vals.add(E.canon3(tuple(R[i][k]-R[j][k] for k in range(8))))
        assert len(vals)==1;radicals.append(next(iter(vals)))
    ri={v:i for i,v in enumerate(radicals)};assert len(ri)==1120

    rank1=sorted({canon(x) for x in itertools.product(range(3),repeat=4) if any(x) and qdet(x)==0})
    assert len(rank1)==16
    U=[];labels=[]
    for x in rank1:
        y4=tuple(int(z) for z in (T@np.array(x,dtype=np.int8))%3)
        y=E.canon3(y4+(0,0,0,0));U.append(ri[y])
        M=np.array(x,dtype=np.int8).reshape(2,2)%3
        col=next(tuple(int(z) for z in M[:,j]) for j in range(2) if np.any(M[:,j]))
        row=next(tuple(int(z) for z in M[i,:]) for i in range(2) if np.any(M[i,:]))
        labels.append((canon(col),canon(row)))
    U=set(U);assert len(U)==16
    dirs=sorted({x for z in labels for x in z});assert len(dirs)==4
    idlab={a:labels[i] for i,a in enumerate(sorted(U))}  # only used for cardinality-independent block names below
    # Rebuild label map in the actual rank1/U correspondence order.
    idlab={}
    for x in rank1:
        y4=tuple(int(z) for z in (T@np.array(x,dtype=np.int8))%3);a=ri[E.canon3(y4+(0,0,0,0))]
        M=np.array(x,dtype=np.int8).reshape(2,2)%3
        col=next(tuple(int(z) for z in M[:,j]) for j in range(2) if np.any(M[:,j]))
        row=next(tuple(int(z) for z in M[i,:]) for i in range(2) if np.any(M[i,:]))
        idlab[a]=(canon(col),canon(row))
    lines={}
    for side in (0,1):
        for d in dirs:
            S=frozenset(a for a,l in idlab.items() if l[side]==d);assert len(S)==4;lines[(side,d)]=S
    assert len(set(lines.values()))==8

    selected=[i for i,L in enumerate(leaves) if len(set(L)&U)==4]
    assert len(selected)==64 and Counter(parity[i] for i in selected)==Counter({0:32,1:32})
    line_of={}
    for i in selected:
        X=frozenset(set(leaves[i])&U);ks=[k for k,S in lines.items() if S==X];assert len(ks)==1;line_of[i]=ks[0]
    assert Counter(line_of.values())==Counter({k:8 for k in lines})

    masks={i:sum(1<<x for x in leaves[i]) for i in selected};pos={v:i for i,v in enumerate(selected)}
    A=np.zeros((64,64),dtype=np.uint8)
    for a,i in enumerate(selected):
        for b,j in enumerate(selected[a+1:],start=a+1):
            if (masks[i]&masks[j]).bit_count()==13:A[a,b]=A[b,a]=1
    assert set(map(int,A.sum(1)))=={8} and int(A.sum())//2==256
    cp=factor(Matrix(A.astype(int).tolist()).charpoly().as_expr())
    lam=symbols('lambda')
    assert cp==lam**38*(lam-8)*(lam-4)**12*(lam+4)**12*(lam+8)

    side0=[i for i in selected if parity[i]==0];side1=[i for i in selected if parity[i]==1]
    B=A[np.ix_([pos[i] for i in side0],[pos[i] for i in side1])]
    C=B@B.T
    assert Counter(int(C[i,j]) for i in range(32) for j in range(i+1,32))==Counter({2:256,0:144,4:96})
    rel={}
    for z in (0,2,4):
        M=(C==z).astype(np.uint8);np.fill_diagonal(M,0);rel[z]=sorted(set(map(int,M.sum(1))))
    assert rel=={0:[9],2:[16],4:[6]}
    # common-neighbor-2 is K16,16 across the two reguli; common-neighbor-4 is two rook graphs.
    for a,i in enumerate(side0):
        for b,j in enumerate(side0):
            if a>=b:continue
            ss=line_of[i][0]==line_of[j][0];sl=line_of[i]==line_of[j];z=int(C[a,b])
            if not ss:assert z==2
            elif sl:assert z==4
    R4=(C==4).astype(np.uint8);np.fill_diagonal(R4,0)
    rcp=factor(Matrix(R4.astype(int).tolist()).charpoly().as_expr())
    assert rcp==(lam-6)**2*(lam-2)**12*(lam+2)**18

    # Orbit of the embedded Q+(3,3) under projective W(E8), then a simultaneous
    # action on that orbit and the 2240 leaves.  Stabilizing orbit point 0 keeps
    # the original words, so restriction to the selected 64 leaves is literal.
    U0=frozenset(U);orb=[U0];oi={U0:0};dq=deque([U0])
    while dq:
        X=dq.popleft()
        for g in ag:
            Y=frozenset(g[x] for x in X)
            if Y not in oi:oi[Y]=len(orb);orb.append(Y);dq.append(Y)
    assert len(orb)==3150
    qgens=[tuple(oi[frozenset(g[x] for x in Q)] for Q in orb) for g in ag]
    off=len(orb);comb=[]
    for qg,lg in zip(qgens,lgens):comb.append(Permutation(list(qg)+[off+x for x in lg],size=off+2240))
    G=PermutationGroup(comb);assert int(G.order())==348364800
    H=G.stabilizer(0);assert int(H.order())==110592
    h64=[]
    for h in H.generators:
        arr=[]
        for v in selected:
            w=int(h(off+v))-off;assert w in pos;arr.append(pos[w])
        h64.append(Permutation(arr,size=64))
    K=PermutationGroup(h64);assert int(K.order())==55296 and [len(o) for o in K.orbits()]==[64]
    assert int(H.order())//int(K.order())==2

    # Exact normal series.  K'' is elementary abelian 2^8; conjugation quotient
    # has order 216.  Its derived 3^3 and 2^3 conjugation image have the diagonal
    # sign pattern of S3^3.
    D1=K.derived_subgroup();D2=D1.derived_subgroup();assert int(D1.order())==6912 and int(D2.order())==256
    assert D2.derived_subgroup().order()==1
    assert Counter(int(x.order()) for x in D2.generate_schreier_sims())==Counter({2:255,1:1})
    assert sorted(len(o) for o in D2.orbits())==[16,16,16,16]
    assert int(K.centralizer(D2).order())==256
    de=list(D2.generate_schreier_sims());di={pkey(x,64):i for i,x in enumerate(de)}
    qper=[]
    for h in K.generators:
        hi=~h;qper.append(Permutation([di[pkey(h*x*hi,64)] for x in de],size=256))
    Q=PermutationGroup(qper);assert int(Q.order())==216
    assert Counter(int(x.order()) for x in Q.generate_schreier_sims())==Counter({6:126,2:63,3:26,1:1})
    Q3=Q.derived_subgroup();assert int(Q3.order())==27 and int(Q.centralizer(Q3).order())==27
    assert Counter(int(x.order()) for x in Q3.generate_schreier_sims())==Counter({3:26,1:1})
    ae=list(Q3.generate_schreier_sims());ai={pkey(x,256):i for i,x in enumerate(ae)}
    cper=[]
    for h in Q.generators:
        hi=~h;cper.append(Permutation([ai[pkey(h*x*hi,256)] for x in ae],size=27))
    C2=PermutationGroup(cper);assert int(C2.order())==8 and Counter(int(x.order()) for x in C2.generate_schreier_sims())==Counter({2:7,1:1})
    fixed=Counter(sum(int(g(i))==i for i in range(27)) for g in C2.generate_schreier_sims() if int(g.order())==2)
    assert fixed==Counter({9:3,3:3,1:1})

    out={
      'schema':'w33.pass8301_8308.qplus33_64leaf_residue.v1','status':'PASS','passes':'8301-8308',
      'embedded_Qplus33_points':16,'embedded_lines':8,'selected_W33_leaves':64,'triality_family_split':[32,32],
      'induced_leaf_graph':{'vertices':64,'degree':8,'edges':256,'connected':True,'bipartite':[32,32],'spectrum':'8^1 4^12 0^38 (-4)^12 (-8)^1'},
      'one_side_common_neighbor_scheme':{'counts':{'0':144,'2':256,'4':96},'degree_relations':{'0':9,'2':16,'4':6},'relation_2':'K16,16 across the two reguli','relation_4':'2 disjoint rook graphs R(4,4), one per regulus'},
      'subquadric_orbit_under_projective_E8':3150,'subquadric_stabilizer_order':110592,
      'faithful_64_leaf_action':{'order':55296,'kernel_from_subquadric_stabilizer':2,'transitive':True,'second_derived':'C2^8','C2^8_orbits':[16,16,16,16],'quotient':'S3^3','exact_sequence':'1 -> C2^8 -> G64 -> S3^3 -> 1'},
      'quotient_certificate':{'order':216,'element_orders':{'1':1,'2':63,'3':26,'6':126},'derived':'C3^3','sign_image':'C2^3','nonidentity_sign_fixed_counts_on_C3^3':{'9':3,'3':3,'1':1}},
      'theorem':'The 64 Eisenstein W33 leaves meeting the explicit Q+(3,3) residue in a full line form a connected 8-regular bipartite 32+32 graph with spectrum +/-8, +/-4 and 0 as certified. The projective-E8 residue stabilizer acts transitively with faithful image 55296 and exact normal series 1 -> C2^8 -> G64 -> S3^3 -> 1. The four C2^8 orbits are the four (triality family, regulus) 16-blocks.',
      'claim_boundary':'Exact finite E8/A2/leaf residue theorem. No Monster or physical identification is inferred here.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','leaves':64,'G64':55296,'quotient':'S3^3'}))
if __name__=='__main__':main()
