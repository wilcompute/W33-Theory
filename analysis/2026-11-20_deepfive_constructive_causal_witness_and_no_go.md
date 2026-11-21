# Five-front TOE audit: constructive linear causal witness, flux-index constraint, drift falsifier and W33 coupling nonselection

**2026-11-20, America/New_York.** Intake master: \`03523a2d1f8a18369ecbce73b4d109bf04e6ee22\`. All evidence here is derived mathematics, explicit finite computation or seeded numerical simulation. **No laboratory hardware, singular-G2 charged Dirac operator, physical anomaly-inflow completion or unfitted BSM prediction was obtained.** The quantum switch, twisted Dirac index theorem and lattice-gauge Wilson actions are established prior art.

## 1. An explicit linear causal witness — not just rank-one reasoning

For the normalized ideal quantum-switch process state \`P=|psi><psi|\` on the 64-dimensional tensor product \`A_in,A_out,B_in,B_out,F_target,F_control\`, define

\[
S=(255/256)I_{64}-P.
\]

For a normalized process \`sigma_AB\` with definite order A-before-B, no backward signaling from B to A is allowed. The normalized Hermitian probe
\`D_BA=J_A(measure-1-and-reprepare-0) tensor [J_B(replace-1)-J_B(replace-0)] tensor I_F\`
has \`||D_BA||_infty=1\` and \`Tr(D_BA sigma_AB)=0\`. The coherent ideal switch instead has \`Tr(D_BA P)=1/8\`. The analogous \`D_AB\` witnesses the opposite definite order, also with ideal expectation \`1/8\`.

For either definite order, trace distance from \`P\` is at least \`1/16\`. The Fuchs–van de Graaf inequality for pure P then gives \`Tr(P sigma)<=1-(1/16)^2=255/256\`. This fidelity bound is linear and hence applies to **all convex mixtures** of the two definite orders:

\[
\forall \sigma_{\rm causal\,sep},\quad \operatorname{Tr}(S\sigma)\ge 0,\qquad
\operatorname{Tr}(SP)=-1/256.
\]

The calculation verifies both backward-signaling probes, 160 independent random pure fixed-order processes, and the dephased definite-order mixture. It reconstructs the projector from **634 nonzero six-qubit Pauli coefficients** (L1 norm \`2.96875\`), with max matrix residual below \`3e-17\`. This deliberately weak witness detects \`vP+(1-v)P_deph\` only for \`v>127/128=0.9921875\`. Published SDP witnesses are much more dephasing-robust. The process-Pauli decomposition is *not automatically a laboratory measurement*: physical implementation needs trusted process instruments and a Choi reconstruction.

## 2. One-photon optical switch: calibrate central gates, probe noncentral ones

The original seven settings with two qutrit Weyl gates are scalar-commutator pairs. Their known-gate 18-mode transfer factors **exactly** into a target unitary times a two-path control phase, with matrix residual \`2.5e-16\`. These central phase fringes therefore do not, on their own, establish black-box indefinite order.

We constructed a distinct unitary test: \`A=X tensor I3\`, \`B=diag(1,exp(0.4i),exp(-0.4i)) tensor I3\`. Its relative-order \`K=(BA)^dagger(AB)\` has \`|Tr K/9|=0.8465243330\` and \`||K-(Tr K/9)I||_F^2=2.5505689821\`. Across nine distinct basis inputs, the control-port probabilities span \`0.1121771423\`; a target-independent two-path phase cannot match all nine. This is an executable optical network *model*, not a physical photonic experiment.

## 3. Chirality: a charge-polynomial necessary condition

For the standard \`E6 27 -> 16_(+1)+10_(-2)+1_(+4)\` and one common rank-r internal bundle E on flat T4, twisted by a charge-q line bundle \`L^q\`, Atiyah–Singer gives

\[
I(q)=\int_{T^4}ch(E)e^{q c_1(L)}|_4=A+Bq+Cq^2,
\]
where \`A=int ch2(E)\`, \`B=int c1(E)c1(L)\`, and \`C=(r/2)int c1(L)^2\`.

The isolated Spin10×U1psi anomaly kernel requires \`I(1)=I(-2)=I(4)\`. Subtracting the three charges yields \`3B-3C=0\` and \`-3B-15C=0\`, **hence \`B=C=0\` exactly**. Pure q² abelian flux cannot produce three anomaly-complete 27s in this common-bundle class.

A conditional topological construction uses an auxiliary SU2 bundle with \`c1(E)=0, c2(E)=-3\`, trivial L; it has \`A=3\` and equal indices \`(3,3,3)\`. This *inputs* three through a Chern number; it is **not** a selected vacuum, Hermitian–Yang–Mills solution, singular-G2 compactification or physical prediction.

## 4. Drift falsifier in the centrality certificate

With a fixed independently warranted unitary promise in d=9, \`||K-(Tr K/d)I||^2_F=d(1-|TrK/d|^2)\`. For phase-locked test contrast \`2p_test-1=g_test*r+b\` and a trusted calibration \`2p_cal-1=g_cal\`, reference/test gains need not agree.

Use exact Clopper–Pearson lower/upper intervals for test/reference (joint 99% via union bound), and externally established bounds \`|g_test-g_cal|<=Delta_g\`, \`|b|<=b_max\`, target trace-norm error \`epsilon_prep\`. Set
\`g_test_up=min(1,max(0,2p_cal_upper-1)+Delta_g)\` and
\`r_lower=max(0, min(1,(2p_test_lower-1-b_max)/g_test_up-epsilon_prep))\`.
Then \`d*(1-r_lower^2)\` is the conservative squared noncentrality upper bound under these assumptions.

At test \`r=.97\` (true squared defect \`0.5319\`), calibration gain \`0.94\`, test gain \`0.98\`, and tolerance norm \`0.25\`, each of **400 seeded** simulated datasets had 150,000 accepted calibration plus 150,000 accepted test measurements. Assuming zero drift generated **400/400 false centrality certificates**; allowing the correct independently justified drift bound \`0.04\` generated **0/400**. This is synthetic evidence of a logical calibration loophole, not observed hardware behavior.

## 5. W33 incidence cannot select a gauge coupling on its own

Construct all 40 symplectic projective points and 40 isotropic lines to obtain the actual degree-four 80-vertex, 160-edge W33 Levi graph. Extract an eight-edge cycle. Assign Z3 link variables and the gauge-invariant single-loop action \`exp(beta Re W)\`, where W is the product around that cycle. Enumerating all \`3^8=6561\` assignments gives precisely \`3^7\` configurations per holonomy, hence

\[
Z(\beta)=3^7(e^\beta+2e^{-\beta/2}),\qquad
\langle\mathrm{Re}W\rangle_\beta={e^\beta-e^{-\beta/2}\over e^\beta+2e^{-\beta/2}}.
\]

With **the same W33 graph and the same Z3 group**, the expectation is 0 at beta=0, 0.5371576811 at beta=1, and 0.8641644978 at beta=2. The derivative is the strictly positive variance of Re W. Graph topology thus does **not** select a unique coupling or Wilson observable; a microscopic action and parameter-selection principle are extra physical requirements.

**Bonus:** one graph edge per exchange tick does not determine an absolute speed: \`speed=(physical length/edge)/(physical duration/tick)\`. Dimensional normalization remains additional input.

## Reproduction and scientific boundaries

The exact scripts, full frozen JSON certificates and 24 focused new tests have been assembled as a downloadable research packet alongside this report. The new scripts import \`analysis/toe_20261120_fivefront_plus_bridge.py\` from the previous commit. Combined with that existing 16-test baseline, **40/40 focused tests pass** in the server-side Python environment.

The explicit witness is a deliberately weak analytic construction for an established quantum-switch phenomenon, not a newly discovered form of causality. The gauge and chirality models are constrained *toy sectors*, not a solved TOE. **No new parameter-free physical observable beyond standard quantum mechanics or known gauge theory has been produced.**

**Literature:** Araújo et al. NJP 17 (2015) 102001, https://doi.org/10.1088/1367-2630/17/10/102001; Branciard et al. Scientific Reports 6 (2016) 26018, https://www.nature.com/articles/srep26018; PRX Quantum 5 (2024) 010325, https://doi.org/10.1103/PRXQuantum.5.010325; twisted Dirac index, https://academicweb.nd.edu/~pmnev/f19/atiyah_singer.pdf.

### Five independent next gates

1. Implement the noncentral 18-mode input-sensitive circuit and calibrate path/environment losses, not just central W33 fringes.
2. Build a genuine charged singular-G2/ADE Dirac problem with complete anomaly inflow and a dynamically selected three-family vacuum.
3. Put externally established positive gain-drift, bias, state-preparation and CPTP promises into a preregistered finite-shot confidence budget.
4. Tighten the causal witness with an SDP dual certificate and compile it into genuinely implementable trusted process instruments.
5. Specify a microscopic action selecting beta and a dimensionful scale, derive an unfitted observable, and compare with independent experimental data.
