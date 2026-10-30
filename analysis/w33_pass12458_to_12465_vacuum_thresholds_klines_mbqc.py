"""Passes 12458-12465 (Claude track).

12458 -- SM_2541 vacuum: the anomalous-U(1) FI term is cancelled by the 42 full singlets alone (exact: q(T_anom) lies in the rational span
  of the singlet charges, rank 6 = 6; the homogeneous D-flat cone has full support, so cone = span), for either FI sign, with EVERY
  singlet switched on; in that D-flat direction all fractional states lift (Dirac + Majorana).  Family-wide in the certificate.  An LP with
  box bounds v <= 10 and c = 1 first returned an empty support -- a scale artefact caught by the exact span check (see the md).
  Not computed: the non-SUSY one-loop potential, its minimisation and the VEV sizes; F-terms do not exist.
12459 -- SM_2541 unification: large-volume DKL thresholds with the 6D coefficients of BOTH fixed tori (Wilson lines on the fixed torus
  off), exact 3x3 solve per hypercharge and the best physical (x_i >= 0, 1/alpha_s >= 0) NNLS fit.  c22: no physical solution for any of
  its six anomaly-free hypercharges; best physical residual >= 33.9 in 1/alpha (control: SM_2913 reproduces 12359's 9.72).
12460 -- k-line lemma: a sum of k distinct lines of a GQ of order (q,q) has weight >= k(q + 2 - k); >= 2q for 2 <= k <= q, and (no-triangle
  step) >= min(2q + 2, q^2 + 1) for k = q + 1.  So every kernel word of W(3,q) needing at most q + 1 lines has weight >= 2q.  Contains the
  other track's exhaustive q = 7 three-line result (7d27e910c) as k <= 3.  Exhaustive at q = 3 up to k = 6 (min weight 6, 8, 8, 8, 8).
12461 -- smallest deficient region at q = 5: counting lemma |R| >= (q+1)(q+1-|x|) + |x| + t (so |x| <= q forces |R| >= 2q + 1), used as
  CP-SAT cuts; status in the certificate.
12462 -- MBQC: (i) embedding lemma -- every N-vertex graph is an induced subgraph of the collinearity graph of W(2N-1, q), any q, so Pauli
  (Z) measurements on W graph states reach every graph state; (ii) but the extractable cut-rank is capped by the ceiling
  1 + C(2n+p-2, 2n-1), polylog in v for fixed p: W(2n-1,p) graph states are classically simulable in time v^{O(log^{p-2} v)}-type
  (quasi-polynomial for p = 3; polynomial for p = 2) via Schmidt-rank-width simulation -- universal only with super-polynomial overhead,
  sharpening 12445; (iii) induced cluster grids: W(3,2), W(3,3) max 2x3 (no 3x3), W(5,2) no 3x3, W(5,3) has 3x3, W(3,5) has 4x5 and more.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12458_to_12465_vacuum_thresholds_klines_mbqc.json"
A = ROOT / "analysis"


def j(p):
    return json.loads((A / p).read_text())


def main():
    checks, res = {}, {}
    sp_ = j("search_drivers_12458/span_Z6II_06_SM_20260917_2541_c22.json")
    dc = j("search_drivers_12458/dflat_controls_Z6II_06_SM_20260917_2541_c22.json")
    vc = j("search_drivers_12458/vacuum_Z6II_06_SM_20260917_2541_c22.json")
    res["12458_c22"] = dict(span=sp_, controls=dc, vacuum=vc)
    checks["12458: c22 -- q(T_anom) in the span of the 42 singlet charges (rank 6 = 6), homogeneous cone full (42), FI support 42 for both signs"] = (
        sp_["rank_singlet_charges"] == sp_["rank_with_anomalous"] == 6 and dc["homogeneous_support"] == 42 and vc["support"] == 42
        and vc["support_opposite_FI_sign"] == 42)
    checks["12458: negative control -- a target outside the singlet span gives empty support (the LP can say no)"] = dc["control_outside_span_support"] == 0
    checks["12458: c22 -- in the all-singlet D-flat direction every fractional state lifts (90 Dirac + 2 Majorana = 92)"] = (
        vc["dflat_support"] == dict(fractional=92, dirac=90, majorana=2, liftable=92))
    m11 = j("search_drivers_12458/lift_c22_kY11_3_maj.json")
    checks["12458: c22 with its lowest hypercharge k_Y = 11/3 -- all 52 fractional states liftable with Majorana (2 self-masses)"] = (
        m11["fractional"] == 52 and m11["liftable_with_majorana"] == 52 and m11["majorana_rescued"] == 2)
    fam = j("search_drivers_12459/family52.json")
    res["12458_12459_family"] = fam
    checks["12458: all 52 SM_2541 models -- full-singlet D-flat support and every fractional state lifted in that vacuum"] = (
        len(fam) == 52 and all(r["dflat_support"] == r["singlets"] and r["liftable_in_vacuum"] == r["fractional"] for r in fam.values()))
    th = j("search_drivers_12459/thresholds_c22.json"); nn = j("search_drivers_12459/nnls_c22.json")
    res["12459_c22"] = dict(exact=th, nnls=nn)
    checks["12459: control -- the NNLS fitter reproduces 12359's SM_2913 residual 9.72"] = abs(nn["control_SM2913_SM"] - 9.72) < 0.01
    checks["12459: c22 -- no physical exact threshold solution for any of its 6 hypercharges (SM or full low-energy content)"] = (
        len(th) == 6 and not any(r[k]["physical"] for r in th for k in ("SM", "full")))
    checks["12459: c22 -- best physical residual >= 33.8 in 1/alpha (SM content), 3.5x SM_2913's"] = min(
        v["resid"] for k, v in nn.items() if k != "control_SM2913_SM" and "_SM_" in k) > 33.8
    checks["12459: all 52 models -- no physical exact threshold solution with the first hypercharge"] = not any(r["exact_physical"] for r in fam.values())
    res["12459_family_min_resid"] = min(r["best_physical_resid"] for r in fam.values())
    kp = j("search_drivers_12460/kline_profile_q3.json"); ke = j("search_drivers_12460/kline_extend_q3.json")
    res["12460"] = dict(profile=kp, extend=ke)
    mins = {int(k): min(int(w) for w in v) for k, v in kp["sums_of_k_lines"].items()}
    checks["12460: q = 3 -- every sum of k = 2, 3, 4 lines obeys |S| >= k(q+2-k) (0 violations); minima 6, 8, 8 >= 2q"] = (
        kp["lemma_violations"] == 0 and mins == {2: 6, 3: 8, 4: 8})
    checks["12460: q = 3 -- exhaustive k = 5, 6 (beyond the proved range k <= q + 1): minimum weight 8 > 2q"] = (
        ke["5"]["min_weight"] == 8 and ke["6"]["min_weight"] == 8)
    c3 = j("search_drivers_12452/deficit_cpsat_q3_R5_cuts.json")
    checks["12461: q = 3 control with the counting cuts -- no deficient region <= 5 (the cuts do not remove the answer 6)"] = c3["no_region_le_R"]
    p = A / "search_drivers_12452/deficit_cpsat_q5_R9_cuts.json"
    if p.exists():
        c5 = json.loads(p.read_text()); res["12461_q5"] = c5
        res["12461_status"] = "PROVED: no deficient region <= 9 at q = 5, so min region = 10 = d" if c5["no_region_le_R"] else "OPEN: " + str({k: v["status"] for k, v in c5["cases"].items()})
    em = j("search_drivers_12462/embed_lemma.json")
    checks["12462: embedding lemma verified -- 3x3 and 5x5 grids, a random 20-vertex graph and W(3,3) itself embed induced in W(2N-1,q), q = 2, 3, 5"] = all(em.values())
    G = {f.stem: json.loads(f.read_text()) for f in (A / "search_drivers_12462").glob("grid_W*.json")}
    res["12462_grids"] = {k: v["status"] for k, v in G.items()}
    st = lambda k: G[k]["status"]
    checks["12462: induced cluster grids -- W(3,2), W(3,3): 2x3 yes, 3x3 no; W(5,2): no 3x3; W(5,3): 3x3 yes; W(3,5): 4x5 yes (all found grids verified induced)"] = (
        st("grid_W3_2_2x3") == "OPTIMAL" and st("grid_W3_2_3x3") == "INFEASIBLE" and st("grid_W3_3_2x3") == "OPTIMAL" and st("grid_W3_3_3x3") == "INFEASIBLE"
        and st("grid_W5_2_3x3") == "INFEASIBLE" and st("grid_W5_3_3x3") == "OPTIMAL" and st("grid_W3_5_4x5") == "OPTIMAL"
        and all(v.get("verified_induced", True) for v in G.values()))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
