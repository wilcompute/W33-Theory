# W33 research: Conwell K8 photon-loss decoder, finite Radon, gauge optimization, A8 selection and ternary code correction

**Date:** 2026-10-29 UTC. **Independent local implementation:** `w33_20261029_conwell_graph_radon_loss_front14.py`; eight targeted tests in `test_w33_20261029_conwell_graph_radon_loss_front14.py` (all passed), exact JSON output `w33_20261029_conwell_graph_radon_loss_front14.json`.

The code builds on the repo's existing Conwell-heptad construction, 28-point CSS checks and native finite-period magnetic symbol. It **does not** demonstrate an implemented photonic quantum computer, a genuine holomorphic Penrose transform, the full 135-link dispersion, an interacting E6 determinant, a quantum threshold or a TOE.

## 1. Complete Conwell graph and heralded-erasure decoder

Identify the 28 nondecomposable binary Plücker vectors with the edges of K8 using their pairs of Conwell heptads. There exist eight vectors v_i in F2^6 (one can choose v_0=0) such that for all edges p_(ij)=v_i+v_j. The v_i span rank six and sum to zero. Thus the six-bit syndrome of an edge set is the degree-parity boundary in the even-weight subspace of F2^8, modulo the all-ones vector. It vanishes precisely when every K8 vertex has even degree or every K8 vertex has odd degree.

The 28-qubit CSS code has ideal syndrome checks of ranks 7 (X) and 6 (Z). A single X error at coordinate p produces syndrome p; a single Z error produces the seven-bit syndrome (p,1). The 378 pairs of X errors split into 168 whose syndrome aliases a single-X error (one of 56 exterior-line triangles completed in three ways) and 210 whose syndrome lies on the binary Klein quadric and is outside the single-error lookup.

For ideal **heralded** photon loss, a subset of at most six lost qubits is correctable precisely when its six-bit columns are linearly independent. Any seven columns depend, and any such dependency supports a nontrivial logical X operator of weight <=7, below the minimal X stabilizer weight 12; thus no seven-or-more erasure subset is correctable.

| Lost k | Correctable subsets | Total subsets |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 28 | 28 |
| 2 | 378 | 378 |
| 3 | 3220 | 3276 |
| 4 | 18760 | 20475 |
| 5 | 73248 | 98280 |
| 6 | 155456 | 376740 |

The 56 dependent triples are K8 triangles. The 315 **minimal** zero-syndrome four-edge supports are 210 K8 four-cycles and 105 perfect matchings. All 1715 uncorrectable four-erasure sets are explained by these 315 circuits and the 56 triangles, each with 25 choices of an extra edge.

For independent heralded loss eta, the **exact ideal-erasure success probability** is

P_success(eta) = sum_{k=0}^6 I_k eta^k (1-eta)^{28-k},

where I=[1,28,378,3220,18760,73248,155456]. This gives 99.994079% at eta=0.01, 99.104138% at eta=0.05, and 92.041603% at eta=0.10. No heralding inefficiency, ancilla loss, correlated error, measurement circuit noise or hardware overhead is included.

## 2. A finite Radon analogue, not Penrose's holomorphic transform

The 15 nonzero F2^4 vectors are the points of PG(3,2), with 35 projective lines {u,v,u+v}. The incidence X-ray transform sends 15 functions to 35 line sums (Tf)(u,v)=f(u)+f(v)+f(u+v). Exact GF2 rank is 11, kernel dimension 4, cokernel dimension 24. The kernel consists exactly of the four-dimensional vector space of restrictions of linear maps f(u)=a·u, the Cauchy additive solutions. The incidence is equivariant under all 12 tested elementary GL4(2) generators.

This provides a reproducible finite projective-incidence transform. **It is not the Penrose transform**: the complex analytic sheaf cohomology, real SU(2,2) structure, helicity and massless-field PDE are missing. Literature: https://encyclopediaofmath.org/wiki/Penrose_transform and https://www.cambridge.org/core/books/abs/twistors-in-mathematics-and-physics/penrose-transform/797A015C7991A87C887DAE0614A195D6 .

