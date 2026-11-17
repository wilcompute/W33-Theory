# An exact unequal-flux scalar block on the eleven-dimensional product

The [earlier product calculation](2026-11-16_D9_mtheory_uplift.md) establishes a homogeneous instability for every unequal mixed-flux ratio and a nonzero torus-momentum instability at equal flux. Here the gauged metric constraints are solved for five sphere-singlet scalar fields at nonzero momentum, for arbitrary mixed-flux ratio. The Breitenlohner–Freedman threshold remains exactly $L^2|k|^2=12$. There is also an exact static marginal mode at a different, flux-dependent momentum. The result concerns the two-derivative product, a solution in the [symmetric-space classification](https://arxiv.org/abs/1611.06139). Other spherical harmonics and higher-derivative terms are outside this calculation.

## A consistent transverse-circle reduction

Use $L=1$, $d=(p^2-q^2)/(p^2+q^2)$, $p^2=4(1+d)$, $q^2=4(1-d)$, $u^2=16$, and $k_1=6+2d$, $k_2=6-2d$. The mixed flux signs can be absorbed in the definitions of the two axions. For a nonzero torus covector choose an orthonormal local frame $x,y$ with the covector along $x$. All fields in a mode are independent of $y$. Use sphere log-radii $\beta_1,\beta_2$ and the transverse-circle log-radius $\gamma$. In a six-dimensional Einstein frame take

$$
ds_{11}^2=e^{-S/2}ds_6^2+e^{2\beta_1}ds_1^2+e^{2\beta_2}ds_2^2+e^{2\gamma}dy^2,\qquad
S=2\beta_1+2\beta_2+\gamma .
$$

The sphere metrics and forms on the right refer to the background. The fluctuating flux ansatz is

$$
G_4=u\,\omega_1\wedge\omega_2
+d\chi_1\wedge dy\wedge\omega_1+d\chi_2\wedge dy\wedge\omega_2 .
$$

The two mixed terms share a $dy$ leg, and each shares a sphere factor with the horizontal term, so the full Chern–Simons source vanishes identically on this ansatz. The dual of the horizontal flux has every base leg and $dy$, so its exterior derivative vanishes. The remaining form equations are precisely the two axion equations. There is no mixed Einstein stress sourcing the transverse-circle gauge field. Thus one can set the discarded vectors and three-form components to zero in this sector even at unequal flux. The axion gradients carry the quantized mixed periods, with a globally closed field strength even when the background axions are only locally linear.

The six-dimensional action has the scalar terms

$$
-\tfrac12 \partial\sigma^T G\,\partial\sigma-\tfrac12\sum_i Z_i(\partial\chi_i)^2-V,\qquad
G=\operatorname{diag}(4,4,2)+\tfrac12 nn^T,\quad n=(2,2,1)^T,
$$

where $\sigma=(\beta_1,\beta_2,\gamma)^T$, $Z_i=e^{-4\beta_i-2\gamma}$, and

$$
V=e^{-S/2}\left[-2k_1e^{-2\beta_1}-2k_2e^{-2\beta_2}
+8e^{-4(\beta_1+\beta_2)}\right].
$$

At the background the axion gradients are $f=(p,q)^T$ along $x$, $V=-16$, and $V_A=-\frac12\sum_i f_i^2(Z_i)_{,A}$.

## Eliminate the scalar metric constraints

Set $\lambda=k^2>0$ and $z=m^2$. For an $\mathrm{AdS}_5$ scalar harmonic $\psi$ with $\Box_5\psi=z\psi$, use axial gauge $h_{xx}=h_{x\mu}=0$. Write $h_{\mu\nu}=A g_{\mu\nu}\psi+B\nabla_\mu\nabla_\nu\psi$ and $\delta\chi_i=i a_i\psi$ with the common factor $e^{ikx}$ implicit. The traceless $\mu\nu$ and mixed $x\mu$ Einstein equations give

$$
B=3A/\lambda,\qquad f^Ta=-4k(A+B).
$$

The trace equation gives $2(\lambda-z+8)A=V_A s^A$ for the amplitude $s=\delta\sigma$. The $xx$ equation then follows, and the trace relation is also implied by the axion equations contracted against $f$. These constraints are needed for the flux-parallel axion. Treating the full torus metric as a fixed background would give a different mass matrix.

Write $z_i=\nabla Z_i|_0$ and $D=V''|_0+\frac12\sum_i f_i^2 z_i z_i^T$. The five scalar amplitudes obey the symmetric generalized eigenvalue problem $\mathsf M v=m^2\mathsf K v$ with

$$
\mathsf K=\operatorname{diag}\left(G,\,I-\frac{3 f f^T}{8(\lambda+3)}\right),
\qquad
\mathsf M=\begin{pmatrix}
\lambda G+D & -\sqrt{\lambda}\,(p z_1,\ q z_2)\\
-\sqrt{\lambda}\,(p z_1,\ q z_2)^T & \lambda I+\frac{5\lambda f f^T}{8(\lambda+3)}
\end{pmatrix}.
$$

The axion kinetic eigenvalues are $1$ and $\lambda/(\lambda+3)$, so the pencil has positive norm for every nonzero momentum. At equal flux the sphere-odd block gives the familiar $m_\pm^2=\lambda-2\pm\sqrt{4+16\lambda}$. The limit of the five eigenvalues as $\lambda\to0^+$ is $0,0,32,4\pm\sqrt{64+80d^2}$. The three nonzero radius-branch limits coincide with the homogeneous radius calculation. The axial gauge itself is singular at zero momentum.

## Exact BF and static thresholds

The exact determinant at the BF value is

$$
\det(\mathsf M+4\mathsf K)=
\frac{72\lambda(\lambda-12)}{\lambda+3}
\left[\lambda^4+40\lambda^3+(336-80d^2)\lambda^2+
(2304-896d^2)\lambda+3840d^2\right].
$$

The bracket is positive for $|d|\le1$ and $\lambda>0$. At one point with $\lambda<12$ the signs of the successive exact principal determinants give one negative pivot. Above 12 the form is positive at large $\lambda$ because its leading term is $\lambda\mathsf K$ up to lower order. Inertia cannot change on either connected domain without a zero of the determinant. Thus **exactly one of these scalars violates BF for each signed Fourier momentum with $0<\lambda<12$, for every flux ratio**. At 12 the BF root is simple and its eigenvector is recorded in the certificate. The original homogeneous BF violation still applies when $d\ne 0$. For the stability criterion and a distinct class of $AdS_5$ mass calculations, see [Martin and Reall](https://arxiv.org/abs/0810.2707).

If $a=\mathcal A/L^2$ is the torus area in AdS units, a general reduced-modular torus has a mode in the band precisely when $a\,\operatorname{Im}\tau>\pi^2/3$, using reduced $\tau$. For all flat shapes this is forced when $a>2\pi^2/(3\sqrt3)$ by the hexagonal shortest-vector bound. Each nonzero lattice covector below threshold contributes one unstable amplitude in the complex Fourier description, with conjugate amplitudes paired for real fields.

At zero mass,

$$
\det(\mathsf M)=\frac{72\lambda^4}{\lambda+3}
\left[\lambda^2+8\lambda-560-80d^2\right].
$$

Its positive root is $\lambda_{\mathrm{static}}=-4+4\sqrt{36+5d^2}$. At constant $\psi$ the mixed equation is trivial, but the $xx$ and trace equations impose the same relation $f^Ta=-4(\lambda+3)A/k$. Thus the root also gives a static linear modulation preserving the external AdS isometries. At fixed periods the product has freely variable torus shape and the momentum can be tuned by changing the aspect ratio at fixed area. The zero is simple as a function of $\lambda$. Constructing a nonlinear branch requires solving the backreaction and the homogeneous constraints and cannot be inferred from the linear massless mode alone.

Reproduce with `python analysis/toe_20261117_11D_unequal_flux_scalar_operator.py`. The matching certificate is `data/toe_20261117_11D_unequal_flux_scalar_operator.json`.
