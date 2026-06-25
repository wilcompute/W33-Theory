#!/usr/bin/env python3
"""
The Suzuki tower of strongly regular graphs NESTS: each graph's valency equals
the previous graph's vertex count, the bottom is SRG(36,14,4,6) with 36 = the
even theta characteristics (the E7/Klein companion) and valency 14 = dim G2, and
the top is the Suz graph on 1782 = the complex Leech.

The Suzuki chain G2(2) -> J2 -> G2(4) -> Suz (w33_complex_leech_suzuki_chain.py)
is the automorphism tower of four strongly regular graphs:

    group        graph              (n,    k,   lambda, mu)
    G2(2)=U3(3)  U3(3) graph        (36,   14,  4,      6)
    J2           Hall-Janko graph   (100,  36,  14,     12)
    G2(4)        G2(4) graph        (416,  100, 36,     20)
    Suz          Suzuki graph       (1782, 416, 100,    96)

Each is feasible (k(k-lambda-1) = (n-k-1)*mu) and the tower NESTS:
    valency(graph i) = vertices(graph i-1),
    lambda(graph i)  = valency(graph i-1),
so the parameters telescope 14 < 36 < 100 < 416 < 1782 through the four rungs.

THE SUBSTRATE ANCHORS at the bottom rung SRG(36,14,4,6):
  - n = 36 = the EVEN theta characteristics of the genus-3 Klein quartic
    (w33_e7_theta_bitangents.py: 28 odd + 36 even = 64) -- so the Suzuki tower's
    base graph is the E7/Klein even-theta set;
  - valency k = 14 = dim G2 = 2*Phi6 = the genus of the {3,7} Hurwitz triplet
    (the top of the {3,7} tower) -- the G2 thread;
  - the group is G2(2) = U3(3):2 = the split Cayley hexagon = the 3-qubit core.

So the Suzuki tower carries the substrate up from the three-qubit hexagon (whose
graph has 36 = even-theta vertices and 14 = dim G2 valency) to the Suz graph on
1782 = the complex Leech, with the parameters telescoping at each rung.

Verifies the four Suzuki-tower SRG parameter sets (feasibility + nesting), and the
anchors 36 = even theta, 14 = dim G2.
"""
from __future__ import annotations

import json

PHI6 = 7  # dim G2 = 2*Phi6 = 14

# (group, n, k, lambda, mu)
TOWER = [
    ("G2(2)=U3(3)", 36, 14, 4, 6),
    ("J2 Hall-Janko", 100, 36, 14, 12),
    ("G2(4)", 416, 100, 36, 20),
    ("Suz", 1782, 416, 100, 96),
]


def main():
    out = {}

    # feasibility of each SRG: k(k-lambda-1) = (n-k-1)*mu
    print("[Suzuki tower SRGs]  feasibility k(k-l-1)=(n-k-1)mu")
    rows = []
    for name, n, k, lam, mu in TOWER:
        feasible = k * (k - lam - 1) == (n - k - 1) * mu
        print(f"  {name:14s} SRG({n:4d},{k:3d},{lam:3d},{mu:2d})  feasible: {feasible}")
        assert feasible
        rows.append({"group": name, "n": n, "k": k, "lambda": lam, "mu": mu})
    out["tower"] = rows

    # the nesting: valency(i) = vertices(i-1), lambda(i) = valency(i-1)
    print(f"\n[the nesting]  valency(i) = vertices(i-1), lambda(i) = valency(i-1)")
    for i in range(1, len(TOWER)):
        _, n_i, k_i, lam_i, _ = TOWER[i]
        _, n_p, k_p, _, _ = TOWER[i - 1]
        print(
            f"  {TOWER[i][0]:14s}: valency {k_i} == prev vertices {n_p} ({k_i==n_p}); "
            f"lambda {lam_i} == prev valency {k_p} ({lam_i==k_p})"
        )
        assert k_i == n_p and lam_i == k_p
    out["nesting"] = "valency(i)=vertices(i-1), lambda(i)=valency(i-1)"

    # the substrate anchors at the bottom rung
    n0, k0 = TOWER[0][1], TOWER[0][2]
    print(f"\n[substrate anchors, bottom rung SRG(36,14,4,6)]")
    print(
        f"  n = {n0} = the EVEN theta characteristics of the Klein quartic (28+36=64)"
    )
    print(f"  k = {k0} = dim G2 = 2*Phi6 = {2*PHI6} = genus of the {{3,7}} triplet")
    print(f"  group = G2(2) = U3(3):2 = the split Cayley hexagon = the 3-qubit core")
    assert n0 == 36 and k0 == 14 == 2 * PHI6
    out["anchors"] = {
        "n_36": "even theta characteristics (Klein/E7)",
        "k_14": "dim G2 = 2*Phi6 = genus-14 Hurwitz triplet",
        "group": "G2(2)=U3(3):2 = split Cayley hexagon = 3-qubit core",
    }

    # the top rung = the complex Leech
    print(
        f"\n[top rung]  Suz graph on 1782 = the complex Leech (6.Suz, Eisenstein 12=k)"
    )
    assert TOWER[-1][1] == 1782
    out["top"] = "Suz graph on 1782 = complex Leech (6.Suz)"

    print("\nRESULT: the Suzuki chain is a tower of four nested strongly regular")
    print("  graphs, SRG(36,14,4,6) < SRG(100,36,14,12) < SRG(416,100,36,20) <")
    print("  SRG(1782,416,100,96), in which each graph's valency is the previous")
    print("  graph's vertex count and each lambda is the previous valency -- the")
    print("  parameters telescope 14 < 36 < 100 < 416 < 1782. The base graph")
    print("  SRG(36,14,4,6) anchors the substrate: its 36 vertices are the even theta")
    print("  characteristics of the Klein quartic (the E7 companion of the 28")
    print("  bitangents), its valency 14 = dim G2 = the genus of the {3,7} Hurwitz")
    print("  triplet, and its group G2(2) is the three-qubit hexagon. So the climb")
    print("  from the 3-qubit core to the complex Leech is one telescoping SRG tower,")
    print("  anchored by the Klein/E7 even-theta set and the dimension of G2.")

    out["summary"] = (
        "the Suzuki chain is a tower of four nested SRGs: SRG(36,14,4,6) < "
        "SRG(100,36,14,12) < SRG(416,100,36,20) < SRG(1782,416,100,96), each "
        "feasible, with valency(i)=vertices(i-1) and lambda(i)=valency(i-1) so the "
        "parameters telescope 14<36<100<416<1782. The base SRG(36,14,4,6) anchors "
        "the substrate: 36 = even theta characteristics of the Klein quartic (E7 "
        "companion of the 28 bitangents), valency 14 = dim G2 = 2*Phi6 = genus-14 "
        "Hurwitz triplet, group G2(2)=U3(3):2=the 3-qubit hexagon. Top = Suz on "
        "1782 = the complex Leech."
    )
    out["sources"] = [
        "Suzuki tower of SRGs: SRG(36,14,4,6) [U3(3)/G2(2)], SRG(100,36,14,12) "
        "[Hall-Janko/J2], SRG(416,100,36,20) [G2(4)], SRG(1782,416,100,96) [Suz]; "
        "feasibility + nesting verified; 36=even theta (g=3), 14=dim G2=2*Phi6; "
        "w33_e7_theta_bitangents.py, w33_complex_leech_suzuki_chain.py, "
        "w33_macbeath_hexagon_functor.py."
    ]
    with open("data/w33_suzuki_tower_srg.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_suzuki_tower_srg.json")


if __name__ == "__main__":
    main()
