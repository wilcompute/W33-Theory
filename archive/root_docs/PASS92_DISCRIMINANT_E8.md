# Pass 92 — The discriminant form of the code-lattice IS the E₈/2E₈ form (O⁺₈(2))

**Status: PASS** — witness `w33_pass92_discriminant_e8.py` (7/7 checks), test
`tests/test_pass92_discriminant_e8.py` (5/5). Self-contained (GF(2) linear algebra).

This resolves the "why does 8 appear everywhere?" question — the glue dimension, the binary code's
minimum distance d = 8, and the E₈ rank are **one object**.

## The computation
The Construction A even lattice Λ_C of C₂(W) = [40,16,8] (Pass 87) has det = 2⁸ and discriminant
group Λ*/Λ = **C⊥/C = (ℤ/2)⁸**. Its discriminant *form* is read off the 256 coset minimum-weights:

| coset weight | count | meaning |
|---|---|---|
| 0 | 1 | zero coset |
| **6** | **120** | norm 1, **anisotropic** (Q=1) = 2⁷−2³ |
| **8** | **135** | nonzero **isotropic** (Q=0) = (2⁴−1)(2³+1) = 15·9 |

with 120 + 135 = 255 = 2⁸−1. Setting Q(v) = (norm/2) mod 2, this is the nondegenerate **plus-type
quadratic form O⁺₈(2)**: 135 isotropic + 120 anisotropic are exactly its counts.

## It is the E₈/2E₈ form
E₈ is even unimodular of rank 8; **E₈/2E₈ = F₂⁸ carries the quadratic form N(x)/2 mod 2 with
precisely 120 norm-1 (anisotropic) and 135 nonzero isotropic vectors**, and O⁺₈(2) acts (the
isotropic-vector graph is SRG(135,70,37,35)). So the discriminant form of the W(3,3) code-lattice
**equals** the E₈/2E₈ form, and:
- the **120 anisotropic** glue vectors are the **240 E₈ roots mod ±1** (240/2 = 120);
- the **135 isotropic** are the E₈/2E₈ isotropic vectors.

## Why it matters
The pervasive **8** of the whole arithmetic tower — glue dimension of the code-lattice, code minimum
distance d=8, E₈ rank — is a single fact: **the discriminant form of the Construction-A lattice of
C₂(W) is the E₈/2E₈ = O⁺₈(2) form.** Combined with Pass 91 (Aut(W) = W(E₆)), W(3,3) now visibly sits
at the confluence of **E₆** (symmetry, 45 tritangent planes) and **E₈** (the 240 roots, both as the
dual-code minimum words of Pass 86 and now as the anisotropic glue vectors mod 2).

## Grounding (internet)
E₈ lattice (Wikipedia / HandWiki): E₈/2E₈ has 120 norm-1 and 135 nonzero isotropic vectors under
O⁺₈(2); the 270 maximal isotropic 4-spaces split into two O⁺₈(2)-orbits of 135.

## Files
- `w33_pass92_discriminant_e8.py`, `.json` — witness (7 checks).
- `tests/test_pass92_discriminant_e8.py` — 5 assertions.
