# The square AdS branch reverses direction twice with mixed-flux imbalance

The [balanced square branch](2026-11-17_11D_square_modulated_branch.md) exists above its static resonance at equal flux. Its nonlinear extension to unequal flux has two reversals of direction. For $d=(p^2-q^2)/(p^2+q^2)$ the approximate critical absolute imbalances are $0.452871056350$ and $0.662072695342$. Between them the branch lies below its static threshold, and outside them it lies above. Neither reversal occurs at a rational ratio of the two nonzero mixed periods. Spectral solutions at two integer flux assignments verify both directions.

## Unequal-flux normal form

Use the same square metric, variables $(A,B,c,v)$, and fixed-winding action as in the equal-flux calculation. The unequal potential and mixed flux weights are

$$
V=-(12+4d)e^{-18c/5-2v}-(12-4d)e^{-18c/5+2v}
+8e^{-48c/5},\qquad
W_\pm=2(1\pm d).
$$

The two flux contributions to the static action are $-W_\pm/\langle X_\pm\rangle$, with $X_\pm=e^{-5A+2B+12c/5\pm4v}$. Fourier reflection conditions and the quarter-turn are imposed on the scalar profiles. All four profiles can now contain both parities under the simultaneous half-period shift. The trace-free torus Einstein equation follows from the square symmetry and the divergence argument of the equal-flux calculation, and is also tested directly.

Let $\Lambda=-4+4\sqrt{36+5d^2}$ be the [exact static threshold](2026-11-17_11D_unequal_flux_scalar_operator.md). Normalizing the coefficient of $v$ to one, the leading mode multiplying $\epsilon(\cos x+\cos y)$ is

$$
(A,B,c,v)
=\left(0,\frac{16d(\Lambda+32)}{\Lambda(\Lambda+28)},
\frac{20d}{3(\Lambda+28)},1\right).
$$

The external warp has zero first harmonic even at unequal flux. The static action's quadratic detuning term is $\kappa(\Lambda)(\lambda-\Lambda)\epsilon^2$, where $\kappa=-8(\Lambda+4)/(\Lambda+28)$ is strictly negative. Let $c_4$ denote the relaxed quartic coefficient. Each of the three backreaction sectors $1,\cos 2x+\cos 2y,\cos x\cos y$ gives an exact correction $-F^T H^{-1}F/2$ to the frozen quartic. The verifier computes $F$ from third variations of the local and fixed-period flux terms and from the warp dependence of the gradients. It uses $80d^2=\Lambda^2+8\Lambda-560$ to make the result rational in $\Lambda$. At $d=0$ it reproduces $c_4=36736/459$.

The simple kernel and nonzero detuning derivative give a local analytic branch by the same square-symmetry argument as before, with

$$
\lambda=\Lambda+s_2(\Lambda)\epsilon^2+O(\epsilon^4),\qquad
s_2=-2c_4/\kappa .
$$

The exact $s_2$ has a ninth-degree numerator and a denominator positive throughout $20\le\Lambda\le22$. The sample value $s_2(20)=18368/459$ and its value at the single-flux endpoint, approximately $69.41318304$, are both positive. Exact real-root isolation gives two simple roots in the physical interval and verifies negative sign between them. The corresponding period ratios $|N_1/N_2|$ for $d\ge0$ are approximately $1.2020963$ and $1.4158505$. A sixth-order calculation is required for the direction exactly at the two real classical critical flux ratios. At generic unequal flux the torus shift again sends $\epsilon$ to $-\epsilon$ and makes the detuning even.

## Integer mixed periods avoid the two quartic zeros

For $N_1N_2\ne0$, the quantization relation can be written

$$
r^2=\frac{(1+d)(3-d)^2}{(1-d)(3+d)^2},\qquad r=|N_1/N_2|.
$$

The sum $T=r^2+r^{-2}$ is rational at integer periods, and its defining equation is even in $d$. Eliminating $\Lambda$ from this equation and the zero numerator of $s_2$ gives the explicit degree-nine resultant recorded in the certificate. Its rational-root set is empty. Thus no product with both mixed periods nonzero has an exactly vanishing $s_2$. The single-flux endpoints were checked separately. At each fixed rational mixed-period ratio, varying the common mixed scale relative to $N_0$ gives quantized detunings dense on the required side of resonance.

## Quantized numerical checks

| Periods $(|N_0|,|N_1|,|N_2|)$ | $d$ | $\lambda-\Lambda$ | First harmonic of $v$ | Largest unprojected residual |
| --- | ---: | ---: | ---: | ---: |
| $(2306,1068,801)$ | $0.6$ | $-1.780\times10^{-4}$ | $0.00726143$ | below $5\times10^{-14}$ |
| $(134,58,29)$ | $0.85663553$ | $+4.197\times10^{-3}$ | $0.01201720$ | below $6\times10^{-12}$ |

The residuals include both local trace-free Einstein components. At these nearby solutions the normalized inverse five-dimensional Newton constant changes by approximately $-2.3964\times10^{-9}$ and $+1.5445\times10^{-7}$, respectively. This agrees with the leading sign of $c_4/8$. The samples test particular detunings numerically. Exact branch existence sufficiently close to resonance follows from the simple-eigenvalue argument. [Crandall and Rabinowitz](https://www.sciencedirect.com/science/article/pii/0022123671900152) · [Lim on warped flux branches](https://arxiv.org/abs/1202.3525)

At each fixed nonzero $d$, the product already has a homogeneous mass strictly below BF. That instability persists sufficiently near the product by continuity. At equal flux the [explicit modulated fluctuation calculation](2026-11-17_11D_square_branch_BF_shift.md) gives a negative quadratic shift of the formerly BF-saturating mode. The reversals here concern where static solutions exist. Stability at larger detuning and the eventual fate of their time-dependent modes remain open.

Reproduce with `python analysis/toe_20261117_11D_unequal_square_branch.py`. The result is `data/toe_20261117_11D_unequal_square_branch.json`.
