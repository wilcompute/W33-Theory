# 2026-11-03 — Eight verified frontiers: q9 Lean ledger, GAP route characters, quantized photonic tomography, W33 invariant-cubic basis, 3D Wilson walk, q13 design and Fisher falsifier

## Audit and provenance

This continuation began at HEAD `dd85b447a319` of `wilcompute/W33-Theory`, with an unclean but completely preserved local worktree. The immediately preceding commits `9e0d5097d` and `df1e1402c` supplied the q9 cubic point-orbit table, 216-route POVM, native 3-voltage W33 Bloch cell, clock Albert algebra and deck physics. Parallel `dd85b447a` already owns the **160-line W(3,13) even set**, its frame orbit, 0/2/4 incidence histogram and the new Burkhardt quartic dictionary; our q13 **eigenspace test** uses that seed but is independently reconstructed. Earlier `w33_pass10949/10950` owns exact compact Albert algebra, and Pass11491 owns a *different* qutrit-state Molien computation. Nothing below derives observed particles, constants, a physical vacuum or gravity.

External work was consulted before these experiments: finite symplectic orbit methods/Witt's lemma and [PSp4(3) subgroup lattice](https://leemans.dimitri.web.ulb.be/atlaslat/psu42.pdf); [photonic self-configuring MPLC (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12770535/), [synthetic-dimensional photonic Dirac points (2026)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13524054/); [fermion doubling in Dirac walks (PRA 114,012208, 2026)](https://doi.org/10.1103/kkz3-fthm), [Wilson circuit realization (2023)](https://www.nature.com/articles/s42005-023-01326-6), and [Albert Jordan identities (Garibaldi et al., 2024)](https://doi.org/10.1017/9781009426862.006). No external paper establishes these particular W33 constructions.

## Front 1 — A real Lean kernel certificate, with a strict proof boundary

`lean/W33Q9CubicClassArithmetic.lean` compiles using Lean 4.32.0-rc1, no `sorry`. It kernel-checks the seven q9 triple class counts adding to 91,558,740, the binomial value, the rational cubic checksum after exact multiplication by the common denominator 2430, distinctness of the isotropic-line coefficient, and the group-order arithmetic. The original exhaustive q9 point-triple enumeration is in `analysis/w33_20261103_q9_seed_cubic_orbit_types.py` (previous commit).

**Important boundary:** This Lean file does NOT yet formalize the finite-field symplectic form, construction of the seven orbits, Witt extension, or the equality of the seven class averages to the full hyperoval-orbit tensor. Those geometric inputs still rely on the independently checked Python arithmetic and mathematical argument. This is a formally verified **arithmetic slice**, not a fully formalized line-reconstruction theorem. Compiling took substantial Windows tool startup time and succeeded with exit code zero.

## Front 2 — Finite phase resolution and shot budget for an IC 216-port detector

`analysis/w33_20261103_phase_bitdepth_condition.py` loads the exact 216-route sign frame and the orthonormal 24D positive eigenspace from previous scripts. It builds 3 independent settings by putting only diagonal phase shifts in front of the same 216-port Naimark receiver; it computes the full 648×576 real Hermitian effect-span Gram (not merely state-vector rank).

| Phase bits | Random masks tested | Best rank | Smallest eigenvalue | Frame condition when complete |
|---:|---:|---:|---:|---:|
| 2 | 5 | 515 | ~0 | incomplete |
| 3 | 5 | 565 | ~0 | incomplete |
| 4 | 5 | 574 | ~0 | incomplete |
| 6 | 2 | **576** | 1.9906852e-6 | 409.20 |
| 10 | 2 | **576** | 1.9639269e-6 | 411.98 |
| arbitrary phases | 2 | **576** | 3.4384346e-6 | 311.36 |

Seeded samples are not impossibility proofs for all 2–4 bit masks. The sampling shows why **full rank does not mean a well-conditioned measurement**.

A separate analytical program `analysis/w33_20261103_phase_fisher_shot_budget.py` evaluates the local Fisher matrix at `rho=I24/24`, where all 216 probabilities in each setting equal `1/216`. For N *detected photons per setting*, `F=216N AᵀA` on the traceless Hermitian parameter space. The CRB for the weakest direction of the sampled 6-bit design is `sd≥0.048225` at one million detected photons/setting and requires at least **23,256,463 detected photons per setting** for `sd≤0.01` to be compatible with the lower bound. This is a **necessary** condition for locally unbiased estimators, not a sufficient sample guarantee; loss, dark counts, calibration, and physical phase shifters are absent.

## Front 3 — Exact full 216 permutation character via GAP, not just matrix eigenspaces

Producer `analysis/w33_20261103_gap_216_irreducibles.g`, GAP 4.16, invoked through the repo's `scripts/run_gap.sh` Cygwin wrapper. Two nonconjugate S5 maximal subgroups of an S6 maximal give DIFFERENT index-216 coset actions:

- Other S5: complex irrep degree multiset `1,6,15,20,20,30,60,64`.
- **W33 route S5: `1,15,15,20,24,30,30,81`.**

