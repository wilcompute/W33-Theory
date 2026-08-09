# Part LXXXI — Normalized Triangle Dirac Involution

**Status:** theorem-grade structural extension  
**Date:** April 27, 2026

Part LXXX closed the \(L,S,Q\) representation triangle with three exact intertwiners:

\[
L_{15}\leftrightarrow S_{15},
\qquad
L_{24}\leftrightarrow Q_{24},
\qquad
S_{20}\leftrightarrow Q_{20}.
\]

This part packages the three edges into a single normalized Dirac operator on

\[
L\oplus S\oplus Q
=
40\oplus36\oplus45
=
121.
\]

## 1. Definition

Define

\[
\mathcal D=
\begin{pmatrix}
0 & B_c/\sqrt{18} & U_c/\sqrt{18}\\
B_c^T/\sqrt{18} & 0 & M_c/\sqrt{72}\\
U_c^T/\sqrt{18} & M_c^T/\sqrt{72} & 0
\end{pmatrix}.
\]

Here:

- \(B_c\) is the centered spread probe carrying \(L_{15}\leftrightarrow S_{15}\);
- \(U_c\) is the centered unique anti-line quotient probe carrying \(L_{24}\leftrightarrow Q_{24}\);
- \(M_c\) is the centered matching-parity matrix carrying \(S_{20}\leftrightarrow Q_{20}\).

## 2. Spectrum

The normalized triangle Dirac operator has spectrum

\[
\boxed{
\operatorname{Spec}(\mathcal D)
=
(+1)^{59},\;0^3,\;(-1)^{59}.
}
\]

Thus \(\mathcal D\) has rank

\[
118
\]

and kernel dimension

\[
3.
\]

## 3. Operator law

The square of \(\mathcal D\) is exactly the projector onto the zero-mean sector:

\[
\boxed{
\mathcal D^2
=
I-P_{\mathrm{mean},L}-P_{\mathrm{mean},S}-P_{\mathrm{mean},Q}.
}
\]

Therefore

\[
\boxed{
\mathcal D^3=\mathcal D.
}
\]

The minimal polynomial is

\[
\boxed{x(x^2-1).}
\]

## 4. Sector decomposition

The square decomposes into the three edge-sector projectors:

\[
\boxed{
\mathcal D^2
=
P_{L15\oplus S15}
+
P_{L24\oplus Q24}
+
P_{S20\oplus Q20}.
}
\]

The ranks are

\[
30,
\qquad
48,
\qquad
40.
\]

So

\[
\boxed{30+48+40=118=2(15+24+20).}
\]

The remaining kernel is exactly

\[
\boxed{3}
\]

mean modes, one for each module \(L,S,Q\).

## 5. Meaning

The full 121-dimensional carrier is now a finite Dirac involution:

\[
\boxed{
\mathcal D^2=1
\quad
\text{on the zero-mean sector}.
}
\]

It has equal positive and negative mode counts:

\[
\boxed{59+59}
\]

plus three zero modes.

This is the cleanest finite Dirac object produced so far by the W(3,3) program.

## 6. Structural compression

The entire chain

\[
\text{Parseval frame}
\to
\text{representation triangle}
\to
\text{closed intertwiners}
\]

compresses to

\[
\boxed{
\mathcal D^3=\mathcal D
\quad\text{on}\quad
L\oplus S\oplus Q.
}
\]

The normalized triangle Dirac operator is the current best candidate for the finite carrier Hamiltonian/Dirac skeleton of the W(3,3) theory.
