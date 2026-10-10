# Passes 11834–11838 — the finite AdS₄ as a field-theory skeleton: Dirac singletons, bulk reconstruction needs both contexts and splits, a finite Poincaré group with Wigner's little groups, and E₈ leaves only one charge commuting with Lorentz

Producer: `analysis/w33_pass11834_11837_singletons_bulk_poincare_e8.py` (exact over all 51 840 elements of Sp(4,3))
Frozen: `data/w33_pass11834_11837_singletons_bulk_poincare_e8.json`
Lean: `formal/W33/Pass11838CliffordQuadric.lean`
Regression: `tests/test_w33_pass11834_11838.py`

These passes follow Passes 11831–11833, where the ω-traceless bivectors of the two-qutrit phase space formed a Clifford
quadric. Its 121 points are:
* 40 contexts: the boundary;
* 45 tensor splits;
* 36 Kramers reversals: the bulk.

There, the stabiliser of a reversal was SL(2,9)·2, and the tangent space was a finite Minkowski space. Here the five
follow-ups are executed.

## 11834 — finite Dirac singletons and a Flato–Fronsdal test

**The linear Weil representation, built exactly.** Each of six transvections is lifted to a unitary U with
U D(v) U⁻¹ = D(gv) for the symmetric Weyl operators (τ = ω², so the action has no phases). The lift is normalised to
det 1 and order 3. The group they generate carries a μ₃ cocycle, which is nontrivial, and it is removed by solving for
generator phases. The result is a homomorphism Sp(4,3) → SU(9): the error on random products is 2·10⁻¹⁴, and the
Clifford action is exact. The parity U₋₁ = P has trace 1, so C⁹ = W₊ ⊕ W₋ with dimensions 5 and 4.

* **Rac = W₊ (5) and Di = W₋ (4)** are irreducible, distinct and complex (Frobenius–Schur indicator 0). By Pass 11210,
  every bulk point's antiunitary T has T² = P: +1 on Rac (bosonic) and −1 on Di (fermionic, Kramers pairs). This matches
  Dirac's singletons: the metaplectic representation of Sp(4,ℝ) = Spin(2,3) splits into Rac (scalar) and Di (spinor).
* **Two-singleton states.**
  * Rac⊗Rac* = 1 + 24 and Di⊗Di* = 1 + 15_D.
  * Rac⊗Di* = 20_c is irreducible.
  * Rac⊗Rac* + Di⊗Di* = 1 + C[40 points of W(3,3)] exactly, the parity-even part of W⊗W̄ = C[F₃⁴].
* **Flato–Fronsdal analogue.** In AdS₄, Rac⊗Rac is multiplicity-free and consists of the bulk massless fields. Here:
  * **Rac⊗Rac = Sym² Rac (15) ⊕ Λ² Rac (10)**, both irreducible, so multiplicity-free;
  * **Sym² Rac is exactly the one nontrivial constituent that the bulk C[36] and the boundary C[40 contexts] share**
    (Gram multiplicities 1, 1, and 0 against everything else);
  * Λ² Rac lies in no permutation module;
  * Di⊗Di = Sym²(10) ⊕ Λ²(6) and Rac⊗Di = 20 are also multiplicity-free, and none of their constituents is a scalar bulk
    or boundary mode.

## 11835 — bulk modes, and what the boundary can reconstruct

| module | constituents |
|---|---|
| C[36 Kramers reversals] (bulk) | 1 + **15_S** + **20_b** |
| C[40 contexts] (boundary) | 1 + **15_S** + 24 |
| C[45 splits] | 1 + **20_b** + 24 |
| C[40 points] | 1 + 24 + 15_D |

Here 15_S = Sym² Rac, 24 = Rac⊗Rac* − 1, 15_D = Di⊗Di* − 1, and 20_b is a real 20 that is not Rac⊗Di*. Each of these
modules has rank 3, and their permutation characters are the classical ones of U₄(2). The identification with singleton
bilinears is the new part.

* **Bulk modes.** The orthogonality graph on the 36 is SRG(36,15,6,6), with spectrum 15¹ 3¹⁵ (−3)²⁰. The 3-eigenspace
  is 15_S and the (−3)-eigenspace is 20_b.
* **Boundary reconstruction is partial.** Each reversal is orthogonal to 10 contexts (its celestial sphere), and each
  context to 9 reversals. This incidence has **rank 16 = 1 + 15**: the boundary sees exactly the Sym² Rac modes and is
  **blind to the 20-dimensional bulk mode**. Since C[36] and C[40] share only two constituents, no Sp-equivariant
  boundary-to-bulk map can do better.
* **The splits see the rest.** The bulk–split incidence (15 orthogonal splits per reversal) has **rank 21 = 1 + 20**.
  So **C[36] = image(contexts) + image(splits)**, overlapping only in constants (16 + 21 = 36 + 1).
* **Reading.** In this finite AdS₄ the interior is reconstructed only by measurement contexts *together with* subsystem
  factorisations. The boundary alone recovers the bilinear (two-Rac) sector. The remaining bulk mode is visible only
  through how the system splits into subsystems.

## 11836 — a finite Poincaré group: mass shells and Wigner's little groups

The finite Poincaré group is M ⋊ SL(2,9), with M = p^⊥ the tangent Minkowski space at a Kramers reversal (81 vectors).

