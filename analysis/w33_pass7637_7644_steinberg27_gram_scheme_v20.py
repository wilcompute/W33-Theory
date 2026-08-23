#!/usr/bin/env python3
"""Pass7637-7644: the local Steinberg image is the Schlaefli V20.

Restrict the global 1120-A2 -> W33 H1 intertwiner T to the valency-81 suborbit
of a base-leaf A2.  The 81 columns collapse to 27 distinct vectors, each three
times.  Their Gram matrix has exactly three off-diagonal levels; those levels
are 9K3, the Schlaefli graph, and H27.  They form a commutative 3-class
association scheme, and the Gram matrix kills exactly the 1+6 part of the
27-point Schlaefli permutation module, leaving the 20-dimensional constituent.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass7509_7516_steinberg_global_intertwiner import build_T
OUT=ROOT/'data/PART_W33_PASS7637_7644_STEINBERG27_GRAM_SCHEME_V20.json'

def const_on_relation(M,R):
    vals=[int(M[i,j]) for i in range(len(R)) for j in range(len(R)) if R[i,j]]
    return len(set(vals))==1, (vals[0] if vals else None)

def main():
    R,A2,J,base,bl,AO,lab,edges,L,P,T,maps=build_T();anchor=bl[0]
    S=[int(x) for x in np.flatnonzero(lab[anchor]==4)];assert len(S)==81
    TS=T[:,S];assert np.linalg.matrix_rank(TS.astype(float),tol=1e-7)==20
    D=defaultdict(list)
    for i,a in enumerate(S):D[tuple(int(x) for x in T[:,a])].append(i)
    assert len(D)==27 and Counter(map(len,D.values()))==Counter({3:27})
    V=np.asarray(list(D.keys()),dtype=np.int64).T;G=V.T@V
    assert Counter(map(int,np.diag(G)))==Counter({11520:27})
    off=Counter(int(G[i,j]) for i,j in itertools.combinations(range(27),2))
    assert off==Counter({-1440:216,2400:108,-3840:27})

    Atri=(G==-3840).astype(np.int64);AS=(G==-1440).astype(np.int64);AH=(G==2400).astype(np.int64)
    for A in (Atri,AS,AH):np.fill_diagonal(A,0)
    I=np.eye(27,dtype=np.int64)
    assert np.array_equal(I+Atri+AS+AH,np.ones((27,27),dtype=np.int64))
    assert set(map(int,Atri.sum(1)))=={2} and set(map(int,AS.sum(1)))=={16} and set(map(int,AH.sum(1)))=={8}
    assert np.array_equal(Atri@AS,AS@Atri) and np.array_equal(Atri@AH,AH@Atri) and np.array_equal(AS@AH,AH@AS)

    # Full association-scheme closure: every product has constant entries on each relation.
    rel=[I,Atri,AS,AH];intersection=[]
    for i,A in enumerate(rel):
        row=[]
        for j,B in enumerate(rel):
            M=A@B;coeff=[]
            for K in rel:
                ok,v=const_on_relation(M,K);assert ok;coeff.append(v)
            row.append(coeff)
        intersection.append(row)

    # Named relation checks.
    assert Counter(round(float(x),8) for x in np.linalg.eigvalsh(Atri.astype(float)))==Counter({-1.0:18,2.0:9})
    SS=AS@AS
    assert {int(SS[i,j]) for i,j in itertools.combinations(range(27),2) if AS[i,j]}=={10}
    assert {int(SS[i,j]) for i,j in itertools.combinations(range(27),2) if not AS[i,j]}=={8}
    assert Counter(round(float(x),8) for x in np.linalg.eigvalsh(AS.astype(float)))==Counter({-2.0:20,4.0:6,16.0:1})
    assert Counter(round(float(x),8) for x in np.linalg.eigvalsh(AH.astype(float)))==Counter({2.0:12,-1.0:8,-4.0:6,8.0:1})

    # Simultaneous eigenmatrix, relation order I, 9K3, Schlaefli, H27.
    Pmat=np.array([
      [1,2,16,8],
      [1,-1,4,-4],
      [1,2,-2,-1],
      [1,-1,-2,2]],dtype=np.int64)
    mult=[1,6,8,12]
    # Verify orthogonality and match a generic joint diagonalization.
    kval=[1,2,16,8]
    assert np.array_equal(Pmat.T@np.diag(mult)@Pmat,27*np.diag(kval))
    C=3*Atri+5*AS+11*AH;w,U=np.linalg.eigh(C.astype(float));clusters=Counter(round(float(x),8) for x in w)
    assert clusters==Counter({-27.0:6,-15.0:8,9.0:12,174.0:1})

    # The Gram matrix is a Bose-Mesner element.  Its spectral support is exactly
    # the 8+12-dimensional part; it annihilates the trivial + Schlaefli-6 sector.
    assert np.array_equal(G,11520*I-3840*Atri-1440*AS+2400*AH)
    geval=[]
    for row in Pmat:
        geval.append(int(11520-3840*row[1]-1440*row[2]+2400*row[3]))
    assert geval==[0,0,4320,23040]
    assert Counter(round(float(x),8) for x in np.linalg.eigvalsh(G.astype(float)))==Counter({0.0:7,4320.0:8,23040.0:12})
    assert np.linalg.matrix_rank(G.astype(float),tol=1e-7)==20

    out={
      'schema':'w33.pass7637_7644.steinberg27_gram_scheme_v20.v1','status':'PASS','passes':'7637-7644',
      'source':'global integral A2-to-W33-H1 intertwiner T, restricted to the valency-81 A2 suborbit of one base-leaf A2',
      'restricted_81_rank':20,'distinct_vectors':27,'multiplicity_each':3,'vector_norm_squared':11520,
      'Gram_off_diagonal_counts':{'-3840':27,'-1440':216,'2400':108},
      'relations':{
        '-3840':{'graph':'9 K3','degree':2,'spectrum':'2^9 + (-1)^18'},
        '-1440':{'graph':'Schlaefli','srg':[27,16,10,8],'spectrum':'16^1 + 4^6 + (-2)^20'},
        '2400':{'graph':'H27','degree':8,'spectrum':'8^1 + 2^12 + (-1)^8 + (-4)^6'}},
      'association_scheme':{'rank':4,'valencies':[1,2,16,8],'multiplicities':mult,'first_eigenmatrix':Pmat.tolist(),'commutative':True,'intersection_numbers':intersection},
      'Gram_Bose_Mesner_formula':'G = 11520 I - 3840 A_(9K3) - 1440 A_Schlaefli + 2400 A_H27',
      'Gram_eigenvalues_by_scheme_idempotent':[0,0,4320,23040],
      'Gram_spectrum':{'0':7,'4320':8,'23040':12},
      'V20_statement':'The Gram kernel is exactly the 1+6 Schlaefli permutation sector; its image has dimension 8+12=20. Thus the local image of the global H1 intertwiner is the 20-dimensional Schlaefli constituent, not an 81-dimensional local module.',
      'negative_boundary':'The numerical appearance of 81 in the global H1/Steinberg sector must not be conflated with this 81-point local permutation suborbit: T has rank only 20 on the latter.',
      'novelty_boundary':'Pass7181/7186 supplied Schlaefli and H27 separately; Pass7629 supplied their common nine-triple complementarity. This pass identifies all three relations directly as the three Gram levels of the restricted global Steinberg intertwiner and proves the exact 20-dimensional spectral projection.',
      'claim_boundary':'Exact finite representation/association-scheme theorem; no physical multiplet identification follows.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','rank':20,'scheme_mult':mult,'Gram_eigs':geval}))
if __name__=='__main__':main()
