"""Pass 11933: radiative selection plus the residual Z3 fixes the Weinberg mediator, and the neutrino spectrum obeys an
eps-independent relation m3/m1 = kappa * Dm2_21/Dm2_31 with kappa ~ 1.

Setting: A2 dual pair at the Eisenstein point (Passes 11928-11932); Weinberg channel L.L with mediator flux 2A2' (12
modes). Radiative selection (the mediator direction with maximal coupling, top eigenspace of the Gram matrix
C = sum_ab Y_ab Y_ab^*) and a vacuum respecting the residual Z3.

1. The Gram top space is exactly 3-dimensional (the flavour qutrit) and contains charges 0 and 2 only (charge 1 is
   radiatively disfavoured, Gram 0.79). Its intersections with the charge sectors: charge 0 -> 1 dim, charge 2 -> 2 dim.
2. Every Z3-symmetric radiative direction gives (1,1,0) at Omega = w.
3. Near the point: the charge-0 direction keeps the pair degenerate (no solar splitting at this order: excluded);
   every charge-2 direction has BOTH the pair splitting and the light mass scaling as eps^2 (log-slopes 2.00).
   Hence eps cancels:  m3/m1 = kappa * (Dm2_21/Dm2_31),  kappa = b/(2a),
   with kappa ~ 0.9 (5-95%: ~0.5-2.5) over the charge-2 directions and over deformation directions.
Reading: inverted ordering with m3 ~ 1.3 meV (range ~0.8-3.8 meV) for m1 ~ 49.5 meV -- conditional only on the A2
flux at (near) the Eisenstein point, radiative selection of the mediator and a Z3-respecting vacuum; no eps, no blow-up
sign. Falsifiable by the mass ordering (JUNO, DUNE) and, for IO, m_bb ~ 15-50 meV.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402
import w33_pass11928_eisenstein_point as E  # noqa: E402
import w33_pass11930_fixed_point_avoiding_higgs as P  # noqa: E402

OUT = ROOT / "data" / "w33_pass11933_radiative_neutrino_relation.json"
A2M, NH = [[2, -1], [-1, 2]], [[4, -2], [-2, 4]]


def main():
    F.NS = np.array([(a, b) for a in range(-7, 8) for b in range(-7, 8)])
    rng = np.random.default_rng(11933)
    T0 = P.tensor(A2M, A2M, NH, E.OM0)
    M = T0.reshape(12, 9)
    C = M.conj() @ M.T
    w, V = np.linalg.eigh(C)
    top = V[:, -3:]
    R = E.rho_matrix(NH)
    wr, Ur = np.linalg.eig(R)
    q = np.array([int(round(np.angle(x) / (2 * np.pi / 3))) % 3 for x in wr])
    res = dict(pass_id=11933, gram_top=[float(x) for x in (w[::-1] / w[-1])[:6]])
    sector_max = {}
    inter = {}
    for cq in range(3):
        S, _ = np.linalg.qr(Ur[:, q == cq])
        sector_max[cq] = float(np.linalg.eigvalsh(S.T @ C @ S.conj())[-1] / w[-1])
        u, s, vh = np.linalg.svd(np.hstack([top, -S.conj()]))
        nul = vh[np.sum(s > 1e-9):].conj().T
        inter[cq] = top @ nul[:3, :] if nul.shape[1] else np.zeros((12, 0))
    res["sector_max_gram"] = sector_max
    res["top_intersection_dims"] = {c: int(inter[c].shape[1]) for c in range(3)}

    def spec(d, eps, dirn):
        Om = E.OM0 + eps * (dirn[0] * np.eye(2) + dirn[1] * E.J)
        sv = np.linalg.svd(np.tensordot(d, P.tensor(A2M, A2M, NH, Om), 1), compute_uv=False)
        return sv / sv[0]

    at_w = []
    for c in (0, 2):
        for k in range(inter[c].shape[1]):
            d = inter[c][:, k] / np.linalg.norm(inter[c][:, k])
            sv = spec(d, 0.0, (1, 0))
            at_w.append(float(abs(1 - sv[1]) + sv[2]))
    res["at_w_dev_from_110"] = max(at_w)
    d0 = inter[0][:, 0] / np.linalg.norm(inter[0][:, 0])
    sv0 = spec(d0, 1e-2, (1, 0.4 + 0.3j))
    res["charge0_split_at_eps_1e-2"] = float(1 - sv0[1])
    B2, _ = np.linalg.qr(inter[2])
    ks, sl = [], []
    for _ in range(24):
        d = B2 @ (rng.normal(size=2) + 1j * rng.normal(size=2))
        d /= np.linalg.norm(d)
        dirn = rng.normal(size=2) + 1j * rng.normal(size=2)
        r = []
        for eps in (3e-3, 1e-3):
            sv = spec(d, eps, dirn)
            r.append((1 - sv[1], sv[2]))
        sl.append((np.log10(r[0][0] / r[1][0]) / np.log10(3), np.log10(r[0][1] / r[1][1]) / np.log10(3)))
        ks.append(r[1][1] / (2 * r[1][0]))
    ks = np.array(ks)
    sl = np.array(sl)
    ratio = 7.42e-5 / 2.43e-3
    res.update(slopes=sl.tolist(), kappa=ks.tolist(), kappa_quantiles=[float(x) for x in np.quantile(ks, [0.05, 0.5, 0.95])],
               m3_meV_quantiles=[float(x) for x in np.quantile(ks, [0.05, 0.5, 0.95]) * ratio * 49.5])
    res["checks"] = {k: bool(v) for k, v in dict(
        gram_top_three=abs(res["gram_top"][2] - 1) < 1e-9 and res["gram_top"][3] < 0.9,
        charge1_disfavoured=sector_max[1] < 0.9 and sector_max[0] > 0.999 and sector_max[2] > 0.999,
        top_intersections_1_0_2=res["top_intersection_dims"] == {0: 1, 1: 0, 2: 2},
        symmetric_radiative_directions_give_110=res["at_w_dev_from_110"] < 1e-9,
        charge0_no_solar_splitting=res["charge0_split_at_eps_1e-2"] < 1e-5,
        charge2_split_and_light_both_eps2=bool(np.all(abs(sl - 2) < 0.05)),
        kappa_order_one=0.2 < res["kappa_quantiles"][1] < 5,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"], res["kappa_quantiles"], res["m3_meV_quantiles"])


if __name__ == "__main__":
    main()
