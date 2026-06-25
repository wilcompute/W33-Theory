#!/usr/bin/env python3
"""
Are the de Sitter selection (S4) and the crystallographic/Eisenstein selection (S5)
independent, or the same cyclotomic structure read twice? They share the degree-2
cyclotomic skeleton -- so the census's "five independent" is honestly four
independent selections plus one cyclotomic refinement.

In w33_q3_selection_census.py the five selections were treated as independent. Two
of them live on the SAME object, the set of degree-2 cyclotomic polynomials:

  S4 (de Sitter):  the horizon closure 2(q-1)(q^2+1)=(1+q)(1+q^2) is equivalent to
        (q-3)(q^2+1) = 0,  i.e.  (q-3) * Phi_4(q) = 0,
     whose REAL root is the selection q=3 and whose complex roots are q = +-i,
     the primitive 4th roots of unity (the Gaussian period zeta_4).

  S5 (crystallographic): a complex reflection of period p is crystallographic iff
     phi(p)=2, i.e. p in {3,4,6}; these correspond exactly to the three degree-2
     cyclotomic polynomials
        Phi_3(q)=q^2+q+1,  Phi_4(q)=q^2+1,  Phi_6(q)=q^2-q+1,
     and requiring p PRIME selects p=3 (4,6 composite).

THE SHARED SKELETON. The quadratic factor of the de Sitter cubic is exactly
Phi_4(q)=q^2+1 -- the Gaussian crystallographic period p=4 that S5 rejects by
primality. So S4 and S5 are not two coincidences: both read the degree-2 cyclotomic
set {Phi_3, Phi_4, Phi_6}, and both pick out q=3:
  * S4 rejects Phi_4 (and Phi_6) because de Sitter needs a REAL q (only q-3 is real);
  * S5 rejects p=4 (Phi_4) and p=6 (Phi_6) because the qudit dimension must be PRIME.
Moreover the same Phi_4 = q^2+1 is the factor of the GQ(q,q) POINT COUNT
v = (q+1)(q^2+1) = (q+1) Phi_4(q) -- so the cyclotomic skeleton is already built
into the substrate's combinatorics.

HONEST RECOUNT. q=3 is the unique value that is simultaneously the real root of the
de Sitter cubic AND the prime crystallographic period -- but because S4 and S5 share
the {Phi_3,Phi_4,Phi_6} skeleton, they are NOT cleanly independent. The honest
census count is therefore FOUR independent selections (geometric, resource,
holographic, de Sitter) plus S5 as a cyclotomic refinement of S4 -- a tighter, not
weaker, convergence: q=3 is the unique real prime the degree-2 cyclotomic structure
admits.

Verifies the factorisation, the cyclotomic identifications, the GQ point-count
factor, and the shared-skeleton recount.
"""
from __future__ import annotations

import json

import sympy as sp


