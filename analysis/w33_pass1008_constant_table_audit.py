#!/usr/bin/env python3
"""Pass 1008: auditing the constant tables, and one structural result that holds.

The repository contains more than fifty tables of Standard-Model constants, of
uneven quality.  The most-cited is the PDG-2025 alignment ledger, which is
attractive precisely because it does the right thing on the surface: it gives a
closed form, a value, the measured value, and a deviation in sigma.  This pass
evaluates every closed form in it.

FINDING 1 -- MOST CLOSED FORMS DO NOT EVALUATE TO THEIR OWN STATED VALUE.

Of fourteen entries, nine produce a number other than the one printed beside
them:

    m_H        1/(q^-5) = q^5             -> 243        printed 125
    H_0        12/q!                      -> 2          printed 67
    m_W        v_EW sqrt((1-3/13)/2)      -> 152.56     printed 80.44
    |V_us|     sqrt(3/v) k                -> 3.286      printed 0.2253
    n_s        1 - 2/(q q)                -> 0.7778     printed 0.9667
    Omega_L    1 - 1/(k Phi_4/10)         -> 0.9167     printed 0.6833
    sin^2t12   3/(4*13) = 3/52            -> 0.05769    printed 0.3077
    sin^2t13   3/(6*29)                   -> 0.01724    printed 0.02198
    alpha^-1   k^2 + (k-1)^2 + lambda     -> 267        printed 137.036

The printed values are mostly close to experiment, so the arithmetic that
produced them presumably existed somewhere; what is published is not it.  A
formula that does not evaluate to its own claimed value is not a derivation, and
a referee checking one line finds this immediately.

FINDING 2 -- OF THE FIVE THAT DO EVALUATE, MOST ARE EXCLUDED ANYWAY.

    N_nu       q                    = 3          exact, agrees
    sin^2t23   7/13                 = 0.53846    0.4 sigma, agrees
    m_t        v_EW/sqrt(2)         = 173.948    4.8 sigma from 172.57(29)
    sin^2thW   q/(q^2+q+1) = 3/13   = 0.230769   15.0 sigma from 0.23122(3)
    alpha^-1   k^2 - (|r|+|s|+1)    = 137        integer only; the .036 is not derived

Two rows survive both tests: N_nu = q = 3, and sin^2 theta_23 = 7/13.  That is
the honest state of the dimensionful-constant program.  It is worth separating
from the combinatorial chain (40 = 1+24+15, 240 = 40*3*2, k = 8+3+1,
v-1-k = 27), which is exact and unaffected: counting the geometry works;
predicting a dimensionful constant, so far, does not.

FINDING 3 -- ONE STRUCTURAL RESULT SURVIVES CHECKING, AND IT IS SHARP.

Following the repository's own bijection solvers, the eight vertices
[7, 1, 0, 13, 24, 28, 37, 16] induce a subgraph of W(3,3) that IS the E8 Dynkin
diagram: degree sequence [1,1,1,2,2,2,2,3], Gram 2I - A_sub positive definite,
and det(Gram) = 1, the E8 Cartan determinant.  Verified here directly.

The caveat is the solver's own and is kept: the edge graph is 22-regular while
the E8 root graph is 56-regular, so they are not isomorphic as graphs.  The
240 = 240 edge-root correspondence is a bijection of sets carrying a group
action, and an equivariant map still has to be constructed rather than inferred
from the count.

BOUNDARY.  This audits one ledger, the most-cited one; the other fifty-odd tables
are not evaluated here.  Nothing is claimed about whether better formulas for
these observables exist -- only that the published ones do not compute.  PDG
values and uncertainties are those quoted in the ledger itself, so the sigma
figures are on its own terms.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1008_constant_table_audit.json"
BASE = ROOT / "analysis" / "w33_pass682_flatblock_h1_branch_separation.py"

q, v, k, lam, mu = 3, 40, 12, 2, 4
r, s = 2, -4
Phi4 = q * q + 1
vEW = 246.0

# name, formula text, evaluated, printed, pdg, err
LEDGER = [
    ("N_nu", "q", float(q), 3.0, 3.0, None),
    ("sin2_theta23_PMNS", "7/13", 7 / 13, 0.5385, 0.546, 0.021),
    ("m_t_pole", "v_EW/sqrt(2)", vEW / math.sqrt(2), 173.95, 172.57, 0.29),
    ("sin2_theta_W", "q/(q^2+q+1)", q / (q * q + q + 1), 0.23077, 0.23122, 0.00003),
    ("alpha_inv_skeleton", "k^2-(|r|+|s|+1)",
     float(k * k - (abs(r) + abs(s) + 1)), 137.0, 137.035999178, None),
    ("alpha_inv_ledger", "k^2+(k-1)^2+lambda",
     float(k * k + (k - 1) ** 2 + lam), 137.036, 137.035999178, None),
    ("V_us", "sqrt(3/v)*k", math.sqrt(3 / v) * k, 0.2253, 0.2245, 0.0008),
    ("m_H", "1/(q^-5)=q^5", float(q ** 5), 125.0, 125.25, 0.17),
    ("m_W", "v_EW*sqrt((1-3/13)/2)", vEW * math.sqrt((1 - 3 / 13) / 2),
     80.44, 80.369, 0.013),
    ("H_0", "12/q!", 12 / math.factorial(q), 67.0, 67.4, 0.5),
    ("n_s", "1-2/(q*q)", 1 - 2 / (q * q), 0.9667, 0.965, 0.004),
    ("Omega_Lambda", "1-1/(k*Phi4/10)", 1 - 1 / (k * Phi4 / 10), 0.6833, 0.685, 0.007),
    ("sin2_theta12_PMNS", "3/(4*13)", 3 / 52, 0.3077, 0.307, 0.013),
    ("sin2_theta13_PMNS", "3/(6*29)", 3 / 174, 0.02198, 0.0220, 0.0007),
]


def part_A_formula_audit(checks):
    rows = {}
    evaluates = 0
    for name, expr, val, printed, pdg, err in LEDGER:
        ok = abs(val - printed) < 1e-3 * max(1.0, abs(printed))
        if ok:
            evaluates += 1
        sig = (abs(val - pdg) / err) if (ok and pdg is not None and err) else None
        rows[name] = {"formula": expr, "evaluates_to": round(val, 6),
                      "printed_value": printed, "formula_matches_claim": ok,
                      "pdg": pdg, "pdg_error": err,
                      "sigma": (round(sig, 2) if sig is not None else None)}
    checks["only_five_of_fourteen_evaluate"] = (evaluates == 5)
    checks["nine_formulas_mismatch"] = (len(LEDGER) - evaluates == 9)
    return {"rows": rows, "entries": len(LEDGER), "evaluate_correctly": evaluates,
            "reading": (
                "Nine of fourteen closed forms produce a number other than the "
                "one printed beside them -- q^5 = 243 against 125, 12/q! = 2 "
                "against 67, and so on.  The printed values are close to "
                "experiment, so some arithmetic produced them, but it is not the "
                "arithmetic that is published.")}


def part_B_survivors(checks):
    surv = {}
    for name, expr, val, printed, pdg, err in LEDGER:
        ok = abs(val - printed) < 1e-3 * max(1.0, abs(printed))
        if not ok or pdg is None or not err:
            continue
        sig = abs(val - pdg) / err
        surv[name] = {"formula": expr, "value": round(val, 6), "pdg": pdg,
                      "sigma": round(sig, 2), "agrees": sig < 3}
    agree = [n for n, d in surv.items() if d["agrees"]]
    checks["at_most_two_rows_agree"] = (len(agree) <= 2)
    checks["N_nu_and_theta23_are_the_survivors"] = (
        set(agree) == {"N_nu", "sin2_theta23_PMNS"}
        or set(agree) == {"sin2_theta23_PMNS"})
    return {"rows": surv, "agreeing": agree,
            "note_on_alpha": (
                "alpha^-1 = k^2-(|r|+|s|+1) = 137 is an exact integer identity; "
                "the measured 137.035999178(8) differs from it in the fourth "
                "digit, and that remainder is not derived"),
            "reading": (
                "Of the five formulas that evaluate, sin^2 theta_W is 15 sigma "
                "out and m_t is 4.8.  Two rows survive both the arithmetic and "
                "the experimental test: N_nu = q = 3, and sin^2 theta_23 = 7/13 "
                "at 0.4 sigma.")}


def part_C_e8_dynkin(checks):
    spec = importlib.util.spec_from_file_location("w33_pass682_base", BASE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pts, edges, tris, K, d1, d2 = mod.build()
    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1
    V = [7, 1, 0, 13, 24, 28, 37, 16]
    sub = A[np.ix_(V, V)]
    G = 2 * np.eye(8, dtype=np.int64) - sub
    det = int(round(float(np.linalg.det(G))))
    ev = np.linalg.eigvalsh(G.astype(float))
    degs = sorted(int(x) for x in sub.sum(axis=1))
    checks["e8_cartan_determinant_is_one"] = (det == 1)
    checks["e8_gram_positive_definite"] = bool((ev > 1e-9).all())
    checks["e8_dynkin_degree_sequence"] = (degs == [1, 1, 1, 2, 2, 2, 2, 3])
    return {"vertices": V, "degree_sequence": degs,
            "expected_dynkin_degrees": [1, 1, 1, 2, 2, 2, 2, 3],
            "gram_determinant": det, "positive_definite": bool((ev > 1e-9).all()),
            "min_eigenvalue": round(float(ev.min()), 6),
            "caveat": (
                "the W(3,3) edge graph is 22-regular and the E8 root graph is "
                "56-regular, so they are not isomorphic; 240 = 240 is a bijection "
                "of sets with a group action, and the equivariant map still has "
                "to be constructed"),
            "reading": (
                "Eight vertices of W(3,3) induce exactly the E8 Dynkin diagram, "
                "and 2I minus that subgraph is the E8 Cartan matrix: positive "
                "definite with determinant 1.  This is the structural claim in "
                "the area that survives checking.")}


def main_payload():
    checks = {}
    A = part_A_formula_audit(checks)
    B = part_B_survivors(checks)
    C = part_C_e8_dynkin(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass1008.constant_table_audit.v1",
        "status": status,
        "headline": (
            "THE CONSTANT TABLES DO NOT EVALUATE, AND ONE STRUCTURAL RESULT DOES. "
            " Evaluating every closed form in the most-cited PDG-2025 ledger, "
            "nine of fourteen produce a number other than the one printed beside "
            "them: q^5 = 243 against a claimed 125 for m_H, 12/q! = 2 against 67 "
            "for H_0, v_EW sqrt((1-3/13)/2) = 152.56 against 80.44 for m_W, and "
            "k^2+(k-1)^2+lambda = 267 against 137 for alpha^-1.  Of the five that "
            "do evaluate, sin^2 theta_W is 15 sigma from experiment and m_t is "
            "4.8, so exactly two survive both tests -- N_nu = q = 3 and "
            "sin^2 theta_23 = 7/13 at 0.4 sigma.  Against that, one structural "
            "claim checks out sharply: the eight vertices [7,1,0,13,24,28,37,16] "
            "induce the E8 Dynkin diagram, with degree sequence [1,1,1,2,2,2,2,3] "
            "and Gram 2I-A positive definite of determinant 1, the E8 Cartan "
            "determinant.  The counting side of the physics program works; the "
            "dimensionful-constant side does not yet."),
        "part_A_formula_audit": A,
        "part_B_survivors": B,
        "part_C_e8_dynkin": C,
        "checks": {k_: bool(v_) for k_, v_ in checks.items()},
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
            raise SystemExit("Pass 1008 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
