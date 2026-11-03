# 2026-11-02 — Eight fronts: W33 photonics, q=7 cubic tomography, and continuum falsifiers

**Research boundary:** Finite exact algebra and idealized reproducible models only. No physical TOE, Standard Model derivation, gravity model or completed photonic experiment is claimed.

**Ownership:** Earlier November 2 research owns the 216-route frame, 24D projector and 216-outcome POVM. Pass 12526 owns the full 36-by-6 simplex partition; parallel Passes 12518–12525 own the q=7 hyperoval seeds and original q=7 orbit claim. Pass 982 and October 29 optical code own the q=3 half-revival. The present work independently tests new mathematics and physical realizability constraints, with attribution.

## Front 1 — Noisy optical compiler

Reproducer: analysis/w33_20261102_eightfront_partB.py. The frozen 4,884-rotation adjacent-mode compiler maps 24 coherent input amplitudes to 216 detector outputs. Three seeded trials per scenario; for each trial all 216 prepared frame states were checked against their ideal full detection histograms. Per-active-element attenuation, independent rotation/phase errors, unitary two-rail crosstalk, uniform detector efficiency 0.85, and a per-detector dark-click approximation are modeled.

| Mode | Element transmission | Mean single-photon survival | Mean normalized-click total variation |
|---|---:|---:|---:|
| Ideal | 1 | 1.00000 | 0 |
| Loss | 0.999 | 0.88866 | 0.02612 |
| 0.001-rad calibration | 0.999 | 0.88867 | 0.02728 |
| Added 0.0004-rad crosstalk | 0.999 | 0.88868 | 0.02735 |
| Severe loss/crosstalk | 0.995 | 0.57567 | 0.12959 |

These assumed parameters are **not measured device data**. Normalized expected clicks are an approximation to heralded detection, not a threshold-detector multi-click distribution. Balanced Clements meshes are a relevant low-depth comparison: https://doi.org/10.1364/OPTICA.3.001460.

## Front 2 — Exhaustive q=7 cubic reconstruction

Reproducers: analysis/w33_20261102_q7_exhaustive_triple_moments.py and analysis/w33_20261102_q7_full_cubic_tensor_types.py. The BFS closes the explicit 40-line seed under eight symplectic transvections to all **720,300** distinct supports, matching the independent parallel-track orbit size. Every support twice covers 160 points. Set x_i=5h_i-2, so x_i is either 3 or -2 and the coordinate sum vanishes.

PSp(4,7) acts on unordered distinct triples in five types: three points on one isotropic line; exactly two orthogonal pairs; exactly one orthogonal pair; zero orthogonal pairs but projectively dependent on a nonisotropic line; and zero orthogonal pairs with projectively independent span. Their counts respectively are 22,400; 548,800; 3,292,800; 137,200; 6,585,600; total 10,586,800. The group-transitivity argument uses projective scalar normalizations and symplectic Witt extension. For an independent triple with all pairings nonzero, the only square-class ambiguity is removed by swapping two unordered labels, as minus one is nonsquare in GF(7).

The normalized orbit-averaged cubic coefficients for those five types are 93/28, -117/343, 57/1372, -142/343, 1/196. The global zero-sum identity independently forces the weighted sum of all distinct-triple moments to equal 800. Repeated-index entries are 6 (all equal), 9/14 (two equal and the other adjacent), or -6/49 (two equal and the other nonadjacent). Hence these five values specify every entry of the entire symmetric 400-cubed tensor, without storing 64 million entries. **For distinct a,b,c, the value 93/28 singles out an isotropic line triple** and reconstructs all lines exactly. The earlier exploratory zero-edge triple (0,8,9) was PROJECTIVELY DEPENDENT and is correctly grouped as a nonisotropic-line triple, not generic independent.

## Front 3 — Absolute irreducibility of the 15D blind sector

Exact group enumeration verifies |PSp(4,3)|=25,920, orbit size 216, stabilizer 120 and stabilizer pair-orbital rank 10. This prevents incorrectly inferring full multiplicity-freeness from six squared-Gram eigenvalues.

Exact modular certificates (analysis/w33_20261102_exact_blind_irreducibility.py): both primes 101 and 103 give 15-dimensional K-kernel and rank **224** for the 225-variable stacked commutant system of eight generating transvections. Only scalar commutants survive. The primes do not divide the group order, and the kernel rank agrees with the characteristic-zero CRT certificate. By semisimplicity and Schur's lemma, the 15D blind outcome module is absolutely irreducible. This does NOT repair the POVM's informational incompleteness: the span rank remains 201 versus 300 real symmetric or 576 complex Hermitian dimensions.

## Front 4 — Correct-trace-form no-go for a natural 27D Jordan deformation

An explicit reducible 27D cubic Jordan control norm is N0(a,b,c,x)=a(bc-||x||²) for x in the 24D route carrier. At basepoint (1,1,1,0) its canonical trace form is diag(1,1,1,2I24); the sharp map (bc-||x||²,ac,ab,-ax) satisfies the adjoint identity exactly.

