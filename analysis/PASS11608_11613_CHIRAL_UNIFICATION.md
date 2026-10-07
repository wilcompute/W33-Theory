# Passes 11608â€“11613 â€” six-front chiral unification packet

Reservation: `ef3f76825` (Sage track).

This packet executes all five follow-ups named after Pass11607 and adds a sixth anomaly-closure pass. The claims are exact algebra/finite-operator statements unless explicitly marked as a physical boundary.

## 11608 â€” exact local decoupling of the penalized internal Weyl block

Let the external positive kinetic operator be any `K_ext` acting on spacetime and let the Spin(10) internal chirality be `Chi`. At a Hesse vacuum `W=s(15/343)rho^6`, Pass11607 gaps `Chi=s` and leaves `Chi=-s`.

For any positive penalty `Delta`,

`H = K_ext tensor I_32 + Delta I_ext tensor P_gapped`,
`P_gapped=(I+s Chi)/2`.

Because the two factors act on different tensor components, the decomposition is exact:

- light block: `K_ext`, multiplicity16;
- heavy block: `K_ext+Delta`, multiplicity16.

Thus
`det(H+mu^2)=det(K_ext+mu^2)^16 det(K_ext+mu^2+Delta)^16`,
the projected light Green function is exactly independent of `Delta`, and the heavy resolvent is suppressed by the added gap. The term is onsite in the external coordinate, so it introduces no new spacetime hopping.

This applies in particular to a positive/squared operator built from Pass11602's newly published local matched-metric covariant Dirac: the external site/spin operator and the Spin(10) internal selector act on separate tensor factors. It does **not** construct the chiral fermion measure.

## 11609 â€” the same Hesse sign selects one whole E8 matter shell

The physical external-A2 center owner gives

`248 = 86 + 81 + 81`

with center eigenvalues `1, omega, omega^2` on
`(78,1)+(1,8)`, `(27,3)`, and `(27bar,3bar)`.

Define

`C=(U-U^dagger)/(i sqrt3)`,
`M=C^2`.

Then `C` has exact spectrum `0,+1,-1`; `M` has `0,1,1`. The physical CP operation is antiunitary and exchanges the two conjugate 81-dimensional grade spaces. Writing that swap as `S`, `K_CP=S o complex-conjugation` gives `K_CP C K_CP^-1=-C` exactly; bare entrywise conjugation of the real diagonal `C` does not.

The polynomial filter

`H_shell=lambda[(15/343)rho^6 M + W C]^2`

therefore leaves the 86-dimensional gauge block untouched. At
`W=s(15/343)rho^6`, the matter shell `C=-s` is an exact kernel while `C=s` gets the same coefficient `4 lambda (15/343)^2 rho^12`.

Crucially, Pass11607 also leaves internal `Chi=-s`. Hence one CP-vacuum bit can choose both signs compatibly. This is an `E6 x SU(3)_ext` shell selector, not an unbroken-E8 invariant mass.

## 11610 â€” the Hesse domain wall has a no-go, and a minimal repair

The naive interface Hamiltonian

`H=-i alpha d_x + m(x) Chi`

does **not** have a Jackiw-Rebbi bulk gap because `Chi` acts only on the internal factor and commutes with `alpha`. In each internal sector the asymptotic spectrum is

`E=s m0 +/- k`,

so zero energy is crossed in the bulk. No protected topological wall index follows from `W(x)Chi` alone.

The minimal repair does **not** require inventing a new matrix. Pass11557's native rank-four Clifford grade `Gamma_*=Z tensor I2` obeys `Gamma_*^2=I` and anticommutes with all three spatial gammas; Pass11602 already uses the same grade in its covariant Wilson regulator and notes that it commutes with Spin transport. Thus use

`H=-i gamma_n d_x + Gamma_* m(x) Chi`.

Now the bulk spectrum is `+/-sqrt(k^2+m0^2)`. For
`m(x)=m0 tanh(x/xi)`, the exact zero-mode envelope is

`f(x)=cosh(x/xi)^(-m0 xi)`.

For internal `Chi=s`, the normalizable mode has `sigma_y=s`. Before selection there is one mode for each internal chirality; after an independent shell/Weyl selector removes one sector, one interface mode remains.

The anticommuting matrix channel is therefore already native. What is still not derived is why the Hesse order parameter couples physically through `Gamma_* Chi`, together with the Lorentzian regulator and anomaly-inflow completion.

## 11611 â€” canonical CP witness sign locks to the selected Weyl sign

Pass11600 supplied real Higgs directions
`h_u=(1,2,4)`, `h_d=(3,1,2)`
and an exact nonzero weak-basis invariant
`J=Im Tr([H_u,H_d]^3)`.

