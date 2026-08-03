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

## Hardware boundary

The RTL is a synthesizable controller/data-path model. It proves ternary arithmetic,
order three, and symplectic frame transport. It does **not** prove that a bare catalog
EOM realizes a deterministic loss-tolerant photonic two-qutrit gate. Existing experiments
support high-fidelity electro-optic qutrit tritters and time-bin qubit entangling gates, while
recent high-dimensional time-bin work supports qutrit preparation and measurement; a
platform-specific qutrit SUM fidelity/loss budget remains an experimental obligation.

## Artifacts

- `analysis/bt2757_qutrit_cx_w33_lagrangian_unipotent.py`
- `data/PART_BT2757_QUTRIT_CX_W33_LAGRANGIAN_UNIPOTENT_results.json`
- `rtl/w33_pass2757_qutrit_cx.sv`
- `rtl/tb_w33_pass2757_qutrit_cx.sv`
- `tests/test_bt2757_qutrit_cx_w33.py`

## External anchors used for the hardware boundary

- E. Hostens, J. Dehaene, and B. De Moor, *Phys. Rev. A* **71**, 042315
  (2005): modular/symplectic qudit Clifford formalism and the SUM gate.
- H.-H. Lu *et al.*, *Phys. Rev. Lett.* **120**, 030502 (2018): electro-optic
  frequency-bin qutrit tritter with high process fidelity.
- H.-P. Lo *et al.*, *Phys. Rev. Applied* **13**, 034013 (2020): process-tomographic
  time-bin controlled-phase/CNOT gate at the qubit level.
- F. Ghafari *et al.*, *Phys. Rev. Lett.* **134**, 180802 (2025): arbitrary
  high-dimensional time-bin state preparation/measurement and certified
  single-photon polarization-time entanglement.

These sources support the single-qutrit and time-bin component technologies. They do not
supply a measured deterministic photonic qutrit SUM gate matching this exact controller,
which is why that claim is excluded from the certificate.
