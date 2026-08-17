# Passes 5816–5823 — the `1+9+6` carrier split is matrix-rank Fourier geometry

## Executive result

The matrix-ring model of Passes 5792–5799 explains not only the outer involution but the entire representation split of the 16-line carrier. The line set is the additive affine torsor

\[
T=M_2(\mathbb F_2).
\]

Its 16 Walsh characters are indexed by the dual matrix space, identified with another copy of `M_2(F_2)` through

\[
\langle Y,M\rangle=\operatorname{tr}(Y^TM).
\]

Under the left/right linear group the dual labels split by matrix rank:

\[
\boxed{16=1+9+6},
\]

one zero matrix, nine nonzero rank-one matrices, and six invertible rank-two matrices. The exact representation theorem is

\[
\boxed{\mathbb Q^{16}_L=\mathbf1\oplus W_9^{\mathrm{rank}\,1}\oplus V_6^{\mathrm{rank}\,2}}.
\]

## Pass 5816 — full Walsh basis

For every matrix label `Y`, define

\[
\boxed{v_Y=\sum_{M\in M_2(\mathbb F_2)}(-1)^{\langle Y,M\rangle}e_M}.
\]

The 16 Walsh vectors satisfy

\[
\boxed{\langle v_Y,v_Z\rangle=16\delta_{YZ}},
\]

so they form an orthogonal rational basis of the line module. Their label-rank census is

\[
\boxed{0^1\oplus1^9\oplus2^6}.
\]

## Pass 5817 — `W_9` is the rank-one Fourier orbit

A nonzero rank-one dual matrix has the unique factorization

\[
\boxed{Y=\phi^Tw^T,\qquad0\ne\phi\in V^*,\quad0\ne w\in W},
\]

so the nine rank-one matrices form a literal `3 x 3` grid indexed by `(\phi,w)`.

Define point- and heavy-fibre Walsh vectors

\[
\boxed{u_{w,\phi}=\sum_{x\in V}(-1)^{\phi(x)}e_{(w,x)}},
\]

\[
\boxed{h_{w,\phi}=\sum_{\psi\in W^*}(-1)^{\psi(w)}e_{(\phi,\psi)}}.
\]

For point–line Reye incidence `R`, point–heavy incidence `H`, and line–heavy disjointness incidence `D`, exact summation gives

\[
\boxed{R^Tu_{w,\phi}=v_{\phi^Tw^T}},
\]

\[
\boxed{H^Tu_{w,\phi}=-2h_{w,\phi}},
\]

\[
\boxed{Dh_{w,\phi}=v_{\phi^Tw^T}}.
\]

Thus all three realizations of the common nine-space are the same nine rank-one additive characters, transported by finite Radon transforms.

## Pass 5818 — `V_6` is the invertible Fourier orbit

For every invertible dual label `Y`,

\[
\boxed{Rv_Y=0},\qquad\boxed{D^Tv_Y=0}.
\]

The six such vectors are independent and no rank-one Walsh vector is killed by either transform. Hence

\[
\boxed{V_6=\operatorname{span}\{v_Y:\det Y=1\}=\ker R=\ker D^T}.
\]

The previously unexplained six-dimensional line constituent is exactly the unit/rank-two Fourier sector.

## Pass 5819 — signed monomial affine action

For

\[
g=(X,A,B)\in M_2(\mathbb F_2)_+:\bigl(GL_2(2)\times GL_2(2)\bigr),
\]

the line action `M -> A M B^{-1}+X` becomes

\[
\boxed{gv_Y=(-1)^{\langle Y',X\rangle}v_{Y'},\qquad Y'=A^{-T}YB^T}.
\]

The verifier checks this on all `576*16=9216` group-element/Fourier-label pairs. Rank is preserved. The exact sector characters satisfy

\[
\boxed{\langle\chi_9,\chi_9\rangle=1},\qquad
\boxed{\langle\chi_6,\chi_6\rangle=1},\qquad
\boxed{\langle\chi_9,\chi_6\rangle=0}.
\]

Both sectors are explicitly rational, so character norm one proves absolute irreducibility.

## Pass 5820 — restriction to the normal 16-group

For `T=M_2(F_2)_+`, the line representation restricts to the regular representation and every additive character occurs exactly once. More precisely,

\[
\boxed{W_9\downarrow_T=\bigoplus_{\operatorname{rank}Y=1}\chi_Y},
\]

\[
\boxed{V_6\downarrow_T=\bigoplus_{\det Y=1}\chi_Y}.
\]

The normal 16-group therefore spectrally separates the common-nine and line-only-six sectors.

## Pass 5821 — transpose on Fourier labels

Matrix transpose acts by

\[
\boxed{\Theta v_Y=v_{Y^T}}.
\]

For `Y=\phi^Tw^T`,

\[
\boxed{Y^T=w^T\phi^T}.
\]

Thus the point/heavy outer involution swaps the two factors of the `3 x 3` rank-one Fourier grid while preserving the six invertible labels as a set.

## Pass 5822 — projective determinant split

Over `F_2`, each nonzero vector in the four-dimensional matrix space is a unique projective point of `PG(3,2)`. The determinant equation selects the nine nonzero rank-one points and its complement consists of the six invertible points:

\[
\boxed{15=9+6}.
\]

The determinant-zero locus carries the explicit `3 x 3` parametrization `(\phi,w)`. This is the standard hyperbolic-quadric/grid rank geometry of `2 x 2` matrices; here the count and product structure are verified directly.

## Prior-art boundary

Fourier decompositions of finite translation schemes and rank-orbit association schemes are classical. An explicit modern treatment of finite bilinear/quadratic-form translation schemes is Kai-Uwe Schmidt, *Quadratic and symmetric bilinear forms over finite fields and their association schemes* (arXiv:1803.04274). The ring `M_2(F_2)` and its two-qubit projective-line use are prior art in Saniga–Planat–Pracna (arXiv:quant-ph/0611063).

The repo-specific result is the exact identification of the already-certified q=5 Reye/heavy modules and incidence maps with these rank-stratified Walsh sectors.

## Evidence boundary

The dimensions `1+9+6` are matrix-rank Fourier strata, not Standard-Model multiplets or quantum states. No particle, gauge, mass/coupling, or continuum interpretation is inferred without an independent physical map.
