"""Pass 7204 -- what alpha(W(3,q)) counts in quantum information, and Clifford rigidity.

PRIOR ART FIRST. analysis/w33_pass5351_5352_hoffman_pauli_latin_symplectic_spread.py already
carries the dictionary at q=2 -- "commuting (totally isotropic) or anticommuting
(nonisotropic) Pauli triples" -- and correctly disclaims it as finite group/code geometry
rather than a physical qubit claim. That disclaimer is kept here.

WHAT IS ADDED. The dictionary extends verbatim to odd q, and under it alpha is not an
abstract extremal number:

    points of W(3,q)      <->  Pauli classes on TWO qudits of dimension q
                               (X^a Z^b tensor X^c Z^d, taken up to scalar, so a
                               projective point is the cyclic group a Pauli generates)
    collinear (B = 0)     <->  the two Paulis COMMUTE
    partial ovoid         <->  a pairwise NON-COMMUTING family
    Sp(4,q)               <->  the Clifford group modulo Paulis

so  alpha(W(3,q))  =  the largest family of Pauli classes on two qudits that pairwise
fail to commute. The computed values read:

    q=2:  5     q=3:  7     q=5:  18     q=7:  33     q=9:  51 or 52

THE q=2 ENTRY IS THE CONTROL, and it is checkable against textbook quantum information: the
maximum pairwise-ANTIcommuting set of Pauli operators on n qubits is 2n+1, so 5 for n=2. This
script builds the 4x4 Pauli matrices explicitly, finds the maximum pairwise-anticommuting
family by exhaustive search, and checks it equals alpha(W(3,2)) computed from the geometry.
If those disagree the dictionary is wrong and nothing below stands.

THE CONSEQUENCE, which is the point. Sp(4,q) is the Clifford group modulo Paulis, so the
Pass 7199/7203 stabilizer bounds say these maximal families are CLIFFORD-RIGID: at q=7 and
q=9 the subgroup of Clifford operations fixing the family setwise has order at most 2. At
q=3 it is exactly 18 (C3 x C6, Pass 7203). Rigidity switches on with q.

NO PHYSICAL CLAIM IS MADE. This is the finite geometry of the Weyl-Heisenberg commutation
form, stated in its quantum-information vocabulary.

    py -3 analysis/w33_pass7204_pauli_reading_of_alpha.py
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7187_q9_orbit_attack import Field, geometry  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main() -> int:
    print("=" * 78)
    print("Pass 7204 -- alpha(W(3,q)) as a Pauli count, with a matrix-level control")
    print("=" * 78)

    import numpy as np

    I2 = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    single = {"I": I2, "X": X, "Y": Y, "Z": Z}
    paulis = {}
    for a, A in single.items():
        for b, Bm in single.items():
            if a == "I" and b == "I":
                continue
            paulis[a + b] = np.kron(A, Bm)
    names = sorted(paulis)
    print(f"\n  CONTROL AT q=2: built {len(names)} non-identity two-qubit Paulis "
          f"(expect 15)")

    def anticommute(u, v):
        A, Bm = paulis[u], paulis[v]
        return np.allclose(A @ Bm, -(Bm @ A))

    anti = {(u, v): anticommute(u, v)
            for u, v in itertools.combinations(names, 2)}
    best = []
    for r in range(1, 8):
        found = None
        for combo in itertools.combinations(names, r):
            if all(anti[(u, v)] for u, v in itertools.combinations(combo, 2)):
                found = combo
                break
        if found is None:
            break
        best = found
    print(f"    max pairwise-ANTICOMMUTING family: {len(best)}  {best}")
    print(f"    textbook value for n qubits is 2n+1 = {2 * 2 + 1}   "
          f"{'MATCHES' if len(best) == 5 else 'MISMATCH'}")

    F = Field(2) if 2 in (2,) else None
    # geometry side at q=2
    import importlib
    m = importlib.import_module("w33_pass7187_q9_orbit_attack")

    class F2:
        q = 2
        add = [[0, 1], [1, 0]]
        mul = [[0, 0], [0, 1]]
        neg = [0, 1]
        inv = {1: 1}

    P, idx, adj, B = geometry(F2())
    n = len(P)
    # maximum independent set in the collinearity graph, exhaustively (15 points)
    bestgeo = 0
    for r in range(1, 9):
        hit = False
        for combo in itertools.combinations(range(n), r):
            if all(B(P[a], P[b]) != 0 for a, b in itertools.combinations(combo, 2)):
                hit = True
                break
        if not hit:
            break
        bestgeo = r
    print(f"    alpha(W(3,2)) from the geometry: {bestgeo}   ({n} points)")
    agree = (bestgeo == len(best) == 5)
    print(f"    DICTIONARY {'CONFIRMED' if agree else 'REFUTED'}: "
          f"matrix answer {len(best)}, geometry answer {bestgeo}")

    if not agree:
        print("""
    THE DICTIONARY FAILED ITS CONTROL. Nothing below is asserted.""")
        return 1

    print("\n  THE READING, now that the control holds\n")
    print(f"    {'q':>3s}  {'alpha':>8s}  {'= max pairwise non-commuting Pauli classes':>44s}")
    for q, a in ((2, 5), (3, 7), (5, 18), (7, 33), (9, "51 or 52")):
        print(f"    {q:3d}  {str(a):>8s}  {'on two qudits of dimension ' + str(q):>44s}")

    print("""
  CLIFFORD RIGIDITY. Sp(4,q) is the Clifford group modulo the Paulis, so a stabilizer in
  Sp(4,q) is exactly the group of Clifford operations fixing the family setwise:

      q=3   |Stab| = 18  (C3 x C6)   EXACT, by enumerating Sp(4,3) -- Pass 7203
      q=7   |Stab| <= 2               Pass 7199
      q=9   |Stab| <= 2               Pass 7199, for the 51-set

  So the maximal non-commuting Pauli families are Clifford-rigid for q >= 7 and highly
  symmetric at q=3. Whatever selects such a family cannot be a Clifford symmetry principle,
  because for q >= 7 there is essentially no Clifford symmetry left to do the selecting.

  NO PHYSICAL CLAIM IS MADE, and the q=2 prior art's disclaimer is inherited: this is the
  finite geometry of the Weyl-Heisenberg commutation form in its QI vocabulary. Note also
  that q=9 means GF(9), not Z/9 -- the qudit there is the Galois qudit, not a mod-9 one.""")

    out = {
        "boundary": ("a translation, not a new computation: alpha(W(3,q)) equals the maximum "
                     "pairwise non-commuting family of Pauli classes on two qudits of "
                     "dimension q. Controlled at q=2 against the textbook 2n+1 using explicit "
                     "matrices. NO physical claim; inherits the q=2 prior art's disclaimer"),
        "prior_art": ("analysis/w33_pass5351_5352_hoffman_pauli_latin_symplectic_spread.py "
                      "carries the commuting/anticommuting dictionary at q=2"),
        "control_q2": {"matrix_answer": len(best), "geometry_answer": bestgeo,
                       "textbook_2n_plus_1": 5, "agree": agree, "family": list(best)},
        "dictionary": {"point": "Pauli class on two qudits, up to scalar",
                       "collinear": "the two Paulis commute",
                       "partial_ovoid": "pairwise non-commuting family",
                       "Sp(4,q)": "Clifford group modulo Paulis"},
        "values": {"q=2": 5, "q=3": 7, "q=5": 18, "q=7": 33, "q=9": "51 or 52"},
        "clifford_rigidity": {"q=3": {"stab": 18, "structure": "C3 x C6", "status": "exact"},
                              "q=7": {"stab": "<= 2", "status": "upper bound"},
                              "q=9": {"stab": "<= 2", "status": "upper bound, 51-set"}},
        "caveat_q9": "GF(9), not Z/9 -- the Galois qudit",
    }
    fp = ROOT / "data" / "PART_W33_PASS7204_PAULI_READING.json"
    fp.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
