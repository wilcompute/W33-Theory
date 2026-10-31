"""Passes 12506-12513 (Claude track): braiding metaplectic anyons on the minimal codewords of W(3,3), and the q = 9 240-point E8 probe.

12507 -- the SU(2)_4 / TL6 braid generators (transvections along a noncommutation path) act on the 216 minimal even line sets (Pass
  173): B3 -> SL(2,3) (11 orbits), B4 -> order 648 with centre 3 and quotient profile = ASL(2,3) (108 + 108), B5, B6 -> PSp(4,3)
  (transitive).
12506 -- the 240 points covered by the q = 9 48-set: two 120-orbits (the swap merges them), collinearity graph 32-regular -- not the
  E8 root graph (control spectrum 56, 28, 8, -2, -4).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "search_drivers_12466"
OUT = ROOT / "data" / "w33_pass12506_to_12513_quantum_bridges.json"


def load(name):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else None


def main():
    checks, res = {}, {}
    b, g4, qt, e8 = load("braid_codewords.json"), load("braid_B4_group.json"), load("braid_B4_quotient.json"), load("e8_icosian_probe.json")
    res.update(braid=b, B4_group=g4, B4_quotient=qt, e8_probe=e8)
    k = b["by_k"]
    checks["12507: braid relations hold; B3/B4/B5/B6 images have orders 24/648/25920/25920"] = (
        b["braid_relations"] and b["far_commutation"]
        and [k[str(i)]["group_order_on_points"] for i in (3, 4, 5, 6)] == [24, 648, 25920, 25920])
    checks["12507: orbits on the 216 minimal codewords -- B4 splits them 108 + 108, B5 is transitive"] = (
        b["minimal_codewords"] == 216 and k["4"]["orbits_on_216"] == [108, 108] and k["5"]["orbits_on_216"] == [216])
    checks["12507: the B4 image has centre 3 and its quotient has the ASL(2,3) (Hessian) element-order profile"] = (
        g4["order"] == 648 and g4["center_order"] == 3 and qt["quotient_order"] == 216 and qt["same_profile"])
    checks["12506: the q = 9 240 points -- two 120-orbits, collinearity graph 32-regular, unlike the E8 root graph (56-regular)"] = (
        e8["covered"] == 240 and e8["orbits_full"] == [120, 120] and e8["collinearity_degrees"] == [32]
        and e8["E8_root_graph_spectrum"] == {"-4.0": 84, "-2.0": 112, "8.0": 35, "28.0": 8, "56.0": 1})
    m9 = load("q9_le46.json")
    if m9:
        res["12509_q9_le46"] = {x: v for x, v in m9.items() if x != "chosen"}
    checks = {x: bool(v) for x, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
