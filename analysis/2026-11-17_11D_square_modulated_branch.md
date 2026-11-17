# A balanced square-torus AdS branch at detuned quantized flux

The [fixed-flux obstruction](2026-11-17_11D_static_bifurcation_obstruction.md) excludes a smooth bifurcation from any *quantized* homogeneous product in this sphere-singlet sector. It leaves open a finite-amplitude solution at nearby detuned flux. At equal mixed flux, two perpendicular waves on a square torus can balance the shape equation. Solving their quadratic backreaction gives a supercritical static branch at $\lambda>20$. Its smooth classical continuation contains integer flux ratios arbitrarily close to resonance. Independent spectral solves find a nonconstant solution at $(|N_0|,|N_1|,|N_2|)=(17,8,8)$ in dimensionless units.

## Reduced action and the constraints

Use the seven-dimensional Einstein-frame reduction on the two round spheres. Write $\beta_1=c+v$, $\beta_2=c-v$, and put the seven-dimensional metric in the form

$$
ds_7^2=e^{2A}ds_{\mathrm{AdS}_5,L=1}^2+\lambda^{-1}e^{2B}(dx^2+dy^2),
\qquad x,y\sim x,y+2\pi .
$$

The internal four-form is the sum of $u\,\omega_1\wedge\omega_2$ and the two sphere forms wedged with independent torus top forms. All its legs are internal, giving zero Chern–Simons source. The horizontal coefficient is constant, and the two mixed flux equations can be integrated at fixed periods. Use

$$
V=-24e^{-18c/5}\cosh(2v)+8e^{-48c/5},\qquad
X_\pm=e^{-5A+2B+12c/5\pm4v}.
$$

The two mixed flux densities relative to their background values are $X_\pm/\langle X_\pm\rangle$. Here the brackets are normalized torus averages. The dimensionless static action per reference torus volume becomes

$$
\begin{aligned}
\mathcal S={}&\left\langle -20 e^{3A+2B}-e^{5A+2B}V\right\rangle
-2\left(\langle X_+\rangle^{-1}+\langle X_-\rangle^{-1}\right)\\
&+\lambda\left\langle e^{5A}
\left[20|\nabla A|^2+10\nabla A\cdot\nabla B-\tfrac{36}{5}|\nabla c|^2
-4|\nabla v|^2\right]\right\rangle .
\end{aligned}
$$

The kinetic cross term follows from the conformal torus curvature $R_2=-2\lambda e^{-2B}\Delta B$ and periodic integration by parts. The normalized flux terms impose the mixed periods exactly. These equations are the two-derivative equations with both sphere isometries and all external AdS isometries.

Work with fields even under reflections of the coordinates in the scalar equations, invariant under the square quarter-turn, and with the combined symmetry of the half-period shift $(x,y)\mapsto(x+\pi,y+\pi)$ and $v\mapsto-v$. The quarter-turn is an orientation-preserving symmetry of the flux ansatz. The torus trace-free Einstein equation follows as well. With the form, scalar, external metric, and torus trace equations satisfied, the weighted internal trace-free Einstein residual $e^{5A}E_{ab}$ is divergence-free. In two-dimensional conformal coordinates this is a periodic holomorphic quadratic differential, hence constant. A square quarter-turn negates a constant trace-free two-tensor, forcing it to vanish. Both components of this constraint are independently evaluated in the spectral solve.

## Exact quartic and bifurcating solution

At $\lambda=20$ the static sphere-odd kernel in the specified symmetry class is one-dimensional, with

$$
v=\epsilon(\cos x+\cos y)+O(\epsilon^3).
$$

The [nonzero momentum determinant](2026-11-17_11D_unequal_flux_scalar_operator.md) shows that every other Fourier length has an invertible physical static operator. The projected zero-momentum even Hessian has determinant $4423680$. The homogeneous odd amplitude is excluded by the combined half-shift condition, and the trace-free constant torus moduli are excluded by the quarter-turn. The elliptic linearization in conformal variables has a nondegenerate principal matrix, with a mixed warp–conformal block and a nondegenerate sphere block. The signed quadratic action coefficient of the kernel is $4(20-\lambda)$, so varying $\lambda$ crosses it transversely.

The order-$\epsilon^2$ forcing of $A,B,c$ has the Fourier basis $1,\cos 2x+\cos 2y,\cos x\cos y$. Solving the nine linear backreaction equations and substituting gives the reduced action

$$
\mathcal S_{\mathrm{red}}=-8-4(\lambda-20)\epsilon^2
+\frac{36736}{459}\epsilon^4
+O\big(\epsilon^6+|\lambda-20|\epsilon^4\big).
$$

The quartic at frozen $A,B,c$ would be $-124$. The relaxed coefficient is positive. By the simple-eigenvalue bifurcation argument on this symmetry subspace, the analytic classical equations have a nearby branch with

$$
\lambda=20+\frac{18368}{459}\epsilon^2+O(\epsilon^4).
$$

Changing $\epsilon$ to $-\epsilon$ is a translation on the torus. In the proof one first uses real classical periods as continuous parameters. The square reference momentum at equal mixed flux is $\lambda=3\pi|N_0|/|N_1|$. Rational values of $|N_1|/|N_0|$ approach $3\pi/20$ from below, so integer flux data hit the finite-amplitude branch arbitrarily close to the product limit. This differs from a bifurcation at fixed quantized periods, which the previous shape argument excludes. Common integer rescaling of the periods raises all physical length scales in Planck units without changing these profiles. [Crandall and Rabinowitz on simple-eigenvalue bifurcation](https://www.sciencedirect.com/science/article/pii/0022123671900152) · [Lim on warped flux branches](https://arxiv.org/abs/1202.3525)

## Numerical check and the effective AdS Newton coefficient

At the quantized ratio $17:8:8$, $\lambda=20.0276531666$ and the numerically solved coefficient of $\cos x+\cos y$ in $v$ is approximately $0.02634240655$. Increasing the Fourier cutoff from four to seven changes this coefficient by less than $10^{-10}$. On the finer grid the maximum of the unprojected four variation residuals is below $7\times10^{-11}$ in the displayed units, and the maximum trace-free Einstein residual is below $10^{-12}$. This tests that particular ratio numerically. The local branch theorem provides exact existence for sufficiently close quantized ratios without specifying an explicit radius of convergence.

At matched periods and reference area, the inverse five-dimensional Newton coefficient relative to the product is $C=\langle e^{3A+2B}\rangle$. A constant variation of $A$ on a solution gives $\mathcal S_{\rm on}=-8C$. Hence the leading branch shift is

$$
C-1=\frac{4592}{459}\epsilon^4+O(\epsilon^6)>0 .
$$

The $17:8:8$ spectral solution gives $C-1\simeq4.7903\times10^{-6}$, close to the leading prediction $4.7773\times10^{-6}$. The dynamical stability calculation on this modulated solution remains open. In particular the equal-flux product has a homogeneous scalar at the BF bound, and the direction of its shift requires the physical fluctuation calculation on the new branch.

Reproduce with `python analysis/toe_20261117_11D_square_modulated_branch.py`. The output is `data/toe_20261117_11D_square_modulated_branch.json`.
