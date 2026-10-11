"""Pass 11910: down quarks, leptons and the CKM in the minimal magnetized home -- a cross-sector test.

Minimal home: every Yukawa sector (up: Q u^c H_u; down: Q d^c H_d; leptons: L e^c H_d) has fluxes (3, 3, 6) on the shared
family torus tau, its own relative Wilson line, and a localised Higgs. By Pass 11906 each sector's masses are
|theta[c/3,0](3 zeta_s, 6 tau)| times the Gaussian factor, so:

1. The Gaussian invariant I_s = m_1 m_2 / m_3^2 = e^{-(4 pi/3) Im tau} is the SAME for every sector (independent of its
   own Wilson line) -- checked on the exact texture for three different Wilson lines.
2. Data (running masses at M_Z, Xing-Zhang-Zhou, arXiv:0712.1419): I_up = 2.67e-8, I_down = 1.91e-5,
   I_lept = 1.64e-5, i.e. implied Im tau = 4.18 (up), 2.60 (down), 2.66 (leptons). Down and leptons agree (invariants to
   17%, Im tau to 2% -- the product form of the Georgi-Jarlskog pattern), the up sector does not (Im tau ratio 1.6;
   ratios within a sector are nearly scale-independent, so running does not close a factor ~700). The minimal home with
   ONE family torus for all sectors is falsified by the up/down comparison: the up Yukawas need a larger effective area.
3. CKM: with a localised Higgs, each Yukawa matrix has one nonzero entry per row (selection i + j = k mod 3), so
   Y Y^dagger is diagonal in the family basis for up and down alike and |V_CKM| is a permutation matrix: V_us = 0
   (also TOE46 front 4). Data need |V_us| = 0.225.
4. A second Higgs component in another selection class (admixture eps) produces mixing linear in eps (0.074, 0.148 for
   eps = 1e-3, 2e-3; 0.286 at 4e-3), so a Cabibbo-sized angle needs only eps ~ 3e-3 -- but it needs a non-localised
   Higgs, which the localised-Higgs dynamics of Passes 11907/11909 does not supply (TOE48: Higgs-mode phases flat).
"""

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11910_cross_sector_invariant_and_ckm.json"
N = np.arange(-40, 41)
DATA_MZ = dict(u=1.27e-3, c=0.619, t=171.7, d=2.90e-3, s=55e-3, b=2.89, e=0.486570e-3, mu=102.71814e-3, tau=1.74624)


def th(a, z, Om):
    return np.sum(np.exp(1j * np.pi * (N + a) ** 2 * Om + 2j * np.pi * (N + a) * z))


def yuk_matrix(zeta, tau, k=0):
    """3x3 Yukawa for a localised Higgs at class k: entry (i, j) nonzero iff i + j = k mod 3, value theta[(i-j)/3]"""
    g = np.exp(-1.5 * np.pi * zeta.imag ** 2 / tau.imag)
    Y = np.zeros((3, 3), complex)
    for i in range(3):
        j = (k - i) % 3
        Y[i, j] = g * th(((i - j) % 3) / 3, 3 * zeta, 6 * tau)
    return Y


def main():
    tau = 2.6j
    inv = []
    for zeta in (0.11 * tau, 0.05 + 0.2 * tau, 0.15 * tau):  # generic nu (away from the level crossing at nu -> 1/3)
        m = np.sort(np.linalg.svd(yuk_matrix(zeta, tau), compute_uv=False))
        inv.append(float(m[0] * m[1] / m[2] ** 2))
    pred = float(np.exp(-4 * np.pi / 3 * tau.imag))
    D = DATA_MZ
    I = dict(up=D["u"] * D["c"] / D["t"] ** 2, down=D["d"] * D["s"] / D["b"] ** 2, lept=D["e"] * D["mu"] / D["tau"] ** 2)
    imtau = {k: float(-np.log(v) * 3 / (4 * np.pi)) for k, v in I.items()}
    # CKM with localised Higgs in each sector
    Yu, Yd = yuk_matrix(0.12 * 4.2j, 4.2j, k=0), yuk_matrix(0.07 * 2.6j + 0.03, 2.6j, k=1)
    Uu = np.linalg.svd(Yu)[0]
    Ud = np.linalg.svd(Yd)[0]
    V = abs(Uu.conj().T @ Ud)
    is_perm = np.allclose(np.sort(V, axis=1), [[0, 0, 1]] * 3, atol=1e-9)
    # admixture eps of a second Higgs class in the down sector: mixing linear in eps (SVD-ordered mass eigenstates)
    vus = []
    for eps in (1e-3, 2e-3, 4e-3):
        Ud2 = np.linalg.svd(Yd + eps * yuk_matrix(0.07 * 2.6j + 0.03, 2.6j, k=2))[0]
        Vm = abs(Uu.conj().T @ Ud2)
        vus.append(float(np.sort(Vm.ravel())[-4]))
    res = dict(pass_id=11910, invariants_exact_texture=inv, invariant_predicted=pred, data_MZ=D,
               data_invariants={k: float(v) for k, v in I.items()}, implied_im_tau=imtau,
               ckm_localised_abs=V.tolist(), ckm_is_permutation=bool(is_perm), admixture_mixing=vus)
    res["checks"] = {k: bool(v) for k, v in dict(
        invariant_universal=max(abs(x / pred - 1) for x in inv) < 1e-3,
        down_lepton_agree=abs(np.log(I["down"] / I["lept"])) < np.log(1.25),
        up_disagrees=I["down"] / I["up"] > 100,
        localised_ckm_trivial=is_perm,
        admixture_mixing_linear=abs(vus[1] / vus[0] - 2) < 0.05 and vus[2] > 0.225 > vus[1],
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
