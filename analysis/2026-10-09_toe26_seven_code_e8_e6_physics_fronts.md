# TOE Round 26: distance-eight W33 qutrit codes, non-factor E8 gate, E6 charge dynamics, scaled-q vacua and C8 prototype

**9 October 2026.** All five independent research directions from Round25 were executed and cross-checked against existing W33/Schläfli/E8/apartment/Bose-Hubbard scripts. Existing parallel contributions remain untouched. Claims below are precise finite mathematical constructions, conditional Hamiltonian calculations, or quantitative prototype requirements, **not** an experimentally confirmed or mathematically complete Theory of Everything.

## Prior-art / provenance

Established **before** this pass: W33 point-line Levi 80 vertices and 160 edges; 1,620 simple length-eight cycles spanning 81D H1; the integral clique–Levi homology bridge; `PSp(4,3)` irreducible Steinberg-81; E8's `sl9 + Λ³9 + (Λ³9)*` Lie algebra in Pass11681; the 27 Schläfli degree-27 permutation module and its `1+6+20` irreducible decomposition in Pass7017-7024; 45 E6 tritangent supports in Pass4659; 45×36 apartment hopping components, symmetry-permitted two-ray transitions and their SRG(45,32,22,24) **compressed** tunneling matrix in Round23–25; fixed-coupling Bose-Hubbard thermodynamic collapse in Round25; and Round25's first `[[160,1,3]]_3` hyperplane-local-Wilson code and its three-edge supporting matching. Other repo codes and logical defenses are separate.

The new results here strengthen the specific matching/Wilson construction to **distance eight** with an analytic global minimum-distance argument and independent integer optimization; test it on W(3,2); obstruct the concrete 6+3 SU9 route to E8; compute dynamical tritangent superselection failure at first order; analyze an extensive scaled-q variational family; and give a full 36-state minimal spectral prototype with leakage.

## 1. Major gain: native eight-local CSS codes `[[160,1,d]]_3`, every d from 3 to 8

Take native 160 incidence-link qutrits and 80 vertex Gauss `X` constraints of rank79. Let `C` denote the 1,620×160 oriented eight-cycle matrix; rank `C=81` over F3. Choose a matching F of r pairwise vertex-disjoint incidence edges and its F3 indicator cochain f. Select **only** eight-cycle Wilson `Z` stabilizers c obeying `f·c=0` mod3.

For six explicitly frozen matchings of sizes `r=3,4,5,6,7,8`, the selected eight-cycle ranks are **all exactly80**, and each has an explicitly extracted basis of only 80 weight-eight Wilson checks. Gauss has rank79, so `n=160, k=160-79-80=1` qutrit. The exact native selected-loop counts are:

| r | Selected eight-cycles | Independent eight-local Z checks | Proven distance |
|--:|--:|--:|--:|
| 3 | 1395 | 80 | 3 |
| 4 | 1332 | 80 | 4 |
| 5 | 1253 | 80 | 5 |
| 6 | 1198 | 80 | 6 |
| 7 | 1137 | 80 | 7 |
| **8** | **1074** | **80** | **8** |

**Proof of the global X-distance, not just syndrome sampling.** Since the Wilson row span is `ker f` inside the full 81D Levi cycle space, its orthogonal is `im(D^T)+span(f)`; every nontrivial logical X has representative f plus a ternary vertex gradient, or twice f plus such a gradient.

Fix r≤8 and a nonconstant ternary potential φ. Let T be its support of differing-label graph edges. If `|T|≥16≥2r`, `wt(f+D^Tφ)≥|T|-r≥r`. If `|T|<16`, the Levi graph is 4-regular with second largest adjacency eigenvalue √6; the Rayleigh cut bound `|δ(S)|≥(4-√6)|S|(80-|S|)/80` implies every nonempty φ color class has size≤10 or ≥70. There must be one class of size≥70; write S for the minority vertices, |S|≤10.

An induced subgraph on at most ten vertices cannot have two independent cycles because the Levi graph has girth8 (a bicyclic graph with minimum cycle length8 needs at least11 vertices). If |S| is 7–10, this forces `|δ(S)|≥16`, contradicting `|T|<16`. Thus `|S|≤6`, where its induced graph is a forest, giving `|δ(S)|≥2|S|+2`. Each F matching edge contributing to the overlap with T consumes a distinct minority vertex, so at most |S| are affected; `wt(f+D^Tφ)≥r+|T|-2|S|≥r+2`. For constant φ weight=r. Thus **d_X=r for all six matchings**.

Every nonzero Z logical is a graph cycle and has weight≥8 by girth. A native eight-cycle excluded by `f·c≠0` exists because the selected rank80 is a proper hyperplane in the full rank81 cycle span; it is a **weight-eight Z logical**. Therefore `d_Z=8` exactly, and total `d=min(r,8)=r`. The d=8 code saturates the upper bound of this eight-local-Wilson hyperplane approach.

