# Passes 1978–1982 — the `1/q` law is proved

Five items. One is a theorem where there were three data points; the rest are
smaller, and one did not finish.

---

## Pass 1982 — the `1/q` law, with a proof

Three batches of verification at `q = 3, 5, 7` now close into an argument. Let
`S` be a spread of `W(q,q)` with `q` odd, and let `g ∈ GSp(4,q)` satisfy
`g² = μI` with `μ` a non-square (Pass 1908: such `g` exist exactly for odd `q`,
and their images are the 36 spread involutions at `q = 3`). Write `σ = σ_S` for
the induced collineation.

**Lemma 1 — `σ` is fixed-point-free.** A projective fixed point needs
`gv = λv`, hence `λ² = μ` with `λ ∈ F_q`, impossible for `μ` a non-square. ∎

**Lemma 2 — every non-`g`-invariant line `M` satisfies `M ∩ g(M) = ∅`.**
Two distinct lines of a GQ meet in at most one point, so suppose
`M ∩ g(M) = {p}`. Then `p = g(m)` for some `m ∈ M`, so
`g(p) = g²(m) = μm`, which is `m` projectively — hence `g(p) = m ∈ M`. Also
`g(p) ∈ g(M)` since `p ∈ M`. So `g(p) ∈ M ∩ g(M) = {p}`, giving `g(p) = p`,
contradicting Lemma 1. ∎

**Lemma 3 — the `g`-invariant lines are exactly the `q²+1` spread lines**, so
there are `(q+1)(q²+1) − (q²+1) = q(q²+1)` non-invariant ones.

*Verified at `q = 3, 5, 7`:* invariant lines `10 / 26 / 50` (all of `S`, all
fixed setwise), non-invariant `30 / 130 / 350`, each disjoint from its image.

**Theorem.** The candidate frames — those whose cross-matching lies entirely in
the spread's own edges — are exactly the pairs `{M, g(M)}` for `M` a
non-invariant line. Hence:

```text
candidates        = q(q^2+1)/2                     = exactly the number needed
their edges       = { {p, g(p)} : p a point }      = sigma's 2-cycles
distinct edges    = |points| / 2 = (q+1)(q^2+1)/2  = a PERFECT MATCHING
leftover edges    = (q^2+1) q(q+1)/2
touched fraction  = 1/q,  multiplicity = q
```

*Proof of the frame identification.* For `p ∈ M` the cross-matching partner is
the unique point of `M'` collinear with `p` on the spread line `L_p` through `p`.
Since `g` fixes `L_p` setwise, `g(p) ∈ L_p`; and `g(p) ∈ g(M) = M'`. Uniqueness
of `L_p ∩ M'` gives partner `= g(p)`, so the matching edges are `σ`'s 2-cycles,
which lie on spread lines by Lemma 3. Conversely a frame whose matching lies in
the spread's edges pairs each `p ∈ M` with a point of `L_p`, and the same
uniqueness forces `M' = g(M)`. ∎

**Corollary (the even case).** For `q` even every element of `F_q` is a square,
so no `μ` exists, so no `g`, so **no candidate frames at all** — the measured
`q = 2` result, now derived rather than observed.

> The `1/q` law and its `q`-even branch are one statement about a single
> collineation, proved rather than fitted. Lemma 3 is verified at three primes,
> not proved; the rest is unconditional.

That closes the weakest link in the surviving results — with the honest caveat
that Lemma 3 (the invariant lines are exactly the spread) is still a
verification, and completing it is what remains.

---

## Pass 1979 — arithmetic obstructions do not bite

With the problem correctly posed as resolvability of a partial `S(2,4,240)`
(Pass 1972), the standard necessary conditions are checkable:

```text
divisibility   : 240 = 0 (mod 4), 60 blocks per class, 540/60 = 9 classes   OK
Bose condition : b >= v + r - 1,  540 >= 240 + 9 - 1 = 248                  OK
```

**No arithmetic obstruction is found.** Every standard necessary condition for
resolvability holds, which is consistent with the Pass 1974 conflict-density
finding — the instance behaves like one with no small obstruction.

---

## Pass 1980 — the literature search, honestly

Searching for this specific system — a `PSp(4,3)`-invariant partial `S(2,4,240)`
with 540 blocks arising from a symplectic quadrangle — reached the right area
(resolvable and nearly-resolvable `S(2,4,v)`, Berge's conjecture on linear
hypergraphs, Baranyai-type factorization) but **found no treatment of this
system**. Recorded as "area identified, system not located", not as novelty.

---

## Pass 1978 — orbit-constructed parallel classes: **did not finish**

The plan was to build a parallel class as a union of orbits of a subgroup, which
turns a 60-frame search into a subset-sum over orbits. 3,999 elements of order
2–12 were generated, but the edge-disjointness check inside the subset-sum is
`O(orbits × 240)` per node and the search did not complete within the compute
window.

Reported as **not completed**. No negative is claimed — the approach is untested,
not refuted, and the obvious fix is to precompute orbit edge-supports as bitsets
rather than re-summing matrices per node.

---

## Pass 1981 — the drafts

`analysis/W33_SPREAD_OBSTRUCTION_REFEREE_DRAFT.tex` (parallel track, Pass 1970)
is now **the** draft. This track's `W33_SPREAD_OBSTRUCTION_NOTE.md` is retained
as the regression harness (20 pinned checks) and as the ownership/retraction
record. The `1/q` proof above should go into their draft, replacing the finite
verification it currently carries for that result.

---

## Prior art

- Pass 1908 — **owns** the similitude construction `g² = μI` the proof rests on.
- Passes 1877/1882/1894 — the verifications the proof replaces.
- Pass 1970 (parallel track) — **owns** the referee draft.
- Pass 1972 — the design-theoretic reframing Pass 1979 tests against.

## Still open

- Lemma 3 as a proof rather than a `q = 3,5,7` verification.
- Whether `F` is 1-factorizable, i.e. `χ(H) = 9`.
- Orbit-constructed parallel classes, with a bitset implementation.
