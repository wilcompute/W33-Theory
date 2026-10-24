"""Passes 12265-12270: the non-SUSY engine's missing mod-2 check located and patched, the two N = 0 engines reconciled sector by sector,
and every model the stock engine accepted wrongly repaired by a lattice shift (Claude track).

12265 -- corpus-wide audit.  4514 T6/Z3 model files of the corpus run through the stock non-SUSY orbifolder (lenient), a patched build
  (strict) and the Python Ploger audit: 2434 load in both, 497 load only in the stock engine, 1583 in neither.  The audit's verdicts
  coincide with the engines': (7f)-only <=> lenient-only (497/497), any (7d) failure <=> rejected by both (1577/1577), clean <=> accepted
  by both except 6 inputs that fail the shift-shift condition (7c), which the audit does not test and the engine enforces.  So the stock
  engine enforces (7d) mod 2 and skips (7e)/(7f).  Lead models: S002 and the A8 Standard Models are consistent; T115
  (N008_F1_04_S037_T115, 12121-12155) is lenient-only.
12266 -- the engine disagreement on Witten-twisted 10s is resolved.  The *_n0-patched orbifolder 1.2.1 build was rebuilt with sector
  output (the earlier link failure: the *_n0 sources had never been compiled).  On the 12254 models it reproduces the stored v2 output and
  agrees with the non-SUSY engine field for field in the untwisted and both Z3-twisted sectors (10 counts included).  It has no
  Witten-twisted sector at all: every Witten-twisted fixed brane fails its local condition N(V_loc^2 - v_loc^2) = 0 mod 2 (55 warnings per
  model, the control included) and is dropped.  Every extra 10 of the non-SUSY engine sits in a Witten-twisted sector.
12267 -- mirage-torsion repairs.  A lattice shift D of one torus' Wilson lines changes the Ploger data by a homomorphism of E8 x E8, so
  a repair exists iff the defect lies in the image subgroup (built exactly from the 480 roots).  All 497 lenient-only models are
  repairable (486 on one torus with a second independent repair, 11 need two tori).  The stock engine's spectrum of each original input is
  compared with the strict engine's spectrum of its repairs: identical in 983/983 (gauge factors, U(1) directions, and all fields with
  sector, fixed point, dimensions and U(1) charges).  So every lenient-only corpus model is the stock-engine shadow of a consistent model
  with the same spectrum; the consistent-subset restatement of 12259/12261 was too strict, and the original counts stand.
12268 -- the bug and the fix.  In the non-SUSY orbifolder's COrbifoldGroup::CheckModularInvariance the Wilson-line product failure sets
  IsModularInvariant = false only inside `if (info) if (verbose) {...}`, with verbose hard-coded false; CRandomModel::Create has the same
  pattern for an ill-defined orbifold group.  Patch: search_drivers_12268/nonsusy_orbifolder_strict.patch (local build ~/orb/nsostrict).
  Pre-check for drivers: ploger_gate.py, which agrees with the strict engine on 4508/4514 (the 6 are the (7c) inputs).
12269 -- main checkout: see the round report.
12270 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12265_to_12270_strict_engine_and_mirage_census.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    ev = json.loads((A / "search_drivers_12265" / "engine_vs_audit.json").read_text())
    t = ev["table"]
    res["12265"] = t
    checks["12265: lenient-only <=> (7f)-only (497); (7d) <=> rejected by both (1577); clean <=> accepted (2434) up to 6 (7c) inputs"] = (
        t.get("lenient=1 strict=0 audit=7f") == 497
        and t.get("lenient=0 strict=0 audit=7d", 0) + t.get("lenient=0 strict=0 audit=7d+7f", 0) == 1577
        and t.get("lenient=1 strict=1 audit=ok", 0) + t.get("lenient=1 strict=1 audit=parse", 0) == 2434
        and t.get("lenient=0 strict=0 audit=ok") == 6
        and not any(k.startswith("lenient=0 strict=1") for k in t))
    sc = json.loads((A / "search_drivers_12266" / "sector_compare.json").read_text())
    res["12266"] = sc
    ok = True
    for lab, d in sc.items():
        if not d["nso"]:
            continue
        for key, n in d["v2"].items():
            ok &= d["nso"].get(key) == n
        ok &= not any(k.startswith("W ") for k in d["v2"])
        ok &= all(d["nso_tens"].get(k, 0) == n for k, n in d["v2_tens"].items())
        ok &= sum(n for k, n in d["nso_tens"].items() if not k.startswith("W ")) == sum(d["v2_tens"].values())
        ok &= d["v2_local_condition_failures"] == 55
    checks["12266: engines agree sector by sector off the Witten-twisted sectors; v2 has none (55 local-condition drops)"] = ok
    cc = json.loads((A / "search_drivers_12267" / "census_compare.json").read_text())
    res["12267"] = cc["summary"]
    per = cc["per_model"]
    checks["12267: all 497 lenient-only models repaired; stock spectrum = repair spectrum in 983/983"] = (
        len(per) == 497 and all(r["shifts"] for r in per) and sum(len(r["shifts"]) for r in per) == 983
        and all(s["verdict"] == "identical" for r in per for s in r["shifts"]))
    res["12267_T115_identical"] = (A / "search_drivers_12267" / "T115.nsoq").exists()
    g = json.loads((A / "search_drivers_12268" / "gate_vs_strict.json").read_text())
    res["12268_gate"] = g
    patch = (A / "search_drivers_12268" / "nonsusy_orbifolder_strict.patch").read_text()
    checks["12268: patch moves the failure flag out of the verbose branch; gate = strict engine on 4508/4514"] = (
        "-\t\t\t\t\t\tif(verbose)" in patch and "IsModularInvariant = false" in patch
        and g.get("('gatePASS', 'strict=1')") == 2434 and g.get("('gateFAIL', 'strict=0')") == 2074
        and g.get("('gatePASS', 'strict=0')") == 6 and "('gateFAIL', 'strict=1')" not in g)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
