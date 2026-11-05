"""Pass 12623 producer (claude track): Fisher significance of DESI BAO's pull on n_s, by dark-energy model.
Reads analysis/toe_uv/ns_fisher.json (written by analysis/toe_uv/ns_fisher.py in WSL with the patched CLASS) and writes data/w33_pass12623_ns_fisher.json.
usage: py -3 analysis/w33_pass12623_ns_fisher.py"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "analysis", "toe_uv", "ns_fisher.json"), encoding="utf-8"))
s = d["pull_significance"]
checks = dict(
    all_eight_fits_present=all(f"{m}_without_{h}" in d for m in ("LCDM", "exp", "cpl", "free_neg") for h in ("sn", "bao")),
    sigmas_physical=all(0.002 < d[k]["sigma"] < 0.006 for k in d if k.endswith(("_sn", "_bao"))),
    control_lcdm_pull_nonzero=s["LCDM"]["significance"] > 1.5,
    thawing_exp_pull_nonzero=s["exp"]["significance"] > 1.0,
    crossing_models_pull_vanishes=s["cpl"]["significance"] < 0.3 and s["free_neg"]["significance"] < 0.3,
    lcdm_with_bao_above_0965_by_more_than_1p5_sigma=s["LCDM"]["distance_from_0965_sigma"] > 1.5,
    crossing_models_with_bao_within_1_sigma_of_0965=s["cpl"]["distance_from_0965_sigma"] < 1 and s["free_neg"]["distance_from_0965_sigma"] < 1,
    no_bao_fits_agree_within_half_sigma=max(d[f"{m}_without_bao"]["ns"] for m in ("LCDM", "exp", "cpl", "free_neg")) - min(d[f"{m}_without_bao"]["ns"] for m in ("LCDM", "exp", "cpl", "free_neg")) < 0.002,
)
out = dict(pass_number=12623, track="claude", fits=d, checks=checks, all_checks_pass=all(checks.values()))
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12623_ns_fisher.json"), "w"), indent=1)
for k, v in checks.items():
    print(k, v)
print("all_checks_pass", out["all_checks_pass"])
