"""Passes 12609-12611 (Claude track).  Haloscopes, SU(5) thresholds and the axion-mass ceiling for the PQ-assisted model.  See PASS12609_12611_PQ_TESTS.md.  Not a theory of everything."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12609_to_12611_pq_tests.json"


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks = {}
    h = load("pq_haloscope.json")
    t = load("pq_gut_thresholds.json")
    c = load("pq_ma_ceiling.json")["ceiling_ueV_by_instability_scale"]
    res = dict(haloscope=h, thresholds=t, ceiling=c)
    checks["12609: control: ADMX excludes KSVZ across 2.7 to 4 ueV and DFSZ over half"] = h["KSVZ_ADMX"] > 0.99 and 0.4 < h["DFSZ_ADMX"] < 0.7
    checks["12609: control: CAPP excludes KSVZ over most of 4.5 to 5.5 ueV"] = h["KSVZ_CAPP"] > 0.8
    checks["12609: Model A is not excluded anywhere in 20 to 220 ueV, best limit 35 times weaker at 25 to 60"] = h["ModelA_20_220"] == 0 and 30 < h["best_ratio_25_60"] < 40
    checks["12610: control: zero thresholds reproduce the two-loop crossing"] = all(t[k]["control_zero_threshold"] < 1e-5 for k in t)
    checks["12610: Model A survives Super-K in 63 to 76 percent of threshold draws"] = 0.6 < t["A"]["span10"]["frac_above_SK"] < 0.66 and 0.73 < t["A"]["span3"]["frac_above_SK"] < 0.79
    checks["12610: B survives in at most 15 percent and the single Q in none"] = t["B"]["span10"]["frac_above_SK"] < 0.2 and t["Q"]["span10"]["frac_above_SK"] == 0
    checks["12610: Hyper-K at 1e35 yr would see Model A in about 80 percent of draws"] = 0.75 < 1 - t["A"]["span10"]["frac_above_HK"] < 0.86
    checks["12611: the m_a ceiling runs from about 28 to about 211 ueV as mu_I goes from 1e10 to 1e11"] = abs(c["1e+10"] - 28.5) < 0.1 and abs(c["1e+11"] - 211.1) < 0.2
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    for k, v in checks.items():
        print(("PASS" if v else "FAIL"), k)
    print("all_checks_pass", res["all_checks_pass"])


if __name__ == "__main__":
    main()
