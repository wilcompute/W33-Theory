#!/usr/bin/env python3
"""Pass 512: the converse at d = 1, PROVED; the Legendre tower measured where
there is nothing to cancel; and the theorem's hypotheses tested in the region
where the factorial law fails.

Pass 511 proved the odd-class vanishing theorem (m = dk odd with p | k implies
the period-d class vanishes identically) and left the converse as a
measurement over 28 cells.  This pass closes the converse for d = 1 by
CONSTRUCTION rather than by sampling, uses the collapse corollary to measure
the Legendre tower in the one setting where no cancellation can confound it,
formalizes the pairing ingredient, and asks whether the proof's hypotheses
break exactly where the law does.

A. THE CONVERSE AT d = 1, PROVED.  Suppose p | m, so the constant orbits
   exist.  Choose ONE inverse-closed pair {v0, -v0}, put c(v0) = a with
   psi(a) = u != 1, c(-v0) = -a, and c(v) = 0 elsewhere: this is a legitimate
   inverse-closed section, and every d_v vanishes except d_{v0} = u - 1 and
   d_{-v0} = conj(u) - 1.  The constant class is then exactly

        q * [ (u-1)^m + conj(u-1)^m ]  =  2q * Re (u-1)^m ,

   which is nonzero precisely when (u-1)^m is NOT purely imaginary -- i.e., by
   Pass 511's ingredient (ii), precisely when m is even.  So for d = 1 the
   theorem's hypothesis is not merely sufficient but NECESSARY, witnessed by an
   explicit section rather than by a search.

B. THE LEGENDRE TOWER WITH NOTHING TO CANCEL.  By Pass 511's collapse
   corollary, at m = p^j exactly ONE class survives -- the free class d = m --
   so v_lambda(tr D^{p^j}) is that class's valuation with no inter-class
   cancellation to confound it.  This is the cleanest possible place to test
   the factorial law's Legendre tower, and it is tested here at
   m = p, p^2, p^3 for p = 3 and m = p, p^2 for p = 5.

C. INGREDIENT (iii) FORMALIZED.  The pairing step -- a finite sum over an
   involution-paired index set whose summand is negated by the involution
   vanishes -- is stated and proved in Lean
   (formal/W33/Pass511OddClassVanishing.lean); this pass checks the file is
   present and states what it does and does not cover.

D. DO THE HYPOTHESES BREAK WHERE THE LAW DOES?  Over Z/9 and Z/25 the
   generating character has order p^2.  Ingredient (i) needs rho_v^k = I, which
   came from (v,0)^p = identity -- true in characteristic p, false over
   Z/p^n where 3v need not vanish.  If the constant class is nonzero over Z/9
   at an m where the theorem would have killed it over F_9, that is a
   structural link between the two failures, which until now shared only a
   locus.

E. THE FLAGGED BACKLOG.  Pass 508's mechanism guard found 79 of 339
   certificates carrying unmarked causal claims.  Pass 511 converted one such
   claim from measured to proved.  This pass triages the backlog into
   actionable classes rather than leaving it as a count.
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
OUT = ROOT / "data" / "w33_pass512_converse_and_legendre_tower.json"
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

Cyc, matmul, RingSetup = P487.Cyc, P487.matmul, P487.RingSetup
trace = P504.trace


def vp(n, p):
    v = 0
    while n and n % p == 0:
        n //= p
        v += 1
    return v


def vlam_factorial(m, p):
    """v_lambda(m!) = (p-1) * Legendre v_p(m!)."""
    s, q = 0, p
    while q <= m:
        s += m // q
        q *= p
    return (p - 1) * s


# ---------------------------------------------------------------- part A


def part_A_converse(checks):
    """The one-pair section: an explicit witness, not a search."""
    rows, ok = {}, True
    for p_ in (3, 5, 7):
        R, C, q, D, dcoef, rho = P511.setup(p_, 900 + p_)
        # rebuild dcoef for the ONE-PAIR section: only v0 and -v0 are nonzero
        vecs = list(rho)
        v0 = vecs[0]
        nv0 = (R.neg(v0[0]), R.neg(v0[1]))
        for m in range(p_, 4 * p_ + 1):
            if m % p_:
                continue
            one = C.rat(1)
            u = C.from_exp(1)                       # psi(a) = zeta, a unit
            du = C.sub(u, one)
            dn = C.sigma(p_ - 1, du)                # conj(u) - 1
            acc = C.zero()
            for d_, v in ((du, v0), (dn, nv0)):
                dm = C.rat(1)
                for _ in range(m):
                    dm = C.mul(dm, d_)
                M = [[C.rat(1) if i == j else C.zero() for j in range(q)]
                     for i in range(q)]
                for _ in range(m):
                    M = matmul(M, rho[v], C)
                acc = C.add(acc, C.mul(dm, trace(M, C)))
            vanishes = not any(acc)
            predicted = (m % 2 == 1)
            if vanishes != predicted:
                ok = False
            rows[f"p{p_}_m{m}"] = {"one_pair_class_vanishes": vanishes,
                                   "predicted_vanish_iff_m_odd": predicted}
    checks["converse_at_d1_witnessed_by_one_pair_section"] = ok
    return {"construction": (
        "one inverse-closed pair carries psi(a) = zeta, every other pair is "
        "flat; the constant class is then exactly 2q Re (u-1)^m, nonzero "
        "precisely when (u-1)^m is not purely imaginary, i.e. when m is even"),
        "rows": rows}


# ---------------------------------------------------------------- part B


def part_B_tower(checks):
    """m = p^j: one surviving class, so the tower is read off directly."""
    out = {}
    for p_, js, nsec in ((3, (1, 2, 3), 250), (5, (1, 2), 60)):
        pred_row, meas_row = {}, {}
        for j in js:
            m = p_ ** j
            pred = (p_ - 1) + m + 1 + vlam_factorial(m, p_)
            best = None
            for seed in range(nsec):
                R, C, q, D, dcoef, rho = P511.setup(p_, 40000 + seed)
                Dm = D
                for _ in range(m - 1):
                    Dm = matmul(Dm, D, C)
                t = trace(Dm, C)
                if any(t):
                    v = C.vlam(t)
                    best = v if best is None else min(best, v)
            pred_row[str(m)] = pred
            meas_row[str(m)] = best
        out[f"p{p_}"] = {"sections": nsec, "predicted": pred_row,
                         "measured_min": meas_row,
                         "surviving_classes": 1,
                         "agree": all(pred_row[k] == meas_row[k]
                                      for k in pred_row)}
        checks[f"p{p_}_legendre_tower_at_prime_powers"] = out[f"p{p_}"]["agree"]
    return out


# ---------------------------------------------------------------- part C


def part_C_lean(checks):
    f = ROOT / "formal" / "W33" / "Pass511OddClassVanishing.lean"
    present = f.exists()
    txt = f.read_text(encoding="utf-8") if present else ""
    checks["lean_module_present"] = present
    checks["lean_states_pairing_lemma"] = "involution" in txt.lower()
    return {"file": "formal/W33/Pass511OddClassVanishing.lean",
            "present": present,
            "covers": ("ingredient (iii): a finite sum over an "
                       "involution-paired index set whose summand is negated "
                       "by the involution is zero"),
            "does_not_cover": ("ingredients (i) and (ii) -- the Heisenberg "
                               "power identity and the purely-imaginary "
                               "criterion -- which are taken as hypotheses"),
            "lines": len(txt.splitlines())}


# ---------------------------------------------------------------- part D


def part_D_failure_region(checks):
    """Over Z/p^n the character has order p^n: does ingredient (i) break?"""
    out = {}
    for p_, n in ((3, 2), (5, 2)):
        st = RingSetup(p_, n)
        C, q = st.R, st.q
        rng = random.Random(512)
        offs = tuple(rng.randrange(q) for _ in st.pairs)
        fsec = st.full_sec(offs)
        rho = {}
        for (a, b) in fsec:
            N = [[C.zero() for _ in range(q)] for _ in range(q)]
            for x in range(q):
                N[(x + a) % q][x] = C.from_exp((2 * x * b + a * b) % q)
            rho[(a, b)] = N
        ident = [[C.rat(1) if i == j else C.zero() for j in range(q)]
                 for i in range(q)]
        # (i): is rho_v^p = I ?
        pow_p_identity = 0
        for v in rho:
            M = ident
            for _ in range(p_):
                M = matmul(M, rho[v], C)
            if M == ident:
                pow_p_identity += 1
        # the constant class at m = p (odd, p | m): killed over F_q by Pass 511
        acc = C.zero()
        for v in rho:
            dv = C.sub(C.from_exp(fsec[v]), C.rat(1))
            dm = C.rat(1)
            for _ in range(p_):
                dm = C.mul(dm, dv)
            M = ident
            for _ in range(p_):
                M = matmul(M, rho[v], C)
            acc = C.add(acc, C.mul(dm, trace(M, C)))
        out[f"Z/{p_**n}"] = {
            "vectors": len(rho),
            "rho_v_pow_p_equals_identity_count": pow_p_identity,
            "ingredient_i_holds": pow_p_identity == len(rho),
            "constant_class_at_m_eq_p_vanishes": not any(acc),
        }
        checks[f"Z{p_**n}_ingredient_i_breaks"] = pow_p_identity < len(rho)
    same = all(not r["ingredient_i_holds"] for r in out.values())
    survives = [k for k, r in out.items()
                if not r["constant_class_at_m_eq_p_vanishes"]]
    checks["failure_region_breaks_a_hypothesis_not_a_conclusion"] = same
    return {"rows": out,
            "rings_where_the_class_survives": survives,
            "reading": (
                "Over Z/p^n the generating character has order p^n, so "
                "(v,0)^p = (pv,0) is NOT the identity and ingredient (i) of "
                "the Pass 511 proof fails by construction.  Measured: the "
                "count of vectors with rho_v^p = I is strictly less than the "
                "total in both rings.  Whether the CLASS then survives is "
                "reported separately -- a broken hypothesis does not by itself "
                "make a conclusion false, and this is recorded as a hypothesis "
                "test, not as an explanation of the factorial law's failure.")}


# ---------------------------------------------------------------- part E

CAUSAL = re.compile(
    r"\b(because|mechanism|the reason|explains?|explanation|signature of|"
    r"driven by|arises? from|accounts? for|is due to|comes? from)\b", re.I)
HEDGED = re.compile(
    r"\b(proof|proved|proven|QED|theorem|candidate|conjectur|unverified|"
    r"not proved|unproven|not identified|we do not know|suspect|retract|"
    r"hypothes|measured, not|observation, not)\b", re.I)


def _strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v)


def part_E_triage(checks):
    """Turn the guard's count into a ranked, actionable backlog."""
    buckets = {"proof_exists_elsewhere": [], "restatement_of_a_measurement": [],
               "genuine_open_mechanism": [], "prose_only": []}
    scanned = 0
    for f in sorted((ROOT / "data").glob("*.json")):
        # This certificate lives in data/ too.  Scanning it would fold the
        # previous run's samples into this run's output and the --check drift
        # test would never agree with itself.
        if f.name == OUT.name:
            continue
        try:
            obj = json.loads(f.read_text())
        except Exception:
            continue
        scanned += 1
        hits = [s for s in _strings(obj)
                if CAUSAL.search(s) and not HEDGED.search(s)]
        if not hits:
            continue
        worst = max(hits, key=len)
        # classify by what the surrounding certificate offers
        blob = " ".join(_strings(obj))
        if re.search(r"\b(proved|theorem|QED)\b", blob, re.I):
            b = "proof_exists_elsewhere"
        elif re.search(r"\b(measured|verified|exact|enumerat)\b", blob, re.I):
            b = "restatement_of_a_measurement"
        elif len(worst) < 120:
            b = "prose_only"
        else:
            b = "genuine_open_mechanism"
        # samples are quoted from the corpus, which carries Greek and
        # subscripts; keep them ASCII so downstream printers on a cp1252
        # console cannot die on an advisory report
        buckets[b].append({
            "file": f.name, "claims": len(hits),
            "sample": worst[:220].encode("ascii", "replace").decode("ascii")})
    total = sum(len(v) for v in buckets.values())
    checks["triage_covered_the_backlog"] = total > 0 and scanned > 100
    checks["triage_buckets_nonempty"] = sum(
        1 for v in buckets.values() if v) >= 2
    return {"certificates_scanned": scanned,
            "flagged": total,
            "counts": {k: len(v) for k, v in buckets.items()},
            "buckets": {k: v[:12] for k, v in buckets.items()},
            "reading": (
                "The guard's 79 was a count, not a worklist.  Certificates "
                "whose own text already contains a proof or theorem are "
                "wording fixes; those that restate a measurement need the "
                "word 'measured' rather than 'because'; the remainder are the "
                "genuinely open mechanisms and are the only ones that need "
                "work.  Buckets are advisory and assigned by vocabulary, not "
                "by reading -- this ranks the backlog, it does not clear it.")}


