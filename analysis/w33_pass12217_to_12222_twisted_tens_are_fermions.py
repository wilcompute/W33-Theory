"""Passes 12217-12222: twisted 10s exist but are always fermions (correcting 12208) -- no scalar 10 anywhere on the route, exhaustively;
the family triplet needs two independent order-2 Wilson lines; symmetric versus asymmetric Z3 twists; paper summary refreshed (Claude track).

12217 -- exhaustive twisted-10 analysis on the full admissible space of one A4-type second Wilson line W = (lambda, mu): the 7 e6+a2
  bases x 864 A4-type lambda x 6561 order-3 mu, with the admissibility of Pass 12161 (231,124 admissible configurations).
  Necessary condition (before any projection phase): a twisted massless 10 needs P = (P1, P2), |P|^2 = 4/3 (no oscillator; with one,
  2/3 < 6/5), |proj_A4 P1|^2 = 6/5.  The first-E8 part alone does NOT exclude it (hits with |P1|^2 = 4/3 and, in Witten-twisted
  cosets, 11/9); combined with the second-E8 class (P2 = 0 resp. |P2|^2 = 1/9 required), exactly 405 of the 231,124 configurations
  admit a twisted 10-type massless vector (four bases; three bases none).  Built as models in the non-SUSY engine: 153 load (the
  other 252 fail its consistency conditions), all SU(5) x U(1), all tachyon-free, and EVERY one carries twisted 10s -- 918 fields,
  all FERMIONS in Witten-twisted sectors; twisted scalar 10s: 0.
  CORRECTION: Pass 12208's 'no twisted 10 of either statistics' held for its 163-model sample only (the class has density 0.17%;
  the 1616-configuration lattice sample of 12212 would expect ~2.8 and saw 0).  What is true, exhaustively on this scope: the 10_H
  is absent from every sector -- untwisted by the theorem of 12170, twisted because the only twisted 10s are fermions.
12218 -- why the family-triplet parent cannot interpolate: SM_2751's untwisted roots with the actual Wilson lines are A1 + A2 + A2 + A4
  (colour A2 and family A2); with W5 = 0, W6 = 0, W6 = W5 or both zero -- every way of making an order-2 direction trivial -- only one
  A2 survives (A1^3 A2 A3 A5; A2 A4 D5; A2 A4 D5; A2 D5 E6).  The base shift gives E6 x SU(3)_family; breaking E6 to the Standard
  Model while keeping the family SU(3) needs two independent order-2 Wilson lines, which is exactly the absence of a symmetric direction.
12219 -- symmetric versus asymmetric Z3 on the native II(2,2): left-only and right-only twists (g1, g2) admit a 2-dim space of
  order-2 translations but freeze all moduli (0 invariant deformations); the symmetric rotations (g1 g2, g1 g2^-1; det(1 - g) = 9)
  admit no translation but keep 2 real moduli (one complex T).  A twisted plane carries a translation or a running radius, never
  both -- the 27-fixed-point obstruction of 12177 is the symmetric half of this dichotomy.
12220 -- cross-track: no reply on origin yet to the 12214 note (checked).
12221 -- paper: Section 9 key idea and scorecard entry 8 and Section 11 open problem 1 now cite Theorems 7.5-7.6; the Section 7 subsection
  carries the twisted-10 correction, the family-triplet reason and the asymmetric dichotomy.
12222 -- synthesis.
"""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12217_to_12222_twisted_tens_are_fermions.json"
D7 = ROOT / "analysis" / "search_drivers_12217"
D8 = ROOT / "analysis" / "search_drivers_12218"
D9 = ROOT / "analysis" / "search_drivers_12219"


def main():
    checks, res = {}, {}
    full = json.loads((D7 / "exhaust10_full.json").read_text())
    res["12217_space"] = full
    adm = sum(v["admissible_pairs"] for v in full.values())
    cand = sum(v["pairs_with_twisted_10_vector"] for v in full.values())
    checks["12217: 7 x 864 lambda, 231124 admissible configurations, exactly 405 admit a twisted 10-type massless vector"] = (
        all(v["lambdas"] == 864 for v in full.values()) and adm == 231124 and cand == 405)
    pairs = json.loads((D7 / "candidate_pairs.json").read_text())
    r = json.loads((D7 / "cand10_results.json").read_text())
    c = Counter()
    for x in r:
        for k, v in x.get("tens", {}).items():
            c[k] += v
    res["12217_models"] = dict(candidates=len(r), loaded=sum(1 for x in r if x["gauge"] != "LOADFAIL"), su5=sum(1 for x in r if "tens" in x),
                               tens=dict(c), tachyon_free=sum(1 for x in r if "tens" in x and x["tachyons"] == 0))
    checks["12217: 153 consistent candidate models, all with twisted 10s (918 Witten-twisted fermions), twisted scalar 10s: 0"] = (
        len(pairs) == 405 and len(r) == 405 and res["12217_models"]["loaded"] == 153 and res["12217_models"]["su5"] == 153
        and c.get("fermion_tw_W", 0) == 918 and not any(k.startswith("scalar") for k in c)
        and all(any("_tw" in k for k in x["tens"]) for x in r if "tens" in x))
    ro = json.loads((D8 / "roots2751.json").read_text())
    res["12218"] = ro
    checks["12218: SM_2751 has two A2 (colour, family) only with both order-2 Wilson lines; every trivial-direction choice leaves one"] = (
        ro["actual"]["A2_count"] == 2 and all(ro[k]["A2_count"] == 1 for k in ("W5=0", "W6=0", "W6=W5", "W5=W6=0"))
        and ro["W5=W6=0"]["type"] == ["A2", "D5", "E6"])
    sa = json.loads((D9 / "sym_asym.json").read_text())
    res["12219"] = sa
    checks["12219: asymmetric Z3: 2 translations, 0 moduli; symmetric Z3: 0 translations, 2 moduli (det(1 - g) = 9)"] = (
        all(sa[k]["translations_mod2"] == 2 and sa[k]["invariant_moduli"] == 0 for k in ("g1", "g2"))
        and all(sa[k]["translations_mod2"] == 0 and sa[k]["invariant_moduli"] == 2 and sa[k]["det_1_minus_g"] == 9 for k in ("g1g2", "g1g2inv"))
        and all(sa[k]["preserves_eta"] and sa[k]["preserves_H"] and sa[k]["order3"] for k in sa))
    tex9 = (ROOT / "papers" / "forty_points" / "sec09_physics.tex").read_text(encoding="utf-8")
    tex11 = (ROOT / "papers" / "forty_points" / "sec11_epilogue.tex").read_text(encoding="utf-8")
    tex7 = (ROOT / "papers" / "forty_points" / "sec07_realforms.tex").read_text(encoding="utf-8")
    checks["12221: Sections 9 and 11 cite Theorems 7.5-7.6; Section 7 carries the twisted-10 correction"] = (
        "Theorems 7.5--7.6" in tex9 and "Theorem~7.6" in tex9 and "Theorem~7.6" in tex11 and "corrects" in tex7 and "twisted fermions" in tex7)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
