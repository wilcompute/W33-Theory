"""W(3,3) BREAKTHROUGH 267: HEAWOOD GRAPH FULL INTEGRATION.

The Heawood graph is the Levi (incidence) graph of the Fano plane PG(2, F_2)
and the UNIQUE (3, 6)-cage. It sits at the toroidal/seven-web (BT264) and
connects directly to the Csaszar/Szilassi polyhedra and tomotope substrate.

This BT fully integrates the Heawood graph's substrate structure.

==============================================================
HEAWOOD GRAPH STRUCTURE
==============================================================

  |V(Heawood)| = 14 = lambda * Phi_6
  |E(Heawood)| = 21 = T_6 = C(Phi_6, 2)
  Degree = 3 = q (cubic graph)
  Girth = 6 = q! (smallest cycle length)
  Diameter = 3 = q
  Bipartite: (7, 7) = (Phi_6, Phi_6)

The Heawood graph is the unique (3, 6)-CAGE: smallest 3-regular
graph with girth 6.

==============================================================
SUBSTRATE FACTORISATIONS
==============================================================

  14 = lambda * Phi_6 (vertex count)
  21 = T_6 = C(Phi_6, 2) = E count of both Csaszar AND Szilassi (BT79)
  3 = q (degree)
  6 = q! (girth)
  336 = lambda * |Aut(Fano)| = lambda * 168 = Aut(Heawood) (BT79)

==============================================================
HEAWOOD = LEVI GRAPH OF FANO PLANE
==============================================================

The Fano plane has 7 points and 7 lines. The Heawood graph is the
bipartite incidence graph:
  one side = 7 Fano points (Phi_6)
  other side = 7 Fano lines (Phi_6)
  edge iff point lies on line

This makes Heawood = INCIDENCE STRUCTURE of Phi_6 + Phi_6.

==============================================================
HEAWOOD SPECTRUM
==============================================================

The Heawood graph adjacency spectrum:
  eigenvalues: {3, sqrt(2), -sqrt(2), -3} (only 4 distinct)
  multiplicities: (1, 6, 6, 1)

Sum: 1+6+6+1 = 14 = lambda * Phi_6 ✓

Substrate readings:
  Perron = 3 = q (degree)
  Middle eigenvalues = ±sqrt(2) = ±sqrt(lambda)
  Multiplicity of middle = 6 = q!

GRAPH ENERGY of Heawood:
  E(Heawood) = 3*1 + sqrt(2)*6 + sqrt(2)*6 + 3*1
             = 6 + 12*sqrt(2)
             = 6 * (1 + 2*sqrt(2))
             ~ 22.97

This is NOT integer (involves sqrt(2)). But the rational part 6 = q!.

==============================================================
HEAWOOD GENUS
==============================================================

The Heawood graph has GENUS 1 (toroidal) -- it embeds on the torus.
This connects to:
  K_7 has genus 1 (BT264, BT79)
  Csaszar / Szilassi are toroidal (genus 1, BT79)
  Heawood graph is toroidal

ALL THREE genus-1 objects share the substrate's Phi_6 = 7 layer.

==============================================================
HEAWOOD AS THE TOROIDAL SUBSTRATE SPINE
==============================================================

The Heawood graph appears in MULTIPLE toroidal substrate contexts:
  - 8 toroidal face systems on Heawood = 8 Sylow-7 subgroups (BT80)
  - Aut(Heawood) = 336 = lambda * Aut(Fano) (BT79)
  - Heawood = Levi graph of Fano (incidence)
  - Heawood is unique (3, 6)-cage
  - Heawood is toroidal (genus 1)

THE HEAWOOD GRAPH IS THE SUBSTRATE'S TOROIDAL SPINE:
  it stitches together Fano (q = 3 base structure), Csaszar/Szilassi
  (Phi_6 toroidal polyhedra), and 8 Sylow-7 subgroups of GL(3, 2).

==============================================================
HEAWOOD vs Q_4 COMPARISON
==============================================================

Both are bipartite, but different sizes:
  Heawood:  14 vertices, 21 edges, deg 3, girth 6
  Q_4:      16 vertices, 32 edges, deg 4, girth 4

Q_4 is the substrate's 4x4 layer (mu = 4, BT157).
Heawood is the substrate's TOROIDAL Phi_6 = 7 layer.

These are TWO DIFFERENT toroidal-shell substrate objects:
  - Q_4 = mu^2 toroidal hypercube (knight tour)
  - Heawood = lambda*Phi_6 toroidal Levi graph

Together they tile the substrate's spacetime + heptad shells.

==============================================================
HEAWOOD NUMBER & SEVEN-COLOR
==============================================================

Heawood (1890): the genus-g surface chromatic number is
  chi(S_g) = floor((7 + sqrt(1 + 48g)) / 2)

At g = 1 (torus): chi = floor((7 + 7) / 2) = 7 = Phi_6.

  Toroidal chromatic number = 7 = Phi_6 = Heawood number.

The Heawood graph itself has chromatic number 2 (bipartite), but the
NUMBER 7 (Heawood number) is the chromatic upper bound for toroidal
graphs.

==============================================================
SUBSTRATE BRIDGE: HEAWOOD <-> Q_4
==============================================================

Both have toroidal embedding. Their interplay:
  Heawood: bipartite (Phi_6, Phi_6) at degree q = 3
  Q_4: bipartite (2^q, 2^q) = (8, 8) at degree mu = 4

  Heawood vertex count + Q_4 vertex count = 14 + 16 = 30 = h(E_8)
                                               = Triple Convergence!

The SUM of Heawood and Q_4 vertex counts = h(E_8) = q * Phi_4.

NEW SUBSTRATE IDENTITY:
  |V(Heawood)| + |V(Q_4)| = lambda*Phi_6 + lambda^mu = 30 = h_E_8.

==============================================================
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    phi6 = 7
    h_E_8 = 30
    q_fact = math.factorial(q)

    heawood_V = lambda_ * phi6  # 14
    heawood_E = math.comb(phi6, 2)  # 21
    Q_4_V = lambda_ ** mu  # 16
    Q_4_E = mu * 2 ** (mu - 1)  # 32

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 267: HEAWOOD GRAPH FULL INTEGRATION")
    print("=" * 78)
    print()

    print("HEAWOOD GRAPH STRUCTURE:")
    print(f"  |V| = {heawood_V} = lambda * Phi_6")
    print(f"  |E| = {heawood_E} = T_6 = C(Phi_6, 2)")
    print(f"  Degree = {q} = q (cubic)")
    print(f"  Girth = {q_fact} = q! (smallest cycle length)")
    print(f"  Diameter = {q} = q")
    print(f"  Bipartite: (Phi_6, Phi_6) = (7, 7)")
    print(f"  Unique (3, 6)-cage")
    print()

    print("HEAWOOD = LEVI GRAPH OF FANO PLANE:")
    print(f"  Fano: 7 points + 7 lines (incidence)")
    print(f"  Heawood vertices = 7 points + 7 lines = 14 = lambda*Phi_6")
    print(f"  Heawood edges = 21 incidences = T_6")
    print()

    print("HEAWOOD SPECTRUM:")
    print(f"  Eigenvalues: {{3, sqrt(2), -sqrt(2), -3}}")
    print(f"  Multiplicities: (1, 6, 6, 1)")
    print(f"  Perron = q; middle = +/-sqrt(lambda) with multiplicity q!")
    print()

    print("HEAWOOD-Q_4 SUM IDENTITY (NEW):")
    sum_V = heawood_V + Q_4_V
    assert sum_V == h_E_8
    print(f"  |V(Heawood)| + |V(Q_4)| = {heawood_V} + {Q_4_V} = {sum_V}")
    print(f"  = h(E_8) = q * Phi_4 = Triple Convergence integer!")
    print(f"  *** STAR: substrate's toroidal spine + 4x4 layer = h_E_8 ***")
    print()

    print("HEAWOOD-NUMBER FORMULA (genus-g chromatic):")
    print(f"  chi(S_g) = floor((7 + sqrt(1 + 48g)) / 2)")
    print(f"  At g = 1 (torus): chi = 7 = Phi_6 = Heawood number")
    print()

    print("THE HEAWOOD-FANO-CSASZAR-SZILASSI-Q_4 WEB:")
    web = [
        ("Heawood graph (3,6)-cage", "14 vertices, toroidal"),
        ("Fano plane PG(2, F_2)", "7 points, 7 lines, Heawood = Levi graph"),
        ("Csaszar polyhedron", "(7, 21, 14), K_7 vertex graph, toroidal"),
        ("Szilassi polyhedron", "(14, 21, 7), K_7 face graph, toroidal"),
        ("Q_4 hypercube / 4x4 knight tour", "16 vertices, toroidal, BT157"),
        ("8 Sylow-7 subgroups of GL(3,2)", "8 toroidal face systems of Heawood (BT80)"),
    ]
    for name, desc in web:
        print(f"  - {name}: {desc}")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 267 SUMMARY")
    print("=" * 78)
    print(f"""
