# The protected toroidal curvature coupling detects the six-form axion

The [kinetic reconstruction](2026-11-15_torus_kinetic_reconstruction.md) leaves one unread scalar when the six momentum directions are used as reflection labels. In that frame the missing scalar is the dual six-form axion. The protected five-dimensional $R^4$ coupling detects it directly. On the torus volume–axion slice, all nonzero Fourier integers occur. Their leading small-volume coefficients are fixed by the large-volume expansion and integral duality.

## Integral axion and volume duality

Fix the determinant-one metric of the six-torus, set the internal three-form periods to zero, and write $z=x+iy$. The variable $x$ is the six-form period, with unit shift in the integral charge convention, and $y$ is the dimensionless eleven-dimensional torus volume. In the momentum–M5 doublet a positive coset block is

$$M(z)=\frac1y\begin{pmatrix}x^2+y^2&x\\x&1\end{pmatrix}.$$

At $x=0$, isotropic radius scaling gives the kinetic factors $y$ for the six momenta, $y^{-1}$ for the six M5 coordinates, and one for the 15 M2 coordinates. The derivative of $M$ at $z=i$ is the six simultaneous momentum–M5 swaps of character 63 in the kinetic certificate. The integral generators $z\mapsto z+1$ and $z\mapsto-1/z$ act on those six doublets and leave the M2 coordinates unchanged. Substitution shows that both preserve every coefficient of the signed cubic. The corresponding subgroup is the arithmetic $SL(2)$ in the standard toroidal $E_{6(6)}$ charge lattice. The verifier also transports the symmetric axion generator to all 36 nonsingular scalar directions using the signed integral Weyl lifts. [Pioline, toroidal charge lattice](https://arxiv.org/abs/hep-th/0506228) · [Ruiz and Varona, volume inversion and the exchanged momentum/M5 towers](https://arxiv.org/abs/2611.00235)

## The large-volume input and a measurable rational-cusp contrast

Let $F(z)$ be the usual dimensionless protected $R^4$ coefficient in five-dimensional Planck units at this fixed shape. In the standard automorphic description it is the $E_6$ Eisenstein coefficient at $s=3/2$. The M-theory parabolic constant term has

$$F(x+iy)=A y^2+B y^{3/2}+o(1),\qquad y\to\infty,\quad A=4\zeta(2),$$

where $B$ is its $SL(6)$ Eisenstein coefficient at the fixed shape. Table 5 gives the powers as $r^8$ and $r^6$ with $r^4=y$. The remainder used here follows from the standard constant-term estimate on the volume cusp, uniformly for the periodic axion at fixed Levi shape. One way to see the uniformity is to use the compact quotient of the unipotent radical. The positive volume ray contracts each unipotent derivative after it is moved to the right of the height element. Uniform moderate growth of all right derivatives then bounds sufficiently high unipotent derivatives by arbitrary inverse powers of $y$. On the compact quotient this bounds the deviation from its average. [Green, Miller, Russo and Vanhove, Table 5](https://arxiv.org/abs/1004.0163) · [Garrett, estimates for Eisenstein constant terms](https://www-users.cse.umn.edu/~garrett/m/v/current_version.pdf)

For coprime $a,q$ with $q>0$, choose integers $r,t$ with $-ar-qt=1$. The integral transformation with bottom row $(q,-a)$ sends $a/q+iy$ to $r/q+i/(q^2y)$. It acts inside the slice, so

$$F(a/q+iy)=\frac{A}{q^4y^2}+\frac{B}{q^3y^{3/2}}+o(1),\qquad y\to0^+.$$

At equal volume and shape the protected coefficient at axion $1/2$ is asymptotically **one sixteenth** of its value at axion zero. The ratio for $a/q$ relative to zero is $q^{-4}$.

In compatible dual charge coordinates the norm of one momentum–M5 doublet is $|m+nz|/\sqrt y$. At the rational cusp, the primitive doublet $(-a,q)$ has norm $q\sqrt y$ and is an integral dual of a momentum direction in the large-volume frame. There is one such doublet for each of the six circle labels, with fixed shape factors. The leading curvature coefficient scales as the inverse fourth power of this tower scale, with the same $q^{-4}$ cusp weight.

For fixed irrational $x$, $y^2F(x+iy)\to0$. Indeed the reduced modular height $h$ is the maximum of $y/|cz+d|^2$ over primitive bottom rows. For large $|c|$, the quantity $yh$ is bounded termwise by $1/c^2$. For finitely many bounded $|c|$ the irrational $cx+d$ is nonzero and the terms go to zero. The cusp expansion bounds $F$ by a constant times $1+h^2$. At a badly approximable irrational, a uniform bound $|cx+d|\geq\kappa/|c|$ even keeps the reduced height bounded. These limits refer to the protected coefficient obtained by taking the low-energy expansion at each finite volume. The energy range of that expansion changes as a tower becomes light.

## Every Fourier integer contributes

Write $\widehat F_n(y)=\int_0^1 F(x+iy)e^{-2\pi i n x}\,dx$. Normalize the rank-one Eisenstein function $E_s$ so that its leading cusp term is $y^s$. The difference $F-AE_2-BE_{3/2}$ is bounded on the modular domain by the cusp expansion and smoothness on the compact remainder. This subtraction uses only the asymptotics. It does not identify the full restriction with a sum of two rank-one functions.

For $s>1$, the primitive-row sum for $E_s$ has rational cusp peaks given by the periodization of

$$\frac{y^s}{q^{2s}\big((x-a/q)^2+y^2\big)^s}.$$

The measures $y^{s-1}E_s(x+iy)\,dx$ converge weakly to point masses at reduced rationals, with weight $C_s/q^{2s}$ for $C_s=\int_{\mathbb R}(1+u^2)^{-s}du$. The total mass bound follows from $\sum_q\varphi(q)/q^{2s}<\infty$. The phase sum at denominator $q$ is the Ramanujan sum $c_q(n)=\sum_{d\mid(q,n)}d\,\mu(q/d)$. Summing over denominators gives $\sum_q c_q(n)/q^{2s}=\sigma_{1-2s}(|n|)/\zeta(2s)$ for $n\ne0$. Here $\sigma_k(n)=\sum_{d\mid n}d^k$.

At $s=2$ the peak has finite second moment, so replacing its phase by the central phase in a fixed Fourier mode costs $O(y)$ in the unscaled Fourier coefficient. At $s=3/2$ weak convergence gives the required next order. Using $C_2=\pi/2$ and $C_{3/2}=2$ therefore gives

$$\widehat F_n(y)=\frac{30}{\pi}\frac{\sigma_{-3}(|n|)}{y}
+\frac{2B}{\zeta(3)}\frac{\sigma_{-2}(|n|)}{\sqrt y}
+o(y^{-1/2}),\qquad n\ne0.$$

The mean has the same leading formula with $\sigma_{-3}(|n|)$ replaced by $\zeta(3)$ and the subleading multiplier $\sigma_{-2}(|n|)$ replaced by $\zeta(2)$. Every fixed nonzero Fourier integer is therefore present for sufficiently small volume on the six-form slice. Equivalently $yF(x+iy)\,dx$ converges to a measure supported on rational axions with masses $A\pi/(2q^4)$ at each reduced fraction. The Fourier asymptotic gives central six-form dependence of the protected interaction, while the finite-volume Fourier–Jacobi coefficients and their instanton measures remain to be determined. [Green, Miller and Vanhove, Fourier modes of protected interactions](https://arxiv.org/abs/1111.2983)

## Independent check with the protected $\partial^4R^4$ coupling

The next protected four-graviton coefficient $G$ has three terms in the same M-theory constant term. Table 8 gives their powers as $r^{14}$, $r^{10}$ and $r^8$, so $G(x+iy)=D y^{7/2}+B_4 y^{5/2}+C_4 y^2+o(1)$. In the paper's Epstein conventions the first coefficient is $D=-8\zeta(4)Z_{S}(-1/2)$, where $S$ is the determinant-one shape appearing in that Epstein sum. Its functional equation gives the useful positive expression $D=Z_{S^{-1}}(7/2)/12$. Thus the rational-cusp ratio is $q^{-7}$, giving **one part in 128** at axion $1/2$ relative to zero. Along rational cusps $G/F^{7/4}$ tends to $D/A^{7/4}$, independent of the denominator.

Subtracting $D E_{7/2}+B_4 E_{5/2}+C_4 E_2$ again leaves a bounded remainder. The peak integrals $C_{7/2}=16/15$ and $C_{5/2}=4/3$ give the first Fourier terms at fixed $n\ne0$,

$$\widehat G_n(y)=
\frac{16D}{15\zeta(7)}\frac{\sigma_{-6}(|n|)}{y^{5/2}}
+\frac{4B_4}{3\zeta(5)}\frac{\sigma_{-4}(|n|)}{y^{3/2}}
+\frac{\pi C_4}{2\zeta(4)}\frac{\sigma_{-3}(|n|)}{y}
+O(y^{-1/2}).$$

The error follows from the finite second moments of these three kernels. This gives a second protected observable with a different divisor sum and tower exponent on the same axion slice. [Green, Miller, Russo and Vanhove, Table 8 and normalization](https://arxiv.org/abs/1004.0163)

Replay the algebraic checks with SymPy.

    python -B analysis/toe_20261116_torus_axion_r4.py

The [certificate](../data/toe_20261116_torus_axion_r4.json) verifies the integral transformations, the match to all 36 scalar directions, representative rational cusps, and the Ramanujan arithmetic. The asymptotic uses the published protected toroidal coupling. It does not provide a quantum identification of the del Pezzo probe and the toroidal theory.
