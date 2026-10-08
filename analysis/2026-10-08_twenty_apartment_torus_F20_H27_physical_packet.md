# 2026-10-08 — W33 twenty-apartment torus homotopy, exact F20 Singer normalizer, H27 flux and physical five-front follow-through

**Research status:** five requested independent fronts plus three outside-the-box ideas executed, including exact computer-verifiable group/chain presentations, a complete symplectic point-group stabilizer determination, 729-pair Heisenberg holonomy census, finite precision photonic-noise controls, and explicit negative/inconclusive particle-physics gates. **None** derives the observed Standard Model, the Einstein equations, a normalized Yukawa coupling or a complete TOE.

**Base:** freshest `W33-Theory/master` initially `8c4fb7a1483c8fdc4de5ddbd7a0bd70fe59b931f` (parallel Pass 398 certificate update, not modified). Worked in an isolated clean research branch/worktree, not the user's already-dirty main checkout. Holotrade commits inspected for research awareness, but this packet contains only W33 theoretical mathematics, so **no changes were made to Holotrade**.

## Provenance: what earlier work already proved

- BT744: W33's 80-vertex Levi incidence graph **is** the type-C2 finite Tits building, its 1,620 eight-cycles **are apartments**, with one orbit under (PSp(4,3)), order 25,920, apartment stabilizer 16, and 81 apartments through each chamber forming a Steinberg homology basis. This pass does **not** claim those known theorems new.
- Passes 369–371 and 5105: regular Payne (H_{27}) on the 27 affine exterior points of each chosen W33 point, with 13+27 partition. Pass 11043: trinification/operator H27 center and nontrivial nine-dimensional commutant dressing. The two original 27D representations are not conjugate.
- Prior Oct 8 packet `analysis/2026-10-08_beyond_five_H27_center_atlas_physical.md`: precise ([C_A,C_B]) rank-one-current commutation law, 1,620-vertex degree-324 incompatibility graph, an explicitly selected inclusion-maximal 45-apartment commuting atlas, and **one 20-apartment signed cycle relation**, whose 40-vertex/60-edge/20-octagonal-face CW complex has integral homology (\(\mathbb Z,\mathbb Z^2,\mathbb Z\)). This pass advances *its homotopy, symmetry and finite gauge fields* rather than re-discovering the counts.
- **Pass 2474** `analysis/w33_pass2474_f20_lifted_normalizer_hom.py`: the Sylow-5 normalizer in (PSp(4,3)) is (5{:}4=F_{20}); its preimage in (Sp(4,3)) is **non-split (5{:}8)**, and the central sign obstructs a naive Hom intertwiner. This is pre-existing; the new result identifies the precise *apartment relation stabilizer* with such a Sylow-5 normalizer.
- **Pass 585** already constructs a Singer-image (F_{20}) in a separate (A_8) representation, with the *same element-order spectrum*. This pass does **not** identify the two ambient (A_8) and (PSp(4,3)) actions.
- **Pass 5617** already develops lattice magnetic translations and (Z_3) Harper flux. This pass specializes a **flat vs projectively twisted holonomy census** to the newly constructed W33 apartment CW torus; the general magnetic-translation mechanism is standard and already in the repo.

## I. Fundamental group: presentation reduces *exactly* to the two-torus

Given the previous 20-apartment signed relation, build the **unoriented union CW complex** (X) from its actual Levi vertices, edges and 20 attached octagonal 2-cells. Its underlying connected 1-skeleton has 40 vertices and 60 edges; choose a deterministic 39-edge BFS spanning tree. Its collapse gives a one-vertex presentation with **21 one-cell generators** \(x_1,\ldots,x_{21}\) and **20 face relators**. Each relator is the oriented 8-cycle word with its tree-edge letters removed. The initial cyclically reduced relator length distribution is (1^4,2^1,3^7,4^7,5^1).

Run the previously independently-tested `w33_pass607_johnson_clique_pi1.tietze_eliminate` on the exact relators, **always** eliminating a generator occurring precisely once in one relator, substituting it everywhere. The certificate records all **19 exact elimination/rewrite steps**, a SHA256 of the entire transcript, and the resulting free-reduced presentation

\[
 \boxed{\pi_1(X)=\langle x_{13},x_{19}\mid x_{13}^{-1}x_{19}x_{13}x_{19}^{-1}=1\rangle\cong\mathbf Z^2.}
\]

