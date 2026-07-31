# Passes 1465–1469 — the constraint block is chiral, and the resolution becomes a colouring problem

Five items. The physics result is that the three Hodge blocks are **not** on equal
footing: two are outer-stable and one is not.

---

## Pass 1465 — the resolution, reformulated: it is a 9-colouring

Each edge lies in exactly 9 frame-matchings, and a resolution has 9 classes.
Therefore the 9 frames through any edge must receive **nine distinct classes**.
So, with `H` the graph on the 540 frames joined when they share an edge:

> **A resolution is exactly a proper 9-colouring of `H` in which every colour
> class has size 60.**

That converts a search into a colouring question with a computable obstruction —
`χ(H) ≥ ω(H)`, and the 9 frames through an edge already form a `K₉`. If `ω(H) ≥ 10`
there is no resolution, full stop.

```text
H is 32-REGULAR  (each frame has 4 edges, each shared with 8 other frames)
K9 present by construction, one per edge, 240 of them
does any edge's K9 extend to a K10 by a common neighbour?   NO  (all 240 checked)
greedy clique search, 300 seeds                             max = 9
```

**`ω(H) = 9`, exactly the value a resolution requires.** So the clique
obstruction is *absent* — the trivial reason for impossibility does not apply, and
`χ(H) = 9` remains possible. Three search methods have now failed on time
(Passes 1441, 1461, 1465) and none has produced an obstruction; the question is
open, and it is now open as a *colouring* problem rather than a search.

Structure worth recording: `H` is the union of 240 `K₉`'s, each frame lying in
exactly 4 of them, `240 × 9 = 2160 = 540 × 4`.

---

## Pass 1466 — the coexact block, in context

```text
PSp(4,3) irreducible degrees:
  1, 5, 5, 6, 10, 10, 15, 15, 20, 24, 30, 30, 30, 40, 40, 45, 45, 60, 64, 81
```

There are exactly **two** degree-45 irreducibles and **three** degree-30. The
coexact block `30 ⊕ 45 ⊕ 45` therefore uses *both* 45s — it is not a choice among
several, it is the whole 45-isotypic part of the group.

---

## Pass 1467 (physics) — the two 45s are FUSED by the outer automorphism

`PSp(4,3)` sits at index 2 in `PGSp(4,3) ≅ W(E₆)`. A repeated degree in a
multiplicity-free decomposition is the classic signature of an outer swap, so:

```text
PGSp(4,3) irreducible degrees:
  1,1,6,6,10,15,15,15,15,20,20,20,24,24,30,30,60,60,60,64,64,80,81,81,90

degree-45 irreducibles in PGSp : 0
degree-90 irreducible in PGSp  : YES
```

**No 45 survives to `PGSp`, and a 90 appears.** Two `PSp`-irreducibles of degree
45 that fuse into one degree-90 irreducible of the full group is exactly what an
outer swap looks like. So:

> **The three Hodge blocks are not on equal footing. The gauge block
> `15 ⊕ 24` and the physical block `81` extend to `PGSp(4,3)` — every one of
> `15, 24, 81` appears in the `PGSp` degree list. The constraint block contains
> `45 ⊕ 45`, a pair defined only over the inner group and exchanged by the outer
> involution.**

**The constraint sector is chiral; the gauge and physical sectors are not.**

That is a sharper statement than it may look, and it rhymes with a result this
corpus already closed: the selection layer found chirality *hostable but not
selectable from inside*, because the substrate's own controller `T` swaps `S±`.
Here the same phenomenon is localised — it lives entirely in the coexact block,
and the physical sector is untouched by it.

---

## Pass 1468 — the involution cannot see the swap

The cover-stabilising involution is class-45 (Pass 1442). Its character values on
the two degree-45 irreducibles:

```text
chi values on the class-45 involution : [-3, -3]
```

**Equal.** So that involution does not distinguish the two 45s — consistent with
their being exchanged by an *outer* element, since an inner class fixed by the
outer automorphism must take equal values on a swapped pair.

This is a datum, not the explanation of the `12`: the representation-theoretic
route to the enrichment is closed off at exactly this point, because the object
that stabilises a cover is blind to the only chirality in the module. **The `12`
stays open**, now with one more avenue eliminated.

---

## Pass 1469 — the sampler guard now encodes the measured rule

Three of my claims were refuted, all from one unrandomised depth-first
enumeration, and **every existence claim from the same pool survived**. So the
rule is not about wording but about use:

> An enumeration may support an **existence** claim however it was ordered. It
> may support a **frequency** or a **universal** only if it is exhaustive or
> randomised.

Implemented: a file is flagged when it enumerates, truncates, does not randomise,
**and** states a frequency or a universal — with exhaustiveness credited, since a
search reporting completion or proving infeasibility is not sampling.

```text
deterministic-order samplers : 135
flagged                      :  19
the parallel track's Pass 1417 exact-cover census : correctly NOT flagged
```

## Prior art

- [Pass 1460](analysis/w33_pass1460_1464_the_complete_hodge_decomposition.md) — the six-irreducible decomposition refined here.
- [Pass 1456](analysis/w33_pass1455_1459_harmonic_is_steinberg_and_a_refutation_of_my_own.md) — the refutation that motivated Pass 1469's rule.
- `THE_SELECTION_LAYER.md` — **owns** the chirality-not-selectable-from-inside result this pass localises to the coexact block.
