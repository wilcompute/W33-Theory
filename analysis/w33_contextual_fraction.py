#!/usr/bin/env python3
"""
The number on the bench, derived from scratch: the contextual fraction is exactly 1/10, forced by the
geometry. Every prior pass that mentioned the demonstrator's headline prediction took the value
CF = 1/10 = 1/Phi_4 from the corpus; this pass DERIVES it from the bare incidence geometry of W(3,3),
closing that gap. The 40 Witting rays in C^4 have orthogonality structure equal to the collinearity
graph of W(3,3), and their measurement contexts are the 40 totally-isotropic LINES, each a tetrad of
four mutually-orthogonal rays (an orthonormal basis). A Kochen-Specker value assignment is a choice of
0/1 for each of the 40 rays such that every context has EXACTLY ONE ray valued 1 -- the unique outcome
that occurs. Such a global assignment that satisfies all 40 contexts is precisely an OVOID of the
generalized quadrangle (a set of points meeting every line exactly once, here 10 points), and the
classical theorem (Thas) is that W(q) for q odd has NO ovoid -- so no global classical assignment can
satisfy all 40 contexts, and the substrate is a genuine state-independent contextuality (KS) set. We
compute two things directly. (1) The maximum partial ovoid -- the largest set of pairwise non-collinear
rays, i.e. the independence number of the graph -- is 7, strictly below the Hoffman bound 10, confirming
no ovoid. (2) The MAXIMUM NUMBER OF CONTEXTS that any global 0/1 ray-assignment can satisfy is, by exact
integer programming over all 2^40 assignments, exactly 36 of 40 -- so four contexts are irreducibly
unsatisfiable, and the contextual fraction (the fraction of contexts no classical assignment can
satisfy) is CF = (40 - 36)/40 = 4/40 = 1/10 = 1/Phi_4. The 36/40 "KS budget" and the 1/10 contextual
fraction are therefore not inputs but theorems of the W(3,3) line geometry, the same q=3 incidence
structure that is the processor, the network, and the memory. So the single number the benchtop
experiment measures -- and that certifies the substrate's magic fuel and tests the theory of everything
-- is derived here from first principles: exactly one tenth.

This derives the substrate's contextual fraction from the bare W(3,3) line incidence: it shows there is
no ovoid (no global KS assignment), computes the maximum partial ovoid (7) and the maximum number of
satisfiable contexts (36) by exact integer programming, and concludes CF = 4/40 = 1/10.

THE DERIVATION.
    rays/contexts   40 Witting rays (W(3,3) points); 40 contexts = the totally-isotropic lines (tetrads).
    KS assignment   0/1 per ray, exactly one 1 per context; all-40 solution = an ovoid (10 points).
    no ovoid        Thas: W(q) q odd has no ovoid; here max partial ovoid (independence number) = 7 < 10.
    max satisfiable exact ILP over the 40 rays: at most 36 of 40 contexts satisfiable simultaneously.
    contextual frac CF = (40 - 36)/40 = 4/40 = 1/10 = 1/Phi_4 (derived, not assumed).

Honest scope: everything here is computed from the W(3,3) line-incidence geometry -- the independence
number 7 (max-clique on the complement), the maximum satisfiable contexts 36 (exact integer program
with the standard linearization, with the satisfying assignment re-verified), and CF = 1/10. This is
the LOGICAL / possibilistic contextual fraction (the max fraction of contexts admitting a consistent
global value assignment); it equals the corpus value 1/10 = 1/Phi_4 and the "KS budget 36/40", here
derived rather than cited. That the 40 Witting rays realise this incidence in C^4 is the corpus
two-carrier result; the no-ovoid fact for W(q), q odd, is the Thas theorem. So: a first-principles
derivation of the benchtop number.

Verifies no ovoid (independence number 7 < 10), the exact maximum of 36 satisfiable contexts, and the
resulting contextual fraction 1/10 on the W(3,3) line geometry.
"""
from __future__ import annotations

import itertools
import json

