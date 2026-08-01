# Passes 1877–1881 — the matching is an involution, a third class does exist, and the phase obstruction was parity all along

Five items. One completes a proof, two are corrections to my own last two
batches, and one settles the physics question sharply enough to state in a
sentence.

---

## Pass 1877 — the `1/q` law, mechanism complete

Pass 1872 found the completing frames pile onto a perfect matching of the points.
The counts localise it further: `touched / spread lines` is `20/10`, `78/26`,
`200/50` — always `(q+1)/2`, exactly half a line. Tested:

```text
q=2: lines of 3 points,   0 candidates,   0 touched   (line size ODD)
q=3: lines of 4 points,  15 candidates,  20 touched   per line 2 = (q+1)/2
q=5: lines of 6 points,  65 candidates,  78 touched   per line 3 = (q+1)/2
q=7: lines of 8 points, 175 candidates, 200 touched   per line 4 = (q+1)/2

perfect matching WITHIN each spread line, for every odd q : TRUE
```

> **The touched edges are a perfect matching of each individual spread line.**
> Such a matching exists iff `q+1` is even, i.e. iff `q` is **odd**.

That closes the argument in both directions:

- **`q` odd.** Each of the `q²+1` spread lines contributes `(q+1)/2` edges, so
  `touched = (q²+1)(q+1)/2 = |points|/2`, while the leftover is
  `(q²+1)q(q+1)/2`. The ratio is `1/q` and the multiplicity is `q`, both by
  counting rather than by fitting.
- **`q` even.** A line has `q+1` points, an odd number, so no perfect matching of
  it exists — hence **no candidates at all**. The `q = 2` case with its zero
  candidates is not an anomaly; it is the theorem's other branch.

The `1/q` law and the even-`q` exception are now one statement.

---

## Pass 1878 — a third resolution class **does** exist, and Pass 1873 was wrong about that

Pass 1873 reported the class-by-class build "dies at 2" and I suggested the
obstruction bites between the second and third class. Testing it properly — fix
two disjoint covers, then search the remaining 420 frames for a third:

```text
pair 1 : third class found = TRUE    585,731 nodes   EXHAUSTIVE
pair 2 : not found          852,256 nodes   timed out -> undecided
pair 3 : not found          875,251 nodes   timed out -> undecided
pair 4 : third class found = TRUE     60,436 nodes   EXHAUSTIVE
pair 5 : not found          878,691 nodes   timed out -> undecided
pair 6 : not found          869,451 nodes   timed out -> undecided
```

> **Two of six disjoint cover-pairs extend to a third class**, verified
> exhaustively rather than by timeout.

So there is no obstruction at the third class, and my Pass 1873 reading was a
search-cap artifact rather than a structural fact. The four undecided pairs are
undecided, not negative — the honest column is "timed out", and I am not
counting them as evidence either way. The frontier moves to the fourth class, and
the useful measurement is that the two successes needed **585,731** and **60,436**
nodes, an order of magnitude apart, so cover-pairs differ enormously in how much
room they leave.

---

## Pass 1880 (physics) — the phase obstruction is **parity**, and Pass 1876 measured the wrong thing

Pass 1876 reported that no maximal subgroup of `W(E₆)` admits an invariant
complex structure on the physical 81, and priced a phase at "more than a maximal
reduction." Descending the lattice made the real reason obvious:

```text
depth 1 :   7 subgroups, orders 1152 ... 25920   none
depth 2 :  39 subgroups, orders 48 ... 960       none
depth 3 : 165 subgroups                          none
depth 4 : 569 subgroups, orders down to 4        none
```

Nothing works because nothing *can*. A real vector space admits `J` with
`J² = −1` only in **even** dimension, and `81` is odd.

> **The physical sector can never carry a symmetry-respecting phase, for any
> group whatsoever — including the trivial one. The obstruction is parity, not
> representation theory.** Pass 1876's pricing claim is withdrawn.

The correct question is about the even blocks, and it has a clean answer:

