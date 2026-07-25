#!/usr/bin/env python3
"""Pass 875: intake audit of the seven-thread external batch.

An external contribution ("Pass 872 -- Secrets Unlocked: 7 Perpendicular
Threads", now in the tree as papers/@Academic @GitHub Keep going, think outside
the bo.md) proposes seven claims.  CLAUDE.md requires that batched claims be
audited AT INTAKE, not after they propagate.  This pass does that.

THE HEADLINE IS REDISCOVERY.  Threads 2 and 4 -- the Ihara zeros on the circle
|u| = 1/sqrt(11), the phases +-72.45 and +-127.09 degrees, and their photonic
measurability -- are ALREADY IN w33_paper.tex, and not in passing:

  * Corollary cor:ramanujan states every complex Hashimoto eigenvalue satisfies
    |u|^2 = k-1 = p_Ih = 11;
  * the remark titled "Phase angles and the photonic predictions" gives
    theta_gauge = arctan sqrt(Phi_4) ~ 72.45 deg and
    theta_chiral = pi - arctan(sqrt(Phi_6)/lambda) ~ 127.09 deg, and states they
    are "in principle measurable as substrate-predicted interference fringes" in
    a photonic implementation;
  * a whole subsection gives the closed-form Ihara zeta and the
    "Ihara--Ramanujan circle" |u| = 1/sqrt(11).

Both angles are recomputed from scratch here (from the Ihara--Bass quadratic
1 - lambda u + (k-1)u^2 = 0 at lambda = 2 and -4) and agree to the stated
precision.  The batch's "perpendicular secret" is the paper's own remark,
including its photonic framing.  This is failure mode 5 of CLAUDE.md, the one
that "cannot be self-checked ... only searched for".

WHAT IS FALSE.

  * Thread 6's Cabibbo formula.  It asserts theta_12 ~ 13.1 deg "as a projection
    of phi_gauge/h = 72.45/12 x pi/pi".  But 72.45/12 = 6.04, and pi/pi = 1, so
    the stated expression evaluates to 6.04 deg against a PDG value of 13.04 deg.
    The formula is arithmetically false as written, off by 7 degrees.
  * Thread 6's CP phase.  delta_CP = 72.45 deg is offered as matching experiment
    "to within experimental error"; the PDG CKM value is about 68.5 deg with an
    uncertainty of a few degrees, so 72.45 is roughly 4 degrees high -- a
    borderline, not a match, and it is presented as the batch's "biggest
    potential prediction".
  * Thread 3's "tightest possible Ramanujan gap".  Saturating the bound requires
    a nontrivial eigenvalue of modulus 2 sqrt(k-1) = 2 sqrt(11) = 6.633..., which
    is irrational; an SRG has integer eigenvalues, so no SRG can achieve it.
    W(3,3) IS Ramanujan (max nontrivial modulus 4 < 6.633), which is the true and
    weaker statement the paper already makes.
  * Thread 7's "40 deep holes".  The Conway--Parker--Sloane classification gives
    23 deep-hole classes in the Leech lattice, one per Niemeier lattice -- the
    batch's own Thread 1 uses the number 23 for exactly this.  "The 40 vertices
    correspond to the 40 deep holes" contradicts it.

WHAT IS TRUE BUT CARRIES NO W(3,3) CONTENT.

  * 196560 = 240 x 819 (checked).  This is division, not a theorem; the claim
    that it "has never been stated in the literature" is not evidence of depth.
  * 23 = q^q - mu = 27 - 4 (checked).  With six free W(3,3) parameters, hitting
    23 is unconstrained -- this is the numerology pattern the repo has retracted
    before.
  * McKay--Thompson 2B coefficients 276 = 240 + 36 and 2048 = 2^11 (checked).
    Every power of two is a power of two; nothing ties 2^11 to the valency.

THE ONE LIVE ITEM.  Thread 2's angle is arctan sqrt(Phi_4) with Phi_4 = Phi_4(3)
= 3^2 + 1 = 10, and Phi_6(3) = 7 for the chiral angle -- verified here from the
Ihara--Bass discriminants (4(k-1) - lambda^2)/4 = 10 and 7.  The integer 10 also
appears as the three-primary rank in four separate lattice computations, where
Pass 828 shows it is the F_3 coalescence rank of the collision class {2,-4}.
Whether the Ihara Phi_4(3) and the coalescence rank are the same 10 or two
different tens is OPEN and is not asserted either way here; they arise from
different constructions (a spectral discriminant versus a mod-3 collision rank).

BOUNDARY.  This pass audits claims; it does not evaluate the batch's Yang--Mills
or umbral-moonshine framing beyond the specific checkable assertions above.
Thread 3's discrete spectral gap is real arithmetic, but a finite graph's
spectral gap is not a statement about continuum Yang--Mills, and no such
implication is certified here.
"""
from __future__ import annotations

