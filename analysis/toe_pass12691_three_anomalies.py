"""Pass 12691: three directions from a literature sweep, each reduced to a self-contained computation.
 (A) Electron g-2 vs the fine-structure constant.  a_e^SM(alpha) = sum_n C_n (alpha/pi)^n + a_had + a_weak, with the universal QED
     coefficients C1 = 1/2, C2 = -0.328478965579 (+ mu,tau 5.197e-7, 1.84e-9), C3 = 1.181241456587 (+ mass-dep. -7.38e-6),
     C4 = -1.912245764926 (+ 0.0028), C5 = 6.737(159) (AKN 2019) or 5.891(61) (Volkov 2024 tenth-order discrepancy);
     a_had = 1.693(12)e-12, a_weak = 0.0303e-12.  Measurement (Fan et al. 2023) a_e = 0.00115965218059(13).
     alpha^-1: Cs (Parker 2018) 137.035999046(27); Rb (Morel 2020) 137.035999206(11).  Outputs Delta a_e for each alpha, the alpha
     implied by a_e, and how much the C5 dispute matters.
 (B) KM3-230213A (220 PeV) vs IceCube non-detection: for a steady isotropic flux with exposure ratio r (IceCube/KM3NeT), the chance the
     single event lands in KM3NeT is p = 1/(1+r); r = 15 (Palmisano et al.) gives p; inverting, the r implied by the quoted 2.5-3.1 sigma.
 (C) Neutron lifetime: beam 888.1 +- 2.0 vs bottle 877.8 +- 0.3; the SM relation tau_n (1 + 3 g_A^2) = 5172.0 +- 1.1 s
     (Czarnecki-Marciano-Sirlin) with g_A from PERKEO III 1.27641(56) and the PDG average 1.2754(13); J-PARC electron-counting beam
     877.2 +4.3/-4.0 (2025 talk).  Which method does g_A back, and what dark-decay branching would the beam value need?
usage: py -3 analysis/toe_pass12691_three_anomalies.py"""
import json, math, os
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
# ---------------- (A)
C = [0.5, -0.328478965579 + 5.197e-7 + 1.84e-9, 1.181241456587 - 7.38e-6, -1.912245764926 + 0.0028]
C5 = {"AKN 2019": (6.737, 0.159), "Volkov 2024": (5.891, 0.061)}
A_HAD, A_HAD_E, A_W = 1.693e-12, 0.012e-12, 0.0303e-12
AE, AE_E = 0.00115965218059, 0.00000000000013
ALPHAS = {"Cs 2018": (137.035999046, 0.000000027), "Rb 2020": (137.035999206, 0.000000011)}
def ae_sm(ainv, c5):
    x = 1 / ainv / math.pi
    return sum(c * x ** (n + 1) for n, c in enumerate(C)) + c5 * x ** 5 + A_HAD + A_W
def dae_dainv(ainv, c5):
    h = 1e-9; return (ae_sm(ainv + h, c5) - ae_sm(ainv - h, c5)) / (2 * h)
A = {}
for c5lab, (c5, c5e) in C5.items():
    for alab, (ainv, aerr) in ALPHAS.items():
        th = ae_sm(ainv, c5); slope = dae_dainv(ainv, c5)
        th_err = math.sqrt((slope * aerr) ** 2 + A_HAD_E ** 2 + (c5e * (1 / ainv / math.pi) ** 5) ** 2)
        d = AE - th; s = math.hypot(th_err, AE_E)
        A[f"{alab} | C5 {c5lab}"] = dict(a_e_SM=th, delta_1e14=d * 1e14, sigma_1e14=s * 1e14, pull=d / s)
        print(f"(A) alpha {alab}, C5 {c5lab}: Delta a_e = {d * 1e14:+.1f} +- {s * 1e14:.1f} (x1e-14), pull {d / s:+.2f}")
    # alpha implied by a_e
    from scipy.optimize import brentq
    ainv = brentq(lambda a: ae_sm(a, c5) - AE, 137.0359, 137.0361)
    slope = dae_dainv(ainv, c5)
    err = math.sqrt(AE_E ** 2 + A_HAD_E ** 2 + (c5e * (1 / ainv / math.pi) ** 5) ** 2) / abs(slope)
    A[f"alpha from a_e | C5 {c5lab}"] = dict(alpha_inv=ainv, err=err, pull_vs_Cs=(ainv - 137.035999046) / math.hypot(err, 2.7e-8),
                                              pull_vs_Rb=(ainv - 137.035999206) / math.hypot(err, 1.1e-8))
    print(f"(A) alpha^-1 from a_e (C5 {c5lab}) = {ainv:.9f} +- {err:.9f}; vs Cs {A[f'alpha from a_e | C5 {c5lab}']['pull_vs_Cs']:+.2f} sigma, vs Rb {A[f'alpha from a_e | C5 {c5lab}']['pull_vs_Rb']:+.2f} sigma")