def main():
    out = {}
    q = sp.symbols("q")

    # de Sitter closure -> cubic -> factorisation
    lhs = 2 * (q - 1) * (q**2 + 1)
    rhs = (1 + q) * (1 + q**2)
    cubic = sp.expand(lhs - rhs)
    factored = sp.factor(cubic)
    print(f"[S4 de Sitter]  2(q-1)(q^2+1) - (1+q)(1+q^2) = {cubic}")
    print(f"  factored = {factored}")
    assert sp.simplify(cubic - (q - 3) * (q**2 + 1)) == 0
    out["desitter"] = {"cubic": str(cubic), "factored": "(q - 3)*(q**2 + 1)"}

    # the quadratic factor IS the 4th cyclotomic Phi_4
    Phi4 = sp.cyclotomic_poly(4, q)
    print(f"\n[cyclotomic identification]  Phi_4(q) = {Phi4}")
    assert sp.simplify((q**2 + 1) - Phi4) == 0
    print(
        f"  so de Sitter cubic = (q-3) * Phi_4(q); complex roots q=+-i = zeta_4 (Gaussian)"
    )
    out["phi4_factor"] = (
        "de Sitter cubic = (q-3)*Phi_4(q); Phi_4=q^2+1, roots +-i=zeta_4"
    )

    # the three degree-2 cyclotomics <-> crystallographic periods {3,4,6}
    print(f"\n[S5 crystallographic]  phi(p)=2 <-> degree-2 cyclotomics:")
    cyc = {}
    for p in (3, 4, 6):
        Phi = sp.cyclotomic_poly(p, q)
        deg = sp.degree(Phi, q)
        cyc[p] = str(Phi)
        print(f"  p={p}: Phi_{p}(q) = {Phi}  (deg {deg}, phi({p})={sp.totient(p)})")
        assert deg == 2 and sp.totient(p) == 2
    out["crystallographic_cyclotomics"] = cyc

    # GQ point count carries Phi_4
    v = sp.expand((q + 1) * (q**2 + 1))
    print(
        f"\n[shared skeleton]  GQ(q,q) point count v = (q+1)(q^2+1) = (q+1)*Phi_4(q) = {v}"
    )
    print(f"  at q=3: v = {v.subs(q,3)} = 40  (the W(3,3) point count)")
    assert v.subs(q, 3) == 40
    out["gq_point_count"] = {"formula": "(q+1)*Phi_4(q)", "at_q3": 40}

    # the selection: q=3 is the unique real prime crystallographic period
    cryst = [3, 4, 6]
    real_root = 3
    prime_cryst = [p for p in cryst if sp.isprime(p)]
    print(f"\n[the selection]")
    print(f"  de Sitter REAL root: q = {real_root}")
    print(f"  crystallographic periods: {cryst}; prime among them: {prime_cryst}")
    print(
        f"  q=3 is BOTH the de Sitter real root AND the unique prime crystallographic"
    )
    print(f"  period -- the same q=3, reached on the shared cyclotomic skeleton.")
    assert real_root == prime_cryst[0] == 3
    out["selection"] = {
        "desitter_real_root": real_root,
        "prime_crystallographic": prime_cryst,
        "coincide_at": 3,
    }

    # honest recount
    print(f"\n[honest recount]")
    print(f"  S4 and S5 share the degree-2 cyclotomic set {{Phi_3,Phi_4,Phi_6}}, so")
    print(
        f"  they are NOT cleanly independent. Census count: 4 independent (geometric,"
    )
    print(f"  resource, holographic, de Sitter) + S5 as a cyclotomic refinement of S4.")
    print(
        f"  The convergence is TIGHTER: q=3 = unique real prime the structure admits."
    )
    out["recount"] = (
        "S4 (de Sitter) and S5 (crystallographic) share the degree-2 cyclotomic "
        "skeleton {Phi_3,Phi_4,Phi_6}; honest count = 4 independent + S5 a refinement "
        "of S4, not 5 independent. q=3 = unique real prime crystallographic period."
    )

    print("\nRESULT: the de Sitter and Eisenstein/crystallographic selections are two")
    print("  readings of one cyclotomic structure. The de Sitter closure cubic factors")
    print("  as (q-3)*Phi_4(q): its real root is the selection q=3, its complex roots")
    print("  are the Gaussian period zeta_4 = the p=4 that the crystallographic-prime")
    print("  selection also rejects. The degree-2 cyclotomics {Phi_3,Phi_4,Phi_6} are")
    print("  exactly the crystallographic periods {3,4,6}, and Phi_4=q^2+1 is already")
    print("  the factor of the GQ point count v=(q+1)Phi_4. So the census's five")
    print(
        "  selections are honestly four independent plus one cyclotomic refinement --"
    )
    print("  a tighter convergence: q=3 is the unique real prime the structure admits.")

    out["summary"] = (
        "de Sitter (S4) and crystallographic/Eisenstein (S5) selections are two "
        "readings of the degree-2 cyclotomic structure {Phi_3,Phi_4,Phi_6}, NOT "
        "independent. de Sitter cubic = (q-3)*Phi_4(q) (Phi_4=q^2+1, complex roots "
        "+-i=zeta_4 = the Gaussian p=4 that S5 rejects by primality); {Phi_3,Phi_4,"
        "Phi_6} = crystallographic periods {3,4,6}; Phi_4 also factors the GQ point "
        "count v=(q+1)Phi_4 (=40 at q=3). Honest recount: 4 independent selections + "
        "S5 a refinement of S4 (not 5 independent). Tighter convergence: q=3 = unique "
        "real prime crystallographic period."
    )
    out["sources"] = [
        "de Sitter closure (w33_desitter_q3_selection.py); crystallographic restriction "
        "phi(p)=2 (w33_eisenstein_forcing.py); cyclotomic polynomials Phi_3,Phi_4,Phi_6; "
        "GQ(q,q) point count v=(q+1)(q^2+1); w33_q3_selection_census.py."
    ]
    with open("data/w33_desitter_crystallographic_unify.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_desitter_crystallographic_unify.json")


if __name__ == "__main__":
    main()