**Independent check:** the companion script formulates minimizing `wt(f+D^Tφ)` as a 400-binary-variable ternary labeling integer program, with exact integer input constraints and a HiGHS MILP optimum/dual bound. Across r=3..8 it independently returned `3,4,5,6,7,8`, all with zero or negligible solver MIP gaps. **Distinguish:** the analytic combinatorial argument supplies the mathematical proof; floating-point mixed-integer optimizer output is independent strong computational validation, not itself a symbolic proof.

**Smaller geometry check:** reconstruct `W(3,2)`: 15 points, 15 lines, 30 Levi vertices, 45 flags, 90 oriented simple eight-cycles spanning rank16 over **F3**. Seeded matching searches retain rank15 hyperplane Wilson checks for r=3,4,5, leaving a single qutrit, with independent MILP optima 3,4,5. This gives computed candidates `[[45,1,3]]_3`, `[[45,1,4]]_3`, and `[[45,1,5]]_3`, though the q=2 optimized distances are computer-verified and do not use the W33 q=3 analytic small-cut proof.

No all-q family with growing distance, efficient decoder, circuit-level threshold, or topological order has yet been established. All matchings break full PSp symmetry and the code has one encoded qutrit (rate 1/160).

Reproducers:
- `analysis/w33_20261009_toe26_css_matching_family.py`
- `analysis/w33_20261009_toe26_css_milp_distance.py`
- `analysis/w33_20261009_toe26_q2_css_transport.py`

## 2. Non-E6-factor E8 test: genuine SU9 route still excludes Steinberg-81

We explicitly target a candidate **not factor-preserving with respect to E6×A2**: exploit the *existing* six-dimensional Schläfli permutation constituent of PSp4(3), embedded as `V_9=V_6 ⊕ 1 ⊕ 1 ⊕ 1` in the SU9 maximal-rank subgroup of E8. PSp4(3) is perfect, so the determinant of the six-dimensional representation is trivial and the block action belongs to SL9 over complex numbers. Use Pass11681's bona fide `248 = sl9(80) + Λ³9(84) + (Λ³9)^*(84)` E8 realization.

Under this G action the `sl9` piece splits as `End(V6)` (36D), **six** copies of V6 (6D each), and eight singlets (total80). The `Λ³9` sector splits as `Λ³V6` (20D), three copies of `Λ²V6` (3×15), three V6 (3×6), and one singlet (total84); the dual does likewise. Every displayed summand is G-invariant and has dimension **at most36**.

Since complex representations of finite groups are semisimple, the **irreducible Steinberg-81 cannot be a constituent of this restricted E8 adjoint representation**. Its multiplicity is exactly zero. This is a different obstacle than merely checking whether `St81=27×3_trivial`; the tested embedding acts on the complete 248D E8 adjoint via a concrete SU9 route.

**Scope:** It rules out the selected `6⊕1^3` SU9 embedding. It does not exclude every PSp4(3) subgroup of E8, or all SU9 subgroup representations, or a symmetry-broken/mixed-sector matter mechanism. No physical interaction identification is produced.

Reproducer: `analysis/w33_20261009_toe26_e8_su9_embedding_obstruction.py`.

## 3. E6 45-sector charge: the exact first-order tunneling instability

The prior 1,620-apartment geometry has 45 tritangent-labeled components of 36 frames under hopping `A3`, and 90-regular second hopping `A2` that can connect the components while preserving PSp4(3). Let `P` be the 1620×45 component-incidence matrix.

The already established compressed sector tunneling matrix is `Q=P^T A2 P/36=18I+(9/4)B` with `B=SRG(45,32,22,24)`. We now explicitly use its spectrum `90^1,22.5^24,9^20` for degenerate perturbation of `H=-(A3+εA2)`.

**First-order lowest-excitation gap:** `Δ= (90−22.5)ε+O(ε²)=67.5ε+O(ε²)`. Exact sparse 1,620-state results at epsilon .001,.003,.01 give gaps approximately `0.0673358,0.201030,0.658969`, compared to first-order `0.0675,0.2025,0.675`. Thus the 45-fold degeneracy splits **at first order** for the full symmetry-allowed A2 term.

All 45 component projections commute with A3 but not A2. A group-invariant diagonal potential on a transitive 45-set must be constant, so full PSp alone cannot select one tritangent charge. An extra physical superselection law could prohibit A2, but no such law has been derived. Also, Q is only a **compression**, not an exact A2-invariant 45D subspace.

Reproducer: `analysis/w33_20261009_toe26_e6_sector_charge_dynamics.py`.

## 4. W(3,q) extensive interacting tower: variational jump but no proven physical vacuum

