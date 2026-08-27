#!/usr/bin/env python3
"""Pass10581-10588: exact central-C3 Fourier decomposition of H27 adjacency.

H27 is the Heisenberg Cayley graph on vertices (u,z), u in F3^2, z in F3,
with connection set {(v,0):v!=0}.  The center Z=C3 translates z, hence the
27-dimensional permutation space splits into three 9-dimensional central
character sectors.

For the trivial character the block is K9 adjacency, spectrum 8^1+(-1)^8.
For either nontrivial character the block is a 9x9 Hermitian magnetic matrix
over Z[omega], omega^2+omega+1=0.  We verify exactly

    (B-2I)(B+4I)=0,

and trace(B)=0, forcing spectrum 2^6+(-4)^3 in each nontrivial sector.
Thus the global H27 eigenspace dimensions 1|8|12|6 are exactly the central-C3
Fourier decomposition: (1+8) in the trivial sector and two copies of (6+3).
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10581_10588_H27_CENTRAL_C3_FOURIER.json'
F=[(a,b) for a in range(3) for b in range(3)]
N=9

def add(u,v): return ((u[0]+v[0])%3,(u[1]+v[1])%3)
def det(u,v): return (u[0]*v[1]-u[1]*v[0])%3
def coc(u,v): return (-det(u,v))%3

# Eisenstein integers a+b*w with w^2+w+1=0, stored as integer pairs.
def ea(x,y): return (x[0]+y[0],x[1]+y[1])
def en(x): return (-x[0],-x[1])
def es(c,x): return (c*x[0],c*x[1])
def em(x,y):
    a,b=x;c,d=y
    return (a*c-b*d, a*d+b*c-b*d)
def ew(k):
    k%=3
    return [(1,0),(0,1),(-1,-1)][k]
def ez(): return (0,0)
def one(): return (1,0)

def mat0(n=N): return [[ez() for _ in range(n)] for _ in range(n)]
def eye(n=N):
    A=mat0(n)
    for i in range(n): A[i][i]=one()
    return A
def madd(A,B): return [[ea(A[i][j],B[i][j]) for j in range(len(A[0]))] for i in range(len(A))]
def mscale(c,A): return [[es(c,x) for x in row] for row in A]
def mm(A,B):
    n=len(A);m=len(B[0]);k=len(B)
    C=[[ez() for _ in range(m)] for _ in range(n)]
    for i in range(n):
      for r in range(k):
        if A[i][r]!=(0,0):
          for j in range(m):
            if B[r][j]!=(0,0): C[i][j]=ea(C[i][j],em(A[i][r],B[r][j]))
    return C
def meq0(A): return all(x==(0,0) for row in A for x in row)
def trace(A):
    t=ez()
    for i in range(len(A)): t=ea(t,A[i][i])
    return t

def block(k):
    B=mat0()
    for i,u in enumerate(F):
      for v in F:
        if v==(0,0): continue
        j=F.index(add(u,v));B[i][j]=ea(B[i][j],ew(k*coc(u,v)))
    return B

def main():
    I=eye()
    B0=block(0)
    # (B0-8I)(B0+I)=0.
    assert meq0(mm(madd(B0,mscale(-8,I)),madd(B0,I)))
    assert trace(B0)==(0,0)  # 8*1 + (-1)*8 = 0
    nontriv=[]
    for k in (1,2):
        B=block(k)
        # (B-2I)(B+4I)=0 exactly in Z[w].
        assert meq0(mm(madd(B,mscale(-2,I)),madd(B,mscale(4,I))))
        assert trace(B)==(0,0)
        nontriv.append({'character':k,'dimension':9,'spectrum':{'2':6,'-4':3}})
    out={
      'schema':'w33.pass10581_10588.h27_central_c3_fourier.v1','status':'PASS','passes':'10581-10588',
      'center':'C3 acting by z-translation on H27',
      'sector_dimensions':[9,9,9],
      'trivial_sector':{'graph':'K9 adjacency','annihilator':'(x-8)(x+1)','spectrum':{'8':1,'-1':8}},
      'nontrivial_sectors':nontriv,
      'global_spectrum':{'8':1,'-1':8,'2':12,'-4':6},
      'constituent_explanation':'1|8 comes from the trivial central character; 12|6 is the sum of two conjugate nontrivial sectors, each split 6|3.',
      'theorem':'The H27 spectral multiplicities 1,8,12,6 are exactly the central-C3 Fourier decomposition of its Heisenberg Cayley adjacency. The trivial central character is K9 with 8^1+(-1)^8; each nontrivial central character is an exact Eisenstein-Hermitian magnetic block with spectrum 2^6+(-4)^3.',
      'boundary':'Exact finite Heisenberg/Eisenstein-ring computation. No identification with the H(4)/(13:6) weighted transport is asserted here.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','sectors':['8^1,-1^8','2^6,-4^3','2^6,-4^3']}))
if __name__=='__main__': main()
