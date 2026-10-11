"""Sampler for Passes 11918/11920: SU(5) on magnetized T4 with det-3 dual fluxes, broken to the SM by a hypercharge Wilson
line w.  Positions: zeta_X = zeta_rep + Y_X N_rep^{-1} w, with 10 = Q(1/6), u^c(-2/3), e^c(1) and 5bar = d^c(1/3), L(-1/2).
Up: Q x u^c (N10, N10); down: Q x d^c (N10, N5); lepton: e^c x L (N10, N5), with the same H_d mode as down (the H_d
position is the same from both couplings because N10 (z_e - z_Q) + N5 (z_L - z_d) = (5/6) w - (5/6) w = 0).
Row columns: sample, down Higgs mode, up Higgs mode, |w|, Im y, md/ms, ms/mb, mu/mc, mc/mt, me/mmu, mmu/mtau,
|V_us|, |V_cb|, |V_ub|, |V_td|   (CKM = U_up^dag U_down on the shared Q index, heavy-first SVD ordering).
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402

PAIRS = {"114": [[1, 1], [1, 4]], "A2": [[2, 1], [1, 2]]}
HYPER = dict(Q=1 / 6, u=-2 / 3, e=1.0, d=1 / 3, L=-1 / 2)


def positions(N10, N5, z10, z5, w):
    s10, s5 = np.linalg.solve(np.array(N10, float), w), np.linalg.solve(np.array(N5, float), w)
    return dict(Q=z10 + HYPER["Q"] * s10, u=z10 + HYPER["u"] * s10, e=z10 + HYPER["e"] * s10,
                d=z5 + HYPER["d"] * s5, L=z5 + HYPER["L"] * s5)


def sample(seed, nsamp, pair, wscale=1.0, G=12, only=None, K=4):
    """K = theta truncation |n_i| <= K. The frozen scans used K = 4, which is accurate to ~1e-7 of the largest singular
    value at large Wilson-line offsets; exact zeros are certified with K = 7 (residual 3e-15)."""
    saved = F.NS
    F.NS = np.array([(a, b) for a in range(-K, K + 1) for b in range(-K, K + 1)])
    try:
        return _sample(seed, nsamp, pair, wscale, G, only)
    finally:
        F.NS = saved


def _sample(seed, nsamp, pair, wscale, G, only):
    N10 = PAIRS[pair]
    N5 = np.round(3 * np.linalg.inv(N10)).astype(int).tolist()
    N10a = np.array(N10, float)
    lam = np.linalg.eigvalsh(N10a)
    rng = np.random.default_rng(seed)
    out = []
    for it in range(nsamp):
        while True:
            xi, yi = rng.uniform(0.5, 3.0), rng.uniform(-0.5, 0.8)
            if min(xi + yi * lam) > 0.4:
                break
        xr, yr = rng.uniform(-0.5, 0.5, 2)
        Om = (xr + 1j * xi) * np.eye(2) + (yr + 1j * yi) * N10a

        def lat(v):
            return v[:2] + Om @ v[2:]

        z10, z5, w = lat(rng.random(4)), lat(rng.random(4)), wscale * lat(rng.random(4) - 0.5)
        if only is not None and it not in only:
            continue
        P = positions(N10, N5, z10, z5, w)
        T = F.T4(Om, G)
        try:
            Yu = F.yukawas(T, N10, N10, P["Q"], P["u"])
            Yd = F.yukawas(T, N10, N5, P["Q"], P["d"])
            Ye = F.yukawas(T, N10, N5, P["e"], P["L"])
            Su = [np.linalg.svd(Y)[:2] for Y in Yu]
            Sd = [np.linalg.svd(Y)[:2] for Y in Yd]
            Se = [np.linalg.svd(Y, compute_uv=False) for Y in Ye]
        except Exception:
            continue
        if not all(np.all(np.isfinite(s)) for _, s in Su + Sd):
            continue
        for kd, (UD, sd) in enumerate(Sd):
            se = Se[kd]
            for ku, (UU, su) in enumerate(Su):
                V = abs(UU.conj().T @ UD)
                out.append([it, kd, ku, np.linalg.norm(w), yi, sd[2] / sd[1], sd[1] / sd[0], su[2] / su[1], su[1] / su[0],
                            se[2] / se[1], se[1] / se[0], V[2, 1], V[1, 0], V[2, 0], V[0, 2]])
    return np.array(out)


if __name__ == "__main__":
    seed, nsamp, pair = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    np.save(sys.argv[4], sample(seed, nsamp, pair))
