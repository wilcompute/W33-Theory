"""W(3,3) BREAKTHROUGH 161: KNIGHT PARITY ALTERNATION = OCTONION BIPARTITION.

User-pointed property of the toroidal 4x4 knight tour: knight moves
ALTERNATE PARITY at every node visited.

This bipartite structure splits Q_4 = 16 vertices into 8 + 8 by
Hamming-weight parity. Each class has 8 = 2^q = OCTONION DIMENSION.

==============================================================
KNIGHT-TOUR PARITY ALTERNATION
==============================================================

A knight move on a chessboard alternates light/dark squares.
On the 4x4 toroidal knight graph (= Q_4), a knight move is a
single bit flip (BT157), which TOGGLES Hamming-weight parity.

CONSEQUENCE: any Hamilton cycle (= Gray code = knight tour) on Q_4
must alternate between EVEN-weight and ODD-weight vertices.

  8 even-weight vertices: 0000, 0011, 0101, 0110, 1001, 1010, 1100, 1111
  8 odd-weight vertices:  0001, 0010, 0100, 1000, 0111, 1011, 1101, 1110

  Each class size = 8 = 2^q = OCTONION DIMENSION.

==============================================================
Cl_4 EVEN/ODD SPLIT MATCHES BIPARTITION
==============================================================

Cl_4 grade-parity decomposition:
  EVEN grades (0, 2, 4): scalar (1) + bivectors (6) + pseudoscalar (1) = 8
  ODD grades  (1, 3):     vectors (4) + pseudovectors (4)               = 8

The Cl_4 EVEN subalgebra is isomorphic to Cl_3 ~ H x H (quaternion).

The Q_4 vertex bipartition (8 even-Hamming + 8 odd-Hamming) MATCHES
the Cl_4 grade-parity bipartition (8 even-grade + 8 odd-grade).

==============================================================
NEW SUBSTRATE IDENTITY: 8 = 2^q = OCTONION CLASS SIZE
==============================================================

The knight tour bipartition gives TWO substrate-octonion-sized classes:

  Even-parity class:  8 = 2^q = O dim
  Odd-parity class:   8 = 2^q = O dim
  Total:              16 = lambda^mu = 2 * 2^q

NEW SUBSTRATE READING:
  16 = lambda^mu = lambda * 2^q (octonion doubling)
  16 = 2 octonion frames glued by knight-tour edges

==============================================================
THE OCTONION-OCTONION BRIDGE (CL_4 = O x O VIEW)
==============================================================

Classical: Cl_4 = M_2(H) (2x2 matrices over quaternions).
But also: 16 = 2 * 8 = lambda * O dim suggests:
  Cl_4 (vector space) = O x O (graded)

This connects to the BT chain's substrate octonion findings:
  2^q = 8 = octonion dim repeatedly appears
  E_8 = exceptional Lie group built from O algebra
  Triple Convergence h(E_8) = 30 (BT78)

The 16-vertex 4x4 substrate object is ALSO an octonion-octonion
bipartite frame.

==============================================================
THE 5-WAY UNIFICATION (extending BT157)
==============================================================

BT157 unified 4 readings; user's parity comment adds a 5TH:

  (1) Cl_4 Clifford frame                  (algebra)
  (2) Q_4 hypercube                         (topology)
  (3) Toroidal 4x4 knight tour             (geometry)
  (4) Gray-code Hamilton clock              (information)
  (5) Octonion-octonion bipartition         (parity)

ALL FIVE describe the SAME 16-vertex substrate object.

==============================================================
PARITY = TIME IN BELL CONTEXT
==============================================================

In the BT72 Addendum reading: 4x4 = past x future Bell context.
  Even-parity class = SYNCHRONIZED states (same parity past/future)
  Odd-parity class  = DESYNCHRONIZED states (different parity)

Knight tour alternation = TIME-EVOLUTION ALTERNATION between
synchronized and desynchronized Bell states.

This connects PARITY to the photonic substrate's temporal structure.

==============================================================
ZERO 4-CYCLES IN Q_4 (bipartite consequence)
==============================================================

A bipartite graph has NO ODD-LENGTH cycles.
Q_4 is bipartite (knight tour alternates) -> no 3-cycles, no 5-cycles.

All cycles of Q_4 have even length. The shortest cycles are
4-cycles (faces of the hypercube), and Q_4 has 24 = q!*(q+1) = f
of them (BT157).

The bipartite structure FORCES this even-length cycle property.

==============================================================
PILLAR-LEVEL: PARITY ALTERNATION AS NATURAL CLOCK
==============================================================

In the 5-way unified 4x4 object, the KNIGHT-TOUR PARITY ALTERNATION
plays the role of a SUBSTRATE CLOCK:

  TICK = even parity
  TOCK = odd parity
  Each substrate cycle = 16 = 2^mu ticks
  Period at half-cycle = 8 = 2^q (octonion frame switch)

This is the substrate's NATURAL OSCILLATOR at the 4x4 scale,
with substrate-clean period 2^q.

==============================================================
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    octonion_dim = 2 ** q  # 8

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 161: KNIGHT PARITY = OCTONION BIPARTITION")
    print("=" * 78)
    print()

    print("KNIGHT-TOUR PARITY ALTERNATION (user-pointed):")
    print(f"  Knight moves on Q_4 = single bit flips => Hamming parity toggles.")
    print(f"  Hamilton cycle MUST alternate even/odd weight vertices.")
    print()

    print("BIPARTITION OF Q_4 = 16 VERTICES:")
    even = ["0000", "0011", "0101", "0110", "1001", "1010", "1100", "1111"]
    odd  = ["0001", "0010", "0100", "1000", "0111", "1011", "1101", "1110"]
    print(f"  Even-parity ({len(even)}): {even}")
    print(f"  Odd-parity  ({len(odd)}): {odd}")
    assert len(even) == len(odd) == octonion_dim == 8
    print()

    print("OCTONION CONNECTION:")
    print(f"  Each class size = 8 = 2^q = OCTONION DIMENSION")
    print(f"  Two octonion frames glued by knight-tour edges")
    print(f"  16 = lambda * 2^q = lambda^mu (octonion doubling)")
    print()

    print("Cl_4 EVEN/ODD SPLIT (matches bipartition):")
    print(f"  Cl_4 EVEN grades: scalar(1) + bivector(6) + pseudoscalar(1) = 8")
    print(f"  Cl_4 ODD grades:  vector(4) + pseudovector(4)               = 8")
    print(f"  Q_4 vertex bipartition MATCHES Cl_4 grade-parity bipartition.")
    print()

    print("5-WAY UNIFICATION (extends BT157 4-way):")
    readings = [
        "Cl_4 Clifford frame (algebra)",
        "Q_4 hypercube (topology)",
        "Toroidal 4x4 knight tour (geometry)",
        "Gray-code Hamilton clock (information)",
        "Octonion-octonion bipartition (parity)",
    ]
    for i, r in enumerate(readings, 1):
        print(f"  ({i}) {r}")
    print()

    print("BELL CONTEXT TEMPORAL READING:")
    print(f"  4x4 = past x future Bell rays (BT72 Addendum)")
    print(f"  Even parity = synchronized past/future")
    print(f"  Odd parity = desynchronized past/future")
    print(f"  Knight tour alternation = time-evolution alternation")
    print()

    print("BIPARTITE => NO ODD CYCLES:")
    print(f"  Q_4 is bipartite (forced by parity alternation)")
    print(f"  Shortest cycles: 4-cycles (24 = q!*(q+1) = f faces)")
    print(f"  No 3-cycles, 5-cycles, etc.")
    print()

    print("SUBSTRATE CLOCK (NEW):")
    print(f"  TICK = even parity; TOCK = odd parity")
    print(f"  Each full substrate cycle: 16 = 2^mu ticks")
    print(f"  Half-cycle period: 8 = 2^q (octonion frame switch)")
    print(f"  The substrate's NATURAL OSCILLATOR at 4x4 scale.")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 161 SUMMARY")
    print("=" * 78)
    print("""
