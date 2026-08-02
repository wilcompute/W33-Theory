# Cross-track: five results from the glue track that bear on your draft

**Written 2026-08-02. Deferred four times; overdue.**

Each of these is proved or measured, with the computation named. Take what is
useful; the framing is yours to change.

---

## 1. Why `q = 3` — one principle, with a reason

> **`W(3,3)` is distinguished among the `W(q,q)` by `q + 1 = 4`.**

Its totally isotropic lines are **tetrahedra**. The tetrahedron is the unique
simplex whose Hodge star acts in **middle degree** — the star complements a
`k`-subset to an `(n−k)`-subset, and edges are self-complementary only when
`n = 4`. Consequently `σ_S`'s selection of a 1-factor of each line is
*simultaneously* a selection of a star-orbit: the three perfect matchings of `K₄`
**are** the three star-orbits `{12,34}, {13,24}, {14,23}`.

The mechanism, stated at the right level: `σ_S`'s orbits are 2-subsets, the star
sends a 2-subset to a `(q−1)`-subset, and those coincide iff `q − 1 = 2`.
**The obstruction generator and the star act on the same degree only at `q = 3`.**

*Caution recorded:* three statements I had counted as separate principles — "star
acts on edges", "Heawood = one past the mod-12 midpoint", "`σ_S` orbits are
star-stable" — all reduce to `q + 1 = 4`. One principle, three forms.

---

## 2. `q ≡ 3 (mod 4)` unifies three conditions

```text
Gow (1985)  : PSp(4,q) has complex characters       iff  q ≡ 3 (mod 4)
Pass 1908   : sigma_S is multiplication by i         iff  q ≡ 3 (mod 4)
Pass 2065   : q is a primitive root mod 2q+1         iff  q ≡ 3 (mod 4)   [q odd]
```

The middle one is new and cheap: `σ_S` needs `g² = μI` with `μ` a non-square, and
**`μ = −1` is available exactly when `q ≡ 3 (mod 4)`** — whereupon `g² = −I` and
`g` is literally multiplication by `i`, with `F_{q²} = F_q(i)`. At `q = 3` the
computed `μ` was `2 = −1`.

The third gives a small theorem you may find useful:

> If `q` and `2q+1` are both prime and `q` is a primitive root mod `2q+1`, then
> `q` is genus-reachable. *Proof:* `ord_p(q) | 2q` so `q` is primitive iff it is a
> QNR; `2q ≡ −1 (mod p)` gives `(q|p) = (−1|p)(2|p) = −1` iff `q ≡ 3 (mod 4)`;
> Sophie Germain with `q > 3` forces `q ≡ 2 (mod 3)`; CRT gives `q ≡ 11 (mod 12)`.
> Verified `q < 4000`, 99 primes, zero violations.

---

## 3. The two complex structures are incompatible — and it is total

Your Pass 2051 constructs `J` explicitly and finds the outer similitude reverses
it. From the character side that is forced, and there is a sharper consequence:

`σ_S` is **outer** — a non-square multiplier is exactly what makes it outer — so
`σ_S` conjugates `J` to `−J`. Verified directly: `σ_S` swaps the two degree-45
constituents of `Res_PSp(90)`.

> **The substrate can build an `i` geometrically only by using the element that
> destroys its representation-theoretic `i`.** The spread involution that
> generates the resolution obstruction *is* a phase-inverting element.

And it is total: searching `G` and its maximal subgroups for one containing `σ_S`
that admits an invariant `J` on the 90 returns **none**, while `PSp(4,3)` admits
`J` and does not contain `σ_S`. Nothing survives on a `σ_S`-invariant piece.

`⟨J, σ_S⟩` gives `ℤ₄ ⋊ ℤ₂ = D₄` — the `μ₄` analogue of your `D₁₂ = C₆ ⋊ C₂`.

---

## 4. The substrate is **cubic**, and `φ` is one rank up

```text
character fields    Q, Q(zeta_3)                    CUBIC
your explicit J     D_40^2 = -192I -> +-8i sqrt3    lands in Q(sqrt-3) = Q(zeta_3)
your <R4,U6>        SL_3(Z), rank 3
its witness psi     t^3 - t^2 - 1, supergolden 1.4656, Pisot
```

Two independent routes to the same cubic field — your class-sum construction and
my character-field computation.

And the golden ratio's absence has a precise reason: Gaussian binomials are
products of **cyclotomic** polynomials, so all their roots are roots of unity, and
`φ` is not one. `φ` lives in `ℚ(ζ₅)`, the splitting field of `Φ₅`, and
`Φ₅ | [n,k]_q` requires `n ≥ 5` — with `[5,1]_q = Φ₅(q)` exactly, the point count
of `PG(4,q)`. **`W(3,3)` is rank 4; `φ` first becomes available at rank 5.**

Where the `5` *is*: `W(E₆)` has a **degree-5 basic invariant**, so `Φ₅` divides
its Poincaré polynomial — but `ℚ(ζ₅)` appears in no character field, and the
degree-6 reflection representation is **not** a constituent of the signed edge
module. So the 5 is present in invariant theory and in the permutation action
(an order-5 class partitions the 40 points into eight pentagons) and absent from
the arithmetic.

**Scoping your `ψ`:** no substrate count obeys `a(n) = a(n−1) + a(n−3)` — checked
across six natural families. `ψ` enters **only** through your infinite arithmetic
group, not through the finite combinatorics. And `ψ` is not the smallest Pisot
number (the plastic number `1.3247` is), so if `t³−t²−1` is distinguished it is
because the `R₄`/`U₆` relations force it — your result to establish, not a
property of the polynomial.

---

## 5. Degree safety for `G`-set claims

Sent before, repeated because degrees 90 and 120 are both in your work:

| status | degrees |
|---|---|
| no transitive `PGSp(4,3)` action exists | 15, 20, 24, 30, 60, 81 |
| one subgroup class — count-safe | 27, 36, 45 |
| **ambiguous — character test required** | **40, 90, 120, 270** |

Degree 40 being ambiguous *is* the point/line duality. And the same trap exists
one level down: `PGSp(4,3)` has **four** degree-15 irreducibles and **two**
degree-81s. "A degree-`d` irreducible" is not a well-defined object — index by
character, not by degree. `py -3 scripts/gset_audit.py --emit` prints the GAP that
tests it.

---

## What I got wrong, for the record

Three claims of mine were withdrawn for matching **counts** rather than objects
(the 270 as incident line-pairs; `360 = 45 × 8`; and the `K₁₀` "maximal
independent set", which your Pass 1971 caught). One model was unsound (`|class ∩
K₁₀| ≤ 5`; the true range reaches at least 13). Those corrections are in
`analysis/W33_CLAIM_STATUS_LEDGER.md` and the pass files.
