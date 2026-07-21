#!/usr/bin/env python3
"""Pass 524: the completeness result is a THEOREM cell by cell, the free-count
characterisation is repaired, and the q = 3 method does NOT transfer to q = 5.

Three things, one of them a negative result and one of them a status upgrade
that costs nothing but attention.

THE STATUS UPGRADE.  Passes 522 and 523 called nullity = |T| + [p does not
divide m] a "measurement".  It is stronger than that, cell by cell.  The lower
bound nullity >= |T| + [p not dividing m] is PROVED: the sieve relations are
genuine (Pass 514) and the vacuous relation is genuine (Pass 523), and the two
families never coexist (Pass 523).  The upper bound comes from exhibiting
explicit sections whose class vectors are linearly independent -- and rank
r forces nullity <= tau(m) - r.  Exhibiting independent vectors is a PROOF of a
rank lower bound, not a sample of one: the independence is exact arithmetic in
Q(zeta_p).  So for every cell where the two bounds meet, the equality is a
theorem about that cell.  What remains open is the statement for all m at once,
which no finite computation can supply.

THE REPAIR.  With free(m) = tau(m) - |T| - [p not dividing m]:
  * if p | m then free = tau(m) - |T|, which is 1 exactly when m = p^a;
  * if p does not divide m then free = tau(m) - 1, which is 1 exactly when
    tau(m) = 2, i.e. when m is prime.
So free(m) = 1 if and only if m is a power of p or m is a prime different from
p -- and free(1) = 0, since tau(1) = 1 and the correction applies.  Pass 517
claimed only the first branch.

THE NEGATIVE RESULT.  The q = 3 law was derived because the valuation profile
(v(e_2), v(e_3)) is a COMPLETE INVARIANT there: four profiles, four trace
vectors.  At q = 5 it is not.  Across 220 sections the profile
(v(e_2), ..., v(e_5)) takes 34 values which carry 52 distinct trace vectors --
so knowing the profile does not determine v(tr D^m).  The q = 3 derivation was
a small-q phenomenon and the method does not transfer.  Recorded so that a
later pass does not attempt it expecting the q = 3 experience.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass524_status_upgrade.json"
INF = 10**8


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P504 = _load("p504", "w33_pass504_trDq_fitting_and_noncommutative.py")
P511 = _load("p511", "w33_pass511_constant_orbit_theorem.py")
P515 = _load("p515", "w33_pass515_sieve_rank.py")
P517 = _load("p517", "w33_pass517_mobius_closed_form.py")

matmul, trace = P487.matmul, P504.trace
divisors, U_set, tau = P515.divisors, P515.U_set, P515.tau


def part_A_upgrade(checks):
    """Cell-by-cell the equality is a theorem, not a measurement."""
    rows, ok = {}, True
    for p_, m, want in ((3, 2, 12), (3, 4, 12), (3, 10, 10), (5, 4, 10),
                        (3, 3, 12), (3, 9, 12), (5, 5, 10), (7, 7, 8)):
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
        lower = len(U_set(m, p_)) + (0 if m % p_ == 0 else 1)
        upper = len(divs) - rk
        if upper != lower:
            ok = False
        rows[f"p{p_}_m{m}"] = {
            "tau": len(divs),
            "proved_lower_bound_on_nullity": lower,
            "rank_witnessed_by_explicit_sections": rk,
            "upper_bound_from_that_rank": upper,
            "equality_is_a_theorem_for_this_cell": upper == lower}
    checks["bounds_meet_on_every_cell"] = ok
    return {"rows": rows,
            "argument": (
                "The lower bound nullity >= |T| + [p not dividing m] is proved: "
                "the sieve relations are genuine (Pass 514), the vacuous "
                "relation is genuine (Pass 523), and the two families never "
                "coexist (Pass 523).  The upper bound comes from exhibiting "
                "sections whose class vectors are linearly independent over "
                "Q(zeta_p); exhibiting independent vectors PROVES a rank lower "
                "bound rather than sampling one, since the independence is "
                "exact arithmetic.  Where the bounds meet, the equality is a "
                "theorem about that cell."),
            "still_open": (
                "The statement for ALL m at once.  No finite computation can "
                "supply it, and the argument above is per-cell.")}


def part_B_repair(checks):
    """free(m) = 1 iff m is a power of p OR a prime other than p."""
    rows, ok = {}, True
    for p_ in (3, 5, 7):
        for m in range(1, 200):
            free = tau(m) - len(U_set(m, p_)) - (0 if m % p_ == 0 else 1)
            k = m
            while k % p_ == 0:
                k //= p_
            is_pow = (k == 1 and m > 1)
            is_other_prime = (tau(m) == 2 and m % p_ != 0)
            pred = is_pow or is_other_prime
            if (free == 1) != pred:
                ok = False
                rows[f"p{p_}_m{m}"] = {"free": free, "predicted": pred}
    checks["repaired_characterisation_holds"] = ok
    checks["free_of_one_is_zero"] = all(
        tau(1) - len(U_set(1, p_)) - 1 == 0 for p_ in (3, 5, 7))
    return {"counterexamples": rows,
            "range": "p in {3,5,7}, m in 1..199",
            "statement": (
                "free(m) = 1 if and only if m is a power of p, or m is a prime "
                "different from p.  If p | m then free = tau(m) - |T|, equal "
                "to 1 exactly for m = p^a; if p does not divide m then "
                "free = tau(m) - 1, equal to 1 exactly when tau(m) = 2.  Also "
                "free(1) = 0, since tau(1) = 1 and the correction applies."),
            "supersedes": (
                "Pass 517 claimed only the first branch, having used the "
                "uncorrected count free(m) = tau(m) - |T|.")}


def part_C_no_transfer(checks):
    """At q = 5 the profile is NOT a complete invariant."""
    def vl(C, x):
        return INF if not any(x) else C.vlam(x)

    tab = {}
    for s in range(220):
        R, C, q, D, dcoef, rho = P511.setup(5, 80000 + s)
        tr, Dm = {}, [[C.rat(1) if i == j else C.zero() for j in range(q)]
                      for i in range(q)]
        for k in range(1, 13):
            Dm = matmul(Dm, D, C)
            tr[k] = trace(Dm, C)
        E, fact = {0: C.rat(1)}, [1] * 6
        for i in range(1, 6):
            fact[i] = fact[i - 1] * i
        for k in range(1, 6):
            acc = C.zero()
            for i in range(1, k + 1):
                t = C.mul(E[k - i], tr[i])
                t = tuple((fact[k - 1] // fact[k - i]) * x for x in t)
                if i % 2 == 0:
                    t = tuple(-x for x in t)
                acc = C.add(acc, t)
            E[k] = acc
        prof = tuple(vl(C, E[k]) for k in range(2, 6))
        vec = tuple(vl(C, tr[m]) for m in range(1, 13))
        tab.setdefault(prof, set()).add(vec)
    nprof = len(tab)
    nvec = sum(len(v) for v in tab.values())
    rigid = all(len(v) == 1 for v in tab.values())
    checks["q5_profile_is_not_a_complete_invariant"] = not rigid
    checks["q5_sampled_enough_profiles_to_tell"] = nprof >= 10
    return {"sections": 220, "profiles": nprof, "distinct_trace_vectors": nvec,
            "profile_determines_vector": rigid,
            "splitting_profiles": sum(1 for v in tab.values() if len(v) > 1),
            "reading": (
                "At q = 3 the profile (v(e_2), v(e_3)) is a COMPLETE invariant "
                "-- four profiles, four trace vectors -- and that is what made "
                "the q = 3 law derivable.  At q = 5 it is not: 34 profiles "
                "carry 52 distinct trace vectors, so the profile does not "
                "determine v(tr D^m).  The q = 3 derivation was a small-q "
                "phenomenon and the method does NOT transfer.  Recorded so a "
                "later pass does not attempt it expecting the q = 3 "
                "experience.")}


def part_D_note(checks):
    f = ROOT / "papers" / "agreement_locus.tex"
    txt = f.read_text(encoding="utf-8") if f.exists() else ""
    checks["standalone_note_written"] = f.exists()
    checks["note_carries_all_three_examples"] = txt.count("\\section{Example") == 3
    return {"file": "papers/agreement_locus.tex",
            "present": f.exists(), "lines": len(txt.splitlines()),
            "contents": (
                "The agreement-locus failure mode with all three worked "
                "examples from this programme: the factorial law (confirmed "
                "only where s_p(m) + [m odd] = 2, which contains every prime "
                "power), the sieve completeness claim (tested only on cells "
                "with p | m, which is exactly the shortcut's own hypothesis), "
                "and the free-count characterisation (a correct proof from a "
                "premise carrying the same blind spot).  Ends with a cheap "
                "test: run the conjecture where it predicts something "
                "DEGENERATE, since degenerate predictions have no room to "
                "absorb an error."),
            "note": (
                "Proposed in four consecutive rounds and folded into the main "
                "papers each time; written this round rather than deferred "
                "again.")}


def main_payload():
    checks = {}
    A = part_A_upgrade(checks)
    B = part_B_repair(checks)
    Cc = part_C_no_transfer(checks)
    Dd = part_D_note(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass524.status_upgrade.v1",
        "status": status,
        "headline": (
            "THE COMPLETENESS RESULT IS A THEOREM CELL BY CELL, NOT A "
            "MEASUREMENT.  Its lower bound nullity >= |T| + [p not dividing m] "
            "is proved -- both relation families are genuine and they never "
            "coexist -- and its upper bound comes from exhibiting explicit "
            "sections whose class vectors are linearly independent over "
            "Q(zeta_p), which PROVES a rank lower bound rather than sampling "
            "one.  Where the bounds meet the equality is a theorem about that "
            "cell; only the all-m statement stays open.  Separately the "
            "free-count characterisation is repaired -- free(m) = 1 exactly "
            "when m is a power of p OR a prime other than p, with free(1) = 0 "
            "-- and a negative result is recorded: at q = 5 the valuation "
            "profile is NOT a complete invariant (34 profiles, 52 trace "
            "vectors), so the q = 3 derivation was a small-q phenomenon and "
            "the method does not transfer."),
        "part_A_status_upgrade": A,
        "part_B_repaired_free_count": B,
        "part_C_q5_does_not_transfer": Cc,
        "part_D_standalone_note": Dd,
        "boundary": (
            "Part A upgrades the status of results already obtained; it proves "
            "the equality for the eight listed cells and NOT for general m.  "
            "Part B is a divisor computation over p in {3,5,7} and m < 200, "
            "plus the two-branch argument, and is exact arithmetic.  Part C "
            "samples 220 sections at q = 5; since it exhibits profiles that "
            "SPLIT, the negative conclusion needs no exhaustiveness -- one "
            "splitting profile suffices.  Part D reports that a file exists "
            "and what it contains."),
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
            raise SystemExit("Pass 524 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
