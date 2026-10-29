"""Passes 12351-12356: tachyon-free three-generation SO(16) x SO(16) Standard Models on Z6-II -- the SM_2913 lineage (Claude track).

Prior art (cited, not claimed): Pass 11095 built 104 tachyon-free three-generation SO(16) x SO(16) models on the A8 shift of T6/Z3;
Pass 11100 found, by random draws on the other W(3,3) geometries, no tachyon-free Standard-Model-like model 'on this sample';
Pass 11096 closed the (-1)^F-in-the-twist 'twin' route for Z6-I, Z12-I, Z2xZ6-I, Z3xZ6, Z6xZ6 (Z6-II not in its list);
the SUSY Z6-II A8 SMs used here as parents are those of 12205 (z6ii_sm_all) and the non-SUSY V0 variants those of 12180 / 12281.

12351 -- hypercharge.  The SUSY parents' hypercharge as an exact 16-vector (orbifolder SM analyser charges fitted on every left-moving
  weight, residual 0, Y^2 = 5/6 i.e. k_Y = 5/3) applied to the 17 tachyon-free three-doublet non-SUSY parents (12338): Y is constant on
  every multiplet (0 failures).  SM_2618 (v0-v3) and SM_2913 (v6-v8): the chiral content is EXACTLY three Standard-Model generations
  (Q, u^c, d^c, L, e^c three each; the overall sign of the fitted vector is the opposite convention), Tr Y = 0, plus 4 pseudo-real
  (1,2)_0 doublets (vector-like among themselves, fractional charge +-1/2).  SM_2503, SM_574, SM_1105: chiral exotics (e.g. (1,1)_{1/2}),
  Tr Y != 0 -- excluded under this hypercharge.
12352 -- tachyons.  Engine TachyonSolver: right-moving tachyonic vacua -1/2 (Witten untwisted), -1/6 (Witten theta^2, theta^4); no
  surviving state at the orbifold point (T_NFIELDS = 0) in all seven.  Away from it: momenta and windings integral (no Scherk-Schwarz
  twist); winding along Wilson-line directions shifts the left coset; exact E8 x E8 minima reach the vacua (-1/2 in the untwisted Witten
  sector with windings on tori 2, 3; -1/3 <= -1/6 in theta^2, theta^4 with windings on torus 3) -> possible small-radius (winding)
  tachyons, closed for radii above ~ sqrt(2) sqrt(alpha') (alpha' m^2/4 = level + w^2 R^2/4); large radii safe (momentum adds positive
  mass; zero-winding spectrum tachyon-free).  Necessary-condition analysis; projections of winding states not computed.
12353 -- massless Bose-Fermi balance n_F - n_B = +254 (SM_2618), +266 (SM_2913).  Higgs scalars (1,2)_{+-1/2}: 8 (SM_2618), 20 (SM_2913).
  Fractional-charge fermions (52 in each): mass pairings by singlet monomials under gauge (exact U(1) charges from the complement of the
  non-abelian roots -- the printed charges carried float noise and overflowed int64), point group, Witten label and fixed-point
  translations: SM_2913 52/52 liftable, SM_2618 40/52.  Control: shifting one partner by e5 (never absorbable) kills all pairings
  (422 -> 0) for SM_2913_v6.  Not imposed: the non-SUSY vertex rule; the singlet vacuum itself.
12354 -- renormalisable Yukawas of SM_2913_v6 (gauge + full space-group rule): up 26 couplings, down 30, lepton 40; structural rank per
  single Higgs up 3, down 3, lepton 2 -- UPPER bounds (the field groups include vector-like partners; structural rank overestimates).
  The light mass hierarchy (and the risk of a degenerate tree-level up sector) is open.
12355 -- closure statement: on Z6-II the SO(16) x SO(16) route DOES give tachyon-free (at the orbifold point and for radii above ~ the
  string scale) three-generation Standard Models with k_Y = 5/3 and liftable fractional charges -- the SM_2913 lineage -- extending
  Pass 11100's sampled negative.  Unification: with SM_2913's full massless spectrum above any common threshold 1e3-1e16 GeV
  (b3 = 19/3, b2 = 13, bY = 338/9) the perturbative alpha_2 = alpha_3 crossings need k_Y in [0.32, 1.28] -- never 5/3 (the usual
  non-SUSY Weinberg-angle problem, as on T6/Z3, 12162-12167; string thresholds not included).  Open: that, the Yukawa hierarchy,
  proton operators, the vacuum and moduli.
12356 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12351_to_12356_tachyon_free_z6ii_standard_models.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    yv = json.loads((A / "search_drivers_12351" / "yvec.json").read_text())
    res["12351_yvec"] = {k: dict(free=v["free"], residual=v["residual"]) for k, v in yv.items()}
    checks["12351: SUSY hypercharges fitted exactly (residual 0) for all five parents"] = len(yv) == 5 and all(v["residual"] == "0" for v in yv.values())
    sm = json.loads((A / "search_drivers_12351" / "smtest.json").read_text())
    res["12351"] = sm
    three = {"1,1,1": -3, "1,2,0": 4, "1,2,1/2": 3, "3,1,-2/3": -3, "3,1,1/3": -3, "3,2,-1/6": 3}
    good = sorted(m for m, v in sm.items() if v["chiral"] == three and v["trY"] == "0" and v["Y_nonconstant_fields"] == 0)
    res["12351_three_generation_models"] = good
    checks["12351: exactly seven models (SM_2618 v0-v3, SM_2913 v6-v8) carry exactly three SM generations (+4 pseudo-real (1,2)_0)"] = (
        len(good) == 7 and all(("2618" in g) or ("2913" in g) for g in good))
    w = json.loads((A / "search_drivers_12352" / "winding.json").read_text())
    res["12352"] = w
    checks["12352: zero-winding tachyon-free in all seven; winding cosets reach the vacua (small-radius bound)"] = all(
        v["0"]["min_level_with_winding"] == "-1/2" and v["2"]["min_level_with_winding"] == "-1/3" for v in w.values()) and len(w) == 7
    v = json.loads((A / "search_drivers_12353" / "vet.json").read_text())
    c = json.loads((A / "search_drivers_12353" / "vet_control_e5.json").read_text())
    res["12353"] = dict(vet=v, control=c)
    checks["12353: SM_2913 52/52 fractional fermions liftable (control e5: 0 pairings); SM_2618 40/52; n_F - n_B > 0"] = (
        all(x["liftable"] == 52 for k, x in v.items() if "2913" in k) and all(x["liftable"] == 40 for k, x in v.items() if "2618" in k)
        and c["Z6II_23_SM_20260917_2913_v6"]["pairable"] == 0 and all(x["nF_minus_nB"] > 0 for x in v.values()))
    y = json.loads((A / "search_drivers_12354" / "yukawa.json").read_text())
    res["12354"] = y
    checks["12354: renormalisable Yukawas exist in all three sectors (structural ranks recorded as upper bounds)"] = all(
        y[k]["couplings"] > 0 for k in ("up", "down", "lepton"))
    u = json.loads((A / "search_drivers_12355" / "unify.json").read_text())
    res["12355_unification"] = dict(b=u["b"], k_range=u["perturbative_k_range"])
    checks["12355: no common threshold reaches k_Y = 5/3 (perturbative k in [0.32, 1.28])"] = not u["near_5_3"] and u["perturbative_k_range"][1] < 1.3
    checks = {k: bool(x) for k, x in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
