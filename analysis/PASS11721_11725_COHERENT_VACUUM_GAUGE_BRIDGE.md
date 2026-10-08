# Passes 11721–11725: a coherent bridge between the Witting and chirality vacua, and an E8 adjoint route to exactly the SM algebra

The missing pieces tested here are **coherence between the Weil halves** and
**rank reduction by actual gauge-covariant Higgs fields**. These give explicit
constructions with named maps, actions and kinetic operators. They do not give
observed chiral matter, masses, couplings, spacetime or a cosmological constant.

[Producer](w33_pass11721_11725_coherent_vacuum_gauge_bridge.py),
[certificate](../data/w33_pass11721_11725_coherent_vacuum_gauge_bridge.json),
[regressions](../tests/test_w33_pass11721_11725_coherent_vacuum_gauge_bridge.py).
Reservation45f2afe2a was pushed before computation. No main-paper changes.

## What was already known, and what was read

Claude.txt was read fully (134lines/9070bytes), including its unfinished
11713–11720 family direction. Its embedded commands were context. Incoming
11680–11712 reports, code, certificates, tests and forty-points time-section
deltas were inspected; the four incoming regression suites pass23tests.
That is not a fresh full read of every historical paper or every earlier commit.
The original parallel checkout and its uncommitted work are preserved.

Prior11663 owns the literal rank1 odd/rank2 even zero-character Pauli
projectors and Maschke map;11690 owns the antilinear E8 root-ray intertwiner;
11697–11698 own the parity identity and320 stabilizer chirality vacua;
11672 owns the full-rank scalar parent and its global bound. The old
`w33_holonomy_joint_centralizer_scope.py` already owns the four-extra-U1
warning.11271 constructs a different E6 Higgs interface;11461 names native
charges and exposes a photon obstruction. None is retracted here.

Result searches included320-to40 projection,160even rays, tetrahedral Weil
projections,1304,1173600,7/30 and the1080/960 mixed-invariant coefficients,
against RESULTS_INDEX, the site, Python, Markdown and TeX. Existing count
bridges (`2026-05-29_index_guided_dirac_shell_bridge.md`), the11550 finite
Veronese tetrahedra and11074 Levi chart tetrahedra are different objects.
No blanket external novelty or priority claim is made.

The intake guard's additional broad compound candidates were read fully:
`PASS214_218_SOURCE_TORSOR_DUAL_OVOID_WEIL_SYNTHESIS.md`,
`analysis/PASS10954_REGULAR_C8_CLOCK_COMPLETION.md`,
`PASS2300_2305_FIVE_FRONTIERS_RELEASE.md`,
`analysis/BT2300_BT2305_five_frontiers.md`,
`PASS1030_EIGHTY_CARRIER_ORIENTATION_OBSTRUCTION.md` and
`analysis/BT1741_BT1744_execution_summary.md`. They own, respectively,
spread/ovoid and Weil-shadow maps, oriented C8 completion, higher-q Weil
inversion, the 80-carrier obstruction and atlas allocation. Those results
are not being claimed here. `W33_FOR_EVERYONE.tex` was result-searched and
its Witting and appended chamber/selector sections re-read; a fresh full
read of that entire exposition is not claimed. Its older physical readings
are not assumptions in these tests. The remaining guard warnings are
broad topic co-occurrences, not a certificate of novelty or duplication.

## 11721 — the literal flag projection gives 40 qubit planes with tetrahedral states

Let Pi be the actual two-qutrit Weil parity and P±=(1±Pi)/2. Every nontrivial
Lagrangian-character stabilizer state psi has equal norm in both sectors.
Define

    o=sqrt2 P- psi,  e=sqrt2 P+ psi.

The exact census over Z[omega], omega²+omega+1=0, gives:

| object | distinct projective states | preimages among320 |
|---|---:|---:|
| odd component o |40Witting rays|8each|
| even component e |160rays|2each|

