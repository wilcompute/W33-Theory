# The spread obstruction in `W(q,q)` — a standalone note

**Scope.** This note collects the results of Passes 1612–1916 that are specific to
`W(3,3)` and its generalisations, with prior art fixed. It exists because Pass
1912 and Pass 1917 found that a neighbouring arc had already been done — once in
the literature and once *in this repository* — and scattered results are exactly
what makes that happen.

Everything below is about the **frame graph** and the **signed edge module** of
the symplectic generalised quadrangle, and survived a corpus check, a guard
sweep, and a literature check.

---

## 0. What is NOT ours — the boundary, drawn explicitly

Pass 1917 searched the corpus for the *result* rather than the topic and found
`analysis/2026-07-15_pass355_sp43_frobenius_schur.md`, dated 15 July, which
already contains:

| statement | owner |
|---|---|
| `Sp(2n,q)` has non-real characters iff `q ≡ 3 (mod 4)` | **Gow (1985)**, cited in Pass 353/355 |
| twisted Frobenius–Schur framework | **Vinroot (2005, 2010)**, cited in Pass 355 |
| Weil pieces `W₊, W₋` are an `FS = 0` complex-conjugate pair | **Pass 355** |
| "the pair is self-conjugate, each piece is not — so a choice is required" | **Pass 355** |
| `(q²+1)/2` as the distinguished degree forcing `q = 3` | **Pass 227** |
| the substrate cannot select chirality internally | **Pass 346** |

**Passes 1900, 1907 and 1914 are therefore retracted as novel.** They re-derive,
for the edge module, what Pass 355 established for the Weil representation, using
citations Pass 355 already carried. The July arc was filed under dated filenames
with no topical signal, which is the documented reason topic-searching fails
here; the fix that worked was searching for `Gow`, `Frobenius`, and `Weil` as
*results*.

---

## 1. The frame graph is 240 edge-disjoint 9-cliques

Let `H` have the 540 frames (unordered pairs of disjoint totally isotropic lines)
as vertices, adjacent when their canonical cross-matchings share an edge.

**Proposition.** Each of the 240 edges of `W(3,3)` lies in exactly 9 frames, all
mutually adjacent; `H` is 32-regular; and `32 = 4 × 8` forces any two adjacent
frames to share exactly one edge. Hence `H` is exactly the union of 240
edge-disjoint 9-cliques.

*Verified:* the 240 cliques cover 8,640 pairs, equal to `|E(H)|`, with no
duplication.

**Corollary.** `χ(H) = 9` iff 540 variables in `1..9` satisfy 240
`AllDifferent(9)` constraints — replacing the 4,860-variable / 99,909-clause CNF
used by earlier attempts.

---

## 2. A spread's `K₁₀` is maximal but not maximum

**Theorem.** Let `S` be a spread of `W(q,q)` — its `q²+1` lines partition the
points. All `C(q²+1, 2)` pairs are frames, and they form an **independent set of
`H`**. Their matchings cover exactly the edges lying off `S`'s own lines, leaving
the `(q²+1)·C(q+1,2)` edges lying on them.

For `q = 3`: 45 frames, covering 180 edges, leaving 60. Exactly 15 frames lie
inside those 60 and `15 × 4 = 60` — perfect arithmetic — yet **there are no
completions**, and not narrowly: the 15 candidates touch only 20 of the 60 edges,
so 40 lie in no admissible frame at all.

> Every spread's `K₁₀` is a **maximal independent set of size 45** in a graph with
> `α(H) = 60`. Verified for all 36 spreads.

This names a reason five earlier resolution searches stalled: `H` has at least 36
highly symmetric traps that a greedy or DFS search enters and cannot locally
leave. Measured: 4,000 random greedy runs never reached 60, topping out at 49.

---

## 3. The `1/q` law and its mechanism

**Theorem.** For `q ∈ {3, 5, 7}` the admissible completing frames number exactly
`(q²+1)q/2` — precisely the number needed — yet the edges they touch number
`(q+1)(q²+1)/2 = |points|/2`, a fraction `1/q` of the leftover, with multiplicity
exactly `q`.

*Measured:* `20/60 = 1/3`, `78/390 = 1/5`, `200/1400 = 1/7`.

