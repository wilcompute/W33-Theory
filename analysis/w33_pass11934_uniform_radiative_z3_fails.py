"""Pass 11934: the radiative + residual-Z3 principle of Pass 11933, applied uniformly, gives (1,1,0) in every sector --
so the neutrino reading is sector-specific, not a universal principle.

At the Eisenstein point (A2 dual pair, Omega = w.1), for each Yukawa channel take the radiative top space of the
mediator (Gram top eigenspace) and its residual-Z3-symmetric directions:
* up (10.10, H_u flux 2A2): top space 3-dim (charges 0 and 2) -> every symmetric direction gives (1,1,0): top = charm;
* down / charged lepton (10.5bar, H_d flux 4.1): top space 1-dim, charge 2 -> (1,1,0) at w and (1, 1 - O(eps^2), 0)
  nearby: m_b = m_s and m_tau = m_mu, with the lightest exactly massless (the dual-pair zero of Pass 11916);
* Weinberg (L.L, 2A2'): (1,1,0) -> inverted ordering (Pass 11933).
Reading: the uniform principle predicts the theta-zero pattern everywhere; three charged sectors contradict the data
(m_c/m_t ~ 4e-3, m_s/m_b ~ 0.02, m_mu/m_tau ~ 0.06). The inverted-ordering prediction of Pass 11933 therefore needs a
reason specific to the neutrino mediator; as a consequence of one universal rule it is excluded. Recorded to prevent
an over-read.
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

OUT = ROOT / "data" / "w33_pass11934_uniform_radiative_z3_fails.json"
A2, A2M = [[2, 1], [1, 2]], [[2, -1], [-1, 2]]
CHANNELS = {"up": (A2, A2, [[4, 2], [2, 4]]), "down_lepton": (A2, A2M, [[4, 0], [0, 4]]), "weinberg": (A2M, A2M, [[4, -2], [-2, 4]])}


def radiative_symmetric(N1, N2, NH):
    T0 = P.tensor(N1, N2, NH, E.OM0)
    n = T0.shape[0]
    M = T0.reshape(n, 9)
    C = M.conj() @ M.T
    w, V = np.linalg.eigh(C)
    k = int(np.sum(w > w[-1] * (1 - 1e-9)))
    top = V[:, -k:]
    R = E.rho_matrix(NH)
    wr, Ur = np.linalg.eig(R)
    q = np.array([int(round(np.angle(x) / (2 * np.pi / 3))) % 3 for x in wr])
    secs = {}
    for cq in range(3):
        S, _ = np.linalg.qr(Ur[:, q == cq])
        u, s, vh = np.linalg.svd(np.hstack([top, -S.conj()]))
        nul = vh[np.sum(s > 1e-9):].conj().T
        if nul.shape[1]:
            secs[cq] = top @ nul[:k, :]
    return k, secs


def main():
    F.NS = np.array([(a, b) for a in range(-7, 8) for b in range(-7, 8)])
    res = dict(pass_id=11934, channels={})
    for name, (N1, N2, NH) in CHANNELS.items():
        k, secs = radiative_symmetric(N1, N2, NH)
        dirs = []
        for c, B in secs.items():
            for j in range(B.shape[1]):
                d = B[:, j] / np.linalg.norm(B[:, j])
                sp = {}
                for eps in (0.0, 1e-2):
                    Om = E.OM0 + eps * (np.eye(2) + (0.4 + 0.3j) * E.J)
                    sv = np.linalg.svd(np.tensordot(d, P.tensor(N1, N2, NH, Om), 1), compute_uv=False)
                    sp[str(eps)] = [float(x) for x in sv / sv[0]]
                dirs.append(dict(charge=c, spectra=sp))
        res["channels"][name] = dict(top_dim=k, symmetric_dims={c: int(B.shape[1]) for c, B in secs.items()}, directions=dirs)
    dev = lambda s: abs(1 - s[1]) + s[2]
    res["checks"] = {kk: bool(v) for kk, v in dict(
        up_top3_and_110=res["channels"]["up"]["top_dim"] == 3 and all(dev(d["spectra"]["0.0"]) < 1e-9 for d in res["channels"]["up"]["directions"]),
        down_lepton_top1_charge2_110=res["channels"]["down_lepton"]["top_dim"] == 1 and list(res["channels"]["down_lepton"]["symmetric_dims"]) == [2]
        and dev(res["channels"]["down_lepton"]["directions"][0]["spectra"]["0.0"]) < 1e-9,
        down_lepton_heavy_pair_stays_degenerate=abs(1 - res["channels"]["down_lepton"]["directions"][0]["spectra"]["0.01"][1]) < 1e-3,
        weinberg_110=all(dev(d["spectra"]["0.0"]) < 1e-9 for d in res["channels"]["weinberg"]["directions"]),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])


if __name__ == "__main__":
    main()
