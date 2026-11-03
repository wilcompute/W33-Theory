"""The top-mass tension with Buttazzo's NNLO fit (arXiv:1307.3536 eq. 61, three-loop running, so not my two-loop code): lambda(M_Pl) = -0.0143 - 0.0066 (M_t - 173.34) + 0.0018 (a3 - 0.1184)/0.0007 + 0.0029 (M_h - 125.15).  Solve lambda(M_Pl) = 0 for M_t and propagate errors, then compare with three measurements of different standing: the direct LHC Run 1 combination (a Monte Carlo mass), a preliminary cross-section pole-mass combination, and PDG-style.
The theory error on lambda(M_Pl) is taken from the paper's weak-scale +-0.0003 in lambda and +-0.0005 in y_t.  This is a rough budget, and it is labelled as such.  usage: py -3 nnlo_top.py"""
import json
import math

MH, DMH = 125.20, 0.11
A3, DA3 = 0.1180, 0.0009
D_LAM_TH = 0.0003 * (0.0029 / 0.00206)                 # lambda(M_t) theory error, carried by the ratio of slopes
D_YT_TH = 0.0005 / 0.00556                             # as an equivalent M_t error
lam = lambda mt, mh=MH, a3=A3: -0.0143 - 0.0066 * (mt - 173.34) + 0.0018 * (a3 - 0.1184) / 0.0007 + 0.0029 * (mh - 125.15)
mt0 = 173.34 + (-0.0143 + 0.0018 * (A3 - 0.1184) / 0.0007 + 0.0029 * (MH - 125.15)) / 0.0066
err = dict(alpha_s=0.0018 * DA3 / 0.0007 / 0.0066, higgs=0.0029 * DMH / 0.0066, lambda_theory=D_LAM_TH / 0.0066, yt_theory=D_YT_TH)
tot = math.sqrt(sum(v * v for v in err.values()))
meas = dict(direct_run1_combination=(172.52, 0.33, "Monte Carlo mass, not pole; a further interpretation ambiguity applies"),
            direct_with_0p5_interpretation=(172.52, math.hypot(0.33, 0.5), "with the usually quoted 0.5 GeV"),
            preliminary_pole_combination=(172.25, 0.95, "version-1 talk, Nov 2025, not final"))
out = dict(Mt_for_lambda_MPl_zero=mt0, error_budget=err, error_total=tot, lambda_MPl_at_172p52=lam(172.52), comparisons={})
for k, (m, e, note) in meas.items():
    out["comparisons"][k] = dict(measured=m, error=e, pull_sigma=(m - mt0) / math.hypot(e, tot), note=note)
# how the scale matters: reduced Planck mass via the two-loop slope of my code would shift this; quoted only as the 2-loop criticality scan
print(json.dumps(out, indent=0))
json.dump(out, open("nnlo_top.json", "w"), indent=1)
