"""Pass 11692: the unbroken E8 symmetry of an elementary two-qutrit tick -- magic is needed for a Standard-Model-shaped
centraliser.

A one-gate tick U = W(a) V_M T1 (Pass 11350) is an element of U(9); after fixing det = 1 it lies in SU(9), whose image
SU(9)/Z3 sits in E8 (Pass 11681).  The Z9 / Z3 ambiguity of the det-normalisation gives THREE E8 lifts, all scanned.
The centraliser of the E8 element in e8 (its unbroken symmetry) is the Cartan of its torus plus the roots it fixes, and
with eigenvalues lambda_i of U these are exactly
        sl9 roots e_i - e_j  with lambda_i = lambda_j,      trivector roots +-(e_i + e_j + e_k)  with lambda_i lambda_j lambda_k = 1.
So the unbroken root system is read off the 9 eigenvalues; irreducible components are classified by (#roots, rank).

FOUND (random (M, a), uniform; each sample in its three lifts):
  * with the magic gate: about 69% of ticks break E8 to its Cartan; the most common non-trivial unbroken symmetry is
    A2 + A2 + A2 (trinification SU(3)^3, ~7%); an SM-shaped A2 + A1 (su(3) + su(2) + five u(1)) occurs in ~0.1%;
  * Clifford-only ticks (no T): A2 + A1 NEVER occurs in the sample (0 of 3 x N); Clifford ticks keep larger symmetries
    (A1 + A2^3, A2 + A5, ...).
Scope: an observation about centralisers of single E8 group elements, sampled; not a derivation of the Standard Model,
which would need a vacuum or dynamics selecting such a tick.
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11330_orbit_census as O  # noqa: E402
import w33_pass11350_linear_decider as L  # noqa: E402

OUT = ROOT / "data" / "w33_pass11692_tick_symmetry_in_e8.json"
NAMES = {(2, 1): "A1", (6, 2): "A2", (12, 3): "A3", (20, 4): "A4", (30, 5): "A5", (42, 6): "A6", (56, 7): "A7",
         (72, 8): "A8", (24, 4): "D4", (40, 5): "D5", (60, 6): "D6", (84, 7): "D7", (112, 8): "D8", (72, 6): "E6",
         (126, 7): "E7", (240, 8): "E8"}
ROOTS = []
for i in range(9):
    for j in range(9):
        if i != j:
            v = np.zeros(9)
            v[i], v[j] = 1, -1
            ROOTS.append(("A", (i, j), v))
for T in itertools.combinations(range(9), 3):
    v = np.zeros(9)
    v[list(T)] = 1
    v -= 1 / 3
    ROOTS.append(("L", T, v))
    ROOTS.append(("Ld", T, -v))


def unbroken_type(lam, tol=1e-7):
    keep = []
    for kind, idx, v in ROOTS:
        if kind == "A":
            val = lam[idx[0]] / lam[idx[1]]
        elif kind == "L":
            val = lam[idx[0]] * lam[idx[1]] * lam[idx[2]]
        else:
            val = 1 / (lam[idx[0]] * lam[idx[1]] * lam[idx[2]])
        if abs(val - 1) < tol:
            keep.append(v)
    if not keep:
        return ()
    R = np.array(keep)
    G = R @ R.T
    n = len(R)
    comp = -np.ones(n, int)
    c = 0
    for s in range(n):
        if comp[s] < 0:
            st = [s]
            comp[s] = c
            while st:
                a = st.pop()
                for b in range(n):
                    if comp[b] < 0 and abs(G[a, b]) > 1e-9:
                        comp[b] = c
                        st.append(b)
            c += 1
    return tuple(sorted(NAMES.get((int((comp == k).sum()), int(np.linalg.matrix_rank(R[comp == k]))), "?")
                        for k in range(c)))


def scan(D, Ms, N, with_T, seed):
    rng = np.random.default_rng(seed)
    z9 = np.exp(2j * np.pi / 9)
    per = [Counter(), Counter(), Counter()]
    for _ in range(N):
        M = Ms[rng.integers(len(Ms))]
        a = D.wl.labels[rng.integers(81)].astype(np.int64)
        U = D.wl.W[D.wl.index(a)] @ D.weil(M) @ (D.T1 if with_T else np.eye(9))
        lam = np.linalg.eigvals(U)
        base = np.prod(lam) ** (-1 / 9)
        for k in range(3):
            per[k][unbroken_type(lam * base * z9 ** k)] += 1
    return per


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    D = L.Decider(2)
    Ms = np.array(O.all_symplectic(D.wl)[0]) % 3
    res = dict(pass_id=11692, samples_per_case=N)
    # calibration: T (x) I alone
    z9 = np.exp(2j * np.pi / 9)
    res["calibration_T_on_qutrit_1"] = list(unbroken_type(np.kron(np.array([1, z9, z9 ** -1]), np.ones(3))))
    res["calibration_Z_on_qutrit_1"] = list(unbroken_type(np.kron(np.exp(2j * np.pi / 3) ** np.arange(3), np.ones(3))))
    for with_T in (True, False):
        per = scan(D, Ms, N, with_T, 11692 if with_T else 11693)
        key = "with_T" if with_T else "clifford_only"
        res[key] = []
        for k in range(3):
            tot = sum(per[k].values())
            res[key].append(dict(lift=k, cartan_only=per[k][()] / tot,
                                 trinification_A2x3=per[k][("A2", "A2", "A2")] / tot,
                                 standard_model_shaped_A1_A2=sum(c for t, c in per[k].items() if list(t) == ["A1", "A2"]) / tot,
                                 standard_model_shaped_count=sum(c for t, c in per[k].items() if list(t) == ["A1", "A2"]),
                                 top=[(list(t), round(c / tot, 4)) for t, c in per[k].most_common(8)]))
        print(key, res[key], flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