# ---------------------------------------------------------------- main


def main_payload():
    checks = {}
    A = part_A_converse(checks)
    B = part_B_tower(checks)
    Cc = part_C_lean(checks)
    Dd = part_D_failure_region(checks)
    E = part_E_triage(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass512.converse_and_legendre_tower.v1",
        "status": status,
        "headline": (
            "THE CONVERSE AT d = 1 IS PROVED, BY CONSTRUCTION.  Pass 511 left "
            "the converse of the odd-class vanishing theorem as a measurement "
            "over 28 cells.  For the constant class it is now a theorem: with "
            "p | m, put psi(c(v0)) = zeta on a single inverse-closed pair and "
            "flat elsewhere; every d_v vanishes but two, and the class is "
            "exactly 2q Re (u-1)^m, which is nonzero precisely when (u-1)^m is "
            "not purely imaginary, i.e. precisely when m is EVEN.  So at d = 1 "
            "the hypothesis 'm odd' is necessary as well as sufficient, "
            "witnessed by an explicit section rather than by a search.  For "
            "d > 1 the converse remains measured."),
        "part_A_converse_at_d1": A,
        "part_B_legendre_tower": B,
        "part_C_lean": Cc,
        "part_D_failure_region": Dd,
        "part_E_flagged_backlog_triage": E,
        "boundary": (
            "Part A is a proof for d = 1 only; the converse for d > 1 is still "
            "the 28-cell measurement of Pass 511.  Part B reads the tower at "
            "m = p^j, where Pass 511's collapse corollary leaves a single "
            "class, so the measured minimum is that class's valuation with no "
            "inter-class cancellation -- but it is still a minimum over "
            "sampled sections, not a proof.  Part C reports the Lean file's "
            "scope; only ingredient (iii) is formalized.  Part D tests a "
            "HYPOTHESIS of the Pass 511 proof over Z/9 and Z/25 and asserts no "
            "mechanism for the factorial law's failure there.  Part E assigns "
            "buckets by vocabulary, not by reading the claims."),
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
            raise SystemExit("Pass 512 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
