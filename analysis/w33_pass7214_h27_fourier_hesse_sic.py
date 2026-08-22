#!/usr/bin/env python3
"""Pass7214: central Fourier blocks of H27 and exact Hesse-SIC/ETF recovery."""
from __future__ import annotations
import itertools,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7214_H27_FOURIER_HESSE_SIC.json'
# Z[omega], omega^2+omega+1=0, element a+b*omega.
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def neg(x): return (-x[0],-x[1])
def sub(x,y): return add(x,neg(y))
def mul(x,y):
    a,b=x;c,d=y
    return (a*c-b*d,a*d+b*c-b*d)
def conj(x): return (x[0]-x[1],-x[1])
def scale(n,x): return (n*x[0],n*x[1])
def wpow(e): return ((1,0),(0,1),(-1,-1))[e%3]
Z=(0,0); ONE=(1,0)
def mmul(A,B):
    n=len(A);m=len(B[0]);k=len(B)
    C=[[Z for _ in range(m)] for __ in range(n)]
    for i in range(n):
      for t in range(k):
        if A[i][t]==Z: continue
        for j in range(m):
          if B[t][j]!=Z:C[i][j]=add(C[i][j],mul(A[i][t],B[t][j]))
    return C
def det3(A):
    return add(add(mul(A[0][0],sub(mul(A[1][1],A[2][2]),mul(A[1][2],A[2][1]))),
                   neg(mul(A[0][1],sub(mul(A[1][0],A[2][2]),mul(A[1][2],A[2][0]))))),
               mul(A[0][2],sub(mul(A[1][0],A[2][1]),mul(A[1][1],A[2][0]))))
def ip(x,y):
    z=Z
    for a,b in zip(x,y):z=add(z,mul(conj(a),b))
    return z

def lines_ag23(U):
    dirs=[(1,0),(0,1),(1,1),(1,2)];S=set()
    for u in U:
      for d in dirs:S.add(tuple(sorted((((u[0]+t*d[0])%3,(u[1]+t*d[1])%3) for t in range(3)))) )
    return sorted(S)

def main():
    U=[(a,b) for a in range(3) for b in range(3)]; ui={u:i for i,u in enumerate(U)}
    det=lambda u,v:(u[0]*v[1]-u[1]*v[0])%3
    M=[[Z for _ in range(9)] for __ in range(9)]
    for i,u in enumerate(U):
      for j,v in enumerate(U):
        if i!=j:M[i][j]=wpow(det(u,v))
    # Hermitian and exact quadratic relation M^2+2M-8I=0.
    for i in range(9):
      for j in range(9):assert M[i][j]==conj(M[j][i])
    M2=mmul(M,M)
    for i in range(9):
      for j in range(9):
        z=add(M2[i][j],scale(2,M[i][j]))
        if i==j:z=add(z,(-8,0))
        assert z==Z
    # K=2 G_SIC = 2I-M. It has rank 3, eigenvalue 6 on its image.
    K=[[neg(M[i][j]) for j in range(9)] for i in range(9)]
    for i in range(9):K[i][i]=(2,0)
    K2=mmul(K,K)
    for i in range(9):
      for j in range(9):assert K2[i][j]==scale(6,K[i][j])
    lines=lines_ag23(U);assert len(lines)==12; L={frozenset(ui[x] for x in line) for line in lines}
    dh={};zero=[]
    for T in itertools.combinations(range(9),3):
        A=[[K[i][j] for j in T] for i in T];d=det3(A);dh[str(d)]=dh.get(str(d),0)+1
        if d==Z:zero.append(frozenset(T))
        else:assert d==(3,0)
    assert set(zero)==L and len(zero)==12 and dh=={'(0, 0)':12,'(3, 0)':72}
    # Exact equivalence to a standard Hesse SIC Gram matrix.
    raw=[]
    for e in range(3):raw.append((Z,ONE,neg(wpow(e))))
    for e in range(3):raw.append((neg(wpow(e)),Z,ONE))
    for e in range(3):raw.append((ONE,neg(wpow(e)),Z))
    Ks=[[ip(raw[i],raw[j]) for j in range(9)] for i in range(9)]
    perm=[0,2,1,4,3,5,8,7,6]; dex=[0,2,1,0,0,0,1,2,0]
    for i in range(9):
      for j in range(9):
        z=mul(conj(wpow(dex[i])),mul(Ks[perm[i]][perm[j]],wpow(dex[j])))
        assert z==K[i][j]
    out={'schema':'w33.pass7214.h27_fourier_hesse_sic.v1','status':'PASS',
      'H27_central_Fourier':{'trivial_sector':'J_9-I_9, spectrum 8^1+(-1)^8','nontrivial_sectors':2,
        'magnetic_block_identity':'M^2+2M-8I=0','each_magnetic_spectrum':'2^6+(-4)^3'},
      'Hesse_SIC':{'gram':'G3=I-M/2','rank':3,'spectrum':'3^3+0^6','unit_norm':True,'off_diagonal_modulus':'1/2',
        'dependent_triples':12,'dependent_triples_exactly':'12 affine lines of AG(2,3)','other_72_scaled_2G_determinant':3,
        'standard_Hesse_equivalence':{'permutation':[0,2,1,4,3,5,8,7,6],'cube_root_gauge_exponents':[0,2,1,0,0,0,1,2,0],'exact':True}},
      'Naimark_ETF':{'gram':'G6=I+M/4','vectors':9,'dimension':6,'frame_bound':'3/2','off_diagonal_modulus':'1/4','Welch_equality':True},
      'representation_reading':'The two nontrivial central characters give the two conjugate 9D magnetic sectors; each is three copies of a degree-3 Schroedinger irreducible.',
      'boundary':'Exact finite H27/Hesse frame theorem. The Hesse SIC is a known qutrit SIC object; the new repo bridge is its derivation from the E8/W33 matter-fibre determinant cocycle.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','dependent_triples':12,'SIC_rank':3,'ETF_rank':6}))
if __name__=='__main__':main()
