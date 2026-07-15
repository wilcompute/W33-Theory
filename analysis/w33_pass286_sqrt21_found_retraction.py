#!/usr/bin/env python3
"""Pass 286: sqrt(21) IS in the substrate -- a RETRACTION of Passes 279 and 285.

Passes 279 and 285 concluded that sqrt(21) does not appear in the substrate, and
that the Koide/FN constant eps* = (5 - sqrt 21)/2 is an artefact of the FN
parametrisation.  BOTH CONCLUSIONS WERE WRONG, and the error was one of method:
those passes searched SPECTRA (SRG eigenvalues, discriminants, group orders) and
COUNTS (flags, edges), and never looked at the one place the number actually
lives -- the METRIC data of the toroidal polyhedra, which this repository has
carried all along in `data/Toroidal-Polyhedra-Realizations.txt`.

That file holds all SEVEN realizations: five Csaszar and two Szilassi (Szilassi,
"On Three Classes of Regular Toroids", 2004).  Computing the 21 edge lengths of
each directly from the published vertex coordinates -- not trusting the file's
own labels -- gives:

    Szilassi v1:  5*sqrt(21)/2  (x2)   and   5*sqrt(21)    (x2)
    Szilassi v2:  2*sqrt(21)    (x2)   and   21*sqrt(21)/4 (x2)

So FOUR of the 21 edges carry sqrt(21) in EACH Szilassi realization, and
sqrt(21) appears in BOTH Szilassi realizations -- while appearing in NONE of the
five Csaszar ones.  The Szilassi polyhedron is the DUAL toroid of Csaszar and the
genus-1 rung of the Jungerman-Ringel ladder that `part18_jungerman_ringel.tex`
claims is parameterised by W(3,3).

Note also Szilassi v2's edge 21*sqrt(21)/4 = 21^{3/2}/4: the 21 appears there
both as a coefficient AND under the root.

WHY THE EARLIER PASSES MISSED IT.  Pass 279's rule -- "to find an irrationality,
test discriminants, not squarefree parts of integers" -- was right as far as it
went, but it silently assumed the only irrationalities in play were SPECTRAL.
A polyhedron's edge lengths are metric data: they are square roots of integer
quadratic forms in the vertex coordinates, and they generate real quadratic
fields with no discriminant anywhere in sight. Pass 285 then compounded the
error by reasoning about COUNTS (21 = C(7,2) edges, Fano flags) and concluding
that a rational 21 "cannot manufacture" sqrt(21) -- true, but irrelevant, because
the sqrt(21) was never coming from the count. It was in the geometry's metric.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "Toroidal-Polyhedra-Realizations.txt"
OUT = ROOT / "data" / "w33_pass286_sqrt21_found_retraction.json"

# exact vertex coordinates, transcribed from the file's published realizations
R2 = sp.Rational
S = sp.sqrt

CSASZAR = {
    1: [(3, -3, -R2(15, 2)), (-3, 3, -R2(15, 2)), (3, 3, -R2(13, 2)),
        (-3, -3, -R2(13, 2)), (1, 2, -R2(9, 2)), (-1, -2, -R2(9, 2)),
        (0, 0, R2(15, 2))],
    2: [(4 * S(15), 0, -10), (-4 * S(15), 0, -10), (0, 8, -6), (0, -8, -6),
        (-1, 2, 1), (1, -2, 1), (0, 0, 10)],
    3: [(12, 0, -4 * S(15)), (-12, 0, -4 * S(15)), (0, 4 * S(15), 0),
        (0, -4 * S(15), 0), (3, -3, -3), (-3, 3, -3), (0, 0, 4 * S(15))],
    4: [(12, 0, -6 * S(2)), (-12, 0, -6 * S(2)), (0, 12, 6 * S(2)),
        (0, -12, 6 * S(2)), (-4, -3, S(2) / 2), (4, 3, S(2) / 2),
        (0, 0, 8 * S(2) / 3)],
    5: [(12, 0, -6 * S(2)), (-12, 0, -6 * S(2)), (0, 12, 6 * S(2)),
        (0, -12, 6 * S(2)), (-3, 3, 2 * S(2)), (3, -3, 2 * S(2)),
        (0, 0, -2 * S(2))],
}
CSASZAR_FACES = [[0, 1, 2], [0, 2, 5], [0, 5, 4], [0, 4, 6], [0, 6, 3], [0, 3, 1],
                 [1, 3, 4], [1, 4, 5], [1, 5, 6], [1, 6, 2], [2, 6, 4], [2, 4, 3],
                 [2, 3, 5], [5, 3, 6]]

SZILASSI = {
    1: [(12, 0, 12), (-12, 0, 12), (0, R2(126, 10), -12), (0, -R2(126, 10), -12),
        (2, -5, -8), (-2, 5, -8), (R2(15, 4), R2(15, 4), -3),
        (-R2(15, 4), -R2(15, 4), -3), (R2(9, 2), -R2(5, 2), 2),
        (-R2(9, 2), R2(5, 2), 2), (7, 0, 2), (-7, 0, 2), (7, R2(5, 2), 2),
        (-7, -R2(5, 2), 2)],
    2: [(12, 0, 12), (-12, 0, 12), (0, 12, -12), (0, -12, -12),
        (R2(3, 2), -R2(21, 4), -9), (-R2(3, 2), R2(21, 4), -9),
        (R2(8, 3), 4, -4), (-R2(8, 3), -4, -4), (R2(20, 3), -2, 4),
        (-R2(20, 3), 2, 4), (8, 0, 4), (-8, 0, 4), (8, 2, 4), (-8, -2, 4)],
}
SZILASSI_FACES = [[0, 1, 13, 8, 7, 4], [0, 4, 3, 2, 10, 12], [0, 12, 9, 6, 5, 1],
                  [11, 3, 4, 7, 6, 9], [11, 9, 12, 10, 8, 13],
                  [11, 13, 1, 5, 2, 3], [2, 5, 6, 7, 8, 10]]


def edges_of(faces):
    E = set()
    for f in faces:
        for i in range(len(f)):
            E.add(tuple(sorted((f[i], f[(i + 1) % len(f)]))))
    return sorted(E)


def edge_lengths(V, faces):
    out = []
    for (a, b) in edges_of(faces):
        d2 = sum((V[a][k] - V[b][k]) ** 2 for k in range(3))
        out.append(sp.radsimp(sp.sqrt(sp.expand(d2))))
    return out


def has_sqrt21(x):
    """does the exact length contain sqrt(21) as a genuine irrationality?"""
    r = sp.radsimp(sp.nsimplify(x))
    if r.is_rational:
        return False
    # square the length: L = c*sqrt(21) iff L^2 / 21 is a rational SQUARE
    sq = sp.nsimplify(sp.expand(r ** 2))
    if not sq.is_rational:
        return False
    ratio = sp.nsimplify(sq / 21)
    return bool(sp.sqrt(ratio).is_rational)


def main():
    checks = {}
    checks["data_file_exists"] = DATA.exists()
    txt = DATA.read_text(encoding="utf-8")
    checks["five_csaszar_blocks"] = len(re.findall(r"Csaszar Polyhedron \(version", txt)) == 5
    checks["two_szilassi_blocks"] = len(re.findall(r"Szilassi Polyhedron \(version", txt)) == 2
    checks["seven_realizations_total"] = (5 + 2) == 7

    report = {}
    total_sqrt21_edges = 0
    for name, table, faces in (("csaszar", CSASZAR, CSASZAR_FACES),
                               ("szilassi", SZILASSI, SZILASSI_FACES)):
        report[name] = {}
        for ver, V in table.items():
            L = edge_lengths(V, faces)
            assert len(L) == 21, (name, ver, len(L))
            uniq = {}
            for x in L:
                k = str(x)
                uniq[k] = uniq.get(k, 0) + 1
            s21 = {k: c for k, c in uniq.items() if has_sqrt21(sp.nsimplify(k))}
            n21 = sum(s21.values())
            total_sqrt21_edges += n21
            report[name][str(ver)] = {
                "edge_count": len(L),
                "distinct_lengths": len(uniq),
                "sqrt21_lengths": s21,
                "sqrt21_edge_count": n21,
            }
            checks[f"{name}_v{ver}_has_21_edges"] = len(L) == 21

    # THE FINDING
    sz = report["szilassi"]
    cs = report["csaszar"]
    checks["szilassi_v1_has_sqrt21"] = sz["1"]["sqrt21_edge_count"] > 0
    checks["szilassi_v2_has_sqrt21"] = sz["2"]["sqrt21_edge_count"] > 0
    checks["both_szilassi_have_sqrt21"] = all(
        sz[v]["sqrt21_edge_count"] > 0 for v in ("1", "2"))
    checks["each_szilassi_has_four_sqrt21_edges"] = all(
        sz[v]["sqrt21_edge_count"] == 4 for v in ("1", "2"))
    checks["no_csaszar_has_sqrt21"] = all(
        cs[v]["sqrt21_edge_count"] == 0 for v in cs)
    checks["sqrt21_IS_in_the_substrate"] = total_sqrt21_edges > 0

    # cross-check against the file's own published labels
    checks["file_states_5sqrt21_over_2"] = "5*sqrt(21)/2" in txt
    checks["file_states_5sqrt21"] = "5*sqrt(21)" in txt
    checks["file_states_2sqrt21"] = "2*sqrt(21)" in txt
    checks["file_states_21sqrt21_over_4"] = "21*sqrt(21)/4" in txt

    # the retracted claims
    eps_star = sp.Rational(5, 2) - sp.sqrt(21) / 2
    checks["eps_star_lives_in_Q_sqrt21"] = sp.sqrt(21) in eps_star.atoms(sp.Pow)

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass286.sqrt21_found_retraction.v1",
        "status": "PASS" if all_pass else "FAIL",
        "RETRACTION": (
            "Passes 279 and 285 concluded that sqrt(21) does not appear in the "
            "substrate. THAT IS FALSE and both conclusions are hereby WITHDRAWN. "
            "sqrt(21) appears in the EDGE LENGTHS of both Szilassi realizations, "
            "computed here directly from the published vertex coordinates."
        ),
        "source": "data/Toroidal-Polyhedra-Realizations.txt (Szilassi, 'On Three "
                  "Classes of Regular Toroids', 2004) -- 5 Csaszar + 2 Szilassi "
                  "= 7 realizations, carried in this repo all along",
        "finding": {
            "szilassi_v1": "5*sqrt(21)/2 (x2) and 5*sqrt(21) (x2) -> 4 of 21 edges",
            "szilassi_v2": "2*sqrt(21) (x2) and 21*sqrt(21)/4 (x2) -> 4 of 21 edges",
            "csaszar_v1_to_v5": "no sqrt(21) in any of the five",
            "pattern": "sqrt(21) is a SZILASSI phenomenon: present in BOTH "
                       "Szilassi realizations, absent from all five Csaszar ones",
            "note": "Szilassi v2's 21*sqrt(21)/4 = 21^{3/2}/4 carries 21 both as "
                    "a coefficient and under the root",
        },
        "per_realization": report,
        "why_279_and_285_missed_it": (
            "Method error, not arithmetic. Pass 279 searched SPECTRA (SRG "
            "eigenvalues, discriminants, group orders) and correctly noted that "
            "the SRG discriminant is 4q^2 -- a perfect square -- so the "
            "collinearity graph is rational throughout. Its rule 'test "
            "discriminants, not squarefree parts' was right but silently assumed "
            "every irrationality in play is SPECTRAL. A polyhedron's edge lengths "
            "are METRIC: square roots of integer quadratic forms in the vertex "
            "coordinates, generating real quadratic fields with no discriminant "
            "in sight. Pass 285 then compounded it by arguing about COUNTS "
            "(21 = C(7,2), Fano flags) and concluding a rational 21 cannot "
            "manufacture sqrt(21) -- true but irrelevant: the sqrt(21) was never "
            "coming from the count, it was in the metric."
        ),
        "what_survives_from_285": (
            "The cyclotomic identity stands: the FN(2,1,0) Koide function is "
            "Q(eps) = Phi_6(eps)/Phi_3(eps), and part18_jungerman_ringel.tex "
            "parameterises the Csaszar torus by Phi_6(q) = q^2-q+1 = 7 at q=3. "
            "What changes is the verdict: sqrt(21) is NOT absent from the "
            "geometry, so the door 285 tried to close is open again."
        ),
        "significance": (
            "eps* = (5 - sqrt 21)/2, the FN parameter on the Koide light cone "
            "(Pass 274), lives in Q(sqrt 21). That field is now known to be "
            "realised in the substrate's own metric data -- specifically in the "
            "Szilassi polyhedron, the dual toroid of Csaszar and the genus-1 rung "
            "of the Jungerman-Ringel ladder that part18 ties to W(3,3). Whether "
            "the two occurrences of Q(sqrt 21) are related is now a live question "
            "rather than a closed one."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
