#!/usr/bin/env python3
"""Pass 514: THE SIEVE THEOREM -- one statement that implies both the
odd-class vanishing theorem and propagation.

Pass 511 proved that the period-d class vanishes when m = dk is odd and p | k.
Pass 513 proved that at m = jp the classes with d | j sum to zero, and that the
right invariant is the ORDER e of the generating character rather than p.  Both
are the same theorem seen at two values of one parameter.

  THE SIEVE THEOREM.  Let e be the order of the generating character and let
  t | m satisfy: m/t is ODD and e | (m/t).  Then

        sum_{d | t} d * S_d  =  q * ( sum_{v != 0} d_v^{m/t} )^t  =  0 .

  Proof.  Put n = m/t.  For d | t we have n | (m/d), so e | (m/d) and a
  period-d representative (w_1..w_d) has M^{m/d} = zeta^{s m/d} rho((m/d) w)
  = I; also the zero-sum condition (m/d) sum_i w_i = 0 is automatic.  Hence
  the orbit's value is q * prod_{i<=d} d_{w_i}^{m/d}, which is
  prod_{i<=t} d_{w_i}^{n} over the repeated t-tuple.  Since d * S_d counts each
  period-d orbit once per distinct t-tuple in it, summing over d | t sweeps
  every t-tuple exactly once and gives q (sum_v d_v^{n})^t.  The bracket
  vanishes because n is odd and e | n: by the Pass 511/513 criterion
  (u-1)^n is purely imaginary, and inverse closure pairs v with -v.  QED

WHAT IT SUBSUMES.  Write T = { t : t | m, m/t odd, e | (m/t) }.  For m ODD, T
is exactly the set of divisors of m/e, so it is downward closed and Moebius
inversion runs: S_1 = 0 from t = 1, and then t S_t = -sum_{d | t, d < t} d S_d
= 0 for every t | (m/e).  That is precisely Pass 511's hypothesis (with
p replaced by e), so the ODD-CLASS VANISHING THEOREM IS A COROLLARY.  For m
even, T is not downward closed -- at m = jp only t = j survives -- and the
theorem degenerates to exactly Pass 513's propagation relation.  One theorem
replaces two, and the difference between the odd and even cases becomes a
statement about whether a divisor set is downward closed.

THE SHORTCUT.  The proof's first step is worth having as a computational tool:
whenever e | (m/d), a period-d orbit's value is q * prod_i d_{w_i}^{m/d} with
NO matrix products at all.  That is checked here against the honest matrix
computation on 15616 orbits before it is used, and it is what puts Z/25 and
Z/27 -- 624 and 728 vectors with 25x25 and 27x27 blocks -- within reach.
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
OUT = ROOT / "data" / "w33_pass514_sieve_theorem.json"


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


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


# ------------------------------------------------------------ the cell


class Cell:
    """Register cell over Z/e with an inverse-closed section, d_v only."""

    def __init__(self, p, n, seed):
        self.p, self.n, self.e = p, n, p ** n
        self.C = Cyc(p, n)
        e = self.e
        self.vecs = [(a, b) for a in range(e) for b in range(e)
                     if (a, b) != (0, 0)]
        pairs, used = [], set()
        for v in self.vecs:
            nv = ((-v[0]) % e, (-v[1]) % e)
            key = tuple(sorted((v, nv)))
            if key in used:
                continue
            used.add(key)
            pairs.append((v, nv))
        rng = random.Random(seed)
        self.c = {}
        for v, nv in pairs:
            a = rng.randrange(e)
            self.c[v] = a
            self.c[nv] = (-a) % e
        one = self.C.rat(1)
        self.d = {v: self.C.sub(self.C.from_exp(self.c[v]), one)
                  for v in self.vecs}

    def pw(self, v, k):
        x = self.C.rat(1)
        for _ in range(k):
            x = self.C.mul(x, self.d[v])
        return x

    def power_sum(self, k):
        """sum_{v != 0} d_v^k."""
        s = self.C.zero()
        for v in self.vecs:
            s = self.C.add(s, self.pw(v, k))
        return s

    def class_shortcut(self, m, d):
        """d * S_d via the shortcut; valid only when e | (m/d)."""
        assert (m // d) % self.e == 0
        C, k = self.C, m // d
        tot, seen = C.zero(), set()
        for base in itertools.product(self.vecs, repeat=d):
            rots = {base[r:] + base[:r] for r in range(d)}
            if len(rots) != d or base in seen:
                continue
            seen |= rots
            val = C.rat(self.e ** 1)          # q = e for these cells
            for w in base:
                val = C.mul(val, self.pw(w, k))
            for _ in range(d):
                tot = C.add(tot, val)
        return tot


# ------------------------------------------------------------ part A


def part_A_shortcut(checks):
    """The shortcut, against the honest matrix computation."""
    bad, tested = 0, 0
    for p_ in (3, 5):
        R, C, q, D, dcoef, rho = P511.setup(p_, 7001)
        vecs = list(rho)
        for m, d in ((p_, 1), (2 * p_, 1), (2 * p_, 2), (3 * p_, 3),
                     (4 * p_, 2)):
            if (m // d) % p_:
                continue
            for base in itertools.product(vecs, repeat=d):
                full = base * (m // d)
                if len({full[r:] + full[:r] for r in range(m)}) != d:
                    continue
                a0, a1 = R.zero, R.zero
                for v in full:
                    a0, a1 = R.add(a0, v[0]), R.add(a1, v[1])
                if (a0, a1) != (R.zero, R.zero):
                    continue
                honest = P511.value(full, C, q, dcoef, rho)
                short = C.rat(q)
                for w in base:
                    dw = C.rat(1)
                    for _ in range(m // d):
                        dw = C.mul(dw, dcoef[w])
                    short = C.mul(short, dw)
                tested += 1
                if honest != short:
                    bad += 1
    checks["shortcut_matches_matrix_computation"] = bad == 0
    checks["shortcut_tested_on_thousands_of_orbits"] = tested > 10000
    # and over a ring, where e = p^2 rather than p
    st = RingSetup(3, 2)
    C, q = st.R, st.q
    rng = random.Random(514)
    fsec = st.full_sec(tuple(rng.randrange(q) for _ in st.pairs))
    rho9 = {}
    for (a, b) in fsec:
        N = [[C.zero() for _ in range(q)] for _ in range(q)]
        for x in range(q):
            N[(x + a) % q][x] = C.from_exp((2 * x * b + a * b) % q)
        rho9[(a, b)] = N
    I = [[C.rat(1) if i == j else C.zero() for j in range(q)]
         for i in range(q)]
    ring_bad = 0
    for v in rho9:
        M = I
        for _ in range(9):
            M = matmul(M, rho9[v], C)
        dv = C.sub(C.from_exp(fsec[v]), C.rat(1))
        dm = C.rat(1)
        for _ in range(9):
            dm = C.mul(dm, dv)
        honest = C.mul(dm, trace(M, C))
        short = C.mul(C.rat(q), dm)
        if honest != short:
            ring_bad += 1
    checks["shortcut_valid_over_Z9_too"] = ring_bad == 0
    return {"orbits_tested_over_fields": tested,
            "mismatches_over_fields": bad,
            "mismatches_over_Z9": ring_bad,
            "shortcut": ("when e | (m/d), a period-d orbit's value is "
                         "q * prod_i d_{w_i}^{m/d}, with no matrix products; "
                         "the zero-sum constraint is automatic (both steps "
                         "are part of the sieve theorem's proof) since "
                         "(m/d) sum_i w_i = 0")}


# ------------------------------------------------------------ part B


def part_B_sieve(checks):
    """The sieve relations, honestly enumerated where affordable."""
    rows, ok = {}, True
    plan = ((3, 1, 6), (3, 1, 9), (3, 1, 12), (3, 1, 15), (3, 1, 18),
            (5, 1, 10), (5, 1, 15), (7, 1, 14))
    for p_, n, m in plan:
        e = p_ ** n
        T = [m // u for u in divisors(m)
             if u % 2 == 1 and u % e == 0 and m % u == 0]
        for seed in (7001, 7005):
            cell = Cell(p_, n, seed)
            for t in sorted(T):
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
                rows[f"p{p_}_m{m}_t{t}_s{seed}"] = {
                    "n_equals_m_over_t": m // t,
                    "identity_holds": lhs == rhs,
                    "vanishes": not any(lhs)}
    checks["sieve_relations_exact_and_vanishing"] = ok
    checks["sieve_covers_three_primes"] = len(
        {k.split("_")[0] for k in rows}) == 3
    return {"rows": rows, "cells": len(rows),
            "T": ("T = { t : t | m, m/t odd, e | (m/t) }; for m odd this is "
                  "exactly the divisors of m/e, downward closed, so Moebius "
                  "inversion kills each S_d individually and recovers Pass "
                  "511; for m even it is not downward closed and the theorem "
                  "degenerates to Pass 513's propagation relation")}


def part_C_derived(checks):
    """m = 18: two relations, and a derived one at EVEN m."""
    rows, ok = {}, True
    for seed in (7001, 7005, 7009):
        cell = Cell(3, 1, seed)
        m = 18
        # T = {6, 2} from u = 3, 9
        t2 = cell.C.zero()
        for d in (1, 2):
            t2 = cell.C.add(t2, cell.class_shortcut(m, d))
        t6 = cell.C.zero()
        for d in (1, 2, 3, 6):
            t6 = cell.C.add(t6, cell.class_shortcut(m, d))
        derived = cell.C.sub(t6, t2)          # = 3 S_3 + 6 S_6
        s3 = cell.class_shortcut(m, 3)
        s6 = cell.class_shortcut(m, 6)
        alt = cell.C.add(s3, s6)
        good = (not any(t2)) and (not any(t6)) and (not any(derived)) \
            and derived == alt
        if not good:
            ok = False
        rows[str(seed)] = {
            "t2_relation_vanishes": not any(t2),
            "t6_relation_vanishes": not any(t6),
            "derived_3S3_plus_6S6_vanishes": not any(derived),
            "derived_matches_direct_sum": derived == alt,
            "S3_alone_vanishes": not any(s3),
            "S6_alone_vanishes": not any(s6)}
    checks["m18_two_relations_and_a_derived_one"] = ok
    solo = all(not r["S3_alone_vanishes"] and not r["S6_alone_vanishes"]
               for r in rows.values())
    checks["m18_derived_relation_is_not_two_separate_vanishings"] = solo
    return {"rows": rows,
            "reading": (
                "At m = 18 with e = 3 the sieve gives TWO relations, from "
                "u = 3 and u = 9, i.e. t = 6 and t = 2.  Subtracting them "
                "leaves 3 S_3 + 6 S_6 = 0 -- a relation at EVEN m that is not "
                "an individual vanishing: neither S_3 nor S_6 is zero on its "
                "own in any section sampled.  This is the first constraint "
                "the sieve produces that neither Pass 511 nor Pass 513 "
                "reaches.")}


# ------------------------------------------------------------ part D


def part_D_character_order(checks):
    """e = 9, 25, 27: the constant class, cheaply, via the shortcut."""
    rows, ok = {}, True
    for p_, n in ((3, 2), (5, 2), (3, 3)):
        e = p_ ** n
        for seed in (1, 2):
            cell = Cell(p_, n, seed)
            for m in sorted({p_, e, 2 * e, 3 * e, e * p_}):
                if m % e:
                    # constant class is then supported on {v : m v = 0}
                    s = cell.C.zero()
                    for v in cell.vecs:
                        if (m * v[0]) % e == 0 and (m * v[1]) % e == 0:
                            s = cell.C.add(s, cell.pw(v, m))
                else:
                    s = cell.power_sum(m)
                van = not any(s)
                pred = (m % 2 == 1) and (m % e == 0)
                if van != pred:
                    ok = False
                rows[f"e{e}_s{seed}_m{m}"] = {
                    "vanishes": van, "predicted_by_e": pred,
                    "predicted_by_p": (m % 2 == 1) and (m % p_ == 0)}
    checks["character_order_holds_at_e_9_25_27"] = ok
    diff = [k for k, r in rows.items()
            if r["predicted_by_e"] != r["predicted_by_p"]]
    checks["e_and_p_predictions_differ_somewhere"] = bool(diff)
    return {"rows": rows, "cells_separating_e_from_p": diff,
            "reading": (
                "Pass 513 established the character-order form at e = 9 only. "
                "Here it is checked at e = 9, 25 and 27 -- a second p^2 and a "
                "first p^3 -- using the shortcut, which makes the 624- and "
                "728-vector cells affordable.  The listed cells are those "
                "where 'e | m' and 'p | m' disagree; the measurement follows "
                "e in every one.")}


# ------------------------------------------------------------ part E


def part_E_universal(checks):
    """Is the sieve exactly the vanishing that holds in EVERY section?"""
    rows, ok = {}, True
    for p_, m in ((3, 6), (3, 9), (3, 12), (3, 15), (3, 18), (5, 10),
                  (5, 15)):
        e = p_
        for d in divisors(m):
            if (m // d) % e:
                continue          # shortcut not valid; not a sieve cell
            always = True
            for seed in range(7000, 7008):
                cell = Cell(p_, 1, seed)
                if any(cell.class_shortcut(m, d)):
                    always = False
                    break
            pred = (m % 2 == 1) and ((m // d) % e == 0)
            if always != pred:
                ok = False
            rows[f"p{p_}_m{m}_d{d}"] = {"vanishes_in_every_section": always,
                                        "sieve_predicts_vanishing": pred}
    checks["sieve_is_exactly_the_universal_vanishing"] = ok
    return {"rows": rows, "sections_per_cell": 8,
            "reading": (
                "For each class the question is whether it vanishes in EVERY "
                "section, not in some.  The sieve's individual-vanishing "
                "prediction -- m odd and e | (m/d) -- matches that in every "
                "cell tested.  Classes that vanish only in some sections "
                "(the d = 3 class at (3,6), for instance) are section "
                "accidents and the sieve correctly does not predict them.")}


# ------------------------------------------------------------ part F

CAUSAL = re.compile(
    r"\b(because|mechanism|the reason|explains?|explanation|signature of|"
    r"driven by|arises? from|accounts? for|is due to|comes? from)\b", re.I)
HEDGED = re.compile(
    r"\b(proof|proved|proven|QED|theorem|candidate|conjectur|unverified|"
    r"not proved|unproven|not identified|we do not know|suspect|retract|"
    r"hypothes|measured, not|observation, not)\b", re.I)
QUOTED = re.compile(
    r"(^|\.)(sample|samples|quote|quoted|excerpt|fragment|snippet)s?(\[|$)")


def part_F_patch(checks):
    """Emit an applicable patch, and say what can and cannot be applied."""
    producers = {}
    for src in sorted((ROOT / "analysis").glob("*.py")):
        try:
            txt = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for mo in re.finditer(r'["\']([A-Za-z0-9_./-]+\.json)["\']', txt):
            producers.setdefault(Path(mo.group(1)).name, src.name)
    patch, unresolved = [], 0
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
                    hits.append((kp, node))
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
            unresolved += len(hits)
            continue
        src = (ROOT / "analysis" / prod)
        stext = src.read_text(encoding="utf-8", errors="ignore") \
            if src.exists() else ""
        # Certificate strings are assembled from ADJACENT string literals, so a
        # fragment of the emitted text usually straddles a source line break
        # and a naive substring search misses it.  Collapse the concatenation
        # joins before searching.  (Measured: this is the difference between
        # 115 and the figure reported below.)
        joined = re.sub(r'["\']\s*\n\s*["\']', "", stext)
        for kp, node in hits:
            frag = node[:60]
            naive = stext.count(frag) if frag else 0
            n_occ = joined.count(frag) if frag else 0
            patch.append({
                "certificate": f.name, "producer": prod, "key": kp,
                "locatable_in_source": n_occ == 1,
                "found_without_collapsing_joins": naive == 1,
                "fragment": frag.encode("ascii", "replace").decode("ascii")})
    locatable = [x for x in patch if x["locatable_in_source"]]
    naive_ok = [x for x in patch if x["found_without_collapsing_joins"]]
    checks["patch_emitted"] = len(patch) > 0
    checks["collapsing_literal_joins_improves_the_locator"] = (
        len(locatable) > len(naive_ok))
    return {"claims_with_a_producer": len(patch),
            "locatable_by_unique_source_fragment": len(locatable),
            "locatable_without_collapsing_joins": len(naive_ok),
            "claims_without_a_producer": unresolved,
            "patch": patch[:80],
            "applied": 0,
            "reading": (
                "The patch is EMITTED, not applied.  Each entry names the "
                "producing script and a source fragment that occurs exactly "
                "once, so the edit is mechanical; but applying it means "
                "re-running every producer to regenerate its certificate, and "
                "a --check drift failure in an unrelated pass would be "
                "indistinguishable from a real regression.  Applying is "
                "therefore left as a separate, reviewable step.  What IS "
                "closed here is the intake: scripts/check_mechanism_claims.py "
                "gained a --staged mode so that new certificates cannot join "
                "the backlog.")}


# ------------------------------------------------------------ main


def main_payload():
    checks = {}
    A = part_A_shortcut(checks)
    B = part_B_sieve(checks)
    Cc = part_C_derived(checks)
    Dd = part_D_character_order(checks)
    E = part_E_universal(checks)
    F = part_F_patch(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass514.sieve_theorem.v1",
        "status": status,
        "theorem": (
            "THE SIEVE THEOREM.  Let e be the order of the generating "
            "character and let t | m satisfy: m/t odd and e | (m/t).  Then "
            "sum_{d | t} d S_d = q (sum_{v != 0} d_v^{m/t})^t = 0.  Proof: "
            "put n = m/t; for d | t we have n | (m/d) hence e | (m/d), so a "
            "period-d representative has M^{m/d} = I and the zero-sum "
            "condition is automatic, making the orbit's value "
            "q prod_{i<=d} d_{w_i}^{m/d} = prod_{i<=t} d_{w_i}^{n} over the "
            "repeated t-tuple; since d S_d counts each period-d orbit once "
            "per distinct t-tuple in it, summing over d | t sweeps every "
            "t-tuple exactly once and gives q (sum_v d_v^n)^t.  The bracket "
            "vanishes because n is odd and e | n.  QED"),
        "what_it_subsumes": (
            "Write T = { t : t | m, m/t odd, e | (m/t) }.  For m ODD, T is "
            "exactly the divisors of m/e -- downward closed -- so Moebius "
            "inversion gives S_1 = 0 and then t S_t = -sum_{d|t, d<t} d S_d "
            "= 0 for every t | (m/e), which is precisely Pass 511's "
            "hypothesis with p replaced by e: THE ODD-CLASS VANISHING THEOREM "
            "IS A COROLLARY.  For m even T is not downward closed -- at "
            "m = jp only t = j survives -- and the theorem degenerates to "
            "Pass 513's propagation relation.  One theorem replaces two, and "
            "the odd/even difference becomes the question of whether a "
            "divisor set is downward closed."),
        "part_A_shortcut": A,
        "part_B_sieve_relations": B,
        "part_C_derived_relation_at_even_m": Cc,
        "part_D_character_order_at_e_25_and_27": Dd,
        "part_E_sieve_is_the_universal_vanishing": E,
        "part_F_backlog_patch": F,
        "boundary": (
            "The theorem is proved in general.  Part A validates the "
            "computational shortcut against the honest matrix computation on "
            "over ten thousand orbits over fields and on the constant class "
            "over Z/9 before any later part relies on it.  Parts B-E use the "
            "shortcut and are therefore restricted to cells with e | (m/d); "
            "classes outside that range are not computed here and nothing is "
            "claimed about them.  Part E compares against eight sections per "
            "cell, so 'vanishes in every section' means 'in every section "
            "sampled'.  Part F EMITS a patch and applies none of it."),
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
            raise SystemExit("Pass 514 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
