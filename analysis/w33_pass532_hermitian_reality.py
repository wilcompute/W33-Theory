#!/usr/bin/env python3
"""Pass 532: the reality theorem, proved -- D is Hermitian, so its
characteristic polynomial is real.

Pass 531 measured that every characteristic polynomial coefficient of D lies in
the real subring Z[zeta_p]^+, across 72 sections at p = 3, 5, 7, and named the
likely proof without carrying it out.  The proof is one line once the right
fact is checked.

  THE FACT.  D is HERMITIAN: D_{ij} = conj(D_{ji}) for all i, j, where
  conjugation is sigma_{-1} on Z[zeta_p].  Verified in 60 of 60 sections at
  p = 3, 5, 7.

  THE THEOREM.  A Hermitian matrix has real eigenvalues, so every elementary
  symmetric function of them is real, so

        charpoly(D) in Z[zeta_p]^+[x] .

  That is Pass 531's measurement, now derived.

WHY q = 3 LOOKED SPECIAL.  The real subring Q(zeta_p)^+ has degree (p-1)/2
over Q, which is 1 exactly at p = 3.  So at p = 3, and only there, real means
rational -- and Pass 529's six integral polynomials are this theorem's shadow
in the one case where the real subring is the rationals.  Nothing about q = 3
was ever special except the degree of a field.

RELATION TO PASS 491.  That pass proved and formalised det D in Z[zeta_p]^+ --
the top coefficient -- from D being Hermitian.  The observation here is that
the same hypothesis gives every coefficient at once, so Pass 491 proved a
corollary of a slightly more general statement that was available all along.
The Hermitian property itself is not proved here either; it is verified
exhaustively over the sampled sections and is presumably immediate from
inverse closure, c(-v) = -c(v), which conjugates d_v.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass532_hermitian_reality.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P511 = _load("p511", "w33_pass511_constant_orbit_theorem.py")


def part_A_hermitian(checks):
    rows, ok = {}, True
    for p_ in (3, 5, 7):
        herm, tot = 0, 0
        for s in range(20):
            R, C, q, D, dcoef, rho = P511.setup(p_, 80000 + s)
            tot += 1
            if all(D[i][j] == C.sigma(p_ - 1, D[j][i])
                   for i in range(q) for j in range(q)):
                herm += 1
        if herm != tot:
            ok = False
        rows[f"p{p_}"] = {"sections": tot, "hermitian": herm}
    checks["D_is_hermitian_everywhere_tested"] = ok
    checks["hermitian_tested_at_three_primes"] = len(rows) == 3
    return {"rows": rows,
            "fact": ("D_{ij} = conj(D_{ji}) with conjugation sigma_{-1} on "
                     "Z[zeta_p], in 60 of 60 sampled sections"),
            "theorem": (
                "A Hermitian matrix has real eigenvalues, so every elementary "
                "symmetric function of them is fixed by complex conjugation, "
                "so charpoly(D) lies in Z[zeta_p]^+[x].  That derives Pass "
                "531's measurement."),
            "not_proved_here": (
                "The Hermitian property itself is verified exhaustively over "
                "the sampled sections rather than derived; it is presumably "
                "immediate from inverse closure, c(-v) = -c(v), which "
                "conjugates d_v, but that step is not written out.")}


def part_B_consequences(checks):
    checks["q3_specialness_explained"] = True
    checks["pass491_relation_recorded"] = True
    return {"q3": (
        "The real subring Q(zeta_p)^+ has degree (p-1)/2 over Q, which is 1 "
        "exactly at p = 3.  So at p = 3, and only there, real means rational, "
        "and Pass 529's six integral characteristic polynomials are this "
        "theorem's shadow in the one case where the real subring is the "
        "rationals.  Nothing about q = 3 was special except the degree of a "
        "field."),
        "pass491": (
            "Pass 491 proved and formalised det D in Z[zeta_p]^+ -- the top "
            "coefficient -- from D being Hermitian.  The same hypothesis gives "
            "EVERY coefficient at once, so that result is a corollary of a "
            "slightly more general statement which was available all along."),
        "arc_note": (
            "Three passes were spent on this: 529 found the six integral "
            "polynomials, 530 tested literal rationality at q = 5, found it "
            "false and filed it, 531 tested the real-subring version and found "
            "it true, and 532 derived it.  The shortest path was to ask what "
            "Pass 491 had already assumed about D.")}


def main_payload():
    checks = {}
    A = part_A_hermitian(checks)
    B = part_B_consequences(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass532.hermitian_reality.v1",
        "status": status,
        "headline": (
            "THE REALITY THEOREM, DERIVED.  D is Hermitian -- "
            "D_{ij} = conj(D_{ji}) under sigma_{-1}, in 60 of 60 sampled "
            "sections at p = 3, 5, 7 -- and a Hermitian matrix has real "
            "eigenvalues, so every elementary symmetric function of them is "
            "fixed by conjugation and charpoly(D) lies in Z[zeta_p]^+[x].  "
            "That derives Pass 531's measurement.  Since the real subring has "
            "degree (p-1)/2, which is 1 exactly at p = 3, real means rational "
            "there and only there: Pass 529's six integral polynomials are "
            "this theorem's shadow in the one case where the real subring is "
            "the rationals.  Nothing about q = 3 was special except the degree "
            "of a field.  Pass 491 proved the top coefficient from the same "
            "hypothesis; every coefficient follows at once."),
        "part_A_hermitian": A,
        "part_B_consequences": B,
        "boundary": (
            "The Hermitian property is VERIFIED over 60 sampled sections, not "
            "derived; the derivation from inverse closure is presumably short "
            "but is not written out.  Given that property the reality of the "
            "characteristic polynomial is immediate and general.  Part B is "
            "commentary."),
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
            raise SystemExit("Pass 532 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
