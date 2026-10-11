"""Pass 11912: the W(3,3) entangling modulus is the family Wilson line.

Two-qutrit magnetized home (flux 3 on each torus of T4, Siegel modulus Omega; normalisation of Pass 11906, toy units
Omega = 6 x physical). Families are the eigenspace of a Wilson-line Pauli on torus 2 (Pass 11900): fixed class a, family
label c. Their localised-Higgs couplings are the genus-2 thetas Theta[(c/3, a/3), 0](0, Omega), and

    Theta[(alpha1, alpha2)](0, Omega) = sum_n e^{i pi (n + alpha2)^2 Omega22} theta[alpha1]((n + alpha2) Omega12, Omega11)

exactly (checked to 1e-16). When Im Omega22 is large the term with n + alpha2 closest to 0 dominates, so the family
texture IS the one-qutrit texture of Passes 11904-11907 with Wilson-line argument

    z_eff = (a~/3) Omega12,   a~ in {0, +1, -1} the representative of a mod 3 (a = 2 -> a~ = -1).

Consequences:
  * a = 0 (left and right families in the same Pauli class): z_eff = 0, the light pair is locked (cf. Passes 11900, 11903).
  * a = 1, 2: the off-diagonal (entangling, W(3,3)) complex-structure modulus acts as a continuous Wilson line. The up
    hierarchy point of Passes 11904/11906 (Omega11 = 25.25 i, Im z = 1.523) is reached at Im Omega12 = 4.57 (a = 1),
    with NO Wilson line: m_c/m_t = 3.61e-3, m_u/m_c = 1.69e-3 for Im Omega22 >= 16 (agreement with the one-qutrit texture
    7.6e-4 at Im Omega22 = 16, 3e-10 at 30); a = 2 gives z_eff = -Omega12/3, the mirror of a = 1 (identical masses).
  * Hence the Wilson-line dynamics of Passes 11907/11909 becomes complex-structure dynamics. Complex-structure moduli
    are stabilised at tree level by three-form fluxes in type IIB (Giddings-Kachru-Polchinski), so the hierarchy point
    can be fixed by flux quanta rather than by the radiative balance that Pass 11909 found to need a top-sector
    cancellation. This is a route, not a constructed flux vacuum.
Side result (recorded, no claim): a small second-class Higgs admixture in the down sector gives Cabibbo-sized mixing but
no Gatto-Sartori-Tonin relation (corr(log V_us, log sqrt(m_d/m_s)) = 0.11 over 400 random admixtures) and V_cb = 0.
"""

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11912_entangling_modulus_is_the_wilson_line.json"
R = np.arange(-14, 15)
N1, N2 = [x.ravel() for x in np.meshgrid(R, R, indexing="ij")]
N = np.arange(-40, 41)


def Th2(a1, a2, Om):
    x1, x2 = N1 + a1, N2 + a2
    return np.sum(np.exp(1j * np.pi * (Om[0, 0] * x1 * x1 + 2 * Om[0, 1] * x1 * x2 + Om[1, 1] * x2 * x2)))


def th(a, z, Om):
    return np.sum(np.exp(1j * np.pi * (N + a) ** 2 * Om + 2j * np.pi * (N + a) * z))


def ratios(m):
    m = np.sort(m)
    return m / m[-1]


def main():
    rng = np.random.default_rng(11912)
    ident = []
    for _ in range(4):
        A = rng.normal(size=(2, 2))
        Om = (A + A.T) / 4 + 1j * (np.array([[2.0, 0.4], [0.4, 1.5]]) + 0.2 * np.eye(2))
        for a1, a2 in ((1 / 3, 1 / 3), (2 / 3, 1 / 3), (0, 2 / 3)):
            lhs = Th2(a1, a2, Om)
            rhs = sum(np.exp(1j * np.pi * (m + a2) ** 2 * Om[1, 1]) * th(a1, (m + a2) * Om[0, 1], Om[0, 0]) for m in R)
            ident.append(float(abs(lhs - rhs) / abs(lhs)))
    conv = {}
    for o22 in (8.0, 16.0, 30.0):
        Om = np.array([[25.25j, 4.57j], [4.57j, o22 * 1j]])
        row = {}
        for a in (0, 1, 2):
            r2 = ratios(np.array([abs(Th2(c / 3, a / 3, Om)) for c in range(3)]))
            r1 = ratios(np.array([abs(th(c / 3, (a / 3) * Om[0, 1], Om[0, 0])) for c in range(3)]))
            row[str(a)] = dict(two_qutrit=[float(x) for x in r2], one_qutrit_z_eff=[float(x) for x in r1],
                               max_rel=float(np.max(abs(r2 - r1) / np.maximum(r1, 1e-300))))
        conv[str(o22)] = row
    hier = conv["30.0"]["1"]["two_qutrit"]
    res = dict(pass_id=11912, identity_rel_err_max=max(ident), convergence=conv,
               hierarchy_from_omega12=dict(mc_over_mt=hier[1], mu_over_mc=hier[0] / hier[1]))
    res["checks"] = {k: bool(v) for k, v in dict(
        exact_identity=max(ident) < 1e-12,
        class_zero_locked=all(abs(conv[k]["0"]["two_qutrit"][0] - conv[k]["0"]["two_qutrit"][1]) < 1e-12
                              for k in conv),
        gaussian_regime_converges=conv["8.0"]["1"]["max_rel"] > conv["16.0"]["1"]["max_rel"] > conv["30.0"]["1"]["max_rel"]
        and conv["30.0"]["1"]["max_rel"] < 1e-4,
        mirror_class_two=np.allclose(conv["30.0"]["2"]["two_qutrit"], conv["30.0"]["1"]["two_qutrit"], rtol=1e-6)
        or conv["30.0"]["2"]["max_rel"] < 1e-4,
        up_hierarchy_without_wilson_line=abs(hier[1] - 3.6e-3) < 2e-5 and abs(hier[0] / hier[1] - 1.7e-3) < 2e-5,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps({k: v for k, v in res.items() if k != "convergence"}, indent=1))


if __name__ == "__main__":
    main()
