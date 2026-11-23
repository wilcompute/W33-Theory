"""Pass 12729 (Claude track), items 1-3 (item 4: explore_pass12729_orbifold_fix.json via inline script; item 5: explore_pass12729_alloc.py).
 (1) A with a large PQ field during inflation: the isocurvature amplitude scales as H_I / (2 pi f_I theta), so H_I,max grows by f_I / f_a.
     f_I needed for H_I = 1e10-1e13 GeV (high-scale inflation can fit ACT better: plateau n_s = 1 - 2/N at N ~ 55-60).
 (2) Bayesian update of A with ACT: A's evidence factors vs the SM: m_t (f_a log-uniform over 4 decades -> m_t density 0.25 |d log10 f_a / d m_t|),
     Omega_DM (pre-inflation theta uniform on [0, pi] -> density 1 / (pi Omega dlnOmega/dtheta) vs SM 1/0.3), inflation tuning (quadratic hilltop
     eta within the ACT 1-sigma window, eta log-uniform on [1e-3, 0.1]), trials factor 8; compared with B' (Pass 12709).
 (3) Low reheating and N_eff in B': de Salas et al. (2015): N_eff < 3 only for T_RH <~ 7 MeV; Hasegawa et al. (2019): N_eff ~ 3.046 for T_RH >~ 10 MeV;
     bound T_RH > 5.96 MeV (2501.01369).  B''s window T_RH = 6-17 MeV overlaps the region where N_eff falls slightly below 3.044.
usage: py -3 analysis/explore_pass12729_round.py"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = {}
# (1)
fa, Hmax0 = 2.48e10, 1.4e5
rows = []
for HI in (1e10, 1e11, 1e12, 1e13):
    fI = fa * HI / Hmax0
    rows.append(dict(H_I=HI, f_I_needed=fI, f_I_over_MPl=fI / 2.435e18))
    print(f"(1) H_I = {HI:.0e} GeV needs a PQ field value f_I >= {fI:.1e} GeV ({fI / 2.435e18:.2f} M_Pl) during inflation")
res["large_fI"] = dict(rows=rows, note="f_I ~ M_Pl needed for H_I ~ 1e13; f_I <= 0.1 M_Pl allows H_I <~ 1e12; the PQ field must then relax to f_a without "
                                       "non-thermal symmetry restoration (parametric resonance), else the post-inflation regime returns")
# (2)
width_rows = {}
slope = 1.47
Om_fac = (1 / (math.pi * 0.12 * 9.7)) / (1 / 0.3)
infl = (2 * 0.0034 / 2 / 0.0128) / math.log(100)
for width in (15.0, 5.0, 2.0):
    mt_fac = width * 0.25 * slope
    A = mt_fac * Om_fac * infl
    width_rows[f"{width:g}"] = dict(A=A, A_trials=A / 8, factors=dict(mt=mt_fac, Omega=Om_fac, inflation=infl))
    print(f"(2) SM m_t prior width {width:g} GeV: A Bayes factor {A:.3f} ({A / 8:.4f} after 8 trials); factors m_t {mt_fac:.2f}, Omega {Om_fac:.3f}, inflation {infl:.3f}")
P09 = json.load(open(os.path.join(ROOT, "data", "toe_pass12709_round.json"), encoding="utf-8"))["evidence"]["rows"]
Bp = [P09[f"exp + scheme | width {w}"]["B_prime"] for w in ("15", "5", "2")]
print(f"(2) B' (Pass 12709): {Bp[0]:.3f}, {Bp[1]:.3f}, {Bp[2]:.3f} -> A now ranks below B'")
res["evidence_A"] = dict(rows=width_rows, Bprime=Bp)
# (3)
res["neff_low_reheating"] = dict(window_Bprime_MeV=[5.96, 17], literature={"de Salas 2015": "N_eff < 3 for T_RH <~ 7 MeV", "Hasegawa 2019": "N_eff ~ 3.046 for T_RH >~ 10 MeV"},
                                 estimate="at the lower edge (6-7 MeV) N_eff ~ 2.9-3.0; the hint (ACT + helium ~ 2.85 +- 0.1) needs T_RH ~ 5-6 MeV, at the edge of the "
                                          "5.96 MeV bound itself (which uses the same N_eff physics): B' can at most account for part of the hint, near T_RH ~ 6 MeV")
print("(3) B''s reheating at 6-7 MeV gives N_eff ~ 2.9-3.0 (de Salas 2015; Hasegawa 2019): a partial, edge-of-window account of the low-N_eff hint")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12729_round.json"), "w"), indent=1)
