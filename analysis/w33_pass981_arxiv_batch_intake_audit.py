#!/usr/bin/env python3
"""Pass 981: intake audit of Passes 881-888, the arXiv-bound batch.

Passes 881-888 (BREAKTHROUGH_PASS88x_*.md on master) propose three arXiv
submissions with dates: a PRL photonic paper in August 2026, an IEEE Trans.
Inform. Theory paper in September, and a Journal of Number Theory paper in
October.  CLAUDE.md requires batched claims to be audited AT INTAKE.  Several of
these claims are refuted by elementary arithmetic, and one of them is refuted by
its own source file.

1.  THE CKM MATRIX (Pass 882) IS EXCLUDED BY EXPERIMENT.

The summary presents four "parameter-free" CKM predictions with agreements
quoted as percentages -- 10%, 11%, 34%, "order-correct".  Percentages are the
wrong unit: the CKM angles are measured to a few parts in 10^4, so the correct
measure is the discrepancy in experimental standard deviations.  In those units
(PDG central values and errors):

        theta_12   14.48 vs 13.04 +- 0.05     ->  28.8 sigma
        theta_23    3.18 vs  2.38 +- 0.06     ->  13.3 sigma
        theta_13   0.893 vs 0.201 +- 0.011    ->  62.9 sigma
        lambda_W   0.250 vs 0.2250 +- 0.0007  ->  35.7 sigma
        Jarlskog  2.06e-5 vs 3.18e-5 +- 0.15e-5 -> 7.5 sigma
        delta_CP   72.45 vs 65.5 +- 3.3       ->   2.1 sigma

Five of the six are excluded outright; only the CP phase, whose experimental
error is large, is even marginal.  A prediction 29 standard deviations from a
measured value is refuted, not in "11% agreement".  Submitting this to PRL as a
successful parameter-free derivation would not survive referee arithmetic.

2.  THE SAME FILE REFUTES ITS OWN "ZERO FITTING" CLAIM.

BREAKTHROUGH_PASS882_CKM_FULL_MATRIX.md derives theta_12 FOUR times, in order:

        arctan(sin phi/(2 sqrt 11 - 1))            = 9.61  degrees
        the same times sqrt(4/3) "colour correction" = 11.10 degrees
        sin^2 theta = g^2/(g^2+k)                   = 60    degrees ("Too large")
        sin theta   = mu/(k+mu) = 1/4               = 14.48 degrees ("Closest yet")

and reports the last.  Selecting among candidate formulas by proximity to the
measured value IS fitting; the summary's "derived ... with zero fitting" and
"parameter-free" are contradicted by the file's own text.  The same file computes
theta_13 = 2.88 degrees and writes "This formula needs revision", while the
summary table reports theta_13 = 0.893 degrees -- a fifth formula, and an
internal inconsistency between the document and its own summary.

3.  THE E8 INDEX IS WRONG BY A FACTOR OF 28 (Pass 881).

The claim is [W(E8) : Sp(4,3)] = 480 = 2 x 240.  But |W(E8)| = 696729600 and
|Sp(4,3)| = 51840, so the index is 13440; with PSp(4,3) of order 25920 it is
26880.  Neither is 480.  (The genuine classical coincidence in this area is
|W(E6)| = 51840 = |Sp(4,3)|, which concerns E6, not E8.)  The accompanying
"bonus theorem" dim(e8) = 248 = 240 + 8 is the standard decomposition of a
semisimple Lie algebra into root spaces plus Cartan subalgebra, true for every
simple Lie algebra and not a W(3,3) result.

4.  THE LEECH EMBEDDING IS DIMENSIONALLY IMPOSSIBLE (Pass 883).

The claim identifies the 40 vertices with coset representatives of "the 5
orthogonal E8 sublattices in the Leech lattice's 5-frame decomposition,
40 = 5 x 8".  Five pairwise orthogonal rank-8 sublattices span rank 40, but the
Leech lattice has rank 24.  No such configuration exists.  The standard fact is
that Leech contains E8^3 (rank 3 x 8 = 24), which is where the "orthogonal E8
sublattice" language comes from.

5.  PASS 885 RESTATES A TEXTBOOK EQUIVALENCE.

"Theorem 885-2: a k-regular graph is Ramanujan if and only if its Ihara zeta
satisfies the graph-theoretic Riemann hypothesis at radius 1/sqrt(k-1)" is the
standard definition-plus-equivalence found in the graph-zeta literature (Terras,
Zeta Functions of Graphs); it is how the graph RH is normally stated.  It is not
new, and it does not require Deligne.  The eigenvalues of a polar-space
collinearity graph are known in closed form, so the Ramanujan property of W(3,3)
follows from those explicit eigenvalues, not from the Weil conjectures.

6.  PASSES 884 AND 887 ARE ARITHMETIC IDENTITIES.

3g - 3 + n = 27 at (g,n) = (6,12) and 27 = 3^3; 196883 = 196560 + 323 with
323 = 17 x 19; 744 = 3 x 240 + 24.  All check out as arithmetic (verified here)
and none carries structural content: with a handful of free small integers these
targets are reachable many ways.  The inference in Pass 884 that this "resolves
the vacuum selection problem of string theory" does not follow from a dimension
count.

7.  NUMBERING.  Master now carries 881 and 882 twice: analysis/w33_pass881_* and
w33_pass882_* (intake audit and spectral-surgery rigidity, committed 20:15) and
BREAKTHROUGH_PASS881_*.md / PASS882_*.md (committed 20:27).  The earlier commit
owns the number under the repository's ownership rule, so the .md pair needs
renumbering, or the pair must be distinguished explicitly.

WHAT SURVIVES.  The Ihara zero phases themselves are correct -- phi = arccos(lam
/ (2 sqrt(k-1))) gives 72.45 and 127.09 degrees, recomputed here -- but they were
already in w33_paper.tex before this batch (Pass 881, this track).  The A5 orbit
count 240 = 4 x 60 in Pass 886 is arithmetically consistent and is the one item
worth pursuing on its own terms.

BOUNDARY.  This audits checkable claims.  It does not evaluate the photonic
device proposal of Pass 888's Paper 1 beyond noting that its physics content is
the already-published zero phases; whether a chip measurement is worth doing is a
separate question from whether the prediction is novel.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass981_arxiv_batch_intake_audit.json"

W_E8 = 696729600
SP43 = 51840
PSP43 = 25920

# (name, predicted, pdg_central, pdg_error)
CKM = [("theta_12", 14.48, 13.04, 0.05),
       ("theta_23", 3.18, 2.38, 0.06),
       ("theta_13", 0.893, 0.201, 0.011),
       ("delta_CP", 72.45, 65.5, 3.3),
       ("lambda_W", 0.250, 0.2250, 0.0007),
       ("jarlskog_e5", 2.06, 3.18, 0.15)]


def part_A_ckm(checks):
    rows = {}
    excluded = 0
    for nm, pred, pdg, err in CKM:
        sig = abs(pred - pdg) / err
        if sig > 5:
            excluded += 1
        rows[nm] = {"predicted": pred, "pdg": pdg, "pdg_error": err,
                    "sigma": round(sig, 2),
                    "percent": round(100 * abs(pred - pdg) / abs(pdg), 1),
                    "verdict": "EXCLUDED" if sig > 5 else "marginal"}
    checks["five_of_six_ckm_excluded_beyond_5sigma"] = (excluded == 5)
    checks["theta12_excluded_beyond_20sigma"] = (rows["theta_12"]["sigma"] > 20)
    return {"rows": rows, "excluded_count": excluded, "total": len(CKM),
            "reading": (
                "Quoted as percentages the CKM predictions look like 10-34% "
                "agreement; in experimental standard deviations, which is the "
                "unit that matters when angles are measured to parts in 10^4, "
                "five of six are excluded -- theta_12 by 28.8 sigma and "
                "theta_13 by 62.9.  Only delta_CP, with a 3.3 degree error bar, "
                "is marginal at 2.1 sigma.")}


def part_B_self_refutation(checks):
    variants = {"arctan(sin phi/(2 sqrt11 - 1))": 9.61,
                "times sqrt(4/3) colour correction": 11.10,
                "sin^2 = g^2/(g^2+k)": 60.0,
                "sin = mu/(k+mu) = 1/4": 14.48}
    reported = 14.48
    pdg = 13.04
    closest = min(variants.items(), key=lambda kv: abs(kv[1] - pdg))
    checks["reported_theta12_is_the_best_fitting_variant"] = (
        abs(closest[1] - reported) < 1e-9)
    checks["multiple_competing_formulas_present"] = (len(variants) >= 4)
    # theta_13 internal inconsistency: body 2.88, summary 0.893
    checks["theta13_body_and_summary_disagree"] = (abs(2.88 - 0.893) > 1.0)
    return {"theta12_variants_in_the_file": variants,
            "reported": reported,
            "closest_to_pdg": {"formula": closest[0], "value": closest[1]},
            "theta13_in_body": 2.88,
            "theta13_body_comment": "This formula needs revision",
            "theta13_in_summary_table": 0.893,
            "reading": (
                "The source file derives theta_12 four times and reports the "
                "variant closest to the measured value, which is selection by "
                "fit; the summary nonetheless calls the result parameter-free "
                "with zero fitting.  theta_13 is 2.88 degrees in the body, "
                "flagged there as needing revision, but 0.893 degrees in the "
                "summary table -- the document and its own summary disagree.")}


def part_C_group_and_lattice(checks):
    idx_sp = W_E8 // SP43
    idx_psp = W_E8 // PSP43
    checks["e8_index_is_not_480"] = (idx_sp != 480 and idx_psp != 480)
    checks["we6_order_equals_sp43"] = (SP43 == 51840)
    checks["five_e8_exceeds_leech_rank"] = (5 * 8 > 24)
    return {"W_E8_order": W_E8, "Sp43_order": SP43, "PSp43_order": PSP43,
            "index_Sp43": idx_sp, "index_PSp43": idx_psp, "claimed_index": 480,
            "real_coincidence": "|W(E6)| = 51840 = |Sp(4,3)| (E6, not E8)",
            "dim_e8_248": "248 = 240 + 8 = roots + rank: standard for any simple Lie algebra",
            "leech_rank": 24, "claimed_orthogonal_E8_count": 5,
            "rank_needed": 5 * 8,
            "standard_fact": "Leech contains E8^3, rank 3 x 8 = 24",
            "reading": (
                "The claimed index 480 is wrong: the true indices are 13440 and "
                "26880.  And five pairwise orthogonal rank-8 sublattices need "
                "rank 40, which does not fit in the rank-24 Leech lattice, so "
                "the '5-frame, 40 = 5 x 8' embedding does not exist.")}


def part_D_arithmetic_and_zeros(checks):
    ident = {"3g-3+n at (6,12) = 27": 3 * 6 - 3 + 12 == 27,
             "27 = 3^3": 3 ** 3 == 27,
             "196883 = 196560 + 323": 196560 + 323 == 196883,
             "323 = 17 x 19": 17 * 19 == 323,
             "744 = 3*240 + 24": 3 * 240 + 24 == 744,
             "240 = 4 x 60 (A5 orbits)": 4 * 60 == 240}
    # Ihara phases: phi = arccos(lam / (2 sqrt(k-1)))
    k = 12
    phases = {str(lam): math.degrees(math.acos(lam / (2 * math.sqrt(k - 1))))
              for lam in (2, -4)}
    checks["arithmetic_identities_true"] = all(ident.values())
    checks["ihara_phases_reproduced"] = (
        abs(phases["2"] - 72.45) < 0.01 and abs(phases["-4"] - 127.09) < 0.01)
    return {"identities": ident, "ihara_phases_deg": phases,
            "zeros_already_in_paper": (
                "w33_paper.tex cor:ramanujan and the remark 'Phase angles and "
                "the photonic predictions' predate this batch (see Pass 881)"),
            "textbook_items": [
                "248 = 240 + 8 (roots + rank)",
                "Ramanujan iff graph RH at 1/sqrt(k-1) (standard, Terras)"],
            "reading": (
                "The arithmetic identities all hold and none carries structural "
                "content.  The Ihara phases are correct and are recomputed here, "
                "but they were already in the main paper before this batch.  The "
                "A5 orbit split 240 = 4 x 60 is the one arithmetically clean new "
                "item.")}


def part_E_numbering(checks):
    checks["numbering_collision_recorded"] = True
    return {"duplicated": [881, 882],
            "mine": ["analysis/w33_pass881_seven_thread_batch_intake_audit.py",
                     "analysis/w33_pass882_spectral_surgery_rigidity.py"],
            "theirs": ["BREAKTHROUGH_PASS881_E8_BIJECTION_EXPLICIT.md",
                       "BREAKTHROUGH_PASS882_CKM_FULL_MATRIX.md"],
            "rule": "the earlier commit owns the number",
            "resolution_needed": (
                "the .md pair was committed later and should be renumbered, or "
                "the two families distinguished explicitly")}


def main_payload():
    checks = {}
    A = part_A_ckm(checks)
    B = part_B_self_refutation(checks)
    C = part_C_group_and_lattice(checks)
    D = part_D_arithmetic_and_zeros(checks)
    E = part_E_numbering(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass981.arxiv_batch_intake_audit.v1",
        "status": status,
        "headline": (
            "INTAKE AUDIT OF PASSES 881-888, THE arXiv-BOUND BATCH: THE CKM "
            "PAPER IS EXCLUDED BY EXPERIMENT AND THE E8 AND LEECH CLAIMS ARE "
            "ARITHMETICALLY FALSE.  Expressed in experimental sigma rather than "
            "percent, five of six CKM quantities are excluded -- theta_12 by "
            "28.8, theta_13 by 62.9, lambda_W by 35.7, theta_23 by 13.3, the "
            "Jarlskog invariant by 7.5 -- and only delta_CP is marginal at 2.1.  "
            "The source file itself derives theta_12 four times (9.61, 11.10, "
            "60, 14.48 degrees) and reports the closest to the measured value "
            "while the summary claims zero fitting, and it gives theta_13 as "
            "2.88 in the body, flagged as needing revision, against 0.893 in the "
            "summary table.  [W(E8):Sp(4,3)] is 13440, not the claimed 480 (the "
            "real coincidence is |W(E6)| = 51840 = |Sp(4,3)|), and dim(e8) = 240 "
            "+ 8 is textbook.  Five orthogonal E8 sublattices cannot embed in "
            "the rank-24 Leech lattice since they span rank 40.  Pass 885's "
            "'theorem' is the standard graph-RH equivalence.  The Ihara phases "
            "are correct but predate the batch in w33_paper.tex.  Master also "
            "carries 881 and 882 twice."),
        "part_A_ckm_excluded": A,
        "part_B_self_refutation": B,
        "part_C_group_and_lattice": C,
        "part_D_arithmetic_and_zeros": D,
        "part_E_numbering": E,
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
            raise SystemExit("Pass 981 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
