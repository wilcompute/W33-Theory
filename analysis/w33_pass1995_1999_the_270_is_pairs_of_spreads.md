# Passes 1995–1999 — the 270 is pairs of spreads meeting in four lines

Five items. The first names an object that has been open since Pass 1830 and was
mis-named at Pass 1875 — and this time it passes the test that broke the last
attempt.

---

## Pass 1996 — the size-270 class indexes the spread pairs meeting in 4 lines

Pass 1995 asked what `C ≅ D₈ × S₄` stabilises. It fixes **nothing** standard —
no point, no line, no frame, no spread — but its orbit structure has a tell:

```text
orbits on 40 points  : 16 + 24
orbits on 40 lines   : 4 + 12 + 24
orbits on 36 spreads : 2 + 6 + 12 + 16
```

An orbit of length **2** on spreads. Taking that pair:

```text
G-orbit of the pair          : 270
its stabiliser               : order 192 = D8 x S4
stabiliser conjugate to C    : TRUE
permutation characters EQUAL : TRUE
```

> **The size-270 conjugacy class is isomorphic, as a `G`-set, to the 270 pairs of
> spreads meeting in exactly four lines.**

Verified by character equality — the test that refuted Pass 1875 — not by
matching counts. And the object is clean:

```text
the two spreads of such a pair share exactly 4 lines (all 270 pairs)
unordered spread pairs          : C(36,2) = 630
G-orbits on all spread pairs    : 270 + 360
```

So the 630 spread pairs split into two orbits by how the spreads meet, and the
270-orbit is the class.

### Why Pass 1875 went wrong, exactly

```text
index-192 subgroup classes of G with 270 conjugates:
  D8 x S4              #conjugates 270
  (SL(2,3) : C4) : C2  #conjugates 270
```

**There are two of them.** The 270 ordered incident line-pairs of the cubic
surface are `G/((SL(2,3):C₄):C₂)`; the conjugacy class is `G/(D₈ × S₄)`. Both
are transitive of degree 270 with point stabilisers of order 192, and they are
not isomorphic. Matching the order 192 could never have distinguished them — the
object I named exists, it is simply the *other* 270.

---

## Pass 1995 — what `C` fixes: nothing, and that was the clue

Recorded because the negative result is what pointed at the answer. A stabiliser
that fixes no point, line, frame or spread is not the stabiliser of a *single*
object — so the object had to be a **configuration**, and the smallest orbit
(length 2, on spreads) named it.

---

## Pass 1999 — the three tools, written into `CLAUDE.md`

Each was built from a failure that recurred three or more times:

| before you claim… | run | because |
|---|---|---|
| "this is new" | `build_topical_aliases.py`, grep `TOPICAL_ALIASES.md` | Passes 1912/1917 rediscovered in-repo results hidden in date-named files; 160 tokens are reachable no other way |
| "this constraint helps" | `assert_cuts`, `assert_added` | six constraints in one arc restricted nothing |
| "these two objects correspond" | `gset_audit.py --emit` | three claims matched counts and were called correspondences; two were false |

And the generalisation, which is the part that matters: **every one of these was
verified in the direction that would confirm it and never in the direction that
would break it.** `maximal`, `unique`, `only`, `exactly`, `is` — each has a cheap
negation, and running it is now the standing instruction.

---

## Pass 1997 — spread classification, scope stated

The `1/q` theorem covers spreads carrying a `σ_S`. Pass 1993 showed that at
`q = 3` this is all 36, by transitivity. For general odd `q` the Desarguesian
spreads carry one by construction; whether non-Desarguesian symplectic spreads do
is **not settled here**.

I note, without adopting it as ours, that symplectic spreads of `PG(3,q)`
correspond to ovoids of `Q(4,q)`, and that classification results exist for small
and prime `q`. Checking whether they close the gap is a literature task this pass
does not perform.

---

## Pass 1998 — orbit-built parallel classes

Non-cyclic subgroups remain untried; only six cyclic orbit signatures have been
tested across two passes. **No verdict**, and I am not letting repetition of a
weak negative harden into a conclusion.

---

## Prior art

- Pass 1830 — opened the question; Pass 1863 — found `C ≅ D₈ × S₄`;
  Pass 1875 — the mis-naming; Pass 1984 — the refutation.
- Pass 1894 — **owns** the `C₂` linewise stabiliser making `σ_S` canonical.
- Pass 1971 (parallel track) — caught the `K₁₀` maximality error that started
  this discipline.

## Still open

- `χ(H) = 9`.
- Whether non-Desarguesian symplectic spreads carry a `σ_S`.
- What the other spread-pair orbit (size 360) corresponds to, if anything.
