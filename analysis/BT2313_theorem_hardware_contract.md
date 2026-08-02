# Pass 2313 — theorem-derived hardware contract

The committed 36-lane spread-mixer masks are decoded directly into their
adjacency matrix \(A\). The executable contract verifies

\[
A=A^\mathsf T,\qquad A\mathbf1=15\mathbf1,\qquad
A^2=9I+6J.
\]

Thirty-six integer probes span the 35-dimensional mean-zero space and satisfy

\[
A^2x=9x.
\]

The contract also exhausts all 1,152 input transitions of the single-\(J\)
phase controller:

\[
(p,c,s_4,s_6,r)\mapsto(p',c').
\]

Its finite register map has kernel

\[
\{(0,0),(2,3)\},
\]

so 48 abstract \(C_4\times C_6\) register states collapse to the canonical
24-state \(C_{12}:C_2\) image exactly as the representation theorem predicts.

This is a semantic golden-vector layer for simulation, formal assertions, and
future synthesis runs. It deliberately makes no timing, power, or fabricated
device claim.
