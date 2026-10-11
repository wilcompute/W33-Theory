"""Pass 11914: the Higgs is the flavour lever -- shared-Q universality, the anarchic spread phase, and the class selection.

1. Shared-Q universality (closes the geometric route to the up/down area mismatch of Pass 11910). In the two-qutrit
   home (genus-2 Siegel thetas, toy units; Omega = i[[25.25, 4.57], [4.57, 16]]) let Q's families be an eigenspace of the
   Pauli Z2 and the right-handed families an eigenspace of ANY of the 40 W(3,3) Pauli points (any eigenvalue), with a
   localised Higgs in any of the 9 classes. Over every full-rank configuration the Gaussian invariant m1 m2 / m3^2 takes
   one value (10^-7.66): it is fixed by Q's family direction alone. Since Q is shared by the up and down Yukawas (as in
   SU(5)), no choice of right-handed W(3,3) eigenspaces can give the observed I_down / I_up ~ 716 with localised Higgs.
2. The spread phase is anarchic. TOE48's minimal Higgs potential has two phases: one Higgs mode, or six equal-norm modes
   with flat phases. With H_u localised (the Pass 11906 up fit) and H_d in the six-mode phase (exact flux-(3,3,6)
   overlaps, random phases), the down spectrum is nearly degenerate and every mass-ordered CKM element has median
   ~ 1/sqrt3 (trimaximal): lepton-like anarchy, not the quark pattern.
3. Class selection. The loop-induced Higgs-mode mass matrix Tr(Y_k Y_k'^dagger) vanishes between different Z3 classes
   (1e-15) and not within a class: the exact magnetic-translation Z3 forbids radiative cross-class admixture at every
   order. The small cross-class admixture that Cabibbo-sized mixing needs (Passes 11910/11912) therefore requires
   explicit breaking of the magnetic-translation symmetry; symmetric Higgs potentials give either the localised or the
   spread phase.
Corrections acknowledged (parallel TOE49, d3c7321f9): Pass 11910's "Cabibbo-sized" statistic used the fourth-largest
|V| entry, not the mass-ordered V_us, and its CKM illustration used two different taus while the minimal home shares one;
TOE49's mass-ordered scan of that ansatz (6,336 points) found none with V_us, V_cb, V_ub all within a factor 2. Pass
11909's Q-band is scheme-dependent: a finite matching counterterm absorbs it, so its physical content is the matched
coefficient of the sum of Yukawa-squared Higgs-mass terms, not the value of Q/m~. Item 2 uses mass-ordered labels.
"""

import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11914_higgs_is_the_flavour_lever.json"
W = np.exp(2j * np.pi / 3)
R = np.arange(-12, 13)
N1, N2 = [x.ravel() for x in np.meshgrid(R, R, indexing="ij")]
MU = [(a, b) for a in range(3) for b in range(3)]
IX = {m: i for i, m in enumerate(MU)}


def Th2(a1, a2, Om):
    x1, x2 = N1 + a1, N2 + a2
    return np.sum(np.exp(1j * np.pi * (Om[0, 0] * x1 * x1 + 2 * Om[0, 1] * x1 * x2 + Om[1, 1] * x2 * x2)))


def Ytensor(Om, k):
    Y = np.zeros((9, 9), complex)
    for c in MU:
        for cp in MU:
            if (c[0] + cp[0] - k[0]) % 3 == 0 and (c[1] + cp[1] - k[1]) % 3 == 0:
                Y[IX[c], IX[cp]] = Th2(((c[0] - cp[0]) % 3) / 3, ((c[1] - cp[1]) % 3) / 3, Om)
    return Y


def paulis():
    X1, X2 = np.zeros((9, 9)), np.zeros((9, 9))
    for c in MU:
        X1[IX[((c[0] + 1) % 3, c[1])], IX[c]] = 1
        X2[IX[(c[0], (c[1] + 1) % 3)], IX[c]] = 1
    Z1, Z2 = np.diag([W ** c[0] for c in MU]), np.diag([W ** c[1] for c in MU])
    mp = np.linalg.matrix_power
    return lambda a, b: mp(X1, a[0]) @ mp(X2, a[1]) @ mp(Z1, b[0]) @ mp(Z2, b[1])


def eigspaces(P):
    ev, U = np.linalg.eig(P)
    ang = np.round(np.angle(ev) / (2 * np.pi / 3)) % 3
    out = []
    for j in range(3):
        idx = [i for i in range(9) if ang[i] == j]
        if len(idx) == 3:
            out.append(np.linalg.qr(U[:, idx])[0])
    return out


