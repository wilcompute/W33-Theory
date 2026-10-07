"""Pass 11647: the union law is a theorem -- reversible frames are the union over SEMISIMPLE reversers.

Setting as in Passes 11537/11644: U = W(a) V_M T1; a solution (Q, k) of (S) gives A = Q J, anti-symplectic, with
A M A^-1 = s^k M^-1, A z1 = -z1; K0 = ker(M - I) cap z1^perp; N_A = (I - A^-1) K0; Pass 11644: A preserves K0.

LEMMA A (semisimple part, every n).  Let A be a k = 0 solution, of order 3^a m (3 not dividing m), and A = A_s A_u its
  Jordan decomposition.  Then A_s = A^N for an ODD N with N = 0 mod 3^a and N = 1 mod m.  So A_s M A_s^-1 = M^-1 and
  A_s z1 = -z1: A_s is again a k = 0 solution (Q_s = A_s J is symplectic and fixes z1).  Its order is prime to 3, so it
  splits (Pass 11644, Theorem 3): frames(A_s) = N_{A_s}^perp.  And I - A^-N = (I - A^-1)(I + A^-1 + ... + A^-(N-1)) with
  K0 A-invariant, so N_{A_s} is contained in N_A.  Hence N_A^perp is contained in the reversible frames.
LEMMA B (k != 0 in the eigenvector cells, every n).  A s A^-1 = s^-1 for EVERY solution (A z1 = -z1, A anti-symplectic,
  s the transvection with centre z1).  If M z1 = +-z1, s commutes with M, and conjugating three times gives
  A^3 M A^-3 = s^(3k) M^-1 = M^-1: A^3 is a k = 0 solution with N_{A^3} contained in N_A; apply Lemma A to it.
THEOREM (union law).  For every n and every class M such that every k != 0 solution of (S) lies in an eigenvector cell
  (M z1 = +-z1) or is dominated by a split k = 0 solution:
      reversible frames  =  union over the SEMISIMPLE k = 0 reversers A of ((I - A^-1) K0)^perp.
  ("Only if": Pass 11537.  "If": Lemmas A, B and Pass 11644 Theorems 1, 3.)  By Pass 11644's Theorem 2, a k != 0
  solution needs an isotropic M-cyclic span of z1; outside the eigenvector cells this happens only in the same-line
  cells, where the domination is checked here class by class.
CERTIFICATE: every class at n = 2 and every orbit of Pass 11373 at n = 3 within the enumeration cap, each solution
  checked: Lemma A's A^N is a solution, split, and dominated; Lemma B's A^3 in the eigenvector cells; and the remaining
  k != 0 solutions dominated by an explicit split solution.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from fractions import Fraction
from math import gcd
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11350_linear_decider as L  # noqa: E402
import w33_pass11352_three_qutrit_geometry as GEO  # noqa: E402
import w33_pass11498_magic_axis_law_all_n as T  # noqa: E402
import w33_pass11644_union_law_splitting as S  # noqa: E402

OUT = ROOT / "data" / "w33_pass11647_union_law_closed.json"
R = L.R


def rank3(vs):
    return len(L.rref3(np.array(vs) % 3)[1]) if len(vs) else 0


def mat_order(A, I):
    cur = I.copy()
    for o in range(1, 2000):
        cur = (A @ cur) % 3
        if not ((cur - I) % 3).any():
            return o
    raise ValueError


def semisimple_power(A, I):
    o = mat_order(A, I)
    a, m = 0, o
    while m % 3 == 0:
        m //= 3
        a += 1
    th = 3 ** a
    N = next(N for N in range(1, 4 * o + 2, 2) if N % th == 0 and (N - 1) % m == 0)
    return np.linalg.matrix_power(A, N) % 3, N, a


def classify(D, M, cap):
    N2 = D.N2
    z = D.z1
    Om = D.wl.Om
    I = np.eye(N2, dtype=np.int64)
    M = np.asarray(M) % 3
    K = S.null((M - I) % 3)
    K0 = S.null(np.concatenate([(M - I) % 3, (z @ Om)[None, :] % 3]))

    def om(u, v):
        return int(u @ Om @ v) % 3
    w1 = next((w for w in K if om(w, z)), None)
    case = 1 if w1 is not None else 2
    w0 = None if case == 1 else L.solve_affine((I - M) % 3, z)[0]
    eig = not ((M @ z - z) % 3).any() or not ((M @ z + z) % 3).any()
    Minv = R._inv_mod3(M) % 3

    def NA(A):
        Ai = R._inv_mod3(A) % 3
        return [(w - Ai @ w) % 3 for w in K0]

    def is_solution_k0(A):
        Q = (A @ D.J) % 3
        return (D.is_symplectic(Q) and not ((Q @ z - z) % 3).any()
                and not ((A @ M @ R._inv_mod3(A) - Minv) % 3).any())

    def splits(A):
        x = w1 if case == 1 else (w0 + z) % 3
        Kt = np.array(list(K0) + [x]).T % 3
        cur = I.copy()
        for o in range(1, 2000):
            cur = (A @ cur) % 3
            if not ((cur @ Kt - Kt) % 3).any():
                return o % 3 != 0
        return False
    sols = []
    for k in range(3):
        ss = T.solutions(D, M, k, cap)
        if ss is None:
            return None
        sols += [(k, (Q @ D.J) % 3) for Q in ss]
    st = Counter()
    split_N = [NA(A) for k, A in sols if k == 0 and splits(A)]
    for k, A in sols:
        nA = NA(A)
        rA = rank3(nA)
        if k == 0:
            if splits(A):
                st["k=0 split (Pass 11644 Theorem 3)"] += 1
                continue
            As, N, a = semisimple_power(A, I)
            ok = is_solution_k0(As) and splits(As) and rank3(nA + NA(As)) == rA
            st["k=0 non-split: Lemma A (A^N semisimple solution, split, dominated) holds"] += ok
            st["k=0 non-split: Lemma A FAILS"] += not ok
        else:
            if eig:
                A3 = np.linalg.matrix_power(A, 3) % 3
                As, N, a = semisimple_power(A3, I)
                ok = (is_solution_k0(A3) and rank3(nA + NA(A3)) == rA and is_solution_k0(As) and splits(As)
                      and rank3(nA + NA(As)) == rA)
                st["k!=0, eigenvector cell: Lemma B (A^3 then semisimple part) holds"] += ok
                st["k!=0, eigenvector cell: Lemma B FAILS"] += not ok
            else:
                ok = any(rank3(nA + nB) == rA for nB in split_N)
                st["k!=0, other cell: dominated by an explicit split k=0 solution"] += ok
                st["k!=0, other cell: NOT dominated"] += not ok
    return st


def summarise(D, items, cap):
    tot, mass = Counter(), Counter()
    for M, w in items:
        st = classify(D, M, cap)
        cell = GEO.cell(np.asarray(M) % 3, D.z1, D.wl.Om)
        if st is None:
            mass["beyond cap"] += w
            continue
        tot.update(st)
        bad = any("FAILS" in k or "NOT" in k for k, v in st.items() if v)
        mass["union law PROVED (theorem + certificate)" if not bad else "NOT proved"] += w
        if any(k.startswith("k!=0, other") for k in st):
            tot[f"classes needing the explicit k!=0 check ({cell})"] += 1
    return tot, mass


def _job(args):
    n, items, cap = args
    D = L.Decider(n)
    return summarise(D, items, cap)


def run(n, nproc=6):
    from multiprocessing import Pool
    if n == 2:
        import w33_pass11330_orbit_census as O
        D = L.Decider(2)
        items = [(np.asarray(M) % 3, 1) for M in O.all_symplectic(D.wl)[0]]
        cap = 3 ** 8
    else:
        import w33_pass11373_three_qutrit_exact_fraction as X
        items = [(np.asarray(M) % 3, int(s)) for M, s in X.read_orbits(3)]
        cap = 3 ** 9
    chunks = [items[i::60] for i in range(60)]
    tot, mass = Counter(), Counter()
    with Pool(nproc) as pool:
        for t, m in pool.imap_unordered(_job, [(n, c, cap) for c in chunks]):
            tot.update(t)
            mass.update(m)
    allm = sum(mass.values())
    return dict(counts=dict(tot), mass={k: str(Fraction(v, allm)) for k, v in mass.items()},
                mass_float={k: v / allm for k, v in mass.items()})


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    out = run(n)
    print(out, flush=True)
    res = json.load(open(OUT)) if OUT.exists() else dict(pass_id=11647)
    res[f"n{n}"] = out
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