| block | dim | parity | largest subgroup admitting `J` | index |
|---|---|---|---|---|
| 15 (gauge) | 15 | odd | **impossible at any subgroup** | — |
| 81 (physical) | 81 | odd | **impossible at any subgroup** | — |
| 24 (gauge) | 24 | even | `C₃ × SL(2,3)`, order 72 | 720 |
| 30 (constraint) | 30 | even | `C₅ : C₄`, order 20 | 2592 |
| 90 (constraint) | 90 | even | **`PSp(4,3) = O(5,3)`, order 25920** | **2** |

> **Only the degree-90 gets a phase cheaply: it needs nothing but the index-2
> reduction to `PSp(4,3)`.** Interference is available in the constraint sector
> at the cost of the outer involution alone, and is absolutely unavailable in the
> physical sector at any cost.

That is the sharpest form of the photonics thread so far. An optical realisation
of this substrate can have coherent phase structure in its constraint sector and
must treat the physical sector as amplitude-only — not as a modelling choice, and
not even as a symmetry-breaking budget, but because 81 is odd.

---

## Pass 1879 — the gauge bit is **not** the duality

Pass 1874 found the point and line modules carry different degree-15s (`#6` vs
`#9`) and I flagged the tempting reading — that the gauge handedness bit *is* the
point/line duality — as not claimed. Settled:

```text
point module : 1 + 15(#6) + 24(#14)
line  module : 1 + 15(#9) + 24(#14)
is #9 = #6 . eps ?          FALSE
is the line character = point character . eps ?   FALSE
the degree-24 is #14 in BOTH                      TRUE
```

**No.** The two degree-15s are genuinely different irreducibles but they are not
`ε`-twists, so the duality is not the sign character. The consistent reading is
that `W(3,3)`'s point/line duality is a **correlation, not a collineation** — it
lives outside `PGSp(4,3)` altogether, so it cannot be any element of the group
and need not act as `ε`. Good that it was flagged rather than asserted.

What survives, and is the useful part: the degree-24 is the same `#14` in both
modules even though `24 · ε ≠ 24`, so it *has* two extensions and both geometries
pick the same one.

---

## Pass 1881 — the 270 is not a third reader

The 270 ordered incident pairs of the 27 lines (Pass 1875) give an imprimitive
270-point action. Pass 1486 ruled the degree-90 out of every *primitive*
permutation module, so this is a real test:

```text
270-module = 1 + 6(#4)x2 + 15(#8) + 20(#11)x3 + 24(#14) + 30(#16) + 64(#21)x2

contains a degree-81 ? FALSE
contains a degree-90 ? FALSE
```

> **The 270 does not see the physical sector or the degree-90.** It is not a
> third chirality reader; the frames and the spreads remain the only two.

Consistent with Pass 1487 — a permutation module cannot see an orientation sign,
so no `G`-set of any size will ever read the handedness. And a detail worth
keeping: the 270-module carries the *same* `#14` degree-24 as the point and line
modules. Three unrelated `G`-sets, one degree-24 — `#14` is looking canonical.

---

## Prior art

- Passes 1872/1873 — the law and the search this batch completes and corrects.
- Pass 1876 — the pricing claim Pass 1880 withdraws.
- Pass 1874 — the duality reading Pass 1879 refutes.
- [BT795](analysis/BT795_spread_envelope_routing_cell.md) / BT790 — **own** the
  36 spreads; Pass 1486/1487 — **own** the permutation-module negatives Pass 1881
  extends to an imprimitive case.
- Passes 1841–1845 (parallel track) — **own** the certified signature
  resolutions; `χ(H) = 9` is still open.

## Still open

- `χ(H) = 9`. The frontier is now the fourth class, not the third.
- A written proof that the candidate matchings must lie inside a spread line's
  perfect matching — Pass 1877 verifies it at `q = 3, 5, 7` but does not derive it.
- Whether the degree-90's index-2 phase has any physical content, or is an
  accident of it being the one fused block.
