"""Pass 12621 (Claude track): trinification axion window, Higgs self-stabilisation by PQ quarks, n_s pull by dark-energy model.  See PASS12621_OUTSIDE_LINKS.md.  Not a theory of everything."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12621_outside_links.json"


def main():
    load = lambda n: json.loads((D / n).read_text())
    tw, hs, ns = load("trin_window.json"), load("pq_higgs_selfstab.json"), load("ns_by_model.json")
    checks = {}
    checks["trinification axion: DMRadio-m3 DFSZ reach covers 0.12-0.8 ueV with theta 0.10-0.30"] = all(r["DMRadio_m3_DFSZ"] for r in tw if r["m_a_ueV"] >= 0.12) and abs(tw[0]["theta"] - 0.299) < 0.01
    checks["control: no new states gives no shift"] = hs["control_none"]["delta_lambda_MP"] == 0
    checks["PQ quarks raise lambda but it stays negative for every model"] = all(hs[k]["delta_lambda_MP"] > 0 and not hs[k]["stays_positive"] for k in ("model_A", "trinification_3", "model_A_low_MX"))
    checks["BAO pulls n_s up by over 0.005 in LCDM and the exponential, under 0.001 in CPL and fading"] = ns["bao_pull"]["LCDM"] > 0.005 and ns["bao_pull"]["exp"] > 0.005 and ns["bao_pull"]["cpl"] < 0.001 and ns["bao_pull"]["free_neg"] < 0.001
    res = dict(trin_window=tw, higgs=hs, ns=ns, checks=checks, all_checks_pass=all(checks.values()))
    OUT.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    for k, v in checks.items():
        print(("PASS" if v else "FAIL"), k)
    print("all_checks_pass", res["all_checks_pass"])


if __name__ == "__main__":
    main()
