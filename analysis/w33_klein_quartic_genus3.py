#!/usr/bin/env python3
"""
The ladder's genus-3 rung: the Klein quartic (24 heptagons / 56 triangles / 84
edges, Aut = PSL(2,7) = 168 = lambda k Phi6) is the substrate's readout layer, and
the heptagon Phi6=7 threads the whole ladder 3 -> 4 -> 7 -> Klein.

The triangulation ladder (w33_genus_ladder_clock.py) goes genus 0 (tetrahedron,
sphere, q & mu) -> genus 1 (torus = Csaszar/Szilassi = Heawood/Fano, the 7-point
heptad). Its next maximally-symmetric rung is the genus-3 KLEIN QUARTIC, the
lowest-genus Hurwitz surface (Wikipedia: Hurwitz/Klein quartic):
  - automorphism group Aut = PSL(2,7), |Aut| = 84(g-1) = 84*2 = 168, and on the
    substrate 168 = lambda * k * Phi6 = 2*12*7 = Phi6 * f = 7*24 (the corpus
    detector/readout layer);
  - regular map {3,7}/{7,3}: 24 heptagons (24*7 = 168) <-> 56 triangles with 24
    degree-7 vertices, sharing 84 = k*Phi6 edges. Euler chi = 24-84+56 = -4 =
    2-2g -> g = 3.
On the substrate the Klein numbers are substrate integers: 24 = f (= Hurwitz-unit
/ D4 seed = heptagons), 56 = v+k+mu = E7 fundamental (= triangles), 84 = k*Phi6 =
2*Hurwitz-bound coefficient (= edges), 168 = lambda*k*Phi6 = PSL(2,7) (= the
clock/readout PSL(2,7) layer of the two-layer split).

So the heptagon Phi6 = 7 is the thread: the Fano plane (7 points, genus-1 torus via
Heawood) becomes the heptagonal tiling (genus-3 Klein quartic) -- the same PSL(2,7)
that is the clock/readout layer, now realized as the maximally-symmetric genus-3
surface. The ladder 3 (triangle) -> 4 (tetrahedron) -> 7 (Fano/torus) -> Klein
(genus 3, PSL(2,7)) climbs from the trit to the readout.

Verifies the Klein quartic Euler/genus and the substrate identities for
24, 56, 84, 168.
"""
from __future__ import annotations

import json

Q, LAM, MU, K, V, F, PHI6 = 3, 2, 4, 12, 40, 24, 7


def main():
    out = {}

    # Klein quartic {7,3}: 24 heptagons, 84 edges, 56 vertices (degree 3) -- or dual
    heptagons, edges, triangles = 24, 84, 56
    # regular map {3,7}: 56 triangles, 84 edges, 24 vertices (degree 7)
    V_, E_, F_ = triangles, edges, heptagons  # {7,3}: F=24 heptagons, V=56, E=84
    chi = V_ - E_ + F_
    g = (2 - chi) // 2
    print(
        f"[Klein quartic]  regular map {{7,3}}: {F_} heptagons, {E_} edges, "
        f"{V_} vertices"
    )
    print(f"  Euler chi = {V_} - {E_} + {F_} = {chi} = 2-2g -> genus g = {g}")
    assert chi == -4 and g == 3
    out["genus"] = g
    out["heptagons"] = heptagons
    out["triangles"] = triangles
    out["edges"] = edges

    # automorphism group and Hurwitz bound
    aut = 168
    print(f"\n[automorphism]  Aut = PSL(2,7), |Aut| = 84(g-1) = 84*{g-1} = {84*(g-1)}")
    print(
        f"  substrate: 168 = lambda*k*Phi6 = {LAM}*{K}*{PHI6} = {LAM*K*PHI6} "
        f"= Phi6*f = {PHI6}*{F} = {PHI6*F}"
    )
    print(f"  = the clock/readout PSL(2,7) layer (two-layer split)")
    assert aut == 84 * (g - 1) == LAM * K * PHI6 == PHI6 * F == 168
    out["aut"] = aut

    # the Klein numbers are substrate integers
    print(f"\n[Klein numbers = substrate integers]")
    print(f"  24 heptagons = f = {F} (Hurwitz-unit / D4 seed)")
    print(f"  56 triangles = v+k+mu = {V}+{K}+{MU} = {V+K+MU} (E7 fundamental)")
    print(f"  84 edges = k*Phi6 = {K}*{PHI6} = {K*PHI6} (Hurwitz-bound coeff)")
    print(f"  168 = lambda*k*Phi6 = PSL(2,7) (readout layer)")
    assert (
        heptagons == F == 24
        and triangles == V + K + MU == 56
        and edges == K * PHI6 == 84
    )
    out["klein_numbers"] = {
        "24": "f",
        "56": "v+k+mu (E7 fund)",
        "84": "k*Phi6",
        "168": "lambda*k*Phi6 = PSL(2,7)",
    }

    # the ladder 3 -> 4 -> 7 -> Klein
    print(f"\n[the ladder]  genus 0 -> 1 -> 3, threaded by the heptagon Phi6=7:")
    print(f"  g=0: tetrahedron (sphere), q=3 / mu=4")
    print(f"  g=1: torus = Csaszar/Szilassi = Heawood/Fano (7-point heptad)")
    print(f"  g=3: Klein quartic ({{7,3}}, 24 heptagons), PSL(2,7)=168=lambda*k*Phi6")
    out["ladder"] = [
        "g0: tetrahedron (q,mu)",
        "g1: Fano/torus (Phi6=7)",
        "g3: Klein quartic PSL(2,7)=168",
    ]

    print("\nRESULT: the triangulation ladder climbs to genus 3. After the triangle")
    print("  (q=3), the tetrahedron (mu=4), and the Fano/torus (Phi6=7, the Heawood")
    print("  clock), the next maximally-symmetric rung is the Klein quartic -- the")
    print("  lowest-genus Hurwitz surface, genus 3, with 24 heptagons / 56 triangles")
    print("  / 84 edges and automorphism group PSL(2,7) of order 168 = lambda*k*Phi6")
    print("  = Phi6*f. Its numbers are all substrate integers (24=f, 56=E7 fund, ")
    print("  84=k*Phi6, 168=PSL(2,7)), and that PSL(2,7) is exactly the clock/readout")
    print("  layer. The heptagon Phi6=7 threads the whole ladder: the Fano heptad")
    print("  becomes the heptagonal genus-3 surface. The ladder climbs from the trit")
    print("  (genus 0) to the readout (genus 3).")

    out["summary"] = (
        "genus-3 rung of the ladder: Klein quartic (lowest-genus Hurwitz"
        " surface), {7,3} = 24 heptagons / 56 triangles / 84 edges, "
        "Euler -4, g=3; Aut=PSL(2,7), 168=84(g-1)=lambda*k*Phi6=Phi6*f "
        "(the clock/readout layer). Klein numbers = substrate integers "
        "(24=f, 56=v+k+mu=E7 fund, 84=k*Phi6). Ladder 3->4->7->Klein "
        "threaded by the heptagon Phi6=7: trit (g0) to readout (g3)."
    )
    out["sources"] = [
        "Klein quartic / Hurwitz surface (Wikipedia); PSL(2,7)=168="
        "84(g-1); {3,7}/{7,3} regular map (24 heptagons/56 triangles/84"
        " edges); corpus 168=lambda*k*Phi6, 84=k*Phi6; "
        "w33_genus_ladder_clock.py, w33_clock_gauge_two_layer.py"
    ]
    with open("data/w33_klein_quartic_genus3.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_klein_quartic_genus3.json")


if __name__ == "__main__":
    main()
