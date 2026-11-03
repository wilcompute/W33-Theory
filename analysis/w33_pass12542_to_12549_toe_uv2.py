"""Passes 12542-12545 (Claude track).  Not a theory of everything: see PASS12542_12549_SUPERNOVAE_HIGGS_ANOMALIES.md.

12542 -- exponential quintessence with real supernovae: sqrt 2 out, sqrt(2/3) viable, lam near 0.6 mildly preferred.
12543 -- the true Higgs trajectory: M_H(M_t) is robust; M_t for M_H = 125.20 lies in 170.88-173.18.
12544 -- no cancellation of the regulator spread for f_g, under a stated assumption.
12545 -- the smallest anomaly-free chiral theory of this shape is one SM generation.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12542_to_12549_toe_uv2.json"


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks, res = {}, {}
    p, d, ht, hf, rc, ae = (load(n) for n in ("sn_quint_pantheon.json", "sn_quint_dovekie.json", "higgs_trajectory.json", "higgs_floor.json", "robust_correlation.json", "anomaly_enum.json"))
    res.update(pantheon=p, dovekie=d, higgs_trajectory=ht, higgs_floor=hf, robust_correlation=rc, anomaly=ae)
    checks["12542: controls: CPL within the published errors for both samples"] = (
        abs(p["CPL"]["w0"] + 0.838) < 0.055 and abs(p["CPL"]["wa"] + 0.62) < 0.22 and abs(d["CPL"]["w0"] + 0.803) < 0.054 and abs(d["CPL"]["wa"] + 0.72) < 0.21)
    qp, qd = {x["lam"]: x for x in p["quintessence"]}, {x["lam"]: x for x in d["quintessence"]}
    checks["12542: sqrt 2 excluded on both samples by Delta chi2 > 40, flat and curved relative to LCDM + k"] = all(q[1.414]["flat_delta"] > 40 and q[1.414]["curved_delta"] - s["LCDM_k"]["delta"] > 40 for q, s in ((qp, p), (qd, d)))
    checks["12542: sqrt(2/3) no worse than LCDM on both samples; lam = 0.6 better than LCDM on both"] = qp[0.816]["flat_delta"] < 0 and qd[0.816]["flat_delta"] < 0 and qp[0.6]["flat_delta"] < -2 and qd[0.6]["flat_delta"] < -3
    checks["12542: quintessence captures less than CPL"] = min(x["flat_delta"] for x in d["quintessence"]) > d["CPL"]["delta"] and min(x["flat_delta"] for x in p["quintessence"]) > p["CPL"]["delta"]
    t = {x["label"]: x for x in ht["robustness"]}
    checks["12543: M_H stable under the UV start: T = 400, 800, 2000 within 0.01 GeV"] = abs(t["base"]["MH"] - t["T=800"]["MH"]) < 0.01 and abs(t["T=800"]["MH"] - t["T=2000"]["MH"]) < 0.01
    s = [x for x in ht["scan"] if "MH" in x]
    checks["12543: M_H rises by under 3 GeV from f_lam = 0.002 to 1"] = all(a["MH"] < b["MH"] for a, b in zip(s, s[1:])) and s[-1]["MH"] - s[0]["MH"] < 3
    r = {x["f_lam"]: x for x in hf["rows"]}
    checks["12543: M_t needed for 125.20 runs from 170.88 to 173.18 and contains the measured value"] = abs(r[1.0]["Mt_for_MH_125p20"] - 170.88) < 0.02 and abs(r[0.0002]["Mt_for_MH_125p20"] - 173.18) < 0.02 and r[1.0]["Mt_for_MH_125p20"] < 172.57 < r[0.0002]["Mt_for_MH_125p20"]
    checks["12543: with f_g, f_y fitted, the implied f_lam 0.0129 gives M_H 127.87, not 125.2"] = abs(ht["target"]["f_lam"] - 0.0129) < 2e-4 and abs(t["base"]["MH"] - 127.87) < 0.02
    checks["12544: G f_g for SM matter ranges 0.037 to 0.72 under the assumed mapping: no cancellation"] = abs(rc["G_fg_range_SM"][0] - 0.0366) < 0.001 and abs(rc["G_fg_range_SM"][1] - 0.7236) < 0.001
    a3 = ae["bifundamental_shape_by_N"]["3"]
    sm = a3["smallest"][0]
    checks["12545: at N = 3 the smallest has 15 Weyl fermions, charges 1, -4, 2, -3, 6, Higgs +-3; larger N need more"] = (
        a3["smallest_weyl"] == 15 and sm["q"] == 1 and sorted(sm["u"]) == [-4, 2] and sm["L"] == [-3] and sm["e"] == [6] and sm["higgs"] == [-3, 3] and sum(x["weyl"] == 15 for x in a3["smallest"]) == 1
        and all(ae["bifundamental_shape_by_N"][str(n)]["smallest_weyl"] > 15 for n in (4, 5, 6, 7)))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])


if __name__ == "__main__":
    main()
