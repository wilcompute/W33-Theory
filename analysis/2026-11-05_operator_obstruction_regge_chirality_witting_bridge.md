# 2026-11-05 — Five TOE Frontiers: Operators, Mobile Matter, Nonlinear Regge, Optical Memory, Chiral Index

**Status:** Executed toy-model calculations with explicit falsifiers, reproducible code, numeric certificates and direct tests. These are **not** a complete Theory of Everything, not experimental data and not an empirical derivation of the Standard Model.

Previous baseline: master commit `79c6320030b3f0c8b3a042c4c9843b1da8ff5d82`; source papers `papers/forty_points/main.pdf`, prior S3 Hamiltonian `analysis/toe_20261105_s3_nonabelian_matter_gauge.py`, ququart/Witting rays `tools/bt1408_witting_contextual_communication_bridge.py`, optical four-port compiler and reset-memory producer. The prior exact 27-state dimension and 4D linearized Ward result are **not** repeated as new discoveries.

## Front 1 — Exact, *conditional* obstruction to the 27 ↔ H27 three-qutrit identification

For the **specific** two-loop S3 gauge Hamiltonian with two fixed 2D matter doublets, the existing rank-27 physical space supports an involution S swapping the two loop holonomies **and** their matter doublets. S is gauge invariant and commutes with all three existing electric, magnetic and matter operators E/M/C.

Burnside character calculation on the 144D raw space gives

\[
\operatorname{Tr}(P_G S)=\frac{1}{6}
  \sum_{h\in S_3}|C_{S_3}(h^2)|\chi_2(h^2)
=\frac{12+3(12)+2(-3)}6=7.
\]

Thus the 27D physical Hilbert space has the exact parity split

\[
\mathcal H_{27}=\mathcal H_+\oplus\mathcal H_-,
\qquad \dim\mathcal H_+=17,\quad\dim\mathcal H_-=10.
\]

The certificate verifies \([S,E]=[S,M]=[S,C]=0\), \(S^2=I\),
trace=7, and parity-resolved physical spectra. This is an **exact
non-scalar commutant witness**: the specific exchange-invariant
operator family cannot generate the full associative
\(\mathrm{Mat}_{27}(\mathbb C)\).

**Important nonclaim:** This says nothing against an abstract isomorphism
of Hilbert spaces, a different 27D unitary representation of order-27
H27, a regular H27 address action, or an enlarged operator family. The
ordinary H27 group of order 27 does not itself have a 27D irreducible
representation; an irreducible *three-qutrit Pauli/Weyl algebra* is a
different mathematical object.

**Additional counter-control:** A gauge-invariant electric coupling
difference \(D=E_1-E_2\) is odd under exchange,
\(SDS=-D\), and gives a nonzero even-to-odd intersector coupling.
So the obstruction is conditional on the symmetric Hamiltonian and
can be removed at the level of this particular parity. This **does not
prove** the enlarged algebra is full \(\mathrm{Mat}_{27}\).

## Front 2 — Propagating matter on a small non-Abelian graph changes 27 to 18

A two-vertex graph with three parallel directed S3 gauge links has a
tree-gauge-fixed representation with two independent loop holonomies.
Place **one mobile colour-doublet excitation**, occupying either vertex,
in \(\mathbf2\oplus\mathbf2\), instead of the previous two
distinguishable fixed matter species \(\mathbf2\otimes\mathbf2\).

Raw unfixed Hilbert dimension \(6^3\times4=864\). After fixing the
spanning tree, the dimension is \(6^2\times4=144\), and the physical
gauge projector rank equals

\[
\frac{144 +3\cdot0+2(-18)}6=18.
\]

This also agrees with direct two-vertex \(S_3^2\) Burnside counting.
The gauge-fixed Hamiltonian has electric holonomy class shifts,
magnetic plaquette-commutator potential and non-Abelian hopping
\(-t\bigl(\begin{smallmatrix}0&D(g)\\D(g)^T&0\end{smallmatrix}\bigr)\),
averaged over three edges (including the gauge-fixed reference edge).
It commutes with residual local gauge action, and has physical
spectrum and noncommuting kinetic and transport terms. A 4-point
parameter scan explicitly verifies ground-state Gauss constraints.

