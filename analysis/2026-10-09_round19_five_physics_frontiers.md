# Round 19 — one-photon local selector, genuine cycle topology, and five physics stress tests

**9 October 2026.** Follow-up to Round17-18 on `wilcompute/W33-Theory/master`.
The prior 150-page `papers/forty_points/main.pdf` was extracted and assessed
in Round17. This report analyses exact native geometry, a deliberately assumed
gauge action, restricted quantum Gaussian vacua, a frozen Z6-II benchmark,
and a hypothetical optical experiment. It does **not** derive gravity,
Standard Model dynamics, a working photonic computer, or a TOE.

## I. Main new theorem: eighth-order *single-photon* local return beats global spectroscopy

The native W33 Levi graph has 40 point, 40 line vertices, 160 edges,
valency four, and girth eight. Five PSp orbit representatives are
`[0,52,68], [0,52,72], [0,52,70], [0,52,74], [0,52,90]`.
They were certified **globally one-particle-isospectral** for Peierls phases
in prior Round14. With external rational unit phasors
`(15+8i)/17,(4-3i)/5,(5+12i)/13`, define one-body Hermitian A.

Compute `L_n(A)=sort_x((A^n)_{xx})` on the **physically specified 80-site
basis**. This is a permutation-invariant collection of local vertex
spectral moments, NOT a unitarily invariant full-spectrum quantity.
At **both** p=1000003 and p=1000033:
- L_0,L_2,L_4,L_6 are identical for all five configurations;
- **L_8 has five distinct values as a full sorted 80-tuple**.
A nonzero modular difference of rational entries is a valid exact
inequality over Q(i). As in Round17, the second algebra F_p[i] is split,
not a field, but remains a valid ring for certifying nonzero residues.

The sixth-order tree identities, independent of the inserted phasors:
`(A^2)_{xx}=4; (A^4)_{xx}=28; (A^6)_{xx}=232`.
For the noninteracting two-boson doublon projected return
`G_n(x,y)=<xx|dGamma(A)^n|yy>`, the diagonal eighth order obeys exactly
`G_8(x,x)=2(A^8)_{xx}+2*binom(8,2)*4*232+binom(8,4)*28^2`
`             =2(A^8)_{xx}+106848.`
Thus the local doublon n=8 witness is **already a single-photon local
walk witness**. No interactions and no 3240-dimensional spectroscopy are
required to resolve these FIVE specific engineered selectors. This is
**not** equivalent to the global Tr A^8 (which is identical across
orbits). It also does not prove a physical choice of selector orbit.

For finite laboratory-like readout in a *mathematical simulation*,
numerically compute `U(t)=exp(-itA)` and sort the 80 local survival
probabilities `|U_xx(t)|^2`.
For the **original** Round16 phases `[.49,-.74,1.22]` at t=2,
the minimum among all ten pairwise histogram L-infinity gaps is
**0.0019966438298684164**; rational phases give
**0.0019917746368658673**. Worst numerical unitarity residual is
below `5e-14`. At t=.25 the gaps are ~1e-9. No finite-shot noise,
fabrication tolerances, detector efficiencies, or exact physical
measurement intervals were certified. All phases externally chosen.
Prior work on quantum walks lifting cospectrality:
D. Emms, S. Severini, R. Wilson, E. Hancock,
*Pattern Recognition* 42 (2009) 1988-2002, DOI 10.1016/j.patcog.2008.10.025.
Do not present this general principle as new.

## II. Native 160-link gauge theory: rank 81 and a *global frustration obstruction*

The 1620 native simple eight-cycles were explicitly enumerated by
their 160-edge signed incidence vectors `C`. The exact row ranks are

`rank_F2(C mod 2)=rank_F3(C mod 3)=81=E-V+1.`

This fills the entire real/rational cycle space too: since every signed
row is a cycle, rank_Q<=81, and rank_F3=81 implies rank_Q>=81.
On a connected graph, node-gradient gauge redundancy has dimension
`V-1=79`. Accordingly, the unfrustrated classical compact U(1)
gauge action `S=-g sum_c cos((Ctheta)_c)` has small-fluctuation
Hessian `g C^T C`: 81 nonzero modes and exactly 79 gauge zero modes.
These counts are exact **finite graph** facts, not 3+1 gauge fields.

Crucial negative discovery: native cycles with indices **(0,1,81)**
share exactly four edges pairwise and satisfy a sign relation
`-F_0+F_1-F_81=0` under the recorded orientation. They are the three
eight-cycle loops of a theta graph formed from three four-link
paths between two opposite vertices.

Consequently the previously suggested *frustrated* action
`S=+g sum_c cos(2F_c)`, g>0, **cannot** attain
`cos(2F_c)=-1` for every plaquette. For the 3-cycle theta,
`sum_{j=1}^3 cos(2F_j) >= -3/2` (tight),
rather than the naive unconstrained -3. Hence at least **1.5g**
of penalty in those three plaquettes is unavoidable.
This invalidates any inference from the Round18 one-edge
`81g cos(2phi)` double well to a globally satisfiable 1620-plaquette
chiral minimum. **Frustrated local flux and global gauge consistency
are separate problems.** No global minimizer was obtained.

One legitimate quantum gauge Hamiltonian proposal is
`H=(E/2)sum_e(-i d/dtheta_e)^2+g sum_c cos(2(Ctheta)_c)`
on 160 U(1) rotor angles modulo the 79 node gauge modes.
We did **not** diagonalize this infinite-dimensional full problem.
Instead a **two-variable toy theta reduction**
`H_theta=(E/2)(-d_x²-d_y²)+g[cos2x+cos2y+cos2(x+y)]`
at E=0.5,g=1 was diagonalized with Fourier cutoffs
4,6,8: lowest energies
`-0.59918343,-0.59939127,-0.59939191`, and positive
first gaps `0.08790,0.08617,0.08616`.
The lowest eigenvector in each truncation has inversion
absolute overlap ~1. Its arbitrary two-flux kinetic metric is
**not** a projection-derived kinetic metric of the 160-link theory.
This establishes a controlled *toy* obstruction and finite rotor
calculation, not a physical chiral vacuum or thermodynamic limit.

