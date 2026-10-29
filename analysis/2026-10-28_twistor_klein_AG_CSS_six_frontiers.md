# Six W33 frontiers: an exact finite twistor/Conwell correspondence and Klein-quadric AG/CSS codes

**Research date:** 2026-10-28. **Executable producer:** `analysis/w33_20261028_twistor_klein_ag_codes_round13.py`. **Tests:** `tests/test_w33_20261028_twistor_klein_ag_codes_round13.py`. **Frozen data:** `data/w33_20261028_twistor_klein_ag_codes_round13.json`.

**Scope firewall.** This packet verifies finite projective incidence, characteristic-two coding theory, and algebraic obstructions in a *supplied* native gauge model. It does **not** derive physical Lorentzian spacetime, the Penrose transform, Einstein gravity, the physical helicity of a photon, a quantum-computing threshold, or an experimentally selected field action. The relevant external classical results are long established; any novelty is the explicit **computational connection and certificates within W33-Theory**, not mathematical-priority claims.

## I. The Klein quadric and Penrose's twistor correspondence

The Plücker map sends a 2-plane spanned by `u,v ∈ F⁴` to the six coordinates `p_ab=u_a v_b-u_b v_a`. Its image is the four-dimensional Klein quadric `Gr(2,4) ⊂ P⁵` cut out by

```
p01*p23 - p02*p13 + p03*p12 = 0.
```

Over complex numbers this `Q⁴ ⊂ CP⁵` describes complexified conformally compactified Minkowski spacetime. A spacetime point corresponds to a `CP¹` twistor line in `CP³`; the intersection of two twistor lines corresponds to null separation. A real Lorentzian spacetime is obtained **only after supplying a suitable real structure**, e.g. the SU(2,2) real form, and choosing a patch/scale. The Penrose transform is a distinct sheaf-cohomological construction of massless fields. The anti-self-dual nonlinear-graviton result requires appropriate curvature integrability and holomorphic geometry, none of which follows from the finite field below.

Sources: Adamo–Bullimore–Mason–Skinner, *Twistor theory at fifty* (2017), https://pmc.ncbi.nlm.nih.gov/articles/PMC5666237/ ; twistor-line incidence in https://www.sciencedirect.com/science/article/pii/0370157383900030 ; Salamon, *Twistor Spaces* (real forms, source PDF), https://sites.duke.edu/scshgap/files/2016/08/salamon_final-1.pdf .

Over `F₂`, a projective line in `PG(3,2)` is a 2D binary subspace with exactly three nonzero vectors. There are 35 such lines, and their 35 distinct Plücker points are precisely `Q⁺(5,2) ⊂ PG(5,2)`. Exhaustive checks show: 15 finite twistor points, 35 finite twistor lines, 105 point-line incidences, 7 lines through each point; 315 meeting and 280 disjoint unordered pairs of twistor lines. Meeting is **exactly** the vanishing of the polar bilinear form on their Plücker points. This is a finite incidence analogue of a part of the twistor correspondence, **not** Minkowski spacetime, time ordering, or a physical causal cone.

## II. Reconstruct all eight Conwell heptads *without* a supplied 8-label table

The projective complement has 28 anisotropic bivectors `p` with `Pf(p)=1`. Join two of them if the projective 3-point line `{p,q,p+q}` remains entirely outside the quadric. Equivalently the polar form `B(p,q)=1`.

An exhaustive graph/clique enumeration reconstructs **exactly eight seven-point Conwell heptads**. Any two heptads intersect in exactly one off-quadric point; every off-quadric point lies on exactly two heptads. Assign that point the **unordered pair of heptad identifiers**. All 28 pairs of 8 labels occur once, and each of the 56 exterior projective lines corresponds to the 3 two-element subsets of a unique 3-element label set. This exactly realizes the known combinatorial Grassmannian `G₂(8)=(28₆,56₃)`.

