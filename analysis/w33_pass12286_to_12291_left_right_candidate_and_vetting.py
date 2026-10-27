"""Passes 12286-12291: a tachyon-free, chirally three-generation left-right candidate on non-SUSY Z6-II; vetting the twelve Z2xZ6-I
brothers; the literature (Claude track).

12286 -- the left-right lead.  Tachyon-free Scherk-Schwarz brother (lattice-valued W6, V0.lam odd) of Z6II_60_SM_20260917_810_v9
  (v4 gives the same chiral content): gauge SU(3) x SU(2)_a x SU(2)_b x SU(8) x U(1)^5; strict engine: 466 fields, T_NFIELDS 0
  (parent: 16 tachyonic), anomaly check passes.  Taking SU(2)_L = SU(2)_a (the factor whose doublets are not halved) and
  Y = T3R + Y', Y' in the span of the five U(1)s, the quark conditions Y'(+-3,2,1) = Y'(+-3,1,2) = +-1/6 leave one free direction t;
  at t = -1/148 (the unique scanned value making the t-dependent colour triplet a quark with no chiral fractional charge) the net chiral
  content is exactly three Standard-Model generations: Q 3; u_R 3 (2 in SU(2)_R doublets + 1 singlet); d_R 3 (2 + 1); L 3;
  e_R 3 (2 + 1); nu_R 2 -- and no chiral state of fractional electric charge.  Higgs candidates: 14 SU(2)_L doublets with |Y| = 1/2,
  10 bidoublets, 14 SU(2)_R doublets with |Y'| = 1/2 (to break SU(2)_R x U(1) to Y).  Tr Y = 0.  k_Y = 8/3 (lattice-vector norm,
  checked on every weight to 2e-12), i.e. sin^2 theta_W = 3/11 at the string scale.  Caveats: 96 fermion and 102 scalar fields of
  fractional charge (vector-like) must be lifted; tachyon-free at the orbifold point only (moduli not studied); the parent's
  SM-analyser identification (12180) picks the other SU(2), whose doublets are halved -- 12180's lemma is not contradicted, the
  closure 'no three-generation Scherk-Schwarz interpolation' assumed that identification; the potential is not computed.
12287 -- the 12 Z2xZ6-I brothers and their parents: levelprobe (orbifolder 1.2.1) dumps; every renormalisable q l bd and bu bd bd
  checked for gauge + space-group invariance by the engine, then the R rule sum (q_sh + osc) = -1 mod (2, 6, 6).  The R rule removed
  nothing in any model (no positive control: counts are upper bounds from gauge + space group).  Brothers do not systematically help.
  Three lineages (SM_128, SM_808, SM_2579; parents and brothers alike) have no renormalisable QLd (128 also no udd); the other nine
  have renormalisable QLd and udd and fail the 11829-type proton test.
12288 -- literature: brother models and generalized (fixed-point dependent) discrete torsion are established (Ploger, Ramos-Sanchez,
  Ratz, Vaudrevange hep-th/0702176; the Bonn theses arXiv:0812.3503, 0812.3560; Z2xZ2 torsion after resolution arXiv:2211.01397).  So the
  12282 coprime-order rule is a restatement of known constraints, verified here on the corpus; the novelty of 12274-12287 is the corpus
  censuses, the 12 Z2xZ6-I brothers (new to the corpus; no Z2xZ6-I brother catalogue found) and the left-right candidate.
12289 -- the rule on an unseen geometry: not done this round.
12290 -- bug report (not sent) and the main-checkout file: user decisions, still open.
12291 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12286_to_12291_left_right_candidate_and_vetting.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    sc = json.loads((A / "search_drivers_12286" / "lr_scan.json").read_text())
    c = sc["candidates"]["-1/148"]
    nc = {k: v for k, v in c["net_chiral"].items()}
    res["12286_net_chiral_doubled"] = nc
    # the engine lists each fermion and its conjugate: counts are doubled
    half = {k: v // 2 for k, v in nc.items()}
    checks["12286: at t = -1/148 the net chiral content is three SM generations (+2 nu_R), no chiral fractional charge"] = (
        c["chiral_fractional"] == 0 and half.get("(3, 2, 1, 1/6)") == -3 and half.get("(3, 1, 2, 1/6)") == 2
        and half.get("(3, 1, 1, -1/3)") == 1 and half.get("(3, 1, 1, 2/3)") == 1 and half.get("(1, 2, 1, 1/2)") == 3
        and half.get("(1, 1, 2, 1/2)") == -2 and half.get("(1, 1, 1, 1)") == -1 and len(half) == 7)
    checks["12286: the other scanned t values all leave chiral fractional charges"] = all(
        v["chiral_fractional"] > 0 for k, v in sc["candidates"].items() if k != "-1/148")
    h = json.loads((A / "search_drivers_12286" / "lr_higgs.json").read_text())
    res["12286_higgs"] = h
    checks["12286: Higgs candidates present, Tr Y = 0; vector-like fractional states recorded"] = (
        h["TrY"] == "0" and h["higgs_scalars"].get("SU2_L doublet, |Y| = 1/2", 0) > 0
        and h["higgs_scalars"].get("SU2_R doublet, |Y'| = 1/2", 0) > 0 and h["fractional_fermion_fields"] == 96)
    k = json.loads((A / "search_drivers_12286" / "lr_ky.json").read_text())
    res["12286_kY"] = k["kY"]
    checks["12286: k_Y = 8/3"] = k["kY"] == "8/3"
    v = json.loads((A / "search_drivers_12287" / "vet.json").read_text())
    res["12287"] = v
    noQLd = sorted({m.split("__")[0] for m, r in v.items() if r["allowed"].get("QLd gauge+SG", 0) == 0})
    res["12287_no_renormalisable_QLd"] = noQLd
    checks["12287: exactly three lineages without renormalisable QLd (parents and brothers alike)"] = noQLd == [
        "SM_20260926_128_23", "SM_20260926_2579_27", "SM_20260926_808_24"] and all(
        (v[m + "__odd"]["allowed"].get("QLd gauge+SG", 0) == 0) == (v[m + "__ctrl"]["allowed"].get("QLd gauge+SG", 0) == 0)
        for m in {x.split("__")[0] for x in v})
    checks["12287: the R rule removed nothing (recorded as an unverified filter)"] = all(
        r["allowed"].get(kk + " gauge+SG", 0) == r["allowed"].get(kk + " gauge+SG+R", 0) for r in v.values() for kk in ("QLd", "udd"))
    checks = {kk: bool(vv) for kk, vv in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
