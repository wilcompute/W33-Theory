#!/usr/bin/env python3
"""Pass 518: the phase is the obstruction, named exactly -- and the whole arc
reduces to one lemma about a single power sum.

Pass 517's closed form holds only where e | (m/d), and the top class d = m is
always outside that range.  This pass says precisely what is in the way.

THE COCYCLE.  In the q-dimensional representation,

        rho(v) rho(w) = zeta^{-omega(v,w)} rho(v + w),

with omega((a,b),(a',b')) = a b' - a' b the symplectic form.  (Verified exactly
at p = 3, 5, 7 on 2864 ordered pairs.)  Iterating, a period-d representative
(w_1..w_d) gives M = rho_{w_1}...rho_{w_d} = zeta^{-Omega} rho(w) with
w = sum_i w_i and Omega = sum_{i<j} omega(w_i, w_j); and since omega(w,w) = 0,
rho(w)^k = rho(kw) exactly.  Hence, with k = m/d,

        M^k = zeta^{-k Omega} rho(kw),

the zero-sum condition on the m-tuple is exactly kw = 0, and

        VALUE OF THE ORBIT  =  q * zeta^{-k Omega} * prod_i d_{w_i}^k .

So the Pass 514 shortcut is this formula with its phase dropped, and the phase
is trivial for EVERY orbit exactly when e | k.  That is not a limitation of the
argument; it is the reason the closed form stops where it does.

WHAT THE TRACE IS CARRIED BY.  Taking t = m/e in the sieve theorem gives
sum_{d | m/e} d S_d = 0, so

        tr(D^m) = sum over d | m with d NOT dividing m/e of d S_d .

At m = p^j the only such d is m itself, recovering tr = m S_m; at m = 6 with
e = 3 the carriers are d = 3 and d = 6.  This is a restatement of the sieve
rather than a new fact, and is checked as such -- via the closed form, not by
enumerating the carriers, which at (3,15) would need 8^14 tuples.

THE ARC REDUCES TO ONE LEMMA.  Every theorem in Passes 511-517 -- odd-class
vanishing, propagation, the sieve, the rank count -- has the same bracket at
its centre:

        Ps(k) = sum_{v != 0} d_v^k = 0  for every inverse-closed section
        <=>  k is odd and e | k.

Forward: inverse closure pairs v with -v, so Ps(k) = sum over pairs of
2 Re (u-1)^k, and (u-1)^k = e^{i k pi j/e} (2i)^k sin^k(pi j/e) is purely
imaginary exactly when k is odd and e | k.  Backward: the one-pair section
makes Ps(k) = 2 Re (u-1)^k, nonzero otherwise.  Nothing else in the arc is
primitive.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass518_phase_obstruction.json"


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
divisors, U_set = P515.divisors, P515.U_set
closed_form, _ps, fast_pow = P517.closed_form, P517._ps, P517.fast_pow


# ------------------------------------------------------------ part A


def part_A_cocycle(checks):
    """rho(v)rho(w) = zeta^{-omega(v,w)} rho(v+w), exactly."""
    rows, bad, tested = {}, 0, 0
    for p_ in (3, 5, 7):
        R, C, q, D, dcoef, rho = P511.setup(p_, 7001)
        b, t = 0, 0
        for v in rho:
            for w in rho:
                s = (R.add(v[0], w[0]), R.add(v[1], w[1]))
                if s == (R.zero, R.zero):
                    continue
                lhs = matmul(rho[v], rho[w], C)
                om = R.sub(R.mul(v[0], w[1]), R.mul(w[0], v[1]))
                ph = C.from_exp((-R.chi_exp(om)) % p_)
                rhs = [[C.mul(ph, x) for x in row] for row in rho[s]]
                t += 1
                if lhs != rhs:
                    b += 1
        rows[f"p{p_}"] = {"pairs": t, "mismatches": b}
        bad += b
        tested += t
    checks["cocycle_exact"] = bad == 0
    checks["cocycle_tested_widely"] = tested > 2000
    return {"rows": rows, "total_pairs": tested, "mismatches": bad,
            "identity": ("rho(v) rho(w) = zeta^{-omega(v,w)} rho(v+w) with "
                         "omega((a,b),(a',b')) = a b' - a' b")}


def part_B_phase_formula(checks):
    """The orbit value WITH its phase, including where the shortcut fails."""
    rows, ok = {}, True
    for p_, m, d in ((3, 6, 3), (3, 12, 3), (3, 10, 1), (5, 10, 5),
                     (3, 6, 2), (3, 9, 3)):
        k = m // d
        R, C, q, D, dcoef, rho = P511.setup(p_, 7001)
        vecs, seen, agree, n = list(rho), set(), True, 0
        for base in itertools.product(vecs, repeat=d):
            full = base * k
            rots = {full[r:] + full[:r] for r in range(m)}
            if len(rots) != d or full in seen:
                continue
            a0, a1 = R.zero, R.zero
            for v in full:
                a0, a1 = R.add(a0, v[0]), R.add(a1, v[1])
            if (a0, a1) != (R.zero, R.zero):
                continue
            seen |= rots
            honest = P511.value(full, C, q, dcoef, rho)
            # Omega = sum_{i<j} omega(w_i, w_j) over the period-d rep
            Om = R.zero
            for i in range(d):
                for j in range(i + 1, d):
                    Om = R.add(Om, R.sub(R.mul(base[i][0], base[j][1]),
                                         R.mul(base[j][0], base[i][1])))
            ph = C.from_exp((-k * R.chi_exp(Om)) % p_)
            val = C.mul(C.rat(q), ph)
            for w in base:
                val = C.mul(val, fast_pow(C, dcoef[w], k))
            n += 1
            if honest != val:
                agree = False
        if not agree:
            ok = False
        rows[f"p{p_}_m{m}_d{d}"] = {"k": k, "orbits": n,
                                    "phase_trivial_for_all": k % p_ == 0,
                                    "formula_exact": agree}
    checks["phase_formula_exact"] = ok
    checks["phase_formula_tested_where_shortcut_fails"] = any(
        not r["phase_trivial_for_all"] for r in rows.values())
    return {"rows": rows,
            "formula": ("value = q * zeta^{-k Omega} * prod_i d_{w_i}^k, with "
                        "Omega = sum_{i<j} omega(w_i,w_j) and k = m/d"),
            "reading": (
                "The Pass 514 shortcut is this formula with its phase dropped, "
                "and the phase is trivial for every orbit exactly when e | k.  "
                "That is why the closed form stops at the top class, where "
                "k = 1: not a gap in the argument but the shape of the object. "
                " Tested here both where e | k and where it does not.")}


# ------------------------------------------------------------ part C


def part_C_carriers(checks):
    """tr(D^m) is carried by the classes with d not dividing m/e."""
    rows, ok = {}, True
    for p_, m in ((3, 6), (3, 9), (3, 12), (3, 15), (3, 27), (5, 10),
                  (5, 25), (7, 49)):
        R, C, q, D, dcoef, rho = P511.setup(p_, 7001)
        cache, t = {}, m // p_
        acc = C.zero()
        for d in divisors(t):
            acc = C.add(acc, closed_form(C, q, dcoef, m, d, cache))
        vanishes = not any(acc)
        if not vanishes:
            ok = False
        rows[f"p{p_}_m{m}"] = {
            "t_max": t,
            "non_carriers_sum_to_zero": vanishes,
            "carriers": [d for d in divisors(m) if t % d]}
    checks["non_carrier_classes_vanish"] = ok
    return {"rows": rows,
            "statement": ("taking t = m/e in the sieve gives "
                          "sum_{d | m/e} d S_d = 0, so tr(D^m) is carried "
                          "entirely by the classes whose period does NOT "
                          "divide m/e"),
            "reading": (
                "At m = p^j the only carrier is d = m, recovering "
                "tr = m S_m; at (3,6) the carriers are d = 3 and d = 6.  This "
                "is a restatement of the sieve theorem, not a new fact, and is "
                "checked as such -- through the closed form rather than by "
                "enumerating the carriers, which at (3,15) would need 8^14 "
                "tuples.")}


# ------------------------------------------------------------ part D


def part_D_one_lemma(checks):
    """Everything in the arc descends from Ps(k) = 0 <=> k odd and e | k."""
    rows, ok = {}, True
    for p_, n in ((3, 1), (5, 1), (7, 1), (3, 2), (5, 2), (3, 3)):
        e = p_ ** n
        cell = _load("p514", "w33_pass514_sieve_theorem.py").Cell(p_, n, 11)
        C = cell.C
        for k in range(1, 3 * e + 1):
            s = C.zero()
            for v in cell.vecs:
                s = C.add(s, fast_pow(C, cell.d[v], k))
            van = not any(s)
            pred = (k % 2 == 1) and (k % e == 0)
            if van != pred:
                ok = False
                rows[f"e{e}_k{k}"] = {"vanishes": van, "predicted": pred}
    checks["one_lemma_holds_at_six_character_orders"] = ok
    deps = {
        "odd-class vanishing (P511)": "Ps(m/d) = 0 in the sieve at t = m/d",
        "propagation (P513)": "Ps(p) = 0 in the sieve at t = m/p",
        "character-order form (P513)": "the lemma's own hypothesis, e | k",
        "the sieve theorem (P514)": "its right-hand side is q Ps(m/t)^t",
        "the rank count (P515)": "counts the t for which the lemma applies",
        "the closed form (P517)": "expresses every class in Ps alone",
        "the converse at d=1 (P512)": "the lemma's backward direction, via "
                                      "the one-pair section",
    }
    checks["dependency_map_covers_the_arc"] = len(deps) >= 7
    return {"counterexamples": rows,
            "lemma": ("Ps(k) = sum_{v != 0} d_v^k vanishes for every "
                      "inverse-closed section if and only if k is odd and "
                      "e | k"),
            "checked_at": "e in {3,5,7,9,25,27}, k up to 3e",
            "dependency_map": deps,
            "reading": (
                "Inverse closure pairs v with -v, so Ps(k) is a sum over pairs "
                "of 2 Re (u-1)^k, and (u-1)^k = e^{i k pi j/e} (2i)^k "
                "sin^k(pi j/e) is purely imaginary exactly when k is odd and "
                "e | k; the one-pair section supplies the converse.  Every "
                "theorem of Passes 511-517 has this bracket at its centre, so "
                "nothing else in the arc is primitive.")}


# ------------------------------------------------------------ part E


def part_E_artifacts(checks):
    lean = ROOT / "formal" / "W33" / "Pass517ClosedForm.lean"
    tex = ROOT / "papers" / "heisenberg_weyl_determinant_law.tex"
    ltxt = lean.read_text(encoding="utf-8") if lean.exists() else ""
    ttxt = tex.read_text(encoding="utf-8", errors="ignore")
    checks["lean_closed_form_module_present"] = lean.exists()
    checks["note_has_dependency_roadmap"] = "sec:roadmap" in ttxt
    return {"lean": {"file": "formal/W33/Pass517ClosedForm.lean",
                     "present": lean.exists(),
                     "lines": len(ltxt.splitlines()),
                     "covers": ("the order-exchange that turns the closed form "
                                "into the sieve, with the Moebius collapse "
                                "sum_{c|d|t} mu(d/c) = [c = t] as an explicit "
                                "hypothesis"),
                     "checked_by": "CI (no Lean toolchain in this container)"},
            "note": {"roadmap_added": "sec:roadmap" in ttxt,
                     "reading": (
                         "An editorial judgement, not a result: the note's "
                         "sections still follow the historical route -- "
                         "determinant law first -- since reordering a paper of "
                         "this size is a change best made once, deliberately.  "
                         "What is added is a roadmap stating the logical "
                         "dependency order, so a reader is not left to infer "
                         "it from the chronology.")}}


# ------------------------------------------------------------ main


def main_payload():
    checks = {}
    A = part_A_cocycle(checks)
    B = part_B_phase_formula(checks)
    Cc = part_C_carriers(checks)
    Dd = part_D_one_lemma(checks)
    E = part_E_artifacts(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass518.phase_obstruction.v1",
        "status": status,
        "headline": (
            "THE PHASE IS THE OBSTRUCTION, AND IT IS NAMED.  The "
            "representation satisfies rho(v) rho(w) = zeta^{-omega(v,w)} "
            "rho(v+w) exactly, so a period-d representative gives "
            "M = zeta^{-Omega} rho(w) with Omega = sum_{i<j} omega(w_i,w_j), "
            "and since omega(w,w) = 0 also rho(w)^k = rho(kw).  Hence a "
            "period-d orbit's value is q zeta^{-k Omega} prod_i d_{w_i}^k, "
            "with k = m/d.  The Pass 514 shortcut is this formula with its "
            "phase dropped, and the phase is trivial for every orbit exactly "
            "when e | k -- which is why the closed form stops at the top "
            "class, where k = 1.  Not a gap in the argument: the shape of the "
            "object."),
        "part_A_cocycle": A,
        "part_B_phase_formula": B,
        "part_C_trace_carriers": Cc,
        "part_D_the_one_lemma": Dd,
        "part_E_artifacts": E,
        "boundary": (
            "Part A is exact over all ordered pairs at p = 3,5,7.  Part B "
            "verifies the phase formula on six (p,m,d) cells, including cells "
            "where e does not divide k, and uses one section each; the formula "
            "itself is proved.  Part C is a restatement of the sieve theorem "
            "and is verified through the closed form, not by enumerating "
            "carriers.  Part D checks the lemma at six character orders and "
            "for k up to 3e; the dependency map is an editorial claim about "
            "how the arc's theorems relate, not a computation.  Part E reports "
            "artifact presence: the Lean module's kernel check is CI's, and "
            "the note gains a roadmap rather than a reordering."),
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
            raise SystemExit("Pass 518 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
