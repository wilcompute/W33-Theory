# Part DCCXLIX — The Octahedron as the Phase Space of the Closure Clock

**Bridge:** `verify_dccxlix_octahedron_closure_phase_space.py` — Verified
**Tests:** `tests/test_dccxlix_octahedron_closure_phase_space.py` — 23/23 pass
**Data:** `data/dccxlix_octahedron_closure_phase_space.json`

---

## 1. What this part identifies

The parallel chain DCCXL–DCCXLVIII built a complete discrete QFT on a
6-level closure-clock with nilpotent generator G = (½)S (DCCXL),
resolvent R(z) (DCCXLI), Jordan residues (DCCXLII), action principle
(DCCXLIII–XLV), action jet tower (DCCXLVI), Ward recursion (DCCXLVII),
and retarded Green uniqueness (DCCXLVIII). The number 6 was a hard
nilpotence cutoff with no explicit geometric realisation.

This part **identifies the closure clock with the octahedron's
vertex set** and shows that the octahedron's f-vector (6, 12, 8)
encodes the entire (nilpotence, codec, oscillator-modes) triple.

---

## 2. The octahedron correspondence

| octahedron data | value | W(3,3) reading |
|---|---:|---|
| **V** (vertices) | **6** | **nilpotence index of G** = q! = E(tetrahedron) = signed bivectors (DCCXIV) |
| **E** (edges) | **12** | **codec** = q(q+1) = generator transitions of G |
| **F** (faces) | **8** | **tomotope cells** = oscillator modes = rank E_8 (DCCXXVII) |
| χ | 2 | sphere Euler characteristic |
| degree (each vertex) | 4 | q + 1 = quaternion basis (DCCXXVIII) |
| antipodal pairs | 3 | q = ternary axes |

The octahedron's f-vector (6, 12, 8) is **exactly** the closure-clock
phase space:

* the **6 clock levels** T₀, …, T₅ ↔ the 6 octahedron vertices
  = the 6 signed Clifford bivectors {±B₂₃, ±B₃₁, ±B₁₂}
* the **12 codec transitions** of G ↔ the 12 octahedron edges
* the **8 oscillator modes** (1 + 5 + 2) ↔ the 8 octahedron faces

---

## 3. Octahedron = L(K₄) of the tetrahedron

The octahedron is the **line graph of K₄** — the 1-skeleton of the
tetrahedron. So each closure-clock level T_i is one **tetrahedron edge**,
and each generator transition is a pair of incident tetrahedron edges.

This places the closure clock at the same level as the DCCXXV tetrahedron
hinge: the tetrahedron's *vertices* host the self-dual sphere mode
(24 flags = 2 codec), and its *edges* host the closure-clock phase space
(6 levels = q!).

---

## 4. The 8 faces as sign patterns

Each octahedron face contains one vertex from each of the three antipodal
pairs (one signed B-bivector per axis), so there are 2 × 2 × 2 = **8
faces** indexed by sign patterns in {±, ±, ±}.

These 8 sign patterns correspond, slot-by-slot, to:

* the 8 **tomotope cells** (DCCXXV; 1 sphere + 5 Császár + 2 Szilassi)
* the rank-8 **Cartan of E_8** (DCCXXVII)
* the 8 **transverse modes of the superstring** (DCCXXVI)

So one octahedron face is "one sign pattern of the three Clifford axes,"
and the **collection of 8 faces unifies four previously-disparate
"8-numbers" in the program**.

---

## 5. The closure clock on tetrahedron edges

The parallel agent's closure clock has

$$
G = \tfrac{1}{2} S, \qquad G^6 = 0 \text{ (nilpotent of index 6)},
$$

and its propagator / resolvent

$$
R(z) = \sum_{k=0}^{5} (zG)^k = (I - zG)^{-1}.
$$

Under the octahedron identification:

* G acts as a **forward walk on tetrahedron edges**, advancing each clock
  level T_i to T_{i+1};
* the factor ½ is the "octahedron-edge-cost" weighting;
* the nilpotence at index 6 is the **finite horizon** — six tetrahedron
  edges exhaust the K₄ edge set;
* the maximal propagation G⁵_{0,5} = 1/32 = (½)⁵ is the deepest reachable
  edge from a starting edge.

Equivalently, the closure resolvent K = ∑_{n=0}^{5} G^n is the **sum of
all ordered walks on octahedron edges from a fixed start**, with the
sphere-Euler-characteristic finite cutoff guaranteed by the tetrahedron's
finite edge set.

---

## 6. Joint chain identification

Combining DCCXVII–DCCXXVIII (my arc) with DCCXL–DCCXLVIII (the closure-
clock arc):

| polytope | role |
|---|---|
| **tetrahedron** (V=4, E=6, F=4) | self-dual sphere mode (DCCXXV); 24 flags = 2 codec |
| **octahedron** (V=6, E=12, F=8) | **closure-clock phase space (this part)** |
| **Császár / Szilassi** (V=7, F=14) | toroidal duality pair (DCCXXV); 5 + 2 = 7 realisations |
| **tomotope** (4, 12, 16, 8) | abstract 4-polytope bookend (DCCXXV); 192 flags = sum |

All four are intertwined by the q = 3 saturation: the tetrahedron is the
genus-0 mode, the octahedron is its line-graph (DCCXLIX), the toroidal
pair is the genus-1 mode (DCCXXV), and the tomotope is the abstract
4D reification (DCCXXV).

---

## 7. Decisive identity

$$
\boxed{\;
\text{octahedron} \;=\; L(K_4) \;=\; \text{closure-clock phase space};
\quad (V, E, F) = (6, 12, 8) = (\text{nilpotence}, \text{codec}, \text{tomotope cells}).
\;}
$$

---

## 8. Honest boundary

* This part is a **geometric bijection** between the closure-clock chain
  and the octahedron; it does **not** derive the closure action, Ward
  recursion, or Green's function from octahedral geometry.
* The 8-faces-as-sign-patterns identification matches the tomotope cells
  numerically; the structural correspondence between octahedron faces
  and tomotope cells is the natural one but not uniquely forced.

---

## 9. One-line summary

$$
\boxed{\;
\text{closure-clock phase space} \;=\; \text{octahedron} \;=\; L(\text{tetrahedron});
\quad (V, E, F) = (q!, \text{codec}, \text{rank } E_8).
\;}
$$
