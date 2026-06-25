#!/usr/bin/env python3
"""
Upgrading the Eisenstein selection (S5) from a realization fact to a FORCING
argument -- and showing it is the SAME q=3 as the quantum-resource selection (S2).

In w33_q3_selection_census.py the Eisenstein complex-polytope tower (Moebius-Kantor
-> Hessian -> Witting = 2T -> E6 -> E8) was logged as a *realization* selection:
q=3 is where the named structure exists. Here it becomes a forcing intersection of
two independent first-principles conditions on the reflection ORDER p:

  (geometric / lattice)  CRYSTALLOGRAPHIC RESTRICTION. A complex reflection of
      period p generates a discrete (lattice / crystallographic) group in the plane
      only when zeta_p = e^{2 pi i / p} generates a rank-2 ring over Z, i.e. when
      the cyclotomic degree phi(p) = 2. The genuinely-complex solutions (p >= 3) are
          phi(p) = 2  <=>  p in {3, 4, 6}
      -- exactly the Eisenstein (p=3,6, Z[omega]) and Gaussian (p=4, Z[i]) periods.
      This is the crystallographic restriction theorem (why only 2,3,4,6-fold
      symmetry tiles the plane), here at the level of complex reflections.

  (quantum resource)  PRIME ORDER. The reflection order p is the dimension of the
      qudit / the order of the central phase omega = e^{2 pi i / p}; a clean
      Heisenberg-Weyl-Clifford structure with nondegenerate discrete-Wigner
      (magic / contextuality) support needs p PRIME (S2). Among {3, 4, 6}, only
          3 is prime    (4 = 2^2, 6 = 2*3 are composite).

  INTERSECTION.  crystallographic AND prime  =  {3, 4, 6} cap {primes} = {3}.

So the lattice condition (geometry) and the prime condition (quantum resource) --
the SAME two principles that appear as S5 and S2 in the census -- intersect at a
UNIQUE period, p = 3. The Eisenstein selection is therefore not just "q=3 is where
E8 shows up": it is forced by crystallographic restriction together with primality,
and it is literally the same q=3 as the magic-dimension selection. The realization
follows: p = 3 -> Z[omega] -> the Witting polytope (240 = E8 roots), symmetry the
Shephard-Todd group #32 of order 155520 = 3 x |Sp(4,3)|.

Honest scope: p=4 (Gaussian) and p=6 also give crystallographic complex lattices --
E8 itself carries Eisenstein, Gaussian and order-6 structures -- so the LATTICE
alone does not single out 3; primality does. Equivalently, of the crystallographic
complex periods only p=3 is an odd prime (a minimal magic qudit). The phi(p)=2 set
and the symplectic orders were verified in GAP (gapsystem/gap-docker):
phi: {3,4,6}; primes-in: {3}; |Sp(4,3)|=51840; 3*51840=155520.
"""
from __future__ import annotations

import json

from sympy import isprime, totient


