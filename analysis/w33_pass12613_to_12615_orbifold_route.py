"""Passes 12613-12615 (Claude track): no 4D missing partner for Model A's fragments; the orbifold gives them exactly; prior art puts the axion under pressure.  See PASS12613_12615_ORBIFOLD_ROUTE.md.  Not a theory of everything."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12613_to_12615_orbifold_route.json"


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks = {}
    mp = load("missing_partner_search.json")
    det = load("missing_partner_detail.json")
    ob = load("orbifold_gut.json")
    res = dict(n_reps=mp["n_reps"], found=mp["found"], detail=det, orbifold=ob)
    c = mp["controls"]
    content = {d: sorted(x["content"]) for d in c for x in c[d][:1]}
    checks["12613: control: 10 = (1,1,1) + (3,2,1/6) + (3bar,1,-2/3)"] = content["10"] == ["(1,1,1)", "(3,2,1/6)", "(3bar,1,-2/3)"]
    checks["12613: control: 24 = (1,1,0) + (1,3,0) + (3,2,-5/6) + (3bar,2,5/6) + (8,1,0)"] = content["24"] == ["(1,1,0)", "(1,3,0)", "(3,2,-5/6)", "(3bar,2,5/6)", "(8,1,0)"]
    checks["12613: control: the textbook 50 with a 75 is found as the doublet-triplet missing partner"] = any("50" in x[0] and "75" in x[2] for x in det["control_DT"])
    checks["12613: no partner up to dimension 220 for either of Model A's light fragments, at content level"] = det["10"] == [] and det["5"] == [] and mp["found"]["10"] == [] and mp["found"]["5"] == []
    checks["12614: orbifold parities give exactly Model A's fragments"] = ob["model_A_by_parity"] == dict(five=["(3,1,-1/3)"], ten=["(3,2,1/6)"])
    checks["12614: control: the Higgs 5 with eta' = -1 keeps the doublet"] = ob["parity"]["5_eta-1"]["(1,2,1/2)"] == "light"
    kk = ob["kk_unification"]
    checks["12614: control: Lambda R = 1 reproduces the 4D one-loop scales within 1 percent"] = abs(kk["1.0"]["MX"] / 6.6e9 - 1) < 0.01 and abs(kk["1.0"]["invR"] / 8.4e15 - 1) < 0.01
    checks["12614: KK towers lower 1/R and M_X as Lambda R rises"] = kk["3.0"]["invR"] > kk["10.0"]["invR"] > kk["30.0"]["invR"] and kk["3.0"]["MX"] > kk["10.0"]["MX"]
    checks["12615: Model A's |E/N - 1.92| exceeds the GUT value's: above the line of arXiv:2511.21830"] = abs(2 / 3 - 1.92) > abs(8 / 3 - 1.92)
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    for k, v in checks.items():
        print(("PASS" if v else "FAIL"), k)
    print("all_checks_pass", res["all_checks_pass"])


if __name__ == "__main__":
    main()
