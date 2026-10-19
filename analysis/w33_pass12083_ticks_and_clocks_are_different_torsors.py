"""Pass 12083: ticks and clocks are two different Z3-torsors over the forty events -- no enlargement of the symmetry
identifies them (Claude track; completes 12072, uses 12080).

Over each event p there are three ticks (Pauli labels k in Z3) and three clocks (E8 involutions). Both are Z3-torsors,
with different structure:
  * ticks: the label shifts are the Pauli translations W_r, shifting labels at p by omega(r,p) -- event-dependent,
    affine, the normal F_3^4 of ASp(4,3); the point stabiliser of the linear Sp(4,3) fixes a label (12072).
  * clocks: the shifts are the Eisenstein unit omega = C^10, central in 3 x Sp(4,3), 3-cycling the clocks at EVERY event
    simultaneously (12080); the point stabiliser of Sp(4,3) acts on the three clocks at p through SL(2,3)/Q8 = Z3
    transitively, fixing none.
Exact obstructions to any identification:
  1. Sp(4,3) is perfect (GAP), so 3 x Sp(4,3) has a unique complement class to its centre: no 'twisted' copy of Sp(4,3)
     acting on clocks with a fixed clock at a point.
  2. |ASp(4,3)| = 4199040 does not divide |W(E8)| = 2^14 3^5 5^2 7 (3-parts 3^8 versus 3^5): the affine group of the ticks
     does not embed in W(E8), so the Pauli translations cannot act on clocks through E8.
  3. Restricted to any copy of Sp(4,3), the tick set is 40 + 80 and the clock set is 120 (12072), so no group containing
     Sp(4,3) acting on both admits an equivariant bijection.
Reading. The clock at an event is a cube root of unity in the Eisenstein structure of E8; the tick label is a Pauli
phase of the two-qutrit Weyl algebra. They are counted alike (3 per event, 120 in all) but carry inequivalent symmetry.
"""

import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12052_real_forms_on_forty_points import build  # noqa: E402
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402

OUT = ROOT / "data" / "w33_pass12083_ticks_and_clocks_are_different_torsors.json"
REC = ROOT / "analysis" / "search_drivers_12083" / "facts.out"


def main():
    checks, res = {}, {}
    A = re.sub(r"\s+", " ", REC.read_text())
    checks["Sp(4,3) is perfect; 3 x Sp(4,3) has one complement class to its centre (GAP)"] = (
        "Sp(4,3) perfect: true" in A and "complement classes of the central 3 in 3 x Sp(4,3): 1" in A)
    W = 696729600
    checks["|W(E8)| = 2^14 3^5 5^2 7 and |ASp(4,3)| = 4199040 does not divide it"] = (
        W == 2 ** 14 * 3 ** 5 * 5 ** 2 * 7 and 3 ** 4 * 51840 == 4199040 and W % 4199040 != 0 and "divides |W(E8)|: false" in A)
    R, C, fib, refl, perm = build()
    Adj, invs, tick, _ = setup()
    Wp = perm(np.linalg.matrix_power(C, 10))
    Pc = np.array([s for k, s in invs if k == "clock"])
    cpt = np.array([next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == {y for y in range(40) if not s[fib[y]].any()}) for s in Pc])
    om = all(not np.array_equal(Pc[i][Wp], Pc[i]) and any(np.array_equal(Pc[i][Wp], Pc[j]) and cpt[j] == cpt[i] for j in range(120)) for i in range(120))
    checks["omega acts trivially on events and 3-cycles the clocks at every event"] = bool(
        om and all(set(Wp[fib[x]]) == set(fib[x]) for x in range(40)))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
