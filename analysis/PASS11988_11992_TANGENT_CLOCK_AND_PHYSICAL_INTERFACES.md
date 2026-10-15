# Passes11988–11992: exact tangent and clock bridges, explicit physical-model interfaces

Reservation `94857ee9e` preceded computation and was pushed after integrating
the simultaneous TOE85 commit. All five requested investigations were executed.
Several useful constructions emerged, but the requested full physical flavour
vacuum, native interacting chiral continuum and nonlinear W33-derived GR remain
open. No result below changes the physical badges in the forty-points paper.

## 11988 — the correct six-space is a projective tangent, not wedge2

Use the **same actual Pauli labels** on both sides. At W33 point
`p0=(0,0,0,1)`, all13 perpendicular transvections fix the point and its opposite
27-shell. Their literal permutations preserve11983's six-dimensional local
E6 projector. Separately, restrict the explicit two-qutrit zero-character
projectors and their transvection gates to11663's odd Weil4. All52 conjugations
on the canonical Pauli generators are checked exactly over Q(omega).

The tempting wedge2 identification fails. For `v=(0,1,0,0)`:

```
atlas6 characteristic polynomial: (x-1)^4 (x^2+x+1), trace3
wedge2(odd Weil4):                (x^2+x+1)^3,       trace-3
```

The full intertwiner equations have36 unknowns and rank36 independently
modulo1009 and1021, with rank progression18,32,36. Thus their characteristic-zero
Hom is zero. The unequal eigenvalue multiplicities also exclude a scalar
projective identification for this element. This is a statement about these
labelled actions, not every possible outer twist or group homomorphism.

**Continue after the failed map.** The reference Witting ray is odd basis
coordinate1. If a stabilizer gate acts by phase chi on that ray and by U3 on
its orthogonal complement, its projective tangent action is **chi^-1 U3**.
Realify that three-dimensional Q(omega) action using z=a+omega b. The resulting
six-dimensional rational action DOES intertwine with the actual atlas6.
The complete Hom has dimension2, and one integral intertwiner is

```
S = [ 1 -1 -1 -1  0  1 ]
    [ 0 -1  0 -1  1  1 ]
    [ 0  0  0 -1 -1  1 ]
    [-1 -1  1  0  0  0 ]
    [ 2  0  0 -1  0  0 ]
    [ 1  0  0 -2  0  0 ],   det S=9.
```

Every one of the13 exact equations R_v S=S T_v is checked. The determinant
refers to the specified bases; it is not an invariant E6-lattice index or a
physical factor of nine. This supplies a named bridge between the native
atlas and the odd-Weil/Witting projective tangent.

In the atlas coordinates, multiplication by i is

```
J=(1/sqrt3) diag(K,K,K),   K=[-1 2; -2 1].
```

For the actual source-fiber Gram G, `J^2=-I` and `J^T G+GJ=0` exactly.
The finite stabilizer preserves J. The11983 polar connection does not:
the exact G-Frobenius squared commutator norms with H0,H1,H2 are8,8,8;
with the orientation-even loop H0 H1 the value is **9**.
Full SO6 holonomy cannot preserve a parallel orthogonal complex structure.
Consequently a family-three interpretation needs a connection reduction or
additional order parameter; a local complex triplet does not automatically
descend through these transports.

Prior11663 owns the odd basis, Witting rays and Pauli dictionary. Prior
`analysis/PASS11664_11671_KERNEL_DYNAMICS.md` already identifies the transverse
odd3 with an even mass-kernel3 on the Witting stabilizer. The additional map
here is to11983's actual native atlas6, including its transport obstruction.
Neither earlier construction is retracted by the distinct wedge2 failure.

## 11989 — release the CP source and retain its actual backreaction

Replace11981's pinned tau=-1 by a dynamical real field and supply the CP-even
potential `kappa(tau^2-1)^2/4`. Keep every eliminated source term and the positive
degree-eight stabilizers. The light problem now has19 real coordinates;
reinstating13 complex positive-mass mediators gives45 real coordinates.
This is a scalar mediator completion of the eliminated potential with
nonrenormalizable EFT stabilizers, not a renormalizable UV completion.

For the five prior CP branches and kappa=64,16,4,1, solve the full19-coordinate
stationarity problem. All **20 numerical local witnesses** have positive19D
and45D Hessians; the smallest45D curvature across the scan is approximately
0.00090945. The relaxed source Schur curvature is positive in every case
(minimum3.6198). Independent finite differences of the DIRECT45-field scalar
energy check a full Hessian, beyond the analytic heavy-block Schur argument.

Eighteen cases retain `|J|>1e-5`. At softer kappa=1, prior draws9 and10 become
weak-CP-small; this is a branch-following observation, not a global phase
classification. Explicit CP partners conjugate all triplets and reverse tau,
preserve energy and reverse J. The neutral source is now minimized jointly,
but this added double well is not11978's seven-condensate singlet sector.

For draw3,kappa4, connect its actual h vacuum to the **prior11951** Nelson–Barr
inverse realization. A fitted real matrix C satisfies `B=C h`; the complex
mixing row therefore conjugates under the actual scalar CP partner. Replace
the original complex Yukawa texture by the real triangular Barr architecture

