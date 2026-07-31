# Passes 1390–1391 — every frame carries a canonical 4-edge matching, and the 540 frames cover the 240 edges 9-to-1

A new named map, produced by taking a *negative* result seriously.

---

## Where it came from

Pass 1385 refuted the tomotope A₄ bridge. The refutation needed one fact along
the way:

> the frame stabiliser's derived subgroup `A₄` acts **faithfully**, as the natural
> degree-4 alternating group, on the 4 points of **each** of the frame's two
> totally isotropic lines, with orbits `[4,4]` on the frame's 8 points.

That fact was collected as evidence against a bridge and then almost discarded.
It has a consequence the refutation did not need. A faithful action on *both*
4-sets embeds `A₄` into `A₄ × A₄` with both projections onto, so the image is the
graph of an isomorphism — a **diagonal**. A diagonal acting on `4 + 4` points
forces an `A₄`-equivariant bijection between the two 4-sets.

So the frame should carry a canonical pairing of its 8 points into 4 *cross*-pairs.
It does.

---

## Pass 1390 — the cross-matching is canonical, and it lands on edges

```text
frames                                                     540
A4-equivariant bijections L -> L' , per frame              1        (all 540)
invariant under the FULL frame stabiliser (order 48)?      YES
invariant under the A4 alone?                              YES
```

**Exactly one, for every one of the 540 frames** — so "canonical" is the correct
word, not "a torsor". And it is preserved by the *whole* stabiliser, not merely by
the `A₄` that produced it, so the matching is an invariant of the frame itself
rather than of a choice made inside it.

Example (frame `{L, L'}` with `L = {1,2,3,40}`, `L' = {4,6,22,34}`):

```text
canonical matching  M = { {1,34}, {2,4}, {3,6}, {22,40} }
```

Then the count, which is where it becomes interesting:

```text
540 frames x 4 cross-pairs                = 2160 incidences
DISTINCT cross-pairs                      =  240
G-orbits on them                          = [240]      -- a single orbit
point stabiliser                          = order 108 = C3 x S3 x S3
are the cross-pairs EDGES of W(3,3)?      = 240 of 240   -- ALL of them
```

### The statement

**The canonical cross-matchings of the 540 frames land exactly on the 240 edges of
`W(3,3)`, covering each edge exactly 9 times.**

```text
    540 frames  --canonical 4-edge matching-->  240 edges       9-regular
                        2160 = 540 x 4 = 240 x 9
```

Three things make this a map rather than a coincidence of integers:

1. **The target is forced, not chosen.** A cross-pair joins a point of `L` to a
   point of `L'`, and `L, L'` are *disjoint* lines — so a priori the pair could
   be collinear or not. **All 240 are collinear**, i.e. genuine edges. Nothing in
   the construction asked for that.
2. **The multiplicity is uniform.** The 240 cross-pairs form a single `G`-orbit,
   so `2160 / 240 = 9` is exact and every edge is covered the same number of
   times. Stabiliser order `108 = 25920/240` checks.
3. **The map is injective.** The four cross-pairs' endpoints are exactly the 8
   points `L ∪ L'`, and each line is a maximal clique of the collinearity graph,
   so the 8 points recover the unordered pair `{L, L'}`. Distinct frames therefore
   give distinct 4-edge matchings.

So each frame is a **4-edge perfect matching of its own 8 points, entirely inside
the edge set** — and the 540 of them tile the 240 edges 9-fold.

---

## Pass 1391 — scope, and what is *not* claimed

**240 is the most overloaded integer in this corpus.** It is the edge count, it is
`|Φ(E₈)|`, and `Y₄₈₀ = 2 × 240` is the directed-edge carrier. The result above is
about the **edge set of `W(3,3)`** and nothing else. In particular:

- **No E₈ reading is claimed.** Pass 1012 established that the 240 edges form a
  single `G`-orbit while the 240 `E₈` roots split `72 + 6 + 81 + 81` under
  `E₆ × A₂`, so no equivariant bijection exists for that embedding. Landing on
  240 edges is landing on the edges, not on the roots.
- **The 2160 is an incidence count, not an object.** `540 × 4 = 2160` counts
  frame–edge incidences with multiplicity; the distinct set has size 240. Any
  comparison with another 2160 in this corpus (BT796's fibration, the
  `[[2160,81,9]]` amplification code) must compare `G`-sets and stabilisers, not
  cardinalities. No such comparison is made here.
- **Novelty checked by result, not topic.** `cross-matching` appears in no other
  file; the map `540 → 4-subsets of the 240 edges`, and the 9-regularity, were
  searched for in `RESULTS_INDEX.md` and the corpus before this was written.

What *is* new is a named, canonical, equivariant map with a computed multiplicity,
recovered from a fact that was collected as evidence for a refutation. The
refutation stands; this is a different use of the same computation.

## Prior art

- [Pass 1385](analysis/w33_pass1385_1389_a4_negative_precision_manuscripts.md) — the faithful `A₄` action this is built on, and the refutation it was collected for.
- [`RESULTS_VOCABULARY.md`](RESULTS_VOCABULARY.md) — the 540 is species 81, `{540:line-nonedge}`, stabiliser `C₂ × S₄`, rank 32. **Five** transitive degree-540 species exist; this is the disjoint-line-pair one.
- [`pass1012`](analysis/w33_pass1012_edge_root_equivariance_obstruction.py) — **owns** the 240-edge/240-root obstruction invoked above.
