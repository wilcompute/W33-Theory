# Pass 11657 — the two-qutrit Hesse space geometrises W(3,3) and its 45 factorisations: states are lines, ticks are points, factorisations are mirrors

Producer: `analysis/w33_pass11657_hesse_space_geometrises_w33.py`
Certificate: `data/w33_pass11657_hesse_space_geometrises_w33.json`
Regression: `tests/test_w33_pass11655_11662.py`

**The space.** The 5-dimensional space of Heisenberg-invariant cubics (Pass 11651) is projectively P⁴, with symmetry
group G₃₃, the Burkhardt group.

## The dictionary

| two-qutrit object | in W(3,3) / GQ | in the Hesse P⁴ | relation in P⁴ |
|---|---|---|---|
| 40 stabiliser bases | **lines** of W(3,3) (Lagrangians) | 40 **points** u_L | Q(4,3) graph: overlap 1/3 (Pass 11651) |
| 40 transvection ticks T_p | **points** of W(3,3) | 40 **lines** (2-dim eigenspaces of the Weil gate) and 40 **planes** (3-dim eigenspaces) | lines meet ⇔ p, q collinear: **the W33 point graph SRG(40,12,2,4)** |
| incidence p ∈ L | incidence | **u_L lies on the tick-line of p** | **160/160**, no false incidences |
| 45 tensor factorisations P ⊕ P^⊥ | points of GQ(4,2) (Pass 11177) | 45 **mirrors** of G₃₃ | orthogonal ⇔ octets disjoint: **SRG(45,12,3,3)**, 1980/1980 |

**Burkhardt, checked rather than assumed.**
* The unique G₃₃-invariant quartic I₄ vanishes identically on all 40 tick-planes: relative residual 2·10⁻¹⁵. **The tick
  planes are the 40 j-planes of the Burkhardt quartic.**
* I₄ and its gradient vanish at all 45 mirror roots. **The 45 factorisation mirrors are its 45 nodes.**
* The 40 stabiliser points are *not* on the quartic.
* So the classical Burkhardt configuration reads, in qutrit terms:

  **j-planes = elementary gates (points of W(3,3)); nodes = tensor factorisations; incidence = Pauli eigenstates.**

* This confirms BREAKTHROUGH 72's "j-planes ~ points of W(3,3)" as an incidence-preserving bijection, not just a count.

## Details

**Ticks.** Every one of the 40 transvection gates acts on the Hesse space with eigenvalue multiplicities (2, 3).
* Two tick-lines meet iff the points are collinear: (meet, collinear) occurs on 480 ordered pairs and
  (disjoint, non-collinear) on 1080.
* Two tick-planes meet in a line iff the points are collinear, and in a single point otherwise.
* **The tick-line carries the one-qutrit picture.** Each tick-line contains exactly the 4 stabiliser points of the
  Lagrangians through p. Since p^⊥/p is a one-qutrit phase space, the tick-line is a copy of the one-qutrit Hesse sphere
  P¹ with its four MUB vertices (Pass 11641).

**Factorisations.** For each of the 90 hyperbolic planes P, the local-parity involution σ_P (−1 on P, +1 on P^⊥) acts on
the Hesse space as a **reflection**.
* σ_P and σ_{P^⊥} give the same mirror, so there are **45 mirrors = 45 tensor factorisations = the 45 reflections of G₃₃**.
* **Two familiar reflections.**
  * The local parity of qutrit 2 is the reflection of the standard factorisation.
  * **SWAP** is the reflection of the diagonal ⊕ antidiagonal factorisation.
* **Orthogonality is Pass 11177's collinearity.** Mirror orthogonality coincides exactly (1980/1980) with Pass 11177's
  GQ(4,2) collinearity, i.e. disjoint octets.
* **A gate-level consequence.** A two-qutrit gate is perfect (AME) iff it moves a factorisation's mirror to an
  orthogonal mirror (Pass 11177, translated).
* **A non-criterion.** Commuting involutions do *not* give the relation: they agree on only 1440 of 1980 ordered pairs.

## Reading

**The repo's central geometry, made concrete.** W(3,3) and its 45 factorisations become concrete projective geometry of
one space, the cubic shadow of two qutrits:
* states (stabiliser bases) are points;
* elementary gates (ticks) are lines;
* "this state is an eigenstate of this tick's Paulis" is incidence;
* "how the register splits into A ⊗ B" is a mirror of the Burkhardt group;
* perfect scrambling is orthogonality of mirrors.

**The duality, seen.** The two SRG(40,12,2,4) graphs (the W33 point graph and its dual Q(4,3)) appear together, the first
on gates and the second on states. That is exactly the W(3,3) vs Q(4,3) duality, made visible.

**Prior art.**
* Classically, G₃₃ is the Burkhardt group: 45 nodes, 40 j-planes.
* PSp(4,3) ≅ PSU(4,2), and GQ(4,2) ≅ H(3,4).
* The 45 factorisations and GQ(4,2) are the Holotrade/Pass 11177 dictionary.
* The tick/state/mirror realisation inside the qutrit Hesse space is new here. The identification of the tick-planes with Burkhardt's j-planes,
  and of the mirrors with its nodes, is checked here through I₄.
