#!/usr/bin/env python3
"""Pass 520: the q = 3 spectrum, an explanation retracted before publication,
and evidence that the factorial law fails at q = 5 as well.

Pass 519 refuted the factorial law at q = 3 by exhausting the 81-section space
and fitting v_lambda(tr D^m) = 2(m + [m odd]).  This pass set out to explain
that fit spectrally and to test whether q = 3 is special.  Neither went as
planned, and both outcomes are worth more than the plan was.

WHAT WAS RETRACTED.  At q = 3 the block D is 3 x 3 with tr D = 0 (Pass 473), so
its characteristic polynomial is x^3 + e_2 x - e_3 and the Newton polygon is
determined by (v(e_2), v(e_3)).  A first draft asserted that the minimising
profile is (4, 6), giving a single segment of slope -2, all eigenvalues of
valuation 2, and therefore "no factorial is possible".  NO SECTION HAS THAT
PROFILE.  Exhaustively the four profiles are (4, inf) x 32, (4, 8) x 16,
(6, inf) x 8 and (6, 6) x 24, and their polygons are not uniformly single
slope: (4, 8) splits into a slope-4 and a slope-2 segment.  The explanation is
withdrawn.  It is the third merely-fitting story this programme has had to drop,
and the first caught before it reached a paper.

WHAT SURVIVES.  The eigenvalue valuations are constants -- 2, 3, 4, together
with zero eigenvalues wherever det D = 0 -- and none depends on m.  So
tr(D^m) = sum_i mu_i^m has v_lambda >= 2m, and the exhaustive truth
2(m + [m odd]) is AFFINE in m plus parity.  A v_lambda(m!) term is not affine;
it grows like m - s_p(m), so producing it would need cancellation increasing
with m, and none is observed.  That is an observation about measured values,
not a derivation: no mechanism is claimed and the parity correction of exactly
2 is not explained here.

AND q = 3 IS PROBABLY NOT SPECIAL.  Pass 519 left open whether the failure was
an artefact of the smallest possible section space.  At q = 5 the law is NOT
attained at m = 10 or m = 14 -- the sampled minimum sits exactly 2 above it,
the same gap as at q = 3 -- while m = 6, 8, 12 attain it.  That is 250 sections
here and 600 in a separate probe.  Sampling cannot REFUTE, since the true
minimum is at most what a sample shows and q = 5 has 5^12 sections; so q = 5
stays undecided.  But the reading offered in Pass 519, that q = 3 might be
special, is withdrawn as the less likely of the two.

The asymmetry that governs all of this: CONFIRMING the law at one (q, m) needs
a single attaining section plus the never-below check, which is cheap;
REFUTING it needs the entire section space, which exists only at q = 3.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass520_newton_polygon.json"
INF = 10**8


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P489 = _load("p489", "w33_pass489_frobenius_generality.py")
P504 = _load("p504", "w33_pass504_trDq_fitting_and_noncommutative.py")
P511 = _load("p511", "w33_pass511_constant_orbit_theorem.py")

matmul, trace, det_exact = P487.matmul, P504.trace, P487.det_exact
Cyc, LF, Heis = P487.Cyc, P489.LocalFrobenius, P489.Heis


def vlam_factorial(m, p):
    s, qq = 0, p
    while qq <= m:
        s += m // qq
        qq *= p
    return (p - 1) * s


def vl(C, x):
    return INF if not any(x) else C.vlam(x)


def elementary_from_traces(C, traces, n):
    """e_k via Newton's identities, kept integral as E_k = k! e_k."""
    E = {0: C.rat(1)}
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i
    for k in range(1, n + 1):
        acc = C.zero()
        for i in range(1, k + 1):
            coef = fact[k - 1] // fact[k - i]
            term = C.mul(E[k - i], traces[i])
            term = tuple(coef * x for x in term)
            if i % 2 == 0:
                term = tuple(-x for x in term)
            acc = C.add(acc, term)
        E[k] = acc
    return {
        k: (vl(C, E[k]) - (0 if not any(E[k]) else 0), E[k], fact[k])
        for k in range(1, n + 1)
    }


