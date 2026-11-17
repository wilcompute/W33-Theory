# The balanced square branch lowers the BF-saturating mass

The [balanced modulated AdS branch](2026-11-17_11D_square_modulated_branch.md) solves the static two-derivative equations near the equal-flux square product. Its dynamical sphere-singlet mode inherited from the homogeneous sphere-radius difference has

$$
m^2L^2=-4-\frac{5880}{43}\epsilon^2+O(\epsilon^4),
$$

where $v=(\beta_1-\beta_2)/2=\epsilon(\cos x+\cos y)+O(\epsilon^3)$. Thus the branch is unstable for sufficiently small nonzero amplitude. This calculation tracks one physical scalar and includes the induced metric and flux perturbations. It uses the same two-derivative equations and AdS normalization as the static branch, with no estimate for higher-derivative terms.

## The induced modes at first order

Use the sphere-singlet perturbation sector invariant under the square rotation. At zero amplitude the BF mode is $\delta v=\psi$ with $\Box_{\mathrm{AdS}_5}\psi=-4\psi$, other fields zero. The mode is odd under sphere exchange combined with the half-period shift. This excludes a homogeneous metric, mean radius, or three-form perturbation in this sector. At the product no nonzero torus Fourier mode is at BF, since the smallest nonzero $\lambda=20$ lies above the exact threshold 12. Constant torus-vector Wilson components are excluded by the square rotation.

To first order in $\epsilon$, the two induced Fourier directions decouple. For each direction reduce along the transverse circle as in the [five-scalar operator](2026-11-17_11D_unequal_flux_scalar_operator.md). The flux perturbation has a leg on that circle and gives no Chern–Simons source. The part of the metric transverse to the chosen circle remains unsourced in this projection. At second order, products of different directions have no torus average. Extra nonzero Fourier components at this order do not enter the mean projection. The mixed flux periods are held fixed, so the perturbation of their torus integrals is zero.

For one direction let $k=\sqrt{20}$, set $u=(1,-1,0)^T$ and $f=(2,2)^T$, and use the axial gauge of the transverse-circle reduction. The induced scalar $\delta\sigma$ has amplitude $\epsilon s\cos(kx)\psi$ on top of $u\psi$. The induced axions have amplitudes $\epsilon a_i\sin(kx)\psi$. The six-dimensional external metric at this order is $\epsilon\cos(kx)(A\,g_{\mu\nu}\psi+B\nabla_\mu\nabla_\nu\psi)$. With $z=-4$, the $x\mu$ and traceless $\mu\nu$ equations give

$$
B=3A/20,\qquad f^Ta=4k(A+B)+8k .
$$

The extra $8k$ comes from the scalar kinetic stress $u^TG u=8$ between the background wave and the homogeneous fluctuation. The scalar equations use the mass Hessian derivative along the background wave as a source. For the flux part, this derivative is computed at fixed background axion current, so $Z_i(\partial_x\chi_i)^2$ picks up relative perturbation $-(\nabla Z_i\cdot u)\epsilon\cos(kx)$. In the linearized axion equation, $Z_i\partial_x\chi_i$ is constant through first order and gives no direct Fourier source from $u\psi$. Solving the five linear amplitude equations gives

$$
s=(-82/129,-82/129,-304/129),\quad
a=(-106\sqrt5/215,-106\sqrt5/215),\quad
(A,B)=(-84/43,-63/215).
$$

The solver separately verifies the trace and $xx$ Einstein constraints with these amplitudes.

## Mean second-order equation

Uplift the induced metric from six to seven dimensions. Its transverse-circle logarithmic radius amplitude is $b_y=s_3+4s_1/5$. The seven-dimensional full metric trace is $H_7=5A+zB-b_y$, and its internal two-dimensional trace for this direction is $3b_y/2$. The static background's second-order homogeneous coefficients are

$$
(A_0,B_0,c_0)=(-13/30,13/20,-11/18).
$$

The homogeneous sphere-odd equation in seven dimensions is the mean projection of

$$
8\Box_7 v = V_v+\tfrac14\sum_i (Z_i)_{,v}F_i^2 .
$$

The direct warp change to $\Box_7\psi$ gives $8A_0$ at order $\epsilon^2$ after factoring out $\psi$. The variation of $\Box_7$ on the background sphere wave gives $10H_7$ after amending it by the metric trace and averaging both directions. The total internal derivative in that term integrates to zero. For the flux term the normalized background energies are $E_\pm=2e^{-10A_7}/(Z_\pm\langle X_\pm\rangle^2)$. The part of their variation linear in $\delta F_{xy}$ averages to zero at this order because $Z_\pm F_{xy,\pm} e^{-4B_7}$ has no first harmonic and the perturbed periods vanish. The flux perturbations still enter through the equations that determine $s,A,B$.

The three resulting coefficients, before extracting the $m^2$ shift, are

| Term | Coefficient in the averaged equation |
| --- | ---: |
| Geometric correction to $\Box_7 v$ | $-39196/645$ |
| Variation of the sphere potential derivative | $-26784/43$ |
| Variation of the flux term | $-617408/645$ |

The required shift is the sum of the last two rows divided by eight, minus the first row. The verifier also linearizes the divergence form *before* dividing by the volume density. In that version the internal total derivative drops out directly, and the background weight multiplying $m^2$ has no net quadratic shift because $3A_0+2B_0=0$. It reproduces the same $-5880/43$ coefficient. Translation on the square sends $\epsilon$ to $-\epsilon$, giving an even mass expansion.

The leading deficit at the numerically constructed $17:8:8$ ratio is about $0.095$ in AdS units. This number is an asymptotic estimate at that ratio. The exact sign statement applies sufficiently close to the product. At any fixed sufficiently small detuning, common integer multiplication of the periods raises $L/\ell_p$ and leaves the two-derivative deficit unchanged, giving parametric separation from local higher-derivative corrections. This checks one instability and leaves open the endpoint, the spectrum at larger detuning, and backgrounds that require a different compactification ansatz.

See [Martin and Reall](https://arxiv.org/abs/0810.2707) for the BF criterion and coupled fluctuation analyses in a distinct class of 11D AdS backgrounds.

Reproduce with `python analysis/toe_20261117_11D_square_branch_BF_shift.py`. The output is `data/toe_20261117_11D_square_branch_BF_shift.json`.