import argparse
import cmath
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass875_seven_thread_batch_intake_audit.json"
PAPER = ROOT / "w33_paper.tex"

K_DEG = 12          # W(3,3) valency
EIGS = [12, 2, -4]  # adjacency spectrum of SRG(40,12,2,4)


def ihara_roots(lam, k=K_DEG):
    """Roots of 1 - lam u + (k-1) u^2 = 0."""
    q = k - 1
    disc = lam * lam - 4 * q
    return [(lam + s * cmath.sqrt(disc)) / (2 * q) for s in (1, -1)]


def part_A_rediscovery(checks):
    """Threads 2 and 4 are already in the main paper."""
    text = PAPER.read_text(encoding="utf-8", errors="ignore")
    markers = {
        "cor:ramanujan": "cor:ramanujan" in text,
        "photonic_predictions_remark": "Phase angles and the photonic predictions" in text,
        "theta_gauge_72.45": "72.45" in text,
        "theta_chiral_127.09": "127.09" in text,
        "closed_form_ihara_zeta": "Closed Form of the Ihara Zeta Function" in text,
        "ihara_ramanujan_circle": "Ihara--Ramanujan circle" in text,
    }
    # independent recomputation of the two angles
    ang = {}
    for lam in (2, -4):
        u = [r for r in ihara_roots(lam) if r.imag > 0][0]
        ang[str(lam)] = {"abs_u": abs(u),
                         "phase_deg": math.degrees(cmath.phase(u))}
    inv_sqrt11 = 1.0 / math.sqrt(11.0)
    on_circle = all(abs(v["abs_u"] - inv_sqrt11) < 1e-12 for v in ang.values())
    gauge_ok = abs(ang["2"]["phase_deg"] - 72.45) < 0.01
    chiral_ok = abs(ang["-4"]["phase_deg"] - 127.09) < 0.01
    checks["paper_already_has_all_markers"] = all(markers.values())
    checks["zeros_on_1_over_sqrt11_circle"] = on_circle
    checks["gauge_angle_72_45_reproduced"] = gauge_ok
    checks["chiral_angle_127_09_reproduced"] = chiral_ok
    return {"paper_markers": markers,
            "recomputed_angles": ang,
            "one_over_sqrt_11": inv_sqrt11,
            "verdict": "REDISCOVERY",
            "reading": (
                "Every element of Threads 2 and 4 -- the 1/sqrt(11) circle, both "
                "phase angles, and the photonic-measurement framing -- is already "
                "present in w33_paper.tex, in a corollary, a remark titled "
                "'Phase angles and the photonic predictions', and a closed-form "
                "zeta subsection.  The angles are recomputed here from the "
                "Ihara--Bass quadratic and agree.  The batch restates the "
                "paper's own result as an unstated secret.")}


def part_B_false_claims(checks):
    theta12_pdg = 13.04
    dcp_pdg = 68.5
    claimed_theta12 = 72.45 / 12.0          # their "phi_gauge/h x pi/pi"
    theta12_false = abs(claimed_theta12 - theta12_pdg) > 5.0
    dcp_gap = abs(72.45 - dcp_pdg)
    # Ramanujan saturation is impossible for integer spectra
    bound = 2 * math.sqrt(K_DEG - 1)
    max_nontrivial = max(abs(l) for l in EIGS if l != K_DEG)
    is_ramanujan = max_nontrivial <= bound
    saturates = abs(max_nontrivial - bound) < 1e-9
    checks["thread6_cabibbo_formula_is_false"] = theta12_false
    checks["is_ramanujan_true_but_not_saturated"] = (is_ramanujan and not saturates)
    return {"thread6_theta12": {"their_expression": "72.45/12 x (pi/pi)",
                                "evaluates_to_deg": claimed_theta12,
                                "pdg_deg": theta12_pdg,
                                "discrepancy_deg": abs(claimed_theta12 - theta12_pdg),
                                "verdict": "ARITHMETICALLY FALSE"},
            "thread6_delta_cp": {"claimed_deg": 72.45, "pdg_deg": dcp_pdg,
                                 "discrepancy_deg": dcp_gap,
                                 "verdict": "NOT a match within error"},
            "thread3_gap": {"ramanujan_bound": bound,
                            "max_nontrivial_eigenvalue": max_nontrivial,
                            "is_ramanujan": is_ramanujan,
                            "saturates_bound": saturates,
                            "verdict": ("'tightest possible' is impossible: "
                                        "saturation needs the irrational "
                                        "2 sqrt(11); SRG spectra are integral")},
            "thread7_deep_holes": {"claimed": 40,
                                   "classification": 23,
                                   "verdict": ("contradicts Conway-Parker-Sloane; "
                                               "23 deep-hole classes, one per "
                                               "Niemeier lattice")},
            "reading": (
                "The Cabibbo expression evaluates to 6.04 degrees against a "
                "measured 13.04, so it is false as written; the CP phase is about "
                "4 degrees off, not a match; Ramanujan saturation is impossible "
                "for an integral spectrum; and the deep-hole count contradicts "
                "the standard classification the batch itself invokes.")}