We further lift all 12 elementary generators of `GL(4,2)` to the six Plücker coordinates, induce permutations of the eight heptads, and **generate the full 20,160-element group**. Every induced generator is even; the permutation image is `A₈ ≅ GL(4,2)`. Stabilizing an unordered pair has order 720, matching `Sp(4,2)`. Thus the correspondence is **equivariant**, not an arbitrary posthoc relabeling. The native period reflection reduces modulo two to an eight-heptad permutation of cycle type `2⁴`, fixing four off-quadric bivectors and no heptad; it does **not** realize a physical Lorentz real structure.

Source and priority: Metod Saniga, *The Complement of Binary Klein Quadric as a Combinatorial Grassmannian* (2015), https://www.mdpi.com/2227-7390/3/2/481 .

## III. Thorough algebraic-geometric evaluation-code census

Evaluate binary projective homogeneous polynomials of degrees 1–4 on the 35 on-quadric points and on the 28 off-quadric points. Because `x_i²=x_i` at binary rational points, the degree-`r` homogeneous evaluation space is exactly the span of squarefree monomials of degrees **1 through r** (not just squarefree monomials of degree exactly r). The software computes the evaluation matrices, exact Gaussian ranks over `F₂`, full weight enumerators when the dimension is at most 21, and exact dual weight enumerators for degree two.

| Evaluation set | degree 1 `[n,k,d]` | degree 2 `[n,k,d]` | degree 3 k | degree 4 k |
|---|---|---|---:|---:|
| Klein quadric, 35 points | **[35,6,16]** | **[35,20,6]** | 34 | 35 |
| Nondegenerate complement, 28 points | **[28,6,12]** | **[28,21,4]** | 27 | 28 |

Degree-one binary Grassmann code weight enumerator is **`1+35 y^16+28 y^20`**; the companion complement evaluation code has **`1+28 y^12+35 y^16`**. These fit together coordinatewise into the full projective simplex `[63,6,32]` code, with all 63 nonzero codewords of weight32. This is an exact **weight-enumerator complementarity**, not only the numerical split `35+28=63`.

The exhaustive degree-two enumerations cover all **1,048,576** on-quadric and **2,097,152** off-quadric codewords. The minimum words occur with weights 6 and 4, respectively. The exact duals of the degree-two codes have parameters **`[35,15,7]`** and **`[28,7,12]`** (exhaustive dual enumeration also performed). Over the quadric the 105 projective lines provide 105 weight-three vectors in the dual of the degree-one code; outside the quadric the 56 external lines provide 56 analogues.

Literature: the classical binary `[35,6,16]` Grassmann code and a seven-error decoder are discussed in *Orbit Structure of Grassmannian G₂,m and a Decoder for Grassmann Code C(2,m)*, https://pmc.ncbi.nlm.nih.gov/articles/PMC10101320/ . Higher-degree codes belong to the higher Grassmann/projective-variety evaluation-code program, e.g. *Higher Grassmann codes*, Finite Fields and Their Applications 76 (2021) https://www.sciencedirect.com/science/article/pii/S107157972100099X . These are **codes from the quadric variety**, not Klein-*quartic* curve Goppa codes; the genus-three Klein quartic appears separately in the repository.

**Repo correction:** Older `analysis/w33_BREAKTHROUGH_42_grassmann_ag_codes_substrate.py` and BT43 label the binary `[7,3,4]` code “Hamming.” It is the **simplex code**; its binary dual `[7,4,3]` is the Hamming code. This is an important terminology fix when comparing Grassmann code families.

## IV. A concrete nested CSS path (not yet photonic fault tolerance)

Since `C₁(X) ⊂ C₂(X)` for the degree-one and degree-two evaluation spaces, choose the CSS X-check space `C₂(X)^⊥` and Z-check space `C₁(X)`. Orthogonality is automatic. The resulting quantum stabilizer code has `k=dim C₂ - dim C₁`. The minimum nontrivial Z-logical weight is the minimum of `C₂\C₁`, which is 6 on the quadric and 4 outside; the minimum nontrivial X-logical weight is 3, certified by the 105 or 56 incidence triples in `C₁^⊥\C₂^⊥`. Thus:

