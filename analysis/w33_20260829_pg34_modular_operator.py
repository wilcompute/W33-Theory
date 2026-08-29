#!/usr/bin/env python3
"""Modular anatomy of the completed PG(3,4) polarity operator H.

The integral theorem gives H^2=16I+5J, H1=21*1 and spectrum
21^1,4^45,(-4)^39.  This audit resolves the exceptional characteristics.
The determinant -21*4^84 shows that only p=2,3,7 can be singular.

p=3,7: only the all-ones direction dies; the 84-dimensional augmentation
hyperplane remains semisimple and invertible.
p=2: rank(H)=17, H^2=J, and on the augmentation hyperplane H is square-zero
of rank 16.  Its 40-coordinate puncture is exactly the rank-16 W33 adjacency
code, while the 45 absolute rows restrict to the rank-15 sentinel subcode.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

from w33_20260829_pg34_polarity_sentinel import geometry, trade_incidence, mm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_PG34_MODULAR_OPERATOR.json'


def rank_mod(M,p):
    A=[[x%p for x in row] for row in M]
    m=len(A); n=len(A[0]); r=0
    for c in range(n):
        pivot=next((i for i in range(r,m) if A[i][c]),None)
        if pivot is None: continue
        A[r],A[pivot]=A[pivot],A[r]
        z=pow(A[r][c],-1,p)
        A[r]=[(z*x)%p for x in A[r]]
        for i in range(m):
            if i==r or not A[i][c]: continue
            z=A[i][c]
            A[i]=[(A[i][j]-z*A[r][j])%p for j in range(n)]
        r+=1
        if r==m: break
    return r


def sub_scalar(H,a,p):
    return [[(H[i][j]-(a if i==j else 0))%p for j in range(len(H))]
            for i in range(len(H))]


def main():
    N,A=geometry(); B,G=trade_incidence(N)
    H=[]
    for i in range(40): H.append(A[i]+B[i])
    for j in range(45):
        H.append([B[i][j] for i in range(40)] +
                 [G[j][k]+(1 if j==k else 0) for k in range(45)])
    assert len(H)==85 and all(len(r)==85 for r in H)
    H2=mm(H,H)
    assert all(H2[i][j]==(21 if i==j else 5) for i in range(85) for j in range(85))
    assert {sum(r) for r in H}=={21}
    assert sum(H[i][i] for i in range(85))==45

    ranks={p:rank_mod(H,p) for p in (2,3,5,7,11,13)}
    assert ranks=={2:17,3:84,5:85,7:84,11:85,13:85}

    # Characteristic 2: H^2=J and H fixes 1.  Since 85 is odd,
    # V=<1> direct-sum Aug, and H|Aug is square-zero.  A basis of Aug is
    # e_i+e_84; its image consists of column differences H_i+H_84.
    aug_images=[]
    for i in range(84):
        aug_images.append([(H[r][i]+H[r][84])%2 for r in range(85)])
    assert rank_mod(list(map(list,zip(*aug_images))),2)==16
    assert rank_mod(H,2)==17

    # The punctured binary plane code is exactly the W33 adjacency code; the
    # 45 absolute-plane rows give exactly the sentinel subcode.
    assert rank_mod(A,2)==16
    assert rank_mod(B,2)==15
    puncture40=[row[:40] for row in H]
    absolute40=[row[:40] for row in H[40:]]
    assert rank_mod(puncture40,2)==16
    assert rank_mod(absolute40,2)==15

    # Characteristics 3 and 7: H1=0, while on Aug, H^2=16I.  The exact
    # eigenspace dimensions retain the integral +4/-4 multiplicities.
    assert rank_mod(sub_scalar(H,1,3),3)==40      # nullity 45
    assert rank_mod(sub_scalar(H,-1,3),3)==46     # nullity 39
    assert rank_mod(sub_scalar(H,4,7),7)==40      # nullity 45
    assert rank_mod(sub_scalar(H,-4,7),7)==46     # nullity 39

    block_ranks={}
    D=[[G[i][j]+(1 if i==j else 0) for j in range(45)] for i in range(45)]
    for p in (2,3,7):
        block_ranks[str(p)]={"A":rank_mod(A,p),"B":rank_mod(B,p),"GplusI":rank_mod(D,p)}
    assert block_ranks=={
        "2":{"A":16,"B":15,"GplusI":15},
        "3":{"A":39,"B":25,"GplusI":45},
        "7":{"A":40,"B":25,"GplusI":45},
    }

    out={
      "schema":"w33.20260829.pg34-modular-operator.v1","status":"PASS",
      "integral":{"identity":"H^2=16I+5J","spectrum":{"21":1,"4":45,"-4":39},
        "determinant":"-21*4^84","singularPrimes":[2,3,7]},
      "characteristic2":{"rank":17,"identity":"H^2=J","decomposition":"<1> direct-sum Aug(84)",
        "onOnes":"identity","augmentationJordan":"J2(0)^16 + J1(0)^52","augmentationRank":16,
        "puncture40Rank":16,"puncture40":"W33 binary adjacency code",
        "absoluteRowsRestricted40Rank":15,"absoluteRowsRestricted40":"[40,15,8]_2 sentinel"},
      "characteristic3":{"rank":84,"kernel":"<1>","augmentation":"invertible semisimple",
        "eigenMultiplicities":{"1":45,"-1":39}},
      "characteristic7":{"rank":84,"kernel":"<1>","augmentation":"invertible semisimple",
        "eigenMultiplicities":{"4":45,"3 (-4)":39}},
      "genericOddCharacteristic":"H is invertible for every prime p not in {2,3,7}",
      "blockRanks":block_ranks,
      "boundary":"The exceptional primes follow exactly from the integral determinant. Their appearance is an arithmetic degeneration theorem; no additional physical identification is inferred."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","singularPrimes":[2,3,7],"ranks":{"2":17,"3":84,"7":84},"binaryAugmentation":"square-zero rank 16"}))


if __name__=='__main__': main()
