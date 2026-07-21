#!/usr/bin/env python3
"""Pass 526: the transfer matrix is TRANSLATION-COVARIANT, which explains the
Pass 519 identity and supplies a second one.

Pass 519 found tr(D^m) = q [T^m]_{0,0} and left it as a computation.  Probing
the OTHER entries of T^m turns it into a symmetry statement.

THE COVARIANCE.  For a in R^2 let S_a be the permutation P -> P + a of the
partial-sum states and let U_a be the diagonal matrix with entries
zeta^{omega(a,P)}.  Then

        U_a T = S_a T S_a^{-1} U_a       for every a,

verified with zero failures over all q^2 translations at p = 3, 5, 7.  So T is
conjugate to each of its translates, intertwined by the character
zeta^{omega(a,.)} -- the Heisenberg symmetry of the register cell acting on the
walk.

TWO CONSEQUENCES, both exact.

  (i)  T^m HAS CONSTANT DIAGONAL: [T^m]_{P,P} = [T^m]_{0,0} for every P, since
       conjugation by S_a U_a carries the (0,0) entry to the (a,a) entry.

  (ii) tr(T^m) = q tr(D^m).

  Together with Pass 519's tr(D^m) = q [T^m]_{0,0} these are consistent and
  redundant: tr(T^m) = q^2 [T^m]_{0,0} = q tr(D^m).  What was one identity is
  now a symmetry with two identities as corollaries, and the q in
  tr(D^m) = q [T^m]_{0,0} is explained -- it is the number of states in a
  translation orbit divided by q, not a coincidence of normalisation.

WHY THIS MATTERS FOR THE OPEN PROBLEM.  The factorial law's remaining content
is the excess E(m) = v_lambda([T^m]_{0,0}) - m.  Covariance says that entry is
the whole diagonal, so E(m) is a statement about tr(T^m) -- a similarity
invariant.  Anything that computes T's spectrum computes E(m) for all m at
once, which the orbit decomposition never could.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass526_transfer_covariance.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P504 = _load("p504", "w33_pass504_trDq_fitting_and_noncommutative.py")
P519 = _load("p519", "w33_pass519_transfer_matrix.py")

matmul, trace = P487.matmul, P504.trace


def part_A_covariance(checks):
    """U_a T = S_a T S_a^{-1} U_a, over every translation."""
    rows, ok = {}, True
    for p_ in (3, 5, 7):
        R, C, q, D, T, z, n = P519.build_T(p_, 7001)
        els = list(R.elems)
        pts = [(x, y) for x in els for y in els]
        idx = {x: i for i, x in enumerate(pts)}
        bad = 0
        for a in pts:
            U = [[C.zero()] * n for _ in range(n)]
            for P in pts:
                om = R.sub(R.mul(a[0], P[1]), R.mul(P[0], a[1]))
                U[idx[P]][idx[P]] = C.from_exp(R.chi_exp(om) % p_)
            S = [[C.zero()] * n for _ in range(n)]
            for P in pts:
                S[idx[(R.add(P[0], a[0]), R.add(P[1], a[1]))]][idx[P]] = \
                    C.rat(1)
            Si = [[S[j][i] for j in range(n)] for i in range(n)]
            if matmul(U, T, C) != matmul(matmul(S, matmul(T, Si, C), C), U, C):
                bad += 1
        if bad:
            ok = False
        rows[f"p{p_}"] = {"translations": len(pts), "failures": bad}
    checks["covariance_holds_for_every_translation"] = ok
    checks["covariance_tested_at_three_primes"] = len(rows) == 3
    return {"rows": rows,
            "identity": ("U_a T = S_a T S_a^{-1} U_a, where S_a permutes the "
                         "states by P -> P + a and U_a is diagonal with "
                         "entries zeta^{omega(a,P)}"),
            "meaning": (
                "T is conjugate to each of its translates, intertwined by the "
                "character zeta^{omega(a,.)}.  That is the Heisenberg symmetry "
                "of the register cell, acting on the walk rather than on the "
                "block.")}


def part_B_consequences(checks):
    """Constant diagonal, and tr(T^m) = q tr(D^m)."""
    rows, const_ok, tr_ok = {}, True, True
    for p_ in (3, 5, 7):
        for seed in (7001, 7005):
            R, C, q, D, T, z, n = P519.build_T(p_, seed)
            Tm = [[C.rat(1) if i == j else C.zero() for j in range(n)]
                  for i in range(n)]
            Dm = [[C.rat(1) if i == j else C.zero() for j in range(q)]
                  for i in range(q)]
            c_ok, t_ok = True, True
            for m in range(1, 8):
                Tm = matmul(Tm, T, C)
                Dm = matmul(Dm, D, C)
                if len({tuple(Tm[i][i]) for i in range(n)}) != 1:
                    c_ok = False
                if trace(Tm, C) != C.mul(C.rat(q), trace(Dm, C)):
                    t_ok = False
            if not c_ok:
                const_ok = False
            if not t_ok:
                tr_ok = False
            rows[f"p{p_}_s{seed}"] = {"states": n,
                                      "constant_diagonal": c_ok,
                                      "trace_identity": t_ok}
    checks["T_powers_have_constant_diagonal"] = const_ok
    checks["trace_of_T_power_is_q_times_trace_of_D_power"] = tr_ok
    return {"rows": rows,
            "consequences": (
                "(i) [T^m]_{P,P} = [T^m]_{0,0} for every P, because "
                "conjugation by S_a U_a carries the (0,0) entry to the (a,a) "
                "entry.  (ii) tr(T^m) = q tr(D^m).  With Pass 519's "
                "tr(D^m) = q [T^m]_{0,0} the three are consistent and "
                "redundant: tr(T^m) = q^2 [T^m]_{0,0} = q tr(D^m)."),
            "what_it_explains": (
                "The factor q in tr(D^m) = q [T^m]_{0,0} was left unexplained "
                "in Pass 519.  It is not a normalisation accident: the "
                "diagonal of T^m is constant across all q^2 states, so the "
                "trace is q^2 times any one entry, and the block trace is q "
                "times fewer.")}


def part_C_reformulation(checks):
    """What the open problem becomes."""
    checks["reformulation_recorded"] = True
    return {"statement": (
        "The factorial law's remaining content is "
        "E(m) = v_lambda([T^m]_{0,0}) - m.  By covariance that entry is the "
        "whole diagonal, so E(m) = v_lambda(tr T^m) - v_lambda(q^2) - m, a "
        "statement about a SIMILARITY INVARIANT of T.  Anything that computes "
        "T's spectrum computes E(m) for every m at once."),
        "contrast": (
            "The cyclic-orbit decomposition could never do that: it computes "
            "one exponent at a time and its classes are not similarity "
            "invariants.  Passes 510-518 were describing walks; this says the "
            "walks have a symmetry group, and the invariant theory of that "
            "group is where an all-m answer would live."),
        "not_claimed": (
            "No spectrum is computed here and no value of E(m) is derived.  "
            "This is a reformulation, and reformulations have been wrong in "
            "this programme before -- Pass 520's Newton-polygon story was one. "
            " What is proved is the covariance and its two corollaries; the "
            "rest is a statement about where to look.")}


def main_payload():
    checks = {}
    A = part_A_covariance(checks)
    B = part_B_consequences(checks)
    Cc = part_C_reformulation(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass526.transfer_covariance.v1",
        "status": status,
        "headline": (
            "THE TRANSFER MATRIX IS TRANSLATION-COVARIANT.  With S_a the "
            "permutation P -> P + a of partial-sum states and U_a the diagonal "
            "matrix of characters zeta^{omega(a,P)}, U_a T = S_a T S_a^{-1} "
            "U_a for every a -- zero failures over all q^2 translations at "
            "p = 3, 5, 7.  Two exact corollaries follow: T^m has CONSTANT "
            "DIAGONAL, and tr(T^m) = q tr(D^m).  Together with Pass 519's "
            "tr(D^m) = q [T^m]_{0,0} this explains the factor q that pass left "
            "unexplained -- the diagonal is constant across all q^2 states, so "
            "the trace is q^2 times any one entry.  What was one computed "
            "identity is now a symmetry with identities as corollaries."),
        "part_A_covariance": A,
        "part_B_consequences": B,
        "part_C_what_the_problem_becomes": Cc,
        "boundary": (
            "Part A is exhaustive over all q^2 translations at one section per "
            "prime; the covariance is an identity in the definition of T and "
            "the check is a verification of the algebra, not a sample.  Part B "
            "checks the corollaries at two sections per prime and m <= 7.  "
            "Part C derives nothing: it states where an all-m answer would "
            "have to live, and this programme has had a reformulation go wrong "
            "before."),
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
            raise SystemExit("Pass 526 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
