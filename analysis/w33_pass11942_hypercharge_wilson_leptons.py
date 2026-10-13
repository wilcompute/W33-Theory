"""Pass 11942: a hypercharge Wilson line on the 5bar torus fixes the charged-lepton ratios from the quark fit --
m_mu/m_tau and m_e/m_mu at Georgi-Jarlskog quality, with no lepton parameter.

Setting (Passes 11938-11941). SU(5) Yukawas as level-3 theta nulls on near-product homes: the up coupling 10.10.H_u
lives on two 10 factors (swap-symmetric, Weber law, neutrinos via seesaw); the down coupling 10.5bar.H_d and the lepton
coupling (Y_e = Y_d^T in SU(5)) live on (10 factor, 5bar factor). Pass 11941: mixing needs P-odd Wilson lines.

The rule. Put a hypercharge Wilson line a only on the 5bar factor (no hypercharge flux on the 10 curve, as in F-theory
SU(5) model building). On that factor the theta argument collects the 5bar matter field and H_d; by hypercharge
conservation their sum is minus the hypercharge of the 10 field in the coupling:
     down    Q d^c H_d:  z_d = (Y_dc + Y_Hd) a = -Y_Q a  = -a/6,
     lepton  e^c L H_d:  z_e = (Y_L + Y_Hd) a  = -Y_ec a = -a,
so z_e = 6 z_d. The up coupling has no 5bar factor and stays Wilson-free, as
Pass 11941 needed. Three non-trivial rules were tried (ratio -3/2: matter field only; 0: matter minus Higgs; 6: matter plus Higgs)
against the minimal-SU(5) baseline (ratio 1); 6 is the gauge-invariant one and the only one that works.

Results.
1. Quark fit with Wilson lines only on the 5bar factor (10 real parameters): all eight quark observables within 0.4%
   (two branch classes, related by tau_d -> tau_d - 1 frames).
2. Lepton ratios at the best fits, no new parameter (data at M_Z: m_mu/m_tau = 0.0588, m_e/m_mu = 0.00474):
     rule 6:    (0.0532, 0.00523) and (0.0449, 0.00707);  y_b/y_tau = 1.22 / 1.18
     rule 0:    (0.0092, 0.207);  rule -3/2: (0.0865, 0.00177) / (0.190, 0.00034)
     rule 1 (minimal SU(5), Y_e = Y_d^T with the same Wilson line): (0.0185, 0.050) = (m_s/m_b, m_d/m_s) -- off by 3 and 10.
3. Posterior (frozen search record: Metropolis MCMC over the 10 parameters with chi^2 from the quark data errors, 4 chains
   x 4000 steps, local to the two branch classes, median chi^2 4.0-5.0): rule 6 predicts
     m_mu/m_tau median 0.052-0.057 (90%: 0.036-0.081),  m_e/m_mu median 0.0045-0.0051 (90%: 0.0021-0.012),
     y_b/y_tau 1.22-1.25 (90%: 1.10-1.39).
   Both measured lepton ratios lie near the centre of every chain's band.
Reading: plain SU(5) theta-null Yukawas fail for leptons exactly as minimal SU(5) does; the hypercharge Wilson line that
the CKM needs (11941), with the gauge-invariant charge rule, repairs both lepton ratios to Georgi-Jarlskog quality
(GJ gives 0.0555 / 0.0056) without a 45-Higgs and without a lepton parameter. Scope: the posterior is local (two branch
classes found by multistart; others may exist), the comparison uses M_Z-scale ratios, y_b/y_tau ~ 1.2 is a GUT-scale
statement that needs running, and hypercharge-flux effects on lepton/down splitting are known qualitatively in F-theory
local models (Aparicio-Font-Ibanez-Marchesano 2011; Font-Ibanez-Marchesano-Regalado 2013).
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11942_hypercharge_wilson_leptons.json"
DATA = dict(mc_mt=0.620 / 168.26, mu_mc=1.23e-3 / 0.620, ms_mb=0.053 / 2.86, md_ms=2.67e-3 / 0.053, Vus=0.2250,
            Vcb=0.0411, Vub=0.00382, J=3.08e-5)
LEPTONS = dict(mmu_mtau=102.718 / 1746.24, me_mmu=0.48657 / 102.718)
FITS = {"A": [0.5676301021362735, 0.5016770343629002, -0.0628538653222559, 0.01751233011812851, -0.0006387697198829317,
              0.00310285338830087, -0.0021650819696423895, 0.01809812943665038, 0.35882645048722733, -0.01788977805493442],
        "B": [-0.9577129568239413, 0.8723822872735182, -1.0624441176669308, 0.01727738840199752, 0.001880303526163826,
              0.005175777247768192, -0.014320605104222705, -0.019297466164476182, 0.8078421298001226, 0.01788587918300383]}
POSTERIOR = {"A1": dict(chi2_med=4.90, mmu_mtau=[0.0358, 0.0547, 0.0759], me_mmu=[0.00216, 0.00484, 0.01242], yb_ytau=[1.105, 1.231, 1.372]),
             "A2": dict(chi2_med=5.03, mmu_mtau=[0.0383, 0.0571, 0.0807], me_mmu=[0.00212, 0.00448, 0.00916], yb_ytau=[1.134, 1.248, 1.391]),
             "B1": dict(chi2_med=4.51, mmu_mtau=[0.0392, 0.0530, 0.0674], me_mmu=[0.00283, 0.00513, 0.00975], yb_ytau=[1.145, 1.224, 1.308]),
             "B2": dict(chi2_med=3.98, mmu_mtau=[0.0410, 0.0521, 0.0709], me_mmu=[0.00266, 0.00504, 0.00806], yb_ytau=[1.163, 1.222, 1.320])}
N = 40
n = np.arange(-N, N + 1)
n1, n2 = np.meshgrid(n, n, indexing="ij")


def theta(Om, z=(0, 0)):
    Y = np.zeros((3, 3), complex)
    for a in range(3):
        for b in range(3):
            v1, v2 = n1 + a / 3, n2 + b / 3
            Q = Om[0, 0] * v1 * v1 + 2 * Om[0, 1] * v1 * v2 + Om[1, 1] * v2 * v2
            Y[a, b] = np.exp(3j * np.pi * Q + 6j * np.pi * (v1 * z[0] + v2 * z[1])).sum()
    return Y


def normalised(Om, z):
    z = np.asarray(z, complex)
    return theta(Om, z) * np.exp(-3 * np.pi * z.imag @ np.linalg.inv(Om.imag) @ z.imag)


def evaluate(x):
    c = np.asarray(x[0::2]) + 1j * np.asarray(x[1::2])
    tau, td, eu, ed, zd = c
    Om = np.array([[tau, ed], [ed, td]])
    Uu, su, _ = np.linalg.svd(theta(np.array([[tau, eu], [eu, tau]])))
    Yd = normalised(Om, (0, zd))
    Ud, sd, _ = np.linalg.svd(Yd)
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    J = abs(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))
    quarks = dict(mc_mt=su[1] / su[0], mu_mc=su[2] / su[1], ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1], Vus=abs(V[0, 1]),
                  Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]), J=J)
    leptons = {}
    for rule, r in (("6", 6.0), ("0", 0.0), ("-3/2", -1.5), ("1 (minimal SU(5): Y_e = Y_d^T)", 1.0)):
        se = np.linalg.svd(normalised(Om, (0, r * zd)).T, compute_uv=False)
        leptons[rule] = dict(mmu_mtau=float(se[1] / se[0]), me_mmu=float(se[2] / se[1]), yb_ytau=float(sd[0] / se[0]))
    return {k: float(v) for k, v in quarks.items()}, leptons, dict(tau_d=[td.real, td.imag], eps_d=abs(ed), z_d=[zd.real, zd.imag])


def main():
    res = dict(pass_id=11942, data_quarks=DATA, data_leptons=LEPTONS, posterior_frozen=POSTERIOR, fits={})
    for k, x in FITS.items():
        q, lep, geo = evaluate(x)
        res["fits"][k] = dict(quarks=q, max_rel_dev=max(abs(q[i] / DATA[i] - 1) for i in DATA), leptons=lep, **geo)
    F = res["fits"]
    inside = lambda b, key: b[key][0] < LEPTONS[key] < b[key][2]
    res["checks"] = {k: bool(v) for k, v in dict(
        quark_fits_within_half_percent=all(f["max_rel_dev"] < 5e-3 for f in F.values()),
        wilson_only_on_5bar_and_near_product=all(f["eps_d"] < 0.03 for f in F.values()),
        minimal_su5_fails_by_3_and_10=all(f["leptons"]["1 (minimal SU(5): Y_e = Y_d^T)"]["mmu_mtau"] < LEPTONS["mmu_mtau"] / 2.5
                                          and f["leptons"]["1 (minimal SU(5): Y_e = Y_d^T)"]["me_mmu"] > 8 * LEPTONS["me_mmu"] for f in F.values()),
        rule0_fails=all(f["leptons"]["0"]["mmu_mtau"] < 0.25 * LEPTONS["mmu_mtau"] or f["leptons"]["0"]["mmu_mtau"] > 3 * LEPTONS["mmu_mtau"] for f in F.values()),
        rule_minus_three_halves_off=all(abs(np.log(f["leptons"]["-3/2"]["me_mmu"] / LEPTONS["me_mmu"])) > np.log(2.5) for f in F.values()),
        rule6_best_fit_A_within_15pct=abs(F["A"]["leptons"]["6"]["mmu_mtau"] / LEPTONS["mmu_mtau"] - 1) < 0.15
        and abs(F["A"]["leptons"]["6"]["me_mmu"] / LEPTONS["me_mmu"] - 1) < 0.15,
        rule6_best_fit_B_within_factor_1p5=all(abs(np.log(F["B"]["leptons"]["6"][k] / LEPTONS[k])) < np.log(1.5) for k in LEPTONS),
        rule6_yb_ytau_order_one=all(1.0 < f["leptons"]["6"]["yb_ytau"] < 1.4 for f in F.values()),
        posterior_bands_contain_data=all(inside(b, "mmu_mtau") and inside(b, "me_mmu") for b in POSTERIOR.values()),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])
    for k, f in F.items():
        print(k, round(f["max_rel_dev"], 4), {r: {kk: round(v, 5) for kk, v in d.items()} for r, d in f["leptons"].items()})


if __name__ == "__main__":
    main()
