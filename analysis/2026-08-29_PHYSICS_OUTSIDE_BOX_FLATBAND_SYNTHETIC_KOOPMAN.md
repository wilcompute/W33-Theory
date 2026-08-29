# Three literature-informed physics attacks

Date: 2026-08-29

These three attacks were selected only after auditing the repository's existing magnetic/BdG, SU(3), Ramanujan, Chern, OAM, and timing work, so they do not repeat already-covered physics fronts.

## 1. 85-state chiral flat band: index protection versus symmetry protection

The 40x45 Hermitian cross-incidence matrix B has rank 25. The chiral block operator D=[[0,B],[B^T,0]] therefore has 35 zero modes, split 15+20.

The new point is that two different protection mechanisms are present.

- Rectangular/chiral index: for any 40x45 off-diagonal coupling T,
  nullity(T^T)-nullity(T)=45-40=5. Hence at least five zero modes survive arbitrary chiral-preserving perturbations. A concrete integer perturbation of B reaches rank 40 and leaves exactly five.
- PSp(4,3) symmetry: the established permutation-module split is 40=1+24+15 and 45=1+24+20. The unmatched 15 and 20 sectors cannot couple equivariantly, so all 35 zero modes survive PSp-equivariant perturbations. In the natural intertwiner family aB+bJ, generic rank remains 25.

Thus the five-mode residue is index protected; the large 35-mode flat band is symmetry protected.

This attack was motivated by the modern flat-band literature, where bipartite/sublattice imbalance and symmetry are distinct mechanisms for enforced zero-energy bands. The finite W33 statement is exact, but no material band or fermion assignment is claimed.

Executable/certificate:
- `analysis/w33_20260829_pg34_flatband_index.py`
- `data/PART_W33_20260829_PG34_FLATBAND_INDEX.json`

## 2. Six microstates as a 3x2 synthetic internal dimension

The exact six-state image C3 x S3 with its unique 3+3 imprimitivity system admits coordinates (chi,t) in F2 x F3. In a convenient gauge,

- z:(chi,t)->(chi,t+1) is the central/common qutrit translation;
- r translates the two chirality blocks in opposite F3 directions;
- s swaps chirality and satisfies s r s=r^-1.

This gives the exact normal form C3 x S3 = (C3 x C3):C2 and turns the residual hinge-point choice into the F2 coordinate. A minimal finite synthetic-ladder Hamiltonian

H = Z + Z^dagger + g X_chi

has characteristic polynomial

((x-2)^2-g^2) ((x+1)^2-g^2)^2.

The physical analogy is to synthetic dimensions in photonics/atomic systems, where discrete internal modes are treated as lattice coordinates and optically coupled. Here only the finite coordinate system is certified; no physical mode implementation or synthetic gauge flux is inferred.

Executable/certificate:
- `analysis/w33_20260829_qutrit_chirality_synthetic_dimension.py`
- `data/PART_W33_20260829_QUTRIT_CHIRALITY_SYNTHETIC_DIMENSION.json`

## 3. Recovery period two as a Koopman mode, with a time-crystal falsifier

Every declared topology-aware Holotrade trajectory eventually reaches a two-state cycle, so on an individual cycle the Koopman operator is the swap matrix with eigenvalues +1 and -1. Formally this supplies a pi-mode for observables odd under the swap.

But the actual headroom observable rejects the stronger time-crystal reading:

- 19/19 cycles: 2255 starts;
- 17/17 cycles: 572;
- 16/16 cycles: 17;
- 16/17 cycles: only 36.

Thus free-line headroom has nonzero overlap with the -1 mode on only 36/2880 = 1.25% of starts. The dominant 19/19 state cycle is headroom-stationary.

Moreover this is a finite deterministic scheduler with lexicographic tie breaking, not a demonstrated periodically driven many-body Hamiltonian; there is no thermodynamic limit or perturbation-robust spontaneous time-translation breaking. Current discrete-time-crystal literature treats robust subharmonic response under periodic driving as essential, so the repo should retain `period-two recovery orbit` / `Koopman -1 mode` language rather than promote these cycles to a time-crystal phase.

Executable/certificate:
- `analysis/w33_20260829_recovery_koopman_timecrystal_boundary.py`
- `data/PART_W33_20260829_RECOVERY_KOOPMAN_TIMECRYSTAL_BOUNDARY.json`

## Literature used to choose the attacks

- D. Yu et al., *A comprehensive review on developments of synthetic dimensions*, Photonics Insights 4 (2025), R06, arXiv:2503.01465.
- *Synthetic dimensions for topological and quantum phases*, Communications Physics 7, 143 (2024).
- V. Khemani, R. Moessner, S. L. Sondhi, *A Brief History of Time Crystals*, and the Rev. Mod. Phys. colloquium on quantum/classical discrete time crystals: the relevant boundary is robust subharmonic response in periodically driven systems, not merely a finite two-cycle.
- Contemporary flat-band/topological-material reviews distinguish sublattice-imbalance flat bands from additional symmetry-protected degeneracy; that distinction motivated the 5-versus-35 zero-mode audit.

## Evidence boundary

All promoted statements above are finite linear algebra, representation theory, permutation-group theory, or deterministic dynamical-systems facts. Literature supplies analogy and falsification criteria, not proof of a physical realization.