## 3. Three-term gauge repair decisively falsified off the torsion grids

The earlier six-term positive compact repair remains a proven all-unitary-Bloch-kernel construction. A seemingly simpler three-term proposal activates original commutator channel 0 along translations e0,e2 and original channel 5 along e0. It passes several small finite torsion grids, but **fails** at the exact unitary character

z=(1,(-17-4i sqrt(21))/25,1,(-2+i sqrt(21))/5).

At this character the earlier global exceptional polynomial Q(z^W-1) vanishes, while z0=z2=1, so all three correction terms have zero Bloch stiffness. This is not a numerical near-zero. On the inactive two-torus z0=z2=1, with x=z1 and y=z3, the exceptional equation (after clearing denominators) is 5x^2-6xy-4x+6y^2-6y+5=0. Combining with its unit-circle reciprocal conjugate gives resultant 180(y-1)^6(5y^2+4y+5), whose two nonidentity unit roots give the conjugate counterexamples. No full lower bound against all two-to-five-term positive repairs is proved.

## 4. Reduced dispersion control, not full 135-link diagonalization

The local numerical producer also evaluates the **reduced four-period magnetic generalized eigenproblem** using M, W and H(-2)=R^T K R from the repo. At the known order-three exceptional momentum and coefficient epsilon=0.001, the repaired nongauge eigenvalue is approximately 0.0009542255 for six added cosines and 0.0028615788 for twelve added cosines; it is zero without repair. The remaining exact gauge-null eigenvalue is retained. This finite reduced-mode comparison **does not** compute the full 135-by-135 link operator or establish physical photon dispersion; loss/crosstalk comparisons require actual optical parameters.

## 5. The exact A8 matter-selection obstruction

The 28 pair labels are the edges of K8. Two edges share one heptad iff they are adjacent in the triangular graph T(8), a strongly regular graph with parameters (28,12,6,4). Its adjacency A satisfies A^2=8I+2A+4J and has eigenvalues 12 (multiplicity 1), 4 (7), -2 (20). The A8 action has only three ordered-pair orbitals, so any A8-invariant symmetric quadratic form on this 28-label permutation representation has the form aI+bA+cJ, with sectors a+12b+28c (1), a+4b (7), and a-2b (20). It cannot uniquely select one of the 28 labels without additional symmetry-breaking data. This is a representation constraint, **not** the result of integrating out the physical E6 charged matter.

## 6. Important correction to a legacy W33 Grassmann-code assertion

The legacy analysis/w33_pass153_grassmann_codes.py asserts [40,5,28] over F3 for the symplectic Lagrangian Grassmann code and claims it exceeds a Plotkin bound. I reconstructed all 130 projective 2-planes in F3^4, selected the 40 symplectic-isotropic planes, formed their 6x40 Plücker evaluation matrix of rank five, and enumerated all 3^5=243 codewords. The exact weight enumerator is

1 + 90 y^24 + 80 y^27 + 72 y^30,

so the code is **[40,5,24]_3**. The claim of minimum distance 28 and the associated Plotkin statement are false for the described construction. The 40 isotropic planes correspond to **lines**, not points, in W(3,3).

## Validation and five independent next directions

The local full producer passed **8/8 dedicated tests**; its JSON records an exhaustive 0–6 erasure census, ideal Pauli one-error syndrome checks, exact finite Radon kernel, 28x28 adjacency identities, exact algebraic gauge counterexample, three reduced-symbol dispersion samples, and the full ternary weight census. The code is a finite mathematical prototype; broader GitHub CI is a separate check.

Five independent next steps: (1) compile the K8 heptad decoder into an actual lossy photonic syndrome circuit; (2) explore a finite sheaf/cohomology realization rather than calling the incidence map the Penrose transform; (3) classify smaller positive native gauge repairs by exact Laurent algebra; (4) diagonalize the full 135-link Bloch Hamiltonian with normalized couplings and experimental control budgets; (5) derive an A8-breaking or preserving selector from one explicit anomaly-consistent E6 matter vacuum and measure a parameter-constrained observable.