The 216-route sign frame supplies an intertwining map onto the 24-dimensional positive point eigenspace. Exactly one of the two S5 coset characters contains a degree-24 constituent, so this selects the **second class unambiguously**. Character scalar products and multiplicities are exact in GAP; the complex commutant dimension is `1+4+1+1+1+1=10`, matching the earlier exact rank-ten orbital algebra. Independent November 3 numeric orbital work had found the same `80=20+60` and equivalent two 15s; a nonzero skew-equivariant complex structure on 60 supports the distinct conjugate 30s. Original GAP text, parser and frozen JSON retain both S5 controls.

## Front 4 — Explicit TWO-dimensional cubic-invariant basis for the W33 24-carrier

`analysis/w33_20261103_w33_24_molien_cubic.py` enumerates ALL 25,920 group permutations. For each g, the character of the positive 24D point module is computed *exactly* as

`chi24(g) = (sum_i A[i,g(i)] + 4 fix(g) - 16)/6.`

Symmetric-power character formulas give invariant multiplicities **Sym²=1, Sym³=2, Sym⁴=6**. On the positive eigenspace `V24`, the two cubics `C_point(x)=sum_i x_i³` and `C_route(x)=sum_s (Z_s.x)³` are both PSp4(3)-invariant. A pair of integer 24D vectors yields determinant **45,889,208,640,000** for their cubic evaluations. Thus these two forms are linearly independent and, since the invariant cubic space has dimension 2, **are an explicit exact basis**.

This supplies a constrained two-parameter family `a*C_point+b*C_route` for any putative PSp-invariant restriction of an Albert cubic norm. It is *not* a Jordan-algebra embedding, and the previous fixed-frame obstruction remains valid. A genuine embedding must respect the trace form and cubic adjoint/product identities and can require moving/symmetry-breaking frames.

## Front 5 — Native 40-cell + four-spinor Wilson–Dirac falsifier

`analysis/w33_20261103_wilson_dirac_3deck_control.py` uses the same three voltage edges `(0,1),(2,3),(4,7)` and a 40×40 W33 normalized graph Laplacian `L(k)`. On its 160-dimensional product with a supplied four-component spinor,

`H(k) = 0.1 L(k) ⊗ I4 + I40 ⊗ [sum_i sin(k_i) alpha_i + 1.5 sum_i(1-cos k_i) beta]`.

The alpha and beta gamma-matrix anticommutation identities are verified. A massless Dirac-only control has all eight Brillouin-corner zeros; without the Wilson mass, the native W33 graph shifts the seven high-corner states slightly but leaves them low in energy (minimum absolute energy 0.00071–0.00214). The **supplied Wilson mass** lifts all seven high-corner minima to at least **2.8569**, while the physical k=0 branch remains gapless. At `|k|=0.03`, the positive slope ratio is 1.000183. The Wilson mass breaks chiral conservation (nonzero commutator with gamma5), exactly the tradeoff stressed by established lattice-fermion theory. This is a standard engineered control, **not emergent W33-only relativistic dynamics** or a Standard Model chirality mechanism.

## Three independently motivated creative follow-ons actually executed

### A. A non-hyperoval can be a pure positive-module design

Prior parallel Pass12527 owns the q13 160-line frame orbit. Our new `analysis/w33_20261103_q13_positive_frame.py` maps that orbit independently into W(3,13) and verifies point incidence histogram `0:1340,2:960,4:80`. Centered integer vector `y=17*coverage-16` obeys **exactly `A y = 12 y`** at all 2380 points (verified through incidence sum `N Nᵀ y = 26 y`, without creating dense adjacency). Its norm² is 870400 and the negative `-14` module energy is exactly zero. Therefore the full symplectic orbit of this y is a tight frame in the 1274-dimensional positive representation by rank-three symmetry. This generalizes the earlier design framework beyond 0/2 hyperovals. It does not imply 160 is optimal.

### B. Explicit invariant-cubic basis rather than another guessed 27D product

The Molien computation proves there are precisely two invariant cubics, and the determinant witness constructs a basis. This means an Albert compatibility search can parameterize ALL symmetry-preserving carrier cubics by two coefficients, allowing a symbolic adjoint identity elimination test rather than trial-and-error dimension matching.

### C. Hardware feasibility constrained by Cramér–Rao, not just matrix rank

The six-bit mask result is informationally complete numerically but has poor inversion conditioning. The Fisher lower bound gives more than **23 million detected photons per setting** for 0.01 standard deviation in the weakest traceless direction at the maximally mixed state. Real detectors would require additional resources. This is a meaningful falsification target for a single-photon implementation.

## Unresolved physical and mathematical tasks

1. Formalize the actual q9 GF9 orbit classification, Witt transitivity and cubic-transfer theorem in mathlib: the present Lean formalization is deliberately restricted to closed arithmetic.
2. Find a practical detector/phase design with a substantially larger smallest eigenvalue, then simulate loss, dark counts and phase calibration statistically.
3. Verify exactly which two degree-30 irreducibles of PSp4(3) are complex conjugates, and construct exact rational idempotents of the route orbital algebra.
4. Solve the cubic Jordan adjoint conditions for the two-parameter invariant cubic family, allowing genuine frame-moving maps into the existing compact Albert algebra.
5. Build a matter-free field action that predicts a Lorentzian cone without externally supplying Dirac spinors or Wilson regulator, and quantitatively rule it out if it fails. Everything here remains mathematical or synthetic physics rather than a TOE.
