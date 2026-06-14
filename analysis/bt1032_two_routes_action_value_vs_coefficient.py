#!/usr/bin/env python3
"""
(R3, honest refinement) Two routes to the gravity term, and what each closes.

BT1031 reduced R3's spectral-action convergence to propinquity convergence of
the edgewise tower, using Latremoliere's continuity of action functionals. This
note draws a sharp, honest distinction that BT1031 glossed:

  * the spectral action VALUE  S(Lambda) = Tr f(D^2/Lambda^2)  at FIXED Lambda,
    vs.
  * the Einstein-Hilbert COEFFICIENT a_2 ~ (1/6) int R, an ASYMPTOTIC
    (Lambda -> inf) expansion coefficient of S(Lambda).

Latremoliere's propinquity continuity gives the first (fixed-Lambda action
value: D_n -> D in propinquity  =>  S_n(Lambda) -> S(Lambda)). It does NOT by
itself give the second: the coefficient a_2 lives in the Lambda -> inf limit,
so extracting it needs the refinement limit (n -> inf) and the cutoff limit
(Lambda -> inf) to commute -- which fixed-Lambda continuity does not assert.

The point is concrete: a finite (truncated) spectrum has NO continuum short-
time/large-Lambda asymptotic; that asymptotic only re-emerges as n -> inf.
So the limit order matters.

The GEOMETRIC / Regge route bypasses this entirely: the Regge deficit-angle
curvature is a per-level LOCAL quantity, and Cheeger-Mueller-Schrader gives
[Regge curvature]_n -> int R directly as the mesh -> 0 (n -> inf), with NO
cutoff limit. So the EH COEFFICIENT is closed by the geometric route
(BT986 verified [Regge]_n -> int R on the sphere); the spectral/propinquity
route closes the action VALUE at each cutoff.

Toy below: the circle Laplacian, truncated at level n, makes the distinction
unmistakable.
"""
from __future__ import annotations

import json
import math


def theta_truncated(t, n):
    # circle S^1 (length 2pi) Laplacian eigenvalues {k^2 : k in Z}, truncated |k|<=n
    return sum(math.exp(-t*k*k) for k in range(-n, n+1))


def theta_continuum(t):
    # Jacobi theta; for small t ~ sqrt(pi/t) (Weyl a_0 = length/sqrt(4 pi t),
    # length = 2 pi  => sqrt(pi/t)). Sum enough terms.
    return sum(math.exp(-t*k*k) for k in range(-2000, 2001))


def main():
    print("TOY: circle Laplacian heat trace Theta(t) = sum exp(-t k^2)")
    print("continuum small-t Weyl leading term = sqrt(pi/t)\n")

    # (a) fixed-cutoff (fixed n) behaviour as t->0: SATURATES at 2n+1
    print("(a) FIXED n, t->0: Theta_n(t) saturates at 2n+1 (no continuum")
    print("    asymptotic) -- the truncation has no short-time singularity:")
    for n in [5, 20, 100]:
        row = "    n=%4d : " % n
        for t in [0.1, 0.01, 0.001, 1e-5]:
            row += f"t={t:<7}{theta_truncated(t, n):8.2f}  "
        print(row + f"  (2n+1={2*n+1})")

    # (b) fixed t, n->inf: action VALUE converges (this is the propinquity/
    #     fixed-cutoff statement)
    print("\n(b) FIXED t, n->inf: action VALUE converges to the continuum:")
    for t in [0.1, 0.01]:
        cont = theta_continuum(t)
        row = f"    t={t}: "
        for n in [5, 20, 100, 500]:
            row += f"n={n}:{theta_truncated(t, n):8.3f}  "
        print(row + f"-> continuum {cont:.3f}  (Weyl sqrt(pi/t)={math.sqrt(math.pi/t):.3f})")

    # (c) the COEFFICIENT (Weyl a_0 ~ sqrt(pi/t)) needs n->inf BEFORE t->0
    print("\n(c) the asymptotic COEFFICIENT (a_0 = sqrt(pi/t)) only appears in")
    print("    the order n->inf THEN t->0. At fixed n it is absent (a).")
    print("    => fixed-cutoff convergence (propinquity, b) is NOT coefficient")
    print("       convergence (c): the limits do not trivially commute.")

    # W(3,3) tie-in (numbers from BT1031): action value vs moments
    spec = {0: 122, 4: 240, 10: 48, 16: 30}
    M0 = sum(spec.values())
    M1 = sum(l*m for l, m in spec.items())
    print("\nW(3,3) tie-in: the F-side action VALUE S(Lambda)=Tr f(D_F^2/L^2)")
    print(f"  is continuous (propinquity); the EH/matter COEFFICIENTS are the")
    print(f"  moments M0=dim H_F={M0}, M1=Tr D_F^2={M1} -- asymptotic objects.")

    print("\nSYNTHESIS (two routes, honest scope):")
    print(" - GEOMETRIC (Regge/CMS, BT986): closes the EH COEFFICIENT")
    print("   a_2 ~ (1/6) int R directly per level, no cutoff limit. The")
    print("   physically decisive route for Newton's constant.")
    print(" - SPECTRAL (propinquity, BT1031): closes the action VALUE at each")
    print("   cutoff; the asymptotic-coefficient extraction needs the n<->L")
    print("   interchange (open in the pure-spectral route, bypassed by Regge).")
    print(" Together: the EH coefficient converges (geometric), and the full")
    print(" spectral action converges at every cutoff (spectral). R3's gravity")
    print(" term is robustly supported from both sides; the only purely-spectral")
    print(" residual is the asymptotic-coefficient uniformity.")

    out = {
        "theorem": "(R3) action value vs EH coefficient; two-route synthesis",
        "toy": "circle Laplacian truncation shows fixed-cutoff convergence "
               "!= asymptotic-coefficient convergence (limits don't commute)",
        "geometric_route": "Regge/CMS closes a_2 ~ (1/6) int R per level "
                           "(no cutoff limit); BT986 verified on the sphere",
        "spectral_route": "propinquity closes the action value at fixed cutoff "
                          "(BT1031); asymptotic coefficient needs n<->Lambda "
                          "interchange",
        "honest_refinement_of_BT1031": "propinquity gives action-VALUE "
            "continuity, not the asymptotic EH COEFFICIENT; the geometric "
            "route supplies the coefficient.",
    }
    with open("data/bt1032_two_routes_action_value_vs_coefficient.json",
              "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt1032_two_routes_action_value_vs_coefficient.json")


if __name__ == "__main__":
    main()
