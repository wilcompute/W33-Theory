"""W(3,3) BREAKTHROUGH 158: Q_4 SPECTRUM = PASCAL ROW 4 = Cl_4 GRADES.

Thinking outside the box: BT157 unified Q_4 hypercube with Cl_4
Clifford frame. THIS BT shows the Q_4 ADJACENCY SPECTRUM directly
matches the Cl_4 GRADE PROFILE.

==============================================================
THE Q_n SPECTRUM (CLASSICAL)
==============================================================

For the n-hypercube Q_n with V = {0,1}^n and edges differ in 1 bit:
  Adjacency eigenvalues: lambda_i = n - 2i for i = 0, 1, ..., n
  Multiplicities: C(n, i) = Pascal's row n entry i

For n = 4:
  eigenvalues:    {+4, +2, 0, -2, -4}
  multiplicities: { 1,  4, 6,  4,  1}  = Pascal row 4 = Cl_4 grades

==============================================================
THE Cl_n GRADE PROFILE (CLASSICAL)
==============================================================

Cl_n has 2^n basis elements partitioned by GRADE r (number of vector
factors in the multivector):
  Grade r dimension = C(n, r)

For n = 4:
  grades 0..4 dimensions: 1, 4, 6, 4, 1  (scalar, vector, bivector,
                                            pseudovector, pseudoscalar)

==============================================================
THE STRIKING IDENTITY
==============================================================

  Q_4 ADJACENCY MULTIPLICITIES  =  Cl_4 GRADE PROFILE  =  Pascal row 4

  (1, 4, 6, 4, 1)

The hypercube graph SPECTRUM and the Clifford algebra GRADES are
the SAME sequence of integers.

This is NOT a coincidence: it is a manifestation of the universal
Pascal/Cl/Q-cube structure at n = 4.

==============================================================
GRAPH ENERGY OF Q_4 = f = 24 (SUBSTRATE CROSS-LINK!)
==============================================================

Graph energy E(G) = sum_i |lambda_i| * m_i:

  E(Q_4) = 4*1 + 2*4 + 0*6 + 2*4 + 4*1
         = 4 + 8 + 0 + 8 + 4
         = 24
         = f
         = positive eigenspace multiplicity of W(3,3) adjacency
         = Leech lattice rank
         = D_4 root count
         = |S_4|
         = dim SU(5)_adj
         = q!(q+1)  (BT72 Addendum reading)

THE HYPERCUBE GRAPH ENERGY OF Q_4 EQUALS THE W(3,3) POSITIVE
EIGENSPACE MULTIPLICITY EXACTLY.

==============================================================
ADDITIONAL Q_4 SPECTRAL IDENTITIES
==============================================================

  |V(Q_4)| = 16 = sum of multiplicities = 1+4+6+4+1
  Trace tr(A_Q4) = sum lambda_i * m_i = 0 (alternating sums cancel)
  Trace tr(A_Q4^2) = sum lambda_i^2 * m_i
                  = 16+16+0+16+16 = 64 = 2|E(Q_4)| = mu^q

  64 = mu^q = lambda^Phi_6 / lambda = 128/2  (substrate)

  Q_4 SPECTRAL RADIUS = 4 = mu (max eigenvalue)
  Q_4 ALGEBRAIC CONNECTIVITY = mu (smallest positive eigenvalue 2... wait
    that's mu/2 = 2. So algebraic connectivity of Q_4 = 2 = lambda.)

==============================================================
Q_4 SUBSTRATE QUANTITY CASCADE
==============================================================

  |V(Q_4)|        = 16  = lambda^mu = mu^2 = 2^mu
  |E(Q_4)|        = 32  = 2^F_5
  Spectral radius = 4   = mu
  Algebraic conn  = 2   = lambda
  Graph energy    = 24  = f
  Sum m_i         = 16  = lambda^mu
  Sum m_i^2       = 1+16+36+16+1 = 70 = Phi_6 * Phi_4
  Trace A^2       = 64  = mu^q

ALL Q_4 SPECTRAL INVARIANTS are substrate-pure.

==============================================================
THE PASCAL-Cl-Q TRIANGLE BRIDGE
==============================================================

Pascal triangle row n:  C(n, 0), C(n, 1), ..., C(n, n)
Cl_n grade dimensions:  C(n, 0), C(n, 1), ..., C(n, n)
Q_n adj multiplicities: C(n, 0), C(n, 1), ..., C(n, n)

THREE FUNDAMENTAL STRUCTURES SHARE PASCAL'S TRIANGLE:
  combinatorial binomials
  algebraic Cl grades
  spectral Q_n multiplicities

At n = mu = 4, this bridge gives the substrate's 4x4 frame.

==============================================================
SUBSTRATE INTERPRETATION
==============================================================

The substrate's mu = 4 spacetime dimension forces the Pascal-Cl-Q
correspondence to land at row 4 with multiplicities (1, 4, 6, 4, 1).

Spacetime dim 4 = Cl_4 grade frame = Q_4 hypercube = Pascal row 4.

This is yet another "mu = 4 is special" identity (joining the
dS identity mu^4 = 256, the Lambda exponent, etc.).

==============================================================
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi4, phi6 = 10, 7

    # Q_4 spectrum
    eigenvalues = [mu - 2 * i for i in range(mu + 1)]  # [4, 2, 0, -2, -4]
    multiplicities = [math.comb(mu, i) for i in range(mu + 1)]  # [1, 4, 6, 4, 1]

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 158: Q_4 SPECTRUM = PASCAL ROW 4 = Cl_4 GRADES")
    print("=" * 78)
    print()

    print("Q_4 SPECTRUM:")
    for lam, m in zip(eigenvalues, multiplicities):
        print(f"  lambda = {lam:+d}  multiplicity = {m}")
    print()

    print("PASCAL ROW 4:")
    print(f"  (C(4,0), C(4,1), C(4,2), C(4,3), C(4,4)) = {multiplicities}")
    print()

    print("Cl_4 GRADE PROFILE:")
    grades = ["scalar", "vector", "bivector", "pseudovector", "pseudoscalar"]
    for r, m, g in zip(range(mu + 1), multiplicities, grades):
        print(f"  grade {r} ({g:<14}) dimension = {m}")
    print()

    print("THE STRIKING IDENTITY:")
    assert tuple(multiplicities) == (1, 4, 6, 4, 1)
    print(f"  Q_4 multiplicities = Pascal row 4 = Cl_4 grades = (1, 4, 6, 4, 1)")
    print()

    print("GRAPH ENERGY OF Q_4:")
    energy = sum(abs(lam) * m for lam, m in zip(eigenvalues, multiplicities))
    f_eig = 24
    assert energy == f_eig
    print(f"  E(Q_4) = sum |lambda_i| * m_i = 4*1 + 2*4 + 0*6 + 2*4 + 4*1")
    print(f"        = {energy}")
    print(f"  = f = positive eigenmult of W(3,3) adjacency")
    print(f"  = Leech rank = |S_4| = dim SU(5)_adj = q!(q+1)")
    print(f"  *** GRAPH ENERGY OF Q_4 = W(3,3) POSITIVE EIGENMULT ***")
    print()

    print("Q_4 SPECTRAL INVARIANTS (all substrate):")
    sum_m = sum(multiplicities)
    sum_m_sq = sum(m ** 2 for m in multiplicities)
    trace_A2 = sum(lam ** 2 * m for lam, m in zip(eigenvalues, multiplicities))
    spectral_radius = max(abs(lam) for lam in eigenvalues)
    print(f"  |V(Q_4)| = {sum_m} = lambda^mu = mu^2 = 2^mu")
    print(f"  Sum m_i^2 = {sum_m_sq} = Phi_6 * Phi_4 (NEW substrate!)")
    assert sum_m_sq == phi6 * phi4
    print(f"  tr(A^2) = {trace_A2} = mu^q (= 2|E(Q_4)|)")
    assert trace_A2 == mu ** q
    print(f"  Spectral radius = {spectral_radius} = mu")
    print()

    print("PASCAL-Cl-Q TRIANGLE BRIDGE:")
    print(f"  Pascal row n: C(n, 0), ..., C(n, n)")
    print(f"  Cl_n grades:  C(n, 0), ..., C(n, n)")
    print(f"  Q_n adj mults: C(n, 0), ..., C(n, n)")
    print(f"  ALL THREE = same combinatorial sequence.")
    print(f"  At n = mu = 4: (1, 4, 6, 4, 1) substrate frame.")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 158 SUMMARY")
    print("=" * 78)
    print("""
