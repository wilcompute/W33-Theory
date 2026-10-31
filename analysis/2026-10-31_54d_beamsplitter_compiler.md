# Exact reciprocal beam-splitter compiler for the W33 54D transducer

Date: 2026-10-31. **Mathematical/circuit specification, not implemented hardware.**

Producer: analysis/w33_20261031_54d_beamsplitter_compiler.py
Certificate: data/w33_20261031_54d_beamsplitter_compiler.json
Regression: tests/test_w33_20261031_54d_beamsplitter_compiler.py

The already-certified perfect plus factor 7 and minus factor 6 of Pass 11062, carried through the U81 cocycle of October 1, are 81x81 real skew matrices F with 27 independent 3x3 weighted triangles each. Each triangle has absolute edge weights {1,2,3}, so F^3=-14F. This sequel to analysis/2026-10-31_five_front_geometry_pulse_bridge.md gives **a fully explicit two-mode interferometer compilation** of the ideal rank-54 pulse.

## Algebra and the canonical axis

Fix the three-mode skew block

\[
F_0=\begin{pmatrix}0&1&-3\\-1&0&2\\3&-2&0\end{pmatrix}.
\]

Its integer null vector is w=(2,3,1), with w.w=14. Define v=w/sqrt(14). A direct multiplication gives F_0^2=ww^T-14I, so

\[
U_0=I+F_0^2/7=2vv^T-I.
\]

This matrix has eigenvalues (1,-1,-1) and determinant +1: **a 180-degree SO(3) rotation about v** (equivalently the negative of a Householder plane reflection). It is implemented as e^(-i*pi*P), P=I-vv^T, with real-symmetric static Hermitian P. It is independent of the choice F or -F and therefore does not select a chiral orientation.

## Four beam splitters and a phase stage

Define real Givens rotations R_12(theta) and R_23(phi), acting on mode pairs (1,2) and (2,3), with

- cos(theta)=2/sqrt(14), sin(theta)=sqrt(10)/sqrt(14);
- cos(phi)=3/sqrt(10), sin(phi)=1/sqrt(10).

Set V=R_23(phi) R_12(theta), so V e1=v. Consequently,

\[
U_0=V\,{\rm diag}(1,-1,-1)\,V^T.
\]

Reading right to left, the **exact chronological circuit** consists of

1. R_23(-phi)
2. R_12(-theta)
3. pi phase on mode 2 and mode 3
4. R_12(+theta)
5. R_23(+phi)

Hence an upper bound of **four conventional real two-mode mixing operations, two pi phase shifters, five parallel circuit stages**, per independent triangle. This is not asserted to be the minimum number of beam splitters, because different optical gate libraries and phase conventions have different native gates.

## Whole 81-mode compilation

For every actual weighted triangle F, sorted by its actual three mode indices, the exact integer null vector is

\[
w=(F_{12},-F_{02},F_{01})
\]

with magnitudes {1,2,3}. A signed permutation S sends canonical (2,3,1) to this w. Thus the actual block is exactly S U_0 S^T. Local port permutations and +/- phase gauge choices are exported for every one of the 27 triangles in each orientation.

The checker verifies the local integer identity F^2=ww^T-14I and the numerical beam-splitter matrix equality with absolute error below 2e-14 on all 54 actual blocks. The 27 triples within each orientation partition all 81 modes. Rank(U-I)=54 is established by the integer projector proof in the parent packet; Pass 11062 supplies the independent 54-dimensional quotient projection certificate.

## What this does and does not achieve

This replaces a seemingly nonreciprocal 3-mode weighted hopping primitive with a *specific reciprocal linear-optical five-stage circuit* for the **orientation-blind exact retyping pulse**. It does not implement the distinct orientation-sensitive quarter-turn (which uses +/-iF), establish any loss/crosstalk budget or pass a laboratory calibration, derive an emergent spacetime, or choose physical CP/handedness.

The core *next experimental falsifier* is to attempt all 27 parallel three-mode transformations and measure the full 81-mode transfer matrix, relative phases, crosstalk, insertion loss and the 54-rank defect after projecting to the certified logical quotient.
