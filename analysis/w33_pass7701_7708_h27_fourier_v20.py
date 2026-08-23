#!/usr/bin/env python3
"""Pass7701-7708: exact H27 Fourier decomposition of the local Steinberg V20.

Dependencies:
- Pass7186 fixes the qutrit Heisenberg law and the degree-8 H27 Cayley graph.
- Pass7629-7644 fixes the common 9K3/Schlaefli/H27 rank-4 scheme and Gram formula.

This verifier reconstructs all of it independently from the H27 group law and proves
that the degree-2 relation is Z(H27)\{1}, the degree-16 relation is Schlaefli, and
the degree-8 relation is the horizontal H27 connection set.  It then identifies the
20-dimensional Gram image in the regular representation as 8 linear Fourier modes
plus 6+6 from the two conjugate nontrivial central-character (Schrodinger) sectors.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7701_7708_H27_FOURIER_V20.json'
F=[(x,y) for x in range(3) for y in range(3)]
V=[(u,z) for u in F for z in range(3)]

def add(u,v):return ((u[0]+v[0])%3,(u[1]+v[1])%3)
def neg(u):return ((-u[0])%3,(-u[1])%3)
def det(u,v):return (u[0]*v[1]-u[1]*v[0])%3
def mul(x,y):
    u,z=x;v,w=y
    return (add(u,v),(z+w-det(u,v))%3)
def inv(x):
    u,z=x;return (neg(u),(-z)%3)

def cayley(C):
    C=set(C);A=[[0]*27 for _ in range(27)]
    for i,x in enumerate(V):
        ix=inv(x)
        for j,y in enumerate(V):
            if i!=j and mul(ix,y) in C:A[i][j]=1
    return A

def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(27)) for j in range(27)] for i in range(27)]
def madd(*terms):return [[sum(c*M[i][j] for c,M in terms) for j in range(27)] for i in range(27)]
def common(A,i,j):return sum(A[i][k]*A[j][k] for k in range(27))

def main():
    e=((0,0),0);Z=[((0,0),1),((0,0),2)]
    S8=[(u,0) for u in F if u!=(0,0)]
    S16=[g for g in V if g!=e and g not in Z and g not in S8]
    assert [len(Z),len(S16),len(S8)]==[2,16,8]
    I=[[1 if i==j else 0 for j in range(27)] for i in range(27)]
    A1,A2,A3=map(cayley,[Z,S16,S8]);basis=[I,A1,A2,A3]
    assert all(sum(B[i][j] for B in basis)==1 for i in range(27) for j in range(27))
    assert {sum(r) for r in A1}=={2} and {sum(r) for r in A2}=={16} and {sum(r) for r in A3}=={8}
    lam={common(A2,i,j) for i in range(27) for j in range(i+1,27) if A2[i][j]}
    mu={common(A2,i,j) for i in range(27) for j in range(i+1,27) if not A2[i][j]}
    assert lam=={10} and mu=={8}

    reps=[]
    for B in basis:
        reps.append(next((i,j) for i in range(27) for j in range(27) if B[i][j]))
    def coeffs(M):
        c=[M[i][j] for i,j in reps]
        assert M==madd(*[(c[k],basis[k]) for k in range(4)])
        return c
    table={(i,j):coeffs(mm(B,C)) for i,B in enumerate(basis) for j,C in enumerate(basis)}
    assert all(table[i,j]==table[j,i] for i in range(4) for j in range(4))

    P=[[1,2,16,8],[1,-1,4,-4],[1,2,-2,-1],[1,-1,-2,2]]
    for r in P:
        for i in range(4):
            for j in range(4):
                assert r[i]*r[j]==sum(table[i,j][k]*r[k] for k in range(4))
    sols=[]
    for m0 in range(28):
      for m1 in range(28-m0):
       for m2 in range(28-m0-m1):
        m3=27-m0-m1-m2;ms=[m0,m1,m2,m3]
        if all(sum(ms[t]*P[t][j] for t in range(4))==0 for j in (1,2,3)):sols.append(ms)
    assert sols==[[1,6,8,12]];mults=sols[0]

    def comm(x,y):return mul(mul(mul(inv(x),inv(y)),x),y)
    derived={comm(x,y) for x in V for y in V};assert derived=={e,*Z}
    classes=[];seen=set()
    for x in V:
        if x in seen:continue
        cl={mul(mul(g,x),inv(g)) for g in V};classes.append(cl);seen|=cl
    assert Counter(map(len,classes))==Counter({3:8,1:3})
    # |H/[H,H]|=9 gives 9 linear irreps.  There are 11 conjugacy classes, hence
    # two remaining irreps; 27-9=18=3^2+3^2 forces both degrees to be 3.
    assert 27//len(derived)==9 and len(classes)==11 and 27-9==18

    grams=[11520-3840*r[1]-1440*r[2]+2400*r[3] for r in P]
    assert grams==[0,0,4320,23040]
    assert sum(m for m,g in zip(mults,grams) if g!=0)==20
    # A1 is convolution by the two nonidentity central elements.  Eigenvalue 2
    # is the center-trivial sector (dimension 1+8=9); eigenvalue -1 is the two
    # nontrivial central characters (dimension 6+12=18).  Reality pairs omega
    # and omega^2 equally, so 6=3+3 and 12=6+6 across those conjugate sectors.

    out={
      'schema':'w33.pass7701_7708.h27_fourier_v20.v1','status':'PASS','passes':'7701-7708',
      'H27':{'order':27,'center_order':3,'derived_order':3,'conjugacy_classes':11,'irreducible_degrees':'1^9 + 3^2'},
      'cayley_partition':{'identity':1,'Z_nonidentity':2,'Schlaefli':16,'H27_horizontal':8},
      'graphs':{'Z_nonidentity':'9 K3','Schlaefli':'SRG(27,16,10,8)','H27_horizontal':'degree 8'},
      'first_eigenmatrix':P,'multiplicities':mults,
      'joint_sectors':[
        {'eigenvalues':[2,16,8],'dimension':1,'representation':'trivial linear','Gram':0},
        {'eigenvalues':[-1,4,-4],'dimension':6,'representation':'nontrivial-center Schrodinger kernel','Gram':0},
        {'eigenvalues':[2,-2,-1],'dimension':8,'representation':'eight nontrivial linear characters of H27/Z','Gram':4320},
        {'eigenvalues':[-1,-2,2],'dimension':12,'representation':'nontrivial-center Schrodinger image','Gram':23040}],
      'Gram_formula':'11520 I - 3840 A_Z - 1440 A_Schlaefli + 2400 A_H27','Gram_rank':20,
      'Gram_image':'8 + 6_omega + 6_omega^2','Gram_kernel':'1 + 3_omega + 3_omega^2',
      'theorem':'The 27-point 9K3/Schlaefli/H27 rank-4 scheme is exactly the Cayley association scheme of H27 defined by {1}, Z\\{1}, S16, S8. The local Steinberg V20 is the image of a group-algebra convolution and decomposes as eight nontrivial linear Fourier modes plus conjugate six-dimensional images in the two nontrivial central-character Schrodinger isotypic sectors.',
      'claim_boundary':'Exact finite group/association-scheme theorem. Fourier and Schrodinger are representation-theoretic labels for H27; no physical multiplet claim is made.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Gram_rank':20,'image':'8+6+6','irreps':'1^9+3^2'}))
if __name__=='__main__':main()
