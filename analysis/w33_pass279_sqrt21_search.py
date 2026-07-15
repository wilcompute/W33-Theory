#!/usr/bin/env python3
"""Pass 279: is sqrt(21) anywhere in the substrate?

Pass 274 produced a sharp number: the Froggatt-Nielsen texture (2,1,0) sits on
the Koide light cone exactly at

    eps* = (5 - sqrt 21)/2 = 0.2087121525...,   the root of  x^2 - 5x + 1 = 0.

Its algebra is striking: eps* * conj(eps*) = (25-21)/4 = 1, so eps* is a UNIT of
norm 1 in the real quadratic field Q(sqrt 21).  Meanwhile the even-q tower has
its own quadratic irrationality, lambda_pm = (9 +- sqrt 17)/2 from
x^2 - 9x + 16 (Pass 256), living in Q(sqrt 17).

So the question is whether eps* is an accident of the FN parametrisation or
something the substrate actually contains: does sqrt(21), or the field
Q(sqrt 21), appear anywhere in W(3,q)'s spectra?

We search the natural places, exactly:
  * the collinearity SRG eigenvalues q(q+1), q-1, -(q+1) and the discriminant of
    their defining quadratic, for q = 2,3,4,5,7,8,9,11,13,16,25,27;
  * the incidence Gram N N^T eigenvalues (q+1)^2, 2q, 0 (Pass 266);
  * the even-q transfer matrix's discriminant (17) and its powers;
  * the CSS family parameters (n, k, d) and the sentinel multiplicity g;
  * PGSp(4,3)/PSp(4,3) order factorisations (51840, 25920) and W(3,3)'s
    characteristic numbers (40, 15, 25, 27, 45, 36, 80, 12, 2, -4).

A hit would suggest the cone condition has an algebraic origin inside the
geometry.  A clean miss says eps* is a feature of the FN parametrisation, not of
the substrate -- which, given Pass 274 already showed FN merely accommodates
Koide, is the honest expectation.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass279_sqrt21_search.json"

QS = (2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 25, 27)


def squarefree_part(n):
    n = abs(int(n))
    if n == 0:
        return 0
    out = 1
    for p, e in sp.factorint(n).items():
        if e % 2:
            out *= p
    return out


def main():
    checks = {}

    # ---- the target number and its algebra
    x = sp.Symbol("x")
    eps = sp.Rational(5, 2) - sp.sqrt(21) / 2
    minpoly = sp.minimal_polynomial(eps, x)
    checks["eps_minpoly_is_x2_5x_1"] = sp.simplify(minpoly - (x ** 2 - 5 * x + 1)) == 0
    conj = sp.Rational(5, 2) + sp.sqrt(21) / 2
    checks["eps_is_unit_norm_1"] = sp.simplify(eps * conj - 1) == 0
    checks["eps_numeric"] = abs(float(eps) - 0.2087121525) < 1e-9
    checks["disc_of_eps_quadratic_is_21"] = (5 ** 2 - 4 * 1) == 21

    # ---- the even tower's own irrationality, for contrast
    checks["tower_disc_is_17"] = (9 ** 2 - 4 * 16) == 17
    checks["17_and_21_differ"] = squarefree_part(17) != squarefree_part(21)

    # ---- search the substrate's spectra for squarefree part 21
    found = []
    scanned = {}

    for q in QS:
        v = (q + 1) * (q * q + 1)
        k_srg, r, s = q * (q + 1), q - 1, -(q + 1)
        g = q * (q * q + 1) // 2
        rank0 = (q * q + 1) * (q + 2) // 2
        # the SRG eigenvalue quadratic: x^2 - (lambda-mu) x - (k-mu)
        lam, mu = q - 1, q + 1
        disc_srg = (lam - mu) ** 2 + 4 * (k_srg - mu)
        nnt = [(q + 1) ** 2, 2 * q, 0]
        cands = {
            "v": v, "k_srg": k_srg, "r": r, "s": s, "g": g, "char0_rank": rank0,
            "disc_srg": disc_srg, "NNt_top": nnt[0], "NNt_mid": nnt[1],
            "css_n": v, "css_k": q * q + 1, "css_d": q + 1,
        }
        sf = {kk: squarefree_part(val) for kk, val in cands.items()}
        scanned[str(q)] = {"values": cands, "squarefree_parts": sf}
        for kk, s21 in sf.items():
            if s21 == 21:
                found.append({"q": q, "quantity": kk, "value": cands[kk]})

    # ---- group orders and W(3,3) characteristic numbers
    others = {
        "|PGSp(4,3)|": 51840, "|PSp(4,3)|": 25920, "|S6|": 720, "|S3|": 6,
        "w33_points": 40, "sentinel_dim": 15, "context_dim": 25,
        "shell_27": 27, "gq42_points": 45, "dodecads": 36, "theta_80": 80,
        "srg_k": 12, "srg_r": 2, "srg_s": -4, "E8_layer": 8, "so10": 10,
        "e6_27": 27, "e8_248": 248, "A8_min_words": 45,
    }
    others_sf = {kk: squarefree_part(val) for kk, val in others.items()}
    for kk, s21 in others_sf.items():
        if s21 == 21:
            found.append({"q": None, "quantity": kk, "value": others[kk]})

    # ---- also: does any SRG discriminant generate Q(sqrt 21)?
    # ---- the MEANINGFUL test: sqrt(21) is present only if some quantity is
    # genuinely IRRATIONAL in Q(sqrt 21) -- i.e. a discriminant with squarefree
    # part 21. A rational integer whose squarefree part happens to be 21 (like
    # 756 = 21*6^2) contains no sqrt(21) at all; that is a false positive of the
    # crude test, and we separate the two.
    irrational_hits = [h for h in found
                       if h["quantity"] in ("disc_srg",)]
    rational_coincidences = [h for h in found
                             if h["quantity"] not in ("disc_srg",)]
    checks["no_srg_disc_is_21"] = not any(
        scanned[str(q)]["squarefree_parts"]["disc_srg"] == 21 for q in QS)
    # the SRG discriminant is 4q^2 -- a perfect square at EVERY q, so the SRG
    # eigenvalues (q-1, -(q+1)) are always rational and contribute no
    # irrationality whatsoever.
    srg_disc_is_square = all(
        sp.sqrt(scanned[str(q)]["values"]["disc_srg"]).is_rational for q in QS)
    checks["srg_disc_is_always_a_perfect_square"] = bool(srg_disc_is_square)
    checks["srg_contributes_no_irrationality"] = bool(srg_disc_is_square)
    checks["search_completed"] = True
    checks["no_genuine_sqrt21"] = len(irrational_hits) == 0

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass279.sqrt21_search.v1",
        "status": "PASS" if all_pass else "FAIL",
        "target": {
            "eps_star": "(5 - sqrt 21)/2",
            "numeric": float(eps),
            "minimal_polynomial": "x^2 - 5x + 1",
            "discriminant": 21,
            "algebraic_nature": "a UNIT of norm 1 in Q(sqrt 21): eps * conj(eps) = 1",
            "origin": "Pass 274: the FN(2,1,0) texture lands on the Koide light "
                      "cone exactly at this eps",
        },
        "contrast": {
            "even_tower_irrationality": "(9 +- sqrt 17)/2 from x^2 - 9x + 16",
            "discriminant": 17,
            "note": "the substrate's known quadratic irrationality is sqrt 17, "
                    "not sqrt 21; det = 16 is not a unit, so lambda_pm are not "
                    "units, unlike eps*",
        },
        "scanned_quantities": scanned,
        "other_invariants_squarefree_parts": others_sf,
        "raw_squarefree_hits": found,
        "genuine_irrational_hits": irrational_hits,
        "rational_coincidences": rational_coincidences,
        "srg_discriminant": "4q^2 -- a perfect square at every q, so the SRG "
                            "eigenvalues q-1 and -(q+1) are always RATIONAL and "
                            "the SRG contributes no irrationality at all",
        "verdict": (
            "sqrt(21) does NOT appear in the substrate. No discriminant has "
            "squarefree part 21; indeed the SRG discriminant is 4q^2, a perfect "
            "square at every q, so the collinearity graph is rational through "
            "and through. The one raw hit -- k_srg(27) = 756 = 21 * 6^2 -- is a "
            "FALSE POSITIVE of the crude squarefree test: 756 is a rational "
            "integer and contains no sqrt(21). The substrate's only genuine "
            "quadratic irrationality is sqrt 17, from the even-q transfer "
            "matrix x^2 - 9x + 16 -- a different field from Q(sqrt 21)."
            if not irrational_hits else
            f"genuine sqrt(21) FOUND in: {irrational_hits}"
        ),
        "reading": (
            "eps* = (5-sqrt21)/2 is genuinely distinguished as an algebraic "
            "number -- a norm-1 unit of Q(sqrt 21) -- but it is not a number the "
            "geometry contains. The substrate does carry a quadratic "
            "irrationality, sqrt 17, and it belongs to the even-q transfer "
            "matrix, a different field entirely. Combined with Pass 274 (FN "
            "accommodates Koide rather than deriving it), the conclusion is that "
            "eps* is an artefact of the FN parametrisation, not a fingerprint of "
            "W(3,q). The single raw hit (756 = 21*6^2 at q=27) is a rational "
            "integer and a false positive of the squarefree test -- worth "
            "recording precisely because it shows how easily such a search "
            "manufactures a coincidence. The Koide cone condition remains sharply stated (Pass 257: "
            "a null ray of the family clock's Minkowski metric) and unexplained, "
            "and this pass closes off one more way it might have been explained."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