The 27 coincidence is **not universal** under changing the matter
Hilbert-space representation. Two vertices and three parallel edges
are still a tiny finite multigraph—not 3+1D moving relativistic matter.

## Front 3 — Genuinely nonlinear 4D Regge–Schläfli action

Triangulate a closed topological 4-sphere as the boundary of the
six-vertex 5-simplex. This is 6 four-simplices, 20 triangle hinges,
15 independently variable edge lengths. For a flat-simplex
Regge action,

\[
S_R(l)=\sum_{t=1}^{20}A_t(l)
   [2\pi-\sum_{\sigma\supset t}\theta_{\sigma t}(l)],
\]

calculate simplex volumes from edge Gram determinants, dihedral
angles from the inverse Cayley–Menger matrix, and hinge areas from
Heron's formula. The equilateral interior dihedral is
\(\theta=\arccos(1/4)\), deficit
\(2\pi-3\arccos(1/4)\), and total 4-volume
\(6\sqrt5/96=\sqrt5/16\).

Add a cosmological term \(S=S_R-2\Lambda V_4\).
At unit edge length the stationary cosmological coefficient is
\(\Lambda=S_R/(4V_4)\approx36.0781891\).
The numerical gradient agrees with the Schläfli identity
\(\partial S_R/\partial l_e
=\sum_{t\supset e}\delta_t\partial A_t/\partial l_e\)
to the reported tolerance. Finite-difference 15×15 Hessian
has eigenvalue clusters with multiplicities **1+5+9** under
the edge permutation action of \(S_6\):

- one negative *uniform-scale* eigenvalue near -5.378218,
- five positive eigenvalues near +5.106393,
- nine positive eigenvalues near +13.002221.

There are **no** zero Hessian modes on this small curved Euclidean
stationary triangulation; this explicitly fails to inherit the four
flat linearized continuum Einstein gauge-zero directions
demonstrated earlier. Curved Regge discretizations do not retain
continuum diffeomorphism gauge symmetry exactly at finite mesh.

**Boundary:** Not Lorentzian Regge, no convergent refinement family,
no quantization, no demonstrated GR constraint algebra, Newton
constant or physical stability (the uniform scale is negative).

## Front 4 — Product Witting readout for an embedded *qutrit* memory Bell witness

The 40 Witting rays \(P_i=|r_i\rangle\langle r_i|\) form a complex
projective 2-design in \(\mathbb C^4\). Their normalized POVM is
\(E_i=P_i/10\), with the exact linear-inversion dual

\[
\rho=\sum_i p_i(5P_i-I_4).
\]

Embed the reference–system maximally entangled qutrit into two
four-mode Hilbert spaces using \(|\Phi_3\rangle=\sum_{a=0}^2|aa\rangle/\sqrt3\).
From 40×40 **local product** outcomes, use weights

\[
w_{ij}=\langle\Phi_3|
 [(5P_i-I_4)\otimes(5P_j-I_4)]
|\Phi_3\rangle
\]

to estimate \(F=\langle\Phi_3|\rho|\Phi_3\rangle\) **unbiasedly**.
The full 1600-outcome distribution is calculated for
\(\rho=p|\Phi_3\rangle\langle\Phi_3|
+(1-p)I_{3\otimes3}/9\), and numerically
reproduces \(F=(1+8p)/9\) to machine precision.

At \(p=.35\) and independent \(\eta_A=\eta_B=.85\),
coincidence efficiency is .7225. Use
\(Y=w_{ij}/.7225\) on coincidences and \(Y=0\)
otherwise: \(\mathbb E Y=F\) only when detection is outcome/state
independent and independently calibrated.

- The dual weights range approximately from -2.3333 to +6.
- For the alternative p=.35, loss-rescaled single-pair estimator
  variance is approximately 2.70495.
- A conservative Hoeffding bound sufficient for a 1%-false-positive,
  95%-power test against separability gives **155,076 input pairs**.
- As a clearly distinct *ideal* global entangling Bell-projector
  benchmark with the same target fidelities and perfect detection,
  an exact binomial rule requires **472 trials**.

These sample numbers should **not** be interpreted as a fair head-to-head
hardware efficiency measurement: the first is distribution-free
conservative, the second is tight for a known ideal alternative.
No deterministically implementable complete two-photon Bell projection
with passive four-port optics is assumed. A local POVM measurement is
informationally complete but statistically noisy, and outcomes or
detector settings must not be postselected based on the witness.

