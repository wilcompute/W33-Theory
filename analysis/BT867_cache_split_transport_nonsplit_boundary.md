# BT867 - Cache Addressing Is Split; Transport Memory Is Not

**Status: PROVEN** by the GAP and finite-field verifier
`analysis/bt867_cache_split_transport_nonsplit_boundary.py`, with evidence in
`data/bt867_cache_split_transport_nonsplit_boundary.json`.

BT859 found two 162-slot Bell-cache branches. The older packet-transport work
also found an exact 162-dimensional ternary extension. BT866 then exposed a
conjugate pair of 5-dimensional oriented-homology characters and left open the
tempting identification

\[
  162_L\stackrel{?}{\longleftrightarrow}5_\omega,
  \qquad
  162_R\stackrel{?}{\longleftrightarrow}5_{\omega^2}.
\]

BT867 refutes both identifications and replaces them with a stronger object.

## The cache branches are two copies of the same G-set

Let

\[
  H=3^3:S_4,
  \qquad |H|=648,
\]

be the line parabolic. GAP computes that both 162-point cache orbits have a
cyclic stabilizer of order four, and that the two stabilizers are conjugate in
\(H\). Therefore

\[
  \mathcal C_L\cong H/C_4\cong\mathcal C_R.
\]

The two cache permutation characters are equal. More sharply, restricting the
BT866 constituents to \(H\), **each** cache contains both conjugate 5-sectors
once and the 30-sector eight times:

\[
 \langle\mathbb C[\mathcal C_L],(5_\omega,5_{\omega^2},30)|_H\rangle
 =
 \langle\mathbb C[\mathcal C_R],(5_\omega,5_{\omega^2},30)|_H\rangle
 =(1,1,8).
\]

Thus left/right cache chirality is not an internal spectral label. It is the
multiplicity label of two isomorphic cache copies, and the outer Weyl
involution exchanges those copies.

## The common 81-base

The parabolic \(H\) has one conjugacy class of cyclic \(C_4\) subgroups. It has
81 members. For any cache stabilizer \(C_4\),

\[
  N_H(C_4)=D_8,
  \qquad
  N_H(C_4)/C_4=C_2.
\]

The stabilizer map gives an objectwise two-sheet cover

\[
  H/C_4\longrightarrow H/N_H(C_4)=H/D_8,
  \qquad 162\longrightarrow81.
\]

Both cache copies map onto the **same** 81 cyclic stabilizers, twice each. The
81 is therefore not another unexplained count: it is the canonical cache-route
base selected by normalizer geometry.

## The four-state fiber is genuinely dihedral

On the union \(\mathcal C_L\sqcup\mathcal C_R\), GAP computes

\[
 C_{\operatorname{Sym}(324)}(H)\cong D_8.
\]

This commutant has exactly 81 orbits, all of size four, and every such orbit
lies over one cyclic \(C_4\) stabilizer. Hence

\[
 \boxed{324=81\times4=81\times2_{\rm deck}\times2_{\rm cache}}
\]

is a fibration theorem, not a factorization coincidence. The two binary labels
carry the full symmetry of a square, \(D_8\), rather than only an abstract
\(C_2\times C_2\) label set.

## Why this is not the old 162-sector

On one two-sheet cache fiber, the deck transformation is

\[
 D=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

Over \(\mathbb F_3\), \(D^2=I\) and 2 is invertible, so the projectors

\[
 P_+=\frac{I+D}{2},\qquad P_-=\frac{I-D}{2}
\]

split the 162-dimensional cache module into two 81-dimensional eigenspaces.
Equivalently, \(D-I\) is rank-one and idempotent on each fiber:

\[
 (D-I)^2=D-I.
\]

The packet-transport fiber is categorically different. Its exact operator is

\[
 N=\begin{pmatrix}0&1\\0&0\end{pmatrix},
 \qquad N^2=0,
\]

and \(I+N\) has order three. Tensoring with the 81-dimensional logical sector
produces the non-split sequence

\[
 0\longrightarrow81\longrightarrow162\longrightarrow81\longrightarrow0.
\]

The cache deck and transport shift cannot be conjugate: one is semisimple and
split; the other is nilpotent and non-split. The equal number 162 names two
different primitives.

## Architecture consequence

The distinction supplies a clean hardware contract:

- the cache layer performs reversible **address selection** on a shared
  81-route base, with a four-state \(D_8\) fiber;
- the transport layer performs ternary **state propagation**, retaining a
  square-zero memory of the previous temporal sheet;
- routing choice and temporal update therefore cannot overwrite one another,
  because they live in different extension classes.

The local 324-slot cache cell is a dihedral address bus over 81 routes. The
independent 162-dimensional unipotent transport is its state-transition
operator. This is the first exact separation of the holonet's control plane
from its temporal data plane.
