# PART CCCCXXII — Photonic Harmonic TQC Algebra from 7 Toroidal Realizations

## Overview

This bridge derives a **photonic harmonic TQC algebra A(7)** directly from the
coordinate and combinatorial data of the seven distinct toroidal polyhedra
realizations in R³ (five Császár + two Szilassi).

The algebra connects the geometric objects of Part CCCCXXI (Toroidal–Fano
bijection) to the photonic bus architecture of Part CCCCXVIII, showing that
every invariant of the photonic TQC bus is a polynomial in q = 3 arising from
the realization data.

---

## The Seven-Mode Algebra A(7)

Each of the 7 realizations defines one photonic mode:

| Mode | Realization  | Role     | Volume                  |
|------|-------------|----------|-------------------------|
| 0    | Császár-1   | input    | 125 = (Q+λ)³ = 5³       |
| 1    | Császár-2   | input    |                         |
| 2    | Császár-3   | input    |                         |
| 3    | Császár-4   | input    |                         |
| 4    | Császár-5   | input    |                         |
| 5    | Szilassi-1  | ancilla  | 5226/5 (denom = Q+λ = 5)|
| 6    | Szilassi-2  | ancilla  | 7976/9 (denom = Q² = 9) |

The **5 + 2 = Φ₆ split** matches the KLM Type-II ancilla architecture:
- 5 = Φ₆ − λ = q² − 2q + 2 input modes (Császár)
- 2 = λ ancilla modes (Szilassi); p_ancilla = 1/μ = 1/4

### Algebra Structure

```
A(7) = Span{ a_i , a†_i : i = 0..6 }   (bosonic Fock modes)

K7 hopping Hamiltonian:
  H_hop = Σ_{i<j} ( a†_i a_j + h.c. )   [21 bond operators]
  Spectral gap = Φ₆ = 7
  Eigenvalues: 6 (×1),  −1 (×6)

Fano cubic interaction:
  V_F = Σ_{(i,j,k) ∈ Fano lines} ( a†_i a†_j a†_k + h.c. )   [7 triples]
  G₂ symmetry: dim G₂ = 14 = 2·Φ₆

Full Hamiltonian:
  H = H_hop + g V_F
```

---

## K7 Spectral Algebra

All 7 realizations share the same **K₇ edge set** (E = 21 = Q·Φ₆).  The
complete graph K₇ defines the hopping algebra:

| Invariant                     | Value | Source            |
|-------------------------------|-------|-------------------|
| K₇ edges                      | 21    | Q · Φ₆            |
| K₇ max eigenvalue             | 6     | Φ₆ − 1            |
| K₇ min eigenvalue             | −1    | (×6, cyclic 1/7)  |
| K₇ spectral gap               | 7     | Φ₆                |
| K₇ handshake: n·degree        | 42    | 2 · 21            |
| Directed K₇ edges             | 42    | (Φ₆−1) · Φ₆       |

---

## Fano Interaction Structure

The 7 lines of the Fano plane PG(2, F₂) provide the 3-photon interaction
vertices of the algebra.  The Fano incidence matrix B (7×7) satisfies the
Szegedy relations:

```
BB^T  = 2I + J   (= λI + J at λ = 2)
B^T B = 2I + J   (self-dual design)
```

| Invariant              | Value | Source            |
|------------------------|-------|-------------------|
| Fano lines             | 7     | Φ₆                |
| Points per line        | 3     | Q                 |
| Lines through a point  | 3     | Q                 |
| Total flags            | 21    | K₇ edges          |

---

## C₂ Orbital Bell-Pair Mode Decomposition

Every realization has a C₂ half-turn symmetry (x,y,z) → (−x,−y,z).
The orbits of vertices and faces under C₂ exhibit **exact duality**:

| Realization | V orbits | F orbits |
|-------------|----------|----------|
| Császár     | 4 = μ    | 7 = Φ₆   |
| Szilassi    | 7 = Φ₆   | 4 = μ    |

- **Császár** vertex orbits: 3 paired vertices + 1 apex (V6, fixed) = μ = 4
- **Szilassi** vertex orbits: 7 paired vertices, no fixed point = Φ₆ = 7
- **Szilassi** face orbits: 3 paired hexagons + 1 singleton (F4, self-maps) = μ = 4

Combined orbital mode counts:
- 5 Császár × μ = 20 = V_W(3,3) / 2 orbital modes
- 2 Szilassi × Φ₆ = 14 = G₂_DIM orbital modes

---

## Volume Harmonic Spectrum

| Realization | Volume (exact)    | Algebraic meaning        |
|-------------|-------------------|--------------------------|
| Császár-1   | 125 = 5³          | (Q+λ)³, ground state     |
| Szilassi-1  | 5226/5            | denominator = Q+λ = 5    |
| Szilassi-2  | 7976/9            | denominator = Q² = 9     |

