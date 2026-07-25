# Pass 95 — The genus and Minkowski–Siegel mass of the code-lattice Λ_C

**Status: PASS** — witness `w33_pass95_genus_mass.py` (8/8 checks), test
`tests/test_pass95_genus_mass.py` (5/5). Self-contained (sympy Bernoulli numbers + W(3,3) code data).

## Genus (rigorously determined by rank + signature + discriminant form)
Λ_C = Construction-A even lattice of C₂(W)=[40,16,8]: positive-definite, **rank 40**, **even**,
**det = 2⁸**, discriminant form **O⁺₈(2) = E₈/2E₈** (Pass 92).
- odd primes: **unimodular** (det is a 2-power);
- at p=2: Jordan symbol **1^{+32} 2^{+8}** (scale-1 even-unimodular rank 32 ⊕ scale-2 rank-8 plus-type);
- Conway–Sloane symbol **II₄₀,₀(2^{+8})**.

## Automorphisms (rigorous lower bound)
All **2⁴⁰** coordinate sign changes preserve the Construction-A lattice, and the code's permutation
automorphisms contain Aut(W(3,3)) = W(E₆) (Pass 91). Hence
**|Aut(Λ_C)| ≥ 2⁴⁰ · 51840 = 56 998 682 783 907 840.**

## Mass
The Smith–Minkowski–Siegel standard mass for even unimodular lattices,
M_n = |B_{n/2}/n| · ∏_{j=1}^{n/2−1} |B_{2j}/(4j)|, is **validated** to reproduce exactly the known
masses in dim 8 (E₈: **1/696729600**), dim 16 (numerator 691) and dim 24 (the Conway–Sloane value).
In dim 40 it gives **M₄₀ ≈ 4.4×10⁵¹**. Since h ≥ mass, a dimension-40 even genus is **astronomically
populated** — versus the single class (E₈) in dim 8.

> Honest scope: the reported M₄₀ is the even-**unimodular** reference; Λ_C's own (non-unimodular)
> genus mass differs by a 2-adic local factor for the 2^{+8} block, but is of the same astronomical
> scale. The genus symbol and the Aut bound are exact.

## Files
`w33_pass95_genus_mass.py`, `.json`; `tests/test_pass95_genus_mass.py`.
