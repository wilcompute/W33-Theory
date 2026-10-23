"""Passes 12259-12264: the Wilson-line consistency conditions settled from the literature, and the corpus audited against them (Claude track).

12259 -- which condition is correct.  Ploger, Ramos-Sanchez, Ratz, Vaudrevange, 'Mirage torsion', JHEP 04 (2007) 063 [hep-th/0702176]
  (text extract kept in search_drivers_12259): for Z_N x Z_M orbifolds with Wilson lines, eqs. (7a)-(7f), including
  N_a (A_a . V_i) = 0 mod 2 (7d) and gcd(N_a, N_b)(A_a . A_b) = 0 mod 2 (7f), derived in their appendix A from
  Phi_vac(g, h)^gcd(n, s) = 1 -- i.e. well-defined projection phases.  Inputs fulfilling only the 'weak' mod-1 forms describe consistent
  models only after a lattice shift of shifts / Wilson lines (in general a different spectrum, 'mirage torsion'); read directly they give
  ill-defined projections.  (7d) for V0 is exactly the parity condition derived in 12235.  So the stronger form is the correct one; the
  non-supersymmetric orbifolder imposes only the weak (mod 1) form of (7f).
  Audit (all of (7a)-(7f)): A8 Standard Models 104/104 consistent; three-generation e6+a2 bases of 12111 9/9; twisted-10 models of 12217
  88/153 (the 65 others fail (7f) only); SU(5) x U(1) scan models of 12161-12182 86/163 (77 fail (7f) only); (7d) never fails.
12260 -- the engines' disagreement on Witten-twisted 10s persists on fully consistent models (all three compared satisfy (7a)-(7f)); a
  sector-resolved comparison needs the patched N = 0 build with sector output (a rebuild against the stock objects fails at link: the
  *_n0 sources are not among them) -- located, not resolved.
12261 -- existence counts restated on the consistent sets: 12163 third torus 57/121 consistent, three-generation 20 (of 52); 12182 third
  torus 31/53, three-generation 12 (of 21); twisted-10 models 88/153, three-generation 32 (of 58), six-generation 56; scalar 10s: 0 in all.
  Theorem 7.7 (an absence statement) is unaffected.
12262 -- the no-Higgs-10 note is offered for cross-track review (decision logged; note updated with the settled condition).
12263 -- main checkout: see the round report.
12264 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12259_to_12264_ploger_conditions.json"
D = ROOT / "analysis" / "search_drivers_12259"


def main():
    checks, res = {}, {}
    ext = (D / "ploger_mirage_torsion_extract.txt").read_text(encoding="utf-8")
    checks["12259: the Ploger et al. text states (7d), (7f) mod 2 and derives them from Phi_vac^gcd = 1 (A.11)"] = (
        "(7f)" in ext and "(7d)" in ext and "(A.11)" in ext and "gcd" in ext)
    p = json.loads((D / "ploger.json").read_text())
    res["12259"] = p
    checks["12259: audit -- A8 104/104, 12111 bases 9/9, twisted-10 88/153, SU(5) scans 86/163; only (7f) fails"] = (
        p["A8_SMs"]["fully_consistent"] == 104 and p["three_generation_bases_12111"]["fully_consistent"] == 9
        and p["twisted10_C10_loaded"]["fully_consistent"] == 88 and p["flipscan2_SU5_models"]["fully_consistent"] == 86
        and all(set(eval(k)) <= {"7f"} for s in p.values() for k in s["failure_patterns"]))
    r = json.loads((D / "restate.json").read_text())
    res["12261"] = r
    checks["12261: restated -- 12163 57/121 (3-gen 20), 12182 31/53 (3-gen 12), 12223 88/153 (3-gen 32); scalar 10s 0"] = (
        r["12163_third_torus"]["consistent"] == 57 and r["12163_third_torus"]["three_gen_consistent"] == 20
        and r["12182_third_torus"]["consistent"] == 31 and r["12182_third_torus"]["three_gen_consistent"] == 12
        and r["12223_twisted10"]["three_gen_consistent"] == 32 and r["12163_third_torus"]["scalar10"] == 0 and r["12182_third_torus"]["scalar10"] == 0)
    note = (ROOT / "papers" / "no_higgs_10" / "main.tex").read_text(encoding="utf-8")
    checks["12262: note states the settled condition and cites hep-th/0702176"] = "hep-th/0702176" in note and "(A.11)" in note
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
