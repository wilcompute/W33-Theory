#!/usr/bin/env python3
"""Pass 522: the blind-spot test fires again -- the sieve is NOT complete, and
the completeness claim was itself confirmed only on its own agreement locus.

Pass 521 named a failure mode: a fitted claim tested only where it cannot fail
receives no evidence.  It also named the obvious next target -- Pass 516/517's
completeness claim, whose cells were chosen for affordability, which correlates
with prime powers.  Running the test breaks the claim.

THE TEST.  The sieve predicts |T| independent linear relations among the tau(m)
cyclic classes, where T = { t | m : m/t odd, e | (m/t) }.  Choose cells with
|T| = 0, where it predicts NONE: a spurious relation has nowhere to hide.  In
all five such cells -- (3,2), (3,4), (3,10), (5,4), (5,6) -- the measured
nullity is 1, not 0.

THE MISSING RELATION, IDENTIFIED.  The period-one class consists of constant
m-tuples (v,...,v), and the zero-sum condition on them is m v = 0 with v != 0,
which is solvable exactly when p | m.  So when p does not divide m the class is
EMPTY and S_1 = 0 trivially -- a relation the sieve does not count, because the
sieve counts relations FORCED BY CANCELLATION, not classes that are vacuous.

THE CORRECTED LAW.

        nullity  =  |T|  +  [ p does not divide m ] ,

verified on eleven cells spanning both regimes: five with |T| = 0 and p not
dividing m, six with p | m where the correction term vanishes.

AND THE BLIND SPOT AGAIN.  Every cell Pass 516 and Pass 517 tested --
(3,3), (3,6), (3,9), (3,15), (3,27), (3,81), (5,5), (5,25), (7,7), (7,49) --
has p | m, so the correction term was 0 in every one of them.  The cells were
chosen because the Pass 514 shortcut needs e | (m/d), which is a condition on
p dividing m; affordability and the blind spot were the same constraint.  That
is the second time in three passes that a claim's test set was selected by
convenience into the locus where it cannot fail.

A SEPARATE, SMALLER RESULT.  The odd-m valuation at the q = 3 profile (4,8) is
also derivable.  There the eigenvalue valuations are {4,2,2} and e_1 = 0, so
mu_2 = -mu_1 + eps with v(eps) = 4; expanding mu_1^m + mu_2^m for odd m gives a
leading term m mu_1^{m-1} eps, whose valuation is v_lambda(m) + 2(m-1) + 4 =
v_lambda(m) + 2m + 2.  That reproduces the measured 10, 12, 16, 24 at
m = 3, 5, 7, 9 -- including the jumps at m = 3 and m = 9, which come from the
factor m and NOT from the spectrum.  Combined with Pass 521, the odd-m minimum
2(m+1) is attained by (4,8) exactly when p does not divide m, and by (6,6)
when it does; the (6,6) side remains open.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass522_completeness_corrected.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P515 = _load("p515", "w33_pass515_sieve_rank.py")
P517 = _load("p517", "w33_pass517_mobius_closed_form.py")
divisors, U_set = P515.divisors, P515.U_set


def vlam_int(n, p):
    v = 0
    while n and n % p == 0:
        n //= p
        v += 1
    return (p - 1) * v


def measure(p_, m, want):
    divs = divisors(m)
    mat, C = [], None
    for seed in range(9500, 9900):
        C, vec = P517.class_vector_fast(p_, m, seed)
        if any(any(x) for x in vec):
            mat.append(vec)
        if len(mat) >= want:
            break
    K = P517.Kfield(C)
    rk = P517.rank_over_K(K, mat)
    return len(divs), rk, len(mat)


def part_A_test_fires(checks):
    """Cells where the sieve predicts NO relations."""
    rows, fired = {}, 0
    for p_, m, ns in ((3, 2, 12), (3, 4, 14), (3, 10, 10), (5, 4, 10),
                      (5, 6, 10)):
        tau, rk, n = measure(p_, m, ns)
        T = len(U_set(m, p_))
        null = tau - rk
        if T == 0 and null > 0:
            fired += 1
        rows[f"p{p_}_m{m}"] = {"tau": tau, "informative_sections": n,
                               "nullity": null, "sieve_predicts": T,
                               "excess_relations": null - T}
    checks["all_five_zero_T_cells_have_an_unpredicted_relation"] = fired == 5
    checks["the_sieve_is_not_complete"] = fired > 0
    return {"rows": rows,
            "verdict": (
                "THE SIEVE IS NOT COMPLETE.  In every cell where it predicts "
                "no relations at all, one relation is present.  Pass 516 and "
                "Pass 517 reported nullity = |T| and called the sieve the "
                "whole relation space; that claim is now known to hold only "
                "where p divides m.")}


def part_B_corrected(checks):
    """nullity = |T| + [p does not divide m], both regimes."""
    rows, ok = {}, True
    plan = ((3, 2, 12), (3, 4, 14), (3, 10, 10), (5, 4, 10), (5, 6, 10),
            (3, 3, 12), (3, 6, 12), (3, 9, 12), (3, 15, 10), (5, 5, 10),
            (7, 7, 8))
    for p_, m, ns in plan:
        tau, rk, n = measure(p_, m, ns)
        T = len(U_set(m, p_))
        corr = 0 if m % p_ == 0 else 1
        null = tau - rk
        if null != T + corr:
            ok = False
        rows[f"p{p_}_m{m}"] = {"tau": tau, "nullity": null, "T": T,
                               "correction": corr, "predicted": T + corr,
                               "agrees": null == T + corr}
    checks["corrected_law_holds_on_every_cell"] = ok
    checks["corrected_law_covers_both_regimes"] = (
        any(r["correction"] == 1 for r in rows.values())
        and any(r["correction"] == 0 for r in rows.values()))
    return {"rows": rows,
            "law": "nullity = |T| + [p does not divide m]",
            "why": (
                "The period-one class consists of the constant m-tuples "
                "(v,...,v), whose zero-sum condition is m v = 0 with v != 0.  "
                "That is solvable exactly when p | m; otherwise the class is "
                "EMPTY and S_1 = 0 holds vacuously.  The sieve counts "
                "relations forced by cancellation and does not count vacuous "
                "classes, so it undercounts by exactly one whenever p does not "
                "divide m.")}


def part_C_blind_spot(checks):
    """Every cell the completeness claim was tested on had p | m."""
    old = [(3, 3), (3, 6), (3, 9), (3, 15), (3, 27), (3, 81), (5, 5),
           (5, 25), (7, 7), (7, 49)]
    rows = {f"p{p}_m{m}": {"p_divides_m": m % p == 0,
                           "correction_term": 0 if m % p == 0 else 1}
            for p, m in old}
    allsame = all(r["correction_term"] == 0 for r in rows.values())
    checks["every_previously_tested_cell_had_p_dividing_m"] = allsame
    return {"previously_tested": rows,
            "diagnosis": (
                "All ten cells used by Passes 516 and 517 satisfy p | m, so "
                "the correction term was zero in every one and the missing "
                "relation could not appear.  The cells were not chosen "
                "adversarially: the Pass 514 shortcut requires e | (m/d), "
                "which is a condition on p dividing m, so the cells that were "
                "AFFORDABLE were exactly the cells where the claim cannot "
                "fail.  Convenience and the blind spot were the same "
                "constraint -- the second instance in three passes, after the "
                "factorial law's prime-power tower."),
            "rule": (
                "When a claim is tested only on cells selected by a "
                "computational convenience, check whether that convenience is "
                "logically related to the claim.  Here it was, twice.")}


def part_D_odd_m(checks):
    """The odd-m valuation at profile (4,8), derived."""
    measured = {3: 10, 5: 12, 7: 16, 9: 24}
    rows, ok = {}, True
    for m, got in measured.items():
        pred = vlam_int(m, 3) + 2 * m + 2
        if pred != got:
            ok = False
        rows[str(m)] = {"measured": got, "derived": pred,
                        "v_lambda_m": vlam_int(m, 3)}
    checks["odd_m_formula_at_profile_4_8"] = ok
    return {"rows": rows,
            "derivation": (
                "At the q = 3 profile (v(e_2), v(e_3)) = (4, 8) the eigenvalue "
                "valuations are {4, 2, 2}.  Since e_1 = tr D = 0 and the third "
                "eigenvalue has valuation 4 > 2, mu_1 + mu_2 = -mu_3 has "
                "valuation 4, so mu_2 = -mu_1 + eps with v(eps) = 4.  For odd "
                "m, mu_1^m + mu_2^m = mu_1^m - (mu_1 - eps)^m has leading term "
                "m mu_1^{m-1} eps, of valuation v_lambda(m) + 2(m-1) + 4 = "
                "v_lambda(m) + 2m + 2.  That reproduces 10, 12, 16, 24 at "
                "m = 3, 5, 7, 9 -- the jumps at m = 3 and 9 coming from the "
                "binomial factor m, NOT from the spectrum."),
            "combined": (
                "With Pass 521: the odd-m minimum 2(m+1) is attained by (4,8) "
                "exactly when p does not divide m, since then v_lambda(m) = 0, "
                "and by (6,6) when p | m.  Why (6,6) supplies 2(m+1) is still "
                "open.")}


def main_payload():
    checks = {}
    A = part_A_test_fires(checks)
    B = part_B_corrected(checks)
    Cc = part_C_blind_spot(checks)
    Dd = part_D_odd_m(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass522.completeness_corrected.v1",
        "status": status,
        "headline": (
            "WE RETRACT THE COMPLETENESS CLAIM OF PASSES 516-517.  The sieve is "
            "not complete, and that claim was itself "
            "TESTED ONLY WHERE IT CANNOT FAIL.  Pass 521 named the "
            "agreement-locus failure mode and pointed at Pass 516/517's "
            "completeness claim as the next target; running the test breaks "
            "it.  In all five cells where the sieve predicts NO relations -- "
            "(3,2), (3,4), (3,10), (5,4), (5,6) -- the measured nullity is 1.  "
            "The missing relation is identified: the period-one class is the "
            "constant m-tuples, whose zero-sum condition m v = 0 with v != 0 "
            "is solvable only when p | m, so for p not dividing m the class is "
            "EMPTY and S_1 = 0 vacuously.  The corrected law is "
            "nullity = |T| + [p does not divide m], verified on eleven cells "
            "across both regimes.  Every cell Passes 516 and 517 used has "
            "p | m -- because the Pass 514 shortcut needs e | (m/d), so the "
            "affordable cells were exactly the cells where the claim cannot "
            "fail.  Convenience and the blind spot were the same constraint, "
            "for the second time in three passes."),
        "part_A_the_test_fires": A,
        "part_B_corrected_law": B,
        "part_C_the_blind_spot_again": Cc,
        "part_D_odd_m_at_profile_4_8": Dd,
        "boundary": (
            "Parts A and B are rank measurements over 8 to 14 informative "
            "sampled sections per cell, in Q(zeta_p), and test only linear "
            "relations with constant field coefficients -- the same scope as "
            "the claim they correct.  A larger sample can only LOWER a "
            "measured rank, hence RAISE the nullity, so the excess relation "
            "found here cannot be a sampling artefact in the direction that "
            "matters; but the corrected law itself is measured on eleven cells "
            "and not proved.  Part C is arithmetic on the previously used "
            "cells.  Part D derives one profile's odd-m valuation and checks "
            "it against four measured points; the (6,6) profile is untouched."),
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
            raise SystemExit("Pass 522 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
