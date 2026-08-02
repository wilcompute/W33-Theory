# Passes 2011–2015 — `q = 11` confirms the candidate-orbit property, and my Pass 2005 multiplicities were for the wrong irreps

Five items. One answers the open question the other track posed; one corrects
numbers I published last batch; one kills a coincidence I deliberately did not
claim.

---

## Pass 2011 — the candidate-orbit property holds at `q = 11`

The parallel track's Pass 1974 isolated the gap in my Pass 1982 proof as the
**candidate-orbit property** — that *every* residual candidate frame is
`{M, σ(M)}` — and proposed looking for the first counterexample at `q = 9` or
`q = 11`. Built `GQ(11,11)` from scratch:

```text
q=11 : points 1464, lines 1464, spread of 122 lines
       edges 96,624, residual 8,052
       CANDIDATES 671  vs (q^2+1)q/2 = 671    EQUAL: True
       touched 732/8052 = 0.090909  vs 1/q = 0.090909
```

> **No counterexample at `q = 11`.** The candidate count equals the
> involution-generated count exactly, and the touched fraction is `1/11` to six
> places.

Four confirmations now — `q = 3, 5, 7, 11` — including the case proposed as the
most likely to break. Still a verification, not a proof; the property remains
open in general and is stated that way.

---

## Pass 2013 — correction: Pass 2005's multiplicities were for the wrong irreducibles

Pass 2005 reported `Sym²(90)` and `Λ²(90)` multiplicities using
`First(irr, x -> x[1] = 15)` and similar — which picks *an arbitrary* degree-15
irreducible, not the one in `V`. `PGSp(4,3)` has **four** degree-15 irreducibles
and **two** degree-81s, and they behave differently:

```text
   irr #6  degree 15   Sym^2 3   Lambda^2 0   <- IS a block of V
   irr #7  degree 15   Sym^2 2   Lambda^2 1
   irr #8  degree 15   Sym^2 0   Lambda^2 3
   irr #9  degree 15   Sym^2 3   Lambda^2 0
   irr #23 degree 81   Sym^2 5   Lambda^2 7
   irr #24 degree 81   Sym^2 7   Lambda^2 5   <- IS a block of V
```

Pass 2005 reported `24: Λ² 4` and `81: Sym² 5, Λ² 7`. Corrected, for `V`'s actual
blocks `#6, #14, #15, #24`:

```text
degree 15 (#6)  : Sym^2 3   Lambda^2 0
degree 24 (#14) : Sym^2 5   Lambda^2 0
degree 30 (#15) : Sym^2 3   Lambda^2 2
degree 81 (#24) : Sym^2 7   Lambda^2 5
```

**The qualitative conclusion survives and gets stronger.** Not "`Λ²` contains no
15" but:

> **`Λ²(90)` contains neither of `V`'s gauge blocks** — the 15 and the 24 both
> have antisymmetric multiplicity **zero**, while `Sym²` contains both. The entire
> gauge sector `15 ⊕ 24` is reachable symmetrically and unreachable
> antisymmetrically.

And an unexpected one:

> **The two degree-81 extensions have *swapped* `Sym²`/`Λ²` multiplicities**
> — `(5,7)` and `(7,5)`. The substrate's chirality is visible in the quadratic
> phase channel, not only in the character values on the outer classes.

This is the same error family as the degree-ambiguity table I built two passes
ago: **"a degree-15" is not a well-defined object.** I built the table for
`G`-sets and then immediately made the analogous mistake for irreducibles.

---

## Pass 2014 — the `360 = 45 × 8` coincidence is **refuted**

Pass 2007 flagged that the 360-orbit's stabiliser has order 144 with
`1152/144 = 8`, and declined to claim a fibration over the 45 octets pending the
test. Running it:

```text
360-orbit stabiliser order 144;  1152/144 = 8
stabiliser contained in a conjugate of the octet stabiliser? FALSE
360-module : 1 + 15x2 + 20x2 + 24 + 60 + 60 + 64 + 81
45-module  : 1 + 20 + 24
45-module is a constituent of the 360-module?              TRUE
```

The 45-module *is* a constituent — a necessary condition — but the decisive test,
whether the stabiliser embeds in the octet stabiliser, **fails**. There is no
fibration.

That is the discipline working as intended: the arithmetic was suggestive, I
recorded it as suggestive, ran the test, and it is negative. Two passes ago this
would have become a claim.

---

## Pass 2012 — explicit quadratic couplings: multiplicities only

The multiplicities above are exact, so five (now seven) independent equivariant
maps `Sym²(90) → 81` exist. **Constructing them is not done here** — that needs
explicit module realisations and Reynolds averaging, which the parallel track has
machinery for (their `A₂₄`, `A₉₀` intertwiners) and this track does not.
Recorded as existence, not construction.

---

## Pass 2015 — the ambiguity table, for the other track

`analysis/CROSS_TRACK_DEGREE_AMBIGUITY.md` gives the table directly: which
degrees admit a unique transitive `PGSp(4,3)` action (27, 36, 45 — a count match
suffices), which are ambiguous (40, 90, 120, 270 — the character test is
required), and which admit **no** transitive `G`-action at all (15, 20, 24, 30,
60, 81 — so identifications at those sizes are `S₆` statements, never `G` ones).

They use degrees 90 and 120; both are ambiguous.

---

## Prior art

- Passes 1971–1975 (parallel track) — **own** the candidate-orbit scoping that
  Pass 2011 tests, and the maximality correction.
- Pass 2005 — the multiplicities Pass 2013 corrects.
- Pass 2007 — the coincidence Pass 2014 refutes.

## Still open

- The candidate-orbit property as a proof (four confirmations, no derivation).
- Explicit construction of the `Sym²(90) → 81` maps.
- `χ(H) = 9`.
