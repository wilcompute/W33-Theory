# 2026-10-08 — A homodyne kurtosis witness for one W33 current-square interaction

**Scope:** Quantitative **two-mode continuous-variable (CV) toy control** derived from a *single* current of Pass11769. It is not a physical implementation of the global 160-current Hamiltonian, not a two-qutrit time/frequency compiler, and not an experimentally measured signal. Gaussian gates alone cannot implement the quartic unitary exactly.

For one W33 incidence \(e\), Pass11769 gives \(J_e=(V_e\cdot q+a)(U_e\cdot p+a)\), where \(\|V_e\|^2=\|U_e\|^2=39/20\), \(U_e\cdot V_e=0\), and \(a=1/\sqrt{20}\). Introduce independent canonical quadratures \(X=(V_e\cdot q)/g\), \(P_Y=(U_e\cdot p)/g\), with \(g^2=39/20\), so \([X,P_Y]=0\). Then

\[
J_e^2=g^4(X+\alpha)^2(P_Y+\alpha)^2,\quad
\alpha=1/\sqrt{39},\quad g^4=(39/20)^2.
\]

An evolution \(e^{-i\tau J_e^2}\) is therefore \(e^{-i\theta(X+\alpha)^2(P_Y+\alpha)^2}\) at \(\theta=(39/20)^2\tau\). Start both modes in uncorrelated canonical vacuum states, \(\mathrm{Var}(X)=\mathrm{Var}(P_X)=\mathrm{Var}(P_Y)=1/2\).

Conditioned on the input \(P_Y=z\), the output \(P_X\) is exactly Gaussian: its mean is \(-2\theta\alpha(z+\alpha)^2\) and its variance is \(1/2+2\theta^2(z+\alpha)^4\). **Unconditionally**, it is a non-Gaussian mixture over \(z\sim N(0,1/2)\). A direct exact rational Gaussian-moment calculation gives

\[
\boxed{\begin{aligned}
\operatorname{Var}(P_X) &= \frac12+\frac{5207}{3042}\theta^2,\\
\kappa_4(P_X) &= \frac{618440}{6591}\theta^4>0,
\end{aligned}}
\]

where \(\kappa_4=\mathbb E[(P_X-\mathbb EP_X)^4]-3\operatorname{Var}(P_X)^2\). As a negative control, Gaussian initial states evolved by **Gaussian unitaries** have \(\kappa_4=0\) in all single-quadrature homodyne distributions. The quartic W33 single-edge law thus has a precise non-Gaussian measurement signature **if** its gate can be implemented.

Illustrative **idealized** signals (no loss, finite squeezing, detector noise or model error):

| \(\tau\) | \(\theta\) | \(\kappa_4\) | excess kurtosis \(\kappa_4/\mathrm{Var}^2\) |
|---:|---:|---:|---:|
| 0.02 | 0.07605 | 0.003139 | 0.01207 |
| 0.03 | 0.114075 | 0.015889 | 0.05825 |
| 0.05 | 0.190125 | 0.122604 | 0.38835 |

For orientation only, using the asymptotic **Gaussian-null** excess-kurtosis variance \(24/N\) yields a 5-sigma shot-scale estimate \(N\approx 600/\gamma_2^2\): about \(4.1\) million, \(1.8\times10^5\), and \(4.0\times10^3\) samples respectively. **These are not validated power calculations**: the actual non-Gaussian alternative has different estimator variance and technical-noise bias.

### Hardware and interpretation gates

1. A single \(e^{-it J_e}\) is Gaussian (bilinear quadratures); the current-*square* \(e^{-it J_e^2}\) is quartic and **not** Gaussian. The exact implementation requires a non-Gaussian resource/nonlinearity, not merely passive time/frequency mixing.
2. Homodyne tomography must measure calibrated fourth cumulants and a matched Gaussian-control circuit with identical measured variance, squeezing and optical loss. Independent calibration of \(\alpha\) and \(\theta\) is required.
3. The W33 full Hamiltonian is a *sum of noncommuting* quartic edge terms, so this experiment does not by itself validate that sum or its spectral gap.
4. The two CV modes are **not** automatically the two qutrit time/frequency bins of the Holonet paper: exact CCR cannot exist in nine dimensions.

Related implementation literature: Budinger et al., *All-optical quantum computing using cubic phase gates*, Phys. Rev. Research **6**, 023332 (2024), DOI 10.1103/PhysRevResearch.6.023332; Anteneh et al., *Deep reinforcement learning for near-deterministic preparation of cubic- and quartic-phase gates*, Phys. Rev. Research **8**, L012048 (2026), DOI 10.1103/wkfp-tf74. These establish proposals/resources for nonlinear gates, **not this device or this W33 signal**.
