#!/usr/bin/env python3
"""Pass 513: the odd-class vanishing theorem is about the CHARACTER ORDER, not
about p; and at prime powers the orbit weight explains a vanishing share of the
Legendre tower.

THE GENERALIZATION.  Pass 511 proved: for m = dk odd with p | k, the period-d
class of the cyclic-orbit decomposition of tr(D^m) vanishes identically over a
finite field of characteristic p.  Both ingredients that used p used it only
through the ORDER OF THE GENERATING CHARACTER, which over F_q happens to be p:

  (i)  rho_v^k = I needs (v,0)^k = identity, i.e. k v = 0 for every v -- which
       is k divisible by the exponent of the additive group as seen by psi;
  (ii) (u-1)^k purely imaginary needs k odd and ord(u) | k for every u in the
       image of psi.

Over Z/p^n the generating character has order p^n, not p.  So the theorem
should SHIFT, and the vanishing condition should read e | k with e = p^n.  It
does: over Z/9 the constant class vanishes at m = 9 and m = 27 and NOT at
m = 3, for every section sampled.  The statement is therefore

    THEOREM (character-order form).  Let R be a finite Frobenius ring with
    generating character psi of order e.  Write m = dk.  If m is odd and
    e | k, the period-d class vanishes identically.

which specializes to Pass 511 when e = p.  The same invariant -- the order of
the generating character -- is what governs the scope of the determinant law
itself (the law holds when e = p and fails over Z/p^n where e = p^n).  Two
statements that had been proved and tested separately turn out to be indexed by
the same number.

THE WEIGHT'S SHARE.  At m = p^j the collapse corollary leaves one class, so
tr(D^m) = m * S_m exactly and v_lambda(S_m) = v_lambda(tr D^m) - v_lambda(m)
with no enumeration required.  This separates what the ORBIT WEIGHT contributes
from what the orbit sum contributes -- and the weight's share of the Legendre
tower falls away fast: it supplies j of the sum_i floor(m/p^i) terms, which is
all of it at j = 1, half at j = 2, and 3/13 at j = 3.  So the weight explains
the first Legendre increment and progressively less thereafter, quantified.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass513_character_order_and_weight_share.json"
INF = 10**8


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P504 = _load("p504", "w33_pass504_trDq_fitting_and_noncommutative.py")
P511 = _load("p511", "w33_pass511_constant_orbit_theorem.py")

Cyc, matmul, RingSetup = P487.Cyc, P487.matmul, P487.RingSetup
trace = P504.trace


def vlam_factorial_terms(m, p):
    """Legendre's floor(m/p^i) terms of v_p(m!)."""
    out, q = [], p
    while q <= m:
        out.append(m // q)
        q *= p
    return out


def ident(C, q):
    return [[C.rat(1) if i == j else C.zero() for j in range(q)]
            for i in range(q)]


# ---------------------------------------------------------------- part A


def part_A_weight_share(checks):
    """m = p^j: tr = m * S_m exactly, so the weight separates."""
    rows = {}
    ok_ident, ok_share = True, True
    for p_, js, nsec in ((3, (1, 2, 3), 250), (5, (1, 2), 60)):
        for j in js:
            m = p_ ** j
            best, best_seed = None, None
            for seed in range(nsec):
                R, C, q, D, dcoef, rho = P511.setup(p_, 40000 + seed)
                Dm = D
                for _ in range(m - 1):
                    Dm = matmul(Dm, D, C)
                t = trace(Dm, C)
                if any(t):
                    v = C.vlam(t)
                    if best is None or v < best:
                        best, best_seed = v, seed
            terms = vlam_factorial_terms(m, p_)
            v_m = (p_ - 1) * j                       # v_lambda(p^j)
            v_fact = (p_ - 1) * sum(terms)
            # tr = m * S_m exactly (single surviving class), so:
            v_Sm = best - v_m
            share = j / sum(terms)
            rows[f"p{p_}_m{m}"] = {
                "v_lambda_trace": best, "minimizing_seed": best_seed,
                "v_lambda_m": v_m, "v_lambda_orbit_sum_S_m": v_Sm,
                "legendre_terms": terms, "v_lambda_m_factorial": v_fact,
                "weight_share_of_legendre": round(share, 4)}
            if not (v_Sm >= 0):
                ok_ident = False
            if j == 1 and abs(share - 1.0) > 1e-9:
                ok_share = False
    checks["weight_separates_at_prime_powers"] = ok_ident
    checks["weight_is_the_whole_tower_only_at_j_eq_1"] = ok_share
    shares = {k: r["weight_share_of_legendre"] for k, r in rows.items()}
    checks["weight_share_decreases_in_j"] = (
        shares["p3_m3"] > shares["p3_m9"] > shares["p3_m27"])
    return {"rows": rows,
            "reading": (
                "At m = p^j exactly one class survives, by the Pass 511 collapse "
                "corollary (a proved consequence of the odd-class theorem), so "
                "tr(D^m) = m * S_m EXACTLY and v_lambda(S_m) follows by "
                "subtraction with no enumeration.  The orbit weight supplies "
                "v_lambda(m) = j(p-1), i.e. j of the sum_i floor(m/p^i) "
                "Legendre terms: all of it at j = 1, half at j = 2, 3/13 at "
                "j = 3.  The weight therefore accounts for the FIRST Legendre "
                "increment and progressively less thereafter.  This is a "
                "quantified limit on the orbit mechanism.  What supplies the "
                "REMAINING Legendre terms is not identified here.")}


# ---------------------------------------------------------------- part B


def minimal_support_class(p_, m, d, pairs_used, seed):
    """Period-d class for a section supported on `pairs_used` pairs only."""
    R, C = P511.setup(p_, seed)[0], None
    R, C, q, D, dcoef0, rho = P511.setup(p_, seed)
    vecs = list(rho)
    # pick pairs_used inverse-closed pairs, flat elsewhere
    seen, chosen = set(), []
    for v in vecs:
        nv = (R.neg(v[0]), R.neg(v[1]))
        if v in seen or nv in seen:
            continue
        seen.add(v)
        seen.add(nv)
        chosen.append((v, nv))
        if len(chosen) == pairs_used:
            break
    active = {}
    for i, (v, nv) in enumerate(chosen):
        e = 1 + (i % (p_ - 1))
        active[v] = C.sub(C.from_exp(e), C.rat(1))
        active[nv] = C.sub(C.from_exp((-e) % p_), C.rat(1))
    dcoef = {v: active.get(v, C.zero()) for v in vecs}

    s, norb, seenT = C.zero(), 0, set()
    support = list(active)
    for base in itertools.product(support, repeat=d):
        full = base * (m // d)
        rots = {full[r:] + full[:r] for r in range(m)}
        if len(rots) != d or full in seenT:
            continue
        a0, a1 = R.zero, R.zero
        for v in full:
            a0, a1 = R.add(a0, v[0]), R.add(a1, v[1])
        if (a0, a1) != (R.zero, R.zero):
            continue
        seenT |= rots
        s = C.add(s, P511.value(full, C, q, dcoef, rho))
        norb += 1
    return (not any(s)), norb


def part_B_minimal_support(checks):
    """A constructive converse recipe: does minimal support suffice?"""
    plan = ((3, 6, 2), (3, 6, 3), (3, 12, 4), (3, 15, 3), (5, 10, 2),
            (5, 15, 5))
    rows, ok = {}, True
    for p_, m, d in plan:
        k = m // d
        hypothesis = (m % 2 == 1) and (k % p_ == 0)
        vanishes, norb = minimal_support_class(p_, m, d, d, 5130 + m)
        rows[f"p{p_}_m{m}_d{d}"] = {
            "k": k, "hypothesis_holds": hypothesis,
            "minimal_support_pairs": d, "orbits_in_support": norb,
            "class_vanishes": vanishes}
        # the recipe SUCCEEDS when the hypothesis fails and the class does not
        if not hypothesis and vanishes and norb > 0:
            ok = False
    checks["minimal_support_witnesses_nonvanishing"] = ok
    return {"rows": rows,
            "recipe": ("support the section on exactly d inverse-closed pairs "
                       "and enumerate the period-d orbits inside that support"),
            "verdict": (
                "The d = 1 converse of Pass 512 used a one-pair section.  The "
                "d-pair generalization produces a nonvanishing class in every "
                "tested cell where the hypothesis fails, so the recipe "
                "extends -- but a recipe that works on six cells is a recipe, "
                "not an induction, and the converse for general d is still "
                "NOT proved.")}


# ---------------------------------------------------------------- part C


def part_C_character_order(checks):
    """The vanishing condition is e | k with e = ord(psi), not p | k."""
    # (ii) the arithmetic criterion in Z[zeta_e], per root of unity
    arith, bad = {}, {}
    for p_, n in ((3, 1), (3, 2), (5, 1), (3, 3), (5, 2)):
        e = p_ ** n
        C = Cyc(p_, n)
        for k in range(1, 2 * e + 1):
            for jj in range(1, e):
                x = C.sub(C.from_exp(jj), C.rat(1))
                xk = C.rat(1)
                for _ in range(k):
                    xk = C.mul(xk, x)
                imag = not any(C.add(xk, C.sigma(e - 1, xk)))
                ordu = e // __import__("math").gcd(jj, e)
                pred = (k % 2 == 1) and (k % ordu == 0)
                if imag != pred:
                    bad[f"e{e}_k{k}_j{jj}"] = imag
        arith[str(e)] = "checked"
    checks["criterion_is_ord_u_divides_k_not_p_divides_k"] = not bad

    # the full class over Z/9: vanishes at m = 9, 27 and not at m = 3
    rows = {}
    ok = True
    for p_, n in ((3, 2),):
        e = p_ ** n
        st = RingSetup(p_, n)
        C, q = st.R, st.q
        for seed in (1, 2, 3):
            rng = random.Random(seed)
            fsec = st.full_sec(tuple(rng.randrange(q) for _ in st.pairs))
            rho = {}
            for (a, b) in fsec:
                N = [[C.zero() for _ in range(q)] for _ in range(q)]
                for x in range(q):
                    N[(x + a) % q][x] = C.from_exp((2 * x * b + a * b) % q)
                rho[(a, b)] = N
            I = ident(C, q)
            for m in (3, 9, 27):
                acc = C.zero()
                for v in rho:
                    dv = C.sub(C.from_exp(fsec[v]), C.rat(1))
                    dm = C.rat(1)
                    for _ in range(m):
                        dm = C.mul(dm, dv)
                    M = I
                    for _ in range(m):
                        M = matmul(M, rho[v], C)
                    acc = C.add(acc, C.mul(dm, trace(M, C)))
                van = not any(acc)
                pred = (m % 2 == 1) and (m % e == 0)
                if van != pred:
                    ok = False
                rows[f"Z{e}_s{seed}_m{m}"] = {
                    "class_vanishes": van,
                    "predicted_by_character_order": pred,
                    "predicted_by_p_alone": (m % 2 == 1) and (m % p_ == 0)}
    checks["Z9_class_follows_character_order_not_p"] = ok
    disagree = [k for k, r in rows.items()
                if r["predicted_by_character_order"]
                != r["predicted_by_p_alone"]]
    checks["the_two_predictions_actually_differ"] = bool(disagree)
    return {"arithmetic_criterion_checked_at_e": sorted(arith),
            "counterexamples": bad,
            "rows": rows,
            "cells_where_the_shift_is_visible": disagree,
            "theorem": (
                "CHARACTER-ORDER FORM.  Let R be a finite Frobenius ring with "
                "generating character psi of order e, and write m = dk.  If m "
                "is odd and e | k, the period-d class vanishes identically.  "
                "Pass 511 is the case e = p.  Over Z/9, e = 9: the constant "
                "class vanishes at m = 9 and 27 and NOT at m = 3, where "
                "'p | m' would have predicted vanishing.  The proof is Pass "
                "511's with p replaced by e throughout: (i) needs k v = 0 for "
                "every v, (ii) needs ord(u) | k for every u in the image of "
                "psi, and both are exactly e | k.")}


# ---------------------------------------------------------------- part D


def part_D_propagation(checks):
    """THE PROPAGATION THEOREM: at m = jp the classes with d | j sum to zero.

    Checking the m = 2p shape at a second prime turned up something stronger
    than a shape.  At (5,10) the period-1 and period-2 classes annihilate
    EXACTLY in every section, and the reason is algebraic:

        S_1 = q sum_v (d_v^p)^2,     2 S_2 = q sum_{v != w} (d_v d_w)^p,

    because tr(M^{m/d}) = q for both (the constant tuple has rho_v^{2p} = I,
    and a period-2 representative has (rho_v rho_w)^p = zeta^{ps} rho(p(v+w))
    = I).  Their sum is q (sum_v d_v^p)^2, which vanishes because sum_v d_v^p
    is exactly the m = p constant class killed by Pass 511.

    Nothing in that is special to j = 2.  For m = jp and any d | j, a period-d
    representative gives M^{m/d} = zeta^{s p j/d} rho((pj/d) w) = I, so its
    value is q times prod_i d_{w_i}^p over the underlying j-tuple, and grouping
    all j-tuples by cyclic orbit gives

        sum_{d | j} d S_d  =  q (sum_{v != 0} d_v^p)^j  =  0 .

    So the vanishing at m = p PROPAGATES to every multiple of p: at m = jp the
    classes whose period divides j cancel exactly, and only the classes with
    d | m, d not dividing j, survive.  This is the first general statement
    about EVEN m, which Passes 510-512 each recorded as untouched.

    It also corrects Pass 511's Part E reading.  That measurement lumped d = 3
    in with d = 1, 2 at (3,6) and concluded the short aggregate generically
    sits below the total.  In fact d = 1 and d = 2 always cancel exactly; the
    residual lives entirely in the d = p class, which j = 2 does not reach.
    """
    rows, ok_id, ok_zero = {}, True, True
    for p_, j in ((3, 2), (3, 3), (3, 4), (3, 5), (5, 2), (5, 3), (7, 2)):
        m = j * p_
        for seed in (7001, 7005):
            R, C, q, D, dcoef, rho = P511.setup(p_, seed)
            lhs = C.zero()
            divisors = [d for d in range(1, j + 1) if j % d == 0]
            for d in divisors:
                term, _ = P511.period_class(R, C, q, dcoef, rho, m, d)
                lhs = C.add(lhs, term)
            Sp = C.zero()
            for v in dcoef:
                dp = C.rat(1)
                for _ in range(p_):
                    dp = C.mul(dp, dcoef[v])
                Sp = C.add(Sp, dp)
            rhs = C.rat(q)
            for _ in range(j):
                rhs = C.mul(rhs, Sp)
            if lhs != rhs:
                ok_id = False
            if any(lhs) or any(rhs):
                ok_zero = False
            rows[f"p{p_}_j{j}_m{m}_s{seed}"] = {
                "divisors_of_j": divisors,
                "identity_holds": lhs == rhs,
                "both_sides_vanish": (not any(lhs)) and (not any(rhs))}
    checks["propagation_identity_exact"] = ok_id
    checks["propagation_both_sides_vanish"] = ok_zero
    checks["propagation_covers_three_primes"] = len(
        {k.split("_")[0] for k in rows}) == 3
    return {"rows": rows, "cells": len(rows),
            "theorem": (
                "THE PROPAGATION THEOREM.  For m = jp and any j >= 1, "
                "sum_{d | j} d S_d = q (sum_{v != 0} d_v^p)^j, and the right "
                "side vanishes identically because sum_v d_v^p is the m = p "
                "constant class killed by Pass 511.  Proof: for d | j a "
                "period-d representative (w_1..w_d) gives "
                "M^{m/d} = zeta^{s p j / d} rho((pj/d) w) = I, since p divides "
                "pj/d; so its value is q times the product of d_{w_i}^p, and "
                "grouping ALL j-tuples by cyclic orbit reproduces "
                "sum_{d | j} d S_d on the left and (sum_v d_v^p)^j on the "
                "right.  QED."),
            "consequence": (
                "The m = p vanishing propagates to EVERY multiple of p: at "
                "m = jp the classes whose period divides j cancel exactly, and "
                "only the classes with d | m and d not dividing j survive.  "
                "This is the first general statement about even m, which "
                "Passes 510-512 each recorded as untouched, and it corrects "
                "Pass 511's Part E reading: that measurement lumped d = 3 in "
                "with d = 1, 2 at (3,6) and concluded the short aggregate "
                "generically sits below the total, whereas d = 1 and d = 2 "
                "always cancel exactly and the residual lives entirely in the "
                "d = p class, which j = 2 does not reach.")}


# ---------------------------------------------------------------- part E

CAUSAL = re.compile(
    r"\b(because|mechanism|the reason|explains?|explanation|signature of|"
    r"driven by|arises? from|accounts? for|is due to|comes? from)\b", re.I)
HEDGED = re.compile(
    r"\b(proof|proved|proven|QED|theorem|candidate|conjectur|unverified|"
    r"not proved|unproven|not identified|we do not know|suspect|retract|"
    r"hypothes|measured, not|observation, not)\b", re.I)
QUOTED = re.compile(r"(^|\.)(sample|samples|quote|quoted|excerpt)s?(\[|$)")


def part_E_worklist(checks):
    """A worklist keyed to the file that PRODUCES each certificate."""
    producers = {}
    for src in sorted((ROOT / "analysis").glob("*.py")):
        try:
            txt = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for mo in re.finditer(r'["\']([A-Za-z0-9_./-]+\.json)["\']', txt):
            producers.setdefault(Path(mo.group(1)).name, src.name)
    items, orphan = [], 0
    for f in sorted((ROOT / "data").glob("*.json")):
        if f.name == OUT.name:
            continue
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        hits = []

        def walk(node, kp):
            if isinstance(node, str):
                if QUOTED.search(kp):
                    return
                if CAUSAL.search(node) and not HEDGED.search(node):
                    hits.append(kp)
            elif isinstance(node, dict):
                for k, v in node.items():
                    walk(v, f"{kp}.{k}" if kp else k)
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, f"{kp}[{i}]")

        walk(doc, "")
        if not hits:
            continue
        prod = producers.get(f.name)
        if prod is None:
            orphan += 1
        items.append({"certificate": f.name, "producer": prod,
                      "keys": sorted(hits)[:8], "n_claims": len(hits)})
    fixable = [i for i in items if i["producer"]]
    checks["worklist_built"] = len(items) > 0
    checks["most_flagged_certificates_have_a_named_producer"] = (
        len(fixable) > len(items) // 2)
    return {"flagged_certificates": len(items),
            "with_named_producer": len(fixable),
            "without_producer": orphan,
            "total_claims": sum(i["n_claims"] for i in items),
            "worklist": items[:60],
            "reading": (
                "Pass 512 bucketed the backlog; the fix still needs the SOURCE, "
                "since certificates are script outputs and editing the JSON "
                "would break every --check drift test.  This maps each flagged "
                "certificate to the analysis file that writes it, so a fix is "
                "a one-line edit in a named producer rather than a search.  "
                "Certificates with no located producer are listed separately: "
                "they are third-stream or legacy artefacts and cannot be fixed "
                "from this track.")}


# ---------------------------------------------------------------- main


def main_payload():
    checks = {}
    A = part_A_weight_share(checks)
    B = part_B_minimal_support(checks)
    Cc = part_C_character_order(checks)
    Dd = part_D_propagation(checks)
    E = part_E_worklist(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass513.character_order_and_weight_share.v1",
        "status": status,
        "headline": (
            "THE ODD-CLASS VANISHING THEOREM IS ABOUT THE CHARACTER ORDER, NOT "
            "ABOUT p.  Both ingredients of Pass 511's proof used p only through "
            "the order e of the generating character, which over F_q happens to "
            "equal p: (i) rho_v^k = I needs k v = 0 for every v, (ii) "
            "(u-1)^k purely imaginary needs k odd and ord(u) | k for every u in "
            "the image of psi -- and both conditions are e | k.  Over Z/9, "
            "where e = 9, the constant class is measured to vanish at m = 9 and "
            "m = 27 and NOT at m = 3, exactly where 'p | m' would have "
            "predicted vanishing.  So the theorem reads: for R a finite "
            "Frobenius ring with generating character of order e, and m = dk "
            "odd with e | k, the period-d class vanishes identically.  The same "
            "invariant governs the determinant law's scope, which holds when "
            "e = p and fails over Z/p^n where e = p^n; two statements proved "
            "and tested separately are indexed by the same number."),
        "part_A_weight_share": A,
        "part_B_minimal_support_converse": B,
        "part_C_character_order_theorem": Cc,
        "part_D_propagation_theorem": Dd,
        "part_E_flagged_worklist": E,
        "boundary": (
            "Part A is exact arithmetic on minima over 250 (p=3) and 60 (p=5) "
            "sampled sections; the identity tr = m S_m at m = p^j is a "
            "corollary of Pass 511, and the weight-share figures are a "
            "quantified LIMIT on the orbit mechanism, not an account of the "
            "remainder.  Part B is a recipe verified on six cells, NOT an "
            "induction: the converse for general d remains unproved.  Part C "
            "verifies the arithmetic criterion exactly in Z[zeta_e] for "
            "e in {3,9,5,27,25} and the full class over Z/9 at three sections; "
            "Z/25 and Z/27 full-class runs are out of reach in this "
            "implementation and are not claimed.  Part D verifies the "
            "propagation identity on 14 cells across p = 3, 5, 7 and "
            "j = 2..5; the identity and the vanishing are both exact, and the "
            "proof is general.  "
            "Part E maps certificates to producers by scanning source for "
            "quoted filenames, which is a heuristic."),
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
            raise SystemExit("Pass 513 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