* **The invariant operators are functions of mass.** Plane waves k ∈ M fall into four shells: k = 0, null (20),
  Kramers-type (30) and split-type (30). The three invariant Cayley operators have eigenvalues:

  | connection set | null k | split-type k | Kramers-type k |
  |---|---:|---:|---:|
  | null (light cone, Brouwer–Haemers) | −7 | 2 | 2 |
  | split-type | 3 | 3 | −6 |
  | Kramers-type | 3 | −6 | 3 |

  So they separate every shell. In particular (A_null − 2)/(−9) is the projector onto the massless shell, a finite
  on-shell (d'Alembertian) condition.
* **Massless little group.** Order 36 (72 with parity). It is 3² ⋊ ℤ₄: the 8 elements of order 3 commute, and the
  abelianisation has order 4. It has 12 classes: **4 helicity characters** (ℤ₄, so h ∈ {0, ½, 1, 3/2} mod 2, with
  −1 = the 2π rotation) and **8 two-dimensional representations** on which the translations act nontrivially. These are
  the finite analogue of Wigner's ISO(2) and its "continuous-spin" representations.
* **Massive little groups.** For both the Kramers-type and the split-type shell the little group is **SL(2,3)**: the
  order statistics match exactly, there are 7 classes, and the abelianisation is ℤ₃. This is the finite SU(2), and it is
  **the one-qutrit Clifford (symplectic) group**. Over F₃ the "timelike" and "spacelike" little groups coincide; there is
  no compact/non-compact distinction. Massive spins are its irreps 1, 1′, 1″, 2, 2′, 2″, 3: spin 0 and spin ½ each come
  in three ℤ₃-labelled copies, spin 1 once. *(A structural observation, not a claim of three generations.)*

## 11837 — the two-qutrit E₈ under the Clifford group: one charge commutes with Lorentz

The Weil representation acts on E₈ = sl₉ ⊕ Λ³C⁹ ⊕ Λ³C⁹* (Pass 11681) by automorphisms. The μ₃ ambiguity of the lifts
acts trivially on Λ³.

* **sl₉ = C[80 nonzero Paulis]** = 1 + 15_D + 24 + 20_c + 2̅0̅_c (norm 5, multiplicity-free).
* **Λ³ (84)** has 7 constituents (norm 7). None lies in a permutation module, and Λ³ is not self-dual.
* **The centraliser in E₈ of the finite Lorentz group SL(2,9) is one-dimensional**: the u(1) generated by P − 1/9,
  where P = the Weil parity = T² = the Rac/Di grading. The centraliser of all of Sp(4,3) is the same line. **No
  non-abelian internal algebra of E₈ commutes with the finite Lorentz group** in this embedding. The only surviving
  charge is a boson/fermion-type parity (a fermion-number-like U(1)). This is a Coleman–Mandula-shaped no-go for
  getting an internal gauge group as the commutant of spacetime inside the two-qutrit E₈.

## 11838 — Lean: the Clifford quadric

`W33.Pass11838CliffordQuadric` proves the following, over every commutative ring:
* J² = Q·1 with Q = ae + b² + cd;
* the polarised anticommutator J_x J_y + J_y J_x = (Q(x+y) − Q x − Q y)·1;
* ω-self-adjointness Jᵀ Ω = Ω J;
* the similitude law Jᵀ Ω J = Q·Ω;
* the Kramers corollary: Q = −1 gives J² = −1 and anti-symplectic J.

Over ZMod 3, by `decide`, it proves the counts 80 + 90 + 72 of nonzero bivectors (projectively 40 + 45 + 36).

## Prior art and scope

* **Classical.**
  * Weil representation of Sp(2n,q), its even/odd splitting, and its linearity for odd q.
  * The permutation characters of U₄(2) = PSp₄(3) on 36/40/40/45 points (ATLAS).
  * Dirac's singletons (1963) and the Flato–Fronsdal theorem (1978).
  * Wigner's little groups.
* **Corpus.**
  * Pass 11210: T² = parity, the Kramers class.
  * Pass 11680: even/odd Weil halves ↔ symmetric/antisymmetric Pauli-invariant triples.
  * Pass 11681: the two-qutrit E₈.
  * Passes 11831–11833.
  * Parallel Round 29 Front IV (`analysis/2026-10-09_toe29_cat_covers_e7_ads_c8.md`) independently reproduces the
    1+20+30+30 tangent census and the light-cone heat kernel. It proves that no translation-invariant strict causal order
    exists on F₃⁴ (3v = 0). That is consistent with this packet: "massless/massive" here are square classes, and no time
    orientation is used or claimed.

  Searches for Wigner, little group, Poincaré, singleton and Flato found only unrelated uses (Higgs little groups,
  Wigner's theorem).
* **New here.**
  * The exact linear Weil representation as an artefact.
  * Sym² Rac = the bulk∩boundary mode, with Rac⊗Rac multiplicity-free.
  * The complementarity of contexts and splits in bulk reconstruction.
  * The finite Poincaré shells and little groups: 3²⋊ℤ₄ massless, SL(2,3) massive.
  * The one-dimensional E₈ centraliser of the finite Lorentz group.
  * The Lean formalisation.
* **Boundary.**
  * These are representation-theoretic statements about a finite kinematic skeleton.
  * "Massless/massive, helicity, spin, bulk/boundary" are names fixed by the stabiliser criteria, not physical
    identifications. No dynamics, coupling, scale or continuum limit is derived.
  * The Flato–Fronsdal statement is an isomorphism of Sp(4,3)-modules, not a constructed holographic map.