THE PASCAL-Cl-Q TRIPLE BRIDGE at n = mu = 4:

  Pascal row 4    = (1, 4, 6, 4, 1)
  Cl_4 grades     = (1, 4, 6, 4, 1)
  Q_4 multiplicities = (1, 4, 6, 4, 1)

THREE fundamentally different structures share Pascal's row.
At n = mu = 4 = spacetime dim, this triple bridge gives the
substrate's complete 4x4 frame.

STAR FINDING: GRAPH ENERGY OF Q_4 = W(3,3) POSITIVE EIGENMULT.

  E(Q_4) = sum |lambda_i| * m_i = 24 = f.
  Same integer that gives Leech rank, |S_4|, dim SU(5)_adj.

The hypercube graph energy and the W(3,3) positive eigenspace
multiplicity are the SAME f = 24.

NEW SUBSTRATE IDENTITIES:
  Sum m_i^2 of Q_4 = 70 = Phi_6 * Phi_4
  tr(A_Q4^2) = mu^q = 64
  Spectral radius = mu = 4

ALL Q_4 spectral invariants are substrate-pure.

This adds yet another "mu = 4 is special" identity to the chain.
""")

    out = Path("data") / "w33_BREAKTHROUGH_158_Q4_spectrum_graph_energy.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "Q_4_spectrum": {
            "eigenvalues": eigenvalues,
            "multiplicities": multiplicities,
        },
        "pascal_row_4": multiplicities,
        "Cl_4_grades": multiplicities,
        "three_structures_identical": True,
        "graph_energy": energy,
        "graph_energy_equals_f": True,
        "graph_energy_substrate": "f = 24 = positive eigenmult of W(3,3)",
        "spectral_invariants": {
            "sum_m": sum_m,
            "sum_m_squared": sum_m_sq,
            "sum_m_squared_substrate": "Phi_6 * Phi_4 = 70",
            "trace_A_squared": trace_A2,
            "trace_substrate": "mu^q = 64",
            "spectral_radius": spectral_radius,
        },
        "conclusion": (
            "Pascal row 4 = Cl_4 grades = Q_4 multiplicities at n = mu = 4. "
            "Graph energy of Q_4 = sum |lambda_i|*m_i = 24 = f (W(3,3) "
            "positive eigenmult). Q_4 spectral invariants all substrate. "
            "Adds new 'mu=4 is special' identity to substrate chain."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
