#!/usr/bin/env python3
"""Pass 298: the ladder of FORCED spectral fields -- and the substrate's own is Q(sqrt6).

Pass 297 established that the oscillator has a genuine forced irrationality --
the Heawood Laplacian's 3 +- sqrt2 -- while Pass 293 showed the sqrt(21) of the
Szilassi edge lengths is a coordinate choice.  So the honest instruction was
"chase sqrt(2), not sqrt(21)".  Chasing it deflates it, and finds the real one.

WHAT sqrt(2) ACTUALLY IS.  The Heawood graph is the Levi (point-line incidence)
graph of the Fano plane PG(2,2).  Computed here at q = 2,3,5, the Levi graph of
PG(2,q) has adjacency spectrum
        +-(q+1),  +-sqrt(q),
so its field is Q(sqrt q).  The clock's sqrt(2) is therefore nothing mysterious:
it is sqrt(q) for the Fano plane, whose order is q = 2.  It is not a universal
constant, it is the order of a particular small plane.

THE SUBSTRATE'S OWN FIELD IS DIFFERENT.  W(3,q) is a generalized QUADRANGLE, not
a plane.  Computed here at q = 2,3,4,5, the Levi graph of GQ(q,q) has spectrum
        +-(q+1),  +-sqrt(2q),  0,
so its field is Q(sqrt(2q)).  At the substrate's own order q = 3 that is
        Q(sqrt 6),
not Q(sqrt 2).  (At q = 2 the doily gives sqrt(4) = 2 -- RATIONAL; at q = 4 it
gives sqrt(8) -> Q(sqrt 2).)

THE LADDER OF FORCED FIELDS.
    tetrahedron K4 (genus 0)          -> Q            (rational, Pass 295)
    doily W(3,2) Levi                 -> Q            (sqrt 4 = 2)
    Fano/Heawood clock  PG(2,2) Levi  -> Q(sqrt 2)    (= sqrt q, q=2)
    substrate W(3,3) Levi             -> Q(sqrt 6)    (= sqrt 2q, q=3)
    Koide eps* = (5-sqrt21)/2         -> Q(sqrt 21)   -- matches NEITHER

CONSEQUENCE.  bt1654_heawood_clock_homology.py already recorded the honest
boundary: the W(3,3) Levi graph has girth 8 and no 6-cycles, so the Heawood clock
is NOT a Levi subgraph of the machine but a separate module coupled to it.  This
pass gives that boundary a field-theoretic form: the coupled clock lives in
Q(sqrt 2) because its order is 2, while the machine itself lives in Q(sqrt 6)
because its order is 3.  And Koide's Q(sqrt 21) is neither, which closes the
"chase sqrt(2)" route as cleanly as Pass 293 closed the sqrt(21) one.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass224_shadow_code_tower import isotropic_lines, pg3_points
from analysis.w33_pass232_even_q_sister_tower import (
    GF, isotropic_lines_gf, pg3_points_gf)

OUT = ROOT / "data" / "w33_pass298_forced_field_ladder.json"


def squarefree(n):
    out = 1
    for p, e in sp.factorint(int(n)).items():
        if e % 2:
            out *= p
    return int(out)


def levi_PG2(q):
    pts, seen = [], set()
    for a in range(q):
        for b in range(q):
            for c in range(q):
                if (a, b, c) == (0, 0, 0):
                    continue
                v = (a, b, c)
                lead = next(x for x in v if x)
                inv = pow(lead, q - 2, q)
                nv = tuple((x * inv) % q for x in v)
                if nv not in seen:
                    seen.add(nv)
                    pts.append(nv)
    n = len(pts)
    A = np.zeros((2 * n, 2 * n), int)
    for i, p in enumerate(pts):
        for j, L in enumerate(pts):
            if sum(p[k] * L[k] for k in range(3)) % q == 0:
                A[i, n + j] = A[n + j, i] = 1
    return A, n


def levi_GQ(q, even=False):
    if even:
        gf = GF({2: 1, 4: 2}[q])
        pts = pg3_points_gf(gf)
        lines = isotropic_lines_gf(gf, pts)
    else:
        pts = pg3_points(q)
        lines = isotropic_lines(pts, q)
    n, m = len(pts), len(lines)
    A = np.zeros((n + m, n + m), int)
    for j, L in enumerate(lines):
        for p in L:
            A[p, n + j] = A[n + j, p] = 1
    return A, n, m


def main():
    checks = {}

    # ---- Levi(PG(2,q)) : eigenvalues +-(q+1), +-sqrt(q)
    plane = {}
    for q in (2, 3, 5):
        A, n = levi_PG2(q)
        ev = sorted({round(float(x), 6) for x in np.linalg.eigvalsh(A)})
        plane[str(q)] = {"vertices": 2 * n, "edges": int(A.sum() // 2),
                         "distinct_eigenvalues": ev,
                         "predicted": [-(q + 1), -math.sqrt(q), math.sqrt(q), q + 1],
                         "field": f"Q(sqrt{squarefree(q)})" if squarefree(q) != 1 else "Q"}
        checks[f"PG2_{q}_has_sqrt_q"] = any(
            abs(x - math.sqrt(q)) < 1e-6 for x in ev)
        checks[f"PG2_{q}_has_q_plus_1"] = any(abs(x - (q + 1)) < 1e-6 for x in ev)
    checks["heawood_field_is_Q_sqrt2"] = plane["2"]["field"] == "Q(sqrt2)"

    # ---- Levi(GQ(q,q)) : eigenvalues +-(q+1), +-sqrt(2q), 0
    quad = {}
    for q, even in ((2, True), (3, False), (4, True), (5, False)):
        A, n, m = levi_GQ(q, even)
        ev = sorted({round(float(x), 6) for x in np.linalg.eigvalsh(A)})
        sf = squarefree(2 * q)
        quad[str(q)] = {"vertices": n + m, "edges": int(A.sum() // 2),
                        "distinct_eigenvalues": ev,
                        "sqrt_2q": math.sqrt(2 * q), "squarefree_2q": sf,
                        "field": f"Q(sqrt{sf})" if sf != 1 else "Q (rational)"}
        checks[f"GQ_{q}_has_sqrt_2q"] = any(
            abs(x - math.sqrt(2 * q)) < 1e-6 for x in ev)
        checks[f"GQ_{q}_has_q_plus_1"] = any(abs(x - (q + 1)) < 1e-6 for x in ev)
    checks["substrate_W33_field_is_Q_sqrt6"] = quad["3"]["field"] == "Q(sqrt6)"
    checks["doily_levi_is_rational"] = quad["2"]["field"] == "Q (rational)"
    checks["substrate_field_is_NOT_sqrt2"] = quad["3"]["squarefree_2q"] != 2

    # ---- Koide's field matches neither
    checks["koide_field_is_21"] = squarefree(21) == 21
    checks["koide_not_sqrt2"] = squarefree(21) != 2
    checks["koide_not_sqrt6"] = squarefree(21) != 6

    ladder = {
        "tetrahedron K4 (genus 0)": "Q  (equilateral; Pass 295)",
        "doily W(3,2) Levi": quad["2"]["field"],
        "Fano/Heawood clock PG(2,2) Levi": plane["2"]["field"],
        "substrate W(3,3) Levi": quad["3"]["field"],
        "Koide eps* = (5-sqrt21)/2": "Q(sqrt21)  -- matches NEITHER",
    }

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass298.forced_field_ladder.v1",
        "status": "PASS" if all_pass else "FAIL",
        "what_sqrt2_actually_is": (
            "The Heawood graph is the Levi graph of the Fano plane PG(2,2). "
            "Computed at q = 2,3,5, Levi(PG(2,q)) has spectrum +-(q+1), +-sqrt(q), "
            "so its field is Q(sqrt q). The clock's sqrt(2) is therefore just "
            "sqrt(q) for a plane of order 2 -- not a universal constant, but the "
            "order of one particular small plane."
        ),
        "the_substrate_has_a_DIFFERENT_field": (
            "W(3,q) is a generalized QUADRANGLE, not a plane. Computed at "
            "q = 2,3,4,5, Levi(GQ(q,q)) has spectrum +-(q+1), +-sqrt(2q), 0, so "
            "its field is Q(sqrt(2q)). At the substrate's own order q = 3 that is "
            "Q(sqrt 6) -- NOT Q(sqrt 2). (The doily q=2 gives sqrt4 = 2, "
            "rational; q=4 gives sqrt8 -> Q(sqrt2).)"
        ),
        "projective_planes": plane,
        "generalized_quadrangles": quad,
        "the_forced_field_ladder": ladder,
        "consequence": (
            "bt1654_heawood_clock_homology.py already recorded the honest "
            "boundary -- the W(3,3) Levi graph has girth 8 and no 6-cycles, so "
            "the Heawood clock is NOT a Levi subgraph of the machine but a "
            "separate coupled module. This pass gives that boundary a "
            "field-theoretic form: the coupled clock lives in Q(sqrt 2) because "
            "its order is 2; the machine lives in Q(sqrt 6) because its order is "
            "3. And Koide's Q(sqrt 21) is neither -- so the 'chase sqrt(2)' route "
            "closes as cleanly as Pass 293 closed the sqrt(21) one. Three forced "
            "fields are now on the table (Q, Q(sqrt2), Q(sqrt6)) and the Koide "
            "constant sits in none of them."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
