# Passes 2767–2771 — M36 factory, metaplectic class sensor, CX compiler, FPGA implementation packet, and remote SUM

## Pass 2767 — one physical factory for all 36 Witting resources

The 36 non-stabilizer Witting rays are not 36 unrelated optical circuits. In the canonical four-mode basis they form four nine-member families

\[
\frac1{\sqrt3}(0,1,-\omega^\mu,\omega^\nu),\quad
\frac1{\sqrt3}(1,0,-\omega^\mu,-\omega^\nu),
\]
\[
\frac1{\sqrt3}(1,-\omega^\mu,0,\omega^\nu),\quad
\frac1{\sqrt3}(1,\omega^\mu,\omega^\nu,0),\qquad \mu,\nu\in\mathbb F_3.
\]

Every ray therefore has one dark mode and three equal-amplitude active modes. The exact preparation compiler selects one of four dark modes, applies one shared balanced three-mode splitter, and applies four local phases from the sixth-root alphabet. The frozen 36-entry ROM reproduces every target ray up to global phase and independently recomputes the BT822 census

\[
8_{\rm deep}+24_{\rm mid}+4_{\rm shallow}=36.
\]

For \(\rho=(1-p)|m\rangle\!\langle m|+pI_4/4\), the target-overlap witness certifies non-stabilizerness below

\[
p_{\rm deep}<\frac{8-2\sqrt3}{9},\qquad
p_{\rm mid}<\frac{7-2\sqrt3}{9},\qquad
p_{\rm shallow}<\frac13.
\]

These are magic-witness boundaries, not distillation thresholds. M36 consists of ququart/two-qubit Witting states, whereas published five-qutrit and Reed–Muller protocols act on qutrit magic states. The controller types the resource as `M36_Q4_RAW`, performs preparation and witnessing, and refuses injection until a separately proved ququart code or verified encoding map is asserted.

## Pass 2768 — the minimal practical 34-class lift sensor

The five W33 permutation carriers produce only 15 signatures for the 34 conjugacy classes of \(\operatorname{Sp}(4,3)\). A permutation and its inverse always have the same cycle profile, so ordinary permutation-cycle carriers cannot close the inverse-class obstruction.

For any two-qutrit Clifford representative \(U_g\), define

\[
\Theta_k(g)=\frac{\operatorname{Tr}(U_g^k)^9}{\det(U_g^k)},\qquad k=1,2.
\]

The quotient is independent of the arbitrary global Clifford phase. The complete census is: five projective carriers 15 classes; projective carriers plus \(\Theta_1\), 30; \((\Theta_1,\Theta_2)\) alone, 33; projective carriers plus both shots, all 34. Constancy was checked across all 51,840 matrices.

## Pass 2769 — the centralizer compiler becomes executable

For

\[
C=C_{\operatorname{Sp}(4,3)}(\mathrm{CX})\cong C_6\times C_3\times S_3,
\qquad |C|=108,
\]

the right-coset space has 480 scheduling states. For every \(g\), choose the shortest representative \(r\) of \(gC\), write \(g=rc\), and use

\[
\boxed{g\,\mathrm{CX}=r\,\mathrm{CX}\,c},\qquad c\in C.
\]

The normalization table verifies this for all 51,840 inputs. Representative length has maximum six and mean 4.241666… . The compiler removes an average 2.555864… generators, with strict reduction for 50,577 elements. Counting only entanglers, the mean reduction is \(19/30\), up to three SUM gates. The 480 canonical cosets require 32 zero-SUM, 416 one-SUM, and 32 two-SUM representatives.

## Pass 2770 — complete FPGA implementation packet

The release contains synthesizable modules for the exact M36 ROM, fail-closed preparation/witness/mapping/injection pipeline, all eight Holonet opcodes including bidirectional SUM and all 144 products of \(D_{12}\), and the remote-SUM feed-forward controller. The exhaustive bench covers all 36 resources, both SUM directions, all 81 Pauli frames, all dihedral products, invalid operands, delayed acknowledgements, and all remote measurement outcomes.

The focused workflow targets an iCE40 HX8K TQ144 using Icarus, Yosys, nextpnr-ice40, and icetime. Local Python evidence is complete; RTL simulation, utilization, placement, timing, and physical power remain remote pending. The deterministic switching census is a technology-independent activity proxy, not watts.

## Pass 2771 — exact entanglement-assisted remote qutrit SUM

Alice and Bob share one maximally entangled frequency-qutrit pair \(|\Phi_3\rangle_{ab}\), while data occupy local time bins. Alice applies reverse SUM from data to link qutrit, measures and sends trit \(m\); Bob applies \(X^{-m}F^2\), direct SUM to his data, measures in the Fourier basis and sends trit \(n\); Alice records \(Z^n\). Every one of nine branches yields

\[
|x,y\rangle\longmapsto|x,y+x\pmod3\rangle.
\]

The verifier checks all nine basis inputs, all nine branches, and 32 random complex superpositions. Conditional on a heralded pair, all outcomes are accepted. Cost: one qutrit Bell pair and two classical trits.

The explicit rate model is

\[
R_{\rm gate}=R_{\rm pair}10^{-\alpha(L_A+L_B)/10}
\eta_{cA}\eta_{cB}\tau_A\tau_B\eta_{dA}\eta_{dB}.
\]

Using 8,200 s\(^{-1}\) only as an illustrative source input, a symmetric 60 km scenario with 0.2 dB/km loss and 0.8 coupling, 0.7 local transmission, and 0.8 detection per end gives about 104 heralded gates/s. This is a scenario, not a measurement. Likewise \(0.806\times0.92^2\simeq0.682\) is a component no-error weight, not process fidelity.

## Evidence

- 18/18 aggregate release checks passed.
- 5/5 focused Python regressions passed.
- All 51,840 lift-sensor and normalization inputs were checked.
- Both manuscript inserts compile standalone.
- Remote RTL, synthesis and P&R evidence is not counted until observed.