**Mechanism.** The touched edges form a perfect matching **within each spread
line**, of size `(q+1)/2`. Such a matching exists iff `q+1` is even, i.e. `q` odd.
For `q` even a line has an odd number of points, no matching exists, and there are
**no candidates at all** — the measured `q = 2` case, which is the theorem's other
branch rather than an exception.

---

## 4. `σ_S`: the obstruction's generator

**Theorem.** Each spread `S` carries a canonical collineation `σ_S`, and the
candidate frames' matching edges are exactly its 2-cycles.

- `σ_S` is a fixed-point-free involution fixing every line of `S` (verified
  `q = 3, 5, 7`).
- The subgroup of collineations fixing every line of `S` is exactly `C₂`, and
  `σ_S` generates it and lies in the centre of `Stab(S)` (order 1440).
- `σ_S` is induced by a **symplectic similitude** `g` with `g² = μI`, `μ` a
  **non-square** multiplier. A projective fixed point would need `λ² = μ` with
  `λ ∈ F_q`, impossible; and a non-square multiplier is exactly what makes `g`
  outer in `PGSp`. In characteristic 2 there are no non-squares, giving the even
  branch again.

**Corollary (`q = 3`).** The 36 `σ_S` are exactly the 36 images of the 72
similitudes with `g² = μI` and non-square multiplier — a bijection with the
spreads. The *other* 540 solutions, with square multiplier, are symplectic, map
to 270 inner involutions, and index the 270 ordered incident line-pairs of the
27 lines on a cubic surface.

> One equation, `g² = μI`, split by the quadratic character of the multiplier,
> yields the 27-lines geometry and the spread geometry.

*Prior-art caution:* the vocabulary here (symplectic spreads, Desarguesian
spreads, `GSp` multipliers, a fixed non-square `ξ`) is entirely standard, so this
correspondence should be treated as **likely known** pending a proper reference,
not as new.

**Connection.** At `q = 3`, `σ_S` fixes 0 points and 10 lines — precisely the
size-36 outer class that is one of only two classes sensitive to the substrate's
full handedness. The element generating the resolution obstruction and the
element reading the chirality are the same.

---

## 5. The signed edge module

Over `PGSp(4,3)` the orientation-signed 240-edge module is multiplicity-free:

```text
V = 15 ⊕ 24  |  81  |  30 ⊕ 90
    (exact)   (harmonic)  (coexact)
      39          81         120
```

- The gauge block `15 ⊕ 24` is the nontrivial part of the 40-point permutation
  module, i.e. `d(functions on points)`; `40 − 1 = 39 = 15 + 24`.
- `Res_PSp(90) = 45 ⊕ 45̄`, a genuine complex-conjugate pair, and
  `dim_ℝ End_PSp(90) = 2`, so `End_ℝ ≅ ℂ` and the invariant complex structures
  are exactly `±J`.
- **The 81 and the 15 are odd-dimensional, so they admit no invariant complex
  structure at any subgroup whatever** — the obstruction is parity, not
  representation theory.
- A permutation module has a canonical permuted basis and is therefore real, so
  no `G`-set — points, lines, octets, spreads, frames, incident pairs — can carry
  a complex pair. **Only an orientation-signed module can.**

The last two points are the part of the chirality arc that is about *this module*
rather than about `Sp(4,q)`, and they survive the Pass 1917 boundary.

---

## 6. Open

- `χ(H) = 9`. Undecided. Best encoding branches on the spread-pair counts
  (60,909 branches vs 2,127,575 plain); free cuts provably cannot help, since a
  cut is free exactly when the spectral relaxation already implies it; prescribed
  automorphisms all fail the clique test; `CP-SAT` symmetry levels 0/2/4 all
  return `UNKNOWN`.
- Whether `max |class ∩ K₁₀| = 13`. 13 is attained; `≥ 14` is undecided.
- A written proof, rather than three verifications, that the candidate matchings
  must lie inside a spread line's perfect matching.

---

*Passes 1612–1916, glue track. Prior art: Gow (1985); Vinroot (2005, 2010);
in-repo Passes 227, 346, 353, 355 (chirality/Weil), BT773 (frame involutions),
BT790/BT795 (spreads and the `K₁₀`), BT794 (transversals), Pass 328 (guard
calibration), Passes 1541/1606/1607 and 1841–1845 (parallel track: octets, the
`195→225` gain, certified signature resolutions).*
