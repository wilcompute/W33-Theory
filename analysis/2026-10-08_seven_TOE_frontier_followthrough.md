# 2026-10-08: seven operational and physical-interface tests after the five-frontier packet

**Disposition:** Seven executed investigations across the five previously requested physics fronts plus two additional cross-checks. **Not** a completion of gravity, the Standard Model, the string vacuum, or a physical TOE.

**Executable source:** `analysis/w33_20261008_six_toe_frontier_followthrough.py`. **Exact/controlled data:** `data/w33_20261008_six_toe_frontier_followthrough.json`. **Independent checks:** `tests/test_w33_20261008_six_toe_frontier_followthrough.py`. Names retain the initial six-frontier label; the committed producer now executes **seven** probes.

## Audit and boundaries

The starting point is the prior [five-frontier pass](2026-10-08_five_physics_frontiers.md), the September 24 two-nonisomorphic-27-graph result, and the [October 8 exact electrical network](2026-10-08_dual_27_electrical_transport.md). The concurrent Pass398 formula-universe freeze (head `4dfd0a470`) was incorporated before creating the separate clean worktree. The review also covered Passes 10952/11038 (CP firewalls), 11374 (an earlier CP-even two-sign ray selector), 11697/11698 (320 paired chiral vacua), 11742–11757 (an actual nonzero holomorphic three-mode cup, CY quotient, Higgs/proton/vacuum obstructions), and the [forty-points epilogue](../papers/forty_points/sec11_epilogue.tex). No physical TOE completion is claimed by any of these earlier certificates. The dual27 graphs, SU(2) Gauss and chiral vacua are **pre-existing**. A source grep found no occurrence in the tracked text/certificates of the new rational dual27 continuous-time average-mixing values `110/729`, `13/1458`, or their `220/13` ratio. Absence from a grep is not a global mathematical novelty claim.

## I. Exact coherent quantum transport, not merely a stochastic channel

For each W33 27-vertex carrier let \(A=A^T\in\{0,1\}^{27\times27}\) and define the supplied unitary Hamiltonian \(H=A\), in units with \(\hbar=1\). Both have the identical spectrum \(8^1,2^{12},(-1)^8,(-4)^6\), but **equality of eigenvalues does not identify position-basis dynamics**. Their exact idempotent projectors are

\[
E_\lambda=\prod_{\mu\ne\lambda}\frac{A-\mu I}{\lambda-\mu},
\quad
e^{-itA}=\sum_\lambda e^{-it\lambda}E_\lambda,
\quad
\overline M=\sum_\lambda E_\lambda\circ E_\lambda.
\]

