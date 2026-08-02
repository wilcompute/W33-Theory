# Passes 2040–2044 — `σ_S` selects a **Hodge-star orbit**, and only `q = 3` allows it

The user's observation that a tetrahedron has a vertex opposite every face is
exactly the Hodge star, and following it closes the loop between the star idea
and the `1/q` law.

---

## Pass 2040 — the tetrahedron's star is **complementation**

In the 3-simplex on `{1,2,3,4}`, each vertex is opposite exactly one face, and
the correspondence is set complementation:

```text
1 <-> {2,3,4}      3 <-> {1,2,4}
2 <-> {1,3,4}      4 <-> {1,2,3}
```

That is `*: Λ⁰ → Λ³` realised combinatorially — take the complement.

**And on the middle degree it acts on edges.** An edge `{i,j}` has complement
`{k,l}`, which is *also an edge*, so `*` is an involution on the 6 edges with
three orbits:

```text
[1,2] <-> [3,4]      [1,3] <-> [2,4]      [1,4] <-> [2,3]
```

---

## Pass 2041 — those three orbits **are** the three perfect matchings

```text
star-orbits of the 6 edges     the 3 perfect matchings of K4
  {12, 34}                       [(1,2),(3,4)]
  {13, 24}                       [(1,3),(2,4)]
  {14, 23}                       [(1,4),(2,3)]
```

They are the same three objects. A perfect matching of `K₄` is precisely a pair
of opposite edges, i.e. a `*`-orbit.

> **Therefore `σ_S` — which selects one perfect matching per line (Pass 2033) —
> selects a Hodge-star orbit.**

That joins the two threads: the `1/q` law is `σ_S` picking one of the `q`
1-factors of `K_{q+1}`, and at the substrate's own `q = 3` those 1-factors *are*
the star-orbits of the tetrahedron. The obstruction generator and the star are
the same choice.

---

## Pass 2042 — and `q = 3` is the **only** `q` where this works

The star sends a `k`-subset of an `n`-set to its complement, an `(n−k)`-subset.
For it to act on **edges** we need `n − 2 = 2`:

```text
n :  3   4   5   6   7   8   9  10  11  12  13
     F  TRUE  F   F   F   F   F   F   F   F   F
```

> **`n = 4` is the unique simplex whose star maps edges to edges.** Since the
> residual copies are `K_{q+1}`, that is `q + 1 = 4`, i.e. **`q = 3`.**

So the reading "`σ_S` selects a star-orbit" is not a general fact about `W(q,q)`
— it is available **only at the substrate's own `q`**. At `q = 5, 7, 11` the
1-factorization is still there and `1/q` still holds, but the matchings are no
longer star-orbits, because the star takes edges of `K₆` to 4-subsets.

That is a derived selection principle for `q = 3`, and it is new. Recorded with
its scope: it says the *star interpretation* is special to `q = 3`, not that the
`1/q` law is.

---

## Pass 2043 — the sevens

The user's arithmetic, checked:

```text
Csaszar  (V,E,F) = ( 7, 21, 14)      all multiples of 7 : 7·1, 7·3, 7·2
Szilassi (V,E,F) = (14, 21,  7)      and 7 + 14 = 21   (i.e. 1 + 2 = 3)
5 Csaszar + 2 Szilassi realizations = 7
tetrahedra inside K7 : C(7,4) = 35
```

The `5 + 2 = 7` realization count is **already in the repo** — `dccxxiii`'s
`mod_7_clock` lists "5 Csaszar + 2 Szilassi = 7 toroidal realisation modes"
alongside Császár's 7 vertices, Szilassi's 7 faces, the Fano plane's 7 points and
the Heawood graph. So the seven-fold structure is theirs and this pass only
confirms the arithmetic.

**Not claimed:** any Fibonacci or golden-ratio content. `7 + 14 = 21` is
`7(1 + 2) = 7·3`, which is the statement that `F = 2E/3` and `V = E/3` for a
vertex-complete triangulation on 7 points — a triangulation constraint, not a
recurrence. Pascal's triangle does encode Fibonacci in its shallow diagonals, but
that is a different pattern from the entries used here (`C(7,1)`, `C(7,2)`,
`C(7,4)`), and I am not asserting a link.

---

## Pass 2044 — the two deferred items

**The `20`/`60` swap.** Pass 2039 found edges and flags differ at `20(#11)/20(#12)`
and `60(#18)/60(#19)`. Checking against the signed edge module
`V = 15(#6) + 24(#14) + 30(#15) + 81(#24) + 90(#25)`:

> **None of `#11, #12, #18, #19` occurs in `V`.** The constituents where the
> point/line duality is visible are exactly the ones the signed edge module does
> not contain.

**`C(7,4) = 35` versus 40 lines.** `35 ≠ 40`, difference 5, and no structural
relation is exhibited. Chased and dropped — a near-miss is not a result, and this
arc has three withdrawn claims that began as near-misses.

---

## Prior art

- `dccxxiii` — **owns** the `5 + 2 = 7` realization count and the mod-7 clock.
- Pass 2033 — `σ_S` as a 1-factor selection; Pass 2036 — the wedge/dot/star
  correspondence; Pass 2029 — the proof `σ_S` rests on.
- The vertex-opposite-face observation, the seven-fold reading and the
  factorization/selection framing are the user's.

## Still open

- `χ(H) = 9`.
- Whether the two levels of factorization are one structure or one vocabulary.