At the canonical Hesse ray
`m=(1,2,3)/sqrt14`,

`W=+15/343`, while the exact `J<0`.

The CP-conjugate vacuum flips both signs. Pass11607 keeps
`Chi=-sign(W)`. Therefore on this exact CP-conjugate pair,

`selected Chi = sign(J)`.

This is a genuine sign weld between the CP-breaking vacuum, the weak-basis CP witness, and the selected internal chirality.

The parallel Pass11606 result strengthens it. Its positive finite-family potential dynamically selects an unequal `(1,2,3)` family alignment and its exact seesaw branch has
`Im Tr[H_e,H_nu]^3=-94163140688/5625<0`.
For its canonical Hesse field `u=(sqrt(2/3),-i/sqrt3)`, the same tetrahedral map gives
`W=256/(2187 sqrt3)>0`.
Pass11607 therefore again keeps `Chi=-1=sign(J_nu)`. The family alignment is no longer merely supplied, although gauge-breaking directions, Yukawa ratios/scales and the Hesse target selecting this CP orbit remain inputs; this is still not a measured CKM/PMNS prediction.

## 11612 â€” every polynomial chirality portal contains W

The exact `W(D3) ~= S4` signed-permutation action was projected on homogeneous Bloch polynomials through degree12.

For every degree `d`, the sign-isotypic dimension equals the ordinary invariant dimension at degree `d-6`. Every computed anti-invariant polynomial divides exactly by

`W=(x^2-y^2)(y^2-z^2)(z^2-x^2)`

and the quotient is invariant.

Thus, on this polynomial Hesse sector,

`anti-invariants = W * invariants`.

Equivalently,

`H_anti(t)=t^6/[(1-t^2)(1-t^3)(1-t^4)]`.

So exact diagonal reflection symmetry forbids every lower-degree polynomial `Chi` portal: loops respecting the symmetry may renormalize `W Chi` or produce `W*invariant*Chi`, but cannot generate a degree<6 Bloch anti-invariant.

This is structural protection of the **absence of lower-degree portals**, not a calculation of the `W Chi` coefficient. Pass11605 independently removes the common scalar U1 Goldstone with its G6 holomorphic `H4` completion while preserving W and the 11607 kernel on all96 vectors. It explicitly does not suppress the lower CP-even `p3,p4` angular terms, so the two protections are complementary. Those angular terms can still move the scalar vacuum.

## 11613 â€” anomaly price of selecting one E8 shell

If the external family `SU(3)` is gauged, one Weyl `(27,3)` shell contributes cubic family anomaly

`A=27`.

For an `SU(3)` irrep `(p,q)`, normalized by `A(3)=1`,

`A(p,q)=dim(p,q)(p-q)(p+2q+3)(2p+q+3)/60`.

The conjugate decuplet `10bar=(0,3)` was already identified as the anomaly repair in the repo's 2026-10-01 chiral-decuplet certificate; this pass does not rediscover it. It has exactly

`dim=10`, `A=-27`, `T=15/2`.

Hence

`(27,3) + (1,10bar)`

has zero continuous family-`SU(3)` cubic anomaly and total Weyl dimension91.

An exhaustive additive search over all nontrivial `SU(3)` irreps of dimension below10 finds no spectator content of total dimension at most9 with anomaly `-27`. So the **new result here is the minimality certificate**: one `10bar` is minimal by total spectator dimension in this inventory.

This does not generate its mass or prove discrete `Delta(54)` anomaly freedom after family-symmetry breaking.

## Integrated picture

The strongest exact synthesis now available is:

`H_external tensor [Hesse-selected E8 matter shell / compatible Spin10 Weyl sign]`

with the following additions and boundaries.

The same Hesse vacuum sign controls the E8 shell bit and internal Weyl bit; the supplied CP witness flips with the same vacuum and has the sign of the surviving internal chirality on the canonical CP pair; exact diagonal reflection symmetry makes `W` the mandatory factor of every polynomial chirality portal; an onsite positive penalty decouples the unwanted internal block without adding external nonlocality; a topological domain wall requires an additional spacetime matrix anticommuting with the kinetic operator; and a gauged continuous family `SU(3)` needs the minimal `10bar` anomaly spectator.

This is a significant closure of the *algebraic chirality-selection chain*. It is not a Theory of Everything. A Lorentzian local fermion measure, full anomaly inflow/cancellation, dynamical Higgs/spectator masses, measured CKM/PMNS data, RG thresholds, continuum gravity, vacuum energy and absolute scale remain open.
