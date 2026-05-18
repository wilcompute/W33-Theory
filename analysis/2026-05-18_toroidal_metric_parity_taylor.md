# Toroidal Metric Parity-Taylor Theorem

## Executive result

The toroidal metric generating function is

\[
P(t)=68+147t+127t^2+86t^3+54t^4+19t^5+3t^6.
\]

It factors as

\[
P(t)=(1+t)Q(t),
\]

so

\[
P(-1)=0.
\]

Now expand at the parity/Euler-cancellation point

\[
t=-1.
\]

Let

\[
u=1+t.
\]

Then the exact Taylor expansion is

\[
\boxed{P(t)=12u+48u^2+0u^3+4u^4+u^5+3u^6.}
\]

Equivalently,

\[
\boxed{\frac{P^{(m)}(-1)}{m!}=c_m,}
\]

where \(c_m\) is the number of metric edge classes of multiplicity \(m\).

So the metric edge-class histogram

\[
1^{12},2^{48},3^0,4^4,5^1,6^3
\]

is exactly the normalized derivative ladder of \(P\) at \(t=-1\).

## The ladder

The normalized derivative ladder is:

| Multiplicity / derivative order | Value | Reading |
|---:|---:|---|
| 1 | 12 | genus numerator / oriented double centered shell |
| 2 | 48 | two copies of the 24-sector |
| 3 | 0 | missing cubic/q slot |
| 4 | 4 | \(\mu=d_Z=q+1\) |
| 5 | 1 | center/mean line |
| 6 | 3 | \(q\) at the sextic cap |

So

\[
\boxed{12,48,0,4,1,3}
\]

is not just a histogram. It is the Taylor data of the metric operator at the parity point.

## Why the missing cubic slot matters

The missing term is

\[
0u^3.
\]

That says there are no metric edge classes of multiplicity \(3\\), even though \(q=3\) is the field size controlling the W33 substrate.

So the metric packet does not put \(q=3\) at degree 3. Instead it pushes the field-size value to the sextic cap:

\[
3u^6.
\]

This is an interesting displacement:

\[
\boxed{q\text{ is absent at cubic order and reappears at sextic order}.}
\]

A natural interpretation is that the toroidal metric realization avoids a direct cubic degeneracy, then recovers \(q\) only after the oriented double-cover / centered-shell structure has been completed.

## Reconstructing the earlier invariants

From the Taylor/histogram coefficients \(c_m\), we recover:

Metric edge classes:

\[
\sum_m c_m=68.
\]

Actual edge instances:

\[
\sum_m mc_m=147.
\]

Phase kernel:

\[
\sum_m(m-1)c_m=147-68=79.
\]

Boolean lift:

\[
\sum_m2^mc_m=504=7\cdot72.
\]

Raw second moment:

\[
\sum_mm^2c_m=401=320+81.
\]

So the Taylor coefficients fully reconstruct the metric moment operator:

\[
\boxed{68,147,79,504,401}
\]

from the parity expansion alone.

## Relation to the spectrum

The target spectrum remains

\[
648^1,(144+36\sqrt6)^{24},72^{30},(144-36\sqrt6)^{24},40^{81}.
\]

The parity-Taylor layer links to it as follows:

\[
48=2\cdot24
\]

matches the two conjugate \(24\)-dimensional sectors.

\[
504/7=72
\]

matches the middle eigenvalue.

\[
401=320+81
\]

matches the minimal X-vector count plus protected homology.

\[
79=160-81
\]

matches the signed phase-frame kernel.

## The theorem

**Toroidal Metric Parity-Taylor Theorem.** The toroidal metric moment generating function has Taylor expansion at the parity/Euler point \(t=-1\):

\[
P(t)=12u+48u^2+0u^3+4u^4+u^5+3u^6,
\qquad u=1+t.
\]

Therefore the metric edge-class multiplicity histogram is exactly the normalized derivative ladder

\[
\frac{P^{(m)}(-1)}{m!}.
\]

The ladder reads

\[
12,48,0,4,1,3:
\]

genus numerator, two 24-sectors, missing cubic q-slot, quartic \(\mu\)/root-4 slot, center, and \(q\) at the sextic cap.

## Why this is useful

The edge-metric packet now has three increasingly algebraic forms:

1. histogram:

\[
1^{12},2^{48},3^0,4^4,5^1,6^3;
\]

2. generating function:

\[
P(t)=(1+t)Q(t);
\]

3. parity Taylor ladder:

\[
P(t)=12u+48u^2+0u^3+4u^4+u^5+3u^6.
\]

The third form is the sharpest: it turns the metric edge spectrum into a derivative object centered at the Euler-cancellation point.

## Honesty boundary

This is an exact finite Taylor/generating-function identity. It interprets the metric edge histogram as derivatives at the parity point; it does not prove physical dynamics, continuum geometry, or empirical observables by itself.