def main():
    out = {}

    # (geometric) crystallographic restriction: phi(p) = 2 for genuinely-complex p
    cryst = [p for p in range(3, 15) if int(totient(p)) == 2]
    print("[crystallographic restriction]  phi(p)=2, p>=3 (genuinely complex):")
    print(f"  p in {cryst}   (Eisenstein p=3,6 -> Z[omega]; Gaussian p=4 -> Z[i])")
    assert cryst == [3, 4, 6]
    out["crystallographic"] = {"condition": "phi(p)=2, p>=3", "set": cryst}

    # (quantum resource) prime order = clean magic qudit
    primes_in = [p for p in cryst if isprime(p)]
    print("\n[prime order]  prime among the crystallographic periods:")
    print(f"  {primes_in}   (4=2^2, 6=2*3 composite; only 3 is prime)")
    assert primes_in == [3]
    out["prime_intersection"] = {"primes_in_cryst": primes_in}

    # the forcing intersection
    forced = sorted(set(cryst) & set(p for p in cryst if isprime(p)))
    print("\n[intersection]  crystallographic AND prime:")
    print(f"  {cryst} cap primes = {forced}   -> p = 3 UNIQUE")
    assert forced == [3]
    out["forced_p"] = forced[0]

    # the realization at p=3
    Sp43 = 51840
    witting = 3 * Sp43
    print("\n[realization at p=3]")
    print(f"  p=3 -> Z[omega] (Eisenstein) -> Witting polytope, 240 = E8 roots")
    print(
        f"  symmetry = Shephard-Todd #32, order {witting} = 3 x |Sp(4,3)| = 3 x {Sp43}"
    )
    assert witting == 155520
    out["realization"] = {
        "ring": "Z[omega] (Eisenstein)",
        "polytope": "Witting 3{3}3{3}3{3}3",
        "vertices": 240,
        "equals_E8_roots": True,
        "symmetry_order": witting,
        "factorization": "155520 = 3 x |Sp(4,3)| = 3 x 51840",
    }

    # link to the census: S5 and S2 are the same q=3
    print("\n[link to the census]")
    print("  S5 (Eisenstein/lattice) and S2 (prime/magic dimension) are not two")
    print("  coincidences but ONE intersection: crystallographic cap prime = {3}.")
    print("  S5 is upgraded from a realization fact to a forcing argument.")
    out["census_link"] = (
        "S5 (crystallographic) AND S2 (prime) intersect uniquely at p=3; S5 upgraded "
        "realization -> forcing"
    )

    # GAP cross-check (run separately via docker; recorded here)
    out["gap_verified"] = (
        "GAP gapsystem/gap-docker: Filtered([2..14],p->Phi(p)=2)=[3,4,6]; "
        "Filtered(that,IsPrimeInt)=[3]; Size(Sp(4,3))=51840; 3*51840=155520"
    )

    print("\nRESULT: the Eisenstein selection is forced, and it is the magic-dimension")
    print(
        "  selection in disguise. Crystallographic restriction (phi(p)=2) admits only"
    )
    print("  the complex periods p in {3,4,6}; requiring the reflection order to be")
    print("  PRIME -- the minimal-magic / clean-qudit condition -- leaves p=3 alone")
    print("  (4 and 6 are composite). So the geometric lattice condition and the")
    print("  quantum-resource prime condition, independent in origin, intersect at a")
    print("  unique p=3, which then realizes Z[omega], the Witting polytope, and E8")
    print(
        "  (240 roots, symmetry 155520 = 3 x |Sp(4,3)|). Two of the census selections"
    )
    print("  collapse into one forcing statement.")

    out["summary"] = (
        "Eisenstein selection upgraded realization -> FORCING, and unified with the "
        "magic-dimension selection. Crystallographic restriction phi(p)=2 admits "
        "complex periods p in {3,4,6} (Eisenstein 3,6 / Gaussian 4); requiring p PRIME "
        "(minimal-magic qudit, S2) leaves {3} uniquely (4,6 composite). So geometry "
        "(lattice) cap resource (prime) = {3}, realizing Z[omega] -> Witting (240=E8 "
        "roots, sym 155520=3x|Sp(4,3)|). GAP-verified (gap-docker): phi-set {3,4,6}, "
        "primes-in {3}, |Sp(4,3)|=51840. Honest: p=4,6 are also crystallographic (E8 "
        "has Gaussian+Eisenstein structures); primality is what singles out 3."
    )
    out["sources"] = [
        "crystallographic restriction theorem (phi(p)=2 <=> p in {3,4,6} for complex "
        "periods); Coxeter, Regular Complex Polytopes (Witting 3{3}3{3}3{3}3, "
        "Eisenstein Z[omega]); Shephard-Todd #32 order 155520; discrete Wigner / magic "
        "needs prime dimension (Gross; Howard et al.); GAP gapsystem/gap-docker; "
        "w33_q3_selection_census.py, w33_q3_triple_selection.py."
    ]
    with open("data/w33_eisenstein_forcing.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_eisenstein_forcing.json")


if __name__ == "__main__":
    main()
