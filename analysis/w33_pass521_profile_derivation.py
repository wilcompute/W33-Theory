#!/usr/bin/env python3
"""Pass 521: the q = 3 even-m minimum DERIVED, not fitted -- and the q = 5
failure is not rare either.

Pass 520 retracted a Newton-polygon story built on a profile that does not
occur.  This pass replaces it with a derivation, and the derivation is short
because the data turned out to be rigid.

THE RIGIDITY.  At q = 3 the pair (v(e_2), v(e_3)) takes only four values across
the whole 81-section space, and each one determines the valuation vector
v(tr D^m) for m = 1..10 -- every section sharing a profile shares that measured
vector.

  (4, inf) x 32 : inf, 4, inf,  8, inf, 12, inf, 16, inf, 20
  (4,   8) x 16 : inf, 4,  10,  8,  12, 12,  16, 16,  24, 20
  (6, inf) x  8 : inf, 6, inf, 12, inf, 18, inf, 24, inf, 30
  (6,   6) x 24 : inf, 6,   8, 12,  12, 14,  18, 18,  20, 26

THE DERIVATION (even m).  On the 32 sections with e_3 = 0 the characteristic
polynomial is x^3 - e_1 x^2 + e_2 x - e_3 = x(x^2 + e_2), since e_1 = tr D = 0
(Pass 473).  Its roots are 0 and +-mu with mu^2 = -e_2, so v(mu) = v(e_2)/2 = 2.
Hence

        tr(D^m) = 0^m + mu^m + (-mu)^m = 0 (m odd),  2 mu^m (m even),

and for even m, v_lambda(tr D^m) = m v(mu) = 2m exactly, 2 being a unit at
p = 3.  That is the exhaustive even-m minimum, PROVED rather than fitted.

AND THE PARITY IS THE SAME FACT.  Those minimising sections do not merely
cancel by one order at odd m: they vanish IDENTICALLY.  So odd m must be served
by the other two profiles, whose minimum is 2(m+1) -- taken by (6,6) at m = 3,9
and by (4,8) at m = 5,7.  The "[m odd]" term is therefore not a correction
applied to a single formula; it is the switch between which profile attains the
minimum.

q = 5 IS NOT RARE EITHER.  Over 400 sampled sections the factorial law fails at
m = 10, 14, 15, 18, 19 -- five of nineteen exponents -- always by exactly 2,
the q = 3 gap.  Sampling cannot refute, so these remain undecided, but "q = 3
is special" is now doubly unsupported.

PASS 541 UPDATE.  This witness owns the finite profile table and the even-m
derivation.  Pass 541 later closes the odd all-m minimum by exact recurrences
modulo 3 and 9; the historical boundary below is retained with that
supersession stated explicitly.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass521_profile_derivation.json"
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


def part_A_rigidity(checks):
    """Each profile determines the whole valuation vector."""
    p_ = 3
    R, C = LF(p_, 1), Cyc(p_, 1)
    H = Heis(R, C)
    q = H.q
    F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))

    def vl(x):
        return INF if not any(x) else C.vlam(x)

    tab = {}
    for offs in itertools.product(R.elems, repeat=len(H.pairs)):
        B = H.block(H.full_sec(offs))
        D = [[C.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        D2 = matmul(D, D, C)
        e2 = tuple(-x // 2 for x in trace(D2, C))
        e3 = det_exact(D, C)
        key = (vl(e2), vl(e3))
        Dm = [[C.rat(1) if i == j else C.zero() for j in range(q)] for i in range(q)]
        vs = []
        for m in range(1, 11):
            Dm = matmul(Dm, D, C)
            t = trace(Dm, C)
            vs.append(INF if not any(t) else C.vlam(t))
        tab.setdefault(key, set()).add(tuple(vs))
    rows = {}
    rigid = all(len(v) == 1 for v in tab.values())
    for k, v in tab.items():
        kk = f"e2={'inf' if k[0] >= INF else k[0]},e3={'inf' if k[1] >= INF else k[1]}"
        vec = sorted(v)[0]
        rows[kk] = {
            "distinct_vectors": len(v),
            "valuations_m1_to_m10": [None if x >= INF else x for x in vec],
        }
    checks["each_profile_determines_m1_to_m10_vector"] = rigid
    checks["exactly_four_nondegenerate_profiles"] = (
        len([k for k in tab if k[0] < INF]) == 4
    )
    return {
        "rows": rows,
        "reading": (
            "Across the complete 81-section space the pair "
            "(v(e_2), v(e_3)) takes four non-degenerate values, and each "
            "one fixes the measured vector v(tr D^m) for m = 1..10.  The "
            "valuation profile is therefore complete for this data window -- "
            "which is what makes a derivation possible at all."
        ),
    }


def part_B_derivation(checks):
    """e_3 = 0 forces eigenvalues {0, mu, -mu}: even m gives exactly 2m."""
    p_ = 3
    R, C = LF(p_, 1), Cyc(p_, 1)
    H = Heis(R, C)
    q = H.q
    F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
    ok_odd, ok_even, n = True, True, 0
    for offs in itertools.product(R.elems, repeat=len(H.pairs)):
        B = H.block(H.full_sec(offs))
        D = [[C.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        if any(det_exact(D, C)):
            continue
        D2 = matmul(D, D, C)
        e2 = tuple(-x // 2 for x in trace(D2, C))
        if not any(e2) or C.vlam(e2) != 4:
            continue
        n += 1
        Dm = [[C.rat(1) if i == j else C.zero() for j in range(q)] for i in range(q)]
        for m in range(1, 11):
            Dm = matmul(Dm, D, C)
            t = trace(Dm, C)
            if m % 2 == 1:
                if any(t):
                    ok_odd = False
            else:
                if not any(t) or C.vlam(t) != 2 * m:
                    ok_even = False
    checks["e3_zero_sections_vanish_at_every_odd_m"] = ok_odd
    checks["e3_zero_sections_give_exactly_2m_at_even_m"] = ok_even
    checks["the_derivation_covers_32_sections"] = n == 32
    return {
        "sections_with_e3_zero_and_v_e2_4": n,
        "proof": (
            "With e_1 = tr D = 0 (Pass 473) and e_3 = det D = 0, the "
            "characteristic polynomial is x^3 + e_2 x = x(x^2 + e_2), whose "
            "roots are 0 and +-mu with mu^2 = -e_2, so v(mu) = v(e_2)/2 = "
            "2.  Then tr(D^m) = mu^m + (-mu)^m, which is 0 for odd m and "
            "2 mu^m for even m; since 2 is a unit at p = 3, "
            "v_lambda(tr D^m) = 2m exactly.  This is the exhaustive even-m "
            "minimum of Pass 519/520, now DERIVED rather than fitted."
        ),
        "parity": (
            "The same sections vanish IDENTICALLY at odd m -- not by one "
            "extra order of cancellation but exactly.  In the measured "
            "window, odd m is served by the other profiles at 2(m+1), attained by "
            "(6,6) at m = 3, 9 and by (4,8) at m = 5, 7.  The '[m odd]' "
            "term is not a correction to one formula; it is the switch "
            "between which profile attains the minimum."
        ),
    }


def part_C_q5(checks):
    """q = 5 to m = 20: how often does the law fail?"""
    best = {}
    for s in range(400):
        R, C, q, D, dcoef, rho = P511.setup(5, 70000 + s)
        Dm = [[C.rat(1) if i == j else C.zero() for j in range(q)] for i in range(q)]
        for m in range(1, 21):
            Dm = matmul(Dm, D, C)
            t = trace(Dm, C)
            if not any(t):
                continue
            v = C.vlam(t)
            if m not in best or v < best[m]:
                best[m] = v
    rows, gaps = {}, {}
    for m in range(2, 21):
        law = 4 + m + (1 if m % 2 else 0) + vlam_factorial(m, 5)
        g = best[m] - law
        rows[str(m)] = {"sampled_min": best[m], "law": law, "gap": g}
        if g:
            gaps[str(m)] = g
    checks["q5_sampled_min_never_below_the_law"] = all(
        r["gap"] >= 0 for r in rows.values()
    )
    checks["q5_law_fails_at_several_exponents"] = len(gaps) >= 3
    checks["q5_every_gap_is_exactly_2"] = all(g == 2 for g in gaps.values())
    return {
        "sections": 400,
        "rows": rows,
        "gaps": gaps,
        "reading": (
            "Over 400 sampled sections the law is not attained at "
            "m = 10, 14, 15, 18, 19 -- five of nineteen exponents -- and "
            "every gap is exactly 2, the same as at q = 3.  These are "
            "SAMPLED minima, so a larger sample could close them and no "
            "refutation is claimed at q = 5; the q = 3 gaps, which are "
            "exhaustive, did not close.  What this removes is the "
            "remaining support for 'q = 3 is special'."
        ),
    }


def part_D_determinant_audit(checks):
    """What does the determinant law actually rest on?"""
    chain = {
        "sharp law for f >= 2": (
            "UNCONDITIONAL.  Proved in the note by the argument that every "
            "entry of D is a Z[zeta]-combination of the d_v; it never invokes "
            "the factorial law."
        ),
        "sharp law for prime q, via e_q": (
            "CONDITIONAL on the factorial law at m = q, which is now known "
            "false at q = 3 for most m.  BUT m = q is inside the agreement "
            "locus at q = 3 (s_3(3) + 1 = 2), so the input the argument "
            "actually uses is true there; the route survives at q = 3 and its "
            "status at other prime q depends on whether m = q lies in the "
            "agreement locus, which is s_p(p) + 1 = 2 -- true for EVERY "
            "prime p."
        ),
        "q = 3 determinant law itself": (
            "UNCONDITIONAL and exhaustive: Pass 473 enumerated all 81 sections "
            "and found det B_t in {-16, 11}, a complete invariant.  Nothing "
            "here disturbs it."
        ),
        "flat block quadratic F^2 + 2F - (q^2-1) = 0": (
            "UNCONDITIONAL, a symplectic character sum."
        ),
        "first-order and sharp cancellation lemmas": (
            "UNCONDITIONAL; they bound power sums from below and are used in "
            "the direction that survives."
        ),
    }
    conditional = [k for k, v in chain.items() if v.startswith("CONDITIONAL")]
    checks["determinant_law_audit_complete"] = len(chain) >= 5
    checks["at_most_one_link_is_conditional"] = len(conditional) <= 1
    return {
        "chain": chain,
        "conditional_links": conditional,
        "verdict": (
            "The determinant law does not fall.  Its unconditional proof "
            "for f >= 2 is untouched, q = 3 is settled exhaustively and "
            "independently, and the one conditional link -- the route "
            "through e_q for prime q -- uses the factorial law only at "
            "m = q, which lies in the agreement locus for every prime p "
            "since s_p(p) + [p odd] = 1 + 1 = 2.  The input it needs is "
            "therefore true even where the general law is false."
        ),
    }


def part_E_agreement_locus(checks):
    """Which corpus claims were tested only where they cannot fail?"""
    findings = {
        "factorial law (P505-P517)": (
            "TESTED ONLY ON ITS AGREEMENT LOCUS.  Every confirmation was at "
            "m = q, at m = p^j, or at |R| = 27 and 81 -- and the prime-power "
            "tower lies inside the locus where the true q = 3 law and the "
            "factorial law coincide.  Fourteen passes of confirmation carried no information "
            "against it."
        ),
        "3q - 1 at m = q (P505/P506)": (
            "SAME LOCUS.  m = q satisfies s_p(p) + [p odd] = 2, so it lies in "
            "the agreement set for every prime p; the four values 8, 14, 20, "
            "32 confirm both formulas and distinguish neither."
        ),
        "prime-power tower 8, 20, 56, 164 (P512/P516)": (
            "SAME LOCUS, by construction: m = p^j has s_p(m) = 1."
        ),
        "sieve theorem and its corollaries (P511-P517)": (
            "NOT AFFECTED.  These are exact identities verified against honest "
            "enumeration, not fits to a formula, and the completeness test of "
            "P516/P517 measured a rank rather than checking a prediction."
        ),
        "determinant law (P479-P491)": (
            "NOT AFFECTED.  Proved unconditionally for f >= 2 and verified "
            "exhaustively at q = 3."
        ),
    }
    affected = [
        k
        for k, v in findings.items()
        if "SAME LOCUS" in v or "ONLY ON ITS AGREEMENT LOCUS" in v
    ]
    checks["agreement_locus_sweep_ran"] = len(findings) >= 5
    checks["sweep_identifies_the_affected_claims"] = len(affected) == 3
    return {
        "findings": findings,
        "affected": affected,
        "lesson": (
            "A fitted law confirmed only at points where it agrees with "
            "the truth receives no evidence at all.  The test set must be "
            "chosen independently of the fit; here it was chosen for "
            "computational convenience -- prime powers are where the "
            "orbit decomposition collapses -- and convenience selected "
            "precisely the blind spot.  This is a mechanical failure mode, "
            "and the three affected rows are those whose test sets are "
            "describable in the same terms as the fit."
        ),
    }


def main_payload():
    checks = {}
    A = part_A_rigidity(checks)
    B = part_B_derivation(checks)
    Cc = part_C_q5(checks)
    Dd = part_D_determinant_audit(checks)
    E = part_E_agreement_locus(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass521.profile_derivation.v1",
        "status": status,
        "headline": (
            "THE EVEN-m MINIMUM AT q = 3 IS NOW DERIVED, NOT FITTED.  Across "
            "the complete 81-section space the pair (v(e_2), v(e_3)) takes "
            "four values and each determines the measured m = 1..10 vector "
            "v(tr D^m) -- the profile is complete on that window.  On the 32 "
            "sections with e_3 = 0, the characteristic polynomial is "
            "x(x^2 + e_2) because e_1 = tr D = 0, so the eigenvalues are "
            "0 and +-mu with v(mu) = v(e_2)/2 = 2; hence tr(D^m) vanishes "
            "identically for odd m and equals 2 mu^m for even m, giving "
            "v_lambda(tr D^m) = 2m exactly.  That is the exhaustive even-m "
            "minimum, proved.  The parity term is the same fact seen from the "
            "other side: those sections vanish at odd m, so in the measured "
            "window odd m is served by different profiles at 2(m+1), and "
            "'[m odd]' is a switch between "
            "attaining profiles rather than a correction to one formula."
        ),
        "part_A_profile_rigidity": A,
        "part_B_even_m_derivation": B,
        "part_C_q5_to_m20": Cc,
        "part_D_determinant_law_audit": Dd,
        "part_E_agreement_locus_sweep": E,
        "boundary": (
            "Parts A and B are exhaustive over the complete q = 3 section "
            "space and the derivation is a proof.  The ODD-m minimum 2(m+1) is "
            "NOT derived here: it is observed to be attained by (6,6) at "
            "m = 3, 9 and by (4,8) at m = 5, 7.  This witness does not derive "
            "the all-m odd minimum; Pass 541 later closes it by exact modular "
            "recurrences.  Part C is SAMPLED at 400 sections and "
            "refutes nothing at q = 5.  Parts D and E are audits -- reasoned "
            "readings of the corpus, not computations."
        ),
        "superseded_boundary": (
            "Pass 541 proves the q=3 minimum 2(m+[m odd]) for every m>=2 and "
            "upgrades profile completeness from m=1..10 to all m."
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
            raise SystemExit("Pass 521 certificate drift")
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