This is not deduced from abelianization: the surviving relator is an explicit *group commutator*. The earlier independent Smith computations prove \(H_0=\mathbb Z,H_1=\mathbb Z^2,H_2=\mathbb Z\), torsion-free.

**Stronger CW consequence (with scope):** the 19 single-letter generator–relator cancellations are elementary cellular presentation moves: after the usual cellular homotopies/2-cell slides they cancel 1-cell/2-cell pairs. The remaining 1-vertex CW complex has two loops and one commutator 2-cell, the standard torus CW structure. This provides a **simple-homotopy equivalence** \(X\simeq_s T^2\), not a *homeomorphism* \(X\cong T^2\). In (X), 40 edges lie in two faces, 20 edges in *four* faces, so it is a genuine branched nonmanifold despite having torus homotopy type.

This is a stronger theorem than an Euler-characteristic or Betti-number match. It gives natural cohomological cup product and flat-gauge classification on this selected complex. It **does not** demonstrate a Lorentzian manifold, an observed compact extra dimension or an Einstein action.

Certificate: `data/w33_20261008_twenty_apartment_fundamental_group.json`, generator: `analysis/w33_20261008_twenty_apartment_pi1_presentation.py`, source verifier in `tests/test_w33_20261008_pi1_f20_H27_flux_physical.py`.

## II. The twenty-apartment support really has Singer-normalizer symmetry F20

Construct (PSp(4,3)) by symplectic projective transvections on the **actual 40 projective points**, and transport the induced action to the 40 projective lines, then to all 1,620 8-cycle apartments. The enumerated projective group has exact order **25,920**.

- The selected **45-apartment commuting atlas** has trivial setwise stabilizer, hence its orbit contains **25,920** atlases. Thus 45 matching the E6 tritangent-plane count is not an equivariant identification of that specific atlas.
- The **20-apartment relation support** has a setwise stabilizer of exact order **20**, so its orbit contains **1,296** such supports (for the selected support, not a global classification of all possible such supports).
- The support stabilizer's element-order distribution is \(\{1:1,2:5,4:10,5:4\}\\), it is nonabelian, its commutator subgroup is cyclic of order 5 and its abelianization is (C_4). Therefore it is **(C_5\rtimes C_4\cong AGL(1,5)=F_{20})**.
- Crucially, this is more than group-order matching: the code enumerates the full normalizer in **all 25,920** projective group elements of one exact order-five element in that stabilizer. The normalizer has **20** elements and is **identical to the computed setwise support stabilizer**.

The relation support therefore has **exactly the Sylow-5 normalizer** symmetry whose symplectic (5{:}8) lift and central-sign obstacle were studied independently in prior **Pass 2474**. This is an actual comparison, not a numerology claim. The 20 faces form two orbits of ten under this subgroup (a selected face has orbit length 10); the *chosen union support* is invariant even though the oriented 20-cell relation signs need not be fixed in the same way.

**Conditional physics veto:** because \(F_{20}^{\rm ab}=C_4\), it has **no order-3 linear characters**, cannot by itself generate the missing order-three (X_3) charge of the proton-hexality ledger, and has no Klein-four Sylow-two subgroup (its 2-Sylow is (C_4)). A different UV gauge factor or bundle equivariance remains possible. The pre-existing (5{:}8) lift must also be used rather than silently discarding the central sign in matter representations.

Certificate: `data/w33_20261008_apartment_torus_symmetry.json` and complete algorithm `analysis/w33_20261008_apartment_torus_symmetry.py`. External group classification agrees that (F_5=AGL_1(F_5)=C_5\rtimes C_4): https://people.maths.bris.ac.uk/~matyd/GroupNames/AG.html .

## III. A **genuine H27** magnetic-flux bridge from torus homotopy, not from 13=13

Since the presentation reduces to the torus cell complex,

\[
H^1\(X;\mathbf F_3\)\cong\mathbf F_3^2,
\quad H^2\(X;\mathbf F_3\)\cong\mathbf F_3,
\quad (a,b)\smile(d,e)=(ae-bd)[X]^*.
\]

Thus the ordinary mod-3 **cup-product pairing is the rank-two alternating symplectic form**, exactly the data used to define the standard order-27 Heisenberg extension (a chosen orientation/sign/basis remains noncanonical). This gives a rigorous route from this **specific selected W33 torus CW complex** to the *abstract* (H_{27}) group—the latter's realization as W33's separate regular/Payne group was already established and the abstract equivalence was explicitly constructed in the prior packet.