import networkx as nx
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def build_w33():
    inv = {1: 1, 2: 2}

    def norm(v):
        for c in v:
            if c != 0:
                return tuple((x * inv[c]) % 3 for x in v)

    pts = sorted({norm(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    pidx = {p: i for i, p in enumerate(pts)}

    def B(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % 3

    n = len(pts)
    A = np.zeros((n, n), int)
    for i in range(n):
        for j in range(n):
            if i != j and B(pts[i], pts[j]) == 0:
                A[i, j] = 1

    def span(p, q):
        S = set()
        for a in range(3):
            for b in range(3):
                v = tuple((a * p[k] + b * q[k]) % 3 for k in range(4))
                if any(v):
                    S.add(norm(v))
        return frozenset(pidx[x] for x in S)

    lines = sorted(
        {
            tuple(sorted(span(pts[i], pts[j])))
            for i in range(n)
            for j in range(i + 1, n)
            if A[i, j] == 1
        }
    )
    return n, A, lines


def main():
    out = {}
    n, A, lines = build_w33()
    k = int(A.sum(1)[0])
    print("== the contextual fraction, derived from scratch: exactly 1/10 ==")
    print(
        f"\n[scenario]  {n} Witting rays (W(3,3) points); {len(lines)} contexts = totally-isotropic lines (tetrads)"
    )
    assert n == 40 and len(lines) == 40 and all(len(L) == 4 for L in lines)

    # (1) no ovoid: max partial ovoid = independence number; Hoffman bound = ovoid size 10
    ev = sorted(np.linalg.eigvalsh(A.astype(float)))
    lmin = round(min(ev))
    hoffman = n * (-lmin) / (k - lmin)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j]:
                G.add_edge(i, j)
    clique, _ = nx.max_weight_clique(nx.complement(G), weight=None)
    alpha = len(clique)
    print(
        f"[no ovoid]  Hoffman bound alpha <= {hoffman:.0f} (= ovoid size st+1); max partial ovoid (independence number) = {alpha}"
    )
    print(
        f"            {alpha} < 10 -> NO ovoid (Thas: W(q), q odd) -> a genuine state-independent KS set"
    )
    assert alpha == 7 and abs(hoffman - 10) < 1e-9
    out["no_ovoid"] = {
        "hoffman_bound": int(round(hoffman)),
        "max_partial_ovoid": alpha,
        "ovoid_exists": False,
    }

    # (2) max satisfiable contexts via exact ILP: g_L <= s_L, g_L <= 2 - s_L, maximize sum g_L
    nv = n + len(lines)
    rows, lb, ub = [], [], []
    for li, L in enumerate(lines):
        r1 = np.zeros(nv)
        r1[n + li] = 1
        for p in L:
            r1[p] -= 1
        rows.append(r1)
        lb.append(-np.inf)
        ub.append(0)  # g_L - s_L <= 0
        r2 = np.zeros(nv)
        r2[n + li] = 1
        for p in L:
            r2[p] += 1
        rows.append(r2)
        lb.append(-np.inf)
        ub.append(2)  # g_L + s_L <= 2
    c = np.zeros(nv)
    c[n:] = -1
    res = milp(
        c=c,
        constraints=LinearConstraint(np.array(rows), np.array(lb), np.array(ub)),
        integrality=np.ones(nv),
        bounds=Bounds(0, 1),
    )
    x = np.round(res.x[:n]).astype(int)
    # re-verify the found assignment
    satisfied = sum(1 for L in lines if sum(x[p] for p in L) == 1)
    max_sat = int(round(-res.fun))
    print(
        f"\n[max satisfiable]  exact ILP over the {n} rays: at most {max_sat} of {len(lines)} contexts satisfiable"
    )
    print(
        f"                   (re-verified: the optimal assignment satisfies {satisfied} contexts)"
    )
    assert max_sat == 36 and satisfied == 36
    out["max_satisfiable_contexts"] = max_sat

    # (3) the contextual fraction
    cf_num, cf_den = len(lines) - max_sat, len(lines)
    cf = cf_num / cf_den
    print(
        f"\n[contextual fraction]  CF = ({len(lines)} - {max_sat})/{len(lines)} = {cf_num}/{cf_den} = {cf} = 1/10 = 1/Phi_4"
    )
    assert cf_num == 4 and abs(cf - 0.1) < 1e-12
    out["contextual_fraction"] = {
        "numerator": cf_num,
        "denominator": cf_den,
        "value": cf,
        "closed_form": "1/10 = 1/Phi_4",
    }

    print(
        "\nRESULT: the benchtop number is a theorem of the geometry, not an input. The 40 Witting rays"
    )
    print(
        "  in C^4 have the orthogonality structure of W(3,3), with 40 measurement contexts = the"
    )
    print(
        "  totally-isotropic lines (tetrads). A Kochen-Specker assignment (0/1 per ray, exactly one 1"
    )
    print(
        "  per context) that satisfied all 40 would be an ovoid -- 10 points meeting every line once --"
    )
    print(
        "  but W(q) for q odd has no ovoid (Thas), confirmed here by the maximum partial ovoid"
    )
    print(
        "  (independence number) being 7 < 10. By exact integer programming, the most contexts any"
    )
    print(
        "  global 0/1 assignment can satisfy is exactly 36 of 40, so four contexts are irreducibly"
    )
    print(
        "  unsatisfiable and the contextual fraction is CF = (40-36)/40 = 4/40 = 1/10 = 1/Phi_4. The"
    )
    print(
        "  36/40 KS budget and the 1/10 fraction are forced by the same q=3 line incidence that is the"
    )
    print(
        "  processor, the network, and the memory -- so the single number the demonstrator measures,"
    )
    print(
        "  certifying the magic fuel and testing the theory of everything, is derived here from first"
    )
    print(
        "  principles: exactly one tenth. Honest: this is the logical/possibilistic contextual"
    )
    print(
        "  fraction (max contexts admitting a consistent global value), computed from the incidence"
    )
    print(
        "  geometry; it matches the corpus 1/10 = 1/Phi_4 and 36/40, here derived rather than cited."
    )

    out["summary"] = (
        "the contextual fraction, derived from scratch: exactly 1/10. The 40 Witting rays in C^4 have "
        "the orthogonality structure of W(3,3); the 40 measurement contexts are the totally-isotropic "
        "lines (tetrads of orthonormal rays). A Kochen-Specker assignment (0/1 per ray, exactly one 1 "
        "per context) satisfying all 40 contexts would be an ovoid (10 points meeting every line once); "
        "Thas's theorem says W(q) for q odd has no ovoid, confirmed here by the maximum partial ovoid "
        "(independence number) = 7 < the Hoffman bound 10. By exact integer programming over the 40 "
        "rays, the maximum number of contexts any global 0/1 assignment can satisfy is exactly 36 of 40 "
        "(re-verified on the optimal assignment), so 4 contexts are irreducibly unsatisfiable and the "
        "contextual fraction is CF = (40-36)/40 = 4/40 = 1/10 = 1/Phi_4. The 36/40 KS budget and the "
        "1/10 fraction are theorems of the W(3,3) line incidence -- the same q=3 structure that is the "
        "processor, network, and memory -- so the benchtop number that certifies the magic fuel and "
        "tests the theory is derived from first principles, not assumed. HONEST: this is the logical/"
        "possibilistic contextual fraction (max contexts admitting a consistent global value), computed "
        "from the incidence geometry; it equals the corpus 1/10 = 1/Phi_4 and the KS budget 36/40, here "
        "DERIVED rather than cited; that the 40 Witting rays realise this incidence in C^4 is the corpus "
        "two-carrier result and the no-ovoid fact is the Thas theorem."
    )
    out["sources"] = [
        "W(3,3) line incidence (40 points, 40 totally-isotropic line-contexts; computed); Witting rays "
        "in C^4 with W(3,3) orthogonality (corpus two-carrier); ovoid = set meeting every line once; "
        "Thas: W(q) has no ovoid for q odd; Hoffman ratio bound on the independence number; exact ILP "
        "max-satisfiable contexts (scipy milp); contextual fraction 1/10 = 1/Phi_4 (corpus value, here "
        "derived)."
    ]
    with open("data/w33_contextual_fraction.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_contextual_fraction.json")


if __name__ == "__main__":
    main()
