"""Driver for Passes 10377-10388 -- verifies (Wx,x) == |x|^2/2 mod 2 at ranks 8 and 24.

Every driver here asserts the isometry convention BEFORE using the matrix. The first
rank-24 run of this computation reported the theorem false because _co0_M3.txt is stored
in the row convention (W G W^T = G) while everything else in the repo uses the column
convention (W^T G W = G). The guard turns that into a one-line fix instead of a false
refutation.

    py -3 analysis/w33_pass10377_10388_refinement_driver.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7217_ovoid_pullback_to_e8 import CARTAN  # noqa: E402
from w33_pass7333_leech_d4_form import invariant_gram  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def orient(W, G):
    """Return W in the COLUMN convention W^T G W = G, transposing if stored as a row action."""
    if np.array_equal(W.T @ G @ W, G):
        return W, "column (as stored)"
    if np.array_equal(W @ G @ W.T, G):
        return W.T, "row (TRANSPOSED to column)"
    raise SystemExit("matrix is not an isometry of G in either convention -- stop")


def check(name, G, W, trials, seed=0):
    r = G.shape[0]
    I = np.eye(r, dtype=np.int64)
    W, conv = orient(W, G)
    assert np.array_equal(W.T @ G @ W, G), "isometry guard"
    assert not (I + W + W @ W).any(), "I + W + W^2 = 0 guard"
    rng = np.random.default_rng(seed)

    pol = True
    for _ in range(400):
        x = rng.integers(-3, 4, r)
        y = rng.integers(-3, 4, r)
        lhs = (int((W @ (x + y)) @ G @ (x + y)) - int((W @ x) @ G @ x)
               - int((W @ y) @ G @ y)) % 2
        if lhs != int(x @ G @ y) % 2:
            pol = False

    B = [int((W @ e) @ G @ e) % 2 for e in I]
    Q = [int(e @ G @ e) // 2 % 2 for e in I]
    diff = [i for i in range(r) if B[i] != Q[i]]

    bad = 0
    for _ in range(trials):
        x = rng.integers(0, 2, r)
        if int((W @ x) @ G @ x) % 2 != int(x @ G @ x) // 2 % 2:
            bad += 1

    print(f"  {name}  (rank {r})")
    print(f"    convention                         {conv}")
    print(f"    polarisations agree                {pol}")
    print(f"    basis vectors where B != q         {diff if diff else 'NONE'}")
    print(f"    random classes tested / failing    {trials} / {bad}")
    print(f"    => B == q identically              {pol and not diff and bad == 0}\n")
    return pol and not diff and bad == 0


def hermitian_points(n, q):
    """Isotropic points of H(2n-1, q^2)."""
    return (q ** (2 * n - 1) + 1) * (q ** (2 * n) - 1) // (q * q - 1)


def main() -> int:
    print("=" * 78)
    print("Passes 10377-10388 driver -- (Wx,x) == |x|^2/2 mod 2")
    print("=" * 78 + "\n")

    G8 = np.array(CARTAN, dtype=np.int64)
    I8 = np.eye(8, dtype=np.int64)
    cox = I8.copy()
    for i in range(8):
        s = I8.copy().astype(np.int64)
        s[i, :] = s[i, :] - G8[i, :]
        cox = cox @ s
    ok8 = check("E8   ", G8, np.linalg.matrix_power(cox, 10), 4000)

    A = np.loadtxt(ROOT / "analysis" / "_co0_G.txt", dtype=np.int64)
    GL, dim = invariant_gram([A[:24], A[24:]], 24)
    if GL is None:
        raise SystemExit("no invariant form recovered")
    if GL[0, 0] < 0:
        GL = -GL
    assert dim == 1 and round(np.linalg.det(GL.astype(float))) == 1
    assert not (GL.diagonal() % 2).any() and GL.diagonal().min() == 4
    WL = np.loadtxt(ROOT / "analysis" / "_co0_M3.txt", dtype=np.int64)
    ok24 = check("Leech", GL, WL, 50000)

    print("  count identity that the theorem had to survive at rank 24:")
    h = hermitian_points(6, 2)
    print(f"    |H(11,4)| = (2^11+1)(2^12-1)/3 = {h}")
    print(f"    Leech/2Leech q-singular classes = 8390655")
    print(f"    3 * {h} == 8390655 : {3 * h == 8390655}")
    print(f"\n  BOTH RANKS CONFIRM THE THEOREM : {ok8 and ok24}")
    return 0 if (ok8 and ok24) else 1


if __name__ == "__main__":
    raise SystemExit(main())