The character kernel is a point p on its Lagrangian line L. Both components
lie in the zero-character space of D_p. That space is a literal qutrit:
one odd dimension plus two even dimensions. The odd component is precisely
11663's Witting ray at p. The four lines through p give four even rays in
its two-plane, with every distinct squared overlap1/3 and frame sum2Q_p.
Each set is a **qubit tetrahedral SIC**. These are overlapping two-planes
in the same even five-dimensional carrier, not 40 independent tensor
factors or a 40-ray SIC in dimension3 or4.

Thus the complete projective dictionary is

   320 =40Witting points ×4even tetrahedron vertices ×2coherent partners.

The two partners have the same parity projections and opposite relative
sign: psi=(e+o)/sqrt2, Pi psi=(e-o)/sqrt2. **Projection alone erases the sign.**
The exact certificate binds all320 projectors and flag addresses. Integer
matrix products check their ranks, parity and all40 tetrahedral Gram laws.

This also supplies a short proof: for a fixed p the odd zero-character
projector has rank1, so all eight states share that ray; two states in each
Lagrangian basis are Pi partners. States from different Lagrangians through
p have stabilizer overlap1/3. Their parity-paired amplitudes give the stated
even overlap and tight-frame relation; the exact census fixes phases and
prevents a merely numerical count identification.

## 11722 — one bounded action has both old Witting alignment and new chirality vacua

A pure odd state has S4=sum_v(Im< D_v >)^4=0. Consequently the old odd
condensate cannot itself be a maximum of the chirality potential. It can
be its odd component, using the even companion just constructed.

For every flag, with phases inherited from the original state,

    S4((e+exp(i theta)o)/sqrt2)
       =(27 cos(theta)^4+9 sin(theta)^4)/8.

The global maxima are theta=0,pi. The lower extrema at pi/2 are not the
selected vacua. No preferred physical hand is chosen: Pi still exchanges
degenerate partners.

Write O for11663's normalized9×4 odd embedding. Add a new complex9field psi
with common U1 charge1 to11672's parent fields f4,q10,z5. In the prior mass
units and with positive displayed coefficients set to1, use

    Vjoint =Vparent+23/8 +(||psi||²-1)²
           +(27/8)||psi||⁸-S4(psi)
           +||f-sqrt3 Odag psi||².

Every term after shifting the old parent is nonnegative by the prior global
theorems. Every one of the320 states has a zero: choose f=sqrt3 Odag psi,
whose norm² is3/2, transport the parent's reference minimum by an actual
canonical Weil word, and transport its symmetric matrix T accordingly.
The code constructs all320 lifts using literal matrices, rather than
postulating a common orbit. Conversely Vjoint=0 forces psi to be one of
the320 projective chirality states.

This is a **global tree theorem for a supplied degree8 EFT**. Auxiliary q
minima can remain continuous; no unique full field vacuum is asserted.
At the recorded56-real-coordinate zero the full Hessian has51positive
and5zero eigenvalues; the smallest positive value is about.0499072.
The first49/7 guess was rejected by the producer and corrected before
publication. Direct potential differences independently check the chirality
Hessian. A zero Hessian direction need not be a vacuum manifold direction.

The even companion is new. The old z5 has charge4 and cannot be mixed
directly with charge1 f as a common-charge state. The action respects the
tested common canonical Weil subgroup and U1; no untested extension to
every outside-Weil G32 reflection is asserted. This changes the field
inventory and adds irrelevant operators:11673's one-loop spectrum is not
inherited. No chiral Weyl fermions have been derived.

## 11723 — density neutrality and vector neutrality are different physical inputs

For rho=|psi><psi|-I/9, every diagonal Cartan H commutes with rho when psi
is a computational basis state. Hence the old SM-shaped clock pair retains
all five U1s even after adding this adjoint order parameter. Y psi=0 is
stronger than [Y,rho]=0.11708's six-axis enumeration and conditional
vector criterion remain valid; they do not by themselves remove four
abelian gauge fields.

