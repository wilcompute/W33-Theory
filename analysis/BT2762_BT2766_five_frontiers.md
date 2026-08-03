# Passes 2762–2766 — transpose reversal, CX centralizer, full gate atlas, physical SUM compiler, and complete ISA

## Pass 2762 — transpose reverses the entangler, but no new entangler is needed

In the standard Pauli-frame coordinates \((x_p,z_p,x_f,z_f)\), the left/right
transpose from Pass 2732 is represented by the anti-symplectic involution

\[
T=\begin{pmatrix}
0&0&1&0\\
0&0&0&-1\\
1&0&0&0\\
0&-1&0&0
\end{pmatrix},
\qquad T^2=I,
\qquad T^{\mathsf T}JT=-J.
\]

It normalizes \(\operatorname{Sp}(4,3)\) but is not an element of it. Conjugating the
controlled-add gate gives the reverse controlled-add:

\[
T\,\mathrm{CX}_{p\to f}\,T^{-1}
=\mathrm{CX}_{f\to p}
=\begin{pmatrix}
1&0&1&0\\
0&1&0&0\\
0&0&1&0\\
0&-1&0&1
\end{pmatrix}.
\]

The outer operation is not required in the hardware gate library. The exact local-Fourier
identity is

\[
\boxed{
\mathrm{CX}_{f\to p}
=(F_pF_f^{-1})\,\mathrm{CX}_{p\to f}\,(F_p^{-1}F_f)
}.
\]

Thus both directions use one physical SUM gate plus local tritters. The anti-symplectic
transpose exchanges twenty of the thirty-four symplectic conjugacy classes in ten pairs
and fixes fourteen classes. The controlled-add class is fixed setwise.

## Pass 2763 — the order-108 centralizer is \(C_6\times C_3\times S_3\)

The full exact centralizer of controlled-add is

\[
C_{\operatorname{Sp}(4,3)}(\mathrm{CX})
\cong C_6\times C_3\times S_3,
\qquad |C|=108.
\]

This is certified constructively: the JSON freezes explicit matrix generators for the
\(C_6\), \(C_3\), and \(S_3\) factors, proves that the central factors generate the
order-18 center, proves that the \(S_3\) complement intersects the center trivially, and
proves that their product contains all 108 elements. Additional invariants are

\[
|Z(C)|=18,
\qquad |C'|=3,
\qquad
\#\{g:|g|=1,2,3,6\}=1,7,26,74.
\]

The group action explains the fixed fringe from Pass 2757. The \(S_3\) factor acts
regularly on the six external fixed lines. The center preserves the two three-line
pencils and rotates each pencil by a 3-cycle. Hence the centralizer is an executable
scheduler for the stationary CX geometry, not merely a centralizer order.

## Pass 2764 — complete geometric gate-class atlas

The verifier constructs all of \(\operatorname{Sp}(4,3)\), all 34 conjugacy classes,
and the five canonical projective carriers:

\[
40\ \text{points},\quad 40\ \text{lines},\quad 160\ \text{flags},\quad
240\ \text{edges},\quad 1620\ \text{apartments}.
\]

For every class the frozen atlas records an exact representative matrix, class size,
centralizer order, matrix order, trace, \(\operatorname{rank}(g-I)\), and the complete
cycle profile on all five carriers. It also records the inverse class, the central
\(-I\) lift, and the transpose image.

A necessary decoder boundary emerges. The five projective cycle profiles yield only
15 distinct signatures for 34 symplectic classes. Projective geometry necessarily
forgets the central sign, and several inverse/transpose pairs remain projectively
indistinguishable. Therefore the canonical decoder is two-stage:

1. use point/line/flag/edge/apartment profiles to select one of 15 geometric signatures;
2. use the exact lift metadata and representative-class table to select the symplectic
   class.

The atlas partitions all \(51{,}840\) matrices with no omission or overlap.

## Pass 2765 — correction and physical time-frequency SUM compiler

The evidence boundary in Passes 2757–2761 was too strong. It stated that the literature
did not supply a measured deterministic photonic qudit SUM gate matching the controller.
That is false.

