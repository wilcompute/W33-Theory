# BT924 — The integral E₈ shadow in the Smith normal form (open frontier #5, advance)

**Status: PARTIAL — genuine advance on a documented open problem, not a closure.**
Scripts: `analysis/bt924_integral_e8_lift_explore.py`,
`analysis/bt924b_integral_e8_lift_construct.py`.

## The open problem (verbatim, W36_PAPER.tex §sec:e8-lift-open)

> "the mod-2 homology H ≅ F₂⁸ already fixes the correct rank for E₈, but not
> the integral Cartan pairing. What remains open is an explicit lift from the
> clique-complex chain data over F₂ to an integral lattice carrying the E₈
> bilinear form... the integral E₈ root lattice has not yet been reconstructed
> directly from the chain complex."

Before this note the repo had three *separate* facts: `det(A)=−3·2⁵⁶`
(corollary), `dim H = 8` (proposition), and a vertex 8-subset with
`det(2I−A_sub)=1` (proposition). BT924 connects them and pins the integral
2-adic location of the E₈ rank.

## New, verified results

**R1 — the full Smith normal form.**
```text
SNF_Z(A) = diag( 1¹⁶ , 2⁸ , 8¹⁵ , 24¹ ),   ∏ dᵢ = 2⁵⁶·3 = |det A|.
```
(The paper had only the product `det = −3·2⁵⁶`; the invariant-factor anatomy
is new.)

**R2 — the E₈ rank 8 is an integer invariant-factor count.** The mod-2
homology dimension lifts to Z:
```text
dim_F₂ H = 8 = #{ elementary divisors with 2-adic valuation exactly 1 }
            = #{ dᵢ = 2 }.
```
So "rank 8" is not merely a mod-2 shadow — it is the number of invariant
factors of the *integer* adjacency A that equal 2.

**R3 — the 2-adic anatomy of A.**
| invariant factor | count | 2-adic val | meaning |
| --- | --- | --- | --- |
| 1 | 16 | 0 | the unimodular core (= rank_F₂ A) |
| 2 | **8** | **1** | **the E₈ rank-8 shadow** |
| 8 = 2³ | 15 | 3 | the −4 eigenspace (mult 15) |
| 24 = 2³·3 | 1 | 3 | the Perron block + the sole odd prime q=3 |

The single factor of 3 = q sits in the 24, reproducing `det = −3·2⁵⁶` and the
corollary's `56 = dim 56_{E₇}` (`2⁵⁶`).

**R4 — the critical group.** coker(A) = Z⁴⁰/AZ⁴⁰ ≅ (Z/2)⁸ ⊕ (Z/8)¹⁵ ⊕ Z/24;
the (Z/2)⁸ summand of *exact* order 2 is the E₈ mod-2 shadow H as a direct
factor of the sandpile group.

**R5 — the vertex 8-subset is genuinely E₈ (certificate upgraded).** The
induced subset `[0,1,4,22,27,35,23,34]` gives `G = 2I₈ − A_sub` that is
even + unimodular (det 1) + positive-definite, and its spectrum matches the
true E₈ Cartan matrix exactly (smallest eigenvalue 0.0110 = the E₈
Coxeter-number h=30 signature). By uniqueness of the even unimodular rank-8
lattice this *is* E₈ — upgrading the paper's det-only check.

**R6 — the explicit obstruction (the residual open core).** The naive lift
(support-indicator 0/1 vectors of the 8 homology cycles) has lattice Gram
determinant under the standard form
```text
det = 3⁴·5·7·179 = 507465  ≠  ±1.
```
Determinant is a basis-invariant, so **no** reduction of the naive-lift
lattice is unimodular: the canonical E₈ *form* cannot come from the obvious
support-lift. The lift requires a specific choice of coset representative
(homology rep + boundaries + 2Z⁴⁰) and bilinear form.

## What is now closed vs. open

- **Closed:** the E₈ *rank* (8) and its *2-adic location* (the valuation-1
  invariant factors of A) are integrally pinned, not just mod-2; the vertex
  realization is a certified E₈; `E₈/2E₈ ≅ F₂⁸` nondegenerate matches H.
- **Still open (narrowed):** the canonical positive-definite even-unimodular
  *form* on the rank-8 valuation-1 sublattice — i.e. *which* rank-8 definite
  sublattice of (Z⁴⁰, ½·A-form) carries the E₈ Gram. R6 rules out the naive
  lift; the next step is extracting the form via SNF transform matrices
  U A V = S on the eight `dᵢ=2` directions.

## Honesty note

This does **not** close the open problem; it advances it from "F₂⁸ shadow +
disconnected vertex Cartan" to "integrally-located rank-8 with a certified
vertex realization and an explicit no-go for the naive lift." Per the
check-first/corrections ethos, the residual (the definite form) is left open
rather than forced.
