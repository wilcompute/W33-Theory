# Integer Chern numbers obstruct the \(T^{p,q}\) warp resonance

The [D3 probe result](2026-11-16_D3_arbitrary_shape_probe.md) identifies a discharge saddle in any smooth, nonconstant, pure-five-form warped solution of the specified Type IIB class. Its external Einstein equation requires a scalar eigenvalue \(32\) for infinitesimal warping about an unwarped Freund–Rubin product. The equal-flux conifold and its quotients miss that value. This calculation extends the obstruction to **every quantized \(T^{p,q}\)**, including quotients, zero-Chern endpoints and harmonics with fiber momentum. It also gives primitive Chern sequences with eigenvalues approaching \(32\) from both sides at inverse-square order. Hence the local warp obstruction has no flux-independent spectral gap.

## The circle-bundle scalar spectrum

Let \(p,q\) be the Chern numbers in the [repo's normalization](2026-11-16_D9_iib_conifold_dual.md), \(L\) the AdS radius, and \(\eta\in[0,1]\) its Einstein shape. Signs of \(p,q\) change monopole orientations and do not affect the scalar spectrum. For both Chern numbers nonzero,
\[
 k_1=L^2/r_1^2=4(1+\eta),\qquad k_2=L^2/r_2^2=4(2-\eta),\qquad
 \left|\frac{q}{p}\right|^2=\frac{(1-\eta)(1+\eta)^2}{\eta(2-\eta)^2}.
\]
The last ratio decreases strictly from infinity to zero, so it selects one interior \(\eta\). The fiber radius obeys \(s^{-2}=p^2(1+\eta)^2/(2\eta)=q^2(2-\eta)^2/[2(1-\eta)]\) with \(s=R_f/L\). In the fiber Fourier sector \(n\in\mathbb Z\), scalar functions are sections over the two spheres with monopole numbers \(np,nq\). Write \(a=|np|\), \(b=|nq|\). The complete dimensionless spectrum in that sector is
\[
 \lambda=4(1+\eta)\left[j(j+1)-a^2/4\right]+
         4(2-\eta)\left[k(k+1)-b^2/4\right]+n^2s^{-2},
 \quad j\in a/2+\mathbb Z_{\ge0},\quad k\in b/2+\mathbb Z_{\ge0}.
\]
This is the sum of two monopole connection Laplacians and the vertical Laplacian. The repo already uses each connection spectrum in the [D9 charged scalar check](toe_20261116_D9_charged_monopole_harmonics.py). Combining them with the Einstein relation is what bounds the sectors that might be resonant. [Gubser, scalar harmonics on \(T^{p,q}\)](https://arxiv.org/abs/hep-th/9807164) · [Gubser and Mitra, Einstein shape and five-form spectrum](https://arxiv.org/abs/hep-th/0108239)

## Exact exclusion at \(32\)

For \(n=0\), only \((j,k)=(2,0)\) and \((0,2)\) can hit \(32\) anywhere on the continuous Einstein shape curve. All other levels are at most \(24\) or at least \(40\). The first candidate requires \(\eta=1/3\) and \(q^2/p^2=32/25\), with the other obtained by exchanging the spheres. Both ratios require irrational \(|q/p|\) and are therefore absent for every integer Chern pair.

For \(n\ne0\) and both Chern numbers nonzero, the vertical term is at least \(2\max(a,b)^2\). Thus \(\max(a,b)\ge5\) puts the eigenvalue above \(48\). With \(a,b\le4\), a spin at least \(7/2\) contributes a horizontal term of at least \(47\), and the vertical term supplies at least two more units. In the remaining 100 labels the shape obeys
\[
 {\cal P}_{a,b}(\eta)=b^2\eta(2-\eta)^2-a^2(1-\eta)(1+\eta)^2=0.
\]
An exact Euclidean polynomial algorithm tests the gcd of \({\cal P}_{a,b}\) with the numerator of \(\lambda-32\) and rules out a common root in \(0<\eta<1\) in all cases. Rational root isolation and interval bounds on each eigenvalue further give \(|\lambda-32|\ge 0.113\) uniformly in the charged sectors of all bundles with \(pq\ne0\). The closest tested label has effective charges \((1,3)\) and spins \((1/2,3/2)\), up to exchange.

When one Chern number vanishes, the geometry is \(S^2\) of radius \(L/2\) times a lens quotient of \(S^3\) of radius \(L/\sqrt2\). Its scalar spectrum is a subset of \(4j(j+1)+2J(J+2)\) with nonnegative integers \(j,J\). It stays at least \(2\) away from \(32\). The pair \((0,0)\) does not give a positive Einstein metric of this circle-bundle form.

## Primitive integer sequences approach from both sides

For the neutral \((2,0)\) harmonic set \(D=25q^2-32p^2\). Evaluating \({\cal P}_{p,q}\) at \(1/3\) gives \(D/27\), while \(|{\cal P}_{p,q}'|\le4(p^2+q^2)\) on \([0,1]\). Checking square residues modulo \(80\) excludes \(D=-6,\ldots,-1\) and \(D=1,\ldots,16\), and \(D=0\) is excluded by irrationality. Hence
\[
 |\lambda_{2,0}-32|\ \ge\ \frac{14}{9(p^2+q^2)}.
\]
The exchanged bound applies to \((0,2)\). The inverse-square order is attained from both sides. Put \(x=5q,\ y=4p\), so \(D=x^2-2y^2\). Multiplication of \(x+y\sqrt2\) by the Pell unit \(19601+13860\sqrt2=(3+2\sqrt2)^6\) preserves \(x\in5\mathbb Z,\ y\in4\mathbb Z\), and acts on \((p,q)\) by an integer matrix of determinant one. Starting at \((1,1)\) and \((38,43)\) gives primitive sequences with the smallest negative norm in magnitude (\(-7\)) and the smallest positive norm (\(17\)). They approach \(|q/p|=4\sqrt2/5\). Expansion of \({\cal P}_{p,q}\) at \(1/3\) gives the signed limit
\[
 \lim p^2(\lambda_{2,0}-32)=-\frac{5D}{12}.
\]
The lower five-form and metric-trace mode has \(m^2L^2=\lambda+16-8\sqrt{\lambda+4}\). For the near-resonant level, its standard-quantization dimension is \(\Delta=\sqrt{\lambda+4}-2\), hence \(\Delta-4=(\lambda-32)/12+O((\lambda-32)^2)\). These are classically near-marginal scalar modes on both sides of dimension four. This conclusion concerns one Kaluza–Klein sector. The unequal-flux homogeneous metric instability identified in the repo remains present. [Gubser and Mitra, Eq. (18)](https://arxiv.org/abs/hep-th/0108239)

## Scope of the local obstruction

For each fixed quantized bundle, the external warp equation \(L^2\Delta u=20(u^{-1}-u^{3/5})\), with \(u=e^{5A}\) in the normalized flux convention, implies local nonlinear rigidity of the warp. If \(\delta=\operatorname{dist}(32,\operatorname{spec}(-L^2\Delta))>0\), its linear inverse gives \(\delta\|u-1\|_2 \le 170\|u-1\|_\infty\|u-1\|_2\) for \(\|u-1\|_\infty\le1/2\), by Taylor's theorem. The argument persists with a smaller \(\delta\) for nearby internal metrics. Along the Pell sequences this sufficient neighborhood shrinks, so the calculation leaves open solutions with small but finite warp on a sequence of different fluxes. It gives no claim about the nonlinear internal Einstein equations at those amplitudes, additional fields, finite-brane backreaction or string corrections.

The external equation alone admits precisely the sort of small finite-amplitude evasion the estimate allows. Freeze the internal metric and take a scalar pulled back from sphere 1 that is axisymmetric and even in \(\cos\theta_1\). In this sector \(L^2\Delta=k_1\Delta_{S^2_{\rm unit}}\), and the eigenvalue \(32\) is simple at \(k_1=16/3\), carried by \(P_2\). The complementary operator is invertible. Solve the complementary equation by the implicit function theorem, writing \(u=1+hP_2+O(h^2)\) with the remainder orthogonal to \(P_2\). The projected equation is
\[
 0=(32-6k_1)h-\frac{32}{5}h^2+O(h^3).
\]
The coefficient is \((112/5)\int P_2^3/\int P_2^2\). Dividing by \(h\) gives an implicit nonconstant branch \(h=(5/32)(32-\lambda_{2,0})+O((32-\lambda_{2,0})^2)\), including the nearby quantized shapes. This solution of the external equation fails the internal Einstein equation at fixed metric. Its traceless part would require \(\nabla^2(e^A)\) to be pure trace because the fixed internal metric is Einstein and the purely internal five-form stress is isotropic. The Hessian evaluated twice on the unit fiber vector vanishes for a fiber-invariant scalar, since the constant-length fibers are geodesics. Its trace would therefore vanish and compactness would force \(A\) constant. Any continuation to a genuine warped solution must let the internal metric respond.

Reproduce with `py -3 -B analysis/toe_20261116_Tpq_warp_resonance.py`. The [JSON certificate](../data/toe_20261116_Tpq_warp_resonance.json) includes the exact charged root intervals and primitive near-resonance examples.
