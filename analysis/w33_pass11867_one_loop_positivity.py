"""Pass 11867: one-loop corrections to the boundary four-point function and the positivity region.

Same conventions as Pass 11861 (unit-normalised boundary operators, crosscap propagator G = 12 Pi_15 for phi,
K = N G / sqrt(216)); the hidden chi is switched off (g' = 0).  One-loop 1PI four-point diagrams of the phi^3 + phi^4
bulk theory, with Euclidean vertex factors (-g3), (-g4) and the stated combinatorial weights:
  bubble   (g4^2 / 2)  sum_{p,q} K_a K_b (p) G(p,q)^2 K_c K_d (q)                       + t + u
  triangle (-g4 g3^2)  sum_{p,q,r} K_a K_b (p) G(p,q) G(p,r) G(q,r) K_c(q) K_d(r)    over the 6 pairs at the quartic vertex
  box      (g3^4)      sum K_a(p) G(p,q) K_b(q) G(q,r) K_c(r) G(r,s) K_d(s) G(s,p)    over the 3 cyclic orders
Everything is computed in the boundary-15 basis; the s-channel operators are scalar on the channels
1, 15, 20, 24, 60 (Sym^2) and vanish on Alt^2.  Positivity D + tree + loop >= 0 is examined channel by channel.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11847_finite_bulk_path_integral as BP  # noqa: E402

OUT = ROOT / "data" / "w33_pass11867_one_loop_positivity.json"


def sym4(T):
    out = np.zeros_like(T)
    for p in itertools.permutations(range(4)):
        out += T.transpose(p)
    return out / 24


def main():
    K36, X, A, G0, N, Cx = BP.setup()
    P = BP.eigenprojectors(A)
    P15 = P[3.0]
    G = 12 * P15
    Pb = BP.eigenprojectors(Cx)[-4.0]
    w, V = np.linalg.eigh(Pb)
    U = V[:, w > 0.5]
    K = U.T @ (N @ G) / np.sqrt(216)  # 15 x 36
    I15 = np.eye(15)
    D = np.einsum("ac,bd->abcd", I15, I15) + np.einsum("ad,bc->abcd", I15, I15) + np.einsum("ab,cd->abcd", I15, I15)
    Kab = np.einsum("ap,bp->abp", K, K)
    C = np.einsum("abp,cdp->abcd", Kab, Kab)
    E15s = np.einsum("abp,pq,cdq->abcd", Kab, G, Kab)
    E15 = E15s + E15s.transpose(0, 2, 1, 3) + E15s.transpose(0, 3, 2, 1)
    G2 = G * G
    Bs = np.einsum("abp,pq,cdq->abcd", Kab, G2, Kab)
    Bub = 0.5 * (Bs + Bs.transpose(0, 2, 1, 3) + Bs.transpose(0, 3, 2, 1))
    Xm = np.einsum("pq,cq->pqc", G, K)  # G(p,q) K_c(q)
    W = np.einsum("pqc,qr,prd->pcd", Xm, G, Xm)  # sum_{q,r} G(p,q)K_c(q) G(q,r) G(p,r) K_d(r)
    Tri0 = np.einsum("abp,pcd->abcd", Kab, W)
    Tri = np.zeros_like(Tri0)
    for perm in [(0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2), (1, 2, 0, 3), (1, 3, 0, 2), (2, 3, 0, 1)]:
        Tri += Tri0.transpose(np.argsort(perm))
    KG = np.einsum("ap,pq->apq", K, G)  # K_a(p) G(p,q)
    Bx = np.einsum("apq,bqr,crs,dsp->abcd", KG, KG, KG, KG, optimize=True)
    Box = Bx + Bx.transpose(0, 2, 1, 3) + Bx.transpose(0, 1, 3, 2)
    structs = dict(D=D, C=C, E15=E15, Bub=Bub, Tri=Tri, Box=Box)
    for nm, Tt in structs.items():
        assert np.allclose(Tt, sym4(Tt), atol=1e-8 * max(1, abs(Tt).max())), nm
    mats = {nm: Tt.reshape(225, 225) for nm, Tt in structs.items()}
    gen = sum(c * mats[nm] / max(1e-12, abs(mats[nm]).max()) for c, nm in zip((1.0, np.pi, np.e, np.sqrt(2), 0.77, 1.31), mats))
    swap = np.zeros((225, 225))
    for a in range(15):
        for b in range(15):
            swap[a * 15 + b, b * 15 + a] = 1
    gen = (gen + gen.T) / 2 + 0.123 * swap
    ev, Qm = np.linalg.eigh(gen)
    clusters = []
    for i, x in enumerate(ev):
        if clusters and abs(x - clusters[-1]["val"]) < 1e-7:
            clusters[-1]["idx"].append(i)
        else:
            clusters.append(dict(val=x, idx=[i]))
    table = []
    for cl in clusters:
        Vk = Qm[:, cl["idx"]]
        row = dict(dim=len(cl["idx"]), swap=round(float(np.trace(Vk.T @ swap @ Vk) / len(cl["idx"])), 6))
        for nm, Mx in mats.items():
            R = Vk.T @ Mx @ Vk
            row[nm] = round(float(np.trace(R) / len(cl["idx"])), 6)
            assert np.allclose(R, row[nm] * np.eye(len(cl["idx"])), atol=1e-6 * max(1, abs(Mx).max())), (nm, row["dim"])
        table.append(row)
    sym = [r for r in table if r["swap"] > 0]

    def lam(r, g3sq, g4):
        return r["D"] - g4 * r["C"] + g3sq * r["E15"] + 0.5 * 0 + (g4**2) * r["Bub"] - g4 * g3sq * r["Tri"] + g3sq**2 * r["Box"]

    def lam_tree(r, g3sq, g4):
        return r["D"] - g4 * r["C"] + g3sq * r["E15"]
    # positivity regions on a grid at g' = 0
    g3s = np.linspace(0, 0.06, 241)
    g4s = np.linspace(-0.4, 0.2, 241)
    region = {}
    for name, f in (("tree", lam_tree), ("one_loop", lam)):
        ok = np.array([[all(f(r, a, b) >= -1e-12 for r in sym) for b in g4s] for a in g3s])
        allowed = [g3s[i] for i in range(len(g3s)) if ok[i].any()]
        g4max = [g4s[j] for j in range(len(g4s)) if ok[0, j]]
        region[name] = dict(max_g3_squared=float(max(allowed)) if allowed else None,
                            g4_window_at_g3_zero=[float(min(g4max)), float(max(g4max))] if g4max else None,
                            allowed_fraction_of_grid=float(ok.mean()))
    res = {"pass_id": 11867, "convention": __doc__.split("One-loop")[1].split("Everything")[0].strip(),
           "channels": table, "regions_g_prime_zero": region}
    json.dump(res, open(OUT, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
