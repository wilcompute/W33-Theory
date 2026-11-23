"""Pass 12728 (Claude track), items 1, 2, 4, 5 (item 3: explore_pass12728_deep.py).
 (1) Low-scale inflation for A (H_I < 1.4e5 GeV, Pass 12727): V^(1/4) = (3 H^2 M_P^2)^(1/4); e-folds N* ~ 57.4 + ln(V^(1/4) / 1e16 GeV)
     + (1/3) ln(T_RH / V^(1/4)) (matter-dominated reheating), T_RH in [1e4 GeV, V^(1/4)]; small-field (hilltop) predictions
     n_s = 1 - (2/N)(p-1)/(p-2) (p = 3, 4, 6, infinity) and plateau-like n_s = 1 - 2/N; against P-ACT-LB n_s = 0.9743 +- 0.0034.
 (2) Sign check of the threshold convention used in Passes 12724-12727: a light colour-triplet pair (b = (0.267, 0, 2)) at M_T < M_G must
     lower the predicted alpha_s (Hisano-Murayama-Yanagida: unification with alpha_s = 0.118 prefers M_T below M_G).
 (4) B''s coupled component: requirements (>= 14-20% of DM, outside mesogenesis, beta ~ 0.3, cold) and the N_eff hint (cold matter cannot
     lower N_eff; no help).
 (5) Timeline forecast: fraction of each completion's parameter space probed by year, from the stated coverages (illustrative).
usage: py -3 analysis/explore_pass12728_round.py"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = {}

# (1)
MP = 2.435e18; H = 1.4e5
V4 = (3 * H * H * MP * MP) ** 0.25
infl = []
for TRH in (1e4, 1e7, V4):
    N = 57.4 + math.log(V4 / 1e16) + math.log(TRH / V4) / 3
    row = dict(T_RH=TRH, N=N)
    for p in (3, 4, 6):
        row[f"hilltop_p{p}"] = 1 - (2 / N) * (p - 1) / (p - 2)
    row["plateau"] = 1 - 2 / N
    row["sigma_from_ACT_plateau"] = (0.9743 - row["plateau"]) / 0.0034
    infl.append(row)
    print(f"(1) V^1/4 = {V4:.1e} GeV, T_RH = {TRH:.0e}: N* = {N:.1f}; n_s: hilltop p=3 {row['hilltop_p3']:.4f}, p=4 {row['hilltop_p4']:.4f}, "
          f"p=6 {row['hilltop_p6']:.4f}, plateau {row['plateau']:.4f} ({row['sigma_from_ACT_plateau']:.1f} sigma below ACT 0.9743)")
eta_needed = (1 - 0.9743) / 2
print(f"(1) a quadratic hilltop (n_s = 1 - 2|eta|) fits ACT with |eta| = {eta_needed:.4f}, at the cost of one tuned parameter")
res["inflation"] = dict(V14=V4, rows=infl, quadratic_hilltop_eta=eta_needed)

# (2)
b = (0.267, 0.0, 2.0); L = math.log(10)
d = [x * L / (2 * math.pi) for x in b]
D = d[2] - d[0] + 12 / 7 * (d[0] - d[1])
res["sign_check"] = dict(triplet_at_MG_over_10_shift_alpha3_inv=D, consistent=D > 0)
print(f"(2) a triplet pair at M_G/10 shifts the predicted alpha_3^-1 by {D:+.2f} (> 0: alpha_s lowered), as Hisano-Murayama-Yanagida require: "
      f"the convention is right; the disagreement with Hall-Nomura's orbifold improvement remains (matter placement / brane terms)")

# (4)
res["coupled_component"] = dict(requirements=["cold (non-relativistic by z ~ 1e5)", "14-20% of DM or more", "outside the mesogenesis sector",
                                               "beta ~ 0.3 to quintessence (fifth force 2 beta^2 f ~ 0.04 within halos)"],
                                candidates=["a pre-inflation axion-like field with a field-dependent decay constant", "a heavy dark-dimension KK mode with a "
                                            "brane coupling to the radion-independent quintessence"],
                                neff="cold matter cannot lower N_eff: the -2 sigma low-N_eff hint is not addressed")
print("(4) coupled component: cold, >= 14-20% of DM, outside mesogenesis, beta ~ 0.3; cannot lower N_eff (the hint stays unexplained)")

# (5)
years = [2027, 2030, 2032, 2035, 2041, 2042, 2045, 2058, 2075]
cov = {}
for y in years:
    A = 0.0 if y < 2030 else (math.log(80 / 40) / math.log(1550 / 34) if y < 2035 else (math.log(400 / 40) / math.log(1550 / 34) if y < 2045 else 0.96))
    belle = 0.0 if y < 2032 else (0.44 if y < 2042 else 0.75)
    lhc = 0.11 if y >= 2041 else 0.0
    Bp = 1 - (1 - belle) * (1 - lhc)
    hyb = lhc
    if y >= 2075: Bp = hyb = 1.0
    if y >= 2058: A = max(A, A)
    cov[y] = dict(A=A, Bprime=Bp, hybrid=hyb)
    print(f"(5) {y}: fraction of parameter space probed - A {A:.0%}, B' {Bp:.0%}, hybrid {hyb:.0%}" + ("; FCC-ee settles vacuum stability for all three" if y == 2058 else ""))
res["timeline"] = dict(coverage=cov, assumptions="A: m_a log-uniform 34-1550 ueV; ALPHA I 40-80 ueV (2028-30), MADMAX/ALPHA II to ~400 ueV by 2035, broadband to "
                                               "~1.5 meV by 2045. B': Belle II 10 ab^-1 (2032) 26-61%, 50 ab^-1 (2042) 62-89%; HL-LHC VLQ to 2 TeV (2041) on M_VL "
                                               "log-uniform 1.74-6 TeV. Hybrid: HL-LHC only until FCC-hh (~2075), which probes y' and M_VL fully.")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12728_round.json"), "w"), indent=1)
