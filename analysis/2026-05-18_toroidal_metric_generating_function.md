# Toroidal Metric Generating Function

## Executive result

The toroidal metric edge multiplicities produced the binomial moment sequence

\[
B_0,B_1,B_2,B_3,B_4,B_5,B_6
=
68,147,127,86,54,19,3.
\]

Package this into the generating function

\[
P(t)=\sum_{k=0}^6B_kt^k.
\]

So

\[
P(t)=68+147t+127t^2+86t^3+54t^4+19t^5+3t^6.
\]

The exact factorization is

\[
\boxed{P(t)=(1+t)Q(t)}
\]

where

\[
\boxed{Q(t)=68+79t+48t^2+38t^3+16t^4+3t^5.}
\]

This is extremely useful because the quotient polynomial contains the phase-kernel value directly:

\[
\boxed{[t]Q(t)=79.}
\]

## Evaluations

The parity cancellation is exact:

\[
P(-1)=0.
\]

The quotient at \(-1\) is the genus numerator:

\[
\boxed{Q(-1)=12.}
\]

The Boolean lift is

\[
P(1)=504=7\cdot72=21\cdot24.
\]

Thus

\[
\boxed{P(1)/7=72,}
\]

which is the middle eigenvalue of the minimal-logical X-association spectrum:

\[
648^1,(144+36\sqrt6)^{24},\boxed{72^{30}},(144-36\sqrt6)^{24},40^{81}.
\]

The quotient value at \(+1\) is

\[
Q(1)=252=21\cdot12.
\]

So the quotient sees the toroidal edge count \(21\) and the genus numerator \(12\) simultaneously.

## Cyclotomic residues

Modulo \(\Phi_3(t)=t^2+t+1\), the polynomial reduces to

\[
P(t)\equiv 11+55t=11(1+5t).
\]

The Eisenstein norm is

\[
N_{\mathbb Z[\omega]}(11+55\omega)
=11^2\cdot21.
\]

So the \(\Phi_3\) evaluation sees two crucial constants together:

\[
\boxed{11=p_{\mathrm{Ih}}}
\]

and

\[
\boxed{21=\text{toroidal edge count}.}
\]

Modulo \(\Phi_4(t)=t^2+1\),

\[
P(t)\equiv -8+80t=8(-1+10t).
\]

Modulo \(\Phi_6(t)=t^2-t+1\),

\[
P(t)\equiv -123+201t=3(-41+67t).
\]

These are less immediately clean than the \(\Phi_3\) residue, but they preserve the expected \(q=3\) and \(\Phi_4=10\) traces.

## Interpretation

The generating function compresses the previous edge-moment identities:

\[
B_0=68=\text{metric edge classes},
\]

\[
B_1=147=\text{actual edge instances},
\]

\[
B_1-B_0=79=\text{phase-frame kernel},
\]

\[
B_2=127=2^7-1=\text{nonempty heptad subsets},
\]

\[
P(1)/7=72=\text{middle association-scheme eigenvalue}.
\]

The new information is the factorization:

\[
P(t)=(1+t)Q(t).
\]

The \((1+t)\) factor is the parity-null / Euler-cancellation layer.  The quotient \(Q\) carries the kernel \(79\), and its \(-1\) evaluation recovers the genus numerator \(12\).

## The theorem

**Toroidal Metric Generating Function Theorem.** The binomial moment sequence of the seven-realization metric edge spectrum defines

\[
P(t)=68+147t+127t^2+86t^3+54t^4+19t^5+3t^6.
\]

This polynomial has the exact factorization

\[
P(t)=(1+t)(68+79t+48t^2+38t^3+16t^4+3t^5).
\]

The factor \((1+t)\) is the parity-null/Euler cancellation.  The quotient contains the phase-kernel coefficient \(79\) and evaluates to the genus numerator \(12\) at \(t=-1\).  Its Boolean value gives

\[
P(1)=504=7\cdot72,
\]

so the middle eigenvalue \(72\) is the per-realization Boolean lift.  Modulo \(\Phi_3\), \(P\) reduces to

\[
11(1+5t),
\]

whose Eisenstein norm is

\[
11^2\cdot21,
\]

exposing the Ihara prime and toroidal edge count together.

## Why this matters

The metric edge data now has four equivalent forms:

1. histogram:

\[
1^{12},2^{48},4^4,5^1,6^3;
\]

2. binomial moments:

\[
68,147,127,86,54,19,3;
\]

3. generating function:

\[
P(t)=(1+t)Q(t);
\]

4. spectral bridge:

\[
P(1)/7=72,\quad Q(-1)=12,\quad [t]Q=79.
\]

So the toroidal metric packet simultaneously encodes:

\[
\boxed{79\text{ phase kernel},\quad 12\text{ genus numerator},\quad 72\text{ middle eigenvalue},\quad 11^2\cdot21\text{ cyclotomic norm}.}
\]

## Honesty boundary

This is an exact finite generating-function identity for the toroidal metric edge spectrum. It does not by itself prove physical dynamics, continuum geometry, or empirical observables.
