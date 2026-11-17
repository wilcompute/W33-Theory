# Two modulated AdS solutions at the same quantized flux

The [unequal-flux square branch](2026-11-17_11D_unequal_square_branch.md) changes direction at two classical flux imbalances where its relaxed quartic coefficient vanishes. The sixth-order coefficient is strictly negative at both reversals. This creates a local fold on each adjoining side where the quartic is positive. At the integer period assignment $(6716,3186,2655)$, the spectral equations have two distinct nonconstant solutions with the same periods and square conformal structure, in addition to the homogeneous product.

## Sixth-order relaxation

Set $d=(p^2-q^2)/(p^2+q^2)$ and let $\Lambda(d)=-4+4\sqrt{36+5d^2}$ be the static threshold. Work in the square rotation-invariant sector with the four profile fields $(A,B,c,v)$ of the [static action](2026-11-17_11D_square_modulated_branch.md). Take $\epsilon$ to be the coefficient of $\cos x+\cos y$ in $v$. The leading fields have profile $\epsilon w(\cos x+\cos y)$, with the first component $w_A=0$. The order-two relaxation uses $1,\cos 2x+\cos 2y,\cos x\cos y$ and was solved in the quartic calculation.

The order-three relaxation has support on the fundamental, $\cos 3x+\cos 3y$, and $\cos 2x\cos y+\cos x\cos 2y$. Set its $v$ coefficient at the fundamental to zero, as required by the amplitude convention. The Hessian is invertible on that complement and on the two higher harmonics. In the sextic action the terms multiplying the unknown order-four profile vanish by the order-two equations. Those multiplying the order-five profile vanish against the static kernel. After the order-three solve, the sixth-order coefficient takes the form

$$
c_6=c_{6,\mathrm{frozen}}-\tfrac12\sum_j F_j^T H_j^{-1}F_j .
$$

Here the frozen term includes the entire order-two backreaction, $F_j$ is the source for the order-three harmonic, and $H_j$ is its normalized static Hessian. The verifier expands the actual reciprocal averages of the mixed flux terms at fixed periods, including the product term in their sixth-order coefficient. It computes each needed torus moment with a tensor Fourier rule of order 12. All integrands have Fourier frequencies of magnitude at most six on each axis, so this quadrature is exact in real arithmetic. Interval arithmetic encloses the evaluations and the elimination pivots over exact rational isolating intervals for both quartic zeros.

At a quartic zero the fourth-order detuning in the stationary equation is $t_*=-3c_6/\kappa$, where $\kappa=-8(\Lambda+4)/(\Lambda+28)<0$. The interval signs give

| Critical $|d|$ | Relaxed $c_6$ | $t_*$ in $\lambda-\Lambda=t_*\epsilon^4+O(\epsilon^6)$ |
| --- | ---: | ---: |
| $0.4528710563501$ | $-584.1367062802$ | $-435.0477969873$ |
| $0.6620726953419$ | $-3072.2626368209$ | $-2270.6509429634$ |

## Folds near both critical ratios

At nearby $d$ let $s=s_2(d)$ be the earlier quadratic detuning coefficient and set $Y=\epsilon^2$. The local analytic branch satisfies

$$
\lambda-\Lambda=sY+t(d)Y^2+O(Y^3),\qquad t(d_*)=t_*<0.
$$

For positive sufficiently small $s$, differentiation gives a nondegenerate fold with

$$
Y_{\rm fold}=-\frac{s}{2t(d)}+O(s^2),\qquad
\lambda_{\rm fold}-\Lambda=-\frac{s^2}{4t(d)}+O(s^3)>0 .
$$

The two positive amplitudes on the two sides of the fold describe distinct geometries. Changing the sign of either amplitude is a torus translation. The earlier rational-root result excludes an exactly vanishing quartic at integer mixed periods. It allows rational mixed ratios approaching the critical point from the positive-quartic side. At each such mixed ratio the common scale of the mixed periods relative to the horizontal period gives detunings dense in the open fold interval. Thus the local classical construction admits infinitely many quantized period assignments with two modulated solutions. This uses the local analytic branch and its nondegenerate turning point. [Crandall and Rabinowitz](https://www.sciencedirect.com/science/article/pii/0022123671900152) · [Lim on warped flux branches](https://arxiv.org/abs/1202.3525)

## A fixed-period spectral verification

For $(|N_0|,|N_1|,|N_2|)=(6716,3186,2655)$, the mixed ratio is $6/5$, with $d\simeq0.4498288713$ and $\lambda-\Lambda\simeq1.41628\times10^{-5}$. At each trial amplitude the spectral method solves the other Fourier equations, then brackets the remaining fundamental equation. This avoids an ill-conditioned simultaneous solve near the fold.

| Solution | $\epsilon$ | Largest unprojected residual | Change in normalized inverse AdS Newton constant |
| --- | ---: | ---: | ---: |
| Lower amplitude | $0.008865568010$ | $7.51\times10^{-14}$ | $+2.64\times10^{-10}$ |
| Higher amplitude | $0.021541628583$ | $1.74\times10^{-10}$ | $-1.55\times10^{-9}$ |

Both residual checks include the independent trace-free Einstein components. This pair is a finite-resolution numerical test at one particular period assignment. Its existence is distinct from an exact bifurcation of a homogeneous product at fixed integer periods, which remains obstructed by the [torus shape equation](2026-11-17_11D_static_bifurcation_obstruction.md). The fold calculation is static. The homogeneous BF instability persists on sufficiently nearby unequal-flux solutions by continuity, and the finite-amplitude dynamical spectrum for the numerical pair remains to be calculated.

Reproduce with `python analysis/toe_20261117_11D_square_sextic_folds.py`. The output is `data/toe_20261117_11D_square_sextic_folds.json`.
