# BT1688 — Exact H1 Character Certificate

## Result

The generated projective symplectic action has order

\[
25920.
\]

The W33 Levi graph has

\[
80\text{ vertices},\qquad 160\text{ edges},\qquad \dim H_1=81.
\]

For each group element, use the chain-character formula

\[
\chi_{H_1}(g)=f_E(g)-f_V(g)+1,
\]

where \(f_E(g)\) is the number of fixed incidence edges and \(f_V(g)\) is the
number of fixed Levi vertices.

The value distribution is

\[
\begin{array}{c|c}
\chi & \#g \\
\hline
-3 & 810 \\
-1 & 3240 \\
0 & 16640 \\
1 & 5184 \\
9 & 45 \\
81 & 1
\end{array}
\]

The exact square sum is

\[
810\cdot9+3240\cdot1+16640\cdot0+5184\cdot1+45\cdot81+1\cdot6561=25920.
\]

Therefore

\[
\langle \chi_{H_1},\chi_{H_1}\rangle
=\frac{25920}{25920}=1.
\]

So the \(81\)-dimensional Levi \(H_1\) character is irreducible over \(\mathbb C\)
for the generated projective symplectic action.  This removes the conditional
from BT1683's Schur step.

## Boundary

This is an exact character certificate for the generated projective symplectic
action.  The script `analysis/bt1688_exact_h1_character_irreducibility.py`
regenerates the group and verifies the square sum.
