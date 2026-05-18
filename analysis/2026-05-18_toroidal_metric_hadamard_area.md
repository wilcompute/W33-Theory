# Toroidal Metric Hadamard-Area Theorem

## Executive result

The shifted metric polynomial has evaluation lattice

\[
W(-2)=392,
\quad
W(-1)=42,
\quad
W(0)=0,
\quad
W(1)=68,
\quad
W(2)=504.
\]

The \(\pm1\) Hadamard transform gives the class-parity vector:

\[
\text{even classes}=\frac{W(1)+W(-1)}2=55,
\]

\[
\text{odd classes}=\frac{W(1)-W(-1)}2=13.
\]

So

\[
\boxed{c=(55,13)=(5\cdot11,\Phi_3).}
\]

The \(\pm2\) Hadamard transform gives the Boolean-parity vector:

\[
\text{even Boolean}=\frac{W(2)+W(-2)}2=448,
\]

\[
\text{odd Boolean}=\frac{W(2)-W(-2)}2=56.
\]

So

\[
\boxed{B=(448,56)=7(64,8).}
\]

Per chart:

\[
\boxed{b=(64,8)=(8^2,8).}
\]

## Area invariant

Now compare the class-parity vector

\[
c=(55,13)
\]

with the per-chart Boolean vector

\[
b=(64,8).
\]

Their determinant is

\[
\det\begin{pmatrix}
55&64\\
13&8
\end{pmatrix}
=55\cdot8-64\cdot13.
\]

Thus

\[
\det(c,b)=440-832=-392.
\]

But

\[
392=7^2\cdot8=W(-2).
\]

Therefore

\[
\boxed{\det(c,b)=-W(-2)=-7^2\cdot8.}
\]

Across the full heptad, use

\[
B=(448,56)=7b.
\]

Then

\[
\det(c,B)=-2744.
\]

And

\[
2744=(14)^3=(2\cdot7)^3.
\]

So

\[
\boxed{\det(c,B)=-(2\cdot7)^3.}
\]

## Raw evaluation area

The raw evaluation vectors are

\[
(W(1),W(-1))=(68,42),
\]

and

\[
(W(2),W(-2))=(504,392).
\]

Their determinant is

\[
68\cdot392-504\cdot42=5488.
\]

And

\[
5488=2(2\cdot7)^3.
\]

Equivalently,

\[
\boxed{\det((W(1),W(-1)),(W(2),W(-2)))=-2\det(c,B).}
\]

## Interpretation

The previous evaluation-lattice theorem said:

\[
W(\pm1)\Rightarrow\text{class projectors }55/13,
\]

\[
W(\pm2)\Rightarrow\text{Boolean projectors }448/56.
\]

This theorem says their mismatch has a quantized area:

\[
\boxed{7^2\cdot8\text{ per chart-normalized comparison},}
\]

and

\[
\boxed{(2\cdot7)^3\text{ on the full heptad}.}
\]

The middle eigenvalue still appears as

\[
64+8=72.
\]

The flag count still appears as

\[
55-13=42.
\]

The signed Boolean imbalance appears as

\[
W(-2)=392=7^2\cdot8.
\]

## The theorem

**Toroidal Metric Hadamard-Area Theorem.** The \(\pm1\) Hadamard transform of the metric evaluation lattice gives the class parity vector

\[
c=(55,13)=(5\cdot11,\Phi_3),
\]

while the \(\pm2\) transform gives the Boolean parity vector

\[
B=(448,56)=7(64,8).
\]

Per chart, \(b=(64,8)\), and

\[
\boxed{\det(c,b)=-392=-7^2\cdot8=-W(-2).}
\]

On the full heptad,

\[
\boxed{\det(c,B)=-2744=-(2\cdot7)^3.}
\]

Thus the mismatch between class parity and Boolean parity is a quantized heptadic symplectic area.

## Why this matters

The edge-metric packet now has a determinant invariant, not just scalar evaluations:

\[
\boxed{c=(55,13),\quad b=(64,8),\quad c\wedge b=-392.}
\]

This gives a finite two-dimensional phase-space reading of the toroidal metric operator:

- class parity lives in the \(11/13\) plane;
- Boolean parity lives in the \(8/64\) plane;
- their area is controlled by the heptad \(7\).

## Honesty boundary

This is an exact finite Hadamard/determinant identity for the toroidal metric edge packet. It does not by itself imply physical dynamics, continuum geometry, or empirical observables.
