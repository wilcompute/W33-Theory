# Pass 96 — The 2-rank ladder is finer than the two-graph

**Status: PASS** — witness `w33_pass96_switching_ladder.py` (10/10 checks), test
`tests/test_pass96_switching_ladder.py` (5/5). Self-contained (graph6 decode + GF(2) rank + integer
SNF via sympy).

## The question
Pass 89 found the 28 graphs SRG(40,12,2,4) split by 2-rank into a graded ladder **{17, 8, 2, 1}** at
2-ranks **{16, 14, 12, 10}**. Is that partition the Seidel switching-class / two-graph structure?

## Answer: **No — the ladder is strictly finer.**
For the Seidel matrix S = J − I − 2A, switching + relabelling act as S ↦ D P S Pᵀ D (D=diag(±1), P a
permutation), both unimodular, so the **Smith normal form of S** ("Seidel Smith group") is a genuine
switching invariant. Computed over all 28:

> **Seidel Smith group = ℤ/3 ⊕ (ℤ/5)²³ ⊕ ℤ/25 ⊕ (ℤ/7)¹⁵ — CONSTANT across all 28.**

They also share the Seidel spectrum {15, −5²⁴, 7¹⁵}. Yet they fall into {17,8,2,1} by the 2-rank of
the **adjacency** matrix. So the arithmetic ladder is **transverse to** the switching class — it
distinguishes graphs the two-graph cannot.

## Two bonus facts
- **W(3,3)** has 2-rank 16 (the generic class of 17); **Q(4,3) is the unique 2-rank-10 graph** (the
  singleton). The cospectral mates sit at **opposite ends** of the ladder, and Q is characterized as
  the unique minimum-2-rank SRG(40,12,2,4) (its maximal glue, Pass 94).
- **Ducey-type law for the Seidel matrix:** the p-part rank of the Seidel Smith group equals the
  multiplicity of the Seidel eigenvalue divisible by p — 5-part rank 24 = mult(−5), 7-part rank 15 =
  mult(7). The **(ℤ/5)²³** echoes the critical group's constant 5-part (Pass 89, Pass 97).

## Files
`w33_pass96_switching_ladder.py`, `.json`; `tests/test_pass96_switching_ladder.py`.