```
Q+(5,2) point set:   CSS [[35,14,3]]
28-point complement: CSS [[28,15,3]]
```

These are mathematically valid binary CSS parameters as constructed, **not** verified optical measurement circuits, qutrit CSS codes, thresholds, or experimentally protected memories. They can detect up to two Pauli errors and correct an arbitrary single-qubit Pauli error under ideal syndrome measurements. The classical degree-one codes alone correct up to 7 (`[35,6,16]`) and 5 (`[28,6,12]`) bit errors, respectively; those classical radii must not be confused with the distance-three CSS constructions.

## V. Executing the preceding five frontier investigations: concrete tests and limitations

1. **Smaller positive repair:** the previous six-term global all-Bloch proof remains intact. For a proposed **four-term**, equal-translation architecture using both native added channels along only `e₀,e₁`, the exact unitary character `z=(1,1,ω,ω²)` (`ω³=1`, nontrivial) has `Q=0` and zero translated-difference weight. Hence that architecture **fails**. Numerical searches also found nonidentity exceptional momenta in each of the six coordinate-fixed two-torus sections; no general no-go for arbitrary 2–5 harmonics follows.
2. **Native spectrum:** the certified commutator curl vanishes at `z=1`, while the finite-momentum completed rank is108. By continuity, modes associated with those disappearing rows soften as momentum approaches zero. A **uniform positive massive gap** for that entire acoustic sector is therefore impossible without further dynamics; this is compatible with an intentionally massless Maxwell-like theory. A complete 135×135 finite-momentum dispersion/equal-coupling hardware comparison has **not** been computed in this packet.
3. **Matter-induced selection:** `GL(4,2) ≅ A₈` acts transitively on the 28 nondegenerate bivectors, each with stabilizer `Sp(4,2)` of size720. Accordingly **no single nondegenerate gauge-kernel choice is invariant under that full finite symmetry**. A microscopic action preserving the full symmetry cannot uniquely prefer one without a symmetry-breaking mechanism. The E₆ matter determinant and anomaly-consistent regulator remain open.
4. **Actual coding construction:** the two exact nested CSS codebooks above are a concrete next engineering candidate; full encoded photonic circuits and noise simulation remain unimplemented.
5. **Parity and real structure:** the actual native reflection induces four swaps of the eight Conwell labels, fixing four of the 28 points. But finite characteristic-two incidence does not specify the Lorentzian `SU(2,2)` conjugation/real slice required for Penrose twistor physics; the known integral-period `Z₂` gluing also remains to be propagated into a real spacetime interpretation.

## VI. Independent experimental falsifiers and next choices

- **Equivariance:** implement the exact 28-element heptad-pair map as a canonical coordinate adapter, then verify the native H27/cover symmetry generators, not just abstract `GL(4,2)`.
- **AG/CSS engineering:** generate actual parity-check matrices and a one-error syndrome decoder for both CSS codes; compare circuits under detected photon-loss, phase noise and qutrit-to-qubit conversion overhead.
- **Twistor reality:** explicitly select a complex structure and `SU(2,2)` real form (or demonstrate none compatible with the native discrete symmetries), then check null incidences and conformal scaling rather than assuming finite incidence is spacetime.
- **Sub-six magnetic repairs:** optimize general asymmetric translated Wilson-loop terms under certified all-Bloch rank and acoustic-stiffness inequalities, recording exact algebraic counterexamples to false positives.
- **Dynamical selection:** derive a gauge-invariant E₆ charged-matter response and determine whether its induced interaction respects the 28-point symmetry or selects/breaks one heptad pair.

## Repeatable local commands

```bash
python analysis/w33_20261028_twistor_klein_ag_codes_round13.py \
 data/w33_20261028_twistor_klein_ag_codes_round13.json
python -m pytest -q tests/test_w33_20261028_twistor_klein_ag_codes_round13.py
```

**Validation status:** dedicated local tests `7/7 PASS`; exact classical codeword enumeration and 20,160-element generated group closure executed. Any whole-repo CI result is separate and must not be claimed until verified after the push.