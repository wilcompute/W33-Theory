"""Passes 12357-12362: sub-orbifold geometries, a large-radius tachyon correction, thresholds, the Casimir force, a minimal singlet set,
mass matrices and proton decay for the SM_2913 lineage (Claude track).

CORRECTION to 12352 (pushed in 27990054e): 'tachyon-free ... for radii above ~ sqrt(2 alpha')' and 'large radii safe' are WITHDRAWN.
The 6D theory of the theta^2-fixed torus e5e6 has tachyons (m_R^2 = -1/6, Witten theta^2 / theta^4 sectors) that the order-2 Wilson line
W5 removes only at zero momentum: they carry half-integer e5 momentum and return for R5 > sqrt(3/8) sqrt(alpha') -- the same threshold as
the torsion window of 12322, here produced by the Wilson line itself.  12352 had assumed integer momenta.

12357 -- mass matrices with the vector-like states (rows Q + Ubar, cols Qbar + U, etc.), minimal singlet degree per entry, light masses
  Froggatt-Nielsen style (random O(1) coefficients x eps^d, M_s >> v).  All ten Higgs choices give three nonzero light masses per sector.
  With all 80 singlets every degree is <= 5 and the hierarchy is at most ~1.5 decades; with the 6-singlet set of 12360 and eps = 0.1 the
  best choice (H6) gives the top O(1) and the down sector near the observed (s, b), but charm ~1.8 decades and up ~2.6 decades too heavy,
  and e, mu too heavy.  Control: at degree 0 the MILP agrees with 12354's independent coupling test on 4080/4080 triples (48 allowed).
12358 -- proton decay.  B - L is a gauged U(1), anomaly-free for every choice of its one free parameter (gravitational, cubic, SU(3)^2,
  SU(2)^2, Y^2 all identically 0); baryon number is not gauged.  Delta B = Delta L = 1 four-fermion operators: QQU*E*, QLU*D* at singlet
  degree 0, QQQL, UUDE at degree 2 (all conserve B - L; suppressed by M_s^2 ~ (3e17 GeV)^2, harmless).  One of 16 colour-triplet scalars
  couples renormalisably to both QQ/UD and QL/UE and must be heavy.  The 6-singlet set has B - L = 0 exactly (U(1)_{B-L} unbroken: a
  massless Z'); 14 singlets carry B - L = +-2 and break it to matter parity (all SM fermions have odd 3(B - L)).
12359 -- sub-orbifolds.  Geometry files for the Witten x theta^s sub-orbifolds (s = 2: e5e6 fixed; s = 3: e3e4 fixed) generated from the
  space group; s = 1 regenerates the shipped Z6-II geometry and reproduces SM_2913_v6 state for state (788/788, weights included); both
  sub-orbifolds' 4D fermions are exactly vector-like (0 unpaired weights; the chiral parent: 214) as their 6D origin requires; Wilson-line
  -on spectra are weight-level subsets of Wilson-line-off ones (0 violations); a geometry with the fixed-torus translations deleted is
  rejected by the engine.  Census over the 99 tachyon-free parents: torus e5e6 has 6D tachyons in 52 (all W5-shifted: 0 with the Wilson
  line on), including all seven three-generation models (SM_2618: 24, SM_2913: 12); torus e3e4 has none in all 99.  The only
  three-doublet parent clean on both tori is SM_1105_v12 (chiral exotics under its parent's hypercharge, 12351).
  Thresholds (DKL large-volume form, coefficients = 6D content, c_i = |G_i|/|G|): b(e5e6) = (80/3, 16, 16) = 16 (5/3, 1, 1) -- exactly
  universal, so that torus cannot move sin^2 theta_W (cf. 12156 for T6/Z3); b(e3e4) = (716/9, 220/3, 124/3) has the wrong pattern: no
  fit reaches the data (residual >= 8.7 in 1/alpha with SM-only running, >= 30 with the full spectrum).  Control: the weight method
  reproduces 12355's parent coefficients (19/3, 13, 338/9) exactly.
12360 -- a minimal singlet set: 6 of the 80 SM-singlet scalars (ids 233, 294, 363, 382, 770, 771) give full structural rank to every
  vector-like and fractional block (Q 3, U 3, D 3, L 4, E 3, X 4, F 20, Z 4); dropping any one breaks a block; 1/100 random 6-sets work.
  Sufficient structural set, not a solved vacuum (no potential minimised; structural rank is an upper bound for non-generic coefficients).
12361 -- Casimir force on the tachyon-free torus e3e4: phases P.W3, P.W4 validated against the engine (the phase-0 components ARE the
  Wilson-line-on spectrum, 1376/1376); E(1/3,1/3) = -4/9 exactly (index-3 sublattice); N_B,eff - N_F,eff = -304 + 1984/9 = -752/9 < 0:
  the Casimir energy is positive and the torus decompactifies unless the 6D vacuum energy A Lambda_6 (not computed) is positive.  Torus
  e5e6 is confined to R5 < sqrt(3/8) by its tachyons (string scale), where no field-theory estimate applies.
12362 -- synthesis.  Upper bounds throughout 12357/12358/12360: the non-SUSY vertex (H-momentum) rule, calibrated in Pass 11097, is not
  imposed, so 'allowed' may still be forbidden.
"""

