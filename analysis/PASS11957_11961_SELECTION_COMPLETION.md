# Passes11957–11961: an enhancement pole, gauged operator quality, real lepton repair and the geometry selection deficit

Codex track, 12 October2026. Reservation `f5c5150cc` pushed before computation.
All five requested investigations were executed, including several extensions
after a first construction failed. These are **separate declared models**, not
one complete W33 action or a solved TOE. Their coefficients and scales still
need an origin in a common physical vacuum.

Producers:
`analysis/w33_pass11957_11959_color_threshold_and_cp_quality.py` and
`analysis/w33_pass11960_11961_clebsch_and_shared_cone.py`.
Matching JSON certificates are in `data/`.
Independent regressions: `tests/test_w33_pass11957_11961_selection_completion.py`.

## Prior work checked

Fetched and reviewed parallel catalogue commit `ac77e01b6`, then pulled it with
GitKraken. It updates the formula inventory to include the preceding packet;
it contains no new scientific producer. Result searches covered threshold
signs/enhancement, gauged Z12/E6 charges, portal sources, real Clebsches and
geometry/constraint coefficients. Relevant paper/index material and the
following prior source/report results were revisited:

-11950: the cubic determinant divisor and required gauge pole.
-11952: ordinary analytic chiral thresholds have the opposite sign.
-11953/11958 precursor: native matter-parity gate and the explicit quartic leak.
-11954: actual neutral-scalar loop and equal-portal control.
-11955: shared vectorlike-kernel charged-mass equality.
-11956: exact positive local kinetic-cone root and invertible six-edge Jacobian.
-11910/11942/11943: prior Georgi–Jarlskog/Wilson lepton splitting, including
  the correction that the Wilson result is a band rather than a sharp prediction.
-11320–11324 and11335–11341: prior flavour/portal running and native nonlinear
  gravity/lapse failures. Their different RG models are not replaced here.
-TOE21: dimensional scale freedom;11301: finite pointwise Leibniz obstruction.

Generic SUSY threshold matching, discrete protection, Georgi–Jarlskog and ADM
closure are **established prior art**. No new generic theorem is claimed for
them. The contribution is the explicit completion maps, counterexamples and
controls below. Corpus searches are bounded, not an exhaustive novelty proof.

##11957: build the required pole with color enhancement

Ordinary chiral fields alone cannot cancel11950's order3 zero. Higgsing an
enlarged color gauge group changes the sign. In a declared supersymmetric
SU5_color model, use two independent fundamental/antifundamental Higgs pairs,
and one additional flavor of holomorphic mass m. The sequence is

`SU5_color -> SU4_color -> SU3_color -> SU3_color`.

With n light spectator flavors, its beta coefficients are
`12-n,10-n,8-n,9-n`. Holomorphic scale matching gives

\[
\Lambda_3^{9-n}=\frac{m\Lambda_5^{12-n}}{v_1^2v_2^2},\qquad
\frac{q_{IR}}{q_{UV}}=\frac{m/\mu}{(v_1/\mu)^2(v_2/\mu)^2}.
\]

Take `v1=v2=v0 z`, `m=m0 z`. Then **q_IR/q_UV is proportional to z^-3**,
and `f_IR=f_UV+3 log(z)/(8pi²)+regular`, exactly the local pole11950 needs.
The minimal nonnegative integer balance is `3-2 n_Higgs+n_chiral=0`,
with `n_Higgs=2,n_chiral=1`.

The actual compact stabilizer is checked: two VEV directions in a fundamental5
leave an8-dimensional SU3 Lie kernel and16 broken vectors. The first rank test
incorrectly complexified Hermitian-generator coefficients and computed a
parabolic stabilizer; stacked real/imaginary constraints corrected that error
before publication. Equal holomorphic Q and Qtilde phases produce mesons z²
while their physical D moments cancel.

An explicit multiplier superpotential imposes `Qtilde_i Q_j=v0² z² delta_ij`
for the first two flavors; the third has mass m0z. Its stated classical home
has F=D=W=0. This is a **color parent**, not ordinary SM SU5 unification, nor
an embedding in the stored E6/string vacuum. Perturbative threshold matching
requires Higgs/mass scales above the strong scale; it cannot be extrapolated
through z=0. Nonperturbative vacuum dynamics can lift classical branches.

