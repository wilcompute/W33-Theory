# Pass 12340: causal response, quantum geometry and a finite-momentum gauge zero

## Result and ownership

For the existing free spinless 27-site, 135-edge cell, the four harmonic flux
probes have an exact common response tensor at **every complex frequency**
in the retarded upper half-plane. Its nonzero-frequency response is reproduced
by four scalar harmonic coordinates, with precisely specified parameters.
Thus matching this response to the harmonic graph metric cannot, by itself,
identify a Maxwell photon or a spacetime metric. This is an explicit control
model, not a no-go theorem against all possible W33 dynamics.

The geometry, spectrum, current-block identities, low-frequency electric
coefficient, thermal static jump and cover-gap obstruction belong to
`analysis/w33_20261027_acoustic_density_backreaction.py` and
`analysis/2026-10-27_acoustic_vacuum_density.md` (commit `c12f80458`).
The present packet completes that response causally, resolves its spectral
weights, and supplies a minimal auxiliary realization and Slater-state metric.
Kubo response, the Kohn formula, sum rules and oscillator realizations are
standard methods; no novelty for those methods is claimed. See
[Watanabe, Liu and Oshikawa, 2020](https://arxiv.org/abs/2004.04561),
especially their equations 3, 4 and the linear sum-rule discussion. Their
vector-potential sign convention differs; ours is fixed below.

Producer: `analysis/w33_pass12340_causal_harmonic_response.py`.
Certificate: `data/w33_pass12340_causal_harmonic_response.json`.
Independent controls: `tests/test_w33_pass12340_causal_harmonic_response.py`.

## Derivation

Set the nearest-edge hopping amplitude, charge and hbar to one. No spatial
volume or physical time normalization is supplied. Let h be the exact
harmonic edge representative of the four integral periods and M=h^T h:

```
10   5  -6   0
 5  10   0  -6
-6   0  12  -6
 0  -6  -6  12
```

M has determinant 2916 and an exact positive LDL diagonal
`10,15/2,36/5,27/5`. The one-particle Hamiltonian K has energies
`-10,-1,5` with multiplicities `1,20,6`. Its exact polynomial spectral
projectors are

P_g=ones(27)/27,
P_m=-(K+10I)(K-5I)/54,
P_p=(K+10I)(K+I)/90.

For Hermitian current vertices J_i, all four-by-four tensors
Tr(P_a J_i P_b J_j) equal c_ab M_ij. The only nonzero coefficients are
c_mm=5/3 and c_mp=c_pm=1/6. The ground orbital is dark to all four currents.
The diamagnetic contact coefficients Tr(P_a d_i d_j K)/M_ij are
`2/27,4/27,-2/9`. These identities are rechecked exactly from the graph;
the prior JSON is not used as a proof premise.

Write f_g=f(-10), f_m=f(-1), f_p=f(5), d=f_m-f_p, and
C=(2f_g+4f_m-6f_p)/27. For Im z>0 the full retarded kernel is

**K_R(z)=[C-2d/(36-z^2)] M.**

Only the -1 to 5 transitions contribute to the retarded commutator. Exactly
degenerate matrix elements contribute to the thermodynamic derivative but
not this retarded commutator. The Euclidean continuation is

K_E(nu)=[C-2d/(36+nu^2)] M,

and its collisionless zero-frequency limit is
R0 M, R0=(4f_g+5f_m-9f_p)/54.

The time-domain distribution is causal:

K_R(t)=M[C delta(t)-(d/3) theta(t) sin(6t)].

The existing electric coefficient d/648 is the nu^2 Taylor coefficient of
this exact expression. The energy 6 is the supplied hopping-model shell
separation, not a measured photon frequency or a new physical constant.

At T>0 the equilibrium grand-potential Hessian instead equals

K_iso=[R0-5f_m(1-f_m)/(3T)] M.

This separately defined static value is not obtained by silently substituting
z=0 into the retarded response. A direct second difference of the Peierls
grand potential checks the difference at T=1/4, mu=-1, where K_iso is negative
while R0 is positive. No relaxation mechanism or relaxation rate is assumed.

## Spectral weight and sum rule

With Fourier convention exp(-i omega t), E=-dA/dt and induced current
j=-K_R A, define the formal flux conductivity sigma(z)=i K_R(z)/z.
There is no spatial-volume normalization, so this is not a measured bulk
conductivity. As a distribution on the real frequency axis,

Re sigma(omega)/(pi M) = R0 delta(omega)
  + (d/36)[delta(omega-6)+delta(omega+6)].

The notation means scalar coefficients multiplying M. For Gibbs populations,
d>=0 and R0>=0: every directional spectral measure is nonnegative. The
full-line sum is exactly pi C M. The poles and this identity are verified
symbolically, rather than inferred from a broadened numerical plot.

At T=0, -1<mu<5, all 21 lower orbitals are filled. Then C=2/9,
R0=1/6, and each finite-frequency delta has coefficient 1/36. Thus 3/4 of
the integrated weight lies at zero frequency and 1/4 at the two optical
deltas combined. A finite single-particle gap does not remove the cell's
flux stiffness. This does not establish a nonzero thermodynamic Drude weight:
the volume limit and normalization have not been constructed. The existing
exact obstruction to a global 21-band gap on the nearest-edge cover stands.

## A constructive identifiability control

For d>0, introduce four real harmonic coordinates with Euclidean inverse
kernel Q(nu)=(36+nu^2)M/(2d), coupling M to the four external probes, and
contact C M. Eliminating the coordinates gives the Schur complement

C M - M Q(nu)^(-1) M = [C-2d/(36+nu^2)] M.

The construction is a positive-mass harmonic system, with frequency 6 in
each coordinate. An exact LDL decomposition transforms it into independent
oscillators. Fewer than four scalar oscillator coordinates cannot reproduce
the rank-four residue d M/6 at the positive-frequency pole. At d=0 the
resonant part vanishes and no oscillator is needed. Parameters depend on
the chosen populations; this is not a state-independent equivalence of
the original fermion theory, all temperatures or higher correlators. It
also does not reproduce the separate equilibrium static degeneracy term.

**Physical implication:** these four collisionless quadratic probes alone
cannot distinguish the fermion cell from this supplied oscillator response.
They therefore cannot certify emergent gauge propagation. Discriminating
tests need spatial momentum, additional operators, nonlinear response or
a defined scaling limit. This conclusion follows from an explicit map,
not from failure to find a continuum interpretation.

## Quantum geometry of the occupied state

At the filled-21 ground state and zero holonomy the occupied projector is
P_occ=P_g+P_m. Its derivatives are

d_i P_occ=-(P_m J_i P_p+P_p J_i P_m)/6.

The Slater determinant's Fubini-Study metric is
g_ij=Tr(d_i P_occ d_j P_occ)/2=M_ij/216, and its Berry curvature
i Tr(P_occ[d_i P_occ,d_j P_occ]) is exactly zero. An independent test
diagonalizes genuinely phase-perturbed Hamiltonians and compares the
determinants of occupied-wavefunction overlaps. The metric is three times
the previously owned electric Taylor coefficient; that ratio follows from
one common transition gap. This is parameter-space quantum geometry at
one point, not a global band invariant or a gravitational metric.

## Validation and reading boundary

### Parallel finite-momentum test: an exact extra magnetic mode

While this packet was being computed, commit
`9baf04f1752fec07d95f6d6fa0dedf44a116f9e5` added
`analysis/2026-10-28_three_mixed_loop_minimal_maxwell.md` and its producer,
certificate and tests. Its complete patch was read and its three tests pass
on this server. It owns the rank-three endpoint factorization
H(-2)=R^T K R and its leading common-cone/generic-rank certificates.

An independent exact finite-momentum test answers one of its stated open
questions. At the nonidentity Bloch character

**z=(omega,omega,1,1), omega^2+omega+1=0**, the exact ranks are:

| Matrix | Rank over Q(omega) |
|---|---:|
| Selected short faces | 105 |
| Short faces plus three mixed channels | 107 |
| Short faces plus all six commutators | 108 |
| Vertex gradient | 27 |

There are 135 edge amplitudes. Therefore the three-mixed action has
135-107-27=**one complex nongauge magnetic zero mode** there, while the
six-loop action has none. Conjugation gives the partner character. These
characters occur on a period-three cover; they are not the constant
harmonic modes at zero momentum.

Every entry is represented exactly as a+b omega. Multiplication is lifted
to the faithful rational block [[a,-b],[b,a-b]], so rational ranks are twice
the displayed field ranks. An explicit 135-edge coefficient-pair vector is
stored in `data/w33_pass12340_mixed_loop_exception.json`. Its norm squared
is 19641258. Exact arithmetic verifies mixed-curl(v)=0, gradient^dagger(v)=0,
and six-curl(v) !=0. Thus the mode is not a gauge artefact or a small singular
value misclassified by a numerical tolerance. A fourth-root modular grid
had missed this exception, illustrating why generic specializations cannot
settle all-momentum behavior.

Producer: `analysis/w33_pass12340_mixed_loop_exception.py`.
Three tests: `tests/test_w33_pass12340_mixed_loop_exception.py`.
This resolves a finite-k boundary; it does not retract the parallel packet's
correct leading-cone or generic-rank identities. The zero is a magnetic
flat direction, not a demonstrated negative mode or an observed particle.

The subsequent parallel commit `686188ce06cb8580179eda56cc917d22965d53d0`
was also read in full before publication. Its all16 order-two-corner checks
explicitly leave other momenta open; our order-three character supplies
an exception outside that checked set. Its reflection/endpoint exchange,
compact-sector and charge-trace results are separate and are preserved.
All five of its repository tests passed here, bringing the focused validation
total to22 passing tests (17 original packet/prior controls plus these5).

### A supplied positive repair that preserves the leading cone

Let L6(z) be the six actual commutator rows. Add the 24 compact harmonics

epsilon sum_(mu=0..3,ab=0..5) [1-cos(f_ab(x+e_mu)-f_ab(x))], epsilon>0.

Each angle is the difference of two gauge-invariant Wilson-loop phases.
Their quadratic symbol is

epsilon w(z) L6(z)^dagger L6(z), w(z)=sum_mu |z_mu-1|^2.

For every nonidentity unitary character, w(z)>0. Positivity then makes the
improved magnetic Hessian's kernel exactly ker(short) intersect ker(L6), the kernel
of the six-loop completion. At identity all six commutator rows vanish,
which is checked directly from their chains; kernel equality holds there
as well. Since L6(k)=O(k) and w(k)=O(k^2), the added term starts at O(k^4),
so the existing O(k^2) common cone is unchanged. At the explicit exception
w=6 and the stored normalized quadratic cost for epsilon=1/1000 is
exactly 49/7800>0. This is a constructive lattice improvement,
with a supplied coefficient and extra loop costs. It does not derive a
selection principle, prove minimal hardware complexity, or settle whether
the six-loop model has additional exceptional characters elsewhere.

### Checks and intake status

The producer passes exact rational projector/current/contact/metric checks.
Thirty independent dense Lehmann evaluations across six T,mu choices and
five upper-half-plane frequencies agree to at most 1.90e-13. Seven tests
also cover the actual Peierls free-energy Hessian, a time-domain Laplace
integral, pole residues, the sum rule, exact oscillator block determinants,
a second period basis, a vertex-gauge transform and occupied-state fidelity.

The snapshot head is `41b1bb2434034af141500087308cd6084cbe4f10`.
The frozen two-week window is 2026-10-14 22:00 UTC through
2026-10-28 22:00 UTC. It contains 729 master-reachable commits.
`analysis/2026-10-28_two_week_patch_manifest.json` records full patch
archival sizes and hashes; archival is explicitly **not semantic reading**.
All 210 PDF pages were extracted. The frozen current PDF is identified in
the companion manifest by SHA256. This continuation read all text on pages1-19
and135-139, additional selected fragments, and visually inspected page132. It has
**not completed every page and every historical diff**. No complete-reading
claim, inherited review flag or completed-TOE claim is made.

The live epilogue's broad phrase about closed Scherk-Schwarz routes needs
to be read with Section7's distinction between supersymmetric parents and
the later non-SUSY left-right lineage. The latter's winding projections and
full string potential remain open. The 17 three-doublet parent leads from
Pass12338 are necessary-condition leads, not certified SM vacua. We leave
the paper unchanged here because this packet does not revalidate the full
string census.

A separate exact convention mismatch appears on page16: Section3 defines
P_u=X^(u1) Z^(u2) but uses the positive determinant commutation phase.
With ZX=omega XZ, that printed definition gives
P_u P_uprime=omega^(-[u,uprime]) P_uprime P_u. The quoted compiler instead
implements P_u=Z^(u1) X^(u2), for which its positive sign is correct.
Already at u=(1,0), uprime=(0,1), XZ=omega^(-1)ZX distinguishes them.
Using the compiler's stated order in the text would fix the mismatch;
alternatively every displayed commutator exponent must be negated.
The vanishing-pairing graph and dimension counts are unaffected. Signed
phase/clock interpretations require their own convention audit; this note
does not silently transfer the compiler's result to the printed convention.

The connected workstation was offline. Calculations here ran on the server.
GitKraken and Continuity MCP/CLI were unavailable; publication uses the
GitHub connector, archival reuses the repo's existing local fallback, and
the manual session decisions are recorded in
`analysis/2026-10-28_pass12340_decisions.jsonl`.

Reproduce the pinned intake with
`python analysis/w33_20261028_two_week_intake.py`; the metadata catalogue
contains every frozen SHA and complete commit message. This archives the
patches and preserves the explicit unfinished-reading boundary.