Round25 proved that holding U>0 fixed at N/v→ρ makes E0/v→−∞. Test the explicit **assumed** scaling `t_q=t0/(q+1)`, `U_q=u/[2(q+1)(q²+1)] = u/v`. Finite q=2,3,5,7,11,31,101 have bounded E0/v from exact many-body operator inequalities:

`-t0ρ-uρ²/2 ≤ liminf E0/v ≤ limsup E0/v ≤ -max(t0ρ,uρ²/2).`

Thus energy extensivity pathology is removed. However, the inequalities do not establish existence of the thermodynamic limit.

Go beyond comparing only a uniform condensate and one-site condensate: use the entire normalized coherent interpolation `psi(a) ∝ sqrt(a) δ_vertex + sqrt(1-a) 1/sqrt(v)`, a∈[0,1]. Its limiting variational energy per site is

`e_trial(a) = -t0ρ(1-a) - (uρ²/2)a².`

Because this function is **strictly concave** for u>0, its minimizer must lie at a=0 (uniform) or a=1 (fully localized). The two variational branches cross discontinuously at **uρ=2t0**. This is a **first-order crossing in a restricted variational ansatz**, not an exact full-many-body phase transition. No dynamical critical exponent, causal 3+1D metric or Lorentzian continuum was derived.

Reproducer: `analysis/w33_20261009_toe26_scaled_tower_competing_vacua.py`.

## 5. Smallest useful doublon prototype: exact eight-site C8 and 36-state quantum dynamics

A W33 Levi apartment is an elementary **eight-link, eight-site bipartite cycle C8**. Take the true attractive Bose-Hubbard model of **two bosons on eight sites**, with an exact Fock space of `8*9/2=36` states. This is a physically distinct minimum graph from the full 80-site/160-link machine; it has exactly one native Wilson plaquette and an accessible nontrivial doublon spectrum.

Project onto its eight on-site pair states. The exact second-order numerator is `K=P H_hop(1-P)H_hop P=4I_8+2 A_C8`, giving **five bands** with multiplicities `1,2,2,2,1`, local integrated weights `1/8,2/8,2/8,2/8,1/8`, and normalized gaps `0,1,2+√2,3+2√2,4+2√2`.

These ratios deliberately **differ** from full-W33's `0,1,4/(4−√6), (4+√6)/(4−√6),8/(4−√6)`, and full-W33 local weights `[1,24,30,24,1]/80`. A successful eight-site experiment tests attractive two-boson interactions, loading, coherent return spectroscopy and calibration; **it cannot by itself confirm full-W33 geometry**.

Full 36D exact bosonic diagonalization at `U/t=8,16,32,64` gives first-pair-gap/t `0.132176,0.0711932,0.0363494,0.0182728`, converging to leading `(2/U)(2−√2)` for t=1. Starting in a site-localized doublon, leakage probability out of the bound band decreases `5.50%,1.51%,0.387%,0.0974%` across these couplings. A hypothetical `t/h=5MHz` supplies concrete but **assumed**, not measured, Fourier times and first gaps.

Proposed experiment: tune eight bosonic sites to ring connectivity with attractive onsite U; independently calibrate t,U; prepare |2_i>; record time-resolved doublon return and pair coincidences; resolve the five groups and leakage; test U/t scaling; independently measure coherence, loss, frequency/connection disorders. The model does not demonstrate a hardware implementation.

Relevant research context (the following are external precedents, **not W33 experiment evidence**):
- Attractive Bose-Hubbard simulation proposal with superconducting resonators: [Phys. Rev. X 3, 031009 (2013)](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.3.031009).
- Interacting photon-pair dynamics in a topolectrical emulator: [Nature Communications 11, 1457 (2020)](https://www.nature.com/articles/s41467-020-14994-7).
- Superconducting circuit Bose-Hubbard flat-band simulator study: [Phys. Rev. B 93, 054116 (2016)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.93.054116).

Reproducer: `analysis/w33_20261009_toe26_c8_doublon_prototype.py`.

## Evaluation and evidence limits

Strongest new constructive result: **native `[[160,1,8]]_3` CSS code** with weight-four X and weight-eight Z checks and globally established minimum distance. A separate q=2 compact computational family supports a wider finite-geometry pattern, but no scalable threshold. Further results mostly tighten no-go boundaries: no Steinberg81 constituent for the concrete `6+3` SU9 E8 embedding; E6 frame charge not protected by unbroken symplectic symmetry; and stable scaled-q attraction requires model choices. Minimal C8 is a **computed** hardware stepping stone.

No physical theory of everything, Standard Model mass/coupling prediction, Lorentzian gravity, device realization, or finite-temperature topological phase has been demonstrated.

Seven Python research producers, seven machine-readable JSON certificates, and `tests/test_w33_20261009_toe26_five_fronts.py` supply reproducible evidence. The structural CSS distance proof is documented separately from independent numerical MILP results.
