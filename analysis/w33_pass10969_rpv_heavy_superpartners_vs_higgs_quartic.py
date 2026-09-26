#!/usr/bin/env python3
"""Pass 10969: harmless R-parity violation needs superpartners above ~1e15 GeV, but the measured
Higgs quartic caps the SUSY scale near 3e10 GeV.

Cross-track join.  The Claude track found (Passes 10960-10967) that in the W(3,3) heterotic class the
Fayet-Iliopoulos term forces a nu^c-type condensate <n>/M_s ~ 0.19-0.39 (cfdc1f2) that regenerates
all three dimension-four R-parity-violating couplings with strength ~ <n>/M_s.  The physics track
(analysis/w33_two_susy_scales.py) holds that supersymmetry is 'structural' with no light
superpartners.  Heavy squarks make R-parity violation harmless: proton decay through lambda'lambda''
scales as 1/m_sq^4.  How heavy, and is that compatible with the Higgs?

1. RPV bound.  p -> e+ pi0 through squark exchange requires |lambda' lambda''| <~ 1e-27 (m_sq/100 GeV)^2
   (Barbier et al., Phys. Rept. 420 (2005) 1, hep-ph/0406039).  With lambda' ~ lambda'' ~ <n>/M_s in
   [0.19, 0.39] this needs m_sq >~ 6e14 - 1.2e15 GeV.
   (Scope: generation structure of the regenerated couplings not computed; a texture suppression of
   the first-generation entries would lower the bound by its square root.)
2. Higgs quartic.  Two-loop SM running (g_Y, g2, g3, y_t, lambda) from the NNLO MSbar matching of
   Buttazzo et al. (arXiv:1307.3536).  Control: lambda(M_Pl) = -0.0150 vs their three-loop fit
   -0.0143 (offset 0.0007, inside their stated theory error); lambda crosses zero at ~5e9 GeV for
   their reference inputs.  With PDG inputs (m_t = 172.57 +- 0.29, m_h = 125.20, alpha_s = 0.1180,
   M_W = 80.369) lambda turns negative at 3.2e10 GeV.
3. MSSM matching at M_S: lambda(M_S) = (g^2 + g_Y^2)/8 cos^2(2 beta) + Delta lambda_stop, with the one-
   loop stop threshold (3 y_t^4 / 8 pi^2) X^2 (1 - X^2/12) >= 0 for X^2 <= 12 (colour/charge-breaking
   safe mixing lies well inside).  So lambda(M_S) >= 0 and M_S <= Lambda_I(m_t).  M_S >= 1e15 GeV
   then requires m_t <= 171.00 GeV: 5.4 sigma below PDG on the experimental error alone (about 2.5-3
   sigma if a +-0.5 GeV pole-mass interpretation uncertainty is added).
4. Audit: analysis/w33_BREAKTHROUGH_475_...py asserts lambda_h(GUT) = 1/40 = +0.025.  The measured
   running gives lambda(1e16 GeV) = -0.0107 (m_t = 172.57); +0.025 is excluded (it would need
   m_t ~ 166 GeV).

Reading: the class cannot be rescued by 'structural' heavy supersymmetry with MSSM matching.  The
two tracks' positions are jointly inconsistent unless m_t is ~1.5 GeV lighter than measured, or
stop mixing is beyond the colour-breaking-safe range, or the high-scale theory is not the MSSM.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass10969_rpv_heavy_superpartners_vs_higgs_quartic.json"
K = 1 / (16 * math.pi ** 2)
PDG = dict(mt=172.57, dmt=0.29, mh=125.20, als=0.1180, mw=80.3692)
N_OVER_MS = (0.19, 0.39)          # cfdc1f2: FI term fixes <n>/M_s
RPV_BOUND = 1e-27                 # |l' l''| < RPV_BOUND * (m_sq / 100 GeV)^2


def beta(t, y):
    gY, g2, g3, yt, lam = y
    gY2, g22, g32, yt2 = gY * gY, g2 * g2, g3 * g3, yt * yt
    b1 = [41 / 6 * gY ** 3, -19 / 6 * g2 ** 3, -7 * g3 ** 3]
    byt = yt * (4.5 * yt2 - 17 / 12 * gY2 - 9 / 4 * g22 - 8 * g32)
    blam = (24 * lam ** 2 - 6 * yt2 ** 2 + 3 / 8 * (2 * g22 ** 2 + (g22 + gY2) ** 2)
            + lam * (12 * yt2 - 9 * g22 - 3 * gY2))
    bij = [[199 / 18, 9 / 2, 44 / 3], [3 / 2, 35 / 6, 12], [11 / 6, 9 / 2, -26]]
    d = [17 / 6, 3 / 2, 2]
    gs = [gY2, g22, g32]
    g = [gY, g2, g3]
    b2 = [g[i] ** 3 * (sum(bij[i][j] * gs[j] for j in range(3)) - d[i] * yt2) for i in range(3)]
    byt2 = yt * (-12 * yt2 ** 2 + yt2 * (131 / 16 * gY2 + 225 / 16 * g22 + 36 * g32 - 12 * lam) + 6 * lam ** 2
                 + 1187 / 216 * gY2 ** 2 - 3 / 4 * gY2 * g22 + 19 / 9 * gY2 * g32 - 23 / 4 * g22 ** 2
                 + 9 * g22 * g32 - 108 * g32 ** 2)
    blam2 = (-312 * lam ** 3 - 144 * lam ** 2 * yt2 - 3 * lam * yt2 ** 2 + 30 * yt2 ** 3 - 32 * g32 * yt2 ** 2
             + 80 * lam * g32 * yt2 + lam ** 2 * (108 * g22 + 36 * gY2) + lam * yt2 * (45 / 2 * g22 + 85 / 6 * gY2)
             - 4 / 3 * gY2 * yt2 ** 2 + lam * (-73 / 8 * g22 ** 2 + 39 / 4 * g22 * gY2 + 629 / 24 * gY2 ** 2)
             + yt2 * (-9 / 4 * g22 ** 2 + 21 / 2 * g22 * gY2 - 19 / 4 * gY2 ** 2)
             + 305 / 16 * g22 ** 3 - 289 / 48 * g22 ** 2 * gY2 - 559 / 48 * g22 * gY2 ** 2 - 379 / 48 * gY2 ** 3)
    return [K * b1[i] + K * K * b2[i] for i in range(3)] + [K * byt + K * K * byt2, K * blam + K * K * blam2]


def initial(mt, mh, als, mw):
    return [0.35830 + 0.00011 * (mt - 173.34) - 0.00020 * (mw - 80.384) / 0.014,
            0.64779 + 0.00004 * (mt - 173.34) + 0.00011 * (mw - 80.384) / 0.014,
            1.1666 + 0.00314 * (als - 0.1184) / 0.0007 - 0.00046 * (mt - 173.34),
            0.93690 + 0.00556 * (mt - 173.34) - 0.00042 * (als - 0.1184) / 0.0007,
            0.12604 + 0.00206 * (mh - 125.15) - 0.00004 * (mt - 173.34)]


def run(mt, mh=PDG["mh"], als=PDG["als"], mw=PDG["mw"]):
    return solve_ivp(beta, (math.log(mt), math.log(1.22e19)), initial(mt, mh, als, mw),
                     dense_output=True, rtol=1e-10, atol=1e-12)


def lam(sol, mu):
    return float(sol.sol(math.log(mu))[4])


def zero(sol, mt):
    ts = np.linspace(math.log(mt), math.log(1.22e19), 4000)
    ls = sol.sol(ts)[4]
    for i in range(1, len(ts)):
        if ls[i - 1] > 0 >= ls[i]:
            a, b = ts[i - 1], ts[i]
            for _ in range(60):
                m = 0.5 * (a + b)
                a, b = (m, b) if sol.sol(m)[4] > 0 else (a, m)
            return math.exp(0.5 * (a + b))
    return None


def mt_needed(target):
    a, b = 165.0, 175.0
    for _ in range(40):
        m = 0.5 * (a + b)
        z = zero(run(m), m)
        a, b = (m, b) if (z is None or z >= target) else (a, m)
    return a


def main():
    ref = run(173.34, 125.15, 0.1184, 80.384)
    control = dict(lambda_MPl_ours=lam(ref, 1.22e19), lambda_MPl_buttazzo_fit=-0.0143,
                   zero_crossing_reference=zero(ref, 173.34))
    assert abs(control["lambda_MPl_ours"] - control["lambda_MPl_buttazzo_fit"]) < 0.002
    s = run(PDG["mt"])
    higgs = dict(zero_crossing_PDG=zero(s, PDG["mt"]), lambda_1e15=lam(s, 1e15), lambda_1e16=lam(s, 1e16),
                 lambda_MPl=lam(s, 1.22e19))
    scan = {f"{m:.2f}": zero(run(m), m) for m in (171.0, 171.5, 172.0, 172.28, 172.57, 172.86, 173.15)}
    need = {f"{T:.0e}": mt_needed(T) for T in (1e11, 1e13, 1e14, 1e15, 1e16)}
    sig = {k: (PDG["mt"] - v) / PDG["dmt"] for k, v in need.items()}
    msq = {f"{x}": 100 * math.sqrt(x * x / RPV_BOUND) for x in N_OVER_MS}
    # BT475 audit: what m_t would lambda(1e16) = +1/40 need?
    a, b = 150.0, 173.0
    for _ in range(40):
        m = 0.5 * (a + b)
        a, b = (m, b) if lam(run(m), 1e16) > 1 / 40 else (a, m)
    audit = dict(claim=1 / 40, measured_lambda_1e16=higgs["lambda_1e16"], mt_needed_for_claim=a)
    out = dict(pass_id=10969, inputs=PDG, rpv_bound=RPV_BOUND, n_over_Ms=N_OVER_MS, control=control, higgs=higgs,
               zero_crossing_scan=scan, mt_needed=need, sigma_below_PDG=sig, m_squark_needed=msq, bt475_audit=audit)
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True))
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