One might be tempted to call every pair of H27 shifts a flat toroidal gauge field. That is **false**: (\pi_1(X)=\mathbf Z^2) is abelian, hence actual flat H27 holonomies must commute. Enumerating all (27^2=729) ordered pairs of group elements with exact matrices gives

\[
[U(a,b,c),U(d,e,f)]=U(0,0,2(ae-bd)),
\]

with the *discrete central curvature* distribution:

| Central phase (mod 3) | Ordered H27 pairs |
|---|---:|
| 0: commuting, admissible as flat holonomy | **297** |
| 1: projective/magnetic nonzero phase | **216** |
| 2: conjugate projective/magnetic phase | **216** |
| **Total** | **729** |

Under simultaneous conjugation, 297 commuting pairs reduce to **105 flat H27 gauge-equivalence classes**, comprising 9 orbits of size 1 and 96 orbits of size 3. For the abelian (Z_3) gauge group there are **9 flat torus characters**, of which 8 are nontrivial.

The determinant pairing can instead be read as the central multiplier of *projective* or magnetically twisted lattice translations. That is a meaningful mathematics-to-physics **kinematic** link; a nonzero multiplier is not an ordinary flat (H_{27}) representation of the torus fundamental group, and no microscopic gauge curvature, physical magnetic flux or spectrum has been derived. The project's existing Pass 5617 separately treats Harper-like (Z_3) magnetic translations; this pass adds the new selected CW complex and exhaustive commuting/twisted-holonomy census.

Certificate: `data/w33_20261008_torus_H27_flat_flux.json`. Implementation: `analysis/w33_20261008_torus_H27_flat_flux.py`. Background magnetic translations: https://arxiv.org/abs/0812.1426 .

## IV. Photonic single-source discrimination with transparent noise envelopes

The prior packet compiled two explicit 27-mode graph Hamiltonians as nine pairwise-disjoint coupler layers, found a fully port-label-invariant binary classifier based on sorted 27-bin output distributions, and certified an ideal-model 95% Hoeffding sufficient sample count. That classification question is **binary model testing**, not 1,404-outcome full tomography, and the simulation assumes nominal ideal transfer matrices.

This pass propagates two *declared* noise allowances: (a) a known **uniform dark-count/conditional background fraction** \\(\beta\\), which scales the separation \(\delta\to\(1-\beta\)\delta\), and (b) an arbitrary bounded \\(\ell_\infty\\) conditional-probability calibration mismatch \\(\epsilon\\) **per candidate distribution**, yielding a conservative cross-hypothesis separating margin (\delta_{\rm robust}\ge\(1-\beta\)\delta-2\epsilon\). Given that positive margin and independent successful detections, a Hoeffding sufficient condition is

\[
n\ge\left\lceil\frac{8\log\(2\cdot27/0.05\)}
 {(\(1-\beta\)\delta-2\epsilon)^2}\right\rceil .
\]

**At 99% survival per interaction layer**, among the tested 36/72/144-stage circuits:

| Uniform conditional background β | Max per-outcome mismatch ε | Selected depth | Conditional expected launches |
|---:|---:|---:|---:|
| 0 | 0 | 72 | 2,217 |
| 5% | 0.01 | 72 | 2,982 |
| 10% | 0.02 | 72 | 4,223 |
| 20% | 0.05 | 72 | 16,972 |

The word **expected** matters: these launches are \(\lceil n/0.99^d\rceil\), not a 95% guarantee on the random successful-detection count. Coupler fabrication, correlated coherent errors, wavelength drift, port-dependent loss, actual detector dark-count models and joint nuisance-parameter estimation have **not** been calibrated. The margins are a sufficient *model-specific* bound. Related experimental quantum-walk work reports a fabricated silicon photonic device implementing tunable walks on five-vertex graphs, not our 27-port chip: https://pmc.ncbi.nlm.nih.gov/articles/PMC7909884/ .

Generator: `analysis/w33_20261008_photon_robust_decision_guards.py`. Certificate: `data/w33_20261008_photon_robust_decision_guards.json`.

## V. String flavor/Yukawa feasibility: another exact *negative / inconclusive* certificate

