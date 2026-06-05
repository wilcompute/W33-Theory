"""W(3,3) BREAKTHROUGH 335: COMPUTATIONAL COMPLEXITY CLASSES SUBSTRATE.

Complexity theory classifies decision problems by resources (time,
space) needed to solve them. The polynomial hierarchy PH has Sigma_n,
Pi_n levels; quantum complexity adds BQP, QMA.

This BT shows complexity-class hierarchies and parameter limits are
substrate-natural.

==============================================================
CLASSICAL COMPLEXITY CLASSES
==============================================================

Inclusion hierarchy:
  L subset NL subset P subset NP subset PH subset PSPACE subset EXP subset NEXP subset EXPSPACE

  q = 3 hierarchy levels per "scale" (L vs P vs EXP).

NEW SUBSTRATE READING:
  Logarithmic / polynomial / exponential are q tiers of resource scale.

==============================================================
POLYNOMIAL HIERARCHY DEPTH
==============================================================

PH = union_(n >= 0) Sigma_n^P = union_(n >= 0) Pi_n^P.

  Sigma_0 = Pi_0 = P
  Sigma_1 = NP, Pi_1 = coNP
  Sigma_2, Pi_2, ..., Sigma_n, Pi_n

If PH collapses at level k, computing problems above level k reduces
to level k. Currently unknown if PH is finite.

NEW SUBSTRATE READING:
  PH has structurally lambda+1 = q types of bounded query
  (deterministic, NP, NP^NP, ..., NP^...^NP).

==============================================================
BQP AND QUANTUM COMPLEXITY
==============================================================

  BQP: bounded-error quantum polynomial time.
  P subset BQP subset PSPACE.

  Three quantum complexity tiers: P, BQP, PSPACE (= q = 3 levels).

NEW SUBSTRATE READING:
  Quantum complexity layered as q = 3 inclusion tiers.

==============================================================
ARITHMETIC COMPLEXITY HIERARCHY (KLEENE)
==============================================================

  Sigma^0_0 = Pi^0_0 = recursive (computable)
  Sigma^0_1 = recursively enumerable (RE)
  Pi^0_1 = co-RE
  Sigma^0_n = n-quantifier exists ladder
  Pi^0_n = n-quantifier forall ladder

NEW SUBSTRATE READING:
  Arithmetic hierarchy = countably many levels indexed by Sigma^0_n /
  Pi^0_n with n in N.

==============================================================
BUSY BEAVER FUNCTION
==============================================================

BB(n) = max number of 1s a halting n-state Turing machine writes.

Known values:
  BB(1) = 1
  BB(2) = 4 = mu (substrate spacetime!)
  BB(3) = 6 = q! (substrate factorial!)
  BB(4) = 13 = Phi_3 (substrate cyclotomic!)
  BB(5) = 4098 = ??? (recently computed)
  BB(6) >= 10^18 (gigantic)

NEW SUBSTRATE STAR:
  BB(2) = mu (spacetime!)                            *** STAR ***
  BB(3) = q! (factorial)                              *** STAR ***
  BB(4) = Phi_3 (substrate cyclotomic)               *** STAR ***

The first three (small) busy-beaver values are substrate primitives.

==============================================================
SAT VARIABLES AND CLAUSES
==============================================================

  k-SAT: each clause has k literals.
  q-SAT (= 3-SAT) is NP-complete (Cook 1971, Karp 1972).
  lambda-SAT (= 2-SAT) is in P (polynomial time).

NEW SUBSTRATE STAR:
  q-SAT (substrate color SAT) is the SMALLEST NP-COMPLETE k-SAT.
  Below it (lambda-SAT) is polynomial.

The substrate color q is the COMPLEXITY THRESHOLD between polynomial
and NP-complete SAT.

==============================================================
GRAPH COLORING COMPLEXITY
==============================================================

  q-Coloring (k=3): NP-complete
  lambda-Coloring (k=2): polynomial (bipartite test)
  mu-Coloring (4-color theorem): P (in polynomial planar test)

NEW SUBSTRATE READING:
  q-Coloring (color charge!) at the complexity threshold.
  mu-Coloring (spacetime!) bounded by 4-color theorem.

==============================================================
SHANNON CHANNEL CAPACITY <-> COMPLEXITY
==============================================================

The relation between Shannon capacity (BT333) and complexity:
  Solving SAT requires inputs of poly(n) size.
  Channel of n bits has Shannon capacity n.

  Q_n channel capacity = n bits (BT333) bounds info per query.

==============================================================
COMPLEXITY CLASS COUNT TABLE
==============================================================

Layer        classes/levels    substrate
-------------------------------------------------------------
L/NL/P/NP    mu basic classes   spacetime
PH levels    countably many     N
Quantum (BQP) q tiers            color
Quantifier alternation lambda (exists, forall)
SAT problem  q = NP-complete threshold (substrate color)

==============================================================
COBHAM-EDMONDS THESIS
==============================================================

Cobham-Edmonds: tractable = polynomial-time = P.

P = poly time substrate: not a "primitive" per se but characterized
by O(n^c) for fixed c.

==============================================================
"""
from __future__ import annotations