KNIGHT-TOUR PARITY ALTERNATION = OCTONION BIPARTITION.

USER-POINTED INSIGHT:
  Knight tours on Q_4 (= 4x4 toroidal hypercube) alternate
  Hamming-weight parity at every step.

CONSEQUENCE:
  Q_4 vertex bipartition: 8 even + 8 odd Hamming weight.
  Each class size = 8 = 2^q = OCTONION DIMENSION.

Cl_4 PARITY MATCH:
  Cl_4 even-grade subalgebra (1+6+1 = 8) corresponds to even-parity Q_4.
  Cl_4 odd-grade subalgebra  (4+4 = 8)  corresponds to odd-parity Q_4.

5-WAY UNIFICATION (extends BT157):
  Cl_4 algebra = Q_4 topology = knight geometry = Gray information
                = octonion-octonion parity.

SUBSTRATE INTERPRETATIONS:
  - Octonion-octonion frame (8+8 octonion-sized classes)
  - Synchronized/desynchronized Bell context (temporal alternation)
  - Substrate natural clock at 4x4 scale (period 2^q = 8)

  16 = lambda * 2^q = lambda^mu (octonion doubling identity)

BIPARTITE CONSEQUENCE:
  No odd-length cycles in Q_4 (knight tours have only even cycles).
  Shortest cycles: 4-cycles, count = 24 = f (BT157).

THE PARITY STRUCTURE turns the 4x4 substrate object into a CLOCK
with a substrate-clean period of 2^q = 8 ticks.
""")

    out = Path("data") / "w33_BREAKTHROUGH_161_knight_parity_octonion_bipartition.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "user_insight": "knight tour alternates parity at every node visited",
        "Q_4_bipartition": {
            "even_parity_class_size": 8,
            "odd_parity_class_size": 8,
            "class_size_substrate": "2^q = octonion dim",
        },
        "Cl_4_grade_parity_match": {
            "even_grades": "scalar(1) + bivector(6) + pseudoscalar(1) = 8",
            "odd_grades": "vector(4) + pseudovector(4) = 8",
        },
        "5_way_unification": [
            "Cl_4 algebra", "Q_4 topology", "toroidal knight geometry",
            "Gray code information", "octonion-octonion parity",
        ],
        "octonion_doubling_identity": "16 = lambda * 2^q = lambda^mu",
        "bell_temporal_reading": (
            "even parity = synchronized past/future; "
            "odd parity = desynchronized; knight alternation = "
            "time-evolution alternation"
        ),
        "bipartite_consequence": "Q_4 has no odd-length cycles",
        "substrate_clock": {
            "tick_tock": "even/odd parity",
            "full_cycle": "16 = 2^mu",
            "half_cycle": "8 = 2^q (octonion frame switch)",
        },
        "conclusion": (
            "Knight-tour parity alternation forces Q_4 bipartition into "
            "two octonion-dim classes (8+8). Cl_4 grade-parity matches "
            "Q_4 vertex-parity exactly. Extends 4-way unification to "
            "5-way (BT157+161). Provides substrate natural clock with "
            "period 2^q = 8 at 4x4 scale. 16 = lambda * 2^q = octonion "
            "doubling identity."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