import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12357_to_12362_sub_orbifolds_thresholds_vacuum_proton.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    s = json.loads((A / "search_drivers_12359" / "summary.json").read_text())
    res["12359_validation"] = {k: v for k, v in s.items() if k != "census"}
    res["12359_census"] = s["census"]
    checks["12359: regenerated Z6-II geometry reproduces SM_2913_v6 state for state; sub-orbifold fermions vector-like; subset relation"] = (
        s["regenerated_parent_identical"] and s["parent_states"] == 788 and s["vectorlike"]["sub2"]["vectorlike"]
        and s["vectorlike"]["sub3"]["vectorlike"] and not s["vectorlike"]["parent"]["vectorlike"]
        and s["subset_e5e6"]["violations"] == 0 and s["subset_e3e4"]["violations"] == 0 and s["bad_geometry_fields"] == 0)
    c = s["census_summary"]
    checks["12359: correction -- e5e6 6D tachyons (all W5-shifted) in 52/99 parents incl. all seven 3-gen models; e3e4 clean in 99/99"] = (
        c["parents"] == 99 and c["e5e6_tachyonic"] == 52 and c["e5e6_all_shifted"] and c["e3e4_tachyonic"] == 0
        and len(c["three_generation_models"]) == 7 and all(v > 0 for v in c["three_generation_models"].values())
        and s["verbose_T_NFIELDS"]["sub2_noW5"] == 12 and s["verbose_T_NFIELDS"]["sub2"] == 0)
    b = json.loads((A / "search_drivers_12359" / "beta.json").read_text())
    th = json.loads((A / "search_drivers_12359" / "thresholds.json").read_text())
    res["12359_beta"] = b; res["12359_thresholds"] = th
    bB = [F(b["sub2_noW5"][k]) for k in ("bY", "b2", "b3")]
    checks["12359: weight-method control (19/3, 13, 338/9); e5e6 coefficients exactly 16 (5/3, 1, 1); no threshold fit is feasible"] = (
        b["parent"] == {"b3": "19/3", "b2": "13", "bY": "338/9"} and bB == [16 * F(5, 3), 16, 16]
        and not any(v["feasible"] for v in th["fits"].values()) and min(v["max_resid_inv_alpha"] for v in th["fits"].values()) > 8)
    cs = json.loads((A / "search_drivers_12359" / "casimir.json").read_text())
    res["12361"] = cs
    t = cs["tally"]
    neff = (F(t["B,0,0"]) - F(t["F,0,0"])) + F(-4, 9) * (F(t["B,1/3,1/3"] + t["B,2/3,2/3"]) - F(t["F,1/3,1/3"] + t["F,2/3,2/3"]))
    res["12361_N_eff_exact"] = str(neff)
    checks["12361: phases validated (phase-0 = Wilson-line-on); E(1/3,1/3) = -4/9; N_eff = -752/9 (decompactifying Casimir force)"] = (
        cs["validated"] and abs(cs["E"]["1/3,1/3"] + 4 / 9) < 1e-6 and neff == F(-752, 9) and abs(cs["N_eff"] - float(neff)) < 1e-4)
    D = A / "search_drivers_12357"
    ctl = json.loads((D / "control.json").read_text())
    y6 = json.loads((D / "yuk6.json").read_text())
    res["12357_control"] = ctl
    res["12357_light_log10_vac6"] = {h: {sec: v[sec]["light"] for sec in v} for h, v in y6.items()}
    h6 = y6["H6_id375_conj"]
    checks["12357: control 4080/4080; three nonzero light masses per sector for all ten Higgs; H6 eps=0.1: top O(1), charm too heavy"] = (
        ctl["disagree"] == 0 and ctl["agree"] == 4080 and ctl["positives"] == 48
        and all(v[sec]["n_light_nonzero"] == 3 for v in y6.values() for sec in v)
        and h6["up"]["light"]["0.1"][2] > 1 and h6["up"]["light"]["0.1"][1] / h6["up"]["light"]["0.1"][2] > 10 ** -1.5)
    vac = json.loads((D / "vacuum.json").read_text()); vc = json.loads((D / "vacuum_check.json").read_text())
    res["12360"] = dict(vacuum=vac, check=vc)
    checks["12360: 6 singlets give full structural rank to every vector-like/fractional block; each necessary; random 6-sets 1/100"] = (
        len(vac["vacuum"]) == 6 and vc["fresh"] and all(not v["full"] for v in vc["drop_one"].values()) and vc["random_hits"] <= 2
        and all(a >= bb for a, bb in vac["rank"].values()))
    p = json.loads((D / "proton.json").read_text()); bl = json.loads((D / "bminusl.json").read_text())
    res["12358"] = dict(proton={k: v for k, v in p.items() if k != "triplet_scalars"}, b_minus_l=bl)
    checks["12358: B-L gauged and anomaly-free, unbroken by the 6-set (14 singlets with B-L=+-2); B not gauged; dim-6 ops at degree 0-2"] = (
        p["gauged_B-L"] and not p["gauged_B"] and all(x == "0" for x in bl["anomalies"].values())
        and all(x == "0" for x in bl["vacuum_3BL"].values()) and len(bl["even_nonzero_singlets"]) == 14
        and p["op_QQUcEc"]["vac6"] == 0 and p["op_QQQL"]["vac6"] == 2 and p["triplets_with_diquark_and_leptoquark_couplings"] == 1)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