We did **not** silently equate the earlier integral holomorphic residue Yukawa with a canonically normalized physical coupling. The source tetraquadric candidate is a specific Klein-four-invariant section of O(2,2,2,2), with 21 orbit-basis coefficients and exact proof of avoiding the 48 ambient fixed points over C. The previous packet's finite-field reductions at (p=3,5,7,11,13) each had singular rational points; those are *bad reductions* and logically say nothing decisive about whether the characteristic-zero fiber is smooth.

This pass also exhaustively searched **20,736 bounded rational projective ambient points** obtained from 12 explicitly listed rational points of each factor (\mathbf P^1\(\mathbf Q\)\). Exactly **246** lie on this polynomial; **none** is a rational singular point within the finite sample. This is an **inconclusive finite-height search**, not a proof of smoothness (nor of singularity) over the algebraic closure of Q/C. A full characteristic-zero saturated Jacobian-ideal computation or a certified good reduction in *every* affine chart remains necessary before claiming a smooth explicit hypersurface.

For a physical mass, actual complex-structure/Kähler moduli, line bundle cohomology representatives, Calabi–Yau Ricci-flat and bundle HYM metrics, harmonic forms, kinetic normalization and flux/FI stabilization are still needed. A January 2025 numerical heterotic paper computes normalized Yukawas with neural metrics and explicitly discusses normalization effects: https://doi.org/10.1016/j.nuclphysb.2024.116778 . Relevant public code: https://github.com/kitft/heteroticyukawas . A January 2026 paper extends HYM calculations to free quotient bundles: https://doi.org/10.1016/j.nuclphysb.2025.117253 . These are methodological references, not computed results of our W33 model.

Generator: `analysis/w33_20261008_tetraquadric_exact_singular_sieve.py`. Certificate: `data/w33_20261008_tetraquadric_exact_singular_sieve.json`.

## Scientific firewall and next decisions

The selected complex (X) is **simple-homotopy equivalent but not homeomorphic** to (T^2); its 20-apartment setwise stabilizer is the **actual (PSp(4,3)) Sylow-5 normalizer**, and its mod-3 cup product supports exactly the alternating rank-two data giving (H_{27}). This is a coherent chain of **mathematical** constructions across three old subprograms (BT744 buildings, Pass2474 Singer normalizers and Pass5617 magnetic flux). The causal physics link still needs an action, source matter coupling, a controlled continuum limit, anomaly cancellation and experimentally discriminating observables. The local C8 Jacobi Lie algebra \(\mathfrak{sp}_6\ltimes\mathfrak h_{13}\) does not automatically glue into an Einstein constraint algebra merely because selected local centers commute.

The selected 20-cycle support's orbit size **1,296** and the H27 flux noncommuting-pair count **432** are independently exact; no equivalence of these two sets is proposed from their divisibility relations. The equality of the 45-cycle atlas count with E6 tritangents likewise remains unsupported by equivariance (indeed its stabilizer is trivial).

**Reproducibility:** scripts under `analysis/w33_20261008_*.py`; JSON certificates under `data/w33_20261008_*.json`; focused tests under `tests/test_w33_20261008_pi1_f20_H27_flux_physical.py`. Source-preserving prior-repo comparisons are embedded in each certificate and above. General presentation background: https://gap-system.github.io/gap/doc/ref/chap48.html .

### Top five independent nonsequential next steps

1. **Classify the 1,296-member torus-support orbit under the full (PSp(4,3))**: compare the selected octagonal CW complexes, their 5:4 normalizers, and potential cover/quotient maps to the Császár–Szilassi polyhedra. Verify any claimed equivariant map directly.
2. **Construct a physical gauge/curvature action on the W33 apartment torus and test the Einstein/ADM closure**: account for noncommuting local currents, discrete torsion and central magnetic flux. Do not treat topological homology as a gravitational field equation.
3. **Build a calibrated 27-port optical unitary plus detector error model**, including port-dependent loss, adversarial coherent coupler errors and a 95%-guaranteed *launch* budget, then compare information-optimal circuits at 36/72/144 stages.
4. **Find an actual (Z_6) symmetry remnant in the heterotic compactification**, including its missing order-three generator independently of the new F20 stabilizer (which cannot carry it), heavy exotics and all anomaly/instantonic selection rules.
5. **Give one certified smooth explicit tetraquadric and a normalized physical Yukawa** via exact Jacobian saturation, cohomology and numerical Ricci-flat/HYM/harmonic integration, distinguishing UV model and experimental comparison.