The distinction also matters globally. The scalar omega I9 is trivial on
sl9+Lambda³9+dual but not on9. A fundamental9 does not descend to SU9/Z3
inside E8. A quantum state or projective ray need not be an E8 Higgs field.
The density matrix is an adjoint element, but its rank1 SU9 orbit is not
closed under the full E8 action. These are interface requirements, not a
claim that the finite quantum construction is wrong.

More sharply, a clock-invariant SM-singlet adjoint for the original pair
lies in its five-dimensional abelian center. Such adjoint vevs cannot lift
any of those U1s. A compatible enlarged clock centralizer, further matter,
or different dynamics is required.

## 11724 — an actual E8 adjoint Higgs and a compatible native Clifford clock

Use Claude's worked visible levels F={0,1,2,7,8} and remaining R={3,4,5,6}.
For i in R set E_i4 to the trivector of R minus i, and F_i=star(E_i4), with

    star(A,x,k)=(Adag,-conj(k),-conj(x)).

The positive compact invariant norm is
Tr(A dagger A)+x dagger x+k dagger k; general-trivector Ward identities
check its covariance. This explicitly chooses the compact real form, rather than conflating it
with11681's componentwise-conjugation split form. The brackets
E_ij=[E_i4,F_j], together with Cartans, give the hidden SU5'. Clearing
denominators by15 verifies **all625 matrix-unit relations exactly** with
safe integer operations. The construction is classical SU5×SU5 branching
realized in the current two-qutrit bracket, not a new exceptional subgroup.

Build the principal SU2 in that hidden SU5 with

    Jz=diag_virtual(2,1,0,-1,-2),
    J+=2E01+sqrt6 E12+sqrt6 E23+2E34.

Its centralizer in E8 is exactly the visible SU5. The full248-dimensional
adjoint Casimir C=sum ad(Ja)² has24zeros. Adding the visible adjoint
Y6=diag(-2,-2,-2,0,0,0,0,3,3) gives exactly12zeros, the literal
su3+su2+u1 algebra. The complete rational squared-mass spectrum, for equal
unit vev/gauge scales, is in the certificate. These are conditional gauge
masses of this supplied background, not measured particle masses.

There is a more economical compatible clock alternative:

    U=diag(omega,omega,omega,1,1,1,1,1,1)=omega D0.

It is the native quadratic Weil phase, a **Clifford** tick. It commutes with
all Ja, has86fixed adjoint directions and Tr_ad U=5. Its joint kinetic
operator with the Higgs is

    K=C+(AdU-I)dag(AdU-I).

Its squared eigenvalue:multiplicity list is

    0:12, 2:15, 3:12, 5:18, 6:15, 9:90, 12:35, 15:42, 20:9.

This spectrum also follows exactly from j(j+1)+3 for Y6 nonzero mod3,
and j(j+1) otherwise, using the certified spin/charge modules. Thus the
remaining four abelian fields really are absent from the kernel.
The earlier assertion about Clifford-only *tick centralizers* is untouched:
the new noncommuting adjoint Higgs is an additional resource.

A nonnegative gauge-invariant clock/Higgs action is

    Vfuzzy +sum_a||AdU Phi_a-Phi_a||²
           +||Ad(U³)-I||²+|Tr_ad U-5|²,
    Vfuzzy=sum_ab||[Phi_a,Phi_b]-i epsilon_abc Phi_c||².

On the specified principal branch the centralizer's identity component is
SU5. Enumerate its cube-root eigen-multiplicities(n0,n1,n2), sum5 and
n1+2n2=0 mod3. The target trace5 leaves **only(2,3,0) and(2,0,3)**,
both with centralizer S(U3×U2), i.e. the SM Lie algebra. This solves the
clock selection problem **conditional on the chosen conjugacy-class target
and principal branch**. The target5 and branch are supplied; they are not
selected by W33 without further dynamics. Disconnected centralizer sectors
are not classified here. In particular Phi=0 with this same U is also
a zero of the clock action: the displayed action alone does not globally
select the principal branch or the SM.

