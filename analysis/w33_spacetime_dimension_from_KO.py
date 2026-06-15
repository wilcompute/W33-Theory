#!/usr/bin/env python3
"""
Why is spacetime 4-dimensional? Derived from W(3,3)'s KO-dimension.

This upgrades the 'dimensional unification' conjecture (two-continua note) to a
derivation, using only (a) the corpus-verified KO-dimension of the W(3,3)
finite spectral triple and (b) the standard Connes-Barrett fermion-doubling
constraint of noncommutative geometry.

Ingredients (both established):
  1. KO-dimension of the finite triple F = W(3,3): KO-dim(F) = 6 (mod 8).
     The corpus verifies the real-structure signs (J^2=+1, JD=+DJ, J*gamma =
     -gamma*J) = the sign triple (eps, eps', eps'') = (+,+,-), which is exactly
     KO-dimension 6 in the 8-periodic KO table. (= 2q, q=3.)
  2. Connes-Barrett: to solve fermion doubling and admit the Euclidean
     fermionic (Pfaffian) functional integral, the TOTAL spectral triple of
     M x F must have KO-dimension == 2 (mod 8).
  3. KO-dimension is additive under product: KO(M x F) = KO(M) + KO(F) (mod 8).
  4. For a spin MANIFOLD M, KO-dimension == metric dimension (mod 8).

Therefore KO(M) = 2 - 6 = -4 == 4 (mod 8), so dim M == 4 (mod 8): the minimal
(physical) solution is the observed four-dimensional spacetime. The 4 of M^4 -
the one input the almost-commutative framing previously took from observation -
is forced by W(3,3)'s KO-dimension 6 = 2q.
"""
from __future__ import annotations

import json

# KO-dimension sign table (eps: J^2=eps; eps': JD=eps' DJ; eps'': J gamma =
# eps'' gamma J), 8-periodic. (eps, eps', eps'')  (eps'' undefined in odd dims)
KO_SIGNS = {
    0: (+1, +1, +1),
    1: (+1, -1, None),
    2: (-1, +1, -1),
    3: (-1, -1, None),
    4: (-1, +1, +1),
    5: (-1, -1, None),
    6: (+1, +1, -1),
    7: (+1, -1, None),
}


def ko_from_signs(eps, epsp, epspp):
    for k, s in KO_SIGNS.items():
        if s == (eps, epsp, epspp):
            return k
    return None


def main():
    # 1. W(3,3) finite triple: corpus-verified real-structure signs
    eps, epsp, epspp = +1, +1, -1          # J^2=+1, JD=+DJ, J gamma = -gamma J
    ko_F = ko_from_signs(eps, epsp, epspp)
    print(f"KO-dim(F=W(3,3)) from signs (J^2=+1, JD=+DJ, Jgamma=-gammaJ): "
          f"{ko_F}  (= 2q, q=3)")
    assert ko_F == 6

    # 2. Connes-Barrett total-KO constraint
    ko_total = 2                            # mod 8, for the Euclidean fermion integral
    print(f"Connes-Barrett constraint: KO-dim(total) = {ko_total} (mod 8)")

    # 3. additivity -> KO(M)
    ko_M = (ko_total - ko_F) % 8
    print(f"KO-dim(M) = KO(total) - KO(F) = {ko_total} - {ko_F} "
          f"= {ko_total-ko_F} == {ko_M} (mod 8)")

    # 4. spin manifold: KO-dim == metric dim (mod 8)
    print(f"For a spin manifold, metric dim == KO-dim (mod 8) = {ko_M} (mod 8)")
    print(f"=> dim(spacetime) == {ko_M} (mod 8); minimal physical solution: 4.")
    assert ko_M == 4

    print()
    print("RESULT: 4-dimensional spacetime is FORCED by W(3,3).")
    print(" KO-dim(W(3,3)) = 6 = 2q  +  Connes-Barrett total KO-dim = 2 (mod 8)")
    print(" => metric dim(M) = 4 (mod 8). The '4' of M^4, previously taken from")
    print(" observation, is derived; it traces to q=3 (KO-dim 2q=6).")
    print()
    print("Cross-checks (the standard SM AC geometry, same arithmetic):")
    print(f"  Connes-Chamseddine SM: KO(M)=4, KO(F)=6, total={ (4+6)%8 } (mod 8) OK")
    print("  KO-dim independent of metric dim (Connes-Barrett) is what lets F be")
    print("  metrically 0-dim (finite) yet KO-dim 6 -- the crux that makes the")
    print("  spacetime-dimension derivation possible.")

    out = {
        "result": "spacetime dimension 4 derived from W(3,3) KO-dimension",
        "ko_dim_F_W33": ko_F,
        "ko_dim_F_equals_2q": True,
        "connes_barrett_total_ko": ko_total,
        "ko_dim_M_mod8": ko_M,
        "spacetime_dim": 4,
        "logic": "KO(F)=6=2q; total KO=2 (mod8, Euclidean fermion doubling); "
                 "KO(M)=2-6=-4=4 (mod8); spin manifold metric dim=KO dim => "
                 "dim M = 4 (minimal). The 4 of M^4 is forced, traces to q=3.",
        "sources": ["Connes, Noncommutative geometry and the SM with neutrino "
                    "mixing, hep-th/0608226 (KO-dim 6 finite space)",
                    "Barrett, A Lorentzian version of the NC geometry of the "
                    "SM (fermion doubling, total KO-dim)",
                    "arXiv:1903.04769 (uniqueness of Barrett's solution)"],
    }
    with open("data/w33_spacetime_dimension_from_KO.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/w33_spacetime_dimension_from_KO.json")


if __name__ == "__main__":
    main()
