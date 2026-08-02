# Pass 2029 — the candidate-orbit property is **proved**, and the `1/q` law is unconditional

The last open step of the spread-obstruction arc closes. What follows is a proof,
not a verification.

---

## The statement

Let `q` be odd, `S` a regular (Desarguesian) symplectic spread of `W(q,q)`, and
`σ_S` the induced fixed-point-free involution fixing every line of `S` (Pass
1908: induced by a similitude `g` with `g² = μI`, `μ` a non-square).

> **Theorem (candidate-orbit property).** Every residual candidate frame is
> `{M, σ_S(M)}` for some line `M ∉ S`.

Open since Pass 1974, where the parallel track correctly identified the gap in my
Pass 1982 argument.

---

## The proof

**Step 1.** A candidate frame `{M, M'}` has all `q+1` cross-matching edges inside
the residual set, i.e. on spread lines. For `p ∈ M` the partner lies on `L_p`, so
`M'` meets `L_p`. Hence `M'` is a **common transversal** of the `q+1` spread
lines `M` meets.

**Step 2** *(standard)*. `M ∉ S` meets exactly `q+1` spread lines, and in a
regular spread those `q+1` lines form a **regulus**.

**Step 3** *(standard)*. A regulus has exactly `q+1` transversals in `PG(3,q)` —
its opposite regulus.

**Step 4** *(this pass)*. **Exactly two of those `q+1` transversals are totally
isotropic.**

Parametrise the quadric by `(su, sv, tu, tv)`, so

```text
ruling A :  L_(s:t) = span{ (s,0,t,0), (0,s,0,t) }     -- the spread lines
ruling B :  N_(u:v) = span{ (u,v,0,0), (0,0,u,v) }     -- the transversals
```

Write `B(x,y) = x J yᵀ` for the symplectic form.

*Ruling A totally isotropic* means `B((s,0,t,0),(0,s,0,t)) = 0` for all `(s:t)`.
Expanding, that is `s²J₁₂ + st(J₁₄ + J₃₂) + t²J₃₄ = 0` identically, forcing

```text
J₁₂ = J₃₄ = 0 ,     J₁₄ = J₂₃ =: c
```

Setting `a := J₁₃`, `b := J₂₄`, the matrix becomes the block form

```text
J = [[0, S], [-Sᵀ, 0]]  with  S = [[a, c], [c, b]] ,   so   det J = det(S)²
```

so **`J` is nondegenerate iff `det(S) = ab − c² ≠ 0`.**

*Transversal isotropy*: `B((u,v,0,0),(0,0,u,v)) = a u² + (J₁₄+J₂₃) uv + b v²`, so

> `N_(u:v)` is totally isotropic **iff** `a u² + 2c·uv + b v² = 0` — a **binary
> quadratic form in `(u:v)`** with discriminant `4c² − 4ab = −4·det(S)`.

Now the two halves:

- **Never exactly one.** Nondegeneracy gives `det(S) ≠ 0`, so the discriminant is
  nonzero and the quadratic has **0 or 2** roots in `PG(1,q)` — never a repeated
  root.
- **At least one.** `M` itself is a totally isotropic transversal, by hypothesis.

**Therefore exactly two.** ∎

**Step 5.** `M` and `σ_S(M)` are both totally isotropic transversals (the latter
because `g` fixes each spread line setwise and maps `M` to a line meeting each
`L_p`). They are distinct since `σ_S` is fixed-point-free. So they *are* the two
roots, and `M' ≠ M` forces `M' = σ_S(M)`. ∎

---

## Verification of the algebra

The coordinate claims were checked exhaustively over all nondegenerate `(a,b,c)`:

```text
   q   nondegenerate triples   mismatches   cases with exactly ONE t.i. transversal
   3                     18            0                                         0
   5                    100            0                                         0
   7                    294            0                                         0
  11                   1210            0                                         0
  13                   2028            0                                         0
```

Zero mismatches on the `J`-shape, on `det J = det(S)²`, and on the root count
predicted by the quadratic character of `−4·det(S)`. **Zero one-root cases**,
which is the load-bearing half.

---

## Consequences

1. **The `1/q` law is unconditional** for every odd `q` and every regular
   symplectic spread. Combined with Pass 2016, its full statement is elementary:
   the residual set is `q²+1` copies of `K_{q+1}`, `σ_S` matches each one, and a
   perfect matching is `1/q` of a complete graph's edges.
2. **The `q`-even branch is unconditional too**: no non-square exists in
   characteristic 2, so no `σ_S`, so no candidates.
3. **A regulus dichotomy, for free.** Reguli of `PG(3,q)` with a totally
   isotropic ruling split by the quadratic character of `−det(S)`: those with
   **two** t.i. transversals, and those with **none**. Only the former arise as
   "the spread lines met by a line of `W(q,q)`" — and the argument above shows
   membership in that class *forces* `−det(S)` to be a square.
4. **`σ_S` gets a regulus definition.** Rather than "the generator of the `C₂`
   linewise stabiliser" (Pass 1894) or "the image of a non-square similitude"
   (Pass 1908):

   > `σ_S` sends each non-spread line `M` to **the other totally isotropic
   > transversal** of the regulus formed by the spread lines `M` meets, and fixes
   > each spread line.

   Three descriptions of one object, and this is the one that makes the
   candidate-orbit property immediate.

---

## What is still standard rather than ours

Steps 2 and 3 are classical projective geometry (regular spreads, reguli and
opposite reguli). Step 4 and the assembly are this pass. The nondegeneracy
argument — that `det J = det(S)²` forces a nonzero discriminant, hence "never
one root" — is the whole content.

---

## Prior art

- Pass 1974 (parallel track) — **owns** the identification of this gap as the
  candidate-orbit property, and was right that my Pass 1982 converse did not hold.
- Pass 1908 — the non-square similitude construction.
- Pass 1894 — the `C₂` linewise stabiliser.
- Pass 2016 — the `K_{q+1}` decomposition, from the user's `66 = C(12,2)`
  observation.
- Pass 2023 — the reduction to a transversal count that made this provable.

## Still open

- `χ(H) = 9`.
- Whether non-Desarguesian symplectic spreads carry a `σ_S` (steps 2–3 assume
  regularity).
