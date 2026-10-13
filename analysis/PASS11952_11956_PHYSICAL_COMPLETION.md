# Passes11952–11956: local Maxwell metric repair and the physical CP completion gates

Codex, 12 October2026. Reservation `aad262fd1` pushed before computation.
This executes all five investigations proposed after11950–11951, with additional
exact vacuum, messenger, scalar-potential, basis-covariance and nonlinear-existence
checks. It does **not** close all five physical problems or solve the TOE.

Producers:
`w33_pass11952_11955_threshold_vacuum_loop_leptons.py`,
`w33_pass11956_local_electric_metric.py`.
Certificates have the same stems in `data/`; independent controls are
`tests/test_w33_pass11952_11956_physical_completion.py`.

## Result ownership and intake

GitKraken fetch showed no new scientific commits after our11950–11951 receipt.
The prior330-commit/916-path intake remains the earlier snapshot; no claim of
complete manual review of that whole corpus is made here. The current `docs/index.html`,
Forty Points physics/ledger, new flavour reports and source dependencies were checked
in the preceding intake and revisited for the present mechanisms.

Searches covered the result index, exact expressions, CP/threshold/holomorphic,
electric-metric/impedance/local-kinetic, family-parity and E6 invariant terms.
The search for `[81,1,1]` correctly led to the earlier
`analysis/w33_20261009_canonical_triplet_isotropy_theorem.py`: it already owns the
exact Levi cycle-projector denominator160 and entry levels. Our period Gram below
is a selected principal submatrix of that prior projector, **not a new graph identity**.
TOE38 owns the native local curl complex; TOE41 owns the canonical-electric
acoustic split. Pass11950 owns the required strong-CP pole;11951 owns the real
determinant witness and inverse mass reconstruction. Pass11946's PMNS exclusion
stands on its stated mu–tau-clean charged-lepton family. No prior result is retracted.

##11952: ordinary chiral thresholds have the wrong sign for the required pole

For supersymmetric SU3 with a massive fundamental/antifundamental pair,
holomorphic scale matching gives

\[
q_{IR}=q_{UV}\det(M_{heavy}/\mu),\quad q=e^{-8\pi^2 f},\qquad
\Delta f=-\frac1{8\pi^2}\log\det(M_{heavy}/\mu).
\]

