"""Passes 12241-12246: Theorem 7.7 -- no scalar 10 in any sector, exhaustively for one and two A4-type Wilson lines; the hidden
SU(5) of SM_2496 broken exactly along its scalar-10 Higgs branch; the Z6-II exception isolated (Claude track).

12241 -- the consistent subspace (V0.W even, 12235).  One line: 165,465 consistent admissible configurations (of 231,124); 294 of the
  405 twisted-10 candidates are consistent (153 load, 141 fail other engine conditions; the 111 odd ones are inconsistent) -- density
  0.178%.  Two lines, even-only sample (seed 31): 366/20,000 = 1.83% (95% CI 1.65-2.03%), 0 scalar-type.  The engine-built counts of
  12161-12182 are unaffected (every loaded model was already consistent).
12242 -- the Z6-II exception: in the Witten-twisted theta^2 and theta^4 sectors of the order-six twist the dump lists 4 bosons and 36
  fermions per sector with right-moving weights that bosons and fermions SHARE (e.g. (+-1/2, -1/6, 1/6, +-1/2)), one boson record
  identical in representation, left and right weights to a fermion record -- no function of the right-mover decides the statistics
  there, and a boson with helicity component 1/2 is unphysical: a suspected labelling artefact of the engine in these two sectors
  (not established).  No result of 12180-12240 uses them (interpolation counts and the hidden scalar 10s are Witten-untwisted).
12243 -- THEOREM (lattice, exhaustive): every consistent pair of A4-type second Wilson lines (W1 on torus 2, W2 on torus 3, both
  leaving the same A4, 3 W1.W2 integral, V0.W even) on the 7 e6+a2 bases: 77,192,286 pairs; 1,417,482 carry a twisted 10-type massless
  vector (1.84%, matching the sampled 1.83%); NONE carries a scalar one (P.V0 = w/2).  Positive control: all 366 sampled hits of 12241
  are found.  With 12217/12230/12235 (one line) and 12170 (untwisted): no scalar 10 in any sector for one or two A4-type lines.
12244 -- SM_2496: the eight roots that the shift-broken class (v9) keeps inside the hidden SU(5) of the unbroken class (v0) are exactly
  the stabiliser of one of v0's scalar-10 weights (all ten stabilisers are A2 + A1); the shift class is, at the root level, the Higgs
  branch of the hidden scalar 10 (group theory; no potential computed).
12245 -- paper: Theorem 7.7 (no 10_H) in the Section 7 subsection.
12246 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12241_to_12246_no_scalar_ten_theorem.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    ps = json.loads((A / "search_drivers_12235" / "parity_space.json").read_text())
    lf = json.loads((A / "search_drivers_12235" / "loadfail_parity.json").read_text())["one_line"]
    cons = sum(v["admissible"] - v["V0W_odd"] for v in ps.values())
    even_cand = lf.get("even|loads", 0) + lf.get("even|LOADFAIL", 0)
    res["12241"] = dict(consistent_one_line=cons, consistent_candidates=even_cand, density=even_cand / cons)
    t4 = json.loads((A / "search_drivers_12224" / "twoline4_31.json").read_text())
    res["12241"]["two_line_even_sample"] = t4
    checks["12241: consistent one-line space 165,465, 294 consistent candidates; two-line even sample 366/20000, 0 scalar"] = (
        cons == 165465 and even_cand == 294 and t4["draws"] == 20000 and t4["hits"] == 366 and t4["scalar_type_configs"] == 0)
    ex = json.loads((A / "search_drivers_12230" / "z6ii_exception.json").read_text())
    res["12242"] = ex
    checks["12242: Z6-II exception confined to 4 bosons per Witten-twisted theta^2 / theta^4 sector, one record duplicated as a fermion"] = (
        all(v["bosons"] == 4 and v["fermions"] == 36 and v["boson_records_also_listed_as_fermion"] == 1 for v in ex.values()))
    rows = [json.loads(p.read_text()) for p in sorted((A / "search_drivers_12243").glob("exhaust2_*.json"))]
    pairs = sum(r["pairs"] for r in rows); hits = sum(r["twisted10_pairs"] for r in rows); sc = sum(r["scalar10_pairs"] for r in rows)
    ctrl = sum(r["control_sampled_hits"] for r in rows); found = sum(r["control_found"] for r in rows)
    res["12243"] = dict(per_base=rows, pairs=pairs, twisted10_pairs=hits, scalar10_pairs=sc, control=[found, ctrl])
    checks["12243: exhaustive two-line: 77,192,286 consistent pairs, 1,417,482 with twisted 10s, 0 scalar; control 366/366"] = (
        len(rows) == 7 and pairs == 77192286 and hits == 1417482 and sc == 0 and ctrl == 366 and found == 366)
    hb = json.loads((A / "search_drivers_12238" / "higgs_branch.json").read_text())
    res["12244"] = hb
    checks["12244: v9's hidden roots = the stabiliser (A2 + A1) of a scalar-10 weight of v0"] = (
        hb["v0_A4_roots"] == 20 and hb["v9_roots_in_A4_span"] == 8 and hb["v9_equals_a_stabiliser"] and set(hb["stabiliser_sizes"]) == {8})
    tex = (ROOT / "papers" / "forty_points" / "sec07_realforms.tex").read_text(encoding="utf-8")
    checks["12245: Theorem 7.7 in Section 7"] = "Theorem 7.7" in tex
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
