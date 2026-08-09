# Part LXXIII — Exact Parseval Measurement Frame

**Status:** theorem-grade structural extension  
**Date:** April 27, 2026

This part sharpens the spread/anti-line channel discovered after the Payne-sheaf and triad-Dirac analysis.  The result is an exact finite measurement frame for the 40-dimensional line module of W(3,3).

## 1. Correct centering

Let `B` be the `40 x 36` incidence matrix from true W(3,3) lines to spreads, and let `R` be the `40 x 90` incidence matrix from true lines to anti-lines.

The correct spread density is

\[
\frac{360}{40\cdot36}=\frac14,
\]

not `1/10`.  The anti-line density is

\[
\frac{1440}{40\cdot90}=\frac25.
\]

Therefore the correctly centered probes are

\[
B_c=B-\frac14J,
\qquad
R_c=R-\frac25J.
\]

## 2. Parseval frame theorem

The centered spread and anti-line probes satisfy

\[
\boxed{
\frac{B_cB_c^T}{18}+\frac{R_cR_c^T}{36}
=
I-\frac{J}{40}.
}
\]

Adding the mean channel gives the full identity resolution

\[
\boxed{
\frac{J}{40}
+
\frac{B_cB_c^T}{18}
+
\frac{R_cR_c^T}{36}
=
I.
}
\]

So the natural incidence probes give an exact Parseval frame for the 40-dimensional line module.

## 3. Signal-processing form

For a line signal `x in R^40`, define

\[
\Phi(x)=
\left(
\frac{1}{\sqrt{40}}\mathbf 1^Tx,
\frac{1}{\sqrt{18}}B_c^Tx,
\frac{1}{6}R_c^Tx
\right).
\]

Then

\[
\boxed{\|\Phi(x)\|^2=\|x\|^2.}
\]

On the zero-mean subspace, the map

\[
x\mapsto
\left(
\frac{1}{\sqrt{18}}B_c^Tx,
\frac{1}{6}R_c^Tx
\right)
\]

is an exact isometry.

## 4. Integer signed probes

Define

\[
B_4=4B-J,
\qquad
R_5=5R-2J.
\]

Then `B_4` has entries `+3,-1`, while `R_5` has entries `+3,-2`.  They are exactly orthogonal:

\[
\boxed{B_4^TR_5=0.}
\]

Their spectra are

\[
\operatorname{Spec}(B_4B_4^T)=288^{15},0^{25},
\]

and

\[
\operatorname{Spec}(R_5R_5^T)=900^{24},0^{16}.
\]

## 5. Meaning

The line module is resolved as

\[
\boxed{1+15+24=40.}
\]

The mean channel carries the trivial sector, the centered spread probe carries the 15-sector, and the centered anti-line probe carries the 24-sector.  Thus W(3,3) supplies a finite signal-processing architecture:

\[
\boxed{
\text{line signal}\longrightarrow
\text{mean}+	ext{spread features}+\text{anti-line features}.
}
\]
