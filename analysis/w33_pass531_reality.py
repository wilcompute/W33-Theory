#!/usr/bin/env python3
"""Pass 531: the q = 3 integrality was REALITY all along -- and that DOES
generalise.

Pass 529 found the six q = 3 characteristic polynomials have rational integer
coefficients.  Pass 530 tested whether that generalises, found ZERO of 40
sections at q = 5 with rational coefficients, and filed it as the fourth q = 3
regularity in a week to fail.  Pass 530 also listed, as explicitly not ruled
out, a weaker statement: coefficients in the REAL subring.  Testing it settles
the matter, and in the opposite direction to the filing.

MEASURED.  At p = 3, 5, 7 -- 72 sections in total -- EVERY characteristic
polynomial coefficient of D lies in the real subring Z[zeta_p]^+, i.e. is fixed
by complex conjugation sigma_{-1}.  Not one exception.

AND THAT EXPLAINS q = 3.  The real subring of Q(zeta_p) has degree (p-1)/2
over Q.  At p = 3 that degree is 1, so Q(zeta_3)^+ = Q and REAL MEANS RATIONAL.
The q = 3 integrality was never a q = 3 fact about integrality; it is the
general fact about reality, seen in the one case where the real subring happens
to be the rationals.  Measured degrees: 1, 2, 3 at p = 3, 5, 7, with rational
coefficients in 30/30 sections at p = 3 and 0/30, 0/12 at p = 5, 7.

A CORRECTION TO PASS 530's FRAMING.  Pass 530 filed this as a failure to
generalise, alongside the profile invariant (Pass 524) and the finiteness of
the charpoly image (Pass 528).  That was right about the LITERAL statement and
wrong about the phenomenon: the underlying fact generalises perfectly, and only
its rational shadow is special to p = 3.  The other three entries on that list
stand; this one is withdrawn from it.

RELATION TO EXISTING WORK.  Pass 491 proved that D Hermitian forces
det D in Z[zeta_p]^+, and formalised it.  What is measured here is the same
statement for EVERY elementary symmetric function of the eigenvalues, not just
the top one.  The natural proof is that D is Hermitian, so its characteristic
polynomial has real coefficients; that is asserted as the likely mechanism and
NOT proved here.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass531_reality.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P511 = _load("p511", "w33_pass511_constant_orbit_theorem.py")
P527 = _load("p527", "w33_pass527_spectrum_deflation.py")


def part_A_reality(checks):
    rows, all_real = {}, True
    for p_, ns in ((3, 30), (5, 30), (7, 12)):
        real = rat = 0
        for s in range(ns):
            R, C, q, D, dcoef, rho = P511.setup(p_, 80000 + s)
            E = P527.epoly(C, D, q)
            is_real, is_rat = True, True
            for k in range(2, q + 1):
                c = E[k]
                den = 1
                for x in c:
                    den = den * x.denominator // gcd(den, x.denominator)
                ci = tuple(int(x * den) for x in c)
                if C.sigma(p_ - 1, ci) != ci:
                    is_real = False
                if any(ci[1:]):
                    is_rat = False
            real += is_real
            rat += is_rat
        if real != ns:
            all_real = False
        rows[f"p{p_}"] = {"sections": ns, "real_coefficients": real,
                          "rational_coefficients": rat,
                          "degree_of_real_subring": (p_ - 1) // 2}
    checks["every_coefficient_is_real_at_every_prime"] = all_real
    checks["rational_exactly_when_the_real_subring_is_Q"] = all(
        (r["rational_coefficients"] == r["sections"])
        == (r["degree_of_real_subring"] == 1) for r in rows.values())
    checks["three_primes_tested"] = len(rows) == 3
    return {"rows": rows,
            "finding": (
                "Across 72 sections at p = 3, 5, 7 every characteristic "
                "polynomial coefficient of D lies in the real subring "
                "Z[zeta_p]^+, without exception.  Rational coefficients occur "
                "at p = 3 only, and the real subring has degree (p-1)/2 over "
                "Q -- which is 1 exactly at p = 3.  So REAL MEANS RATIONAL "
                "there, and the q = 3 integrality is the general reality seen "
                "in the one case where the real subring is the rationals."),
            "likely_mechanism_not_proved": (
                "D is Hermitian, so its characteristic polynomial should have "
                "real coefficients; Pass 491 proved and formalised the top "
                "case, det D in Z[zeta_p]^+.  Extending that argument to every "
                "elementary symmetric function is the natural proof and is NOT "
                "carried out here.")}


def part_B_correction(checks):
    checks["pass530_entry_withdrawn"] = True
    return {"withdrawn": (
        "Pass 530 filed the q = 3 integrality as the fourth q = 3 regularity "
        "in a week to fail at q = 5, alongside the profile invariant "
        "(Pass 524) and the finiteness of the charpoly image (Pass 528).  That "
        "was correct about the LITERAL statement -- rational coefficients "
        "really do fail at q = 5 -- and wrong about the phenomenon.  The "
        "underlying fact, reality, generalises perfectly; only its rational "
        "shadow is special to p = 3.  This entry is withdrawn from that list."),
        "what_stands": (
            "The other three entries stand unchanged: the factorial law's "
            "agreement locus (Pass 519), the profile invariant (Pass 524), and "
            "the finiteness of the charpoly image (Pass 528) all genuinely "
            "fail beyond q = 3."),
        "lesson": (
            "Pass 530 tested the literal generalisation, found it false, and "
            "listed the weaker statement as untested rather than testing it.  "
            "The weaker statement was true and was the real content.  When a "
            "generalisation fails, the next move is to weaken it, not to file "
            "it.")}


def main_payload():
    checks = {}
    A = part_A_reality(checks)
    B = part_B_correction(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass531.reality.v1",
        "status": status,
        "headline": (
            "THE q = 3 INTEGRALITY WAS REALITY ALL ALONG, AND THAT "
            "GENERALISES.  Across 72 sections at p = 3, 5, 7 every "
            "characteristic polynomial coefficient of D lies in the real "
            "subring Z[zeta_p]^+ -- no exceptions.  The real subring has "
            "degree (p-1)/2 over Q, which is 1 exactly at p = 3, so there REAL "
            "MEANS RATIONAL: the six integral polynomials of Pass 529 are the "
            "general reality seen in the one case where the real subring is "
            "the rationals.  Pass 530 had filed the failure of literal "
            "rationality at q = 5 as a fourth q = 3 regularity that does not "
            "transfer; that entry is WITHDRAWN.  The literal statement fails, "
            "the phenomenon does not."),
        "part_A_reality": A,
        "part_B_correction_to_pass530": B,
        "boundary": (
            "Part A samples 30, 30 and 12 sections at p = 3, 5, 7 and measures "
            "reality exactly, by comparing each coefficient with its image "
            "under sigma_{-1} in Z[zeta_p].  It is a measurement, not a proof: "
            "the natural argument -- D Hermitian, hence a real characteristic "
            "polynomial, extending Pass 491's result for det D to every "
            "elementary symmetric function -- is stated and not carried out.  "
            "Part B is a correction to an earlier framing, not a computation."),
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
            raise SystemExit("Pass 531 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
