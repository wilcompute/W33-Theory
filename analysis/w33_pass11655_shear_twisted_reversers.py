"""Pass 11655: shear-twisted reversers are conjugacy problems -- the last case of the union law (Pass 11647).

A solution (Q, k) of (S) with k != 0 gives A with A M A^-1 = s^k M^-1, A z1 = -z1 (Pass 11644).
LEMMA C (every n).  If Y in Sp fixes z1, fixes K0 = ker(M - I) cap z1^perp pointwise, and Y M Y^-1 = s^k M, then for
  EVERY k-solution A, A' = A Y is a k = 0 solution with N_{A'} = N_A.
  Proof: A^-1 M^-1 A = s^k M (since A^-1 s A = s^-1), so A' M A'^-1 = A (s^k M)^-1 ... = M^-1 exactly when
  Y M Y^-1 = A^-1 M^-1 A = s^k M;  A' z1 = A z1 = -z1;  A'^-1 w = Y^-1 A^-1 w = A^-1 w for w in K0 (A preserves K0 and Y
  fixes it), so (I - A'^-1) K0 = (I - A^-1) K0.  Then Lemma A of Pass 11647 applies to A'.
  So the k != 0 solutions of a class are disposed of by ONE Y per (M, k), independent of the solution.
WHY THE SIMPLE ANSATZ FAILS.  Taking Y a symmetric shear along l = span(z1, M z1) requires k E11 in Im(phi - 1) for the
  induced action phi of M on Sym^2(l); this fails in every case (checked), which is why no short word in A, M and
  transvections dominates (Pass 11647).
CERTIFICATE (n = 3, the six same-line orbits with k != 0 solutions; n = 2 and n = 3 eigenvector cells for comparison):
  existence of Y by exhaustive search of the affine solution space, and A Y checked for every k != 0 solution.
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
import w33_pass11350_linear_decider as L  # noqa: E402
import w33_pass11352_three_qutrit_geometry as GEO  # noqa: E402
import w33_pass11498_magic_axis_law_all_n as T  # noqa: E402
import w33_pass11644_union_law_splitting as S  # noqa: E402

OUT = ROOT / "data" / "w33_pass11655_shear_twisted_reversers.json"
R = L.R


def Y_space(D, M, k, K0):
    N2 = D.N2
    z = D.z1
    I = np.eye(N2, dtype=np.int64)
    Ak = (D.s_pow[k] @ M) % 3
    Lm = (np.kron(I, M.T) - np.kron(Ak, I)) % 3                       # Y M - s^k M Y = 0, row-major vec(Y)
    rows, rhs = [Lm], [np.zeros(N2 * N2, np.int64)]
    for v in [z] + list(K0):
        Z = np.zeros((N2, N2 * N2), np.int64)
        for i in range(N2):
            Z[i, i * N2:(i + 1) * N2] = v
        rows.append(Z)
        rhs.append(np.asarray(v) % 3)
    return L.solve_affine(np.concatenate(rows) % 3, np.concatenate(rhs) % 3)


def find_Y(D, M, k, K0, cap=3 ** 12):
    sp_ = Y_space(D, M, k, K0)
    if sp_ is None:
        return None, "no linear Y"
    x0, Bs = sp_
    if 3 ** len(Bs) > cap:
        return None, f"space 3^{len(Bs)} beyond cap"
    for co in itertools.product(range(3), repeat=len(Bs)):
        y = x0.copy()
        for c, b in zip(co, Bs):
            y = (y + c * np.asarray(b)) % 3
        Y = y.reshape(D.N2, D.N2)
        if D.is_symplectic(Y):
            return Y, "found"
    return None, "no symplectic Y"


def run(n, cells_only_same_line=False):
    D = L.Decider(n)
    z = D.z1
    Om = D.wl.Om
    N2 = 2 * n
    I = np.eye(N2, dtype=np.int64)
    if n == 2:
        import w33_pass11330_orbit_census as O
        items = [(M, 1) for M in np.array(O.all_symplectic(D.wl)[0]) % 3]
    else:
        import w33_pass11373_three_qutrit_exact_fraction as X
        items = [(np.asarray(M) % 3, s) for M, s in X.read_orbits(3)]
    st = Counter()
    for M, w in items:
        M = np.asarray(M) % 3
        sols = {k: T.solutions(D, M, k, 3 ** 9 if n == 3 else 3 ** 8) for k in (1, 2)}
        if any(v is None for v in sols.values()) or not (sols[1] or sols[2]):
            continue
        cell = GEO.cell(M, z, Om)
        eig = cell.startswith("Mz1")
        if cells_only_same_line and eig:
            continue
        K0 = S.null(np.concatenate([(M - I) % 3, (z @ Om)[None, :] % 3]))
        Minv = R._inv_mod3(M) % 3

        def NA(A):
            Ai = R._inv_mod3(A) % 3
            return [(x - Ai @ x) % 3 for x in K0]
        for k in (1, 2):
            if not sols[k]:
                continue
            Y, why = find_Y(D, M, k, K0)
            st[f"{cell} | (M,k) pairs | Y: {why}"] += 1
            if Y is None:
                continue
            for Q in sols[k]:
                A = (Q @ D.J) % 3
                Ap = (A @ Y) % 3
                Qp = (Ap @ D.J) % 3
                ok = (D.is_symplectic(Qp) and not ((Qp @ z - z) % 3).any()
                      and not ((Ap @ M @ R._inv_mod3(Ap) - Minv) % 3).any()
                      and all(not ((a - b) % 3).any() for a, b in zip(NA(Ap), NA(A))))
                st[f"{cell} | k!=0 solutions: A Y is a k=0 solution with N(AY) = N(A): {ok}"] += 1
    return dict(st)


def main():
    res = json.load(open(OUT)) if OUT.exists() else dict(pass_id=11655)
    for n in (2, 3):
        res[f"n{n}"] = run(n)
        print(n, res[f"n{n}"], flush=True)
        json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
