# Flux quantization obstructs the static torus modulation

The [unequal-flux scalar calculation](2026-11-17_11D_unequal_flux_scalar_operator.md) gives a static nonzero-momentum zero mode at $\lambda_*=-4+4\sqrt{36+5d^2}$. A zero mode is a necessary linear test for an AdS-invariant modulated solution. At fixed quantized flux, it also has to satisfy the equation of the homogeneous torus shape. That equation obstructs every small-amplitude bifurcation with a nonzero first-order torus modulation in the sphere-singlet sector of this two-derivative product. The obstruction combines a fixed-flux variational identity with a restriction on equal-length vectors in a two-dimensional lattice.

## An exact condition for a one-direction modulation

Use the six-dimensional Einstein-frame reduction and notation of the scalar calculation. If a static profile depends on only $\theta$, a dimensionless $2\pi$-periodic angle, write

$$
ds_6^2=e^{2A(\theta)}ds_{\mathrm{AdS}_5}^2+\lambda^{-1}d\theta^2,\qquad
\sigma=(\beta_1,\beta_2,\gamma)^T.
$$

The proper length of the reference $x$ circle is proportional to $\lambda^{-1/2}$. Scale the reference transverse length proportional to $\lambda^{1/2}$ when varying $\lambda$, so that the reference area and all three flux periods are held fixed. The physical scale of the transverse circle can still vary through $\gamma$. Let $G,Z_i,V$ be the six-dimensional kinetic matrix, axion kinetic functions, and potential given in the scalar calculation. Eliminating the axion profile at its fixed winding gives

$$
\chi'_i=\frac{f_i}{\sqrt{\lambda}}\,
\frac{e^{-5A}/Z_i}{\langle e^{-5A}/Z_i\rangle}.
$$

Here primes are $\theta$ derivatives and brackets mean the angular average. Up to a common constant, the static action evaluated on these profiles is

