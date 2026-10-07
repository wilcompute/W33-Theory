"""Pass 11658: the CP sign of the Hesse sector at one and two qutrits, and why the reflection tower stops at two.

TIME REVERSAL on the Hesse space is complex conjugation u -> conj(u) (B is real), composed with the Clifford action.
A CP-odd Hesse invariant is a G-invariant polynomial of bidegree (k, k) in (u, conj u) that changes sign under
u -> conj(u); in the qutrit state psi it has degree 3k.  Dimensions by Reynolds rank over the reflection group:
  * n = 1 (G6, calibration): even dims 1, 1, 2, 3, 3, 4, 5, 6 (the ring R[rho, p3, p4]); the first CP-odd invariant is at
    k = 6 -- Codex's W of Passes 11600/11614 (= -108^3 times the MUB Vandermonde, Pass 11641; psi-degree 18).
  * n = 2 (G33): even dims 1, 1, 2, 4, 6, 10, 16, 27 and CP-ODD dims 0, 0, 0, 0, 0, 2, 5, 10 for k = 1..8 (even + odd =
    the exact Molien total 1, 1, 2, 4, 6, 12, 21, 37; k = 9, 10 are lower bounds).  The first CP-odd Hesse invariants of two
    qutrits are at k = 6 (two of them, psi-degree 18), the same bidegree as Codex's W at one qutrit; the two-qutrit
    lowest arrow (degree 6, Pass 11492) is invisible to the Hesse sector.
THE TOWER STOPS AT n = 2.  The local parity sigma_P (a tensor factorisation) acts on the even Weil representation of
W_1 (x) W_(n-1) as -1 exactly on odd_1 (x) odd_(n-1), of dimension (3^(n-1) - 1)/2: 1 at n = 2 (a reflection: G33),
4 at n = 3 (checked: parity of qutrit 3 and SWAP(1,2) have a 4-dim -1 eigenspace on the 14-dim space).  So two qutrits is
the unique size at which tensor factorisations act as reflections of the Hesse space.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11651_n_qutrit_hesse_space as H  # noqa: E402

OUT = ROOT / "data" / "w33_pass11658_hesse_cp_tower.json"


def group(n):
    d, pts, idx, B, wg = H.setup(n)
    G = H.closure([H.R_of(B, g) for g in wg.values()])
    if n == 2:
        G = H.closure([M for M in G if H.is_reflection(M)])
    return np.array(G)


def odd_even_dims(G, kmax, npts=60, seed=0):
    rng = np.random.default_rng(seed)
    dim = G.shape[1]
    X = rng.normal(size=(npts, dim)) + 1j * rng.normal(size=(npts, dim))
    IM = np.einsum("gij,pj->gpi", G, X)
    IMC = np.einsum("gij,pj->gpi", G, X.conj())
    out = {}
    for k in range(1, kmax + 1):
        ev_rows, od_rows = [], []
        for _ in range(8 + 6 * k):
            l1 = (rng.normal(size=dim) + 1j * rng.normal(size=dim))
            l2 = (rng.normal(size=dim) + 1j * rng.normal(size=dim))
            a1, a2 = (IM @ l1).astype(complex), (IM @ l2).astype(complex)
            f = (a1 ** k * np.conj(a2) ** k).mean(0)
            b1, b2 = (IMC @ l1).astype(complex), (IMC @ l2).astype(complex)
            fc = (b1 ** k * np.conj(b2) ** k).mean(0)
            ev_rows.append(f + fc)
            od_rows.append(f - fc)
        scale = max(np.linalg.svd(np.array(ev_rows), compute_uv=False)[0], 1e-300)
        rk = lambda rows: int((np.linalg.svd(np.array(rows), compute_uv=False) > 1e-9 * scale).sum())  # noqa: E731
        out[k] = dict(even=rk(ev_rows), odd=rk(od_rows))
        print(k, out[k], flush=True)
    return out


def molien_totals(G, K):
    """exact dim of G-invariants in Sym^k V (x) Sym^k Vbar, k = 1..K: (1/|G|) sum_g |h_k(eig g)|^2"""
    ev = np.array([np.linalg.eigvals(M) for M in G])
    h = np.zeros((len(G), K + 1), complex)
    h[:, 0] = 1
    for i in range(ev.shape[1]):
        geo = ev[:, i][:, None] ** np.arange(K + 1)[None, :]
        new = np.zeros_like(h)
        for k in range(K + 1):
            new[:, k] = (h[:, :k + 1] * geo[:, k::-1]).sum(1)
        h = new
    return {k: int(round(float((np.abs(h[:, k]) ** 2).mean()))) for k in range(1, K + 1)}


def tower():
    res = {}
    for n in (2, 3):
        d, pts, idx, B, wg = H.setup(n)
        par = np.zeros((d, d))
        for a in pts:
            b = list(a)
            b[-1] = (-b[-1]) % 3
            par[idx[tuple(b)], idx[a]] = 1
        ev = np.linalg.eigvals(H.R_of(B, par))
        res[f"n{n}"] = dict(hesse_dim=B.shape[1], minus_one_multiplicity_of_local_parity=int(np.sum(np.abs(ev + 1) < 1e-6)),
                            predicted=(3 ** (n - 1) - 1) // 2)
    return res


def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = json.load(open(OUT)) if OUT.exists() else dict(pass_id=11658)
    if stage in ("tower", "all"):
        res["tower"] = tower()
        print(res["tower"], flush=True)
    if stage in ("n1", "all"):
        res["n1"] = odd_even_dims(group(1), 8)
    if stage in ("n2", "all"):
        res["n2"] = odd_even_dims(group(2), int(sys.argv[2]) if len(sys.argv) > 2 else 10)
    if stage in ("molien", "all"):
        for n, K in ((1, 8), (2, 10)):
            tot = molien_totals(group(n), K)
            res[f"molien_n{n}"] = tot
            if f"n{n}" in res:
                res[f"reynolds_complete_n{n}"] = {str(k): (res[f"n{n}"][str(k) if str(k) in res[f"n{n}"] else k]["even"]
                                                          + res[f"n{n}"][str(k) if str(k) in res[f"n{n}"] else k]["odd"]) == tot[k]
                                                  for k in tot if (str(k) in res[f"n{n}"] or k in res[f"n{n}"])}
        print({k: v for k, v in res.items() if k.startswith(("molien", "reynolds"))}, flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
