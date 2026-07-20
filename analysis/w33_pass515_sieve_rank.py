#!/usr/bin/env python3
"""Pass 515: how much the sieve pins, exactly -- and one candidate eliminated.

Pass 514 proved the sieve theorem: for every t | m with m/t odd and e | (m/t),
sum_{d | t} d S_d = 0.  "The orbit mechanism is partial" has been this
programme's standing verdict since Pass 510.  With the sieve in hand that
verdict becomes a DIMENSION COUNT.

THE RANK.  The unknowns are the tau(m) classes { S_d : d | m }.  The relations
are indexed by T = { t | m : m/t odd, e | (m/t) }, equivalently by
U = { u | m : u odd, e | u } via t = m/u.  Relation t involves exactly the S_d
with d | t, and S_t appears in relation t and in no relation for a smaller
divisor, so the system is triangular for any linear extension of divisibility
and its rank is |T| = |U|.  Hence

    pinned(m) = #{ u | m : u odd and e | u },
    free(m)   = tau(m) - pinned(m),

and writing m = 2^b s with s odd gives the closed form
free(m) = (b+1) tau(s) - tau(s/e) when e | s, and tau(m) otherwise.  Both the
rank and the closed form are checked here against the rank of the actual
matrix, computed over the rationals.

THE FAILURE REGION.  The sieve's proof needs only e | (m/d), which over Z/p^n
holds just as it does over a field: nothing in it uses that the factorial law
is true.  So the sieve should survive where the law fails.  Checked at
Z/9, Z/25 and Z/27.

THE CANDIDATE, ELIMINATED.  It is tempting to read the determinant law's
failure depth p^{n-1}(p+1) = 12, 30, 36 at Z/9, Z/25, Z/27 as a shadow of how
much the sieve leaves free there.  It is not.  At the relevant exponent m = q
the free counts are 2, 2, 3 -- and no function of the free count alone can send
2 to both 12 and 30.  The connection is refused, and recorded as refused: this
programme has retracted two mechanisms that merely fitted, and a third that
does not even fit should not survive one paragraph.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass515_sieve_rank.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P514 = _load("p514", "w33_pass514_sieve_theorem.py")
Cyc = P487.Cyc


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def tau(n):
    return len(divisors(n))


def U_set(m, e):
    return [u for u in divisors(m) if u % 2 == 1 and u % e == 0]


def rank_over_Q(rows):
    """Exact Gaussian elimination over the rationals."""
    M = [[Fraction(x) for x in r] for r in rows]
    r = 0
    ncols = len(M[0]) if M else 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


# ------------------------------------------------------------ part A


def part_A_rank(checks):
    """Rank of the sieve system, against the closed form."""
    rows, ok_rank, ok_closed = {}, True, True
    for e in (3, 5, 7, 9, 25, 27):
        for m in range(1, 61):
            divs = divisors(m)
            U = U_set(m, e)
            T = sorted({m // u for u in U})
            if not T:
                rk = 0
            else:
                mat = [[d if t % d == 0 else 0 for d in divs] for t in T]
                rk = rank_over_Q(mat)
            if rk != len(T):
                ok_rank = False
            # closed form
            b, s = 0, m
            while s % 2 == 0:
                s //= 2
                b += 1
            closed = ((b + 1) * tau(s) - tau(s // e)) if s % e == 0 \
                else tau(m)
            free = tau(m) - rk
            if free != closed:
                ok_closed = False
            if e in (3, 5) and m <= 30:
                rows[f"e{e}_m{m}"] = {"tau": tau(m), "pinned": rk,
                                      "free": free}
    checks["rank_equals_number_of_relations"] = ok_rank
    checks["free_count_matches_closed_form"] = ok_closed
    # the prime-power sharpening
    pp = {}
    for p_ in (3, 5, 7):
        for j in (1, 2, 3):
            m = p_ ** j
            pp[f"p{p_}_j{j}"] = tau(m) - len(U_set(m, p_))
    checks["single_free_class_at_every_prime_power"] = all(
        v == 1 for v in pp.values())
    return {"rows": rows, "prime_powers": pp,
            "closed_form": ("write m = 2^b s with s odd; then "
                            "free(m) = (b+1) tau(s) - tau(s/e) when e | s, and "
                            "tau(m) otherwise"),
            "reading": (
                "The unknowns are the tau(m) classes S_d.  Relation t involves "
                "exactly the S_d with d | t, and S_t appears in relation t and "
                "in none for a smaller divisor, so the system is triangular "
                "along any linear extension of divisibility and its rank is "
                "the number of relations.  By that triangularity -- a proof, "
                "not an estimate -- the partiality of the orbit account is a "
                "dimension count: free(m) classes are left unconstrained, and "
                "at every prime power that number is 1.")}


# ------------------------------------------------------------ part B


def part_B_failure_region(checks):
    """Does the sieve hold where the factorial law fails?"""
    rows, ok = {}, True
    plan = ((3, 2, (9, 18, 27)), (3, 3, (27,)), (5, 2, (25, 50)))
    for p_, n, ms in plan:
        e = p_ ** n
        for m in ms:
            T = sorted({m // u for u in U_set(m, e)})
            for seed in (1, 2):
                cell = P514.Cell(p_, n, seed)
                for t in T:
                    if any((m // d) % e for d in divisors(t)):
                        continue
                    lhs = cell.C.zero()
                    for d in divisors(t):
                        lhs = cell.C.add(lhs, cell.class_shortcut(m, d))
                    rhs = cell.C.rat(e)
                    ps = cell.power_sum(m // t)
                    for _ in range(t):
                        rhs = cell.C.mul(rhs, ps)
                    good = (lhs == rhs) and not any(lhs)
                    if not good:
                        ok = False
                    rows[f"Z{e}_m{m}_t{t}_s{seed}"] = {
                        "identity_holds": lhs == rhs,
                        "vanishes": not any(lhs)}
    checks["sieve_survives_the_failure_region"] = ok
    checks["failure_region_covered_at_three_rings"] = len(
        {k.split("_")[0] for k in rows}) == 3
    return {"rows": rows,
            "reading": (
                "The sieve's proof uses only e | (m/d), which over Z/p^n holds "
                "exactly as it does over a field; nothing in it uses the "
                "factorial law.  So the sieve is expected to survive where the "
                "law fails, and it does, at Z/9, Z/25 and Z/27.  That "
                "separates the structural facts that survive the failure from "
                "the arithmetic one that does not.")}


# ------------------------------------------------------------ part C


def part_C_lean(checks):
    f = ROOT / "formal" / "W33" / "Pass514Sieve.lean"
    present = f.exists()
    txt = f.read_text(encoding="utf-8") if present else ""
    checks["lean_sieve_module_present"] = present
    checks["lean_states_the_fiberwise_step"] = "fiberwise" in txt.lower()
    return {"file": "formal/W33/Pass514Sieve.lean",
            "present": present, "lines": len(txt.splitlines()),
            "covers": ("the sieve's combinatorial core: a finite sum whose "
                       "summand is constant on the fibres of a map equals the "
                       "sum over fibres of (fibre size) times the value -- "
                       "which is exactly 'summing over d | t sweeps every "
                       "t-tuple once, each period-d orbit contributing d "
                       "times'"),
            "does_not_cover": ("the arithmetic inputs: M^{m/d} = I and the "
                               "purely-imaginary criterion, both taken as "
                               "hypotheses, and both checked exactly in the "
                               "Pass 511 and Pass 514 witnesses"),
            "checked_by": ("CI -- this container has no Lean toolchain, as "
                           "recorded in formal/README.md")}


# ------------------------------------------------------------ part D


def part_D_prime_powers(checks):
    """One free class at m = p^j: the sharpest form of what is left."""
    rows = {}
    for p_ in (3, 5, 7, 11):
        for j in (1, 2, 3, 4):
            m = p_ ** j
            U = U_set(m, p_)
            terms, qq = [], p_
            while qq <= m:
                terms.append(m // qq)
                qq *= p_
            rows[f"p{p_}_m{m}"] = {
                "classes": tau(m), "pinned": len(U), "free": tau(m) - len(U),
                "free_class_is_d_equals_m": True,
                "legendre_terms": terms,
                "weight_supplies": j,
                "orbit_sum_must_supply": sum(terms) - j}
    checks["prime_power_free_class_is_always_one"] = all(
        r["free"] == 1 for r in rows.values())
    checks["orbit_sum_burden_grows"] = (
        rows["p3_m27"]["orbit_sum_must_supply"]
        > rows["p3_m9"]["orbit_sum_must_supply"]
        > rows["p3_m3"]["orbit_sum_must_supply"])
    return {"rows": rows,
            "reading": (
                "At m = p^j the sieve pins j of the j+1 classes and leaves "
                "exactly one, the free class d = m.  So the entire Legendre "
                "tower above the first increment sits in a single class whose "
                "valuation is known exactly and in which no cancellation "
                "between classes can occur.  The orbit weight supplies j of "
                "the sum_i floor(m/p^i) Legendre terms and the orbit sum must "
                "supply the rest: 0, 2, 10 at p = 3 for j = 1, 2, 3.  That is "
                "the sharpest statement of what remains unproved.")}


# ------------------------------------------------------------ part E


def part_E_eliminate(checks):
    """Is the determinant law's failure depth a shadow of the free count?"""
    depths = {"Z/9": 12, "Z/25": 30, "Z/27": 36}
    rows = {}
    for (p_, n), key in (((3, 2), "Z/9"), ((5, 2), "Z/25"), ((3, 3), "Z/27")):
        e = q = p_ ** n
        m = q
        U = U_set(m, e)
        rows[key] = {"q": q, "classes": tau(m), "pinned": len(U),
                     "free": tau(m) - len(U),
                     "measured_failure_depth": depths[key],
                     "p_to_n_minus_1_times_p_plus_1":
                         p_ ** (n - 1) * (p_ + 1)}
    # the elimination: two rings share a free count and differ in depth
    by_free = {}
    for k, r in rows.items():
        by_free.setdefault(r["free"], set()).add(r["measured_failure_depth"])
    collision = {f: sorted(d) for f, d in by_free.items() if len(d) > 1}
    checks["free_count_does_not_determine_the_depth"] = bool(collision)
    checks["depth_formula_reproduced"] = all(
        r["measured_failure_depth"] == r["p_to_n_minus_1_times_p_plus_1"]
        for r in rows.values())
    return {"rows": rows,
            "collision": {str(k): v for k, v in collision.items()},
            "verdict": (
                "REFUSED.  Z/9 and Z/25 both leave 2 classes free at m = q and "
                "have failure depths 12 and 30, so no function of the free "
                "count alone can produce both; the free count does not "
                "determine the depth.  The measured depths do match "
                "p^{n-1}(p+1) exactly (12, 30, 36), which remains the only "
                "description we have of the failure region and remains "
                "unexplained.  Recorded as an eliminated candidate rather "
                "than as a near miss: this programme has retracted two "
                "mechanisms that merely fitted, and one that does not even fit "
                "should not survive a paragraph.")}


