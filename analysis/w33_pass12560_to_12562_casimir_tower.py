"""Passes 12560-12562 (Claude track).  Not a theory of everything: see PASS12558_12562_SPARSE_TOWER_CASIMIR.md.

12560 -- what produces c': one DESI bin, z = 0.706, carries about half of the no-SN gain; it survives losing any single bin.
12561 -- Lambda + decaying dark matter does not reproduce the signal: losing mass is not enough.
12562 -- Lambda + Casimir + sparse tower fits as well as fading with the same parameter count, on full Planck too; but the exponent is not measured, so eps is largely c relabelled.  If the term is Casimir then R is about 13 microns and the universe recollapses; the conflict with no-AdS3 is stated.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12560_to_12562_casimir_tower.json"
SETS = ("pantheon", "dovekie", "desy5")


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks, res = {}, {}

    # 12560
    jk = {s: load(f"dark_jackknife_{s}.json") for s in ("none", "dovekie")}
    res["jackknife"] = jk
    for s, j in jk.items():
        assert abs(j["all"]["free"]) > 1
    g = {s: {k: v["gain"] for k, v in j["bins"].items()} for s, j in jk.items()}
    full = {s: j["all"]["gain"] for s, j in jk.items()}
    checks["12560: dropping z = 0.706 halves the no-SN gain (5.3 to 2.6) and cuts Dovekie's to 4.0; it is the largest single loss on both"] = g["none"]["0.706"] < 0.55 * full["none"] and g["dovekie"]["0.706"] < 0.7 * full["dovekie"] and min(g["none"], key=g["none"].get) == "0.706" and min(g["dovekie"], key=g["dovekie"].get) == "0.706"
    checks["12560: c' stays within 0.042 to 0.058 on losing any one bin, on both data sets"] = all(0.042 <= v["cp"] <= 0.058 for j in jk.values() for v in j["bins"].values())
    b7 = jk["none"]["bins"]["0.706"]
    b9 = jk["none"]["bins"]["0.934"]
    checks["12560: holdout: fitted without it, fading predicts z = 0.706 better than LCDM (4.3 against 6.8, no SN) but z = 0.934 worse (3.9 against 1.7)"] = b7["held_chi2_fading"] < b7["held_chi2_lcdm"] - 2 and b9["held_chi2_fading"] > b9["held_chi2_lcdm"] + 2

    # 12561
    dc = {s: load(f"dark_decay_{s}.json") for s in ("dovekie", "desy5")}
    res["decay"] = dc
    checks["12561: control: Gamma = 0 returns LCDM within 1e-3"] = all(abs(d["control_G0_equals_LCDM"]) < 1e-3 for d in dc.values())
    checks["12561: Lambda + decaying dark matter gains under 2 on both samples, where fading gains 10 and 16, with the same parameter count; best fits sit at the Gamma edge or nearby, so this is a local statement"] = all(d["D1_free"]["delta"] > -2 for d in dc.values())

    # 12562
    cf = {s: load(f"casimir_fits_{s}.json") for s in SETS}
    fut = {s: load(f"casimir_future_{s}.json") for s in ("dovekie", "desy5")}
    res["best"] = {s: {k: dict(delta=v["delta"], prod=v["prod"], f=v["f"], eps=v["eps"], R_micron=v["R_micron"], c_eff=v["info"]["c_eff"], dln_mKK=v["info"]["dln_mKK_rec_to_0"], w_phi=v["info"]["w_phi"]) for k, v in c["best"].items()} for s, c in cf.items()}
    res["fading"] = {s: dict(neg=c["fading_neg"], pos=c["fading_pos"]) for s, c in cf.items()}
    res["eps_profile"] = {s: c["eps_profile"] for s, c in cf.items()}
    res["n_scan"] = {s: c["n_scan"] for s, c in cf.items()}
    res["future"] = fut
    neg = {s: c["best"]["0.7071_-1"] for s, c in cf.items()}
    pos = {s: c["best"]["0.7071_1"] for s, c in cf.items()}
    checks["12562: compressed: negative Casimir with sparse tower within 0.2 of fading on Pantheon+ and better on both DES samples, same parameter count"] = abs(neg["pantheon"]["delta"] - cf["pantheon"]["fading_neg"]) < 0.2 and neg["dovekie"]["delta"] < cf["dovekie"]["fading_neg"] and neg["desy5"]["delta"] < cf["desy5"]["fading_neg"]
    pref = {s: pos[s]["delta"] - neg[s]["delta"] for s in SETS}
    res["sign_preference"] = pref
    checks["12562: the negative sign is preferred, mildly: by 0.6, 1.7, 3.5 at b = 1/sqrt 2"] = all(p > 0 for p in pref.values()) and abs(pref["pantheon"] - 0.56) < 0.1 and abs(pref["dovekie"] - 1.74) < 0.1 and abs(pref["desy5"] - 3.54) < 0.1
    ns = {s: {float(k): v["delta"] for k, v in c["n_scan"].items()} for s, c in cf.items()}
    spread = {s: max(v.values()) - min(v.values()) for s, v in ns.items()}
    res["n_scan_spread"] = spread
    checks["12562: the exponent is NOT measured: Delta chi2 varies by under 1.5 from n = 1 to 12 on all samples, and n = 4 is no minimum"] = all(x < 1.5 for x in spread.values()) and all(min(v, key=v.get) != 4.0 for v in ns.values())
    checks["12562: without the Casimir term the sparse tower alone gains under 3: the slope is needed"] = all(c["eps_profile"]["0.0"]["delta"] > -3 for c in cf.values())
    R5 = {s: v["R_micron"]["5"] for s, v in neg.items()}
    res["R5_micron"] = R5
    checks["12562: if the term is Casimir with the 5 graviton dof, R is 12.6 to 13.8 microns; R ~ |eps|^(-1/4), so this agreement is weak evidence"] = all(12.5 < r < 13.9 for r in R5.values())
    ratios = {s: abs(v["info"]["c_eff"]) / v["prod"] for s, v in neg.items()}
    res["c_over_cprime"] = ratios
    checks["12562: identity c_eff / (f b) = 4 |eps| / (f V_today): recomputed from the fit within 1e-6, and the value is well above 4, as the data want"] = all(abs(abs(v["info"]["c_eff"]) - 4 * 0.7071 * abs(v["eps"]) / (v["info"]["ol"] + v["eps"])) < 1e-6 for v in neg.values()) and all(x > 13 for x in ratios.values())
    for s, ff in fut.items():
        assert ff["control_Z0"]["t_turnaround_H0"] is None
    checks["12562: future, at n = 4, an extrapolation: negative branch turns around 7 to 9 Gyr from now at b = 1/sqrt 2, V crosses zero first; the positive branch and the Z = 0 control never do"] = all(7 < ff["0.7071_-1"]["t_turnaround_Gyr"] < 9.5 and ff["0.7071_-1"]["t_V_zero_Gyr"] < ff["0.7071_-1"]["t_turnaround_Gyr"] and ff["0.7071_1"]["t_turnaround_H0"] is None for ff in fut.values())

    # full Planck
    pc = {s: load(f"class_casimir_{s}.json") for s in ("dovekie", "desy5")}
    res["planck"] = {s: {k: dict(delta=v.get("delta"), eps=v.get("eps"), prod=v.get("p", {}).get("prod"), S8=v.get("info", {}).get("S8"), lens=v.get("lens"), parts=v.get("parts"), failed=v.get("failed")) for k, v in d.items() if isinstance(v, dict)} for s, d in pc.items()}
    for s, d in pc.items():
        res["planck"][s]["free_neg_delta"] = d["free_neg"] - d["LCDM"]
        res["planck"][s]["free_pos_delta"] = d["free_pos"] - d["LCDM"]
    a, b = res["planck"]["dovekie"], res["planck"]["desy5"]
    checks["12562: full Planck with two fluids: negative Casimir at least as good as the free-slope fading fit run on both samples, by 0.15 and 0.53, inside fit scatter"] = 0 < a["free_neg_delta"] - a["b707_neg"]["delta"] < 0.6 and 0 < b["free_neg_delta"] - b["b707_neg"]["delta"] < 0.6
    checks["12562: lensing post hoc is neutral between negative Casimir and fading: within 0.3 on both samples"] = abs(a["b707_neg"]["lens"] - 20.205) < 0.3 and abs(b["b707_neg"]["lens"] - 20.368) < 0.3
    checks["12562: full Planck: the negative branch beats the positive on both samples"] = a["b707_neg"]["delta"] < a["b707_pos"]["delta"] and b["b707_neg"]["delta"] < b["b707_pos"]["delta"]
    checks["12562: compressed and full Planck eps agree within 0.1 at b = 1/sqrt 2"] = abs(a["b707_neg"]["eps"] - neg["dovekie"]["eps"]) < 0.1 and abs(b["b707_neg"]["eps"] - neg["desy5"]["eps"]) < 0.1

    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    print(json.dumps(res["planck"], indent=0, default=float)[:2500])
    print(R5, pref, spread, ratios)


if __name__ == "__main__":
    main()
