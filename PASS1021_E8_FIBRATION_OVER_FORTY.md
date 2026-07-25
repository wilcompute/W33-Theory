# Pass 1021 — the E8 roots fiber 6:1 over the W(3,3) points, and it is the points, not the lines

**Certificate:** `analysis/w33_pass1021_e8_fibration_over_forty.g` →
`data/w33_pass1021_e8_fibration_over_forty.json` (9/9 checks, **deterministic**, GAP 4.16.0, 33 s)

---

## The result

Pass 1020 refuted the edge↔root bijection: the 240 W(3,3) edges carry rank 10 and
the 240 E8 roots carry rank 13, so no equivariant bijection exists. That was the
negative half. This is the positive half — **the correspondence does exist, one
level down.**

> **Theorem.** There is a 6:1 `Sp(4,3)`-equivariant fibration
> **240 E8 roots → 40 W(3,3) points**, factoring as `240 → 120 → 40`, whose fibre
> is the Eisenstein unit group `⟨−1, ω⟩ ≅ ℤ₆`. The quotient action is
> `PSp(4,3) = U4(2)` of rank 3 with subdegrees `[1, 12, 27]`, and its valency-12
> orbital graph is `srg(40,12,2,4)`. The quotient is conjugate in `S₄₀` to the
> **point** action of the quadrangle, **not** to its dual line action; the two are
> non-conjugate. The full normaliser `N_{W(E8)}(⟨ω⟩)` maps onto
> `W(E6) = U4(2):2` of order 51840, the automorphism group of the base.

So `240 = 40 × 6`, with the 6 exactly the units of `ℤ[ω]`.

## The two groups of order 51840 were never in conflict

This is what makes Pass 1020's dichotomy finally make sense. The corpus spent
years asserting `Sp(4,3) ≅ W(E6)` because both act on the picture with order
51840. They are not isomorphic — and they are not competing. **They sit at two
different levels of one fibration:**

| level | set | group | rank |
|---|---|---|---|
| total space | 240 E8 roots | `Sp(4,3) = 2.U4(2)` | 13 |
| fibre | `⟨−1, ω⟩` | `ℤ₆` (Eisenstein units) | — |
| base | 40 W(3,3) points | `W(E6) = U4(2):2` | 3 |

`Sp(4,3)` is the symmetry of the total space; `W(E6)` is the symmetry of the base.
The map `Sp(4,3) → U4(2)` has kernel `⟨−1⟩` — the antipodal map, which is exactly
what dies on the base. The extra `ω` and the complex conjugation that complete
`U4(2)` to `U4(2):2` live in the normaliser, not in `Sp(4,3)`. **Neither group was
ever wrong; each was being attached to the wrong level.**

## The construction is canonical, not a search

The order-3 element is not found by random search. Let `c` be the Coxeter element
(the product of the eight simple reflections). Then, all verified as hard
assertions:

```text
Order(c)  = 30 = h(E8)
c^15      = the antipodal map −1   (the longest element w₀)
c^10      = regular of order 3, fixed-point-free on the 240 roots
⟨c^5⟩     = ⟨−1, c^10⟩ = ℤ₆        (order 6)
```

So the fibre group **is** `⟨c⁵⟩`, and the whole certificate is deterministic —
byte-identical across runs, unlike Pass 1020's randomised element.

## Which 40? The points

For odd `q` the quadrangle `W(q,q)` is **not** self-dual (its dual is `Q(4,q)`), so
the 40 points and the 40 totally isotropic lines give two degree-40 actions. Both
collinearity graphs are `srg(40,12,2,4)` — parameters cannot separate them. The
certificate therefore decides by **conjugacy of the actions in `S₄₀`**, which is
decisive:

| test | result |
|---|---|
| E8 quotient conjugate to the **point** action | **true** |
| E8 quotient conjugate to the **dual line** action | **false** |
| point and line actions conjugate to each other | **false** |

E8 selects the points. This is the `p40a`/`p40b` question from Pass 338, settled
here from inside `W(E8)` rather than by ATLAS lookup — necessary, because Pass
1020 showed Pass 338's degree-240 labels are interchanged, so its `p40a`/`p40b`
assignment could not be trusted and was re-derived from scratch.

### The same answer, confirmed a second way — and it names a vacuum

`analysis/BT812_five_vacua.md` already tabulates the orbit anatomies of all five
maximal subgroup classes of `PSp(4,3)`, and records exactly this dichotomy:

```text
index 40  (point parab) points [1, 12, 27]   lines [4, 36]
index 40  (line parab)  points [4, 36]       lines [1, 12, 27]
```

The E8 quotient computes point-subdegrees `[1, 12, 27]`. By BT812's table that is
the **point parabolic** — an independent confirmation of the `S₄₀` conjugacy
test, from a witness written for an unrelated purpose.

BT812 names that class *"the holonet split: 40 = 1 + 12 + 27 (self + gauge shell +
matter shell)"* and observes that the architecture's foundational decomposition is
*"one of five, not the only one"*, calling the other four a vacuum degeneracy.
This pass removes the degeneracy **for anything that has to sit under E8**: of the
five vacua, the E8 fibration lands on the point-parabolic one and no other. The
split the architecture was already built on is the one E8 forces.

## Prior art — cited, not reclaimed

The rediscovery guard and a targeted grep both fired here, and correctly:

- `archive/documents/W33_COMPLETE_THEORY.tex:198,708,716` — *"the 40 points of
  W(3,3) correspond bijectively to the 40 diameters of the Witting polytope, which
  has 240 vertices forming the E8 root system"*, with 40 listed as "base
  structure". **The 40 ↔ 40 correspondence and `40 × 6 = 240` are that file's.**
  Asserted there without proof; proved here.
- `archive/data/ChatSoFar.txt:2954,3033` — *"the Coxeter element `c` of `W(E8)` has
  order 30, and `c⁵` (order 6) partitions the 240 roots into exactly 40 orbits of
  6."* An unverified chat log, but in the repo, and **correct**. Verified here, and
  the group is identified: `⟨c⁵⟩` is the Eisenstein unit group. That
  identification is what makes the construction canonical.
- `exploration/WITTING_W33_S12_SYNTHESIS.py` — asserts "W33 point ↔ Witting
  diameter". Treated as unverified (that file carries four errors corrected in
  Pass 1020) and checked independently.
- Pass 1020 — `K = Sp(4,3)` transitive on the roots, the block sizes, the rank
  obstruction.
- Pass 338 — `p40a` and `p40b` are non-conjugate in `S₄₀`; re-verified, not
  reclaimed.

**What is new:** that the size-6 blocks *are* the `⟨−1,ω⟩`-orbits (computed, not
assumed); the quotient identified as rank-3 `U4(2)` with `srg(40,12,2,4)`; the
**point-versus-line determination**; the normaliser image `W(E6)`; and the
two-level reading that dissolves the `Sp(4,3)` vs `W(E6)` confusion.

## What this does not say

The fibration is 6:1, so it is **not** a bijection and does **not** resurrect the
edge↔root claim — that remains refuted by the rank obstruction. Nothing here
transports the 240 *edges* anywhere; the edges live on the base, the roots live on
the total space, and `240 edges ≠ 240 roots` as actions. The honest statement is a
fibration onto the 40 points, not a correspondence with the 240 edges.
