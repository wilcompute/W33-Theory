"""Pass 11700: no two-qutrit gate realises an odd triality -- the only triality on a D4 x D4 dual pair is the central Z3 of
SU(9)/Z3 inside E8.

Setting: Pass 11687's dual pair D4_A x D4_B (centralisers of the two qutrits' Pauli groups) and the three cosets of
E8/(D4 + D4), (8v,8v) + (8s,8s) + (8c,8c), 64 roots each.  A gate U in U(9) normalising the Pauli group acts on e8 only
after a determinant-one lift U det(U)^(-1/9) zeta9^k; the three lifts differ by the scalar zeta9, whose E8 image is the
Z3-grading element g (it acts by omega on Lambda^3).  g cycles the three cosets (Pass 11687).

FOUND (every generator of the stabiliser of the tensor factorisation, all three lifts):
  * qutrit-1 Cliffords F(x)I, S(x)I, Z(x)I, X(x)I; qutrit-2 Cliffords I(x)F, I(x)S; SWAP; complex conjugation K:
    each lift permutes the three cosets CYCLICALLY, and for every gate exactly one lift fixes all three cosets.
  * Hence the coset permutation of a gate is exactly its central-lift ambiguity: modulo the centre, no element of the
    extended (anti-unitary) local Clifford group, nor SWAP, acts on the cosets at all, and no lift of any of them is a
    transposition (8s <-> 8c with 8v fixed).
Reading: the classical E8 contains odd trialities of D4 x D4 (the normaliser in W(E8) maps onto S3), but none is realised
by a two-qutrit gate; the cyclic triality that is realised is the centre of SU(9)/Z3, i.e. the operator/three-fermion/
three-hole grading.  In light-cone language (so(8) transverse algebra, 8s/8c = the two ten-dimensional chiralities) the
gates never exchange the two spinor chiralities.  Contrast Pass 11689: the 27/27bar chirality IS flipped by Pauli
inversion and by antiunitarity separately.  Scope: a statement about gate actions on root cosets; no spacetime is derived.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11687_11691_two_qutrit_e8_dictionary as Dct  # noqa: E402

OUT = ROOT / "data" / "w33_pass11700_triality_is_central.json"
W3 = np.exp(2j * np.pi / 3)


def main():
    d = Dct.E8Data()
    Rn = d.R / np.linalg.norm(d.R, axis=0)
    Hp = [i for i in range(240) if d.deg[i][0] == 0 and d.deg[i][1] == 0]
    Hq = [i for i in range(240) if d.deg[i][2] == 0 and d.deg[i][3] == 0]
    mixed = [i for i in range(240) if i not in Hp and i not in Hq]
    B = []
    for i in Hp + Hq:
        if np.linalg.matrix_rank(np.array(B + [d.X[i]])) > len(B):
            B.append(d.X[i])
    B = np.array(B).T

    def key(x):
        c = np.linalg.solve(B, x)
        return tuple(int(t) for t in np.round((c - np.floor(c + 1e-9)) * 2) % 2)
    cos = {}
    for i in mixed:
        cos.setdefault(key(d.X[i]), []).append(i)
    cid = {i: k for k, (_, L) in enumerate(sorted(cos.items())) for i in L}

    def perm(U, anti):
        img = d.Ad(U, anti) @ Rn
        G = Rn.conj().T @ img
        res = np.linalg.norm(img, axis=0)[None, :] ** 2 - np.abs(G) ** 2
        assert np.all(res.min(0) < 1e-8)
        return res.argmin(0)

    F = np.array([[W3 ** (a * b) for b in range(3)] for a in range(3)]) / np.sqrt(3)
    S = np.diag([1, 1, W3])
    Z = np.diag([1, W3, W3 * W3])
    X = np.roll(np.eye(3), 1, 0)
    I3 = np.eye(3)
    gens = {"F(x)I": (np.kron(F, I3), False), "S(x)I": (np.kron(S, I3), False), "Z(x)I": (np.kron(Z, I3), False),
            "X(x)I": (np.kron(X, I3), False), "I(x)F": (np.kron(I3, F), False), "I(x)S": (np.kron(I3, S), False),
            "SWAP": (np.eye(9)[[3 * (k % 3) + k // 3 for k in range(9)]], False), "K": (np.eye(9), True)}
    out = {}
    for name, (U, anti) in gens.items():
        b = complex(np.linalg.det(U)) ** (-1 / 9)
        rows = []
        for k in range(3):
            p = perm(U * b * np.exp(2j * np.pi * k / 9), anti)
            cm = Counter((cid[i], cid[p[i]]) for i in mixed)
            mp = {a: c for (a, c) in cm}
            assert len(cm) == 3 and len(set(mp.values())) == 3
            fixed = sum(a == c for a, c in mp.items())
            rows.append(dict(lift=k, coset_map=[mp[a] for a in range(3)],
                             kind="identity" if fixed == 3 else ("cyclic" if fixed == 0 else "transposition")))
        out[name] = rows
    res = dict(pass_id=11700, coset_sizes=sorted(len(L) for L in cos.values()), gates=out,
               any_transposition=any(r["kind"] == "transposition" for v in out.values() for r in v),
               every_gate_has_one_identity_lift=all(sum(r["kind"] == "identity" for r in v) == 1 for v in out.values()))
    print(json.dumps(res, indent=1))
    json.dump(res, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
