# Passes 721–725 — formal rigidity, the missing two-branch cycle module, self-calibrating optics, nonfactorizable dropout, and all-phase control

## Pass 721 — Formal rigidity and the exact local degree-two census

Pass 681 proved

\[
H^1(PSp(4,3),\operatorname{End}_{\mathbf F_2}(V))=0,
\qquad V=H_1(W(3,3);\mathbf F_2),\quad \dim V=81.
\]

That already implies **all-orders formal rigidity**: a nontrivial deformation over an Artin local ring would have a first nonzero congruence layer, and that layer would define a forbidden nonzero class in \(H^1\).

To localize the still-ambient degree-two problem, Pass 721 constructs an explicit minimal projective resolution over a verified elementary abelian subgroup

\[
E\cong(C_2)^4.
\]

The free ranks are

\[
7,\ 5,\ 10,\ 21,
\]

the syzygy dimensions are

\[
31,\ 49,\ 111,\ 225,
\]

and the induced Hom-complex differential ranks are

\[
126,\ 205,\ 505.
\]

Therefore

\[
\dim\operatorname{Ext}^0_E(V,V)=441,
\qquad
\dim\operatorname{Ext}^1_E(V,V)=74,
\qquad
\dim\operatorname{Ext}^2_E(V,V)=100.
\]

The scalar trace summand has

\[
\dim H^2(E,\mathbf F_2)=\binom{5}{2}=10,
\]

so the exact **local traceless degree-two target** has dimension

\[
\boxed{90}.
\]

These ninety classes are not promoted to global classes. Indeed, all seventy-four local degree-one classes are killed by global fusion, because the global degree-one group is zero. Since a Sylow-2 subgroup has order \(64\) and odd index \(405\), restriction from the full group to the Sylow subgroup is injective in characteristic two. The remaining numerical global \(H^2\) problem is therefore a Sylow stable-elements/Lyndon–Hochschild–Serre computation, while the actual deformation functor is already rigorously trivial.

## Pass 722 — The missing W33 two-branch correspondence module

The missing natural two-branch module exists, but it appears in an unexpected place.

Let \(Z_1\) be the integral cycle lattice of the W33 collinearity graph. It has rank

\[
201=120+81,
\]

where the saturated triangle-boundary lattice \(B_1\) has rank \(120\), and the quotient is the protected homology lattice \(H_1\) of rank \(81\).

On fundamental-cycle coordinates, the signed-turn operator \(K\) satisfies

\[
(K+6I)(K-2I)=0,
\]

and, crucially, \(K+6I\) is entrywise even. Hence

\[
S_{\rm cyc}=\frac{K+6I}{2}
\]

is an integral operator satisfying

\[
\boxed{S_{\rm cyc}(S_{\rm cyc}-4I)=0}.
\]

Thus the full cycle lattice realizes the same nodal order

\[
\mathbf Z[S]/(S(S-4))
\]

that governed the q=2/S8 deformation frontier.

In a unimodular boundary-adapted basis,

\[
S_{\rm cyc}=
\begin{pmatrix}
4I_{120}&Y\\
0&0_{81}
\end{pmatrix}.
\]

The extension block \(Y\) has rank \(67\) and Smith invariants

\[
1^{66},\ 12^1.
\]

The sum of the two saturated eigenlattices therefore has quotient

\[
\boxed{\mathbf Z_1/(L_4+L_0)\cong(\mathbf Z/4)^{66}},
\]

with index

\[
4^{66}=2^{132}.
\]

So the full W33 cycle lattice is a large, exact, highly nonsplit two-branch module, even though \(H_1\) alone is scalar-commutant rigid and one-branch. This is a q=2/S8 order on a W33 module; it does not replace the separate search for the corrected q=3 cyclotomic rank-four interface.

## Pass 723 — Self-calibrating waveform optics

The waveform falsifier is upgraded from a calibrated simulator to an identification-and-compilation loop.

Dedicated calibration packets estimate nine hardware quantities:

- actuator gain;
- ringing decay and kick;
- AR(1) phase-noise coefficient and innovation scale;
- coherent second-harmonic amplitude;
- coherent neighboring-mode leakage;
- detector recovery time;
- count-dependent dead-load coefficient.

