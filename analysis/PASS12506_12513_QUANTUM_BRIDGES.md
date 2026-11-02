# Passes 12506–12513: braiding five metaplectic anyons acts transitively on the minimal codewords; the q = 9 "240" is not E₈

Claude track. Producer: `analysis/w33_pass12506_to_12513_quantum_bridges.py`. Drivers in `analysis/search_drivers_12466`:
`braid_codewords.py` and `e8_icosian_probe.py`. Context:

- the other track's TL₆ / SU(2)₄ braid representation (ad8846e59);
- its A₅ × C₂ torsion work on the q = 9 set (937445da5, 6343cdf59);
- Pass 173's route code;
- 12501's q = 9 stabiliser.

## 12507: braiding acts on the minimal even line sets of W(3,3)

The other track (ad8846e59) realised the Temperley–Lieb algebra TL₆ at δ = √3, the SU(2)₄ / metaplectic point, on two qutrits. Its
braid generators are the order-3 Clifford "tick" gates, i.e. symplectic **transvections** T_p(x) = x + ω(x,p)p along an induced path
p₀ … p₄ in the noncommutation graph.

So the braid group B_k acts on W(3,3) and on the **216 minimal even line sets**: Pass 173's route codewords, one PSp(4,3)-orbit.
`braid_codewords.py` checks the braid relations and far commutation, then computes:

| braid group | generators | image on the 40 points | orbits on the 216 codewords |
|---|---|---|---|
| B₃ | 2 | order **24** = SL(2,3), binary tetrahedral | 11 (4 × 12, 7 × 24) |
| B₄ | 3 | order **648** | **108 + 108** |
| B₅ | 4 | order 25,920 = PSp(4,3) | **216 (transitive)** |
| B₆ | 5 | 25,920 | 216 |

**The B₄ image (order 648)** has centre of order 3, derived subgroup of order 216, and a quotient by the centre of order 216 whose
element-order profile is exactly that of the Hessian group **ASL(2,3) = 3²:SL(2,3)** (orders 1, 2, 3, 4, 6 with counts 1, 9, 80, 54,
72). Cui–Wang report that the braid image of the one-qutrit SU(2)₄ metaplectic model is a subgroup of SU(3) of order 648 with centre
Z₃, whose quotient by the centre is the Hessian group of order 216. Order, centre and quotient profile all match. Isomorphism is not
proved here [C].

**Reading [I].** With metaplectic anyons as the braiding substrate:

- **five anyons** suffice for braiding alone to move any minimal codeword of the two-qutrit line code to any other;
- *(Later: Pass 12521 identifies the halves as "the fixed point c covered / not covered" and G as its stabiliser; see `PASS12518_12525_HYPEROVAL_FLOOR_HESSE_DICTIONARY.md`.)*
- **four anyons** split the 216 supports into two halves of 108. This is analogous to, but not the same object as, Pass 173's
  split of the 432 *signed* minimal vectors into two chiral orbits of 216. Whether the 108 + 108 halves are exactly the images of
  Pass 173's chiral orbits has not been checked [C];
- **three anyons** give the binary tetrahedral group.

## 12506: the 240 covered points of the q = 9 set are not an E₈ root system

The 48-line set at q = 9 covers 240 points, and its stabiliser contains 2I (McKay: 2I ↔ E₈; the E₈ roots are the icosians). Testing
the obvious hypothesis (`e8_icosian_probe.py`):

- **Orbits.** The 480 non-swap stabiliser matrices act as 240 permutations of the 240 points. They are **not regular**: there are two
  orbits of 120, merged by the X ↔ Y swap. 2I acts as A₅ with four free orbits of 60.
- **Geometry.** The collinearity graph on the 240 points is 32-regular with an irregular spectrum. The E₈ root graph, computed from
  the roots in the same script as a control, is 56-regular with spectrum 56, 28, 8, −2, −4.

**Verdict:** a numerical coincidence with an orbit-level echo (two halves of 120 swapped by an involution, as E₈ = 2I ⊔ τ·2I), but no
E₈ root geometry. Recorded as a negative so it is not re-chased. The other track's A₅ × C₂ (order 120) action on this set (937445da5)
is a subgroup of 12501's full order-480 stabiliser.

## 12508: what the literature says about these bridges

- **Two-qutrit geometry.** W(3,3) is the commutation geometry of two qutrits, with automorphisms tied to W(E₆) (Planat–Saniga and
  coauthors, 2007). State-independent contextuality from two-qubit states does **not** generalise to odd-prime qudits, which agrees
  with 12499.
- **Metaplectic anyons.** SU(2)₄ braiding is not universal: its image is a finite Clifford group, and universality needs an extra
  non-Clifford gate or a measurement (Cui–Wang 2015; Cui–Hong–Wang). The other track's TL₆ / SU(2)₄ representation sits inside this
  known picture.
- **Golden gates.** Parzanchevski–Sarnak golden gates use finite subgroups of PU(2) (octahedral = single-qubit Clifford mod phase;
  icosahedral), with reductions related to Ramanujan Cayley graphs of PSL(2,p) (Lubotzky–Phillips–Sarnak). The exceptional subgroups
  of PGL(2,q) that stabilise our minimal even sets (S₄ for the cube at q = 7, A₅ at q = 9 and q = 11) are abstractly the same groups.
  **This is an analogy [I], not a computed map.** A concrete bridge would have to match a specific reduction of the golden-gate lattice
  with the stabiliser in PSp(4,q). It has not been built.