```
Mfull = [ m  0 ],    det Mfull = mu det m > 0,
        [ B mu ]
```

with real positive-det m and positive mu. In the heavy-decoupling limit the
matched comparator gives J=3.08e-5, its conjugate -3.08e-5, and the supplied
down-mass ratios/CKM entries. The hierarchy and real couplings are **fitted**,
not predicted or selected by the geometry. The nonzero complex texture of
11981 is not silently kept while using the Barr determinant theorem.

A deliberate real leakage column epsilon d in the zero block gives
`d arg det M/depsilon=-Im(B m^-1 d)/mu`; the benchmark is0.16451705.
Thus the tree-level matching does not protect total strong CP. A symmetry
forbidding leakage, scalar/colored loop thresholds, the full singlet/E6 vacuum,
RG running, scale selection and a global minimum remain required.
The general E6 Nelson–Barr route is established
[Schwichtenberg–Tremper–Ziegler](https://arxiv.org/abs/1802.08109).

## 11990 — a complete computing process for the five gates

Encode11987's C4 data in the actual odd two-qutrit subspace. Use four of the
five even states as auxiliaries, leaving one spectator. For
`U=V diag(exp(i phi_j)) Vdag`, set d_j=O V_j and a_j=E_j. Follow the closed
four-plane path

```
D_j=cos(theta/2)d_j+exp(i psi_j)sin(theta/2)a_j:
meridian theta0->pi/2; longitude psi0->-2phi_j; return meridian.
```

Its geometric phase is exactly `-integral sin(theta/2)^2 dpsi_j=phi_j`.
With P the rank-four dark projector, the specified control

```
H=Delta(I-P)+i[Pdot,P]
```

obeys `Pdot=-i[H,P]` and `PHP=0`: exact dark-space transport with zero
dynamical phase. Smooth cubic ramps give explicit finite-time controls.
Full nine-level Schrodinger integration of all five gates gives maximum
encoded operator error2.77e-11; an independent adjoint-gate path is also tested.
Removing the counterdiabatic term at the short duration produces large leakage.
The full81-element two-qutrit Weyl expansion of sampled Hamiltonians is frozen.

**Use the new parallel work concretely.** TOE92's generic Givens compiler is
reused, credited, and independently reconstructed for each of the five gates.
The certificate includes chronological rail phases and at most six two-mode
rotations. This is an alternative **single-photon four-rail ququart** carrier
for the same4x4 matrices. Two virtual qubits in one photon are not an entangling
gate between independently encoded photons. The9-level path likewise assumes
arbitrary shaped two-qutrit controls, including odd/even parity mixing.
Neither is measured hardware, a scalable architecture or a noise threshold.
General holonomic/transitionless methods are prior art:
[Zanardi–Rasetti](https://arxiv.org/abs/quant-ph/9904011),
[Zhang et al.](https://arxiv.org/abs/1905.09524).

## 11991 — a native four-period cover and a precise Lorentz repair

Use the actual TOE83/85 augmented27-vertex,135-edge,99-face complex.
Its rational harmonic1-cochain kernel has dimension26. Exactly8 dimensions
are center-invariant and none are H27-fixed. Extract four distinct rational
two-dimensional linear-character planes for `(1,0),(0,1),(1,1),(1,2)`.
This representation content agrees with the earlier TOE87/88 work; the new
objects are the explicit harmonic cochains, primitive cover and regulator.

Choosing any two planes gives six possible H27-invariant rank-four quotients.
The center-faithful real irreducibles have minimum dimension6, so they cannot
supply a different four-dimensional quotient. Pick the first two planes,
gauge away a spanning tree, and compute the integer cycle-period image by HNF.
The raw normalization has index81; dividing by its actual lattice gives a
**primitive connected Z4 cover with27 sites per cell**. All99 face boundaries
close exactly in the cover. This is not an externally inserted Cartesian T4.
It remains a selected periodic graph, not a derived unique smooth spacetime.

The actual positive acoustic metric is

```
G=(1/27) [10  5 -6  0]
         [ 5 10  0 -6]
         [-6  0 12 -6]
         [ 0 -6 -6 12].
```

The single acoustic Bloch band has `lambda(k)=k^T G k+O(|k|^4)` and the
periodic-cover heat asymptotic has spectral dimension4. The quotient choice
supplies the rank; this is not dynamical selection of four dimensions.
A108-component native Wilson/overlap kernel gives actual four-direction
Dirac scaling, exact GW projectors, finite gauge-covariance controls and no
zero at the15 nonzero Brillouin corners tested. There is no uniform all-momentum
gap/locality theorem or global non-Abelian Weyl measure. Free index is zero.

**Full H27 cannot preserve a Lorentz metric on this four-space.** Its invariant
symmetric forms have dimension2 and signatures(4,0),(2,2),(0,4), never(3,1).
This is verified in both character and primitive integral deck coordinates;
HNF mixes the character lattices, so block form is not assumed in both bases.

**The parallel subgroup supplies an exact repair.** Read the actual nine
elements selected by the independent TOE84 H1 and TOE85 H2 ternary rank tests:

```
A={(0,b,c): b,c in F3}.
```

A fixes the entire real `(1,0)` character plane. An explicit Lorentz metric
and timelike vector in primitive deck coordinates are

```
eta=(1/54) [-4  1 -3  0]        u=(3,0,2,1)^T,
           [ 1  8  0 -3]        u^T eta u=-1.
           [-3  0  6 -3]
           [ 0 -3 -3  6]
```

Both the metric and vector have **exact stabilizer A** among all27 group
elements. Thus breaking H27 to the previously selected commuting subgroup
permits3+1 signature. Each of the four maximal commuting subgroups could fix
its own character plane; the code criterion picks this one for the selected
two-orbit complex. Three four-period choices contain that plane, and the
timelike line within the plane, signature, orientation and dynamical action
remain additional choices. The Lorentz metric is not the positive acoustic
diffusion metric relabeled as spacetime.

Prior11389/Oct9 own native abelian covers and subgroup-dependent dimension;
11977/11984 own earlier native/supplied-time and supplied-T4 regulators.
General harmonic-cover methods are
[Kotani–Sunada](https://doi.org/10.1090/S0002-9947-00-02632-5), and overlap
fermions are [Neuberger](https://arxiv.org/abs/hep-lat/9801031).

## 11992 — test genuine nonlinear Einstein dynamics, and reject a false shortcut

Import the known **unpolarized Gowdy T3 vacuum Einstein model** as a positive
control. The full metric, not a graph-clock analogy, is differentiated with an
independent two-jet curvature implementation. Its two canonical pairs are
the interacting P,Q gravitational-wave polarizations. The first-order lambda
constraints have exactly zero integrability defect under their nonlinear PDEs.
The periodic global momentum constraint is retained.

Sixteen independent metric jets give Ricci residuals below3e-16 while their
Kretschmann curvature is generically nonzero. Removing the nonlinear couplings
produces Ricci errors up to0.1202. A de Sitter control independently checks the
curvature convention and normalization. Evolve both polarizations at32 and64
spatial points: final-field difference2.06e-8, fine metric constraint residual
1.44e-12 and fine Ricci residual5.24e-14. This is a reproducible nonlinear GR
benchmark, not a derivation of GR, an exact finite graph constraint algebra,
or proof of full unreduced ADM/quantum closure.

There is also an exact gate on a tempting shortcut: so6 is simple, dimension15;
so(1,3) has dimension6. Every Lie homomorphism has ideal kernel and is either
injective or zero, so only zero is possible. Thus the connected SO6 atlas
holonomy cannot be pushed through a nontrivial continuous homomorphism into
four-dimensional Lorentz holonomy. Breaking the structure group, adding fields
or changing the connection is required; compact internal gauge roles survive.

Gowdy dynamics is classical prior art, explicitly credited to
[Berger–Garfinkle](https://arxiv.org/abs/gr-qc/9710102). The existing11961 ADM
necessary conditions,11976 finite scalar-bracket failure and11985 clock
construction are preserved, not silently promoted to Einstein gravity.

## Parallel intake, validation and what remains

During this turn TOE85 and then TOE86–92 arrived. The full76-file latter
inventory was reviewed, all seven narrative reports read, selected relevant
producers read in full and certificates inspected. This is **not** a claim of
manual sentence-by-sentence review of all34,091 added lines or every routing
integer. The intake manifest records every path/hash/JSON parse. TOE92's actual
compiler and TOE84/85's actual subgroup elements are used above, not inferred
from matching counts. TOE87's three-orbit counterexample prevents an overbroad
claim of universal clock selection. The newer communications/QKD results are
not imported as physical TOE evidence.

The source guard initially named the old Witting exposition, TOE45 and
11663/11664; these were read for the relevant maps and credited. The final
source guard is quiet. No general novelty claim is made for realification,
Barr matching, geometric control, graph-cover diffusion or Gowdy gravity.
The specific credited paths are `W33_FOR_EVERYONE.tex`,
`analysis/2026-10-10_toe45_cusp_tomography_parallel_research_audit.md`,
`analysis/PASS11663_ODD_WEIL_NORMAL_MAP.md` and
`analysis/PASS11664_11671_KERNEL_DYNAMICS.md`.

All five producers have JSON certificates. Independent tests check exact maps,
direct45D UV energy, quantum evolution, primitive periods, symmetry-breaking
metric examples and full4D curvature. The dedicated workflow freezes, regenerates
all five, and retests. Actual local/hosted receipts are recorded separately.
The papers remain unchanged; unrelated and parallel work is preserved.
The full local intake/interface suite passed99 tests in87.35s, including every
TOE85–92 regression module and18 new interface tests. Hosted replay is
reported only when its actual completion receipt is available.

**Still open:** a common microscopic action selecting these choices; a jointly
stable full singlet/E6/physical flavour vacuum; protected total strong CP;
global chiral measure and interacting native continuum; dynamical Lorentz
selection; nonlinear W33-derived Einstein constraints; G, Lambda and observed
parameter predictions; scalable physical quantum controls and fault tolerance.
