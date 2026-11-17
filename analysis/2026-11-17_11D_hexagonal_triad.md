# Resonant three-wave AdS branches on a hexagonal torus

The two-derivative product admits a different local modulation when its torus is hexagonal. Three shortest reciprocal vectors obey a sum relation, so their Fourier amplitudes couple cubically. For unequal mixed flux the cubic is nonzero, giving a signed branch on both sides of the static resonance. The square calculation's two quartic reversals do not occur in this leading hexagonal coefficient. This concerns the sphere-singlet static equations and leaves the dynamical instability to be tested on the resulting finite-amplitude solutions.

Use the seven-dimensional fixed-period action in the [square branch calculation](2026-11-17_11D_square_modulated_branch.md), with its unequal potential and flux weights from the [unequal branch calculation](2026-11-17_11D_unequal_square_branch.md). The reference inverse torus metric is proportional to the determinant-one hexagonal form. Coordinates of period $2\pi$ can be chosen so that the normalized momentum norm is $n^2+m^2-nm$. The vectors $(1,0),(0,1),(1,1)$ all have norm one. They form the same hexagonal root arrangement as $A_2$, with a resonant vector sum. This is a statement about the reciprocal lattice. A coupling to the repo's particle gauge algebra would need an additional construction.

Let $C=\cos x+\cos y+\cos(x+y)$, $d=(p^2-q^2)/(p^2+q^2)$ and $\Lambda=-4+4\sqrt{36+5d^2}$. In the profile order $(A,B,c,v)$, the static kernel is

$$
w=\left(0,\frac{16d(\Lambda+32)}{\Lambda(\Lambda+28)},
\frac{20d}{3(\Lambda+28)},1\right).
$$

Take the leading profile to be $\epsilon wC$. Exact Fourier convolution gives $\langle C^2\rangle=\langle C^3\rangle=3/2$. For a local exponential term with weight $n$ and exponent vector $e$, the cubic is $n(e\cdot w)^3/4$. The inverse averages of the fixed-period flux terms give the same cubic sign because their first harmonic averages to zero. The gradient cubic vanishes because $w_A=0$. The order-two backreaction cannot change this coefficient since its quadratic contraction with the kernel is zero. The reduced action therefore begins as

$$
\mathcal S=-8+\kappa(\lambda-\Lambda)\epsilon^2+c_3\epsilon^3
+O\left(\epsilon^4+|\lambda-\Lambda|\epsilon^3\right),
$$

$$
\kappa=-\frac{12(\Lambda+4)}{\Lambda+28},\qquad
c_3=\frac{384d(\Lambda^2+54\Lambda-64)}{(\Lambda+28)^2}.
$$

The verifier reduces this expression exactly using $80d^2=\Lambda^2+8\Lambda-560$. Since $\Lambda\ge20$, the remaining factor is positive. Thus $c_3$ vanishes only at equal mixed flux. With $\epsilon$ normalized to the first harmonic of $v$, the nonconstant branch satisfies

$$
\lambda-\Lambda=
\frac{48d(\Lambda^2+54\Lambda-64)}{(\Lambda+4)(\Lambda+28)}\epsilon
+O(\epsilon^2).
$$

