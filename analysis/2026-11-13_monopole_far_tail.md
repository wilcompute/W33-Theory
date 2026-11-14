# Projected monopole scattering beyond the earlier outer cutoff

The replay continues the radius-9 Robin profile to 4608 in the eight open channels at E=0.002. It keeps the full interior match at 36 and samples the same fitted scalar profile on logarithmic shells. Two meshes vary the number of cells per octave. The closed-channel comparison through radius 72 applies to the earlier calculation, while this replay uses the projected equations beyond 36. [Closed-channel check](2026-11-13_monopole_closed_feedback.md)

In the interaction picture the free channel phases drop out of the projected generator norm. A flux-preserving generator V induces the Riccati derivative of the unitary reflection graph R. Its contribution is [I,−R] V [R;I], with the two rectangular factors of norm sqrt(2). Thus the phase-stripped reflection has a limit whenever V is integrable in operator norm. Its change after a cut is at most twice the integral of that norm. The absolute change in any conversion probability is at most the change in reflection in operator norm, by trace distance between the normalized outgoing vectors. [Invariant imbedding](https://www.sciencedirect.com/science/article/pii/0096300375900272)

A linearized zero-mass scalar component would naively contribute a nonintegrable 1/r term. In this background the four zero directions are gauge tangents. Along a gauge orbit of the vacuum the fermion operator transforms by an invertible change of basis, so its first variation is a commutator with the vacuum operator. Compressing this commutator to the vacuum zero-energy space gives zero. For a smooth equivariant fermion mass map, the tangent displacement therefore contributes at order 1/r² or faster to the projected generator. Massive modes have Yukawa decay. This establishes integrability for the projected Robin model under that equivariance assumption. It does not establish convergence for the full coupled scattering problem.

The executable independently probes the directional derivative in the actual mass implementation at two step sizes. The exponential-integral diagnostic uses a multiplier measured on the grid after removing the fitted linear massless term. It is conditional on the measured envelope continuing beyond the grid and does not cover a remaining quadratic massless contribution. A quantitative tail bound would require explicit coefficient bounds, rather than a sampled envelope.

Replay with `py -3 analysis/toe_20261113_monopole_far_tail.py`. Use `--cells-per-octave 32` for the finer shell mesh.

For a quantitative version, write the scalar displacement as u/r + v(r), with u the zero-mode coefficient and ||v(r)|| ≤ b exp[−m(r−R)]/r. Here b can be chosen as R times the Euclidean norm of the massive boundary amplitudes, because the vacuum eigenvectors are orthonormal. If L bounds the first derivative of the projected generator at vacuum and M bounds its second derivative along the displaced profiles, Taylor's formula and the tangent cancellation give

    ||V(r)|| ≤ L b exp[−m(r−R)]/r + M (||u||+b)^2/(2r²).

Consequently, for a cutoff T≥R the conversion change is bounded by

    2 L b exp(mR) E1(mT) + M (||u||+b)^2/T.

This identifies which finite-dimensional derivative norms are needed for a uniform bound. It also distinguishes the potentially algebraic remainder from the Yukawa contribution. A finite-grid estimate of the first term alone gives no bound on their sum.

## First shell mesh

With sixteen cells per octave the conversion at E=0.002 is 80.7414327% at radius 2304 and 80.7415518% at 4608. The maximum projected first derivative along the fitted massless coefficient is 1.85e−14 in operator norm, comparable to the difference between finite-difference steps. The fitted scalar coefficient itself has norm 3.32e−6. The data are consistent with the exact gauge-tangent argument. The sampled Yukawa envelope would give a residual generator integral 7.12e−6 beyond 4608 if it remained valid. This last figure is an envelope diagnostic, with no claim of uniform validation or of a bound on full-channel scattering.

## Shell refinement

Thirty-two cells per octave give 80.7418656% at radius 4608. The two meshes differ by 0.000314 percentage points there. The finer mesh changes by 0.000121 percentage points from radius 2304 to 4608. These are finite comparisons, and the fitted profile has the same core on both meshes. The finer replay ran through Remote Desktop Commander. The projected limit exists under the stated gauge equivariance assumption. A certified numerical interval for that limit still needs uniform derivative constants.
