#!/usr/bin/env python3
"""Passes 5744--5751: W33 symplectic overlay on the known ternary quadratic code.

Prior art is part of the theorem boundary, not a footnote:
- B. G. Rodrigues (Discrete Math. 308 (2008), 1941--1950) already gives the
  self-orthogonal [40,10,18]_3 design code and its [40,30,4]_3 dual with 260
  weight-4 words.
- K. Kaipa and P. Pradhan (arXiv:2405.12011, 2024) explicitly study the ternary
  quadratic Veronese 3-fold / second-order projective Reed--Muller code on PG(3,3).

This verifier checks the repository-specific coordinate bridge and machine-layer synthesis:
5744  W33 non-collinearity rowspace equals the quadratic Veronese code.
5745  C=V B V^T with a 10-sparse involutory symmetric core B.
5746  C^2=0 mod 3; the standard CSS consequence is [[40,20,4]]_3.
5747  The 130 minimum projective dual supports are exactly the PG(3,3) lines.
5748  Each coordinate has 13 three-query repair groups = 4 W33 + 9 ambient.
5749  The 130 line checks have rank 30 and span the full classical dual.
5750  Minimum logical rays have commutation graph J_3(4,2)=SRG(130,48,20,16).
5751  There are 234 distinct nondegenerate symplectic W33 overlays on the same code;
      each ambient projective line is W33-isotropic in exactly 72 overlays.

No measured-physics, gauge-field, spacetime, Standard-Model, coupling, or uniqueness
claim follows from these finite-geometry statements.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

Q = 3
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS5744_5751_QUADRATIC_CODE_OVERLAYS.json"
MONOMIALS = [(i, j) for i in range(4) for j in range(i, 4)]
J0 = np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]], dtype=np.int64) % Q
B0 = np.array([
    [0,0,0,0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,2,0,0,0],
    [0,0,0,0,0,1,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,1,0,0],
], dtype=np.int64)


def rank_mod(A, p=Q):
    A = np.asarray(A, dtype=np.int64).copy() % p
    m, n = A.shape
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if A[i, c] % p), None)
        if pivot is None:
            continue
        A[[r, pivot]] = A[[pivot, r]]
        A[r] = A[r] * pow(int(A[r, c]), -1, p) % p
        for i in range(m):
            if i != r and A[i, c] % p:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
        if r == m:
            break
    return r


def canon(v):
    v = tuple(int(x) % Q for x in v)
    if not any(v):
        return None
    i = next(i for i, x in enumerate(v) if x)
    inv = pow(v[i], -1, Q)
    return tuple(x * inv % Q for x in v)


def points():
    P = sorted({canon(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    assert len(P) == 40
    return P


def veronese(P):
    return np.array([[(p[i]*p[j]) % Q for i,j in MONOMIALS] for p in P], dtype=np.int64)


def alternating(coeff):
    a,b,c,d,e,f = coeff
    M = np.zeros((4,4), dtype=np.int64)
    for (i,j),x in {(0,1):a,(0,2):b,(0,3):c,(1,2):d,(1,3):e,(2,3):f}.items():
        M[i,j] = x % Q
        M[j,i] = (-x) % Q
    return M


def pairing(a, J, b):
    return int(np.asarray(a, dtype=np.int64) @ J @ np.asarray(b, dtype=np.int64)) % Q


def noncol(P, J=J0):
    return np.array([[pairing(a,J,b)**2 % Q for b in P] for a in P], dtype=np.int64)


def lines(P):
    idx = {p:i for i,p in enumerate(P)}
    L = set()
    for i,j in itertools.combinations(range(40),2):
        a,b = np.asarray(P[i]), np.asarray(P[j])
        s = set()
        for x,y in itertools.product(range(Q), repeat=2):
            if x == y == 0:
                continue
            s.add(idx[canon((x*a+y*b) % Q)])
        assert len(s) == 4
        L.add(tuple(sorted(s)))
    L = sorted(L)
    assert len(L) == 130
    return L


def isotropic(L, P, J=J0):
    return pairing(P[L[0]], J, P[L[1]]) == 0


def weight_enum(G):
    out = Counter()
    for a in itertools.product(range(Q), repeat=10):
        w = np.asarray(a, dtype=np.int64) @ G % Q
        out[int(np.count_nonzero(w))] += 1
    return dict(sorted(out.items()))


def srg(A):
    A = np.asarray(A, dtype=np.int64)
    d = A.sum(axis=1)
    assert len(set(map(int,d))) == 1
    la, mu = set(), set()
    for i in range(len(A)):
        for j in range(i+1,len(A)):
            c = int(A[i] @ A[j])
            (la if A[i,j] else mu).add(c)
    assert len(la) == len(mu) == 1
    return [len(A), int(d[0]), next(iter(la)), next(iter(mu))]


def symplectic_form_classes():
    S = set()
    for c in itertools.product(range(Q), repeat=6):
        if any(c) and rank_mod(alternating(c)) == 4:
            S.add(canon(c))
    S = sorted(S)
    assert len(S) == 234
    return S


def compute_certificate():
    P = points()
    V = veronese(P)       # 40x10
    G = V.T % Q           # 10x40
    C = noncol(P)

    # 5744: exact rowspace bridge; ordinary spectrum is prior art and independently replayed.
    assert rank_mod(G) == rank_mod(C) == rank_mod(np.vstack([G,C])) == 10
    W = weight_enum(G)
    assert W == {0:1,18:1560,24:21060,27:18800,30:16848,36:780}

    # 5745: sparse factorization.
    assert np.array_equal(V @ B0 @ V.T % Q, C)
    assert np.array_equal(B0, B0.T)
    assert np.array_equal(B0 @ B0 % Q, np.eye(10,dtype=np.int64))
    assert np.count_nonzero(V) == 216 and np.count_nonzero(B0) == 10
    assert np.count_nonzero(C) == 1080

    # 5746: square-zero/self-orthogonality.
    assert np.max(C @ C % Q) == 0
    assert np.max(G @ G.T % Q) == 0

    L = lines(P)
    H = np.zeros((130,40), dtype=np.int64)
    for r,l in enumerate(L): H[r,list(l)] = 1
    assert np.max(H @ V % Q) == 0
    assert rank_mod(H) == 30
    assert rank_mod(np.vstack([G,H])) == 30  # C <= C^perp, not a direct sum.
    assert set(map(int,H.sum(1))) == {4}
    assert set(map(int,H.sum(0))) == {13}

    # 5747: d(C^perp)=4; the 130 minimum projective supports are exactly projective lines.
    for r in (1,2,3):
        for S in itertools.combinations(range(40),r):
            assert rank_mod(G[:,S]) == r
    dep4 = {tuple(S) for S in itertools.combinations(range(40),4) if rank_mod(G[:,S]) < 4}
    assert dep4 == set(L)

    # 5748: 13 disjoint-by-helper repair groups per symbol; 4 are W33 native.
    iso0 = [isotropic(l,P,J0) for l in L]
    assert Counter(iso0) == Counter({True:40,False:90})
    profile=[]
    for p in range(40):
        through=[r for r,l in enumerate(L) if p in l]
        n=sum(iso0[r] for r in through)
        profile.append((len(through),n,len(through)-n))
    assert set(profile) == {(13,4,9)}

    # 5749: H spans the full classical dual and gives x_p=-sum(other 3) on every line.
    assert 40-rank_mod(H) == 10
    assert np.max(H @ G.T % Q) == 0

    # 5750: minimum logical line rays and their commutation graph.
    A = np.zeros((130,130), dtype=np.int64)
    for i,l in enumerate(L):
        s=set(l)
        for j in range(i+1,130):
            if s.intersection(L[j]): A[i,j]=A[j,i]=1
    assert srg(A) == [130,48,20,16]
    I=[i for i,x in enumerate(iso0) if x]
    O=[i for i,x in enumerate(iso0) if not x]
    AI=A[np.ix_(I,I)]
    AO=A[np.ix_(O,O)]
    X=A[np.ix_(I,O)]
    assert srg(AI) == [40,12,2,4]
    assert set(map(int,X.sum(1))) == {36}
    assert set(map(int,X.sum(0))) == {16}
    assert set(map(int,AO.sum(1))) == {32}
    assert np.array_equal(H @ H.T % Q, (np.eye(130,dtype=np.int64)+A) % Q)

    # 5751: 234 reconfigurable symplectic overlays, all preserving exactly the same code.
    forms=symplectic_form_classes()
    mats=set()
    line_mult=np.zeros(130,dtype=np.int64)
    for c in forms:
        J=alternating(c)
        CJ=noncol(P,J)
        assert rank_mod(CJ) == 10
        assert rank_mod(np.vstack([G,CJ])) == 10
        assert np.max(CJ @ CJ % Q) == 0
        mats.add(CJ.tobytes())
        iz=np.asarray([isotropic(l,P,J) for l in L],dtype=np.int64)
        assert int(iz.sum()) == 40
        line_mult += iz
    assert len(mats) == 234
    assert set(map(int,line_mult)) == {72}

    GL4=(81-1)*(81-3)*(81-9)*(81-27)
    PGL4=GL4//2
    Sp4=3**4*(3**2-1)*(3**4-1)
    PGSp4=Sp4
    assert PGL4 == 12130560 and PGSp4 == 51840 and PGL4//PGSp4 == 234

    terms=2*np.count_nonzero(V)+np.count_nonzero(B0)
    return {
      "schema":"w33.pass5744_5751.quadratic_code_overlays.v1",
      "prior_art":{
        "Rodrigues_2008":"known [40,10,18]_3 self-orthogonal design code; dual [40,30,4]_3 with 260 weight-4 words; full code/design automorphism L4(3):2_1",
        "Kaipa_Pradhan_2024":"known ternary quadratic Veronese 3-fold / second-order projective Reed-Muller code on PG(3,3), including higher weight spectra",
        "claim_tier":"code parameters and Veronese family are prior art; exact W33 coordinate bridge and finite machine-layer synthesis are new-to-repo unless separately sourced"
      },
      "pass_5744":{"parameters":[40,10,18],"weight_enumerator":{str(k):int(v) for k,v in W.items()},"codewords":59049,"bridge":"rowspace_F3(W33_noncollinearity)=quadratic_Veronesecode_C3(PG(3,3))"},
      "pass_5745":{"factorization":"C=V B V^T mod 3","V_nnz":216,"B_nnz":10,"B_squared_is_identity":True,"C_nnz":1080,"factorized_term_count":int(terms),"direct_over_factorized_ratio":float(1080/terms),"B":B0.tolist()},
      "pass_5746":{"C_squared_zero_mod3":True,"self_orthogonal":True,"standard_css_consequence":"[[40,20,4]]_3","warning":"standard consequence of known classical code; not coding-theory novelty"},
      "pass_5747":{"dual_distance":4,"minimum_projective_supports":130,"minimum_vector_words":260,"supports":"all projective lines of PG(3,3)"},
      "pass_5748":{"repair_groups_per_coordinate":13,"queries_per_repair":3,"w33_native_groups":4,"ambient_nonisotropic_groups":9,"law":"x_p=-sum_{q in L\\{p}} x_q mod 3"},
      "pass_5749":{"H_shape":[130,40],"H_rank_F3":30,"row_weight":4,"column_weight":13,"kernel_dimension":10,"rowspace_is_full_dual":True,"containment":"C subset C^perp"},
      "pass_5750":{"logical_line_graph":"J_3(4,2)","srg":[130,48,20,16],"w33_isotropic_induced_srg":[40,12,2,4],"isotropic_lines":40,"nonisotropic_lines":90,"cross_degrees":[36,16],"nonisotropic_induced_degree":32},
      "pass_5751":{"PGL4_order":PGL4,"PGSp4_order":PGSp4,"symplectic_overlays":234,"distinct_overlay_matrices":234,"all_overlays_same_code":True,"native_lines_per_overlay":40,"each_line_native_in_overlays":72,"architecture":"one ambient 40-coordinate quadratic code supports 234 selectable W33 symplectic routing overlays without changing code space","boundary":"finite reconfiguration statement only"}
    }


def main():
    R=compute_certificate()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(R,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS_5744_5751",json.dumps({"code":R["pass_5744"]["parameters"],"css":R["pass_5746"]["standard_css_consequence"],"dual_d":R["pass_5747"]["dual_distance"],"logical_graph":R["pass_5750"]["srg"],"overlays":R["pass_5751"]["symplectic_overlays"]},sort_keys=True))

if __name__ == "__main__": main()
