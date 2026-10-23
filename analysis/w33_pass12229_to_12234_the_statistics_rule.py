"""Passes 12229-12234: the statistics rule of the twisted sectors -- a 10 is a scalar iff P.V0 = w/2 mod 1 -- turns the twisted-10
results into lattice statements; the 58 three-generation twisted-10 models carry only scalar 1s and 5s (Claude track).

12229 -- the 58 three-generation twisted-10 models (12223): their scalar SU(5) representations, over every sector, are only singlets and
  5s (11,952 and 840 states); with no 10, 15, 24 or larger scalar, SU(5) cannot be broken to the Standard Model in field theory in any
  of them.
12230 -- the projection rule, read off the engine: in every sector of five models (one-line and two-line, 30 sectors) the quantity
  (P.V0 - R0) mod 1 -- P the left momentum, R0 the spacetime component of the right-moving weight, integral for bosons and
  half-integral for fermions -- is the constant w/2 (w the Witten label).  Hence a massless state is a SCALAR iff P.V0 = w/2 mod 1 and a
  fermion iff P.V0 = (w+1)/2 mod 1.  It reproduces every observed 10: untwisted 10s (w = 0, P.V0 = 1/2: fermions, 12170's '16 odd
  under the split parity'), one-line twisted 10s (w = 1, P.V0 in Z: fermions, 12225), two-line Witten-untwisted twisted 10s
  (w = 0, P.V0 = 1/2: fermions).  With 12225 (all 4050 one-line twisted 10-type massless momenta have w = 1 and P.V0 in Z) the
  one-line statement 'no scalar 10 in any sector' is now a lattice theorem on the full admissible space, independent of the engine's
  statistics assignment.
12231 -- two A4-type lines, scalar test on the lattice (12230 rule) over a large sample: see the data (draws, hits, scalar-type
  configurations, density).
12232 -- the main checkout was fast-forwarded: the blocking untracked files of the parallel track were byte-identical to origin
  except one JSON that was semantically identical (formatting only); all ten were backed up before the fast-forward.
12231 -- result: 20,000 two-line draws, 401 configurations with a twisted 10-type massless vector (2.0%, 95% CI 1.8-2.2%), and NO
  scalar-type one (no 10-type momentum with P.V0 = w/2): with two lines too, every twisted 10 is a fermion -- a large sample, lattice-only.
  Scope of the rule: on T6/Z3 the spacetime component R0 fixes the statistics in every sector (30/30 in five models); on Z6-II the
  constant-phase part holds (12/12 sectors) but two Witten-twisted sectors carry bosons with R0 = 1/2, so there the statistics is read
  from the engine, not from R0.
12233 -- SU(5) 10s in the non-free Z2W x Z6-II split-parity models of 12180 with an A4 factor (134 models): 106 untwisted fermions,
  12 Witten-twisted fermions and 54 SCALAR 10s -- all 54 in nine models of one parent, Z6II_06 SM_20260917_2496, whose SUSY gauge group
  is SU(5) x SU(3) x SU(2) with quark doublets (1, 3, 2): the SU(5) is HIDDEN.  The scalar 10s obey the rule (w = 0, P.V0 integral,
  R0 = 0).  No scalar 10 of a visible SU(5) occurs on Z6-II either (its visible group is already SU(3) x SU(2) in every parent).
12234 -- synthesis.
"""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12229_to_12234_the_statistics_rule.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    v = json.loads((A / "search_drivers_12229" / "vet58.json").read_text())
    res["12229"] = dict(models=v["models"], union=v["union"])
    checks["12229: the 58 three-generation twisted-10 models carry only scalar SU(5) singlets and 5s"] = (
        v["models"] == 58 and set(v["union"]) == {"1", "5"})
    s0 = json.loads((A / "search_drivers_12230" / "selection.json").read_text())
    sm = json.loads((A / "search_drivers_12230" / "selection_more.json").read_text())
    allsec = [s0["sectors"]] + [x["sectors"] for x in sm.values()]
    rule = all(len(vals) == 1 and vals[0] == ("0" if k.split(", ")[1] == "0" else "1/2") for sec in allsec for k, vals in sec.items())
    tens = [t for x in sm.values() for t in x["tens"]]
    res["12230"] = dict(models=1 + len(sm), sectors=sum(len(s) for s in allsec), tens_observed=sorted({str(t) for t in tens}))
    checks["12230: (P.V0 - R0) mod 1 = w/2 in all 30 sectors of 5 models; every observed 10 obeys it and is a fermion"] = (
        rule and sum(len(s) for s in allsec) == 30 and all(t[0] in (19, 20) for t in tens)
        and all((float(eval(t[2])) - (0.5 if t[1].split(',')[1].strip() == '1' else 0.0)) % 1 == 0.5 for t in tens))
    ch = json.loads((A / "search_drivers_12225" / "character.json").read_text())
    checks["12230: one-line theorem -- all 4050 twisted 10-type massless momenta have w = 1, P.V0 in Z, hence fermions by the rule"] = (
        ch["stats"] == {"1|0": 4050})
    t3 = json.loads((A / "search_drivers_12224" / "twoline3_17.json").read_text())
    res["12231"] = t3
    checks["12231: two lines, lattice scalar test on 20000 draws: no scalar-type 10 configuration"] = (
        t3["draws"] == 20000 and t3["scalar_type_configs"] == 0)
    z = json.loads((A / "search_drivers_12229" / "z6ii_tens.json").read_text())
    res["12233"] = dict(models=z["models"], total=z["total"])
    sc = [m for m in z["per_model"] if any(k.startswith("scalar") for k in m["tens"])]
    res["12233"]["scalar_models"] = [m["model"] for m in sc]
    sel = json.loads((A / "search_drivers_12230" / "selection_z6ii_2496.json").read_text())
    stens = sorted({(t["m"], str(t["sector"]), t["WV0"], t["R0"]) for t in sel["tens"]})
    res["12233"]["rule_on_hidden_scalar_10s"] = stens
    checks["12233: Z6-II: 134 A4 models; the only scalar 10s (54) sit in the HIDDEN SU(5) of parent SM_2496 and obey the rule (w=0, P.V0 in Z, R0=0)"] = (
        z["models"] == 134 and z["total"].get("scalar|w0|tw") == 54 and len(sc) == 9 and all("SM_20260917_2496" in m["model"] for m in sc)
        and all(t[0] in (15, 16) and t[2] == "0" and t[3] == "0" and t[1].split(",")[1].strip() == "0" for t in stens))
    checks["12233: on Z6-II the constant phase holds in 12/12 sectors"] = len(sel["sectors"]) == 12 and all(len(v) == 1 for v in sel["sectors"].values())
    checks = {k: bool(x) for k, x in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