This resolves the **local sign/order construction problem**, not the full
strong-CP phase: the regular coefficient of the light determinant and the
global genus-two modular law are still uncomputed. Standard matching is from
[Intriligator–Seiberg,hep-th/9509066](https://arxiv.org/abs/hep-th/9509066),
section4.1; it is cited rather than rediscovered.

##11958: explicit gauged suppression, with the spectator and soft loopholes included

Start from11953's family-twisted E6 pairs and add a continuous U1Z. The inventory
is E6×U1X×U1Z with the following (X,Z) charges:

| fields | multiplicity | (X,Z) |
|---|---:|---:|
|27A,bar27A|one pair|(+1,0),(-1,0)|
|27B,bar27B|two pairs|(-1,0),(+1,+1)|
|27C,bar27C|two pairs|(-1,-1),(+1,0)|
|P|one|(0,+1)|
|three constraint multipliers|three|(0,-1)|
|two singlet spectators|two|(0,+1)|
|PhiMinus,PhiPlus|one pair|(0,-12),(0,+12)|

Neutral high-scale multipliers contribute no anomalies. All **eight** continuous
E6²X/E6²Z, gravitational, cubic and mixed Abelian anomaly sums vanish exactly.
Phi± break U1Z to gauged Z12; low P and T condensates subsequently break it.
S and T retain the11953 family parity making their16/bar16 backgrounds even.
The desired `d(27_native,27A,27B)` mixing and real `mu27Abar27A` remain allowed.

In cutoff units choose `P=rho Lambda`, `S=(v,i v)`, `T=(v,-i v)` with
`v²=rho Lambda²`. Replace the earlier constant v² by LambdaP and add

\[
W_{high}=R(\Phi_-\Phi_+-\Lambda^2)
 +U(\Phi_-P^{12}/\Lambda^{11}-f^2).
\]

All multipliers vanish at the stated F=D=W=0 home. With
`d=(2rho+rho²)/12`, the exact high-field squared norms are
`u_minus=(sqrt(d²+4)+d)/2`, `u_plus=(sqrt(d²+4)-d)/2`.
Their product is1 and their difference cancels the low U1Z D term. The input
f² is chosen for this branch; rho is **not derived**.

### Exact singlet stability and its important limitation

There are seven charged complex VEV variables and five holomorphic constraints.
A nonzero constraint minor is `-144 P^11 PhiMinus² v³`; the rank is5.
Its two complex kernels are precisely the two gauge directions. The positive
rank-two moment-map Gram lifts their radial partners. Two additional spectator
masses `PhiMinus P^10/Lambda^10` are exactly nonzero. Therefore the canonical-K
singlet Hessian has **26 positive physical real directions and two gauge phases**.
Other E6 components are outside this proof.

Positivity does not mean soft robustness. A neutral-U fluctuation gives the
Rayleigh upper bound

\[
m_{min}/\Lambda\le\sqrt{2[(12\sqrt{u_-}\rho^{11})^2+\rho^{24}]}.
\]

At the supplied `rho=1/32`, `Lambda=10^16 GeV`, some physical singlet is no
heavier than **4.71653 GeV**. Generic TeV soft terms therefore cannot be treated
as small perturbations. Sequestering or a different stabilization must be
computed; a tree-stable branch is not a viable softly broken vacuum by itself.

### Polynomial suppression and the inverse-spurion counterexample

The unwanted QHdDc has (X,Z)=(-1,0). For a condensate monomial
`T^a S^b P^c PhiMinus^d PhiPlus^e`, neutrality requires
`a-b=1`, `a+c=12(d-e)`. Its rho exponent is
`(a+b)/2+c=a+c-1/2 >=23/2`.
Thus the first analytic upper-block dressing is **rho^(23/2)**; first complex
light-mass or mu corrections are orderrho^12.

But charge counting was not enough. Without another tag,
`Lambda27Bbar27C+P27Cbar27C` is allowed and induces
`27C=-Lambda27B/P`. This negative-charge condensate destroys that branch and
the polynomial bound. The audit found this before publication.

Add an **unbroken spectator Z2**, with C and barC odd and every other field
even. All ordinary mixed anomaly coefficients are even. Every spectator
vertex is then at least quadratic: there is no linear source, C=barC=0 is
the tree solution, and perturbative SUSY superpotential nonrenormalization
does not generate inverse-P light vertices. Nonperturbative and soft effects
are not covered by this statement.

The two massive full C pairs have total color threshold index12, so their
mass phase is `arg(P^12)`, real in the PhiMinus-real gauge on the selected
F-flat branch. Anomaly cancellation has therefore not silently introduced
a new tree determinant phase.

### Compute the soft leakage instead of claiming all-order strong CP

The allowed Kähler term `P† T QHdDc/Lambda³` gives an upper Yukawa of order
`(m_soft/Lambda)rho^(3/2)` if F_P is of orderm_softP.
The negative-Z constraint multipliers can also acquire VEVs. At fixed moduli,
their exact response to F0 is

\[
X=\frac{F_0}{2\Lambda(1+\rho)},\quad
Y=\frac{F_0}{4\Lambda(1+\rho)},\quad Z=0.
\]

Their permitted `X T QHdDc/Lambda²` and Y counterpart add leakage of the
same parametric order as the Kähler term. Using the **actual11951 quark-fit
inverse matrix**, the linear sensitivity is `||B m^-1/mu||`; the full4×4
determinant independently verifies it. Supplied rho1/32, soft/cutoff10^-13
and unit coefficients give a combined example envelope **1.7791×10^-12**.
This is not a bound on every Wilson coefficient or the total theta of the
full theory. The light-mode gate means the fixed-modulus soft response itself
needs justification. Gluino phases, vacuum shifts and full E6 masses remain open.

Discrete/SUSY-breaking protection is known prior art. A distinct model in
[Evans et al.,2002.04204](https://arxiv.org/abs/2002.04204) uses different
discrete/R and mediation rules. Its assumptions are not imported as proof
for this inventory.

##11959: equal portals are not protected by the actual fermion box

For the11954 non-SUSY benchmark, the two real singlet-Yukawa rows r,t have
equal norm, but the Higgs mass matrix breaks that apparent alignment:

\[
F=\begin{pmatrix}r\\t\end{pmatrix}m^Tm(r^T,t^T)
 =\begin{pmatrix}1/200&7/2500\\7/2500&49/10000\end{pmatrix}.
\]

The exact mixed term in `Tr[(M†M)²]` is `2h² S†F S`. Its one-loop CW scale
derivative sources a portal matrix with unequal diagonals and a nonzero
offdiagonal even when the tree portals are equal. This is the **fermion-box
source**, not the entire beta function with scalar/gauge/wavefunction terms.

Then vary the CP-scalar VEV/mass while holding B,mu and the light tree matrix
fixed, reducing scalar Yukawas as1/vCP. The actual neutral-scalar loop is

|vCP in reference units|delta theta|
|---:|---:|
|1|−2.78216×10^-6|
|10|−1.45858×10^-7|
|100|−2.90527×10^-9|
|1000|−4.36318×10^-11|

This demonstrates a controlled suppression route for **that contribution**,
without erasing the tree weak-CP matrix. It does not derive vCP, prove an RG
fixed trajectory, or calculate the softly broken supersymmetric theory above.

##11960: real Clebsches repair charged masses; two more real neutrino directions suffice

SU5 tracelessness of the45-Higgs tensor gives three equal color entries t
and weak entry−3t. The factor−3 is established Georgi–Jarlskog prior art.
With the11951 shared positive kernel A and supplied real quark matrix m,
take only two diagonal real45 coefficients:

`Y45=diag(c1,c2,0)`, `Y5=m-Y45`,
`Md=m A`, `Me=A^T(m-4Y45)^T`.

The quark fit stays exactly fixed. Two fitted real coefficients reproduce
the repo's two charged-lepton ratios. The finite one22-coefficient scan fails
within its locked interval; it is not a global exclusion. Three coefficient
solutions are stored, two of which give the same charged left Gram after a
real electron-sign change.

The positive **diagonal** bare Majorana ansatz still fails the four supplied
neutrino comparators in finite multistart. Instead of ending there, add real
12 and13 entries while fixing n23=0. Its positivity is enforced by a real
correlation disk. Four real parameters then fit all four angle/splitting
comparators with residuals below10^-12. Takagi SVD, physical mass ordering
and consistent Weyl charged rotations are used.

The CP phase is not fitted. The stored roots give conditional delta values
about **79.385°,247.424°,302.508°**, with nonzero J. **Multiple branches prevent
a unique phase prediction.** This establishes compatibility of a real bare
neutrino sector with the inherited quark mixing kernel; it is not a
parameter-free W33 prediction or a selected observed vacuum.

The45-Higgs input also brings colored partners and proton/gauge constraints;
these are not solved by a charged-mass fit. See the distinct model of
[Haba et al.,2402.15124](https://arxiv.org/abs/2402.15124).
The earlier Wilson-line band and11946's specified mu–tau-clean exclusion
remain valid on their original assumptions.

##11961: the shared cone constrains an ADM class, but leaves154 native directions

For a declared continuum Maxwell Hamiltonian with electric/magnetic
coefficients alpha,beta, an explicit transverse periodic-field calculation
gives `{H[N],H[M]}=alpha beta D[q^-1(NdM-MdN)]`.
The11956 cone has alpha=2,beta=1 in its supplied units.

In the local ADM-class ansatz

`Hg=a/sqrt(q)(pi_ij pi^ij-lambda pi²)-b sqrt(q)R+c sqrt(q)`,

an exact flat-slice calculation gives the usual momentum term abD plus
`2ab(2lambda-1) integral pi(N DeltaM-M DeltaN)`.
A divergence-free pi22=cosx has nonconstant trace and a nonzero obstruction
unless **lambda=1/2**. Sharing the normal-deformation bracket with the matter
cone then requires **ab=alpha beta=2**. The separate a and cosmological
coefficient c remain free. This is a necessary calculation in the stated
continuum class; standard ADM completion is prior art, not a native lattice
gravity derivation. References:
[Hojman–Kuchař–Teitelboim](https://inspirehep.net/literature/113155),
[Anderson,gr-qc/0511070](https://arxiv.org/abs/gr-qc/0511070).

The native deficit is sharper than “we need weight dynamics.” The160 link
weights map to six independent entries of the Gauss-reduced kinetic form G.
The11956 invertible six-edge minor and its contraction bound make this a
local submersion. Therefore **the isotropic level set has dimension154**.
A supplied selector `V=sum_six(G-I/2)²` has Hessian `2J^T J`, rank6 and154
zero directions at the root. It cannot select a unique microscopic geometry.
Those are algebraic weight directions, **not154 derived gravitons**.

Native electric/magnetic geometry, its continuum limit, the nonlinear
constraint algebra, quantum closure and physical Newton/CC constants are
still unbuilt. Existing finite Leibniz/lapse obstructions are not repealed
by this conditional continuum exercise.

## Verification and independent next targets

The first41-control replay had40PASS and one symbolic-test assumption error:
Cbar was wrongly assumed nonzero despite its zero solution. That assumption
was corrected without changing a physical certificate. Final local and
exact-SHA hosted results are recorded in the publication receipt.

Five independent next investigations:

1. Embed the color-enhancement pole in a genuine genus-two/E6 spectrum and derive its global phase.
2. Calculate mediation/sequestering or alternative stabilization for the light quality singlet, rather than assuming soft robustness.
3. Derive the real Clebsch and Majorana texture coefficients from native invariant dynamics instead of fitting them.
4. Select or falsify the distinct lepton CP branches with a common scalar vacuum and additional observables.
5. Supply dynamics for the154 microscopic kinetic directions and both electric/magnetic geometry, then test native gravitational closure.