## Front 5 — A genuine overlap chiral index, with a regulator-sign obstruction

As a controlled step beyond 1D SSH paired edge modes, construct
a 2D toroidal U(1) lattice with uniform integer flux
\(Q\in\{-2,-1,0,1,2\}\), sites \(L=4,6,8\).
Build the gamma5-Hermitian Wilson Dirac matrix with
\(m\in\{1,2.5\}\), then define
\[
D_{\rm ov}=I+\gamma_5\,\operatorname{sgn}(H_W),
\quad
\operatorname{index}D_{\rm ov}
=-\frac12\operatorname{Tr}\operatorname{sgn}(H_W).
\]

30 combinations are diagonalized; the link-plaquette flux matches the
integer \(Q\), eigenvalue gaps remain nonzero, and selected explicit
overlap matrices satisfy the Ginsparg–Wilson chiral relation
\(\gamma_5D+D\gamma_5=D\gamma_5D\).

With this coordinate/orientation convention:
- in branch \(m=1\), index \(=-Q\);
- in branch \(m=2.5\), index \(=+Q\).

This is a **known** topological overlap-index mechanism and follows
Kurokawa–Fujiwara, the 2026 lattice-index K-theory treatment and the
lattice-GW literature. It provides a concrete obstruction to claiming
that quantum geometry alone selects a definite observed chirality:
the flux sign and regulator mass branch are separate inputs.
It is 2D, not a chiral anomaly-free 3+1D Standard Model vacuum.

## Cross-disciplinary consequences and additional independent tests

1. **Representation obstruction before dimension numerology.**
   Match the *full covariant operator algebra*, centralizer and
   irreducible sector structure, not a repeated number 27.
2. **Regulator and background dependence.**
   A topological index is robust inside a gapped sector but its sign
   can change when the regulator branch is deliberately changed.
   A genuine vacuum selector must dynamically choose the phase.
3. **Operational measurement penalty.**
   An informationally complete symmetric POVM need not be
   statistically efficient for one specific entanglement witness.
4. **Curved-versus-flat gauge consistency.**
   Exact linearized Ward identities need a nonlinear refinement
   programme; a finite Regge curved stationary point can have
   no Hessian gauge nullspace.

These are falsification opportunities, not proven novel laws of nature.

## Reproduction

Run from W33-Theory repo root:

```powershell
python analysis/toe_20261105_s3_exchange_mobile_obstruction.py
python analysis/toe_20261105_regge_s4_nonlinear_hessian.py
python analysis/toe_20261105_witting_memory_dual_frame.py
python analysis/toe_20261105_overlap_flux_chirality_index.py
python -m pytest -q --noconftest tests/test_toe_20261105_nextfive_deeper.py
```

Four machine-readable JSON records under `data/` use corresponding
names `toe_20261105_s3_27_exchange_mobile_no_go.json`,
`toe_20261105_nonlinear_4d_regge_curved_hessian.json`,
`toe_20261105_witting_qutrit_memory_product_dual.json`,
`toe_20261105_overlap_dirac_2d_chirality_index.json`.

No independent, unrelated files on the primary Windows checkout
are staged, reset or overwritten. An attempted newly named worktree
could not finish owing to low disk free space; the Git client removed
its incomplete creation, and work was carried out in the existing
clean `C:\Repos\TOE-Next5-20261105` research worktree.

## References and provenance

- Original local prior-model code paths above; consult exact
  repository history before claiming any component is novel.
- Regge action and gradient identity (existing treatment):
  https://docs.rs/phyz-regge/latest/phyz_regge/regge/index.html
- Lattice Wilson–Dirac index and K-theory, 2026:
  https://doi.org/10.1007/s11005-026-02080-w
- Uniform-flux Wilson-Dirac index:
  https://doi.org/10.1103/PhysRevD.67.025015
- Overlap fermions and Ginsparg–Wilson relation:
  https://academic.oup.com/ptep/article/2012/1/01A106/1557500

**Explicit boundaries:** No full TOE, no physical Higgs/flavour
vacuum selector, no uniquely reconstructed spacetime from W33,
no measurable Newton constant, no manufactured optics and no
new published mathematical theorem are established here.
