# TOE Round 25 — exact distance-three W33 code and four independent physics frontiers

**9 October 2026.** Repository: `wilcompute/W33-Theory`. This pass executes all five independent directions from Round24 and distinguishes exact mathematics, assumptions of a toy Hamiltonian, prior results, and experimental requirements. No claim of a complete Theory of Everything, established physical vacuum, observed physical spectrum, 4D Lorentzian gravity, or built hardware is made.

## Originality audit

Previously established in the repository: W33's GQ/Levi 40+40 objects, 160 edges, 1,620 native eight-cycles and 81D cycle space; BT1688 irreducibility of the 81D PSp4(3) Steinberg module and the earlier full group character calculation; Pass4659/4616's 27 Schläfli carrier and 45 tritangent/support bijection; Pass 4474's 1,620 apartments; Round23's 45×36 overlap-three frame components; Round24's exact distance-one partial Wilson codes and strong-coupling five-band prediction; `SRG(45,32,22,24)` transport graph already used elsewhere in the repository. New claims below concern **newly tested connections/obstructions** and an explicitly selected high-distance CSS construction, not these original objects.

## 1. The actual E8/PSp character-factorization test

The W33 first homology is the 81-dimensional irreducible Steinberg representation of `G=PSp(4,3)`, order 25,920. Enumerate the exact G action and find an order-five element `g` fixing no W33 points, no lines and no flags. The virtual chamber–vertex permutation character gives

`chi_St81(g) = #fixed flags - #fixed points - #fixed lines +1 = 0-0-0+1 = 1.`

If an 81-dimensional module were `R_27 tensor C^3_trivial`, for **ANY** 27D representation R, then `chi_St(g)=3 chi_R(g)`; hence `chi_R(g)=1/3`. This is impossible because traces of finite-order group representations are algebraic integers. This test improves Round24's obstruction from one specific 27-line permutation representation to **every** 27D candidate with a trivial three factor.

There is a second, **externally sourced classification** point, not independently group-classification-proved here: the only nonabelian finite simple subgroups of `PGL_3(C)` are `A5`, `PSL(2,7)`, and `A6`. The 25,920-element simple group PSp4(3) is not one of them, so it has no nontrivial projective 3-dimensional representation. Therefore a symmetry action factoring into the standard `E6 × A2` factors cannot endow the A2 fundamental 3 with a nontrivial projective PSp action. Under such a **factor-preserving embedding assumption** the above no-go is particularly restrictive.

This is emphatically **not** an impossibility theorem for the full E8 Lie algebra or an arbitrary non-factor-preserving embedding, nor does it exclude different groups, extensions, gradings or spontaneous symmetry breaking. No actual E8 intertwiner is constructed.

Sources for external group classification:
- https://archive.mpim-bonn.mpg.de/id/eprint/3662/1/preprint_2009_76.pdf
- https://www.math.rwth-aachen.de/homes/sam/ctbllib/doc2/chap11_mj.html

Reproducer: `analysis/w33_20261009_toe25_e8_character_factorization_nogo.py`.

## 2. What an E6-sector conservation law must forbid: exact 45-sector tunneling compression

Let `A3` be the 8-regular 1,620-apartment hopping graph on pairs sharing exactly three of their four rays, and `A2` be the 90-regular hopping graph on pairs sharing exactly two rays (not three). Round23 proved A3 has 45 disjoint components of 36 states each; Round24 proved those component labels are exactly the previously established E6-tritangent 45-set.

Construct the `1620×45` incidence matrix `P` of components, with every column of length 36. The *normalized uniform-sector compression* of the symmetry-invariant A2 is

`Q = P^T A2 P / 36 = 18 I_45 + (9/4) B_45,`

where the binary matrix `B_45` is **exactly** strongly regular with parameters `SRG(45,32,22,24)`. Verify algebraically `B^2=32I+22B+24(J-I-B)`. Q's exact eigenvalues are `90^1, 22.5^24, 9^20`; its off-diagonal inter-sector amplitudes are 9/4 on precisely the 32 adjacent tritangent sectors.

