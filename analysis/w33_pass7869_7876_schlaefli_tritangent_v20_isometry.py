#!/usr/bin/env python3
"""Pass7869-7876: literal Schlaefli -> tritangent V20 intertwiner.

Construct the classical 27 lines on a smooth cubic surface in double-six notation
(a_i,b_i,c_ij) and the 45 tritangent planes.  Their 45x27 incidence matrix B is the
objectwise transport already implicit in Pass7184/7621.  This pass isolates the
one-line operator identity
    B^T B = 4 I + J - A_Schlaefli.
Therefore on the Schlaefli (-2)-eigenspace V20, B^T B=6I: B/sqrt(6) is an exact
W(E6)-equivariant isometry into the 45-coordinate tritangent module.  Mod 2, the
same integer matrix has rank 21 and its column-difference/even image has rank 20,
so one matrix simultaneously realizes the real Schlaefli V20 and binary tritangent
selector V20.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7869_7876_SCHLAEFLI_TRITANGENT_V20_ISOMETRY.json'

def rank_mod(A,p):
    M=np.asarray(A,dtype=int).copy()%p;m,n=M.shape;r=0
    for c in range(n):
        z=next((i for i in range(r,m) if M[i,c]),None)
        if z is None:continue
        M[[r,z]]=M[[z,r]];M[r]=(M[r]*pow(int(M[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and M[i,c]:M[i]=(M[i]-int(M[i,c])*M[r])%p
        r+=1
    return r

def matchings(items):
    items=tuple(items)
    if not items:
        yield ();return
    i=items[0]
    for k in range(1,len(items)):
        j=items[k];rest=items[1:k]+items[k+1:]
        for tail in matchings(rest):yield tuple(sorted(((min(i,j),max(i,j)),)+tail))

def main():
    a=[('a',i) for i in range(6)];b=[('b',i) for i in range(6)]
    c=[('c',i,j) for i in range(6) for j in range(i+1,6)]
    lines=a+b+c;idx={x:i for i,x in enumerate(lines)};assert len(lines)==27
    planes=[]
    for i in range(6):
      for j in range(6):
        if i!=j:planes.append((('a',i),('b',j),('c',min(i,j),max(i,j))))
    pm=sorted(set(matchings(range(6))));assert len(pm)==15
    for m in pm:planes.append(tuple(('c',i,j) for i,j in m))
    assert len(planes)==45 and len(set(planes))==45
    B=np.zeros((45,27),dtype=np.int64)
    for r,t in enumerate(planes):
        for L in t:B[r,idx[L]]=1
    assert set(map(int,B.sum(0)))=={5} and set(map(int,B.sum(1)))=={3}

    Aint=B.T@B-5*np.eye(27,dtype=np.int64)
    As=np.ones((27,27),dtype=np.int64)-np.eye(27,dtype=np.int64)-Aint
    assert set(map(int,Aint.sum(1)))=={10} and set(map(int,As.sum(1)))=={16}
    la=set();mu=set()
    for i,j in itertools.combinations(range(27),2):
        q=int(As[i]@As[j]);(la if As[i,j] else mu).add(q)
    assert la=={10} and mu=={8}
    spec=Counter(round(float(x),8) for x in np.linalg.eigvalsh(As.astype(float)))
    assert spec==Counter({-2.0:20,4.0:6,16.0:1})

    I=np.eye(27,dtype=np.int64);J=np.ones((27,27),dtype=np.int64)
    assert np.array_equal(B.T@B,4*I+J-As)
    Y=B.astype(float)-np.ones((45,27))/9
    ys=Counter(round(float(x),8) for x in np.linalg.eigvalsh(Y.T@Y))
    assert ys==Counter({6.0:20,0.0:7})

    # Exact projector onto the -2 Schlaefli eigenspace:
    # E20=(4I+J-As)/6 after removing the 1 and 6 sectors via the identity above.
    # On any x with As x=-2x and Jx=0, ||Bx||^2=6||x||^2.
    assert np.linalg.matrix_rank(B.astype(float))==21
    assert rank_mod(B,2)==21
    Beven=(B[:,1:]+B[:,[0]])%2
    assert rank_mod(Beven,2)==20
    assert all(int(Beven[:,j].sum())%2==0 for j in range(Beven.shape[1]))

    out={
      'schema':'w33.pass7869_7876.schlaefli_tritangent_v20_isometry.v1','status':'PASS','passes':'7869-7876',
      'objects':{'cubic_lines':27,'tritangent_planes':45,'line_degree_in_planes':5,'plane_size':3},
      'Schlaefli':'SRG(27,16,10,8), spectrum 16^1+4^6+(-2)^20',
      'exact_operator_identity':'B^T B = 4 I + J - A_Schlaefli',
      'V20_isometry':'On V20={x: Jx=0, A_Schlaefli x=-2x}, B^T B=6I; hence B/sqrt(6) is an isometric W(E6)-equivariant embedding into R^45.',
      'centered_incidence_spectrum':'6^20 + 0^7','real_rank_B':21,'F2_rank_B':21,'F2_even_column_difference_rank':20,
      'binary_bridge':'The identical integer incidence matrix B generates the 20D even tritangent-selector image over F2 after taking column differences.',
      'theorem':'The local Schlaefli V20 and the 45-coordinate tritangent V20 are not merely isomorphic by dimension: the classical 45x27 cubic-surface incidence matrix is the explicit intertwiner, with exact scale sqrt(6) over R and the canonical even 20D image over F2.',
      'prior_art_boundary':'Pass7184 owns the binary V20 identification; Pass7621 owns the real centered 20D coefficient module. This pass isolates and verifies the literal classical incidence operator connecting them.',
      'claim_boundary':'Exact cubic-surface/W(E6) representation geometry only.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','identity':'B^T B=4I+J-A','V20_scale':'sqrt(6)','rank2_even':20}))
if __name__=='__main__':main()