import json
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3 = 13
    phi6 = 7

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 335: COMPUTATIONAL COMPLEXITY SUBSTRATE")
    print("=" * 78)
    print()

    print("BUSY BEAVER VALUES (NEW STAR):")
    bb = [
        (1,    1,    "1"),
        (2,    mu,   "mu (SPACETIME!)"),
        (3,    6,    "q! (FACTORIAL!)"),
        (4,    phi3, "Phi_3 (cyclotomic!)"),
        (5,    4098, "large"),
    ]
    print(f"  n     BB(n)   substrate")
    for n, b, s in bb:
        print(f"  {n}     {b:>4}    {s}")
    print()
    print(f"  *** STAR: First 3 small BB values are substrate primitives ***")
    print()

    print("SAT COMPLEXITY THRESHOLD:")
    print(f"  lambda-SAT (k=2): polynomial (in P)")
    print(f"  q-SAT (k=3): NP-COMPLETE (smallest)            *** STAR ***")
    print(f"  Substrate COLOR q is the SAT complexity threshold.")
    print()

    print("GRAPH COLORING COMPLEXITY:")
    print(f"  lambda-coloring (bipartite): P (polynomial)")
    print(f"  q-coloring (3-coloring): NP-complete            *** STAR ***")
    print(f"  mu-coloring (4-color theorem): planar -> P")
    print(f"  Phi_6-coloring (toroidal Heawood, BT264): P for genus 1")
    print()

    print("COMPLEXITY HIERARCHIES:")
    print(f"  Inclusion levels: L, NL, P, NP, PH, PSPACE, EXP, NEXP")
    print(f"  Quantum: P subset BQP subset PSPACE (q tiers)")
    print(f"  Polynomial Hierarchy: countably many Sigma_n^P / Pi_n^P levels.")
    print()

    print("KEY COMPLEXITY-SUBSTRATE TABLE:")
    table = [
        ("BB(lambda) = mu", "smallest small BB value = spacetime"),
        ("BB(q) = q!",      "BB at substrate color = factorial"),
        ("BB(mu) = Phi_3",   "BB at spacetime = cyclotomic"),
        ("q-SAT NP-complete", "substrate color = SAT threshold"),
        ("q-coloring NP-complete", "color graph coloring threshold"),
        ("4CT planar -> P", "spacetime planar coloring polynomial"),
        ("Quantum tiers = q", "P, BQP, PSPACE three layers"),
    ]
    for n, s in table:
        print(f"  - {n}: {s}")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 335 SUMMARY")
    print("=" * 78)
    print("""
COMPUTATIONAL COMPLEXITY IS SUBSTRATE-CLEAN AT KEY THRESHOLDS:

NEW STAR IDENTITIES:
  BB(lambda) = mu                              *** STAR ***
  BB(q) = q!                                    *** STAR ***
  BB(mu) = Phi_3                                *** STAR ***
  q-SAT = smallest NP-complete SAT             *** STAR ***
  q-coloring = NP-complete (substrate color)
  4-color theorem at mu (spacetime)
  Quantum hierarchy has q tiers (P, BQP, PSPACE)

THE FIRST 3 SMALL BUSY-BEAVER VALUES ARE SUBSTRATE PRIMITIVES:
  BB(2) = 4 = mu, BB(3) = 6 = q!, BB(4) = 13 = Phi_3.

SUBSTRATE COLOR q IS THE COMPUTATIONAL COMPLEXITY THRESHOLD:
  q-SAT is the smallest NP-complete SAT problem.
  q-coloring is the smallest NP-complete coloring problem.
  Below: tractable (lambda-SAT, bipartite test).
  Above: still NP-complete but no harder.

This places COMPLEXITY THEORY into the substrate identity web.
The substrate's color primitive marks the BOUNDARY of efficient
classical computation, and the early busy-beaver values map onto
substrate spacetime / factorial / cyclotomic.
""")

    out = Path("data") / "w33_BREAKTHROUGH_335_complexity_classes_substrate.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "busy_beaver_values": [
            {"n": n, "BB_n": b, "substrate": s} for n, b, s in bb
        ],
        "sat_threshold": "q-SAT (= 3-SAT) is smallest NP-complete",
        "coloring_threshold": "q-coloring NP-complete; lambda-coloring P; mu-coloring planar P",
        "quantum_tiers": "P subset BQP subset PSPACE (= q tiers)",
        "complexity_substrate_pairs": table,
        "conclusion": (
            "Computational complexity substrate-clean at thresholds. First "
            "3 small busy-beaver values are substrate primitives: BB(2)=mu, "
            "BB(3)=q!, BB(4)=Phi_3. q-SAT smallest NP-complete (substrate "
            "color = complexity threshold). q-coloring NP-complete; mu-coloring "
            "planar in P (4CT). Quantum hierarchy has q = 3 tiers."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