def part_C_true_but_empty(checks):
    ok1 = (240 * 819 == 196560)
    ok2 = (3 ** 3 - 4 == 23)
    ok3 = (240 + 36 == 276 and 2 ** 11 == 2048)
    checks["arithmetic_identities_check_out"] = (ok1 and ok2 and ok3)
    return {"196560_eq_240x819": ok1,
            "23_eq_27_minus_4": ok2,
            "mckay_thompson_2B_arithmetic": ok3,
            "verdict": "TRUE ARITHMETIC, NO W33 CONTENT",
            "reading": (
                "These identities hold but are divisions and small-integer "
                "coincidences.  With six free W(3,3) parameters an unconstrained "
                "search reaches most small integers, which is the numerology "
                "pattern this repository has retracted before.")}


def part_D_live_item(checks):
    # Phi_4(3) = 10 and Phi_6(3) = 7 from the Ihara-Bass discriminants
    q = K_DEG - 1
    phi_gauge = (4 * q - 2 ** 2) / 4.0     # lambda = 2
    phi_chiral = (4 * q - (-4) ** 2) / 4.0  # lambda = -4
    checks["phi4_is_10_and_phi6_is_7"] = (
        abs(phi_gauge - 10.0) < 1e-12 and abs(phi_chiral - 7.0) < 1e-12)
    return {"phi_gauge": phi_gauge, "phi_chiral": phi_chiral,
            "phi4_of_3": 3 ** 2 + 1, "phi6_of_3": 3 ** 2 - 3 + 1,
            "other_tens": ["w33_paper.tex L_2^#/L_2 three-primary rank",
                           "Pass 803 cut lattice (read there as Phi_4(3))",
                           "Pass 826 K four-branch gluing",
                           "Pass 827 adjacency three-branch gluing",
                           "Pass 828 coalescence rank of the class {2,-4} mod 3"],
            "status": "OPEN",
            "reading": (
                "The gauge angle is arctan sqrt(Phi_4(3)) with Phi_4(3) = 10 and "
                "the chiral angle uses Phi_6(3) = 7, both recovered here from the "
                "Ihara--Bass discriminants.  The integer 10 also occurs as a "
                "three-primary rank in four lattice computations, explained by "
                "Pass 828 as an F_3 collision rank.  Whether these are the same "
                "10 is open and is asserted neither way: one is a spectral "
                "discriminant, the other a mod-3 rank.")}


def main_payload():
    checks = {}
    A = part_A_rediscovery(checks)
    B = part_B_false_claims(checks)
    C = part_C_true_but_empty(checks)
    D = part_D_live_item(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass875.seven_thread_batch_intake_audit.v1",
        "status": status,
        "headline": (
            "INTAKE AUDIT OF THE SEVEN-THREAD BATCH: THE HEADLINE IS "
            "REDISCOVERY.  Threads 2 and 4 -- Ihara zeros on |u| = 1/sqrt(11), "
            "the phases 72.45 and 127.09 degrees, and their photonic "
            "measurability -- are already in w33_paper.tex as Corollary "
            "cor:ramanujan, a remark literally titled 'Phase angles and the "
            "photonic predictions', and a closed-form Ihara zeta subsection; both "
            "angles are recomputed from the Ihara--Bass quadratic here and agree. "
            " Thread 6's Cabibbo formula is arithmetically false (72.45/12 = 6.04 "
            "degrees against a measured 13.04) and its CP phase is about 4 "
            "degrees off, not a match.  Thread 3's 'tightest possible Ramanujan "
            "gap' is impossible for an integral SRG spectrum, though W(3,3) is "
            "Ramanujan.  Thread 7's '40 deep holes' contradicts the 23-class "
            "classification the batch itself cites.  Threads 1 and 5 reduce to "
            "true but contentless arithmetic.  The single live item is the "
            "recurrence of Phi_4(3) = 10, which is also the Pass 828 coalescence "
            "rank; whether they are the same 10 is left open."),
        "part_A_rediscovery": A,
        "part_B_false": B,
        "part_C_true_but_empty": C,
        "part_D_live_item": D,
        "checks": {k: bool(v) for k, v in checks.items()},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    pl = main_payload()
    text = json.dumps(pl, sort_keys=True, separators=(",", ":")) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text() != text:
            raise SystemExit("Pass 875 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
