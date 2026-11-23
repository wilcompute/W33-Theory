"""Pass 12730 (Claude track), items 1, 2, 3, 5 (item 4: explore_pass12730_alloc_qat.py).
 (1) Orbifold sign mapping for the hybrid: mismatch delta = alpha_3^-1(meas) - alpha_3^-1(pred) at one loop (+0.26 at two loops, Pass 12702);
     the localised threshold raises the predicted alpha_3^-1 by Delta = (6/7) ln(Lambda R) / 2pi (Contino-Pilo-Rattazzi-Trincherini), so
     delta_new = 0.26 - Delta; the Lambda R that cancels it and the range with |delta_new| < 0.1.
 (2) Relaxation of A's large PQ field: literature status (parametric resonance restores PQ for large initial amplitude unless the model makes
     resonance ineffective; Kearney-Orlofsky-Pierce 1601.03049, Harigaya-Ibe-Kawasaki-Yanagida 1507.00119, Kofman-Linde-Tkachev).
 (3) N_eff in B': T_RH > 5.96 MeV corresponds to N_eff > 2.98 (Barbieri et al. 2501.01369, BBN+Planck+lensing+DESI); at the window edge
     Delta N_eff ~ -0.06 vs the ACT + helium hint ~ 2.85.
 (5) Prior-art map for the three completions.
usage: py -3 analysis/explore_pass12730_round.py"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = {}
c = 6 / 7 / (2 * math.pi)
rows = []
for LR in (3, 5, 6.7, 10, 15, 30, 64, 100):
    D = c * math.log(LR); rows.append(dict(Lambda_R=LR, Delta=D, delta_new=0.26 - D))
    print(f"(1) Lambda R = {LR}: orbifold threshold +{D:.2f} -> hybrid mismatch {0.26 - D:+.2f}")
LR0 = math.exp(0.26 / c); lo = math.exp(0.16 / c); hi = math.exp(0.36 / c)
print(f"(1) exact cancellation at Lambda R = {LR0:.1f}; |mismatch| < 0.1 for Lambda R = {lo:.1f}-{hi:.1f}; protection needs M_* R >= 9.8 (compatible near 10-15)")
res["orbifold_mapping"] = dict(rows=rows, cancel_at=LR0, window_0p1=[lo, hi])
res["pq_relaxation"] = dict(status="model-dependent: generic large-amplitude PQ oscillations restore the symmetry by parametric resonance (returning to the "
                                   "post-inflation regime where the axion is 19% of DM); models with ineffective resonance (e.g. Harigaya-Ibe-Kawasaki-Yanagida) "
                                   "or enhanced explicit breaking (Kearney-Orlofsky-Pierce) are needed")
print("(2) A's large-f_I escape needs a model where parametric resonance is ineffective; otherwise PQ is restored and the 19%-of-DM problem returns")
res["neff"] = dict(bound="T_RH > 5.96 MeV <-> N_eff > 2.98 (2501.01369)", delta_neff_edge=-0.06, hint=2.85,
                   verdict="B' at its window edge lowers N_eff by only ~0.06; it does not explain the hint (corrects Pass 12729's 2.9-3.0)")
print("(3) B' edge: N_eff ~ 2.98 (Delta -0.06): not the hint (2.85); corrects Pass 12729")
res["prior_art"] = {
    "A": ["Redi-Strumia, Axion-Higgs unification (1208.6013): f_a ~ 1e11 from the quartic zero"],
    "hybrid": ["Ibanez-Valenzuela (1301.5167, 1403.6081): high-scale SUSY with tan beta ~ 1 at 1e10-1e13 GeV fits m_h",
               "Heavy higgsino DM at the vanishing-quartic scale (2609.28740)", "Hall-Harigaya Higgs parity: quartic zero = new-physics scale (1803.08119)",
               "Tavartkiladze (1803.11164): pseudo-Goldstone Higgs in SO(10) (template for the Q+U mechanism)"],
    "B_prime": ["no paper combining dark dimension + vectorlike top partner + species-scale quartic zero found",
                "no paper combining B-mesogenesis with the dark dimension found"],
    "universal": ["y' floor: only upper bounds on VLQ Yukawas found in the stability literature (PRD 107 036018, 1812.11303)"]}
print("(5) prior art recorded: A (Redi-Strumia), hybrid base (Ibanez-Valenzuela, Hall-Harigaya, 2609.28740), B' and the y' floor appear new")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12730_round.json"), "w"), indent=1)