This is the [standard average-mixing formalism](https://arxiv.org/abs/1103.2578) of Godsil, applied here to the pre-existing W33 dual27 example. All entries in the exact time-mean \(\overline M\) are rational. Histograms for *unordered distinct* pairs, which sum to \(\binom{27}{2}=351\):

| \(\overline M_{ij}\) | 27 opposite W33 points | 27 transverse null lines |
|---|---:|---:|
| \(13/1458\) | 216 | 0 |
| \(14/729\) | 0 | 162 |
| \(20/729\) | 108 | 108 |
| \(26/729\) | 0 | 81 |
| \(110/729\) | 27 | 0 |

The coherent walk is **unitary** with measured residual \(\lVert U^\dagger U-I\rVert_{\max}<10^{-12}\). The independently implemented discrete Fourier quadrature over 32 equally spaced samples from one \(2\pi\) period agrees with exact projectors to \(10^{-12}\); gaps of the integer eigenvalues have absolute value below 32, making the Fourier cancellation exact in principle.

At supplied dimensionless \(t=0.43\) the 351 pair probabilities also fall into distinct three-class histograms, detailed in JSON. We also constructed the Szegedy 27-to-729 isometry

\[
V|i\rangle=|i\rangle\otimes\frac1{\sqrt8}\sum_{j\sim i}|j\rangle
\]

and the product of two reflections on the 729-dimensional directed-edge register. \(V^\dagger V=I_{27}\); both reflectors preserve norm. The symmetric uniform superposition over 216 directed edges is a fixed state. Szegedy's construction is established prior art, not a W33 invention: [Szegedy (2004)](https://arxiv.org/abs/quant-ph/0401053); [Wocjan–Temme](https://arxiv.org/abs/2107.07365).

**Hardware firewall:** a 27-path, single-photon or other 27-level encoding and correct coupling matrix are *inputs*, not physical results. Uniform amplitude loss \(e^{-\gamma t/2}\) changes unconditional success but does not alter conditional, normalized position probabilities; graph-dependent loss and disorder are open calibration issues. Same spectral eigenphases means phase estimation **alone** cannot distinguish the carriers; position-resolved interferometry can under the stated encoding.

## II. Actual local Lie closure over \(\mathbb Q\) on an eight-cycle in W33

Prior packet showed one Poisson-bracket obstruction for the canonical nearest-edge current

\[
J_{ij}=(p_i+p_j)(q_i-q_j),\quad
\{q_i,p_j\}=\delta_{ij}.
\]

On the explicit induced W33 Levi eight-cycle, with Levi vertex addresses \([0,40,1,44,4,53,13,41]\), write \(J_{ij}=p^TM_{ij}q\), where \(M_{ij}=(e_i+e_j)(e_i-e_j)^T\). Then \(\{J_M,J_N\}=J_{[M,N]}\) (for the defined bracket order). The initial eight edge matrices generate a **34-dimensional** Lie algebra under all nested commutators, computed two independent ways:

- exact rational Gaussian elimination of integer-matrix commutator words, which terminates at **34**;
- elimination modulo 101, also **34**.

This does *not* yet identify the abstract 34D Lie algebra. Every generated \(M\) annihilates the all-ones vector on the right and the alternating point/line covector on the left, and has \(\mathrm{tr}M=0\). Those two invariant vectors plus trace constrain the possible algebra to dimension at most 48 on eight vertices; 34 is more restrictive. The full 80-vertex Lie closure, canonical phase-space metric constraints, correct continuum limit, and the Dirac hypersurface-deformation algebra remain untested. This is a robust and exact negative answer for the eight-neighbor-generators-only model.

For perspective, discrete first-class hypersurface constraints **have been constructed** in appropriate gravity sectors: [Bonzom–Dittrich, 2013](https://arxiv.org/abs/1304.5983). A graph current algebra, even if it closes, is not automatically Einstein dynamics.

## III. Spontaneous chirality: a testable obstruction and a wall-energy scale

Pass 11698 already proves 320 relevant W33 chiral stabilizer vacua, grouped into 160 conjugate-sign pairs; Pass 11374 supplied another symmetry-even toy phase selector with two conjugate minima. Here we construct the **line graph of the actual 80-vertex W33 Levi graph**: its 160 incidence flags have 480 adjacency edges, and each flag has degree six. An exact graph-connectivity calculation gives

\[
\lambda_{\mathrm{edge}}(\mathrm{FlagGraph})=6.
\]

For the *supplied ferromagnetic* \(\mathbb Z_2\) toy Hamiltonian \(E=-J\sum_{xy}s_xs_y\), \(J>0\), connectedness yields exactly **two** uniform ground states, exchanged by global sign. A nonuniform configuration creates a cut \(\delta(S)\), and its energy relative to either ground state is \(2J|\delta(S)|\ge12J\). Thus local coupling can order the discrete signs without picking the absolute handedness. The \(12J\) is a **graph-domain-wall energy**, not a cosmological wall tension or mass, and \(J\) is supplied rather than derived.

A CP-even action cannot, on its own, distinguish a configuration from its exact CP conjugate; choosing a unique handedness demands a physical source or global selection mechanism with its own independent consistency tests. This is compatible with, but does not solve, the broader domain-wall considerations in [Krauss–Rey](https://arxiv.org/abs/hep-ph/9203212).

## IV. A sharpened string-vacuum candidate *filter*: proton hexality

The previous pass verified that conventional matter parity alone leaves the dangerous \(QQQL\), \(U^cU^cD^cE^c\) dimension-five operators invariant. As a constructive **charge-filter replacement**, use the following \(\mathbb Z_6\) residues, a proton-hexality-type representative of the established symmetry family:

| Superfield | \(Q\) | \(U^c\) | \(D^c\) | \(L\) | \(E^c\) | \(N^c\) | \(H_u\) | \(H_d\) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Charge mod 6 | 0 | 1 | 5 | 4 | 1 | 3 | 5 | 1 |

All Yukawa couplings, \(H_uH_d\), \(N^cN^c\), and the Weinberg operator are neutral; \(U^cD^cD^c\), \(QLD^c\), \(LLE^c\), \(LH_u\), \(QQQL\), and \(U^cU^cD^cE^c\) are all non-neutral. The residues of the last two are **4** and **2**, respectively. A singlet with \(B-L=-2\), \(q_6=0\), can acquire a VEV without breaking this \(Z_6\) filter, while the assigned \(N^c\) condensate of \(q_6=3\) would break it to a \(Z_3\) subgroup. We obtain mixed modular sums \(SU(3)^2 Z_6=18\), \(SU(2)^2 Z_6=18\) and weighted gravitational \(Z_6=102\), divisible by six; these are **necessary modular checks**, not a full discrete gauge anomaly or Green–Schwarz certificate.

An exhaustive restricted charge-only scan allowing all desired couplings and forbidding all six hazardous examples has counts \(N=2:0,3:0,4:8,5:0,6:24\). The eight \(Z_4\) charge-filter solutions **do not contradict** the literature's classification of anomaly-free discrete gauge symmetries: the scan has not imposed its full anomalies, field-equivalence quotient, or worldsheet constraints. The actual proton-hexality classification is prior work: [Dreiner–Luhn–Thormeier](https://arxiv.org/abs/hep-ph/0512163).

**This is not a new heterotic compactification.** The repository's specific FI, spectral-exotic and three-generation vacua must each be tested for this symmetry's **actual** realization. Real smooth heterotic line-bundle Standard Models with proton filters exist in the literature: [Anderson–Gray–Lukas–Palti](https://arxiv.org/abs/1202.1757).

## V. Canonically normalized flavor and one-loop running, with input audit

The repository's actual Pass 11742 *already* supplies a nonzero selected holomorphic cubic coefficient \(1/2\) in a declared residue normalization. That does not supply all matrix entries or the Ricci-flat/Hermitian–Yang–Mills kinetic metrics. To expose the underdetermination without assuming them, this pass supplies explicit **control** \(3\times3\) holomorphic Yukawa textures \(Y_u,Y_d\) and positive kinetic matrices \(K_Q=\operatorname{diag}(1,4,9)\), \(K_U=\operatorname{diag}(2,1,3)\), \(K_D=\operatorname{diag}(1,2,4)\). Their canonical counterparts are

\[
Y_u^{\mathrm{phys}}=K_Q^{-1/2}Y_uK_U^{-1/2},\quad
Y_d^{\mathrm{phys}}=K_Q^{-1/2}Y_dK_D^{-1/2}.
\]

The control \(Y_u\) is diagonal \((0.5,0.2,0.05)\), and the complex \(Y_d\) entries are explicitly specified in the certificate and producer. The smallest three normalized up-type singular values become \((0.00962250,0.1,0.35355339)\), versus \((0.05,0.2,0.5)\) without the metric. The rephasing-invariant mixing number

\[
J=\operatorname{Im}\big(V_{00}V_{11}V_{01}^{*}V_{10}^{*}\big)
\]

changes from \(-0.000946459\) in the *un-normalized toy control* to \(+0.00003104397\) in its stated metric. Under a further arbitrary common unitary left-family basis rotation, the normalized singular values and J agree within numerical precision (absolute J difference \(<2\times10^{-17}\)). This is an explicit **basis-invariant but metric-dependent** observable. Invertible normalization never lifts the rank of a model containing only one independently certified nonzero holomorphic coefficient: its matrix rank remains 1; unspecified additional cup products could change this.

A supplied one-loop SM top-Yukawa-only approximation with *fixed* gauge couplings \((g_Y,g_2,g_3)=(0.357,0.65,1.16)\), \(y_t(173\,\mathrm{GeV})=0.94\), gives \(y_t(1000\,\mathrm{GeV})\approx0.857586723\). It ignores gauge running and all other Yukawas, and is **not a derived or precision-matched measurement**. The literature makes the missing kinetic normalization requirement explicit: [Blesneag et al. (2018)](https://arxiv.org/abs/1801.09645), [Butbaia et al. (2024)](https://arxiv.org/abs/2401.15078).

## VI. Experimental shot-budget upper bound (extra)

The earlier measure-and-prepare channels (not the coherent walks of Part I) exhibit 54 ordered off-diagonal point-side pairs whose **two-step** transition probability is zero, while every line-side pair is positive, with minimum \(1/64\). For a **known differentiating pair** and symmetric, stipulated depolarizing readout contamination \(\eta=1/10\), the conditional gap is exactly \((1-\eta)/64=9/640\).

For independent binary experiments and desired two-sided Hoeffding error at most 0.05, a conservative sufficient count is \(n\ge 2\log(2/.05)/(9/640)^2\), i.e. **37,308 detected shots per known pair**. A further independent uniform photon survival factor \(\exp(-0.1\cdot0.43)\) yields a conservative **40,659 launched trials**, if loss is treated as a null observed outcome instead of postselection. This bound is deliberately conservative and conditional: unknown vertex labeling, switching systematic errors, crosstalk, preparation quality and coherent/interferometric noise are not accounted for. It does not establish a usable experimental protocol without calibration.

## VII. Counterintuitive classical-versus-coherent transport (extra)

Combine the prior **exact effective resistance** with this pass's coherent **time-average** \(\overline M_{ij}\). Every unordered pair lies in the following classes:

| Carrier | Graph distance | Effective resistance | \(\overline M_{ij}\) | Pair count |
|---|---:|---:|---:|---:|
| Point | 1 | 13/54 | 20/729 | 108 |
| Point | 2 | 29/108 | 13/1458 | 216 |
| Point | 3 | 5/18 | 110/729 | 27 |
| Line | 1 | 13/54 | 20/729 | 108 |
| Line | 2 | 22/81 | 14/729 | 162 |
| Line | 2 | 43/162 | 26/729 | 81 |

Thus **point-side distance-three pairs** have coherent time-average probability \((110/729)/(13/1458)=220/13\approx16.923\) times the point-side distance-two pairs, despite larger classical effective resistance. This separates unitary interference from classical random-walk transport in a particularly clean, exact W33 example. It is **not** a superluminal or acausal signalling claim: graph distance, elapsed physical time and speed of light have not been identified, and the limit averages over arbitrary long walk times.

## Test conditions and physical status

The independent regression explicitly reconstructs all exact projectors, tests 32-point Fourier time averages, independently builds the 729-by-27 walk isometry, recomputes the rational/modular 34-dimensional Lie closure, verifies 160-flag edge cuts, scans the finite \(Z_N\) charge candidates, and tests metric/frame invariance and the RGE control. Earlier dual27 and five-frontier regressions are run together. None of these tests establishes a 4D first-class gravitational constraint system, singles out a chirality from an exact CP-symmetric action, produces a new consistent string vacuum, predicts particle masses, or demonstrates photonic hardware. The next experiments should be framed to falsify concrete models rather than interpret finite counts as measured constants.
