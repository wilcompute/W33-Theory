# Pass 2757 — qutrit controlled-add and its exact W33 fixed geometry

## Result

The missing two-register Clifford instruction is now executable and certified. On the
computational basis it is the qutrit controlled-add gate

\[
\operatorname{CX}_{p\to f}\lvert p,f\rangle
=\lvert p,f+p\pmod 3\rangle.
\]

On Pauli-frame coordinates \((x_p,z_p,x_f,z_f)\in\mathbb F_3^4\), conjugation is

\[
(x_p,z_p,x_f,z_f)\longmapsto
(x_p,z_p-z_f,x_f+x_p,z_f),
\]

with exact symplectic matrix

\[
M_{\rm CX}=\begin{pmatrix}
1&0&0&0\\
0&1&0&-1\\
1&0&1&0\\
0&0&0&1
\end{pmatrix}.
\]

The verifier checks all 81 Pauli frames directly, not only the four generators. It also
checks

\[
M_{\rm CX}^{3}=I,
\qquad
(M_{\rm CX}-I)^2=0,
\qquad
\operatorname{rank}(M_{\rm CX}-I)=2,
\qquad
M_{\rm CX}^{T}JM_{\rm CX}=J.
\]

The rank matters terminologically: this is a rank-two symplectic unipotent of Jordan type
\(2+2\), not a rank-one symplectic transvection.

## Fixed-geometry theorem

The image and kernel of \(M_{\rm CX}-I\) coincide. They are a two-dimensional totally
isotropic subspace of \(\mathbb F_3^4\), hence one projective W33 line. The induced action
on the canonical carriers has cycle census

\[
\begin{array}{c|c}
\text{carrier}&\text{cycle profile}\\ \hline
40\ \text{points}&1^4\,3^{12}\\
40\ \text{lines}&1^7\,3^{11}\\
160\ \text{flags}&1^{10}\,3^{50}\\
240\ \text{collinearity edges}&1^6\,3^{78}.
\end{array}
\]

The four fixed points are exactly the axis line. The six fixed edges are exactly its
\(K_4\) edges. The seven fixed lines consist of the axis plus six external fixed lines;
the latter form two three-line pencils attached at two distinguished axis points.

This gives a literal W33 routing interpretation for the first entangling ISA instruction:
its stationary geometry is not an arbitrary four-point set but a Lagrangian line together
with a rigid \(3+3\) fixed-line fringe.

## Conjugacy-class resolution

Enumerating all \(51{,}840\) matrices in the generated symplectic group reveals a
necessary refinement. There are \(720\) elements with order three,
\(\operatorname{rank}(M-I)=2\), and \((M-I)^2=0\), but they split into two classes:

\[
\begin{array}{c|c|c|c}
\text{line action}&\text{class size}&|C_{\operatorname{Sp}(4,3)}(M)|&\text{fixed lines}\\ \hline
1^1 3^{13}&240&216&1\\
1^7 3^{11}&480&108&7.
\end{array}
\]

The controlled-add gate lies in the \(480\)-class. Thus the Jordan type \(2+2\) and
the fixed projective line do not determine the conjugacy class; the six-line fixed
fringe does. The W33 line carrier supplies an exact class identifier that is invisible
from the nilpotent rank alone.

## Bell-qutrit preparation and completeness

The same gate closes the paper's preparation equation:

\[
\operatorname{CX}_{p\to f}(F_3\otimes I)\lvert 00\rangle
=\frac1{\sqrt3}(\lvert00\rangle+\lvert11\rangle+\lvert22\rangle),
\]

whose reduced density is \(I_3/3\). Together with the two local Fourier and phase
generators, exact closure gives

\[
\left\langle F_p,F_f,S_p,S_f,\operatorname{CX}_{p\to f}\right\rangle
=\operatorname{Sp}(4,3),
\qquad |\operatorname{Sp}(4,3)|=51840.
\]

The repository already had this abstract closure in BT825 and the optical Bell-qutrit
build sheet in BT1337. This pass supplies the missing executable data path, Pauli-frame
path, exhaustive tests, and W33 permutation certificate.

## Corrected hardware boundary

The RTL is a synthesizable controller/data-path model. It proves ternary arithmetic,
order three, and symplectic frame transport, but by itself it does not establish optical
loss or process fidelity.

The original release incorrectly stated that no measured deterministic photonic qudit
SUM implementation existed. Imany *et al.*, *npj Quantum Information* **5**, 59
(2019), DOI `10.1038/s41534-019-0173-8`, implemented deterministic two-qudit modulo-SUM
logic within one photon using frequency as the control qudit and time as the target. Their
qutrit operation is exactly

\[
|f,t\rangle\mapsto|f,t+f\pmod3\rangle,
\]

with reported computational-basis fidelity \(0.92\pm0.01\). Applied to a frequency
superposition and the zeroth time bin, it produced
\((|00\rangle+|11\rangle+|22\rangle)/\sqrt3\) and certified entanglement of formation
at least \(1.19\pm0.12\) ebits.

Thus the controller has a direct physical compiler when the logical control register is
encoded in frequency and the logical target register in time. Remaining obligations are
source efficiency, insertion-loss optimization, full process characterization in the
chosen implementation, fault tolerance, and the separate \(M_{36}\) magic pipeline.

## Artifacts

- `analysis/bt2757_qutrit_cx_w33_lagrangian_unipotent.py`
- `data/PART_BT2757_QUTRIT_CX_W33_LAGRANGIAN_UNIPOTENT_results.json`
- `rtl/w33_pass2757_qutrit_cx.sv`
- `rtl/tb_w33_pass2757_qutrit_cx.sv`
- `tests/test_bt2757_qutrit_cx_w33.py`

## External anchors

- E. Hostens, J. Dehaene, and B. De Moor, *Phys. Rev. A* **71**, 042315
  (2005): modular/symplectic qudit Clifford formalism and the SUM gate.
- H.-H. Lu *et al.*, *Phys. Rev. Lett.* **120**, 030502 (2018): electro-optic
  frequency-bin qutrit tritter with process fidelity \(0.9989\pm0.0004\).
- P. Imany *et al.*, *npj Quantum Information* **5**, 59 (2019): deterministic
  single-photon time-frequency two-qudit gates and the measured qutrit modulo-SUM gate.
- F. Ghafari *et al.*, *Phys. Rev. Lett.* **134**, 180802 (2025): arbitrary
  high-dimensional time-bin state preparation/measurement and certified
  single-photon polarization-time entanglement.
