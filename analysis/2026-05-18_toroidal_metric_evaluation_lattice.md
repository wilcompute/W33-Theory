# Toroidal Metric Evaluation-Lattice Theorem

## Executive result

Let

\[
W(s)=P(s-1)=\sum_m c_ms^m,
\]

where

\[
c_1,c_2,c_3,c_4,c_5,c_6=12,48,0,4,1,3.
\]

Then

\[
W(s)=12s+48s^2+0s^3+4s^4+s^5+3s^6.
\]

Evaluate around the Euler/parity zero:

\[
\boxed{W(-2)=392=7^2\cdot8,}
\]

\[
\boxed{W(-1)=42=7\cdot6,}
\]

\[
\boxed{W(0)=0,}
\]

\[
\boxed{W(1)=68=4\cdot17,}
\]

\[
\boxed{W(2)=504=7\cdot72=7\cdot8\cdot9.}
\]

This is the five-point evaluation lattice of the toroidal metric operator.

## Class parity projectors from \(W(\pm1)\)

The values

\[
W(1)=68,
\]

and

\[
W(-1)=42
\]

recover the even/odd metric-class counts:

\[
\text{even classes}=\frac{W(1)+W(-1)}{2}=55=5\cdot11,
\]

\[
\text{odd classes}=\frac{W(1)-W(-1)}{2}=13=\Phi_3.
\]

So \(W(\pm1)\) are the class-parity projectors.

Their difference is

\[
55-13=42,
\]

one toroidal chart flag count.

## Boolean parity projectors from \(W(\pm2)\)

The values

\[
W(2)=504
\]

and

\[
W(-2)=392
\]

recover the even/odd Boolean lifts:

\[
\text{even Boolean lift}=\frac{W(2)+W(-2)}{2}=448=7\cdot64,
\]

\[
\text{odd Boolean lift}=\frac{W(2)-W(-2)}{2}=56=7\cdot8.
\]

Per realization:

\[
448/7=64,
\]

\[
56/7=8.
\]

Therefore the middle eigenvalue decomposes as

\[
\boxed{72=64+8.}
\]

This is the same middle eigenvalue in the spectrum

\[
648^1,(144+36\sqrt6)^{24},\boxed{72^{30}},(144-36\sqrt6)^{24},40^{81}.
\]

## Why this is useful

The evaluation lattice gives two different parity projectors:

\[
W(\pm1):\quad \text{class parity},
\]

\[
W(\pm2):\quad \text{Boolean-lift parity}.
\]

The first exposes

\[
13=\Phi_3,
\]

and

\[
55=5p_{\mathrm{Ih}}.
\]

The second exposes

\[
8=1+\Phi_6,
\]

and

\[
64=8^2.
\]

So the toroidal metric packet now has a compact projector interpretation:

\[
\boxed{\text{class projector: }13/55,}
\]

\[
\boxed{\text{Boolean projector: }8/64,}
\]

\[
\boxed{\text{spectrum bridge: }8+64=72.}
\]

## The theorem

**Toroidal Metric Evaluation-Lattice Theorem.** In the shifted variable \(s=1+t\), the toroidal metric multiplicity operator

\[
W(s)=\sum c_ms^m
\]

has the five-point lattice

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

The \(\pm1\) pair gives the class parity projectors

\[
55=5\cdot11
\]

and

\[
13=\Phi_3.
\]

The \(\pm2\) pair gives the Boolean parity projectors

\[
448=7\cdot64
\]

and

\[
56=7\cdot8.
\]

Hence

\[
W(2)/7=72
\]

is the middle association-scheme eigenvalue, while

\[
W(-2)=392=7^2\cdot8
\]

is the signed Boolean imbalance.

## Honesty boundary

This is an exact finite evaluation-lattice identity for the toroidal metric edge packet. It does not by itself infer physical dynamics, continuum geometry, or empirical observables.