**Important no-go:** `A2 P != P Q`. Therefore the uniform 45-sector space is **NOT an exact invariant subspace** of A2 and the 45×45 matrix is a **compression**, not the exact reduced Hamiltonian. In particular, an averaged 9/4 hopping is not a per-frame microscopic matrix element. A2 couples not just distinct tritangent sectors but also sector-internal excited modes.

Each projector onto an A3 component commutes with `H=-t A3`. A2 violates that conservation law while preserving full PSp symmetry. Thus W33/PSp alone **cannot protect** a tritangent-sector superselection rule; any fundamental prohibition of A2 must be an additional physical constraint or conserved charge. This is new interaction data joining the existing E6 45-object geometry, not a new discovery of the graph SRG(45,32,22,24).

Reproducer: `analysis/w33_20261009_toe25_e6_sector_tunneling_quotient.py`.

## 3. A controlled W(3,q) fixed-filling tower — and why naive attraction collapses

For the classical symplectic GQ family, v(q)=2(q+1)(q²+1) Levi sites with degree k(q)=q+1. At boson count N≈ρv with ρ>0 fixed consider the standard attractive graph Bose-Hubbard Hamiltonian with hopping t and attraction U, both held fixed as q increases.

**Exact energy bounds** in the N-boson sector:

`- U N(N-1)/2 - t k N <= E0 <= -U N(N-1)/2.`

The upper bound is the on-site all-N-bosons state; the lower bound follows from the one-body graph spectral norm k and maximum possible on-site pair count N(N-1)/2. Since k/v→0, the squeezed exact limit is

`E0/v² -> -U ρ²/2`, and hence `E0/v -> -infinity`.

This fixed-coupling attractive theory has **no finite extensive thermodynamic energy density**. It therefore cannot justify naive extrapolation of the Round21–24 few-boson vacuum results into a stable field-theory vacuum.

Uniform N-boson condensate trial energy is `-t kN - U N(N-1)/(2v)`. The localized N-boson trial beats this uniform trial when

`U/t > 2k/[(N-1)(1-1/v)]`,

which tends to zero at fixed positive density. This is a variational comparison, **not** a proof of thermodynamic spontaneous symmetry breaking.

One *additional* possible scaling is `t_q=t0/k(q)`, `U_q=u/v(q)`, making kinetic and attraction energies both extensive; the uniform and localized trial branches then cross at `u ρ≈2t0`. This is deliberately marked **assumed rather than derived**. The unmodified family still lacks a stable 4D diffusion plateau (Round21).

Exact q=2,3,5,7,11,31,101 evaluations and analytic limits included. Finite-q ground states remain positive and symmetric for any t>0; the order of h→0 and q→∞ limits has NOT been solved.

Reproducer: `analysis/w33_20261009_toe25_thermodynamic_tower.py`.

## 4. Breakthrough: an exact [[160,1,3]]_3 local W33 gauge CSS code

Round24 demonstrated distance1 for edge/vertex-complement Wilson selections. Here construct a strictly stronger **distance-three qutrit CSS code**.

Let D be the native oriented 80×160 incidence boundary, rank79 over F3. All 1,620 simple length-eight Levi cycles generate an 81D cycle space. Pick three *pairwise vertex-disjoint* incidence edges; exact deterministic indices `[0,4,8]` in the script's native flag ordering. Define the 160-component ternary cochain f that is +1 on these three edges and zero elsewhere.

Select those oriented eight-cycle Wilson Z checks with `f·c=0 mod3`. Exact result: **1,395** cycles obey the equation, with rank **80**; a deterministic elimination explicitly materializes only **80 independent weight-eight Wilson generators**. Every one of the 160 edges is supported by the selected-check span, and the 80 generator set has the same constraints. The 80 four-edge vertex Gauss X operators have rank79, so physical qutrits n=160, independent stabilizer rank159, **k=1 logical qutrit**.

An explicit logical X is supported on exactly the three chosen edges, `X_f`. It commutes with every Wilson and Gauss check but is not a Gauss stabilizer. **No weight-one or weight-two X error can commute with all selected Wilson checks:** this is verified independently by normalizing all 160 Wilson syndrome columns in F3 and checking they are nonzero and all projectively distinct. This exhausts every possible weight-one/two X operator, including combinations with Pauli exponents ±1.