Restricting to rotation by 60 degrees and inversion fixes the constant trace-free torus moduli and selects one invariant fundamental shell. In this sector the static kernel is simple and the detuning derivative is nonzero. The other nonzero Fourier lengths do not meet the static threshold. At nonzero $d$, the homogeneous radius sector has no zero mass. The same elliptic simple-eigenvalue construction used for the square branch therefore gives a local analytic curve. For reference, see [Crandall and Rabinowitz](https://www.sciencedirect.com/science/article/pii/0022123671900152) and [Lim's warped flux branches](https://arxiv.org/abs/1202.3525).

The signed amplitude has a geometric meaning. A translation can shift the three wave phases, but their resonant phase combination is invariant. It cannot reverse all three signs simultaneously because the third vector is the sum of the first two. For $d\ne0$, the two sides of resonance correspond to opposite signs of this invariant triad amplitude. General three-wave resonance is established pattern-formation theory. The coefficient here is computed from this particular constrained flux action. [Cross and Hohenberg](https://doi.org/10.1103/RevModPhys.65.851)

At equal flux the cubic vanishes, and the fourth moment is $\langle C^4\rangle=45/8$. Solving the quadratic backreaction in all forced shells of squared length $0,1,3,4$, with the kernel component held fixed, changes the frozen quartic from $-246$ to $5923/9$. Thus the small-imbalance detuning has the joint expansion

$$
\lambda-\Lambda(d)=59d\epsilon+\frac{5923}{27}\epsilon^2
+O\left(d^3\epsilon+d^2\epsilon^2+d\epsilon^3+\epsilon^4\right).
$$

Sphere exchange maps $(d,\epsilon)$ to $(-d,-\epsilon)$ and restricts the orders of the remainder. This predicts a nondegenerate local fold for small nonzero $d$, with leading detuning $-93987d^2/23692$ and signed amplitude $-1593d/11846$. A two-parameter continuation would test the explicit finite-amplitude pair near this equal-flux limit. The quartic calculation uses the exact Fourier shell decomposition $C^2=3/2+C+C_{\sqrt3}+C_2/2$, with each nonconstant shell having norm squared $3/2$ in the normalized average.

The $A_2$ hexagonal identification is already in the repo's [packing discussion](w33_BREAKTHROUGH_309_sphere_packing_substrate.py), and the [overview](../W33_FOR_EVERYONE.tex) describes $A_2$ zero-sum root triangles and maps to cubic supports. The present calculation does not identify those finite root triangles with these spacetime momentum modes. It supplies a flux-action coefficient for the momentum triad, leaving such a map to be constructed.

At area $a=\mathcal A/L^2$, the fundamental reference momentum on the hexagonal torus is $\lambda=8\pi^2/(\sqrt3 a)$. The mixed period ratio $4/3$ gives $\eta=4/5$, hence $d=3/5$. Two integer flux assignments test opposite sides of the branch.

| Periods $(|N_0|,|N_1|,|N_2|)$ | $\lambda-\Lambda$ | Signed first harmonic of $v$ |
| --- | ---: | ---: |
| $(127,68,51)$ | $-0.0250030$ | $-0.0007054235051$ |
| $(262,140,105)$ | $+0.0166413$ | $+0.0004688070865$ |

The spectral solver retains complete 60-degree Fourier orbits and solves all four profile equations. Refining the reciprocal cutoff from four to six and the grid from 30 to 42 changes either amplitude by less than $10^{-14}$. The fine-grid unprojected scalar and metric residuals are below $5\times10^{-14}$ and the three trace-free coordinate components are below $10^{-16}$. The tensor trace is contracted with the nonorthogonal hexagonal inverse metric. These are finite-resolution numerical solutions, supported by the analytic local branch argument. The calculation imposes the hexagonal conformal structure and the two sphere rotation groups.

A separate equal-flux numerical control at periods $(68,37,37)$ gives amplitude $0.001927136168$ and detuning $0.0008146110152$. Its ratio of detuning to squared amplitude is $219.3439$, close to the predicted limiting $5923/27=219.3704$. The same refinement and local Einstein checks pass there. This independently tests the equal-flux quartic after the cubic has vanished.

The earlier [fixed-quantized-flux bifurcation obstruction](2026-11-17_11D_static_bifurcation_obstruction.md) remains applicable. Here each sample is detuned from its homogeneous static threshold and has finite amplitude. At each fixed nonzero rational mixed-period ratio, integer horizontal-to-mixed scale ratios can approach the critical area from both directions. Common rescaling can make the compactification large in Planck units. For fixed unequal flux, the homogeneous product has a BF violation, which persists on sufficiently nearby branches by continuity. This construction expands the set of static saddles. Determining a stable endpoint still requires further work.

At equal flux the homogeneous BF mode also moves downward on the hexagonal branch. At order $\epsilon^2$, its mean equation uses only the homogeneous quadratic backreaction and pairs of a Fourier wave with its opposite. All three axes have the same length and the same first-order response as the two axes of the [square BF calculation](2026-11-17_11D_square_branch_BF_shift.md). The quadratic homogeneous backreaction scales with $\langle C^2\rangle$, and different axes average to zero in this projection. Therefore the coefficient is $3/2$ times the square result,

$$
m^2 L^2=-4-\frac{8820}{43}\epsilon^2+O(\epsilon^4).
$$

Sphere exchange at equal flux sends $\epsilon$ to $-\epsilon$ and makes this mass expansion even. The cubic triad is relevant to the static branch at unequal flux. It does not enter the equal-flux quadratic BF shift. Both the equal and fixed-unequal-flux branches are unstable sufficiently near their homogeneous limits.

Run `python analysis/toe_20261117_11D_hexagonal_triad.py`. Its matching output is `data/toe_20261117_11D_hexagonal_triad.json`.
