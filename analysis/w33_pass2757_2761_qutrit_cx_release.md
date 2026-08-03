# Passes 2757–2761 — controlled-add hardware and W33 conjugacy resolution

## Pass 2757 — exact controlled-add / SUM gate

The computational instruction

\[
|p,f\rangle\mapsto |p,f+p\pmod 3\rangle
\]

is implemented and exhaustively checked on all nine computational basis states. Its
Pauli-frame action is checked on all 81 frame labels and agrees exactly with

\[
M_{\rm CX}=\begin{pmatrix}
1&0&0&0\\
0&1&0&-1\\
1&0&1&0\\
0&0&0&1
\end{pmatrix}\in\operatorname{Sp}(4,3).
\]

The gate has order three, \((M-I)^2=0\), and \(\operatorname{rank}(M-I)=2\).

## Pass 2758 — the fixed W33 Lagrangian line

The image and kernel of \(M-I\) coincide in one totally isotropic two-space. The
induced W33 cycle profiles are

\[
40\text{ points}:1^4 3^{12},\quad
40\text{ lines}:1^7 3^{11},\quad
160\text{ flags}:1^{10}3^{50},\quad
240\text{ edges}:1^6 3^{78}.
\]

The fixed points are exactly one line, and the fixed edges are exactly that line's six
\(K_4\) edges. The seven fixed lines are the axis plus two three-line pencils attached
at two axis points.

## Pass 2759 — conjugacy class resolved by geometry

The full generated group of order \(51{,}840\) contains \(720\) order-three elements
with rank-two square-zero nilpotent part. They split into two conjugacy classes:

\[
\begin{array}{c|c|c}
\text{line profile}&\text{class size}&\text{centralizer order}\\ \hline
1^1 3^{13}&240&216\\
1^7 3^{11}&480&108.
\end{array}
\]

Controlled-add is the \(480\)-class. Jordan type \(2+2\) is insufficient to identify it;
the six-line fixed fringe is the exact W33 class certificate.

## Pass 2760 — executable RTL and exhaustive regression

The release adds a synthesizable computational data path, a sequential Pauli-frame
tracker, an order-three chain, and an exhaustive SystemVerilog testbench. The testbench
covers the 9 basis states, all 81 frames, and all \(81^2\) frame pairs for preservation
of the symplectic form. The local Python suite passes 3/3. A focused GitHub Actions
workflow installs Icarus Verilog and reruns both the exact certificate and RTL simulation.
Remote CI is future evidence until observed.

## Pass 2761 — manuscript promotion and corrected evidence boundary

The Holonet wrapper reaches a host-independent theorem insert. It records the exact gate,
fixed geometry, conjugacy split, Bell-qutrit preparation, and

\[
\langle F_p,F_f,S_p,S_f,\operatorname{CX}_{p\to f}\rangle
=\operatorname{Sp}(4,3).
\]

The original release said no measured deterministic photonic qutrit SUM existed. Pass
2765 corrects that statement: Imany *et al.*, *npj Quantum Information* **5**, 59
(2019), experimentally implemented the same modulo-SUM truth table inside one photon,
using frequency as control and time as target, with qutrit computational-basis fidelity
\(0.92\pm0.01\). The remaining physical boundary is implementation-specific loss and
full process engineering, plus the separate protected \(M_{36}\) magic pipeline.

## Evidence

- 24 exact checks in the frozen JSON certificate.
- 3/3 local Python regressions.
- Standalone LaTeX insert compiled successfully.
- Local Icarus/Yosys tools were unavailable; the checked-in workflow supplies independent
  RTL execution and must not be described as passed until GitHub reports success.
