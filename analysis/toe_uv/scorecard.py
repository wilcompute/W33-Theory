"""One table of every out-of-sample and cross-probe number per dark-energy model (Passes 12597-12626), regenerated from the JSONs so it can be refreshed when a run lands.
Rows: LCDM, fading c<0 (free_neg), fading c>0 (free_pos), CPL, thawing exponential.
Columns: full-data chi2 gain over LCDM (Dovekie, class_fit_dovekie: plik-lite + tau + DESI + SN; no lensing/fs8), out-of-sample elpd gain (Dovekie, DES-SN5YR; prior-truncated rows where they exist), BAO pull on n_s in sigma (Pass 12623), DES Y3 shear at fixed background (Pass 12625 addendum), DR3 BAO Asimov distinguishability from LCDM (Pass 12625; upper bound), MCMC held-BAO elpd and joint CPL+DES refit when present.
usage: py -3 scorecard.py   (writes scorecard.json and scorecard.md)"""
import json
import os

J = lambda n: json.load(open(n)) if os.path.exists(n) else None  # noqa: E731
fit = J("class_fit_dovekie.json")
nsf = J("ns_fisher.json")
sd = J("sign_des.json")
fc = J("dr3_forecast.json")
mc = J("mcmc_desy5_bao_free_neg.json")
dj = J("des_joint_cpl.json")
sp = J("shear_ppd.json")
spk = J("shear_ppd_kids_dovekie.json")
desj = J("class_des_dovekie_joint.json")


def ppd(ds, hold, m):
    for suf in ("_trunc", ""):
        d = J(f"class_ppd_{ds}_{hold}{suf}.json")
        if d and f"{m}_infl1" in d["rows"]:
            return d["rows"][f"{m}_infl1"]["elpd"], suf == "_trunc"
    return None, False


rows = {}
MAP = dict(LCDM="LCDM", fading_cneg="free_neg", fading_cpos="free_pos", CPL="CPL", exp="exp_neg", KLT=None)
PPDM = dict(LCDM="LCDM", fading_cneg="free_neg", CPL="cpl", exp="exp", KLT="klt25")
NSM = dict(LCDM="LCDM", fading_cneg="free_neg", CPL="cpl", exp="exp")
for lab, key in MAP.items():
    r = dict(full_chi2_gain=(fit["LCDM"]["chi2"] - fit[key]["chi2"]) if key else None)
    for ds in ("dovekie", "desy5"):
        if lab in PPDM:
            a, ta = ppd(ds, "sn", PPDM[lab])
            b, tb = ppd(ds, "bao", PPDM[lab])
            l1, _ = ppd(ds, "sn", "LCDM")
            l2, _ = ppd(ds, "bao", "LCDM")
            r[f"oos_gain_{ds}"] = (a + b) - (l1 + l2) if None not in (a, b) else None
            r[f"oos_truncated_{ds}"] = ta or tb
    if lab in NSM and nsf:
        r["ns_bao_pull_sigma"] = nsf["pull_significance"][NSM[lab]]["significance"]
    sk = dict(LCDM="LCDM", fading_cneg="free_neg", fading_cpos="free_pos", CPL="CPL").get(lab)
    if sd and sk:
        r["des_shear_fixed_bg_rel_lcdm"] = (sd[sk]["des"] + sd[sk]["desp"]) - (sd["LCDM"]["des"] + sd["LCDM"]["desp"])
    fk = dict(fading_cneg="free_neg", fading_cpos="free_pos", CPL="CPL").get(lab)
    if fc and fk:
        r["dr3_bao_vs_lcdm_dovekie"] = fc["dovekie_DR3_sqrt35"][f"LCDM_vs_{fk}"]
    rows[lab] = r
if desj:
    for lab, k in (("LCDM", "LCDM"), ("fading_cneg", "free_neg"), ("exp", "exp")):
        if k in desj["rows"]:
            rows[lab]["joint_des_chi2_gain"] = desj["rows"]["LCDM"]["chi2"] - desj["rows"][k]["chi2"]
    if dj:
        rows["CPL"]["joint_des_chi2_gain"] = desj["rows"]["LCDM"]["chi2"] - dj["chi2"]
if sp:
    for lab, k in (("LCDM", "LCDM"), ("fading_cneg", "free_neg"), ("fading_cpos", "free_pos"), ("CPL", "CPL"), ("KLT", "KLT")):
        if k in sp:
            rows[lab]["shear_heldout_elpd_rel_lcdm"] = sp[k]["elpd_shear"] - sp["LCDM"]["elpd_shear"]
    for lab in rows:
        if rows[lab].get("oos_gain_dovekie") is not None and rows[lab].get("shear_heldout_elpd_rel_lcdm") is not None:
            rows[lab]["oos_gain_dovekie_plus_shear"] = rows[lab]["oos_gain_dovekie"] + rows[lab]["shear_heldout_elpd_rel_lcdm"]
if spk:
    for lab, k in (("LCDM", "LCDM"), ("fading_cneg", "free_neg"), ("fading_cpos", "free_pos"), ("CPL", "CPL"), ("KLT", "KLT")):
        if k in spk:
            rows[lab]["shear_heldout_kids_rel_lcdm"] = spk[k]["elpd_shear"] - spk["LCDM"]["elpd_shear"]
    for lab in rows:
        r = rows[lab]
        if None not in (r.get("oos_gain_dovekie_plus_shear"), r.get("shear_heldout_kids_rel_lcdm")):
            r["oos_gain_dovekie_plus_des_kids_shear"] = r["oos_gain_dovekie_plus_shear"] + r["shear_heldout_kids_rel_lcdm"]
if mc:
    rows["fading_cneg"]["mcmc_desy5_bao_elpd"] = mc["elpd_held"]
    rows["fading_cneg"]["mcmc_frac_c_positive"] = mc.get("frac_c_positive")
json.dump(rows, open("scorecard.json", "w"), indent=1)
cols = ["full_chi2_gain", "oos_gain_dovekie", "oos_gain_desy5", "shear_heldout_elpd_rel_lcdm", "shear_heldout_kids_rel_lcdm", "oos_gain_dovekie_plus_shear", "oos_gain_dovekie_plus_des_kids_shear", "ns_bao_pull_sigma", "des_shear_fixed_bg_rel_lcdm", "joint_des_chi2_gain", "dr3_bao_vs_lcdm_dovekie", "mcmc_desy5_bao_elpd"]
md = ["| model | " + " | ".join(cols) + " |", "|---" * (len(cols) + 1) + "|"]
for lab, r in rows.items():
    md.append(f"| {lab} | " + " | ".join("" if r.get(c) is None else f"{r[c]:+.2f}" for c in cols) + " |")
open("scorecard.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print("\n".join(md))