## 12509: is 48 the minimum at q = 9? (status)

`q9_le46.py` (12502) asks whether an even line set of size ≤ 46 exists. Its result is recorded in `q9_le46.json` when the run
finishes. Only INFEASIBLE would be a proof.

## Sources

- M. Planat, A.-C. Baboin, M. Saniga, *Multi-line geometry of qubit-qutrit and higher-order Pauli operators* (2007), and *On the Pauli
  graphs of N-qudits*, arXiv:quant-ph/0701211.
- S. X. Cui, Z. Wang, *Universal quantum computation with metaplectic anyons*, J. Math. Phys. 56 (2015), arXiv:1405.7778; S. X. Cui,
  S.-M. Hong, Z. Wang, *Universal quantum computation with weakly integral anyons*, arXiv:1504.03383.
- O. Parzanchevski, P. Sarnak, *Super-Golden-Gates for PU(2)*, Adv. Math. (2018), arXiv:1704.02106.
- *Two-letter words and a fundamental homomorphism ruling geometric contextuality*, arXiv:1605.07118.

## 12509: q = 9 minimality — the search did not finish (status of record)

`q9_le46.py` ran for 38,814 s (10.8 h, longer than its 3 h limit because the machine was loaded) and ended **UNKNOWN**. It found no
even line set of ≤ 46 lines, and it did not prove that none exists. **The minimum at q = 9 remains in [32, 48].** *(Later: settled at 48, Passes 12518–12519.)* The 48-set is the
best known upper bound, and no proof of optimality is claimed.

## 12510: the 4-anyon braid image is 3^{1+2}:SL(2,3), the one-qutrit Clifford group

`braid_structure.py` analyses the order-648 image G of B₄:

- its largest normal 3-subgroup O₃(G) has **order 27**, is **non-abelian** and has **exponent 3**: the extraspecial Heisenberg group
  3^{1+2}₊;
- Z(O₃) = Z(G) has order 3;
- G/O₃ has SL(2,3)'s element-order profile, 1¹ 2¹ 3⁸ 4⁶ 6⁸;
- G has 4 Sylow 3-subgroups.

So G has the structure **3^{1+2}₊ : SL(2,3)**, the Heisenberg–Weyl group extended by SL(2,3). That is the structure of the
**one-qutrit Clifford group**, and of the one-qutrit SU(2)₄ metaplectic braid image (Cui–Wang). Its quotient by the centre has the
profile of ASL(2,3), the Hessian group: the symmetry group of the Hesse configuration and of the d = 3 Hesse SIC. The other track
realises that SIC from native Clifford data (8f5a8ce87, `analysis/2026-10-31_chiral_tetrahedra_hesse_and_jones.md`).

> **Braiding four SU(2)₄ anyons acts on the two-qutrit geometry W(3,3) through a group with the structure 3^{1+2}:SL(2,3), a central
> extension of the Hesse SIC's symmetry group.** It splits the 216 minimal codewords into 108 + 108. Five anyons reach all of
> PSp(4,3).

The structure is verified (normal series and quotient profiles). A full isomorphism with Cui–Wang's explicit SU(3) matrices is not
built.

## 12511: the B₄ halves are an invariant independent of chirality

On the **432 signed** minimal codewords (a support together with a choice of which 5-line half is "+"):

- the control works: PSp(4,3) gives Pass 173's **two chiral orbits of 216**, and B₅ gives the same split;
- **B₄ gives four orbits of 108**, each lying inside one chiral orbit.

So 4-anyon braiding preserves chirality, as all of PSp(4,3) does. On top of that it splits the supports 108 + 108: two independent
binary invariants, giving 2 × 2 = 4 classes. This settles the open question left by the 12507 correction.

## 12512: every "(obs ± σ)" claim on the site, through the fair null

`site_claims_audit.py` parses every "⟨prediction⟩ (obs: X ± σ" row of `docs/index.html`. Twelve rows are found. Each is judged at
expression cost ≤ 3, because the site's formulas use 2–3 integer leaves:

| verdict | rows |
|---|---|
| **excluded by experiment** | 1: sin²θ_W = 3/13 (16.7σ) |
| **consistent but not evidence** (≥ 30% of random alphabets reach it) | 11: Cabibbo, α_s, the three PMNS angles, Δm² ratio, n_s (twice), m_H, Ω_DM, Ω_b |
| **rare under the null** | **0** |

The site's PMNS note now carries this summary.

## 12513: the golden-gate bridge — what is and is not built

The q = 7 cube matching is the block system of an S₄ acting on the 8 points of PG(1,7). On the Bloch sphere, the octahedral group
(single-qubit Clifford mod phase) acts on the 8 **cube vertices**, which are the Bravyi–Kitaev **T-type magic states**, with the
antipodal pairs as blocks. A reduction map sending those 8 magic states to PG(1,7) and the golden-gate octahedral group to the cube's
stabiliser would make the analogy concrete. It needs Galois descent: √3 ∉ F₇, so the magic-state coordinates live in F₄₉. **The map is
not built; the bridge remains an interpretation [I].**
