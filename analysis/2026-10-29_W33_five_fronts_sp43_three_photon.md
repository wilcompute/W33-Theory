# W33 five-front continuation and outside-box optical discriminator — 2026-10-29

**Status:** reproducible mathematical results plus ideal standard-quantum-optics predictions.

**Parallel-commit reconciliation:** Commit 812e85e2 (published during this research) independently establishes the full 28-graph SRG binary CSS atlas, the same W33/dual [[40,8,6]] versus [[40,20,4]] contrast, and a constructive 8-mode E8 order-four optical-sign witness. Those results are now PRIOR REPOSITORY WORK and are not claimed novel here. This continuation separately certifies all 51,840 natural Sp(4,3) to integral E8 word identities, implements a 40-mode rectangular mesh, reconstructs 1120-vertex C3(3), and provides the full distinct-output three-photon discriminator that is not in the parallel atlas. These do not solve the Theory of Everything, predict fundamental constants, demonstrate a fault-tolerant machine, or establish an exact q=7 CSS distance. Prior repo work and outside literature are acknowledged.

## 1. Identifying the integral E8 double cover
The earlier releases established a faithful PSp(4,3) action on the logical eight-dimensional plus-type quadratic space H of the [[40,8,6]] adjacency CSS code and found an order-four E8 lift of a finite involution. The new producer analysis/w33_20261029_sp43_integral_cover.py constructs 240 E8 roots, finds exact integer Cartan-preserving lifts of the seven generators, and **enumerates every group element twice in parallel**: as its natural four-dimensional F3 symplectic matrix and its integer eight-dimensional E8 root action. All generator word equalities agree, the natural -I4 maps to the integral -I8, and both representations contain 51,840 distinct elements. Exactly two integral elements map onto each of the 25,920 mod-two elements.

Therefore the constructed nonsplit E8 lattice subgroup is **Sp(4,3)**, NOT merely some unspecified order-51,840 group. It is distinct from the same-order but different group PGSp(4,3) ≅ W(E6). Of the 315 projective involutions, 270 have order-four integral lifts and 45 have order-two lifts (540 and 90 lifts, respectively). A central global sign needs an actual physical controlled encoding to become observable in relative phase.

## 2. Rectangular 40-mode photonic compilation
analysis/w33_20261029_rectangular_optical_mesh.py uses independent two-sided Givens elimination to synthesize U=exp(-i pi A/2) on the one-photon W33 40-mode Hilbert space. Relative to the prior triangular decomposition:

| Measured numerical metric | Rectangular | Triangular |
|---|---:|---:|
| Active adjacent two-mode gates | 656 | 653 |
| Sequential disjoint-mode gate layers | **40** | 77 |
| Max reconstruction error | 4.72e-16 | 4.44e-16 |
| Worst input survival at per-active-gate eta=.999 | **.9649166711** | .9560580643 |
| Mean input survival at same eta | .9677314659 | **.9679187334** |
| Input-zero survival | .9719032631 | .9804659819 |

The rectangular architecture reduces depth by 48%; it does NOT uniformly improve photon survival under the specified component-loss model. Path-propagation loss and detector errors are not modeled. A single photon in 40 modes still cannot encode the entire 256-dimensional logical Hilbert space of eight qubits. Design antecedent: Clements et al., Optica 3, 1460 (2016), https://doi.org/10.1364/OPTICA.3.001460 .

## 3. Dual-polar dynamics at increasing geometry rank
analysis/w33_20261029_dual_polar_C3_3.py constructs all 1,120 Lagrangian 3-spaces of F3^6 and all 3,640 isotropic 2-planes; every plane belongs to four Lagrangians. The dual-polar graph has degree 39, diameter 3, shell sizes [1,39,351,729], intersection arrays b=[39,36,27,0], c=[0,1,4,13], a=[0,2,8,26], and eigenvalues [39,11,-1,-13]. Any pair at distance three has exactly 52 length-three walks. For nearest-neighbor CTQW the offsite amplitude is of order t^3, nonzero for arbitrarily early generic positive times: graph diameter does NOT imply an exact Lorentzian light cone. The dimensionless adjacency walk revives at t=pi/2; there is no derived seconds-scale clock. Standard theory: https://doi.org/10.1007/s00013-023-01829-2 .

## 4. Three-photon graph discrimination (new concrete protocol)
The point W(3,3) graph and its dual line-intersection graph are nonisomorphic SRG(40,12,2,4) graphs with identical spectra. Literature: Spence (2000), https://doi.org/10.37236/1500 . Their ideal quarter-cycle walk matrix is U=(2J-5(I+A))/15. All photon probabilities are therefore exact rational numbers from integer bosonic permanents.

analysis/w33_20261029_three_photon_dual_discriminator.py constructs both graphs and checks ALL 608,400 pair-input/pair-output combinations: the complete aggregate **two-photon distinct-output** histograms are identical. It then calculates all 9,880 distinct three-photon output triples for each of all 3,240 independent three-photon input triples per graph. The W33 point graph has 2,880 independent triples with one common neighbor and 360 with FOUR; the dual graph has 1,080 with zero common neighbors and 2,160 with TWO. Each common-neighbor class has a unique complete output histogram.

For each of the 360 W33 four-common-neighbor input triples, there are four distinct-output triples with exact probability 26244/11390625 = **0.002304** each. For ANY independent input triple of the dual graph, the maximum such probability is 11664/11390625 = **0.001024**. This is an ideal, falsifiable optical graph discriminator **inside conventional quantum mechanics**, not a beyond-QM effect. Noise/loss, photon distinguishability and hardware imperfections require further analysis.

### Beyond the original five: dual adjacency quantum code
The two cospectral point graphs have very different binary adjacency ranks: W33 rank 16, dual rank **10**. The dual's self-orthogonal adjacency code is exactly **[[40,20,4]]**: all 780 weight-two patterns excluded, 270 weight-four kernel words enumerated and all are nonstabilizers; exhaustive 1,024 stabilizers have minimum weight **12**. Contrast the prior W33 [[40,8,6]]. This is a mathematical contrast, not evidence for a new physical interaction.

## 5. Honest q=7 distance firewall
Previous exhaustive work certifies the W(3,7) binary adjacency CSS code [[400,48,d]] with **10 <= d <= 14**, and randomized searches found weight 14. The new MILP producer analysis/w33_20261029_q7_milp_falsifier.py tests A*x=2*y with binary x, integral y and fixed support size, factoring point transitivity and adjacent/nonadjacent second-point orbits. Both 20-second weight-ten feasibility jobs ended at the solver time limit without a counterexample or proof of infeasibility. **Inconclusive; the exact distance remains unknown.** Weight-twelve feasibility is also open. Any d=14 theorem requires actual proof or a reproducible solver infeasibility certificate.

## Reproduce
python analysis/w33_20261029_sp43_integral_cover.py
python analysis/w33_20261029_rectangular_optical_mesh.py
python analysis/w33_20261029_dual_polar_C3_3.py
python analysis/w33_20261029_three_photon_dual_discriminator.py
python analysis/w33_20261029_q7_milp_falsifier.py 10
python -m unittest discover -s tests -p test_w33_20261029_advanced_five_beyond.py -v

The E8 full enumeration is slower (~45 s on Linux). The optical and three-photon scripts use NumPy; the q7 MILP script uses SciPy. Preserve existing unrelated local modifications when synchronizing the user checkout. All physically interpretable claims remain at the representation/prototype level unless a real device and independent test are supplied.
