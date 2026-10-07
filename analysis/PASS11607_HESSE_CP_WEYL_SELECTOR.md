# Pass 11607 — the Hesse CP discriminant becomes a dynamical Weyl selector

Reservation: `7d4cdfacf` (Sage track).

This pass welds two results that were previously separate:

- Pass 11593: on the executable Spin(10) Dirac carrier, every gauge-invariant Hermitian selector lies in `span{I, Chi}`; the two-tick clock flips `Chi`.
- Pass 11600: the Hesse flavor vacuum has a real CP-odd discriminant
  `W=(x^2-y^2)(y^2-z^2)(z^2-x^2)`, and its 24 minima split into two 12-ray A4 orbits with
  `W=+15 rho^6/343` and `W=-15 rho^6/343`.

The new result is that these two odd characters cancel under a diagonal action.

## Minimal odd flavor coefficient

The exact signed-permutation realization of `W(D3) ~= S4` was enumerated on homogeneous polynomials in the Hesse Bloch coordinates. The projector onto the permutation-sign representation has dimensions

`0,0,0,0,0,0,1`

in Bloch degrees 0 through 6.

Therefore no nonzero polynomial can carry the odd `S4/A4` character below degree 6, and the degree-6 space is one-dimensional. Its generator is exactly

`W=(x^2-y^2)(y^2-z^2)(z^2-x^2)`.

Each Bloch coordinate is bilinear in the canonical Hesse doublet, so the lowest polynomial flavor coefficient capable of compensating an odd chirality selector has field degree 12.

This is a finite exact computation, not a claim that every possible nonpolynomial or multi-field UV completion has the same bound.

## Pin lift of the clock/chirality flip

Using the exact 32-dimensional Spin(10) Clifford carrier, set

`R=i Gamma_10`.

This is the already-certified two-tick clock. Exactly,

`R^2=-I`,
`R Chi R^-1=-Chi`.

For all 45 Spin(10) bivectors, conjugation by `R` stays inside the bivector algebra: the 36 bivectors not containing `Gamma_10` are fixed and the nine containing it are negated. Thus `R` is a Pin normalizer of the gauge algebra while exchanging the two 16-dimensional Weyl blocks.

Because `R^2=-I`, the lift is projective on spinors, but its adjoint action is an honest order-two automorphism.

## Diagonal cancellation

Let an even Hesse transformation act trivially on the Spin(10) carrier. Let the odd CP/reflection coset act additionally by `Ad_R`.

Then

`W -> epsilon W`,
`Chi -> epsilon Chi`,

with the same `epsilon=+-1`. Therefore

`W Chi`

is exactly invariant under the diagonal action and still commutes with the Spin(10) gauge algebra.

This is how the Pass 11593 no-go is evaded: the coefficient multiplying `Chi` is no longer a clock-even scalar. It is itself the dynamically selected odd Hesse order parameter.

## A positive polynomial filter with an exact Weyl kernel

A linear `W Chi` portal gives a chirality splitting but is not a positive projector globally. The Hesse minima provide a stronger polynomial construction because every minimum obeys

`|W|=(15/343) rho^6`.

For `lambda>0`, define

`H_gap = lambda [ (15/343) rho^6 I + W Chi ]^2`.

It is manifestly positive. At a minimum with `W=s (15/343) rho^6`, `s=+-1`,

`H_gap = 4 lambda (15/343)^2 rho^12 P_s`,
`P_s=(I+s Chi)/2`.

Hence one Weyl-16 is an exact zero-energy kernel and the conjugate Weyl-16 has exact penalty

`4 lambda (15/343)^2 rho^12`.

The 12 CP-conjugate vacua exchange the two kernels. The even A4 subgroup preserves each vacuum-sign orbit; the odd coset exchanges the orbit and the Weyl chirality together.

The linear diagonal portal has scalar-field degree 12. The manifestly positive exact-kernel square has scalar-field degree 24.

## Physical boundary

This closes a finite-carrier selector obstruction, not the entire chirality problem. The construction is an internal positive penalty/filter. It does not by itself:

- construct a Lorentzian chiral path-integral measure;
- prove perturbative or global anomaly cancellation;
- select the E8 `(27,3)` shell rather than `(27bar,3bar)`;
- derive or protect the high-dimension portal coefficient;
- prove locality or continuum decoupling of the penalized Weyl block.

Those are separate physical requirements. The important new point is narrower and exact: **the Hesse CP vacuum supplies the missing odd coefficient required by the unique Spin(10) Weyl selector, and a polynomial positive filter can make one Weyl block an exact kernel.**