$$
R_5\langle e^{3A}\rangle
+\left\langle e^{5A}\left(20\lambda (A')^2
-\tfrac{\lambda}{2}\sigma'^T G\sigma'-V\right)\right\rangle
-\tfrac12\sum_i\frac{f_i^2}{\langle e^{-5A}/Z_i\rangle}.
$$

The Einstein term gives $+20(A')^2$ after periodic integration by parts. The fixed-winding expression for the axions has no remaining explicit $\lambda$ dependence. Varying the shape at fixed profiles is an allowed metric variation and requires the exact equation

$$
\left\langle e^{5A}
\left[20(A')^2-\tfrac12 \sigma'^T G\sigma'\right]\right\rangle=0 .
$$

At leading order in a static marginal wave, the external metric constraint gives $A=V_A s^A/[2(\lambda_*+8)]$, where $s$ is the scalar amplitude. The exact background identity is $V_A(G^{-1})^{AB}V_B=32(1+d^2)$. Since $\lambda_*\ge20$ and $|d|\le1$, Cauchy–Schwarz implies

$$
20 A^2-\tfrac12 s^T Gs \ \le\ -\frac{9}{98}\,s^T Gs<0 .
$$

A nonzero static null vector has $s\ne0$ because the static axion block is positive. Shape variation therefore excludes a one-direction branch at quadratic order. As an independent check, the verifier solves the second-order averaged external and scalar equations at equal flux with sphere perturbations $\beta_1=-\beta_2=\epsilon\cos\theta$. The mean coefficients are $(A_0,\beta_{1,0}=\beta_{2,0},\gamma_0)=(-5/3,-1/6,-10/3)$. The remaining averaged Einstein constraint has coefficient $-40\epsilon^2$ in the convention used by the script.

## A necessary balance for several directions

Consider any smooth branch preserving the full external AdS and the two sphere rotation groups. At nonzero torus momentum, internal torus diffeomorphisms put the first-order metric in the transverse gauge used for the five-scalar block. The allowed invariant internal four-form has a constant horizontal component and one mixed torus-area component for each sphere. Thus the nonzero static modes at leading order belong to the static marginal shell of the scalar block. The homogeneous torus-shape directions can be subtracted as tangents to the product family.

At quadratic order, different wavevectors are orthogonal in the integrated shape equation. Rotation of a single wavevector gives the trace-free shape stress proportional to $u u^T-I/2$, where $u$ is its unit physical direction. The proportionality sign and its nonzero magnitude follow from the one-direction variation. The coefficient for a mode with fixed normalization is the same for every direction at the same $\lambda_*$ and flux ratio. Consequently the shape equation requires

$$
\sum_j w_j\left(u_j u_j^T-\tfrac12 I\right)=0,\qquad w_j>0
$$

for the occupied unoriented momentum axes. The weights include squared wave amplitudes. A single axis cannot cancel. For two axes, the sum is proportional to $I$ only if the axes are orthogonal and their weights agree. Three or more axes require a shell with at least three distinct unoriented equal-length lattice vectors. These conditions concern the static shape equation. They do not follow by looking only at the scalar masses with the shape prescribed externally.

## The quantized shell cannot balance

Let $Q$ be the positive binary quadratic form with determinant one for the normalized momentum lattice. A reciprocal lattice label $n$ has $\lambda(n)=4\pi^2 n^T Q n/a$, where $a=\mathcal A/L^2$ is the reference product torus area in AdS units.

At integer four-form periods the [product quantization relations](2026-11-16_D9_mtheory_uplift.md) imply that $\eta=(1+d)/2$ is algebraic. For nonzero $N_1,N_2$, square their ratio to obtain

$$
N_1^2(1-\eta)(1+\eta)^2-N_2^2\eta(2-\eta)^2=0 .
$$

The single-flux endpoints are algebraic as well. For a nonzero $N_1$ one has

$$
\frac{a}{\pi}=\frac{16|N_1|}{|N_0| k_2\sqrt{8\eta}},
$$

with the index-exchanged expression if $N_1=0$. Thus $a/\pi$ and $\lambda_*$ are nonzero algebraic numbers. Each resonant momentum must satisfy

$$
n^T Q n=q_*=\frac{a\lambda_*}{4\pi^2},
$$

which is a nonzero algebraic number divided by $\pi$, hence transcendental.

- Two orthogonal equal-length lattice covectors $n_1,n_2$ would have Gram matrix $q_* I$. Its determinant is $\det[n_1,n_2]^2$ because $\det Q=1$, forcing $q_*=|\det[n_1,n_2]|$ to be an integer.
- With three distinct equal-length axes, take the third covector to be $a_1 n_1+a_2 n_2$, with nonzero rational $a_1,a_2$. If the off-diagonal Gram entry of the first two covectors is $r$, the third equal-length condition gives $r/q_*=(1-a_1^2-a_2^2)/(2a_1a_2)$, which is rational. The Gram determinant then forces $q_*^2(1-(r/q_*)^2)=\det[n_1,n_2]^2$, again making $q_*$ algebraic.

Both kinds of balanced shell are impossible. Thus a static marginal mode at fixed integer flux is obstructed as a tangent to a modulated branch of this product. The calculation does not constrain a branch at finite amplitude, a branch that breaks the sphere symmetries, or theories where corrections lift the torus shape. The time-dependent BF instability remains as derived in the scalar calculation.

For the flux normalization see [Witten](https://arxiv.org/abs/hep-th/9609122). For genuine warped branches of other Freund–Rubin systems and the role of a nonlinear continuation test see [Lim](https://arxiv.org/abs/1202.3525) and [Kinoshita and Mukohyama](https://arxiv.org/abs/0903.4782).

Reproduce with `python analysis/toe_20261117_11D_static_bifurcation_obstruction.py`. The matching certificate is `data/toe_20261117_11D_static_bifurcation_obstruction.json`.