def universality():
    pauli = paulis()
    Om = np.array([[25.25j, 4.57j], [4.57j, 16j]])
    Ys = {k: Ytensor(Om, k) for k in MU}
    points = []
    for v in itertools.product(range(3), repeat=4):
        if any(v) and not any(tuple((2 * x) % 3 for x in v) == p for p in points):
            points.append(v)
    EQ = eigspaces(pauli((0, 0), (0, 1)))
    inv = []
    for p in points:
        for E in eigspaces(pauli(p[:2], p[2:])):
            for k in MU:
                for Eq in EQ:
                    s = np.sort(np.linalg.svd(Eq.T @ Ys[k] @ E, compute_uv=False))
                    if s[2] > 1e-6 and s[0] > 1e-12 * s[2]:
                        inv.append(np.log10(s[0] * s[1] / s[2] ** 2))
    return len(points), len(inv), float(min(inv)), float(max(inv))


def spread_and_selection():
    spec = importlib.util.spec_from_file_location("a", ROOT / "analysis" / "w33_pass11906_magnetized_normalisation_audit.py")
    A = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(A)
    tau = 4.209036j
    T = A.Torus(tau, 200)

    def Ymat(Y, h):
        M = np.zeros((3, 3), complex)
        for (i, j, k), v in Y.items():
            M[i, j] += h[k] * v
        return M

    def ordered(M):
        U, s, _ = np.linalg.svd(M)
        o = np.argsort(s)
        return U[:, o], s[o]
    hu = np.zeros(6, complex)
    hu[0] = 1
    Uu, su = ordered(Ymat(T.yuk(0.1206 * tau / 2, -0.1206 * tau / 2), hu))
    rng = np.random.default_rng(11914)
    rows = []
    for nu in (0.0, 0.12, 0.2):
        Y = T.yuk(nu * tau / 2, -nu * tau / 2)
        for _ in range(200):
            h = np.exp(2j * np.pi * rng.random(6)) / np.sqrt(6)
            Ud, sd = ordered(Ymat(Y, h))
            V = abs(Uu.conj().T @ Ud)
            rows.append([sd[1] / sd[2], sd[0] / sd[1], V[0, 1], V[1, 2], V[0, 2]])
    med = np.median(np.array(rows), axis=0)
    T2 = A.Torus(0.13 + 1.7j, 200)
    Y = T2.yuk(0.21 + 0.33j, -0.07 + 0.11j)
    M = np.array([[sum(Y[(i, j, k)] * np.conj(Y[(i, j, kp)]) for i in range(3) for j in range(3)) for kp in range(6)]
                  for k in range(6)])
    cross = max(abs(M[k, kp]) for k in range(6) for kp in range(6) if (k - kp) % 3)
    same = min(abs(M[k, kp]) for k in range(6) for kp in range(6) if (k - kp) % 3 == 0)
    return dict(up_ratios=[float(su[1] / su[2]), float(su[0] / su[1])],
                spread_median=dict(ms_mb=float(med[0]), md_ms=float(med[1]), Vus=float(med[2]), Vcb=float(med[3]),
                                   Vub=float(med[4]))), float(cross), float(same)


def main():
    npts, nconf, lo, hi = universality()
    spread, cross, same = spread_and_selection()
    res = dict(pass_id=11914, w33_points=npts, full_rank_configs=nconf, log10_invariant_range=[lo, hi], spread=spread,
               class_mixing_cross=cross, class_mixing_same_min=same,
               data_MZ=dict(ms_mb=0.019, md_ms=0.053, Vus=0.225, Vcb=0.041, Vub=0.0037))
    sm = spread["spread_median"]
    res["checks"] = {k: bool(v) for k, v in dict(
        forty_points=npts == 40,
        invariant_universal=nconf > 1000 and hi - lo < 0.01,
        spread_phase_anarchic=all(abs(sm[k] - 1 / np.sqrt(3)) < 0.1 for k in ("Vus", "Vcb", "Vub")) and sm["ms_mb"] > 0.3,
        class_selection_exact=cross < 1e-12 and same > 1e-3,
        up_fit_reproduced=abs(spread["up_ratios"][0] - 3.6e-3) < 2e-5 and abs(spread["up_ratios"][1] - 1.7e-3) < 2e-5,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