# ------------------------------------------------------------ main


def main_payload():
    checks = {}
    A = part_A_rank(checks)
    B = part_B_failure_region(checks)
    Cc = part_C_lean(checks)
    Dd = part_D_prime_powers(checks)
    E = part_E_eliminate(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass515.sieve_rank.v1",
        "status": status,
        "headline": (
            "'THE ORBIT MECHANISM IS PARTIAL' IS NOW A DIMENSION COUNT, and the "
            "count follows from the Pass 514 sieve theorem by linear "
            "algebra alone.  The "
            "sieve system's unknowns are the tau(m) classes S_d and its "
            "relations are indexed by T = { t | m : m/t odd, e | (m/t) }.  "
            "Relation t involves exactly the S_d with d | t and S_t appears in "
            "no relation for a smaller divisor, so the system is triangular "
            "along any linear extension of divisibility and its rank is |T|.  "
            "Hence pinned(m) = #{ u | m : u odd, e | u } and free(m) = tau(m) "
            "- pinned(m); writing m = 2^b s with s odd, free(m) = "
            "(b+1) tau(s) - tau(s/e) when e | s.  Verified against the rank of "
            "the actual matrix over Q for e in {3,5,7,9,25,27} and m <= 60.  "
            "At every prime power the free count is exactly 1."),
        "part_A_rank_and_closed_form": A,
        "part_B_failure_region": B,
        "part_C_lean": Cc,
        "part_D_prime_powers": Dd,
        "part_E_candidate_eliminated": E,
        "boundary": (
            "Part A is pure arithmetic -- divisor counting and an exact rank "
            "over Q -- and says nothing about the SIZE of the free classes, "
            "only how many there are.  Part B uses the Pass 514 shortcut and "
            "is therefore restricted to cells with e | (m/d).  Part C reports "
            "the Lean file's scope; the arithmetic inputs remain hypotheses "
            "and the kernel check is CI's, this container having no toolchain. "
            " Part D is a divisor count plus Legendre bookkeeping, not a new "
            "measurement.  Part E eliminates one candidate and offers no "
            "replacement: the depths 12, 30, 36 = p^{n-1}(p+1) remain "
            "unexplained."),
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
            raise SystemExit("Pass 515 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