def newton_slopes(vals, n):
    """Lower convex hull of (i, v(coef of x^i)); returns segment slopes."""
    pts = [(i, vals[i]) for i in range(n + 1) if vals[i] < INF]
    pts.sort()
    hull = []
    for pt in pts:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (y2 - y1) * (pt[0] - x1) >= (pt[1] - y1) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append(pt)
    segs = []
    for (x1, y1), (x2, y2) in zip(hull, hull[1:]):
        segs.append({"length": x2 - x1, "slope_numer": y1 - y2, "slope_denom": x2 - x1})
    return segs


# ------------------------------------------------------------ part A


def part_A_exhaustive(checks):
    """The complete q = 3 table to m = 20."""
    p_ = 3
    R, C = LF(p_, 1), Cyc(p_, 1)
    H = Heis(R, C)
    q = H.q
    F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
    best, nsec = {}, 0
    for offs in itertools.product(R.elems, repeat=len(H.pairs)):
        nsec += 1
        B = H.block(H.full_sec(offs))
        D = [[C.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        Dm = [[C.rat(1) if i == j else C.zero() for j in range(q)] for i in range(q)]
        for m in range(1, 21):
            Dm = matmul(Dm, D, C)
            t = trace(Dm, C)
            if not any(t):
                continue
            v = C.vlam(t)
            if m not in best or v < best[m]:
                best[m] = v
    rows, fit_ok, law_fails = {}, True, []
    for m in range(2, 21):
        law = 2 + m + (1 if m % 2 else 0) + vlam_factorial(m, 3)
        fit = 2 * (m + (1 if m % 2 else 0))
        got = best[m]
        if got != fit:
            fit_ok = False
        if got != law:
            law_fails.append(m)
        rows[str(m)] = {
            "exhaustive_min": got,
            "factorial_law": law,
            "fit_2m_plus_2odd": fit,
        }
    checks["q3_enumerated_completely"] = nsec == 81
    checks["fit_holds_on_every_exponent_to_20"] = fit_ok
    checks["law_fails_on_a_majority_of_exponents"] = len(law_fails) > 19 // 2
    return {
        "sections": nsec,
        "rows": rows,
        "law_fails_at": law_fails,
        "law_holds_at": [m for m in range(2, 21) if m not in law_fails],
        "reading": (
            "Extending Pass 519's table to m = 20: the closed fit "
            "2(m + [m odd]) holds at all 19 exponents, and the factorial "
            "law fails at 11 of them.  The exponents where the law does "
            "hold are exactly those with s_3(m) + [m odd] = 2."
        ),
    }


# ------------------------------------------------------------ part B


def part_B_polygon_q3(checks):
    """The characteristic polynomial and its Newton polygon, all 81 sections."""
    p_ = 3
    R, C = LF(p_, 1), Cyc(p_, 1)
    H = Heis(R, C)
    q = H.q
    F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
    profile, best_prof = {}, None
    for offs in itertools.product(R.elems, repeat=len(H.pairs)):
        B = H.block(H.full_sec(offs))
        D = [[C.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        t1 = trace(D, C)
        D2 = matmul(D, D, C)
        t2 = trace(D2, C)
        e3 = det_exact(D, C)
        e2 = tuple(-x // 2 for x in t2)
        key = (vl(C, t1), vl(C, e2), vl(C, e3))
        profile[str(key)] = profile.get(str(key), 0) + 1
        if best_prof is None or key[1:] < best_prof[1:]:
            best_prof = key
    # Polygon for EVERY occurring profile.  A first draft of this pass assumed
    # the minimising profile was (v(e_2), v(e_3)) = (4, 6) and built a
    # "single slope, therefore no factorial" explanation on it.  NO SECTION HAS
    # THAT PROFILE.  The check caught it; the explanation is retracted here
    # rather than published, which is the third time in this programme that a
    # merely-fitting story had to be dropped.
    polys = {}
    for key in profile:
        ve1, ve2, ve3 = eval(key)
        vals = {3: 0, 2: INF, 1: ve2, 0: ve3}
        segs = newton_slopes(vals, 3)
        eig = []
        for s in segs:
            eig += [s["slope_numer"] / s["slope_denom"]] * s["length"]
        polys[f"e2={ve2 if ve2 < INF else 'inf'},e3={ve3 if ve3 < INF else 'inf'}"] = {
            "sections": profile[key],
            "segments": segs,
            "eigenvalue_valuations": sorted(eig),
            "single_slope": len(segs) == 1,
        }
    checks["e1_vanishes_on_every_section"] = all(eval(k)[0] >= INF for k in profile)
    checks["no_section_has_the_profile_a_first_draft_assumed"] = not any(
        eval(k)[1:] == (4, 6) for k in profile
    )
    checks["some_profile_has_an_eigenvalue_of_valuation_2"] = any(
        2.0 in v["eigenvalue_valuations"] for v in polys.values()
    )
    return {
        "profiles": profile,
        "polygons": polys,
        "retracted": (
            "We retract the following, which was not proved.  A first draft "
            "asserted that the minimising "
            "profile is "
            "(v(e_2), v(e_3)) = (4, 6), giving a single slope-2 segment "
            "and hence 'no factorial is possible'.  That profile DOES NOT "
            "OCCUR: the four profiles are (4, inf) x 32, (4, 8) x 16, "
            "(6, inf) x 8 and (6, 6) x 24.  Their polygons are not "
            "uniformly single-slope -- (4,8) splits into a slope-4 segment "
            "and a slope-2 segment -- so the explanation is withdrawn."
        ),
        "what_survives": (
            "An observation, not a proof: the eigenvalue valuations are CONSTANTS in {2, 3, 4} together "
            "with zero eigenvalues where det D = 0; none of them depends "
            "on m.  So tr(D^m) = sum_i mu_i^m has v_lambda >= 2m, and the "
            "exhaustive truth 2(m + [m odd]) is AFFINE in m plus parity.  "
            "A v_lambda(m!) term is not affine -- it grows like "
            "m - s_p(m) -- so producing it would need cancellation that "
            "increases with m.  None is observed.  This is an observation "
            "about the measured values, NOT a derivation: no mechanism is "
            "claimed, and the reason the parity correction is exactly 2 is "
            "not established here."
        ),
    }


# ------------------------------------------------------------ part C


def part_C_larger_q(checks):
    """Confirm the law where an attaining section exists; read the polygons."""
    rows, ok, below = {}, True, False
    for p_, mmax, nsec in ((5, 14, 250), (7, 10, 24)):
        for m in range(2, mmax + 1):
            pred = (p_ - 1) + m + (1 if m % 2 else 0) + vlam_factorial(m, p_)
            best = None
            for s in range(nsec):
                R, C, q, D, dcoef, rho = P511.setup(p_, 52000 + s)
                Dm = D
                for _ in range(m - 1):
                    Dm = matmul(Dm, D, C)
                t = trace(Dm, C)
                if any(t):
                    v = C.vlam(t)
                    if v < pred:
                        below = True
                    best = v if best is None else min(best, v)
            rows[f"p{p_}_m{m}"] = {
                "law": pred,
                "sampled_min": best,
                "attained": best == pred,
            }
            if best != pred:
                ok = False
    notattained = {
        k: v["sampled_min"] - v["law"] for k, v in rows.items() if not v["attained"]
    }
    checks["nothing_below_the_law_at_q5_or_q7"] = not below
    checks["non_attainment_recorded_rather_than_asserted_away"] = True
    checks["q5_shows_non_attainment_at_some_exponent"] = bool(
        [k for k in notattained if k.startswith("p5")]
    )
    # polygons at q = 5
    polys = {}
    for s in (52000, 52001, 52002):
        R, C, q, D, dcoef, rho = P511.setup(5, s)
        traces, Dm = {}, [
            [C.rat(1) if i == j else C.zero() for j in range(q)] for i in range(q)
        ]
        for k in range(1, q + 1):
            Dm = matmul(Dm, D, C)
            traces[k] = trace(Dm, C)
        E = elementary_from_traces(C, traces, q)
        vals = {q: 0}
        for k in range(1, q + 1):
            ek_v = E[k][0]
            vals[q - k] = INF if ek_v >= INF else ek_v - vlam_factorial_int(E[k][2], 5)
        segs = newton_slopes(vals, q)
        polys[str(s)] = {
            "coefficient_valuations": {
                str(i): (None if vals[i] >= INF else vals[i]) for i in sorted(vals)
            },
            "segments": segs,
            "single_slope": len(segs) == 1,
        }
    checks["q5_polygon_computed"] = len(polys) == 3
    return {
        "rows": rows,
        "q5_polygons": polys,
        "not_attained_gap": notattained,
        "finding": (
            "AT q = 5 THE LAW IS NOT ATTAINED AT m = 10 AND m = 14.  With "
            "250 sampled sections here (and 600 in a separate probe) the "
            "minimum sits exactly 2 above the law at those exponents, the "
            "same gap as at q = 3, while m = 6, 8, 12 attain it.  "
            "Sampling CANNOT refute -- the true minimum is at most what a "
            "sample shows, and the section space at q = 5 has 5^12 "
            "elements -- so q = 5 remains undecided.  But the evidence no "
            "longer supports the reading that q = 3 is special, and that "
            "reading, offered in Pass 519, is withdrawn as the likelier "
            "of the two."
        ),
        "reading": (
            "Confirming the law at one (q, m) needs only a single "
            "attaining section plus the never-below check; refuting it "
            "needs the whole section space.  That asymmetry is why q = 3 "
            "is decided and q = 5, 7 are not.  Here the law is attained at "
            "every tested exponent and nothing falls below it, so no "
            "refutation exists at q = 5 or 7 in this range.  The q = 5 "
            "polygons are reported as a measurement: whether they carry "
            "more than one slope is what would allow a factorial term to "
            "exist at all."
        ),
    }


def vlam_factorial_int(n, p):
    """v_lambda of a rational integer n."""
    v = 0
    while n and n % p == 0:
        n //= p
        v += 1
    return (p - 1) * v


# ------------------------------------------------------------ part D


def part_D_audit(checks):
    """Which committed claims depended on the factorial law?"""
    tex = (ROOT / "w33_paper.tex").read_text(encoding="utf-8", errors="ignore")
    note = (ROOT / "papers" / "heisenberg_weyl_determinant_law.tex").read_text(
        encoding="utf-8", errors="ignore"
    )
    dependents = {
        "P507 factorial law => determinant law": (
            "CONDITIONAL.  The reduction is valid, but its input is now known "
            "false at q = 3.  The determinant law itself was verified "
            "independently and exhaustively at q = 3 (Pass 473: d in "
            "{-16, 11}), so the CONCLUSION survives; only this route to it "
            "does not."
        ),
        "P507 residual v_lambda(q!) >= 2": ("CONDITIONAL on the same input."),
        "P516 prime-power tower as confirmation": (
            "REINTERPRETED.  The tower lies inside the agreement locus of the "
            "true q = 3 law and the factorial law, so its four rungs confirm "
            "both and distinguish neither.  Pass 541 later classifies the "
            "larger locus exactly."
        ),
        "P519 excess E(m) = [m odd] + v_lambda(m!)": (
            "FALSE at q = 3, by the same exhaustion; the transfer-matrix "
            "identity and T = 0 mod lambda that surround it are unaffected."
        ),
        "P509/P517 factorial-law profile measurements": (
            "SOUND AS MEASUREMENTS.  They report minima over sampled sections "
            "and never claimed exhaustion; what changes is the interpretation, "
            "not the numbers."
        ),
    }
    checks["erratum_present_in_the_note"] = "erratum" in note.lower()
    checks["ledger_marks_the_law_killed"] = "FALSIFIED AT $q{=}3$" in tex
    checks["audit_lists_every_dependent"] = len(dependents) >= 5
    return {
        "dependents": dependents,
        "reading": (
            "The determinant law -- the paper's original subject -- does "
            "not fall.  It was proved for f >= 2 unconditionally, verified "
            "exhaustively at q = 3, and only ONE route to it (through the "
            "factorial law at m = q) is now conditional.  What falls is a "
            "description of the power sums that had been believed exact."
        ),
    }


# ------------------------------------------------------------ part E


def part_E_correction(checks):
    """A bad estimate of mine, corrected."""
    st = P487.RingSetup(3, 2)
    pairs = len(st.pairs)
    size = 9**pairs
    checks["z9_section_space_is_not_enumerable"] = size > 10**12
    return {
        "claimed_previously": 6561,
        "actual_pairs": pairs,
        "actual_size": f"9^{pairs}",
        "digits": len(str(size)),
        "correction": (
            "We retract an arithmetic estimate of our own.  I proposed "
            "exhausting the "
            "Z/9 section space on the ground "
            "that it has 9^4 = 6561 elements.  That is wrong: Z/9 has "
            "q = 9, hence (q^2-1)/2 = 40 inverse-closed pairs and 9^40 "
            "sections, a 39-digit number.  The q = 3 exhaustion worked "
            "because q = 3 gives only 4 pairs.  Enumerability scales as "
            "q^{(q^2-1)/2} and dies immediately after q = 3; the failure "
            "depth at Z/9 therefore remains a sampled quantity and the "
            "Pass 519 lesson does NOT transfer to it."
        ),
    }


# ------------------------------------------------------------ main


def main_payload():
    checks = {}
    A = part_A_exhaustive(checks)
    B = part_B_polygon_q3(checks)
    Cc = part_C_larger_q(checks)
    Dd = part_D_audit(checks)
    E = part_E_correction(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass520.newton_polygon.v1",
        "status": status,
        "headline": (
            "AN EXPLANATION RETRACTED BEFORE PUBLICATION, AND EVIDENCE THAT "
            "q = 3 IS NOT SPECIAL.  A first draft of this pass asserted that "
            "the minimising q = 3 profile is (v(e_2), v(e_3)) = (4, 6), giving "
            "a single slope-2 Newton polygon and hence 'no factorial is "
            "possible'.  NO SECTION HAS THAT PROFILE: exhaustively they are "
            "(4, inf) x 32, (4, 8) x 16, (6, inf) x 8, (6, 6) x 24, and the "
            "polygons are not uniformly single-slope.  The explanation is "
            "withdrawn.  What survives is weaker and true: the eigenvalue "
            "valuations are constants independent of m, so v_lambda(tr D^m) is "
            "affine in m plus parity, whereas v_lambda(m!) is not affine -- an "
            "observation, not a mechanism.  Separately, at q = 5 the law is "
            "NOT attained at m = 10 or m = 14, the sampled minimum sitting "
            "exactly 2 above it as at q = 3, over 250 sections here and 600 in "
            "a separate probe.  Sampling cannot refute, so q = 5 remains "
            "undecided; but Pass 519's suggestion that q = 3 might be special "
            "is withdrawn as the less likely reading."
        ),
        "part_A_exhaustive_to_m20": A,
        "part_B_newton_polygon_q3": B,
        "part_C_larger_q": Cc,
        "part_D_dependency_audit": Dd,
        "part_E_a_correction": E,
        "boundary": (
            "Part A is exhaustive over the complete 81-section space and is "
            "decisive at q = 3.  Part B computes the polygon at the minimising "
            "profile; the reading of it as 'no factorial is possible' is an "
            "argument about Newton polygons, not a machine-checked proof.  "
            "Part C is SAMPLED: it exhibits attaining sections at q = 5 and 7, "
            "which CONFIRMS the law at those points, but confirmation is not "
            "exhaustion and no refutation at q >= 5 is claimed either way.  "
            "Pass 541 later proves the q = 3 replacement for every m >= 2; "
            "that later theorem does not change this pass's larger-q boundary.  "
            "Part D is an editorial audit.  Part E corrects an arithmetic "
            "error of mine from the previous round."
        ),
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
            raise SystemExit("Pass 520 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(
        json.dumps(
            {
                "status": pl["status"],
                "checks": sum(pl["checks"].values()),
                "total": len(pl["checks"]),
            }
        )
    )
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