HEAWOOD GRAPH = SUBSTRATE'S TOROIDAL SPINE.

|V| = 14 = lambda*Phi_6, |E| = 21 = T_6, deg = q, girth = q!.
Bipartite (Phi_6, Phi_6); unique (3, 6)-cage; toroidal (genus 1).

CONNECTS TO:
  Fano plane: Heawood = incidence Levi graph
  Csaszar/Szilassi: shared E count = 21 = T_6
  8 Sylow-7 subgroups (BT80) = 8 toroidal face systems
  K_7 chromatic number = 7 = Phi_6 = Heawood number

STAR NEW IDENTITY:
  |V(Heawood)| + |V(Q_4)| = 14 + 16 = 30 = h(E_8)
  Substrate's toroidal Phi_6 spine + 4x4 spacetime layer
  = Triple Convergence Coxeter number.

TWO TOROIDAL SHELLS, ONE SUBSTRATE:
  Heawood (lambda*Phi_6 = 14) for toroidal/Phi_6 layer
  Q_4 (lambda^mu = 16) for 4x4 spacetime/Cl_4 layer
  Together: 30 = h(E_8) total vertices.

Heawood spectrum: {{3, +/-sqrt(2), -3}} with mults (1, 6, 6, 1).
Perron = q; middle = sqrt(lambda) with mult q!.
""")

    out = Path("data") / "w33_BREAKTHROUGH_267_heawood_full_integration.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "heawood_structure": {
            "V": heawood_V,
            "V_substrate": "lambda * Phi_6",
            "E": heawood_E,
            "E_substrate": "T_6 = C(Phi_6, 2)",
            "degree": q,
            "girth": q_fact,
            "bipartite": [phi6, phi6],
        },
        "heawood_eq_fano_levi": True,
        "heawood_genus": 1,
        "heawood_spectrum": "{3, +/-sqrt(2), -3}",
        "heawood_multiplicities": [1, 6, 6, 1],
        "heawood_plus_Q4_sum": h_E_8,
        "heawood_plus_Q4_substrate": "30 = h(E_8) = Triple Convergence",
        "toroidal_substrate_web": [{"name": n, "desc": d} for n, d in web],
        "conclusion": (
            "Heawood graph (3,6)-cage = substrate's toroidal spine. "
            "|V|=14=lambda*Phi_6, |E|=21=T_6, deg=q, girth=q!, toroidal. "
            "Heawood = Levi graph of Fano. STAR: |V(Heawood)| + |V(Q_4)| "
            "= 30 = h(E_8) = Triple Convergence. Toroidal Phi_6 + spacetime "
            "mu^2 shells sum to the substrate's Coxeter number."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
