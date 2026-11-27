# The full shared tick logarithm is nonlocal, yet still loses cycle connectivity

The factorially weighted local cumulant model leaves open the behavior of the actual shared-label transfer. Here the logarithm of that full transfer has a cut-and-rejoin operator cost that grows at least linearly in cycle length. Even so, its thermal trace leaves enough weight on fragmented graphs that connectivity still vanishes. This distinction matters when judging whether thermodynamic graph weights can be inferred from an effective Hamiltonian's locality.

## Model and an extensive operator witness

Use the repository's full shared-label operator \(K_l=L^{-1}\sum_a A_a^{\otimes l}\), with \(L=120\), \(A_a=s I+(1-s)P_a\), and \(0<s<1\). Each \(P_a\) is a rank-three two-qutrit tick projector. The assignment under test is one independent shared label per connected cycle. The dimensionless operator of a component is \(H_l=-\log K_l\). See the [original shared-label thermal construction](2026-11-27_elementary_exchange_dynamics_five_fronts.md).

Take \(\psi=|00\rangle\) and \(\phi=|++\rangle\). Under each of these states the possible projector expectations are \(0,1/3,1\). The ticks with expectation one on the computational state lie in the nonzero pure-phase Weyl directions. The ticks with expectation one on the Fourier state lie in the nonzero pure-shift directions. These sets are disjoint.

On the product vector \(\Psi=\psi^{\otimes m}\otimes\phi^{\otimes m}\), put the first block on one cycle and the second on another. In either homogeneous block choose a tick with expectation one. Since \(K_m\ge A_a^{\otimes m}/L\), operator monotonicity of the logarithm gives an expected energy at most \(\log L\) in each block. Compare to one joined \(2m\)-cycle on the same product vector. Every summand of \(K_{2m}\) contributes at most \(u^m\) to its expectation, with \(u=(1+2s)/3<1\): at least one of the two states has projector expectation at most \(1/3\). Scalar Jensen applied to the spectral measure of \(K_{2m}\) then implies

\[
\langle H_{2m}-(H_m\otimes I+I\otimes H_m)\rangle_\Psi
\ \ge\ m\log(1/u)-2\log L.
\]

In particular, this rule cannot be represented on these cycles by the previous summable consecutive-window Hamiltonian, whose difference under rejoining two cycles is uniformly bounded. The witness concerns the full shared-label rule per connected component. It does not show that a distinct tick propagation model with local label updates has this nonlocality.

## A bulk-normalized thermal bound for every positive power

At inverse-temperature parameter \(p>0\) for \(H_l\), the matter trace is \(\operatorname{Tr}K_l^p\). Write \(Z_p=\operatorname{Tr} A_a^p=3+6s^p\), independent of the choice of label. Uniformly in \(l\),

\[
c_p\;\le\; \frac{\operatorname{Tr} K_l^p}{Z_p^l}\;\le\; C_p.
\]

For \(p\ge1\), use \(c_p=L^{-p}, C_p=1\). The lower bound follows from \(K_l\ge A_a^{\otimes l}/L\) and eigenvalue monotonicity. The upper bound follows from convexity of the Schatten \(p\)-norm. For \(0<p\le1\), use \(c_p=1,C_p=L^{1-p}\), by concavity of the trace power and Rotfel'd trace subadditivity, respectively. At \(p=1\) the ratio equals one exactly. [Trace subadditivity for positive operators](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/223D29F61734BD21EA58FE540B333224/S0008439500007438a.pdf/subadditivity_inequalities_for_compact_operators.pdf)

At fixed total site count \(n\), multiplying the matter traces over components contributes a common \(Z_p^n\), which cancels from probabilities. A Wilson weight \(q>0\) per cycle then gives residual weights \(w_l=q\operatorname{Tr}(K_l^p)/Z_p^l\) in \([qc_p,qC_p]\). The connected contribution is at most \(C_p/c_p\) times its counterpart at the constant fugacity \(qc_p\), and the total partition coefficient is at least that of the constant-fugacity model. Thus the connected probability tends to zero at fixed \(p,s,q\). This proof uses the full trace over the component Hilbert space. It does not assume the occupation conservation of the pair-swap model.

## Exact decay exponent at power two

The repository's tick overlaps give \(\operatorname{Tr}(P_a P_b)\) equal to 3 for identical labels, 0 for distinct outcomes on the same direction, and 1 for different projective directions. Their ordered-pair counts are 120, 240 and 14040. Thus \(\operatorname{Tr}(K_l^2)\) is the average of \(\operatorname{Tr}(A_a A_b)^l\) over these ordered pairs. The diagonal has one-site trace \(Z_2\); both off-diagonal traces are strictly smaller for \(s<1\). It follows that \(w_l=q/L+O(\rho^l)\), with \(\rho<1\) at any fixed \(0<s<1\). The graph generating function is \(\exp(\sum_{l\ge3} w_l z^l/(2l))\), a factor \((1-z)^{-q/(2L)}\) times an analytic nonzero factor near \(z=1\). Consequently the connected probability decays as a positive constant times \(n^{-q/(240)}\). At the example Wilson weight \(q=(1+2e^{-3})/3\), the exponent is only 0.00152719. The limiting statement can therefore coexist with a substantial connected probability at finite size. The distinct limit \(s=1\) restores the ordinary Wilson weights. [Singularity analysis](https://doi.org/10.1137/0403019)

Run the Python verifier with one BLAS thread. It constructs all 120 projectors, checks the mixed-state overlap witness, reproduces the power-two formula by direct eigenvalue calculations through three registers, and evaluates the cycle generating function through 4096 sites.
