"""Passes 12235-12240: the statistics rule derived from the projection phase, with the parity condition that consistency imposes;
the rule on the A8 route; the hidden SU(5) of SM_2496 (Claude track).

12235 -- derivation.  The Witten element g = (V0, s0) acts trivially on T6, so its projection phase on a state of sector h =
  (w, n, m_a) is (P.V0 - R.s0) - (1/2)(V_h.V0 - v_h.s0) with R.s0 = R0, v_h.s0 = w and V_h.V0 = w V0^2 + n V1.V0 + sum m_a W_a.V0.
  Hence (P.V0 - R0) = (1/2)(w (V0^2 - 1) + n V1.V0 + sum m_a W_a.V0) mod 1.  With V0^2 = 2 (split x split) this is w/2 exactly when
  V1.V0 and every W.V0 are even.  The parity is not automatic: about 30% of the one-line admissible space (V0.W integral, 12161)
  has V0.W odd -- and there the constant would depend on whether a fixed-point label is written 1 or -2, i.e. the projection is
  ill-defined.  The engine agrees: every odd-parity configuration fails to load (111/111 one-line, 36/36 two-line candidates), every
  loading model has even parity; the observed models have V0^2 = 2 and products 0 (or 2).  So on every consistent model the rule
  'scalar iff P.V0 = w/2' is derived, not fitted.
12236 -- two lines, two further seeds of 20,000 draws each (lattice-only scalar test): see the data.
12237 -- the rule on the A8 SO(16) x SO(16) route of Pass 11095 (three Standard Models): constant w/2 in 18/18 sectors, R0 fixes the
  statistics in all of them, V0^2 = 2 and all products even (0 or 2): it covers their Higgs doublets like every other scalar.
12238 -- the hidden SU(5) of SM_2496 under interpolation: of its 20 split V0, nine keep the hidden SU(5) unbroken and carry massless
  hidden scalar 10s in the unpaired (theta^2, theta^4) sectors, so they survive at large radius (n_B - n_F = 144); the other eleven break
  it by the shift to A2 + A1 (one A3), n_B - n_F = 48 -- the SU(3) x SU(2) pattern a 10 vev would produce (observation, condensation not
  computed).  The parent keeps at most two generations at large radius (generations (1, 2), 12180b).
12239 -- paper: the Section 7 boundary now states the rule's scope (derived on every consistent model with even products; on Z6-II
  R0 does not fix the statistics in two Witten-twisted sectors).
12240 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12235_to_12240_the_rule_derived.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    d = json.loads((A / "search_drivers_12235" / "derive.json").read_text())
    res["12235_models"] = d
    checks["12235: every model the rule was observed in has V0^2 = 2 and all V0 products even"] = (
        len(d) == 6 and all(v["V0sq_is_2"] and v["all_even"] for v in d.values()))
    ps = json.loads((A / "search_drivers_12235" / "parity_space.json").read_text())
    res["12235_space"] = ps
    odd = sum(v["V0W_odd"] for v in ps.values()); adm = sum(v["admissible"] for v in ps.values())
    checks["12235: about 30% of the one-line admissible space has V0.W odd (65,659 of 231,124)"] = adm == 231124 and odd == 65659
    lf = json.loads((A / "search_drivers_12235" / "loadfail_parity.json").read_text())
    res["12235_engine"] = lf
    one, two = lf["one_line"], lf["two_line"]
    checks["12235: engine rejects every odd-parity configuration (111/111, 36/36); every loading model has even parity"] = (
        one.get("odd|LOADFAIL") == 111 and "odd|loads" not in one and one.get("even|loads") == 153
        and sum(c for k, c in two.items() if k.split("|")[0] != "(0, 0)" and k.endswith("LOADFAIL")) == 36
        and not any(k.split("|")[0] != "(0, 0)" and k.endswith("loads") for k in two))
    t = [json.loads((A / "search_drivers_12224" / f"twoline3_{s}.json").read_text()) for s in (17, 23, 29)]
    res["12236"] = t
    checks["12236: two lines, three seeds x 20,000 draws: no scalar-type twisted 10"] = all(x["draws"] == 20000 and x["scalar_type_configs"] == 0 for x in t)
    a8 = {n: json.loads((A / "search_drivers_12237" / f"selection_a8_{n}.json").read_text()) for n in (1, 40, 90)}
    par = json.loads((A / "search_drivers_12237" / "a8_parity.json").read_text())
    ok = all(len(s["sectors"]) == 6 and all(len(v) == 1 and v[0] == ("0" if k.split(", ")[1] == "0" else "1/2") for k, v in s["sectors"].items())
             and not any((x[0] == "B" and x[1] != "0") or (x[0] == "F" and x[1] != "1/2") for vv in s["statistics_vs_R0"].values() for x in map(tuple, vv))
             for s in a8.values())
    res["12237"] = dict(parity=par)
    checks["12237: A8 route, 3 SMs: constant w/2 in 18/18 sectors, R0 fixes statistics, V0^2 = 2, products even"] = ok and all(v["all_even"] and v["V0sq"] == "2" for v in par.values())
    h = json.loads((A / "search_drivers_12238" / "hidden2496.json").read_text())
    res["12238"] = h
    keep = [r for r in h["interpolations"] if r["hidden_scalar_10"]]
    brk = [r for r in h["interpolations"] if not r["hidden_scalar_10"]]
    checks["12238: SM_2496: 9 V0 keep hidden SU(5) with scalar 10s (n_B - n_F = 144), 11 break it (48); parent generations (1, 2)"] = (
        len(keep) == 9 and all(r["SS_diff"] == 144 and r["gauge"].startswith("A4") for r in keep) and len(brk) == 11
        and all(r["SS_diff"] == 48 for r in brk) and h["parent_generations"] == {"even": 1, "odd": 2})
    tex = (ROOT / "papers" / "forty_points" / "sec07_realforms.tex").read_text(encoding="utf-8")
    checks["12239: Section 7 boundary states the rule's scope"] = "even products" in tex and "Witten-twisted sectors of" in tex
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