## III. Quantum vacuum: test a stronger would-be symmetry-broken coherent state

Pass11769 constructed a stable positive interacting 78-coordinate
quantized W33 current-square Hamiltonian `sum J_e²` and the
centered complex-Gaussian trial with energy about **128.887391415527**.
Round18's squeezed *star-centered real* trial improved a much worse
bound to **229.06536**, still inferior to the centered complex state.

Now use the **better complex** covariance
`C=t*C0`, quantum phase `F=f*diag(s)` from Pass11769, with
coherent displacements `qmean=s_q*q_star`,
`pmean=s_p*p_star`; optimize all four parameters
(s_q,s_p,log(t),f) at W33 stars 0,1,40,41.
The correct nonzero-mean Wick energy per incidence is
`[(X+a)^2+vx][(Y+a)^2+vy]+4(X+a)(Y+a)c+2c²`.
All sampled stars return **128.887391415527**, with optimal
star displacements numerically indistinguishable from zero.
An explicitly calculated 2x2 Hessian for those displacements
at the centered optimum is positive definite.

**Negative result with content:** in this 4-parameter restricted family,
pushing the already best centered complex Gaussian toward any sampled
classical zero-current star fails to lower the variational energy.
This is not an exact spectral lower bound or a proof against all
inhomogeneous, fully squeezed, or non-Gaussian states. The prior
non-Gaussian Ritz state remains an even better upper bound.

## IV. Heterotic Z6-II: 90 necessary couplings, no new non-Abelian cull

The frozen 176-state **Z6-II** benchmark is independent of the
concurrently added **Z6-I** 33-model Pass11810-11815 results.
Round18 found 424 exact nine-U1 neutral cubic monomials with
repetition; 90 pass the corrected-R and non-R filters.
Round19 explicitly screened those 90 via four non-Abelian invariant
representation channels SU3_colour, SU2_L, SU4_hidden, SU2_hidden:
**all 90 survive** the existence-of-tensor-invariant necessary masks.
This is an informative negative: group-representation existence
does **not** supply the missing worldsheet coupling amplitudes.
Potential vanishing from repeated identical bosonic chiral superfields
and antisymmetric contractions remains an additional issue.

The newer parallel W33 Pass11810-11815 work instead studies a
different Z6-I Standard Model family: an epsilon-only
untwisted up Yukawa, a top/charm degeneracy, and hidden-composite
channels at higher order. Its correction that orbifolder
`AddCoupling` omits the R rule must not be silently applied
as the Z6-II field-specific cubic amplitude.
Inputs still absent from the frozen Z6-II schema: constructing
elements, picture-changing and oscillator polarizations, gamma
actions, worldsheet instantons/moduli. The corrected H-momentum
rules and extra local selection rules matter; consult
Buchmuller et al. *Nucl Phys B* 785 (2007), 149-209 and recent
rule-4 refinement in Phys Rev D 2026, DOI 10.1103/p6p2-46s1.
**No actual nonzero worldsheet coupling or F/D-flat vacuum was
computed here.**

## V. Blocked-optics randomization repairs one confound, not every confound

Round18 proved a rank-four no-go for signal and leakage both
proportional to the same phase command `r`.
Randomly and independently operate a physical blocked/unblocked
optical path `b in {0,1}`, alongside phase command `r`,
electronics sham `e`, detector swap `d`. In the synthetic model

`y = beta_opt*(r*b)+beta_wire*r+beta_sham*e+beta_swap*d+noise.`

Design matrix `[1,r*b,r,e,d]` has **full rank five**.
For a 4096-shot synthetic dataset, ordinary least squares
recovered `beta_opt=0.0800300, beta_wire=0.0499894`
from true `0.08,0.05`. This is a valid conditional
**identifiability repair**, not a statistical power or hardware proof.

The counterexample remains exact: if a stray electronics effect
also follows `r*b` (block-correlated leakage), scenarios
(beta_opt,beta_block_leak)=(.08,0) and (0,.08) produce
**bit-for-bit identical** outcomes under the same random noise.
Physical blocked-light injection, reference path, independent
actuators, and calibrated leakage controls are still required.
The whole demonstration is synthetic.

## Reproduction and research integrity

Producers:
`analysis/w33_20261009_round19_onephoton_local_eighth.py`,
`analysis/w33_20261009_round19_local_doublon_probe.py`,
`analysis/w33_20261009_round19_finite_time_onephoton_readout.py`,
`analysis/w33_20261009_round19_gauge_cycle_frustration.py`,
`analysis/w33_20261009_round19_theta_quantum_rotor.py`,
`analysis/w33_20261009_round19_vacuum_displaced_complex_gaussian.py`,
`analysis/w33_20261009_round19_heterotic_nonabelian_cubic.py`,
`analysis/w33_20261009_round19_blocked_optics_design.py`.

Focused regression: `pytest -q tests/test_w33_20261009_round19_five_frontiers.py`.
All certificates are generated from native source definitions, not made-up
physics parameters. Graph invariants and modular inequalities are exact
within explicitly specified rational phase settings; Fourier truncation,
Gaussian minimization, finite-time evolution, and photonic regression
are **numeric or synthetic**. Git commits from other agents must be
merged without overwriting unrelated local modifications.
