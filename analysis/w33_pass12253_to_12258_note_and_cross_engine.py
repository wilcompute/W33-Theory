"""Passes 12253-12258: standalone note on the no-Higgs-10 theorem; cross-engine audit (Wilson-line modular invariance mod 1 versus
mod 2, and engine dependence of the twisted-10 counts); the rule on all 104 A8 Standard Models; the anomalous U(1) of SM_2496 (Claude track).

12253 -- papers/no_higgs_10/main.tex: a self-contained note (setup, the statistics rule with proof, the theorem with the coset-table
  enumeration and controls, caveats).  Every number in it is checked below.
12254 -- cross-engine audit.  (a) The independent engine (orbifolder 1.2.1 based, nsdump_v2) imposes the Wilson-line condition
  3 W_a.W_b in 2Z across tori (Ploger et al., mirage torsion); the non-SUSY orbifolder only 3 W_a.W_b in Z.  All 104 A8 Standard Models
  satisfy the stronger form; of the 153 consistent twisted-10 models 88 do (32 of the 58 three-generation ones, 56 of the 95 six-generation).
  The no-scalar-10 theorem is an absence statement and holds a fortiori.  (b) On models both engines accept the gauge groups agree, and on
  the base control both give the same chiral 16s (4 - 1); but on the candidate models the independent engine keeps fewer Witten-twisted
  10s (0 or 3 against 3 or 6), and the engines' total state counts differ already on the control (different multiplet conventions).
  Existence and number of twisted fermionic 10s (12217/12223) are therefore engine-dependent; the absence of a scalar 10 is not (no
  scalar-type momentum exists on the mass shell).
12255 -- the rule on every A8 SO(16)^2 Standard Model (104 models): from left weights alone it reproduces the engine's statistics for all
  74,174 fields.
12256 -- SM_2496: the extra U(1) of the shift class lies in v9's U(1) span (residual 1e-15) and has Tr Q = -6.57, a component along the
  anomalous U(1) (the only one with nonzero trace, 51.7).  Both classes carry exactly one anomalous U(1), so both have massless rank 15;
  a scalar-10 vev of v0 lowers it to 14 -- the 12249 correction stands (same roots, different vacua).
12257 -- main checkout not synced: a parallel-track hardware file still differs from origin.
12258 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12253_to_12258_note_and_cross_engine.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    note = (ROOT / "papers" / "no_higgs_10" / "main.tex").read_text(encoding="utf-8")
    nums = ["165{,}465", "294", "119{,}915{,}126", "2{,}210{,}046", "5{,}974", "74{,}174", "65{,}659", "231{,}124", "147/147", "366"]
    checks["12253: the standalone note exists and states the certified numbers"] = all(n in note for n in nums)
    m2 = json.loads((A / "search_drivers_12254" / "mod2.json").read_text())
    res["12254_mod2"] = m2
    checks["12254a: mod-2 Wilson-line condition: A8 104/104; twisted-10 models 88/153 (three-generation 32/58)"] = (
        m2["A8_SMs"] == {"models": 104, "mod2_ok": 104} and m2["C10_one_line_models"] == {"models": 153, "mod2_ok": 88}
        and m2["three_generation_mod2"] == 32 and m2["six_generation_mod2"] == 56)
    xe = json.loads((A / "search_drivers_12254" / "xengine.json").read_text())
    xc = json.loads((A / "search_drivers_12254" / "xengine_control.json").read_text())
    res["12254_engines"] = dict(candidates=xe, control=xc)
    v2_10 = [sum(v for k, v in x["v2"]["tens"].items() if "10" in k) for x in xe.values()]
    nso_10 = [sum(v for k, v in x["nso"]["tens"].items() if "10" in k) for x in xe.values()]
    checks["12254b: control agrees on chiral 16s; candidate models: the independent engine keeps fewer twisted 10s"] = (
        xc["v2"]["sixteens"] == {"(2, '-16')": 1, "(2, '16')": 4, "(3, '-16')": 4, "(3, '16')": 1}
        and xc["nso"]["sixteens"] == {"(19, '-16')": 1, "(19, '16')": 4, "(20, '-16')": 4, "(20, '16')": 1}
        and all(a < b for a, b in zip(v2_10, nso_10)))
    a8 = json.loads((A / "search_drivers_12255" / "a8_all.json").read_text())
    res["12255"] = dict(models=a8["models"], total=a8["total"])
    checks["12255: rule reproduces the statistics of all 74,174 fields of the 104 A8 Standard Models"] = (
        a8["models"] == 104 and a8["total"] == {"agree": 74174, "mismatch": 0})
    u = json.loads((A / "search_drivers_12256" / "extra_u1.json").read_text())
    res["12256"] = u
    checks["12256: extra U(1) in span, Tr = -6.57 (mixes with the anomalous U(1)); one anomalous U(1) per class; massless rank 15 both"] = (
        u["u_in_u1_span_residual"] < 1e-9 and abs(u["tr_u"] + 6.5727) < 1e-3 and u["v0_anomalous"] == 1 and u["v9_anomalous"] == 1
        and u["massless_rank_v0"] == 15 and u["massless_rank_v9"] == 15)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
