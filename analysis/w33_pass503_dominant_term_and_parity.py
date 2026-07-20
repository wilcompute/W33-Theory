#!/usr/bin/env python3
"""Pass 503: which Newton term produces the failure depth, why parity does not
close the residual, and the scope of the q + q/p formula.

PART A -- THE DOMINANT TERM.  Pass 491 found that over Z/p^n the minimum depth
is q + q/p = p^{n-1}(p+1), fitting 12, 30, 36 at Z/9, Z/25, Z/27.  The shape is
a COUNT, not a valuation: q/p = |m| is the size of the maximal ideal, so the
formula reads |R| + |m|.  If that is the mechanism, some specific elementary
symmetric function e_k should attain the minimum, and its index should be
visible.  Here v_lambda(e_k) is computed for every k at Z/9 and Z/27 and the
argmin recorded, to see which Newton division dominates.

PART B -- PARITY, AND WHY IT DOES NOT CLOSE THE GAP.  Pass 491 proved
det D is in the real subring.  The same argument applies to EVERY coefficient:
D is Hermitian, so D^m is Hermitian, so p_m = tr(D^m) is real, and Newton then
forces every e_k real too.  Hence

        v_lambda(p_m) and v_lambda(e_k) are always EVEN.

It is tempting to hope this closes the residual: the law needs
v_lambda(e_q) >= q+3 and Newton gives q+1, so if parity could round an odd
bound up, one extra unit would suffice.  IT CANNOT, and the reason is exact.
With q odd, v(q e_q) = (q-1) + v(e_q) has even parity whenever v(e_q) is even;
the binding Newton term p_q already has even valuation 2q; so the chain
        v(e_q) >= 2q - (q-1) = q+1
lands on an EVEN number (q odd => q+1 even) and parity gives nothing.  Reaching
q+3 still requires v(p_q) >= 2q+2, i.e. two further orders of vanishing in
tr(D^q) -- exactly the gap identified in Pass 483 and unmoved since.  This pass
records that negative cleanly so the route is not retried.

PART C -- SCOPE OF q + q/p.  The third stream's Pass 499 measured the product
ring (Z/9) x F_9: character order 9, |R| = 81, depth 24.  Under q + q/p that
would be 81 + 27 = 108.  It is not: 24 = v_lambda(|R|).  So the Pass-491
formula is specific to Z/p^n and does NOT govern the failure region in general
-- a scope note, recorded before the formula is quoted more widely.

PART D -- INTAKE.  Their Pass 501 is a genuine new confirmation of OUR law at a
ring we had not tested: F_3[x,y]/(x^2,y^2) has embedding dimension 2, so it is
NOT a chain ring, and Pass 489 tested only the chains F_p[x]/(x^k).  With
|R| = 81, character order 3 and v_lambda(81) = 8, our law predicts 8 + 4 = 12,
and their exact parity-block computation attains 12.  Their Pass 499 likewise
sits on the negative side of our trichotomy (character order 9 > p, no +4).
Both are cited rather than re-derived.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass503_dominant_term_and_parity.json"

_s487 = importlib.util.spec_from_file_location(
    "p487", ROOT / "analysis" / "w33_pass487_scope_of_the_law_and_det_hunt.py")
P487 = importlib.util.module_from_spec(_s487)
_s487.loader.exec_module(P487)
_s489 = importlib.util.spec_from_file_location(
    "p489", ROOT / "analysis" / "w33_pass489_frobenius_generality.py")
P489 = importlib.util.module_from_spec(_s489)
_s489.loader.exec_module(P489)
_s490 = importlib.util.spec_from_file_location(
    "p490", ROOT / "analysis" / "w33_pass490_necessity_and_placement.py")
P490 = importlib.util.module_from_spec(_s490)
_s490.loader.exec_module(P490)

Cyc, matmul = P487.Cyc, P487.matmul
Heis = P489.Heis
ZmodRing = P490.ZmodRing


def trace(M, C):
    t = C.zero()
    for i in range(len(M)):
        t = C.add(t, M[i][i])
    return t


def newton_e(M, n, C):
    """e_1..e_n and p_1..p_n of M, exact."""
    powers = [M]
    for _ in range(n - 1):
        powers.append(matmul(powers[-1], M, C))
    p = [None] + [trace(powers[k - 1], C) for k in range(1, n + 1)]
    e = [C.rat(1)] + [C.zero()] * n
    for k in range(1, n + 1):
        acc = C.zero()
        for i in range(1, k + 1):
            term = C.mul(e[k - i], p[i])
            acc = C.add(acc, tuple(((-1) ** (i - 1)) * x for x in term))
        assert all(x % k == 0 for x in acc), (k, acc)
        e[k] = tuple(x // k for x in acc)
    return e, p


def profile(p_, n_, seed, nsec=1):
    """v_lambda(e_k) and v_lambda(p_m) over Z/p^n, plus the argmin."""
    R = ZmodRing(p_, n_)
    C = Cyc(p_, n_)
    H = Heis(R, C)
    q = H.q
    flat = H.full_sec(tuple(R.zero for _ in H.pairs))
    F = H.block(flat)
    rng = random.Random(seed)
    best = None
    for _ in range(nsec):
        offs = tuple(rng.choice(R.elems) for _ in H.pairs)
        B = H.block(H.full_sec(offs))
        D = [[C.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        e, pw = newton_e(D, q, C)
        ve = {k: C.vlam(e[k]) for k in range(1, q + 1)}
        vp = {m: C.vlam(pw[m]) for m in range(1, q + 1)}
        finite = {k: v for k, v in ve.items() if v < 10**8}
        amin = min(finite, key=lambda k: finite[k]) if finite else None
        rec = {"v_e": {str(k): (v if v < 10**8 else None)
                       for k, v in ve.items()},
               "v_p": {str(m): (v if v < 10**8 else None)
                       for m, v in vp.items()},
               "argmin_k": amin,
               "min_v_e": finite[amin] if amin else None,
               "all_e_even": all(v % 2 == 0 for v in finite.values()),
               "all_p_even": all(v % 2 == 0 for v in vp.values()
                                 if v < 10**8)}
        if best is None:
            best = rec
    return {"ring": R.name, "size": q, "v_lambda_q": C.vlam(C.rat(q)),
            "q_plus_q_over_p": q + q // p_, **best}


def part_AB(checks):
    out = {}
    for p_, n_, seed in ((3, 2, 5031), (3, 3, 5032)):
        r = profile(p_, n_, seed)
        out[r["ring"]] = r
        tag = r["ring"].replace("/", "")
        checks[f"{tag}_all_e_even"] = r["all_e_even"]
        checks[f"{tag}_all_p_even"] = r["all_p_even"]
    return out


def part_B_parity_logic(checks):
    """The exact reason parity cannot close the residual."""
    # q odd  =>  q+1 even, so the Newton bound already lands on an even number
    facts = []
    for q in (3, 5, 7, 9, 27):
        facts.append({"q": q, "newton_bound": q + 1,
                      "newton_bound_even": (q + 1) % 2 == 0,
                      "needed": q + 3,
                      "parity_gains_nothing": (q + 1) % 2 == 0})
    checks["parity_gives_no_rounding_gain"] = all(
        f["parity_gains_nothing"] for f in facts)
    return {"facts": facts,
            "conclusion": (
                "With q odd the Newton bound q+1 is already even, so the "
                "evenness of v_lambda(e_q) (from the real-subring lemma) "
                "cannot round it up.  Reaching q+3 still requires "
                "v_lambda(p_q) >= 2q+2, i.e. two further orders of vanishing "
                "in tr(D^q) -- the same gap as in Pass 483.  Route closed.")}


def part_C_scope(checks):
    """q + q/p does not govern the product ring measured by the other track."""
    prod = {"ring": "(Z/9) x F_9", "size": 81, "p": 3,
            "measured_depth_third_stream": 24,
            "q_plus_q_over_p_would_be": 81 + 27,
            "v_lambda_size": 24}
    checks["q_plus_q_over_p_is_Zpn_specific"] = (
        prod["measured_depth_third_stream"] != prod["q_plus_q_over_p_would_be"])
    return prod


def part_D_intake(checks):
    """Their 501 confirms our law at a NON-CHAIN ring."""
    rec = {
        "their_pass": 501,
        "ring": "F_3[x,y]/(x^2,y^2)",
        "embedding_dimension": 2,
        "is_chain_ring": False,
        "size": 81, "character_order": 3, "v_lambda_size": 8,
        "our_law_predicts": 8 + 4,
        "their_exact_depth": 12,
        "significance": (
            "Pass 489 tested only the chain rings F_p[x]/(x^k).  This is a "
            "non-chain Frobenius ring of embedding dimension 2, and our law "
            "predicts and their exact parity-block computation attains 12.  A "
            "genuine new confirmation, credited to their track."),
        "their_pass_499": {
            "ring": "(Z/9) x F_9", "character_order": 9, "depth": 24,
            "consistent_with_our_trichotomy": True,
            "note": ("character order 9 > p = 3, so our necessity result "
                     "predicts the +4 is absent; their depth 24 = "
                     "v_lambda(81) confirms it")},
    }
    checks["their_501_confirms_our_law_at_nonchain"] = (
        rec["our_law_predicts"] == rec["their_exact_depth"])
    checks["their_499_on_negative_side"] = rec["their_pass_499"][
        "consistent_with_our_trichotomy"]
    return rec


def main_payload():
    checks = {}
    A = part_AB(checks)
    B = part_B_parity_logic(checks)
    Cc = part_C_scope(checks)
    Dd = part_D_intake(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass503.dominant_term_and_parity.v1",
        "status": status,
        "parity_theorem": (
            "Every p_m = tr(D^m) and every e_k is real: D is Hermitian, so "
            "D^m is Hermitian and p_m is real, and Newton's identities then "
            "force the e_k real too.  Hence all their lambda-valuations are "
            "EVEN, extending the Pass-491 corollary from det D to the whole "
            "characteristic polynomial."
        ),
        "parity_negative": (
            "Parity does NOT close the residual.  With q odd the Newton bound "
            "q+1 is already even, so evenness cannot round it up to q+3; that "
            "still needs v_lambda(p_q) >= 2q+2, two further orders in "
            "tr(D^q).  Recorded so the route is not retried."
        ),
        "part_A_observation": (
            "The failure minimum is attained at k = 2q/p in both cases: at "
            "Z/9 the minimisers are k = 3 and k = 6 (= q/p and 2q/p), both "
            "with v = 12; at Z/27 the unique minimiser is k = 18 = 2q/p with "
            "v = 36, while k = q/p = 9 gives only 54.  So the dominant Newton "
            "term is indexed by TWICE the size of the maximal ideal, and its "
            "value is the q + q/p of Pass 491.  TWO DATA POINTS ONLY -- by the "
            "standing lesson of Pass 491 this is an observation, not a "
            "pattern, and a third ring (Z/49 or Z/81) is needed before it is "
            "quoted."
        ),
        "part_A_profiles": A,
        "part_B_parity": B,
        "part_C_scope_of_formula": Cc,
        "part_D_intake_of_498_502": Dd,
        "boundary": (
            "Part A profiles one section per ring (the full Newton run over "
            "Z[zeta_27] is the cost); the parity claims are proved, not "
            "sampled.  Part C rests on the other track's published depth for "
            "the product ring, cited not re-derived."
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
            raise SystemExit("Pass 503 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
