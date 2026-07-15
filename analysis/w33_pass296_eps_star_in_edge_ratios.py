#!/usr/bin/env python3
"""Pass 296: is eps* = (5 - sqrt21)/2 expressible in Szilassi edge ratios?

Pass 274 put the Koide light cone at eps* = (5 - sqrt 21)/2, a norm-1 unit of
Q(sqrt 21).  Pass 286 found sqrt(21) in the Szilassi edge lengths; Pass 293 then
showed it is a coordinate choice, not forced.  Edge LENGTHS are not scale
invariant, so the sharper question is whether sqrt(21) -- and hence eps* -- lives
in the scale-invariant data: the RATIOS of edge lengths.

It does, and cleanly, in BOTH published realizations:
    v1:  Edge7 / Edge1 = (5*sqrt21/2) / (5/2) = sqrt(21)
    v2:  Edge5 / Edge1 = (2*sqrt21)  / 2      = sqrt(21)
So sqrt(21) is exactly a ratio of two edge lengths in each Szilassi realization,
and being a ratio it survives any rescaling of the polyhedron.  eps* is then the
arithmetic expression (5 - r)/2 in that ratio r, and its conjugate (5 + r)/2 is
the other root, with product 1.

HONEST WEIGHT.  This does NOT undo Pass 293. The ratio is still a consequence of
Szilassi's chosen coordinates; a generic realization has no such rational
relation. What the ratio formulation adds is that the occurrence is at least
SCALE-INVARIANT -- it is not an artefact of how big the polyhedron was drawn --
and that both of Szilassi's independent choices produce the SAME ratio sqrt(21)
from their respective shortest edges.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass296_eps_star_in_edge_ratios.json"

R2 = sp.Rational
S = sp.sqrt

# the published edge-length tables (exact), by realization
V1_LENGTHS = {
    "e1": R2(5, 2), "e2": 5 * S(2) / 2, "e3": 3 * S(106) / 4, "e4": 18 * S(6) / 5,
    "e5": S(1514) / 4, "e6": 15 * S(2) / 2, "e7": 5 * S(21) / 2, "e8": R2(23, 2),
    "e9": 7 * S(206) / 5, "e10": 5 * S(21), "e11": sp.Integer(24), "e12": R2(126, 5),
}
V2_LENGTHS = {
    "e1": sp.Integer(2), "e2": 2 * S(13) / 3, "e3": 5 * S(253) / 12,
    "e4": 3 * S(101) / 4, "e5": 2 * S(21), "e6": 8 * S(13) / 3,
    "e7": 2 * S(349) / 3, "e8": R2(44, 3), "e9": 4 * S(29), "e10": sp.Integer(24),
    "e11": 21 * S(21) / 4,
}


def main():
    checks = {}
    x = sp.Symbol("x")
    eps = R2(5, 2) - S(21) / 2

    # ---- sqrt(21) as an exact ratio of two edge lengths, in each realization
    found = {}
    for name, T in (("v1", V1_LENGTHS), ("v2", V2_LENGTHS)):
        hits = []
        keys = list(T)
        for a in keys:
            for b in keys:
                if a == b:
                    continue
                r = sp.radsimp(sp.simplify(T[a] / T[b]))
                if sp.simplify(r - S(21)) == 0:
                    hits.append({"ratio": f"{a}/{b}",
                                 "numerator": str(T[a]), "denominator": str(T[b])})
        found[name] = hits
        checks[f"{name}_realizes_sqrt21_as_an_edge_ratio"] = len(hits) > 0

    checks["both_realizations_give_sqrt21_as_a_ratio"] = all(
        len(v) > 0 for v in found.values())
    # the specific clean ones
    checks["v1_e7_over_e1_is_sqrt21"] = sp.simplify(
        V1_LENGTHS["e7"] / V1_LENGTHS["e1"] - S(21)) == 0
    checks["v2_e5_over_e1_is_sqrt21"] = sp.simplify(
        V2_LENGTHS["e5"] / V2_LENGTHS["e1"] - S(21)) == 0
    # in both cases the denominator is the SHORTEST edge
    checks["v1_denominator_is_shortest"] = V1_LENGTHS["e1"] == min(
        V1_LENGTHS.values(), key=lambda z: float(z))
    checks["v2_denominator_is_shortest"] = V2_LENGTHS["e1"] == min(
        V2_LENGTHS.values(), key=lambda z: float(z))

    # ---- eps* from the ratio
    r = sp.Symbol("r", positive=True)
    eps_expr = (5 - r) / 2
    checks["eps_star_from_ratio"] = sp.simplify(eps_expr.subs(r, S(21)) - eps) == 0
    conj = (5 + S(21)) / 2
    checks["eps_times_conjugate_is_1"] = sp.simplify(eps * conj - 1) == 0
    checks["eps_minpoly_x2_5x_1"] = sp.simplify(
        sp.minimal_polynomial(eps, x) - (x ** 2 - 5 * x + 1)) == 0
    checks["ratios_are_scale_invariant"] = True   # r = L_a/L_b is unchanged by scaling

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass296.eps_star_in_edge_ratios.v1",
        "status": "PASS" if all_pass else "FAIL",
        "finding": (
            "sqrt(21) is exactly a RATIO of two edge lengths in BOTH published "
            "Szilassi realizations: v1 has Edge7/Edge1 = (5*sqrt21/2)/(5/2) = "
            "sqrt(21), and v2 has Edge5/Edge1 = (2*sqrt21)/2 = sqrt(21). In each "
            "case the denominator is the realization's SHORTEST edge. Being a "
            "ratio, this is scale-invariant -- unlike the raw lengths."
        ),
        "sqrt21_ratios": found,
        "eps_star": {
            "definition": "(5 - sqrt21)/2, the FN parameter on the Koide light "
                          "cone (Pass 274)",
            "from_the_ratio": "eps* = (5 - r)/2 with r = Edge7/Edge1 (v1) or "
                              "Edge5/Edge1 (v2)",
            "numeric": float(eps),
            "minimal_polynomial": "x^2 - 5x + 1",
            "unit": "eps* * conj(eps*) = 1 -- a norm-1 unit of Q(sqrt 21)",
        },
        "honest_weight": (
            "This does NOT undo Pass 293. The ratio is still a consequence of "
            "Szilassi's chosen rational coordinates; a generic realization from "
            "the ~14-dimensional moduli space has no such relation. What the "
            "ratio formulation adds is that the occurrence is at least "
            "SCALE-INVARIANT -- not an artefact of how large the polyhedron was "
            "drawn -- and that both of Szilassi's independent coordinate choices "
            "produce the SAME ratio sqrt(21) against their respective shortest "
            "edges. That is a sharper coincidence than the raw lengths were, but "
            "it is still a coincidence of two choices, not an invariant."
        ),
        "reading": (
            "eps* is reachable from the Szilassi metric by a scale-invariant "
            "construction: take the ratio of a sqrt(21)-edge to the shortest "
            "edge, get sqrt(21), and form (5 - sqrt21)/2. Whether that means "
            "anything depends entirely on Pass 293's open question -- whether "
            "some natural sub-family of realizations forces the relation. If it "
            "does, this is a bridge; if not, it is arithmetic on two pretty "
            "coordinate choices."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
