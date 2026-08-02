# Passes 2036–2039 — wedge / dot / star as Császár / Szilassi / tetrahedron, and factorization vs selection

The user's two proposals, tested. Both hold, and together they give the arc a
single operational vocabulary.

---

## Pass 2036 — the three polyhedra realise the three operations, by signature

The three operations differ by what they do to degree:

```text
wedge  ^ : RAISES  degree   0-cells -> 1-cells
dot    . : LOWERS  degree   2-cells -> 1-cells
star   * : REVERSES degree  k <-> n-k   (involution; fixed on middle degree)
```

And the three polyhedra differ by which completeness they have:

```text
tetrahedron  V= 4 E= 6 F= 4   E = C(V,2): TRUE    E = C(F,2): TRUE
Csaszar      V= 7 E=21 F=14   E = C(V,2): TRUE    E = C(F,2): false
Szilassi     V=14 E=21 F= 7   E = C(V,2): false   E = C(F,2): TRUE
```

> **Császár is wedge-complete** — every pair of vertices spans an edge.
> **Szilassi is dot-complete** — every pair of faces meets in an edge.
> **The tetrahedron is both, because it is self-dual: the star is internal.**

Both operations land on the *same* 21-dimensional edge space, from opposite
directions — which is exactly the relationship `∧` and `·` have.

### The star, made precise by Hodge dimensions

```text
complex        V   E   F   exact  harmonic  coexact   internal star?
tetrahedron    4   6   4       3         0        3   YES  (3 = 3)
Csaszar        7  21  14       6         2       13   no   (6 != 13)
Szilassi      14  21   7      13         2        6   no   (13 != 6)
```

Neither toroidal polyhedron admits a star **internally** — but they are duals of
each other, and `(6,2,13) ↔ (13,2,6)`:

> **The Hodge star is the map *between* Császár and Szilassi, not a map inside
> either. The tetrahedron is its fixed point** — the self-dual case where the
> two conditions have not yet separated.

That is the user's "on either side of it", derived rather than asserted.

---

## Pass 2037 — and this diagnoses why `W(3,3)` has no star

```text
W(3,3) clique complex (40, 240, 160, 40) : exact 39, harmonic 81, coexact 120
39 != 120  ->  no internal star
```

Pass 1866 proved the absence representation-theoretically (all Frobenius–Schur
indicators `+1`). The polyhedral picture gives the *dimensional* reason, and one
extra fact:

```text
120 = 39 + 81 ,  i.e.  240 = 2 x 120
```

> The coexact block is **exactly half** the edge space, and `exact ⊕ harmonic`
> has the same dimension as `coexact`.

But not equivariantly: `{15, 24, 81}` versus `{30, 90}` are different modules.
So even the "half-star" fails, and it fails for the same reason the full one
does — dimensions match, objects do not. **Checked before claiming**, which in
this arc is the whole discipline.

---

## Pass 2038 — factorization is wedge, selection is dot, and the star is the transpose

The user's second proposal, in matrices.

**Factorization = expansion.** `K_{q+1}` with `q+1` even has

```text
A(K_{q+1}) = P_1 + P_2 + ... + P_q
```

a decomposition of the adjacency matrix into `q` **permutation matrices**, each a
perfect matching — a Birkhoff-type decomposition. This *builds* the whole from an
indexed family: degree-raising, wedge-like.

**Selection = contraction.** `σ_S` picks one `P_i`. Extracting a single term
against the family is degree-lowering, dot-like — and the overlap is exactly

```text
<A, P_i> / <A, A> = [(q+1)/2] / [q(q+1)/2] = 1/q
```

> **The `1/q` law is the inner product of one permutation matrix with the sum of
> all `q` of them.** Factorization builds, selection extracts, and the ratio is
> the law.

**The star = the transpose.** The frame incidence `M` is `540 × 240`, and
`χ(H) = 9` reads two ways:

```text
row view    : partition the 540 frames into 9 classes, each an exact cover
column view : each edge's 9 frames receive 9 distinct colours
```

These are the same condition seen through `M` and `Mᵀ`. So the two levels of the
arc are one operation applied twice:

| level | object | operation |
|---|---|---|
| `K_{q+1}` | adjacency matrix | factor into `q` matchings, **select one** → `1/q` |
| frame hypergraph | incidence `M` | factor into 9 exact covers → `χ(H) = 9` |

and the star relating them is `M ↔ Mᵀ`.

**Flagged, not claimed:** that the two levels are the *same* structure rather
than the same vocabulary. This arc has three withdrawn results from treating a
shared concept as a shared object, and "both are factorizations" is a shared
concept.

---

## Pass 2039 — edges vs flags: identical degrees, different `G`-sets

`W(3,3)` has 240 edges (point pairs) and 240 flags (line pairs meeting in a
point). Testing whether they are the same `G`-set:

```text
edges : 1(#1) + 15(#6) + 15(#9) + 20(#11) + 24(#14)x2 + 60(#18) + 81(#24)
flags : 1(#1) + 15(#6) + 15(#9) + 20(#12) + 24(#14)x2 + 60(#19) + 81(#24)
characters equal ? FALSE
differing : 20(#11) vs 20(#12) ,  60(#18) vs 60(#19)
```

> **Identical degree profiles, different irreducibles — so edges and flags are
> NOT isomorphic `G`-sets.** The difference is exactly a point/line swap at the
> degree-20 and degree-60 constituents.

My **first** printout of this showed degrees only and looked identical; the
characters said otherwise. That is the fourth time in this arc the
degree-vs-irreducible distinction has been load-bearing, and the first where my
own output actively concealed it. `scripts/gset_audit.py` prints indices for
exactly this reason.

---

## The five, honestly

- **1-factorization link between levels** — framed operationally (Pass 2038), not
  established. No resolution exists to test against.
- **The 240 flags** — done (Pass 2039), and the answer is a negative with a
  mechanism.
- **`C(7,4) = 35` versus 40 lines** — not attempted.
- **Face-bonding at the frame level** — not attempted.
- **The tetrahedron result into the referee draft** — not done; it belongs in the
  parallel track's document, which they maintain.

---

## Prior art

- `dccxxiii`, BT1844 — **own** the genus oscillator and the ladder.
- Pass 1866 — **owns** the no-Hodge-star result; Pass 1874 — the point/line
  module difference that Pass 2039 sees again.
- Pass 1972 — the 1-factorization reading of `χ(H) = 9`.
- The wedge/dot/star correspondence and the factorization/selection framing are
  the user's.