The calibration methods are reference-interferometer step response, dark-trace spectral estimation, harmonic regression, pulse-pair recovery fitting, and count-load regression.

The fitted model selects among blocked, guarded-balanced, and alternating schedules. It selects the same guarded-balanced schedule as the hidden oracle:

\[
\boxed{\texttt{balanced\_g4}}.
\]

On an independent 500-replay hardware stream,

\[
q_{0.95}^{\rm selected}=0.0464856\ \text{rad},
\]

whereas blocked quadratures give

\[
q_{0.95}^{\rm blocked}=0.0586082\ \text{rad}.
\]

The self-compiled schedule therefore improves the worst-channel 95-percent error by

\[
\boxed{20.68\%},
\]

remains unsaturated, and preserves the original \(286\) configurations.

## Pass 724 — Nonfactorizable dropout and an anytime matrix confidence sequence

The pair-propensity factorization

\[
\pi_{ij}=gq_iq_j
\]

is removed. Instead, the exact latent model is

\[
O_i=GB_i\prod_{r:i\in S_r}L_r,
\]

with two blockwise latent factors and one sparse factor on channels \((0,1)\). Shared factors generate genuine pair interactions that cannot be represented by a common gate and independent channels.

Direct joint-pilot counts give time-uniform entrywise intervals. If the common entrywise radius is \(r_t\), then

\[
\|P_t-\widehat P_t\|_{\rm op}\le d r_t,
\]

so

\[
\widehat P_t+d r_t I
\]

is an anytime Loewner upper model. Every true pair matrix is covered in the deterministic replay.

An open-ended restarted likelihood-ratio process detects the drifting \((0,1)\) interaction after

\[
\boxed{3104\text{ shots}}.
\]

Direct matrix weighting reduces covariance error relative to the factorized model to

\[
\boxed{0.0076193}
\]

of the factorized error. A rank-two-plus-sparse residual model detects fourteen off-diagonal sparse entries, explains over 70 percent of residual energy in its rank-two component, and approaches the direct estimator while strongly outperforming factorization. The Loewner upper model contains the truth, preserves whitening, and keeps selector separation positive.

## Pass 725 — Exact semilinear certificates for all twenty-two controller phases

The complete declared controller domain contains

\[
7776
\]

cells, split among

\[
54
\]

discrete science chambers \((Q,s_1,s_2)\) and

\[
22
\]

distinct root phases.

Pass 725 batch-compiles the dynamic program and gives every phase an exact finite-domain symbolic certificate. For each science chamber, the four cost coordinates

\[
(c_1,c_2,o,\kappa)
\]

are represented by an irredundant union of integer orthotopes. The full classifier uses

\[
1857
\]

maximal monochromatic boxes, reduced to an irredundant DNF of

\[
\boxed{1615\text{ boxes}}.
\]

The compiled lookup reproduces all \(7776\) dynamic-programming cells exactly and preserves the \(1308\) unique tagged-pair cells.

The controller also computes the smallest integer credit applied to the covariance-tagged trace cost that restores the desired pair phase. Across the atlas, the credit distribution begins

\[
0^{1308},\ 1^{655},\ 2^{642},\ 3^{728},\ldots
\]

and at the nominal \(\kappa=1\) point the exact minimum is

\[
\boxed{2\text{ blocks}}.
\]

## Verification boundaries

- Pass 721 computes the exact \(E=(C_2)^4\) local degree-two census and proves formal rigidity from global \(H^1=0\); it does not claim that any of the ninety local traceless classes survives global fusion.
- Pass 722 realizes the q=2/S8 nodal order on the W33 cycle lattice; it does not realize the corrected q=3 cyclotomic interface.
- Pass 723 assumes an auxiliary reference interferometer and a nine-parameter hardware family.
- Pass 724 assumes independent pilot packets sharing the science state and a declared smooth drift envelope.
- Pass 725 is exact on the declared integer domain. Its orthotope DNF is not yet the globally minimal continuous min-plus arrangement in \(\mathbf R^4\).