For Nlambda=N0+lambda*Croute(x) with the **same** trace form and basepoint, the vector part of the sharp map becomes -ax+(3lambda/2)Z-transpose(Zx)². Set a=b=c=0 and choose x with nonzero gradient. The twice-sharp scalar component is -(9lambda²/4)||Z-transpose(Zx)²||², whereas Nlambda(y)*a=0. Thus all nonzero lambda are excluded in this family, using the proper nondegenerate trace form, not merely the naive Euclidean gradient. Other 27D Jordan forms, particularly exceptional simple Albert structures, remain open. Standard cubic norm axioms: Kevin McCrimmon, A Taste of Jordan Algebras.

## Front 5 — Connected voltage covers with vanishing gap

A single W33 oriented edge gets cyclic voltage +1 modulo m (reverse -1), all other edges zero. The m-fold covers are connected, 12-regular, 40m vertices, and each has the same local neighborhoods. The analytic Rayleigh bound for the normalized Laplacian is lambda_2 <= [2-2cos(2pi/m)]/480, giving O(m^-2). Shift-invert eigenvalue checks:

| Cover layers | Vertices | Numeric gap | Exact upper-bound value |
|---|---:|---:|---:|
| 3 | 120 | 0.00530547 | 0.00625000 |
| 5 | 200 | 0.00242614 | 0.00287910 |
| 9 | 360 | 0.000818103 | 0.000974815 |
| 15 | 600 | 0.000301921 | 0.000360227 |

This is an **artificial bottleneck cover**, not a local isotropic three-dimensional or Lorentzian continuum. It supplies a constructive counterexample to the bare W33 graph's persistent-gap obstruction, not a physical solution.

## Creative front 6 — Detector symmetry twirling

Use symplectic automorphisms to **physically** reassign nominal route outcomes to output ports and average away fixed per-detector gain errors. A seeded illustrative gain distribution with standard deviation 0.07415 falls to 0.00268 after 750 random-walk group assignments (maximum residual 0.00848). Requires reconfigurable hardware switching; software label permutation alone does NOT reduce detector bias.

## Creative front 7 — Two-stage 36-by-6 POVM instrument

Pass 12526's prior 36 regular five-simplexes partition the 216 routes. Independently checked one six-member block [0,26,102,147,173,208], integer sign Gram 48I6-8J6. If P_g denotes the rank-5 projector for a block, its six existing POVM effects sum to G_g=(2/15)P_g. Conditional six-outcome effects on the same five-space are F_s|g=(5/6)|u_s><u_s|. With a first-stage Lüders instrument for G_g, the composite effect sqrt(G_g) F_s|g sqrt(G_g) equals the original E_s=(1/9)|u_s><u_s| exactly. This is a mathematically valid two-stage **instrument blueprint**, not yet a fabricated or optimized 36-port receiver.

## Creative front 8 — Static-disorder quantum echo

A toy 40-mode adjacency Hamiltonian H=JA revives perfectly at pi/J (this half-revival mechanism was previously known in Pass 982). We tested independently seeded static Gaussian on-site diagonal disorder. Twelve trials per setting give mean process/entanglement fidelity |Tr(U(pi/J))/40|²:

| Onsite disorder sigma/J | Mean fidelity |
|---|---:|
| 0 | 1 |
| 0.01 | 0.999495 |
| 0.05 | 0.986772 |
| 0.10 | 0.954869 |

These are chosen toy couplings, not photon physics constants.

## Reproducibility

Scripts: analysis/w33_20261102_eightfront_partA.py; analysis/w33_20261102_eightfront_partB.py; analysis/w33_20261102_q7_exhaustive_triple_moments.py; analysis/w33_20261102_q7_full_cubic_tensor_types.py; analysis/w33_20261102_216_stabilizer_orbitals.py; analysis/w33_20261102_blind_commutant_probe.py; analysis/w33_20261102_exact_blind_irreducibility.py. Frozen outputs are data/w33_20261102_eightfront_partA.json, eightfront_partB.json, q7_exhaustive_triple_moments.json, q7_full_cubic_tensor_types.json, 216_stabilizer_orbitals.json, blind_commutant_probe.json, and exact_blind_irreducibility.json. The q7 exhaustive orbit enumerator takes about two minutes on the tested Windows machine; other programs finish in seconds.

## Next five independent research directions

1. Compile a lower-depth balanced or sequential 36-by-6 optical receiver, with actual threshold detector and heralding statistics.
2. Find the complete irreducible decomposition and centralizer algebra of the 216D permutation module, including both 15D spectral pieces.
3. Extend the cubic-orbit classification and full-line tomography to GF(9), testing characteristic-three special behavior and extra square classes.
4. Search the moduli of nondegenerate 27D cubic trace forms and genuine simple Albert embeddings, not the reducible control.
5. Build multi-directional, growing-diameter covers and test spectral dimension, causal propagation and emergent Lorentz invariance against local lattice field theory.
