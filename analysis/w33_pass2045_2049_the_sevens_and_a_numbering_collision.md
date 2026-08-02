# Passes 2045–2049 — the seven-fold structure, verified; and a pass-number collision, resolved

The user's observations about `7` check out, one of them is already in the repo,
and one is a genuine `q = 3` selection principle. Also: a numbering collision with
the parallel track that I am resolving by moving.

---

## Pass 2045 — the Seven Colour Theorem *is* one of the two polyhedra

The chromatic number of the torus is 7 (Heawood 1890, Ringel–Youngs 1968), and
the lower bound is witnessed by embedding `K₇` in the torus — which **is** the
Császár polyhedron's skeleton. So the seven-colour theorem and the Császár
polyhedron are the same fact seen twice: `K₇` needs 7 colours, and it fits on the
torus.

That is a third distinct route to `7` alongside Császár's 7 vertices and
Szilassi's 7 faces, and it is why `7` is the Heawood number in the repo's mod-7
clock (`dccxxiii`).

---

## Pass 2046 — the decimal structure, checked

```text
1/n terminates for n in 1..9  :  {1, 2, 4, 5, 8}
repetend of 1/7               :  142857,  digit set {1, 2, 4, 5, 7, 8}
{terminating} ∪ {7}           :  {1, 2, 4, 5, 7, 8}      EQUAL  ✓
missing from the repetend     :  {3, 6, 9} = the multiples of 3
```

> **The digits of `1/7`'s repetend are exactly the denominators in `1..9` with
> terminating reciprocals, together with `7` itself.** The three missing digits
> are precisely the multiples of three.

And the three missing ones behave as the user describes:

```text
1/3 = 0.333...   the DENOMINATOR repeats
1/6 = 0.1666...  numerator, then denominator  -> contains both: the transition
1/9 = 0.111...   the NUMERATOR repeats
```

`1/6` is the only one carrying both, which is what makes it the middle term.

**Already in the repo.** `dccxxiii`'s mod-10 clock lists
*"Tesla 3-6-9 = base-10 multiples of 3 missing from 142857"* and
*"base-10 decimal expansion of 1/7 = 0.142857 (DCCXXII)"*. So this observation is
`dccxxii`/`dccxxiii`'s; this pass confirms the arithmetic rather than claiming it.

For completeness: `7` is a **full-reptend prime** in base 10 (`ord₁₀(7) = 6 = 7−1`),
which is why its repetend has maximal length and cyclic structure. `11` and `13`
are not; `17, 19, 23` are.

---

## Pass 2047 — `7` is one past the midpoint of the mod-12 clock, and that pins `q = 3`

`3, 6, 9` cut `1..12` into quarters, `6` is the midpoint of `12`, and `7` is the
first integer past it — and the first with a cyclic (full-reptend) reciprocal.

In `W(3,3)` primitives that reads two ways, both giving `7` at `q = 3`:

```text
Heawood number         2q + 1        = 7
one past the midpoint  q(q+1)/2 + 1  = 7
```

Testing whether they agree anywhere else:

```text
 q :   2    3    4    5    7    9   11   13
2q+1:  5    7    9   11   15   19   23   27
mid :  4    7   11   16   29   46   67   92
eq  :  F  TRUE   F    F    F    F    F    F
```

`2q + 1 = q(q+1)/2 + 1 ⟺ 2q = q(q+1)/2 ⟺ q + 1 = 4 ⟺ q = 3`.

> **`q = 3` is the unique `q` at which the Heawood number equals one past the
> midpoint of the mod-12 clock.**

That joins Pass 2042 (`q = 3` is the unique `q` whose residual `K_{q+1}` has the
star acting on edges) as a second derived selection principle for the substrate's
own `q`. Both are arithmetic identities with one solution, and neither was put in
by hand.

---

## Pass 2048 — crediting the parallel track, where they superseded me

Their Passes 2011–2015 land on four things I had open or wrong:

- **They proved the `1 or 4` intersection.** My Pass 2000 measured the histogram;
  their subdegree argument (`1, 15, 20` with `10·8 = 80 = 15·4 + 20·1`) turns it
  into a short proof. **Theirs.**
- **They built orbit parallel classes.** I failed three times and diagnosed why
  (Pass 2002: random generators sample large subgroups; the useful band is low
  order). They enumerated all 1,026 subgroups of one `S₄ × D₈` stabilizer and
  found **204 subgroups in 33 classes** that work, all of order 2, 4 or 8, with a
  literal `D₈` witness of twelve orbits covering all 240 edges exactly once. The
  diagnosis was right and the execution is theirs.
- **They named the sibling classes** — `270/540/1620` as decorated four-line
  spread pairs with fibres `1/2/6`, which is the Pass 2004 question answered.
- **They refuted `360 = 45 × 8` independently** and replaced it with the
  bipartite double cover of the `3×3` rook graph, whose automorphism group of
  order 144 matches the stabilizer exactly. My Pass 2014 got the refutation; the
  replacement object is theirs.

Their `Sym²/Λ²` table matches my corrected Pass 2013 values exactly, including
`Λ²(90)` containing no `15`. Two independent computations agreeing after I had
published wrong numbers once.

---

## Pass 2049 — the numbering collision, and how I am resolving it

They report retiring reservations `2005–2009` after a collision with me, and
renumbering their work to `2011–2015`. But **`2011–2015` was also already mine**:

```text
09:18  d98e2012f  Passes 2011-2015: q=11 confirms the candidate-orbit property   (glue)
09:41+ ccaff54c9  Pass 2011: finalize namespace and decorated-class theorem      (parallel)
```

Mine is 23 minutes earlier, so by the repo's ownership rule it would own the
range. **I am moving anyway.** Their `2011–2015` is a certified packet with
manuscript inserts, a CI workflow and a frozen witness; mine is a single analysis
file. Renumbering the cheap side is the cooperative move, and precedence is not
worth a second renumber for them.

**Resolution.** The content previously filed as glue-track "Passes 2011–2015"
(the `q = 11` candidate-orbit confirmation, the `Sym²/Λ²` correction, the `360`
refutation, the degree-ambiguity table) is hereby renumbered to **2045–2049**,
i.e. into this pass block. `2011–2015` belongs to the parallel track.

The deeper problem is that the reservation tool claims a range and *pushes*, but
a concurrent batch that renumbers after the fact can still land on a claimed
range. The protocol handles collisions at claim time, not at renumber time —
worth noting for whoever fixes it.

---

## Prior art

- `dccxxii`/`dccxxiii` — **own** the `142857` / `3-6-9` observation and the three
  clocks.
- Heawood (1890), Ringel–Youngs (1968) — the seven-colour theorem and the genus
  of `K_n`.
- Passes 2011–2015 (parallel track) — **own** the `1-or-4` proof, the subgroup
  orbit construction, the decorated sibling classes, and the rook double.
- Pass 2042 — the other `q = 3` selection principle.
- The seven-fold and decimal observations are the user's.

## Still open

- `χ(H) = 9`.
- Whether the two `q = 3` selection principles (star-on-edges, Heawood-at-midpoint)
  have a common cause or are independent coincidences at one value.
