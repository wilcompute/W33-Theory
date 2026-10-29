#!/usr/bin/env python3
"""Finite 15x15 point-plane polarity transform, symplectic W(3,2) and eigenspaces.

Classical finite polar design; new-to-project comparison with the exact
Klein/Hamming two-ruling stabilizer-frame intertwiner. No SU5 embedding
or physical Lorentzian spacetime is inferred from dimensions 10 and 5.
"""
import json
from pathlib import Path
import sys


def pairing(x,y):
    return (((x>>0)&1)*((y>>1)&1) + ((x>>1)&1)*((y>>0)&1)
          + ((x>>2)&1)*((y>>3)&1) + ((x>>3)&1)*((y>>2)&1))%2


def matrix():
    pts=range(1,16)
    M=[[1-int(pairing(p,q)) for q in pts] for p in pts]
    assert all(M[i][j]==M[j][i] for i in range(15) for j in range(15))
    assert all(M[i][i]==1 and sum(M[i])==7 for i in range(15))
    assert all(sum(M[i][k]*M[j][k] for k in range(15))==(7 if i==j else 3)
               for i in range(15) for j in range(15))
    B=[[3*M[i][j]-1 for j in range(15)] for i in range(15)]
    assert all(sum(B[i][k]*B[k][j] for k in range(15))==(36 if i==j else 0)
               for i in range(15) for j in range(15))
    return M,B


def certificate():
    M,B=matrix()
    # Point graph of W(3,2): A=M-I, degree6; adjacent pair shares1
    # common neighbor, nonadjacent pair shares3.
    A=[[M[i][j]-int(i==j) for j in range(15)] for i in range(15)]
    assert all(sum(row)==6 for row in A)
    assert all(sum(A[i][k]*A[k][j] for k in range(15)) ==
        (6 if i==j else (1 if A[i][j] else 3))
        for i in range(15) for j in range(15))
    lines=[(a,b,a^b) for a in range(1,16) for b in range(a+1,16)
           if a^b>b and pairing(a,b)==0]
    assert len(lines)==15 and all(sum(p in L for L in lines)==3 for p in range(1,16))
    # A eigenvalues: 6(1),1(9),-3(5); T eigen: +1(10),-1(5).
    # Direct integer trace determines eigenspace sizes because T^2=I.
    assert sum(B[i][i] for i in range(15))==30
    assert sum(B[i][j] for j in range(15) for i in range(15))==90
    return {
        'status':'EXACT_SYMPLECTIC_POLARITY_ORTHOGONAL_INVOLUTION',
        'geometry':'W(3,2) doily (15 points, 15 lines, 3 points/line)',
        'point_collinearity_srg':[15,6,1,3],
        'adjacency_eigenvalues':{'6':1,'1':9,'-3':5},
        'M':'15x15 symmetric symplectic point-plane incidence, M^2=4I+3J',
        'M_matrix':M,
        'B_equal_6T':B,
        'T_formula':'(3M-J)/6',
        'T_symmetry':'T=T^T; T^2=I; T1=1',
        'T_eigenspaces':{'+1':10,'-1':5},
        'T_trace':5,
        'T_integer_exact':True,
        'relationship_to_previous':'A symplectic polarity identifies alpha/beta generator labels, making the prior two-ruling orthogonal frame transform a symmetric involution.',
        'physical_scope':'The 10+5 dimensions are Sp4(2) symmetry sectors; no SU5 or E6 representation equivalence, causality, helicity or TOE established.'
    }


if __name__=='__main__':
    out=json.dumps(certificate(),indent=2)+'\n'
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(out,encoding='utf8')
    else:print(out,end='')
