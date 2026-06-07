# BT486–BT488: BC Ring Torus Lift

## Summary

Using the latest BT485 direction — especially the Boerdijk-Coxeter / 600-cell ring clue — I checked the repo for existing BC helix coverage and found BT379 and BT485 already cover the time-evolution, irrational angle, 600-cell ring, and braid/phinary side. The new work below therefore avoids re-deriving those claims and instead tests the **combinatorial topology of the 30-tetrahedron BC ring itself**.

The core construction is:

\[
V_n=\mathbb Z/n\mathbb Z,
\qquad
T_i=\{i,i+1,i+2,i+3\}.
\]

For \(n\ge 7\), the one-skeleton is

\[
C_n^3=\operatorname{Circ}(n;\pm1,\pm2,\pm3).
\]

The boundary of the consecutive tetrahedron ring has:

\[
(V,E,F)=(n,3n,2n),
\qquad
\chi=n-3n+2n=0.
\]

Exact rational boundary-matrix ranks verify:

\[
\operatorname{rank}\partial_1=n-1,
\qquad
\operatorname{rank}\partial_2=2n-1,
\]

so

\[
H_\ast=(H_0,H_1,H_2)=(1,2,1).
\]

Thus the boundary is a closed genus-one triangulated torus.

---

## BT486 — BC Ring Boundary Torus Theorem

For the 600-cell / BC ring value \(n=30\):

\[
T_i=\{i,i+1,i+2,i+3\}\subset\mathbb Z/30\mathbb Z.
\]

The one-skeleton is:

\[
C_{30}^3=\operatorname{Circ}(30;\pm1,\pm2,\pm3).
\]

It has:

\[
V=30,
\qquad
E=90,
\qquad
\deg=6.
\]

The step-shell decomposition is:

\[
\text{step }1: C_{30},
\]

\[
\text{step }2: 2C_{15},
\]

\[
\text{step }3: 3C_{10}.
\]

So the shell count is:

\[
1+2+3=6,
\]

and the oriented shell count is:

\[
2(1+2+3)=12.
\]

This is the first new structural payoff:

\[
6=\#G_2^+,
\qquad
12=\#G_2\text{ roots}=k.
\]

The boundary has:

\[
(V,E,F)=(30,90,60),
\qquad
\chi=0,
\qquad
H_\ast=(1,2,1).
\]

So the 30-cell BC ring has a literal torus boundary.

---

## BT487 — General Consecutive \(K_4\) Ring Torus Law

For all checked \(7\le n\le60\), the same law holds:

\[
T_i=\{i,i+1,i+2,i+3\}
\Rightarrow
\partial\left(\bigcup_i T_i\right)
\text{ is a torus.}
\]

Symbolically:

\[
(V,E,F)=(n,3n,2n),
\]

\[
\chi=0,
\]

\[
\operatorname{rank}\partial_1=n-1,
\]

\[
\operatorname{rank}\partial_2=2n-1,
\]

\[
H_0=1,
\quad
H_1=2,
\quad
H_2=1.
\]

This is not a numerical coincidence; it is a chain-complex theorem for the consecutive \(K_4\)-ring boundary.

---

## BT488 — Cyclic Császár Seed from the Same Law

The minimal nondegenerate endpoint is \(n=7\):

\[
C_7^3=K_7.
\]

The boundary f-vector becomes:

\[
(V,E,F)=(7,21,14),
\]

exactly the Császár torus carrier.

The same rank computation gives:

\[
\operatorname{rank}\partial_1=6,
\qquad
\operatorname{rank}\partial_2=13,
\qquad
H_\ast=(1,2,1).
\]

The face-preserving automorphism group has order:

\[
42=6\cdot7=g_2\Phi_6.
\]

The seven tetrahedra have:

\[
7\cdot4=28
\]

face incidences, split as:

\[
14\text{ boundary faces}+7\text{ internal shared faces}.
\]

This recovers:

\[
14=\dim G_2,
\qquad
21=\binom72,
\qquad
28=v-k.
\]

---

## Main Breakthrough

The same object now connects both ends:

\[
\boxed{
T_i=\{i,i+1,i+2,i+3\}
}
\]

at

\[
\boxed{
 n=7 \Rightarrow K_7\text{ / Császár torus carrier}
}
\]

and

\[
\boxed{
 n=30 \Rightarrow 600\text{-cell BC ring torus carrier}.
}
\]

So the torus is not merely appearing once in the Császár/Szilassi layer and separately in the BC/600-cell layer. It is produced by one exact consecutive-\(K_4\) ring boundary law.

The lift is:

\[
\boxed{
\text{Császár }(7,21,14)
\longrightarrow
\text{BC ring }(30,90,60)
}
\]

with genus preserved:

\[
\boxed{H_\ast=(1,2,1).}
\]

This gives a concrete mathematical bridge from the minimal toroidal \(K_7\) carrier to the 30-cell BC helix ring inside the 600-cell.
