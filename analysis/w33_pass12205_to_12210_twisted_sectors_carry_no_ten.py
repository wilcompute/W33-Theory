"""Passes 12205-12210: the twisted sectors carry no 10 at all; a single native C3 already freezes the Narain moduli; the
refined audit confirms 12200; an order-3 Scherk-Schwarz route stays open (Claude track).

12205 -- audit of the 103 Z6-II parents with a Gamma-valued order-2 direction (12200) under the refined criterion of 12199b
  (all products of W_2t with V, W1..W6 and W_2t^2/2 even): all 103 directions pass, 0 parity violations, all 103 parents
  (even, odd) = (1, 2).  12200 and the 12180 closure stand unchanged.
12206 -- the placement dichotomy: with a translation-symmetric direction the paired (odd-sector) net is even (12199b/12205),
  so with three generations N_even is 1 or 3; N_even = 3 occurs once in 128 (SM_2751, untwisted family triplet), never with
  such a direction.  Why N_even = 3 and a symmetric direction exclude each other is NOT derived here (empirical, 0/103).
12207 -- order-3 Scherk-Schwarz on T6/Z3: the twist fixes a 3-dimensional space of Lambda/3Lambda (one order-3 translation
  per plane; det(1 - theta) = 27; mod 2 kernel 0, as in 12177), so a Z3 Scherk-Schwarz twist is geometrically available.  It is
  NOT closed by the order-three law of the paper, since two independent order-3 twists (Z3 x Z3) evade that law; building
  it needs a Z3 R-symmetry twist the engines do not implement.  OPEN.
12208 -- the twisted sectors carry no 10: in all 163 SU(5) x U(1) models of the e6+a2 route saved by Passes 12161-12182
  (nsodump dumps), every one of the 614 fields in the SU(5) 10 is a Z3-untwisted, Witten-untwisted FERMION; there is no
  twisted 10 of either statistics.  So the missing 10_H is not a parity selection in the twisted sectors -- the 10 simply does
  not occur there; with the untwisted theorem (12170) the 10_H is absent from every sector in this sample.  Mass-shell bound
  (not a proof): a 10 weight has SU(5)-projected norm 6/5, a massless Z3-twisted state total norm 4/3 (2/3 with an oscillator),
  so a twisted 10 needs an orthogonal component of norm exactly 2/15, never realised in the sample.
12209 -- single-C3 points of the native Narain lattice (12194-12198): the tangent space of O(2,2)/O(2)xO(2) at H is 4-dim
  (control); the deformations invariant under the full C3 x C3 are 0 (= 12198) and under EACH single C3 also 0.  A single C3
  already freezes all four moduli, so the 2-dim translation space it allows (12203) sits at a rigid point: a running
  interpolation radius requires breaking the native symmetry completely.
12210 -- synthesis.
"""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12205_to_12210_twisted_sectors_carry_no_ten.json"
D = ROOT / "analysis" / "search_drivers_12205"


def main():
    checks, res = {}, {}
    a = json.loads((D / "audit.json").read_text())
    gam = [r for r in a.values() if r["gamma_dirs"]]
    ref = [r for r in a.values() if r["refined_dirs"]]
    res["12205"] = dict(parents=len(a), gamma=len(gam), refined=len(ref), gens={str(k): n for k, n in Counter((r["even"], r["odd"]) for r in ref).items()})
    checks["12205: 103 Gamma-valued Z6-II directions all pass the even-products criterion; all (1, 2); no violations"] = (
        len(a) == 128 and len(gam) == 103 and len(ref) == 103 and all((r["even"], r["odd"]) == (1, 2) for r in ref)
        and not [r for r in ref if r["odd"] % 2])
    alln = Counter(r["even"] for r in a.values())
    res["12206"] = {str(k): n for k, n in alln.items()}
    checks["12206: N_even = 3 in exactly one parent, which has no Gamma-valued direction"] = (
        alln[3] == 1 and all(not r["gamma_dirs"] for r in a.values() if r["even"] == 3))
    z = json.loads((D / "z3_translation.json").read_text())
    res["12207"] = z
    checks["12207: T6/Z3 admits a 3-dim space of order-3 translations (mod 3 kernel 3), none of order 2"] = (
        z["kernel_mod3"] == 3 and z["kernel_mod2"] == 0 and z["det(1-theta)"] == 27)
    t = json.loads((D / "tens.json").read_text())
    res["12208"] = t
    checks["12208: 163 SU(5) models, 614 fields in the 10, all Z3-untwisted Witten-untwisted fermions; no twisted 10"] = (
        t["models"] == 163 and t["counts"] == {"fermion|untw-W|Z3-untwisted": 614})
    s = json.loads((D / "single_c3.json").read_text())
    res["12209"] = s
    checks["12209: native Narain tangent space 4 (control); invariant deformations 0 under C3 x C3 and under each single C3"] = (
        s == {"tangent": 4, "C3xC3": 0, "C3_first": 0, "C3_second": 0})
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