---

## Heawood 14-Mode Harmonic Rail

The Heawood graph (incidence graph of the Fano plane) is the harmonic rail of
the TQC bus:

| Invariant                        | Value | Source      |
|----------------------------------|-------|-------------|
| Heawood vertices                 | 14    | G₂_DIM      |
| Heawood edges                    | 21    | K₇ edges    |
| Heawood degree                   | 3     | Q           |
| Harmonic oscillator frequency²   | 2     | λ           |
| Bipartite parts                  | 7 + 7 | Fano pts + lines |

The Heawood biadjacency matrix equals the Fano incidence matrix B, so
BB^T = 2I + J gives the non-trivial eigenvalue **2 = λ**, confirming
frequency² = λ.

---

## Photonic Bus Connections

| Quantity                      | Value  | Source                   |
|-------------------------------|--------|--------------------------|
| Type-II fusion probability    | 1/2    | 1/λ                      |
| KLM primitive probability     | 1/4    | 1/μ                      |
| Fusion denominator            | 2      | Toric logical qubits = λ |
| KLM denominator               | 4      | Toric GSD = μ            |
| Sum of denominators           | 6      | Φ₆ − 1 = K₇ degree       |

---

## G₂ / Algebra Dimension / CSS Toric Closing

| Invariant                     | Value | Identity                    |
|-------------------------------|-------|-----------------------------|
| G₂ Lie algebra dimension      | 14    | 2·Φ₆                        |
| U(7) algebra dimension        | 49    | Φ₆² = 2·K₇_edges + Φ₆      |
| \|PSL(2,7)\|                  | 168   | 24·Φ₆                       |
| Toric logical qubits          | 2     | λ (genus-1 → k = 2g = 2)   |
| Toric GSD                     | 4     | μ                            |
| Császár Euler characteristic  | 0     | 7 − 21 + 14 = 0 (torus)    |
| μ + λ                         | 6     | Φ₆ − 1 = K₇ max eigenvalue |

---

## Algebra Theorem

> The seven toroidal polyhedra realizations in R³ generate the 7-mode
> photonic harmonic TQC algebra A(7).  The 5 Császár realizations form the
> input register with K₇ hopping Hamiltonian (spectral gap Φ₆ = 7, 21 bond
> operators) and 7 Fano triple-mode interactions.  The 2 Szilassi
> realizations are the KLM Type-II ancilla pair (p = 1/4 = 1/μ), giving the
> 5+2 = Φ₆ bus split.  C₂ symmetry decomposes each Császár into μ = 4
> Bell-pair modes and each Szilassi into Φ₆ = 7 Bell-pair modes; combined
> totals are 5·4 = 20 = V_W33/2 and 2·7 = 14 = G₂_DIM orbital modes.  The
> Heawood 14-mode harmonic rail has frequency² = λ = 2 and biadjacency
> equal to the Fano incidence BB^T = 2I + J.  Volume spectrum: C1 = 5³ =
> (Q+λ)³, S1 = 5226/5 (denom Q+λ), S2 = 7976/9 (denom Q²).  The full
> algebra has U(7) dimension Φ₆² = 49 = 2·K₇_edges + Φ₆, G₂ symmetry of
> dimension 2·Φ₆ = 14, and the toric CSS code on each Császár K₇
> triangulation has k = 2 = λ logical qubits and GSD = 4 = μ.  Every
> constant is a polynomial in q = 3.

---

## Honesty Boundary

This is an invariant-matching algebra theorem.  It does not claim a new
optical threshold, a physical G₂ anyon realisation, or a new proof of the
K₇ CSS distance bound.

---

## Verification

- **48/48 checks pass** (exact arithmetic, stdlib only)
- **98/98 pytest tests pass**
- Results: `PART_CCCCXXII_toroidal_photonic_algebra_results.json`

---

## Files

| File | Purpose |
|------|---------|
| `exploration/PART_CCCCXXII_TOROIDAL_PHOTONIC_ALGEBRA.py` | Bridge (48 checks) |
| `tests/test_toroidal_photonic_algebra_ccccxxii.py` | 98 pytest tests |
| `PART_CCCCXXII_toroidal_photonic_algebra_results.json` | Results (PASS) |
| `PART_CCCCXXII_TOROIDAL_PHOTONIC_ALGEBRA_BRIDGE.md` | This document |

---

## Related Parts

- **CCCCXXI** — Seven Toroidal Polyhedra ↔ Fano Octonion Framework (source realization data)
- **CCCCXVIII** — Photonic Harmonic TQC Bus (five-layer bus; this part extends with explicit realization algebra)
- **CCCCXX** — G₂ / Octonion / Fano integration
