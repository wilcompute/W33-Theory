# Part CCLXVI — Tomotope as Universal Turing Machine Skeleton

## Theorem

The face-vector of the tomotope, the abstract regular 4-polytope with automorphism
group of order 192, is

    (TV, TE, TF, TC) = (4, 12, 16, 8)

and this tuple encodes the parameter set of a universal 2-state, 3-symbol Turing
machine in exact arithmetic alignment with the strongly regular graph W(3,3) =
srg(40, 12, 2, 4).

---

## The Three Layers of the Coincidence

### Layer 1 — Geometric (tomotope polytope)

The tomotope is the unique abstract regular 4-polytope with:

| face dimension | count |
|----------------|-------|
| vertices (0)   | TV = 4 |
| edges (1)      | TE = 12 |
| 2-faces (2)    | TF = 16 |
| cells (3)      | TC = 8 |
| flags           | T_FLAGS = 192 |
| blocks          | T_BLOCKS = 48 |

Euler characteristic: TV − TE + TF − TC = 4 − 12 + 16 − 8 = **0** (toroidal).

### Layer 2 — Computational (Turing machine)

A complete 2-state, 3-symbol Turing machine is parameterised by
(μ, q) = (tape-alphabet size, number of states) = (4, 3).  Its transition table
has μ × q = **12** entries.

| Turing quantity              | formula    | value |
|------------------------------|-----------|-------|
| tape-alphabet size μ          | TV        | 4     |
| number of states q            | —         | 3     |
| transition-table size         | μ × q     | **12** |
| symbol-pair configurations    | μ²        | 16    |
| 2^states (binary branching)   | 2^q       | 8     |
| Busy-Beaver BB(2,3)           | V33 − λ   | 38    |

Face-vector ↔ Turing table:

    TV = μ = 4                  (tape alphabet)
    TE = μ × q = 12 = K        (transition table  ≡  W(3,3) valency)
    TF = μ² = 16                (symbol-pair space)
    TC = 2^q = 8                (binary state tree)

### Layer 3 — Algebraic (W(3,3) and symmetry groups)

| identity | formula | value |
|----------|---------|-------|
| Face-vector sum = V33 | TV+TE+TF+TC | **40** |
| Face-vector split | TV+TF = TE+TC | 20 |
| Flags = \|Aut(C₂×Q₈)\| | T_FLAGS | **192** |
| \|W(E₆)\| / \|N\| | 51840 / 192 | **270** directed transport edges |
| \|W(D₅)\| / \|N\| | 1920 / 192 | **10** Schläfli valence |
| \|W(E₆)\| / \|W(D₅)\| | 51840 / 1920 | **27** lines on cubic surface |
| TE + g | 12 + 15 | **27** lines on cubic surface |

---

## The Cuboctahedron Bridge ("think outside the box")

A cube has 12 edges.  Truncating each at its midpoint produces a cuboctahedron with
exactly **12 vertices** — one per cube edge.  This is the geometric source of K = 12:

    cube → cut at 12 edge-midpoints → cuboctahedron (12 vertices)
    ≡  W(3,3) valency K = 12
    ≡  tomotope edge count TE = 12
    ≡  Turing transition-table size μ × q = 12

The group C₂ × Q₈ (which also has order 192 = T_FLAGS) contains exactly 12 elements
of order 4: the six quaternion axes {±i, ±j, ±k} paired with two C₂ parities.
These 12 elements are the algebraic cuboctahedron.

---

## Stabiliser Cross-Links

The orbit-stabiliser theorem applied to the 192-flag tomotope yields:

| orbit type | count | stabiliser size | W(3,3) meaning |
|-----------|-------|----------------|----------------|
| vertices  | 4     | 48             | T_BLOCKS = 48  |
| edges     | 12    | 16             | TF = 16        |
| 2-faces   | 16    | 12             | TE = K = 12    |
| cells     | 8     | 24             | f = 24 (W33 multiplicity) |

Every stabiliser size is a W(3,3) parameter.

---

## Orbit File Verification

All four orbit families are confirmed from machine-generated orbit data in
`axis_bundle_content/TOE_tomotope_axis_block_twist_v02_20260228/`:

| file | orbits | flags each | total |
|------|--------|-----------|-------|
| `tomotope_edge_orbits_12.json`   | 12 | 16 | 192 |
| `tomotope_vertex_orbits_4.json`  | 4  | 48 | 192 |
| `tomotope_face_orbits_16.json`   | 16 | 12 | 192 |
| `tomotope_cell_orbits_8.json`    | 8  | 24 | 192 |

Each family tiles the flag set {0, …, 191} without overlap (verified programmatically).

---

## Verification Summary

| file | checks | result |
|------|--------|--------|
| `exploration/PART_CCLXVI_TOMOTOPE_TURING_BRIDGE.py` | 30/30 | ✓ VERIFIED |
| `tests/test_tomotope_cclxvi.py` | 37/37 | ✓ ALL PASS |
| `PART_CCLXVI_tomotope_results.json` | — | `"verified": true` |

---

## Bridge Index (B1 – B30)

| id  | identity |
|-----|----------|
| B1  | TV+TE+TF+TC = V33 = 40 |
| B2  | TE = K = 12 |
| B3  | TV = MU = 4 |
| B4  | TV × q = TE  (Turing completeness μ×q=k) |
| B5  | TF = MU² = 16 |
| B6  | TC = 2^q = 8 |
| B7  | TC = 2×MU = 8 |
| B8  | TE/TV = q = 3 |
| B9  | TF/TV = MU = 4 |
| B10 | TF/TC = LAM = 2 |
| B11 | TV−TE+TF−TC = 0 (Euler = 0) |
| B12 | TV+TF = TE+TC = 20 |
| B13 | T_FLAGS = N_ORDER = 192 |
| B14 | T_FLAGS = TE × TF |
| B15 | T_FLAGS = TV × T_BLOCKS |
| B16 | T_FLAGS = TC × f |
| B17 | \|N\|/TE = TF = 16 |
| B18 | \|N\|/TF = TE = 12 |
| B19 | \|N\|/TC = f = 24 |
| B20 | \|N\|/TV = T_BLOCKS = 48 |
| B21 | \|order-4 elements of C₂×Q₈\| = TE = K = 12 |
| B22 | cuboctahedron vertices = 12 = K |
| B23 | \|W(E₆)\|/\|N\| = 270 |
| B24 | \|W(D₅)\|/\|N\| = 10 |
| B25 | \|W(E₆)\|/\|W(D₅)\| = 27 |
| B26 | q × MU = K |
| B27 | BB(2,3) = V33 − λ = 38 |
| B28 | T_BLOCKS/TE = TV = 4 |
| B29 | T_BLOCKS/q = TF = 16 |
| B30 | TE + g = 27 (lines on cubic surface) |
