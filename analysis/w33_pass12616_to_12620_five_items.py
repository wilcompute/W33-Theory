"""Passes 12616-12620 (Claude track).  See PASS12616_12620_FIVE_ITEMS.md.  Not a theory of everything."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12616_to_12620_five_items.json"


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks = {}
    cm = load("pq_complete_multiplets.json")
    tg = load("trin_gates.json")
    ot = load("orbifold_twoloop.json")
    en = load("en_discriminator.json")
    sn = load("class_ppd_dovekie_sn.json")["rows"]
    bao = load("class_ppd_dovekie_bao.json")["rows"]
    res = dict(complete=cm, trin=tg, orbifold=ot, en=en, ppd=dict(sn=sn, bao=bao))
    t3 = cm["3_pairs"]
    checks["12616: three vectorlike (3,3bar,1) meet at M_U 3.5e16 with M_X 2.9e11 and tau above 1e38"] = abs(t3["two_loop"]["MU"] / 3.48e16 - 1) < 0.02 and abs(t3["two_loop"]["MX"] / 2.85e11 - 1) < 0.02 and t3["tau"] > 1e38
    checks["12616: N_DW = 1 allows E/N = 8/3 or -4/3"] = sorted(round(x, 3) for x in t3["EN_set_ndw1"]) == [-1.333, 2.667]
    checks["12616: one pair has no solution, two pairs no N_DW = 1"] = cm["1_pairs"]["two_loop"] is None and cm["2_pairs"]["EN_set_ndw1"] == []
    checks["12616: sigma stability with 27 colours puts the m_a ceiling below 1 ueV"] = tg["ceiling"] is not None and tg["ceiling"] < 1.0
    checks["12617: control: Lambda R = 1 reproduces the 4D two-loop scales within 0.1 percent"] = abs(ot["LR1"]["MX"] / 2.728e10 - 1) < 1e-3 and abs(ot["LR1"]["invR"] / 3.965e15 - 1) < 1e-3
    checks["12617: matter on the SU(5) brane is excluded at Lambda R >= 3"] = ot["LR3"]["tau"] < 2.4e34 and ot["LR10"]["tau"] < 2.4e34
    checks["12617: brane terms of +-1 keep M_X in the window in 82 percent of draws"] = abs(ot["brane_band"]["1.0"]["frac_MX_window"] - 0.8175) < 0.01
    checks["12618: controls: (3,1,-1/3) gives 2/3, (3,1,2/3) gives 8/3, complete SU(5) gives 8/3"] = en["control: single (3,1,-1/3)"]["EN"] == "2/3" and en["control: single (3,1,2/3)"]["EN"] == "8/3" and en["control: SU(5) 5 complete"]["EN"] == "8/3"
    checks["12618: Model A N_DW = 1 is above the GUT line, N_DW = 5 below"] = en["Model A, N_DW = 1"]["above_GUT_line"] and not en["Model A, all +"]["above_GUT_line"]
    tot = {k: sn[k]["elpd"] + bao[k]["elpd"] for k in sn if k in bao}
    res["ppd_total"] = tot
    checks["12620: posterior predictive: fading and CPL within 1 in total elpd"] = abs(tot["free_neg_infl1"] - tot["cpl_infl1"]) < 1
    checks["12620: both beat LCDM out of sample by more than 5 in elpd"] = tot["free_neg_infl1"] - tot["LCDM_infl1"] > 5 and tot["cpl_infl1"] - tot["LCDM_infl1"] > 5
    checks["12620: retraction: CPL's point estimate missed SN by 17 while its posterior predictive is within 1.1 of fading"] = sn["cpl_infl1"]["chi2_best"] - sn["LCDM_infl1"]["chi2_best"] > 15 and abs(sn["cpl_infl1"]["elpd"] - sn["free_neg_infl1"]["elpd"]) < 1.1
    checks["12620: exponential also beats LCDM by over 3, and the three evolving models lie within 3"] = tot["exp_infl1"] - tot["LCDM_infl1"] > 3 and max(tot[k] for k in ("free_neg_infl1", "cpl_infl1", "exp_infl1")) - min(tot[k] for k in ("free_neg_infl1", "cpl_infl1", "exp_infl1")) < 3
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    for k, v in checks.items():
        print(("PASS" if v else "FAIL"), k)
    print("all_checks_pass", res["all_checks_pass"])


if __name__ == "__main__":
    main()
