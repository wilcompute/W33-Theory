# Passes 2030–2035 — the tetrahedron **is** the unit, and the `1/q` law is a 1-factor selection

The user's structural proposal, tested piece by piece. Most of it holds and it
connects the whole arc; one part is a clean negative.

---

## Pass 2030 — the two maximal adjacencies, and where they coincide

The proposal: the tetrahedron carries **both** forms of maximal adjacency, and
the two toroidal polyhedra sit on either side of it. That is exactly right, and
the reason is self-duality:

| object | vertices | edges | faces | maximality | genus |
|---|---|---|---|---|---|
| **tetrahedron** | 4 | 6 | 4 | skeleton `K₄` **and** dual `K₄` — both | 0 |
| **Császár** | 7 | 21 | 14 | skeleton `K₇` — **vertex**-complete | 1 |
| **Szilassi** | 14 | 21 | 7 | faces pairwise adjacent — **face**-complete | 1 |

> At `h = 0` the two maximality conditions **coincide**, because the tetrahedron
> is self-dual. At `h = 1` they **split** into a dual pair. The tetrahedron is
> not merely one rung below — it is the rung where the two conditions have not
> yet separated.

That is the repo's genus oscillator `(4,6,4) → (7,21,14)` read structurally
rather than numerically.

---

## Pass 2031 — Pascal rows 4 and 7, precisely

```text
row  4 : (1,  4,  6,  4, 1)
row  7 : (1,  7, 21, 35, 35, 21, 7, 1)
row 12 : (1, 12, 66, 220, 495, 792, 924, ...)
```

- **Row 4.** `V, E, F = 4, 6, 4` are literally the middle three entries. The
  row's palindrome **is** the self-duality: `V = F` because `C(4,1) = C(4,3)`.
- **Row 7.** The **two 7s** and the **two 21s** are the dual pair — Császár
  `(7, 21, ·)` and Szilassi `(·, 21, 7)`. Here the palindrome is the duality
  *between two objects* rather than within one.
- **The central 35 = `C(7,4)` is the number of tetrahedra inside `K₇`.** So the
  user's "the tetrahedron could be emergent out of the two toroidal polyhedra"
  has a precise reading: the Császár skeleton contains exactly `C(7,4) = 35`
  tetrahedra, and 35 is the row's central entry.

In general `V = C(n,1)`, `E = C(n,2)`, `F = 2E/3` (the triangulation constraint,
integral iff `n ≡ 0, 1 mod 3`), and tetrahedra `= C(n,4)`. At `n = 12`:
`12, 66, 44, 495`.

---

## Pass 2032 — **every line of `W(3,3)` is a tetrahedron**

This is where the proposal meets the arc:

```text
all 40 t.i. lines are 4 pairwise-collinear points (= K4 skeleton) : True
spread lines 10, each contributing C(4,2) = 6 edges -> residual 60
```

> **The residual set of a spread seed in `W(3,3)` is ten disjoint tetrahedra.**

Pass 2016 said "`q²+1` copies of `K_{q+1}`". At the substrate's own `q = 3` that
reads: **ten tetrahedra**. The unit the user is pointing at is the substrate's
own line.

---

## Pass 2033 — the `1/q` law is a **1-factor selection**

`K_{q+1}` with `q+1` even is 1-factorizable into exactly `q` perfect matchings:

```text
q= 3 : K4  has  6 edges =  3 matchings x 2 edges   -> 1/3
q= 5 : K6  has 15 edges =  5 matchings x 3 edges   -> 1/5
q= 7 : K8  has 28 edges =  7 matchings x 4 edges   -> 1/7
q=11 : K12 has 66 edges = 11 matchings x 6 edges   -> 1/11
```

> **`σ_S` selects one 1-factor of each `K_{q+1}`. That is the entire `1/q` law.**

At `q = 3` it is as small as it gets: `K₄` has exactly **three** perfect
matchings — `{01|23}, {02|13}, {03|12}` — and `σ_S` picks one of the three. The
`3` in `1/3` is the number of ways to pair four points.

### The echo worth flagging carefully

`χ(H) = 9` is a **1-factorization** question for the frame hypergraph (Pass
1972), and the `1/q` law is a **1-factor selection** in `K_{q+1}`. The same
concept at two levels. I am recording that as an echo and **not** as a claim —
this arc has three withdrawn results from treating a shared concept as a shared
object.

---

## Pass 2034 — the BC helix: a clean negative

A Boerdijk–Coxeter helix is a chain of **face-bonded** tetrahedra. Testing how
the 40 tetrahedra of `W(3,3)` actually bond:

```text
|L_i ∩ L_j| over all 780 pairs : {0: 540, 1: 240}
pairs sharing >= 2 points      : 0
```

> Two distinct t.i. lines meet in **at most one point**. No two share an edge,
> let alone a face. **The 40 tetrahedra are vertex-bonded only, so there is no
> BC helix in the line structure.**

The 540 disjoint pairs are exactly the frames, and the 240 point-sharing pairs
are the flags. So the tetrahedra do assemble — but by vertices, into the frame
and flag geometry, not into a face-bonded helix.

---

## Pass 2035 — what the "unit" claim does and does not support

**Supported.** The tetrahedron is the substrate's line; the residual is ten of
them; `σ_S` acts on each as a 1-factor choice; the `1/q` law is that choice; the
tetrahedron is the self-dual rung where both maximal adjacencies coincide, and
the toroidal pair is where they split.

**Not supported.** No face bonding, so no BC helix from the lines. And the
tetrahedron does not "emerge from" the toroidal pair in the oscillator's own
order — it *precedes* them at `h = 0`. What is true is the containment in the
other direction: `K₇` contains `C(7,4) = 35` tetrahedra.

**Not tested.** Whether the tetrahedron functions as a *unit* in the sense the
user means — a topological harmonic oscillator whose excitations are the higher
rungs. The oscillator exists in the repo (`dccxxiii`) and the tetrahedron is its
ground state; whether the substrate's dynamics factor through it is a physics
claim this pass does not make.

---

## Prior art

- `dccxxiii` — **owns** the genus oscillator and the three clocks.
- BT1844 / `w33_toroidal_h6_66_bridge` — **own** the complete-adjacency ladder.
- Pass 2016 — the `K_{q+1}` decomposition; Pass 2029 — the proof it rests on.
- The two-maximal-adjacencies framing, the Pascal reading, and the tetrahedron-
  as-unit proposal are the user's.

## Still open

- `χ(H) = 9`, now visibly a 1-factorization question at the level above the one
  the `1/q` law settles.
- Whether the two 1-factorizations are related by anything more than analogy.