This is standard, not a new threshold formula: Intriligator–Seiberg,
[hep-th/9509066](https://arxiv.org/abs/hep-th/9509066), section4.1,
equations4.10–4.13. Positive Dynkin indices give the same zero-order sign for
other ordinary chiral representations. In the regular UV setting of11950,
the light determinant contributes order3, so heavy analytic masses with orders
`r_a>=0` yield total order `3+sum(r_a)`, never zero or a pole.

**Consequence:** counting more ordinary colored exotics cannot generate the
required `epsilon^-3` factor. It adds determinant zeros. Vector/Higgsed-gauge
thresholds, a genuinely singular UV kinetic function and an isolated selected
CP-safe vacuum remain different possibilities. No actual string threshold with
the needed coefficient has been computed. This narrows11950's threshold target;
it does not invalidate its local necessity theorem.

##11953: explicit CP vacuum without a constant FI term

Take S1,S2 of X charge−1, T1,T2 of charge+1, neutral X0,Y0,Z0,
canonical Kähler potential and real superpotential

\[
W=X_0(S_1T_1-v^2)+2Y_0(S_2T_2-v^2)
  +3Z_0(S_1T_2+S_2T_1).
\]

For v=1, the home `(S1,S2,T1,T2)=(1,i,1,-i)`, with all neutral fields zero,
has **W=F=D=0 without FI**. The gauge-invariant CP-odd quantity `Im(S1 T2)=-1`
changes sign in the conjugate home. Generic real mediator Yukawas distinguish
the two scalar flavours and transmit this phase; the actual weak-CP witness
of11951 verifies that the full scalar-plus-Yukawa theory is not merely a
gauge rephasing of a real mass matrix.

At gauge coupling1, the exact fourteen-real-coordinate Hessian eigenvalues are

\[
0,\quad4\ (\times2),\quad16\ (\times4),\quad64\ (\times2),\quad72,
\quad180,\quad288,\quad98\pm2\sqrt{1753}.
\]

The single zero is the gauged common phase; all13 physical singlet-sector
eigenvalues are positive. Arbitrary v is a supplied scale. Since W=0 and F=D=0,
canonical-K ordinary N=1 supergravity has the same local supersymmetric
Minkowski home in this sector. This is a classical zero vacuum energy in
unbroken SUSY, **not a prediction of the observed cosmological constant** or
a SUSY-breaking/Standard-Model vacuum.

### Complete E6 field inventory and the invariant that defeats the zero block

Add complete representations

`27_A(+1)+bar27_A(-1)+2[27_B(-1)+bar27_B(+1)]`

under E6×U1X. All added pairs have family-Z2 sign−1. The total matter parity is
`(-1)^Qpsi * family_Z2`. The added10 mediators are therefore odd, while the
added16 and bar16 singlet condensates are even. This differs explicitly from
11951's **native** E6 exotics and preserves that earlier obstruction.
E6²X, gravitational-X and X³ cancel within every full conjugate pair.

The mixing is the named invariant `d(27_native,27_A,27_B)`, selecting
`16_native 10_A 16_B`. Replace SiTj in W by the E6 contraction
`27_Bi dot bar27_Bj`; equal-norm conjugate-weight VEVs cancel all E6 and X D terms.
The singlet home remains F=D=W=0. Other E6 components are not stabilized by
the singlet Hessian; their masses, full stabilizer and reduction to the SM
are open. This is a complete representation inventory, not a finished vacuum.

Unfortunately E6 also allows the specific dimension-five invariant

\[
\frac1\Lambda d_{ijk}27_Q^i27_H^j d^{k\ell m}
  \overline{27}_{A,\ell}\overline{27}_{B,m}.
\]

Its nonzero SO10 channel is `(16_Q 10_H)->bar16` contracted with
`(bar10_Dc bar16_T)->16`. It contains the SU5 term
`10_Q bar5_Hd bar5_Dc singlet_T`, hence **T Q Hd Dc/Λ**.
Its Qpsi charge, X charge and total parity are all neutral.

More generally, any additive U1 or discrete charge rule with neutral
coefficients allowing `QHd dc`, `S D dc`, `D Dc` and `ST` also allows
`T QHd Dc`. Thus this ordinary conjugate-condensate completion loses the
S-only all-order zero-block selection rule of11951. This theorem is restricted
to these allowed operators and neutral coefficients; it is not a theorem
against non-Abelian flavour rules, charged spurions or geometric locality.

At SM level an explicit real, parity-compatible messenger gives
`W=Λ R Rc+QHd Rc+T1 R Dc`, yielding `-T1 QHd Dc/Λ` on elimination.
For the11951 mass witness its full5×5 determinant is
`14 Λ+6+i`. A real tree determinant therefore fails already at this allowed
operator, before invoking loops. For large dimensionless Λ, its phase is
`1/(14 Λ)+O(Λ^-2)`. No physical cutoff ratio is derived.

##11954: calculate the scalar loop rather than infer protection from the triangle

This is a **separate non-SUSY benchmark**, not the total loop correction to
the11953 supersymmetric model. The potential, field normalization, scalar
Hessian and Yukawa vertices are specified in the producer/certificate.
It is a gauge-invariant CP-real two-singlet alignment potential plus
`p_i(H²-1)(|Si|²-1)/4` and an R_xi Goldstone lift.
The home is stationary; the physical charged-scalar Hessian is positive.

With `M=U diag(m) V†` and real-scalar Yukawa vertices Gamma_a, evaluate the
neutral-scalar self-energy at zero external momentum in MSbar:

\[
\delta M=\frac1{16\pi^2}\sum_a\Gamma_a V\operatorname{diag}
[m_i B_0(0;m_i^2,s_a^2)]U^\dagger\Gamma_a,
\quad\delta\bar\theta=\operatorname{Im}\operatorname{Tr}(M^{-1}\delta M).
\]

The two real portal coefficients `(0.1,0.2)` give
**delta theta=−2.7821570777109913×10^-6**, despite a real tree determinant.
Independent Feynman-parameter quadrature checks the analytic B0 expression.
The divergent theta coefficient is exactly zero; changing the subtraction
scale leaves the first-order theta invariant. CP conjugation reverses its
sign; zero portals and equal portals cancel this particular contribution.

Near `(0.1,0.1+eta)`, the slope is about−2.77716×10^-5 per unit eta.
The supplied benchmark would need a portal difference of order a few10^-6
to reach10^-10 through this contribution alone. Equality has not been shown
to survive RG evolution. Gauge diagrams, vacuum/tadpole shifts, two loops,
soft terms and the gluino phase are not included, so no EDM-safe model is claimed.
This is the reducible portal danger anticipated in
[Valenti–Vecchi,2105.09122](https://arxiv.org/abs/2105.09122), equation7;
their restricted mediator estimates are not applied to our scalar completion.

##11955: common unified mixing transmits CP but cannot repair charged-mass equality

An added matter-parity-odd vectorlike5 pair can mix right-handed down fields
and left lepton doublets through the same positive Hermitian kernel

`K=I-B†B/(mu²+|B|²)`, `A=positive sqrt(K)`.

With one real SU5 Yukawa m,
`Md=m A`, `Me=A^T m^T=Md^T`. Therefore their singular spectra coincide
**for every B and m**, regardless of how large the induced CKM/PMNS phase is.
Common mixing alone cannot repair the unacceptable minimal-SU5 mass relation.
Real Clebsch factors/additional real Yukawa structures are needed. Unified
vectorlike mixing itself is prior art in
[Schwichtenberg–Tremper–Ziegler,1802.08109](https://arxiv.org/abs/1802.08109);
their model uses additional Yukawa structures and assumed scalar VEVs.

For real bare Majorana n the same doublet mixing gives `mnu=A^T n A`.
The explicit supplied witness has **J_PMNS≈0.0220196**, nonzero reactor
mixing and `[K,P_mu-tau]≠0`; conjugating B reverses J, and real B gives J=0.
These numbers are not an observed lepton fit. The left charged rotation uses
`Me* Me^T` in the two-component convention, and the neutrinos use Takagi
vectors of `mnu† mnu`. A unitary-basis covariance regression checks both.
This bypasses the **premise** of11946; it does not contradict or supersede its
exclusion of the specified mu–tau-clean family.

##11956: exact existence of local electric weights repairing the leading light cone

Use TOE38's original160-edge marked three-deck Levi complex,1382 zero-winding
octagons and three commutator cells. Let B0 be its gradient and V the three
chord-voltage columns. The period-one harmonic representatives are

`h=V-B0 (B0^T B0)^+ B0^T V`.

Their Gram is `[[81,1,1],[1,81,-3],[1,-3,81]]/160`, a direct use of the
prior canonical cycle projector. An exact rank78 minor and rational linear
solve establish that **every native-octagon first derivative can be cancelled
by static massive-edge relaxation**. The commutator rows have P0=0 and their
remaining derivative Gram is exactly `[k]_cross^T [k]_cross`, for all six
quadratic coefficients. No fitted magnetic tensor is substituted.

For a positive local diagonal electric kinetic matrix W=diag(w_e), Gauss
reduction gives the weighted harmonic form

\[
G(W)=V^TWV-V^TWB_0(B_0^TWB_0)^+B_0^TWV.
\]

**The first raw fit was wrong:** setting `h^T W h=I/2` on the old harmonic
basis fails the weighted Gauss projection. Full Bloch replay caught it before
publication. The final construction uses G(W), not that raw fit.

A numerical solve finds positive local w in roughly `[0.1700,1.3717]` with
G≈I/2. To turn existence into a theorem, round all160 coefficients to exact
rationals with denominator10^12, and vary six selected edges in an infinity
ball of radius10^-8. Rational graph inversion and the exact six-variable
Jacobian certify:

- inverse-Jacobian infinity norm <1000;
- Newton displacement <10^-9 and <one quarter of the ball radius;
- every second derivative of a Gram entry has absolute value≤256 on the ball;
- fixed-point contraction norm <1/10; all weights stay between1/8 and2.

Banach's theorem supplies an **exact positive root G=I/2** in that ball,
unique with the other154 coefficients fixed. The stored rational center is
an approximate implementation of that root, not the exact algebraic coefficients.
The derivative bound follows from weighted leverage≤1/min(w) and
`G_ii≤V_i^T W V_i≤2`; six rows and six variables give the stated factor36.

At the root, both transverse leading branches obey

\[
\boxed{\omega^2=2|k|^2}
\]

in **every real direction**, with no nonlocal projector in the action:

`H=sum_e E_e²/(2w_e)+||P A||²/2`, `B†E=0`.

Finite Bloch checks on three directions and three radii preserve Gauss,
retain a positive third gap and approach the double acoustic value2.
Finite-k degeneracy is not exact. This construction repairs the canonical-
electric leading birefringence by changing explicitly declared local input
coefficients; it does not refute TOE41's fixed-unit-weight result.
The marking and weight selection are supplied. No unique physical speed,
Lorentz-invariant charged matter, RG stability or spontaneous metric selection
has been derived.

### Why this is still not a gravitational action

Naively promote each w_e to a variable while retaining fixed magnetic energy
and no geometry kinetic term. Its primary constraint pi_w=0 requires
`dot pi_w=E_e²/(2w_e²)=0`, forcing the electric field to vanish.
Thus that particular promotion is inconsistent with generic electromagnetic
waves. A physical metric extension must couple electric and magnetic geometry
and supply its own dynamics/constraints.

Primary literature distinguishes metric Maxwell closure from closure for
birefringent tensor geometry:
[Düll et al.,1611.08878](https://arxiv.org/abs/1611.08878) and
[Schneider et al.,1708.03870](https://arxiv.org/abs/1708.03870).
We have not solved those closure equations for this lattice. Newton's coupling,
the cosmological constant and a continuum gravitational constraint algebra
remain open; matching a cone does not determine them.

## Validation and remaining targets

The initial30-control replay passed before the final E6 test; final results
and the exact-SHA hosted replay are recorded in the publication receipt.
The controls include exact symbols, independent scalar-loop quadrature,
random mass transposes, basis changes, exact rational contraction bounds,
walk derivatives and full gauge-reduced Bloch spectra. No11949 producer is
rerun or its quality certificate modified by this packet.

Five independent next investigations:

1. A colored vector/enhancement threshold with the required sign and global modular phase.
2. A geometric or non-Abelian rule suppressing the explicit E6 quartic leak without suppressing the desired cubic.
3. A portal-alignment/RG calculation in one complete CP sector, including vacuum shifts and SUSY breaking.
4. A shared real-Yukawa/Clebsch lepton construction that fits masses and neutrinos rather than reconstructing inputs.
5. A dynamical selection of local electric/magnetic geometry with gravitational constraint closure and a controlled continuum limit.
