"""Pass 12622 producer (claude track): DES-SN5YR replication of the Pass 12620 posterior-predictive cross-validation.
Reads analysis/toe_uv/class_ppd_{dovekie,desy5}_{sn,bao}.json and class_holdout_desy5_bao_neutral.json; writes data/w33_pass12622_desy5_ppd.json.
usage: py -3 analysis/w33_pass12622_desy5_ppd.py"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UV = os.path.join(ROOT, "analysis", "toe_uv")


def L(n):
    return json.load(open(os.path.join(UV, n), encoding="utf-8"))


tot = {}
for ds in ("dovekie", "desy5"):
    sn, bao = L(f"class_ppd_{ds}_sn.json")["rows"], L(f"class_ppd_{ds}_bao.json")["rows"]
    tot[ds] = {m: sn[f"{m}_infl1"]["elpd"] + bao[f"{m}_infl1"]["elpd"] for m in ("LCDM", "free_neg", "cpl", "exp")}
gain = {ds: {m: v - t["LCDM"] for m, v in t.items() if m != "LCDM"} for ds, t in tot.items()}
best = {ds: max(g, key=g.get) for ds, g in gain.items()}
rows = sorted(L("class_holdout_desy5_bao_neutral.json")["rows"]["free_neg"], key=lambda r: r["train_chi2"])
bimodal = rows[1]["train_chi2"] - rows[0]["train_chi2"] < 1.0 and abs(rows[1]["p"]["cp"] - rows[0]["p"]["cp"]) > 0.02
drops = {f"{ds}_{h}_{k}": 40 - v["n"] if ds == "desy5" else 24 - v["n"] for ds in ("dovekie", "desy5") for h in ("sn", "bao") for k, v in L(f"class_ppd_{ds}_{h}.json")["rows"].items()}
checks = dict(
    every_evolving_model_beats_lcdm_on_both_compilations=all(v > 2 for g in gain.values() for v in g.values()),
    best_model_differs_between_compilations=best["dovekie"] != best["desy5"],
    desy5_sn_held_all_evolving_beat_lcdm=all(L("class_ppd_desy5_sn.json")["rows"][f"{m}_infl1"]["elpd"] > L("class_ppd_desy5_sn.json")["rows"]["LCDM_infl1"]["elpd"] + 3 for m in ("free_neg", "cpl", "exp")),
    desy5_fading_bao_training_bimodal=bimodal,
)
out = dict(pass_number=12622, track="claude", total_elpd_infl1=tot, gain_over_lcdm=gain, best_model=best, fading_bao_two_lowest_training=rows[:2], failed_draws=drops, checks=checks, all_checks_pass=all(checks.values()))
json.dump(out, open(os.path.join(ROOT, "data", "w33_pass12622_desy5_ppd.json"), "w"), indent=1, default=float)
print(json.dumps(dict(gain=gain, best=best, checks=checks), indent=1, default=float))
print("all_checks_pass", out["all_checks_pass"])
