"""Outside link (Pass 12621): fitted n_s under each dark-energy model, with and without DESI BAO in training.  Reads existing fit files; no new fits.
usage: py -3 ns_by_model.py"""
import json
out = {}
for f in ("class_growth_dovekie_none.json", "class_growth_desy5_none.json", "class_fit_dovekie.json", "class_fit_desy5.json", "class_des_dovekie_joint.json"):
    d = json.load(open(f))
    rows = d.get("rows", d)
    out[f] = {k: rows[k]["p"]["ns"] for k in ("LCDM", "exp", "free_neg", "relax", "CPL") if k in rows and isinstance(rows[k], dict) and "p" in rows[k]}
for h in ("sn", "bao"):
    d = json.load(open(f"class_holdout_dovekie_{h}_neutral.json"))
    out[f"trained_without_{h}"] = {m: min(r, key=lambda r: r["train_chi2"])["p"]["ns"] for m, r in d["rows"].items()}
out["bao_pull"] = {m: out["trained_without_sn"][m] - out["trained_without_bao"][m] for m in out["trained_without_sn"]}
json.dump(out, open("ns_by_model.json", "w"), indent=1)
print(json.dumps(out["bao_pull"]))