For a structural proof of minimum weight: the X logical coset consists of f plus oriented vertex cuts. The native 4-regular bipartite Levi graph has nonzero edge cuts of size ≥4, and its only size-four cuts are single-vertex stars. The latter follows from `|δ(S)|≥(4-√6)|S|(80-|S|)/80`, bipartite even cut sizes, and direct cases for one and two vertices. A vertex star meets the three disjoint edges in at most one place; therefore f plus a cut has weight≥3. Cuts of size≥6 also cannot reduce weight below3. The logical X distance is **exactly 3**.

Every nontrivial logical Z lies in ker(D), so contains a graph cycle; GQ incidence girth8 gives **Z-distance at least8**. Thus

`[[160,1,3]]_3` **exactly**.

This is a genuine stabilizer code correcting an arbitrary single-qutrit error in the ideal code model. It is not an error threshold, scalable quantum LDPC family, protected vacuum at finite temperature, or measured hardware. Three distinguished edges break full PSp symmetry. Actual fault-tolerant extraction circuits remain a separate problem.

Reproducer: `analysis/w33_20261009_toe25_css_distance_three.py`.

## 5. Hardware-specific conditions for the five-band W33 doublon test

The conditional spectroscopic target requires **80 bosonic sites and 160 calibrated links** and coherent preparation of an on-site two-boson *doublon* with real attractive onsite interaction U (a hard-core-only two-level simulator is insufficient). The five leading strong-attraction band weights per local source are exactly `[1,24,30,24,1]/80`, and the nonzero gaps are multiples of `2t²(4-√6)/U`. Earlier Round24 verified projector weights without assuming point↔line symmetry.

For an **illustrative, explicitly hypothetical** hopping frequency `t/h=5 MHz` and U/t in 16,32,64,128, the leading smallest excitation-frequency gaps are respectively **0.9691, 0.4845, 0.2423, 0.1211 MHz**. Fourier resolution of about ten smallest-gap periods needs **10.32, 20.64, 41.28, 82.55 microseconds**, respectively. At U/t=32 the full 3,240-state diagonalization from Round23 predicts ≈1% finite-U correction to the leading pair gap. A hypothetical T2≈100μs implies a pure-dephasing Lorentzian FWHM ≈3.18 kHz **in the simplest exponential-coherence model**; real loss, pulse constraints and frequency disorder also matter.

Requirements: verify all 160 correct couplings and frequencies, calibrate t and U independently, load a site-selective doublon, measure site-resolved return/conditional two-particle coincidence through >10 gap cycles, repeat on point and line sites, extrapolate U/t and quantify disorder and linewidth. The computation is a *requirements certificate*: no apparatus has been built or demonstrated feasible.

Relevant published context (these DO NOT demonstrate the exact W33 setup):
- Site-resolved many-body Bose-Hubbard spectroscopy in superconducting circuit lattices: https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.7.L022038
- Proposed multilevel Rydberg tweezer Bose-Hubbard analog: https://journals.aps.org/pra/abstract/10.1103/PhysRevA.109.053317

Photonic Holonet boundary: a single photon with passive linear optics does not automatically supply the *two interacting bosons* and nonlinear attractive U required by this test.

Reproducer: `analysis/w33_20261009_toe25_hardware_spectroscopy_targets.py`.

## Scientific bottom line

Most important **positive** result: an explicit native Wilson-constraint `[[160,1,3]]_3` code with 80 materialized weight-eight Wilson generators and independent syndrome column test. Most important **negative** results: exact order-five trace blocks all trivial-A2 27×3 Steinberg identifications, full symplectic symmetry fails to protect E6 sector labels against an allowed A2 hop, and the unscaled attractive thermodynamic tower has divergent energy density. Additional conditional outputs: the 45-sector E6 transport SRG compression and a quantitative spectroscopy hardware checklist.

All results are mathematical or conditional on specified Bose-Hubbard/stabilizer/frame Hamiltonians. No 3+1D Lorentzian gravity, actual E8 Standard Model matter intertwiner, physical mass or experimentally verified TOE follows.

Five reproducible Python producers, five JSON result certificates, and focused `tests/test_w33_20261009_toe25_five_fronts.py` are supplied.