Imany *et al.*, *npj Quantum Information* **5**, 59 (2019), DOI
`10.1038/s41534-019-0173-8`, experimentally implemented deterministic two-qudit logic
inside one photon using frequency as the control qudit and time as the target qudit.
For qutrits their SUM operation is exactly

\[
|f,t\rangle\longmapsto |f,t+f\pmod3\rangle.
\]

Their qutrit implementation used three time bins of 3 ns width and 6 ns center spacing,
three frequency bins separated by 380 GHz, a chirped fiber Bragg grating with
\(-2\,\mathrm{ns/nm}\) dispersion to produce one- and two-bin frequency-conditioned
delays, and an 18 ns switched wraparound path. They reported computational-basis SUM
fidelity \(0.92\pm0.01\). Applied to
\((|0\rangle+|1\rangle+|2\rangle)|0\rangle/\sqrt3\), the gate produced the qutrit Bell
state and certified entanglement of formation at least \(1.19\pm0.12\) ebits.

The direct Holonet compiler is therefore:

\[
|p\rangle_{\rm logical}\mapsto |p\rangle_{\rm frequency},
\qquad
|f\rangle_{\rm logical}\mapsto |f\rangle_{\rm time},
\]

followed by the published time-frequency SUM network. The exact nine-mode permutation is
frozen as

\[
3p+f\longmapsto 3p+(f+p\bmod3).
\]

This closes the physical principle and supplies a measured qutrit implementation. It does
not close source efficiency, insertion-loss engineering, fault tolerance, or the magic
state injection threshold.

## Pass 2766 — all eight Holonet instructions now have a digital contract

The ISA is encoded in three bits:

| opcode | instruction | exact digital semantics |
|---:|---|---|
| `000` | \(F_p\) | past-frame Fourier update |
| `001` | \(F_f\) | future-frame Fourier update |
| `010` | \(S_p\) | past quadratic-phase update |
| `011` | \(S_f\) | future quadratic-phase update |
| `100` | CX | direction operand selects \(p\to f\) or \(f\to p\) |
| `101` | \(\sigma^5=Z\) | register operand increments the selected Z frame |
| `110` | \(D_{12}\)-mirror | left multiplication by \(r^a m^b\), \(r^6=m^2=1\), \(mrm=r^{-1}\) |
| `111` | \(M_{36}\)-magic | typed request for ray 0–35 with BT822 grade ROM; retirement waits for `magic_ack` |

The magic opcode is intentionally a resource handshake. It preserves the canonical BT822
ray order and exports the exact three-grade census \(8+24+4\) as deep/mid/shallow metadata.
The finite substrate identifies 36 distinguished rays, but the repo still lacks a certified optical preparation,
distillation, injection, decoder, and threshold. Encoding an invented non-Clifford
unitary would conceal that gap.

The SystemVerilog release contains combinational basis-SUM and frame-step blocks, the
complete \(D_{12}\) multiplication law, and a sequential ISA controller. The exhaustive
remote testbench covers 18 bidirectional basis vectors, 3888 frame/instruction vectors,
and all 144 \(D_{12}\) products. The local exact suite passes 27/27 certificate checks
and 4/4 focused regressions.

## Artifacts

- `analysis/bt2762_five_frontiers.py`
- `data/PART_BT2762_BT2766_FIVE_FRONTIERS_results.json.gz`
- `data/PART_BT2764_SP43_GEOMETRIC_GATE_CLASS_ATLAS.json.gz`
- `rtl/w33_pass2762_holonet_isa.sv`
- `rtl/tb_w33_pass2762_holonet_isa.sv`
- `tests/test_bt2762_five_frontiers.py`
- `analysis/BT2764_gate_class_atlas_w33_insert.tex`
- `analysis/BT2766_five_frontiers_holonet_insert.tex`

## Evidence boundary

The group, geometry, class atlas, direction-reversal identities, D12 protocol, and digital
ISA transitions are exact finite statements. The published time-frequency experiment
establishes a deterministic single-photon qutrit SUM implementation with measured
fidelity. The remaining universality gap is specifically the physical \(M_{36}\) magic
resource pipeline and its fault-tolerance threshold.
