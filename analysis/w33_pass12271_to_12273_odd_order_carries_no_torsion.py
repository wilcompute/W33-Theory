"""Passes 12271-12273: odd versus even order -- the lattice representative of a Z3 Wilson line carries no torsion, that of a Z2 Wilson
line does (Claude track).

12271 -- relabelling test.  W -> W + 2r (r a root with r.V0 integral, applied to an identical-WL pair together on T6/Z3) changes no
  Ploger datum.  Measured with the stock non-SUSY engine (strict build for consistent inputs):
    T6/Z3, models failing only (7f) (first 40 of the 12267 census):      80/80 spectra identical
    T6/Z3, consistent models (40 random, >= 2 Wilson-line tori, A8 SMs among them): 80/80 identical
    T6/(Z2^W x Z2 x Z2), order-2 inputs failing only (7f) (even_gen.py):    60/80 identical
    T6/(Z2^W x Z2 x Z2), consistent repairs of those inputs:               39/80 identical (2 more: same sectors, other charges)
  The last line is the control that falsified the first reading: at even order the relabelling is NOT harmless even on consistent
  models.  That is the published mirage-torsion statement (Ploger, Ramos-Sanchez, Ratz, Vaudrevange, hep-th/0702176): lattice shifts of
  Wilson lines act as generalized discrete torsion.  Cited, not claimed.  What is measured here: at order 3 no such dependence appears,
  either on consistent models or on the mod-1-only inputs the stock engine accepted.  Suspected mechanism (not proved): the phases a
  lattice shift can induce are signs, and an order-3 projection admits no nontrivial sign (Z2 (x) Z3 = 0).
12272 -- the even-order brothers.  Among four consistent lifts of each order-2 input (two repairs, two relabellings of the first): 1, 2, 3,
  4 distinct spectra for 2, 22, 12, 4 of the 40 inputs -- a lower bound on the torsion brothers per input.  The stock engine's output of
  an order-2 input agrees with neither repair in 30/40 (with both in 3).
12273 -- synthesis.  Together with 12267 (every lenient-only T6/Z3 corpus model's stock spectrum equals that of its consistent repairs):
  the corpus's T6/Z3 spectra, counts and lead models (T115 included) are spectra of consistent models, and the consistent-subset restatement
  of 12259/12261 was too strict.  Order-2 Wilson-line scans run on the stock engine would not be safe; the corpus has none on that engine.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12271_to_12273_odd_order_carries_no_torsion.json"
D = ROOT / "analysis" / "search_drivers_12271"


def main():
    checks, res = {}, {}
    rl = json.loads((D / "relabel_cmp.json").read_text())["summary"]
    oc = json.loads((D / "oddctrl_cmp.json").read_text())
    res["12271"] = dict(relabel=rl, odd_consistent=oc)
    checks["12271: odd order 80/80 + 80/80 invariant; even order 60/80 (weak) and 39/80 (consistent)"] = (
        rl.get("('odd', 'identical')") == 80 and oc.get("identical") == 80
        and rl.get("('even', 'identical')") == 60 and rl.get("('ctrl', 'identical')") == 39)
    load = [l.split() for l in (D / "even_load.txt").read_text().split("\n") if l.strip()]
    checks["12271: every order-2 input is lenient-only and both repairs are strict-consistent (40 + 80)"] = (
        sum(1 for p in load if p[0].endswith("_o.txt") and p[1:] == ["lenient=1", "strict=0"]) == 40
        and sum(1 for p in load if p[0].endswith(("_s0.txt", "_s1.txt")) and p[1:] == ["lenient=1", "strict=1"]) == 80)
    br = json.loads((D / "brothers.json").read_text())
    res["12272"] = br["distribution"]
    checks["12272: distinct consistent spectra per input 1/2/3/4 for 2/22/12/4 inputs"] = br["distribution"] == {"1": 2, "2": 22, "3": 12, "4": 4}
    ev = json.loads((D / "even_cmp.json").read_text())["summary"]
    res["12272_stock_vs_repairs"] = ev
    checks["12272: stock output of an order-2 input agrees with neither repair in 30/40, with both in 3"] = (
        ev.get("('different spectrum', 'different spectrum', 'different spectrum')", 0)
        + ev.get("('different spectrum', 'different spectrum', 'identical')", 0) == 30
        and ev.get("('identical', 'identical', 'identical')") == 3)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