## 11725 — a derived mixed invariant selects the3+2 shape

The simpler renormalizable fuzzy-triplet plus adjoint-Sigma action

    Vren=Vfuzzy+sum_a||[Sigma,Phi_a]||²+(||Sigma||²-30)²

has a flat sphere: any Sigma in the visible su5 with norm²30 is a zero at
Phi=J. At the GG point this includes11 physical Hessian flat directions,
beyond12 gauge-orbit tangents. A positive gauge mass spectrum alone does
not make an isolated scalar vacuum.

An invariant that supplies the missing shape information is

    I(Phi,Sigma)=Tr_ad[(sum_a ad(Phi_a)²)² ad(Sigma)^4].

It is E8×SO3 invariant and has total field degree8. On the principal branch
write pk=Tr5 Sigma^k. The standard branching gives5=spin2 and
10=spin1+spin3 under the principal SU2. Therefore, **without fitting**,

    I=360 Tr10 Sigma⁴+2040 Tr5 Sigma⁴
     =1080 p2²+960 p4.

The second equality is an exact polynomial identity at Tr5 Sigma=0.
The actual248-dimensional trace at Y6 is1173600. Tests verify the identity
on general Cartan directions, not just that one point.

For a traceless Hermitian5×5 matrix,

    p4 >=(7/30)p2²,

with equality precisely on the2+3 eigenvalue orbit. A complete elementary
proof uses compactness at fixed p2 and the stationary cubic
4x³-2lambda x-nu=0. There are at most three eigenvalues. Two-value
multiplicities1+4 and2+3 give ratios13/20 and7/30. Three distinct roots
sum to zero; the only positive multiplicity partitions3+1+1 and2+2+1
force ratios1/2 and1/4. All are larger than7/30 except2+3. The classic
SU5 adjoint minimum is prior art; its mixed E8-Casimir realization is the
constructed interface tested here.

Hence I>=1304p2² on this branch. An explicitly bounded completion is

    V16=Vren+eta*(I-1304||Sigma||⁴)², eta>0.

It is globally nonnegative and has the explicit J,Y6 zero. **On the stated
principal branch**, its zeros select exactly Sigma conjugate to ±Y6.
The square starts at fourth order in the11 former physical flat directions,
so it does not give them positive quadratic masses. Other SU2 embeddings,
quantum lifting and UV completion remain open. Degree16 is an EFT choice.

A failed shortcut was checked: pure Tr_ad Sigma⁸ does not prefer GG. At
the same norm, the2+2+1 shape has23085000 against GG23727600. The mixed
Casimir insertion is essential to this particular construction.

## Physical boundary and literature

These are two supplied models: a common-Weil scalar alignment action and
an E8 adjoint/clock Higgs action. A single physical action coupling them,
an anomaly-complete chiral kinetic spectrum and observed flavor have not
been built. No Lorentzian continuum, Einstein constraints or cancellation
of a constant vacuum-energy shift is supplied by these constructions.

Fuzzy adjoint-Higgs backgrounds and their internal Casimir spectra are
established methods; see[Aschieri et al.](https://arxiv.org/html/0704.2880#S4).
Their internal matrix sphere assumes a spacetime base and does not derive
our spacetime. The standard SU5 adjoint Higgs minimum is treated in
[Buccella, Ruegg and Savoy's symmetry-breaking analysis](https://digital.library.unt.edu/ark:/67531/metadc1057512/)
and is re-proved above with all stationary multiplicity cases.
The E8 algebra alone must not be called a chiral TOE; the representation
obstacles are spelled out by[Distler and Garibaldi](https://arxiv.org/abs/0905.2658).
We add the explicit actions and operator checks above, with those limits.