A["Cs_vs_Rb_sigma"] = (137.035999206 - 137.035999046) / math.hypot(2.7e-8, 1.1e-8)
print(f"(A) Cs vs Rb: {A['Cs_vs_Rb_sigma']:.2f} sigma")
res["electron_g2_alpha"] = A
# ---------------- (B)
B = {}
for r in (15.0, 30.0, 70.0):
    p = 1 / (1 + r); B[f"r={r:g}"] = dict(p=p, sigma_one_sided=norm.isf(p))
    print(f"(B) exposure ratio r = {r:g}: p(event lands in KM3NeT) = {p:.4f} -> {norm.isf(p):.2f} sigma (one-sided)")
for s in (2.5, 3.1):
    p = norm.sf(s); B[f"implied r for {s} sigma"] = 1 / p - 1
    print(f"(B) quoted {s} sigma corresponds to an effective exposure ratio r ~ {1 / p - 1:.0f}")
res["km3net"] = dict(rows=B, note="counting alone with IceCube's 15x exposure gives ~1.5 sigma; the quoted 2.5-3.1 sigma needs IceCube's spectral/EHE "
                                  "non-detections over a wider energy range (effective r ~ 160-1000) or Auger, i.e. depends on the flux shape")
# ---------------- (C)
Cn = {}
beam, sbeam, bottle, sbottle = 888.1, 2.0, 877.8, 0.3
Cn["beam_vs_bottle_sigma"] = (beam - bottle) / math.hypot(sbeam, sbottle)
for lab, (gA, sgA) in {"PERKEO III": (1.27641, 0.00056), "PDG average": (1.2754, 0.0013)}.items():
    t = 5172.0 / (1 + 3 * gA ** 2); st = math.hypot(1.1 / (1 + 3 * gA ** 2), 5172.0 * 6 * gA * sgA / (1 + 3 * gA ** 2) ** 2)
    Cn[f"tau_SM from g_A ({lab})"] = dict(tau=t, err=st, pull_vs_bottle=(t - bottle) / math.hypot(st, sbottle), pull_vs_beam=(t - beam) / math.hypot(st, sbeam))
    print(f"(C) g_A {lab} = {gA}: tau_SM = {t:.1f} +- {st:.1f} s; vs bottle {(t - bottle) / math.hypot(st, sbottle):+.2f} sigma, vs beam {(t - beam) / math.hypot(st, sbeam):+.2f} sigma")
jp, sjp = 877.2, 4.15
Cn["J-PARC electron counting"] = dict(tau=jp, pull_vs_bottle=(jp - bottle) / math.hypot(sjp, sbottle), pull_vs_beam=(jp - beam) / math.hypot(sjp, sbeam))
Cn["dark_branching_needed"] = 1 - bottle / beam
print(f"(C) beam vs bottle {Cn['beam_vs_bottle_sigma']:.2f} sigma; J-PARC e-counting vs beam {Cn['J-PARC electron counting']['pull_vs_beam']:+.2f} sigma; "
      f"dark branching needed for the beam value {Cn['dark_branching_needed'] * 100:.2f}%")
res["neutron_lifetime"] = Cn
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12691_three_anomalies.json"), "w"), indent=1)
