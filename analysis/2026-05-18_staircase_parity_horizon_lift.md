# Staircase Parity-Horizon Lift

## Executive result

The parallel staircase commit shows that the integer-genus steps of

\[
g(K_n)=\frac{(n-3)(n-4)}{12}
\]

land on W(3,3) invariants.  The corrected numerator is

\[
T(n)=g(K_n)\cdot k=(n-3)(n-4).
\]

At the main staircase steps:

| \(n\) | \(g(K_n)\) | \(T(n)=gk\) | Reading |
|---:|---:|---:|---|
| 7 | 1 | 12 | valency / Császár torus |
| 12 | 6 | 72 | correction horizon / middle eigenvalue |
| 19 | 21 | 252 | \(Q(1)\), metric polynomial quotient |
| 28 | 55 | 660 | \(c_{even}k=55\cdot12\) |
| 36 | 88 | 1056 | motive/conductor level |

The local parity-code block is the \(n=12\) row:

\[
T(12)=72.
\]

But

\[
\binom{12}{2}=66,
\]

so

\[
\boxed{T(12)=72=66+6.}
\]

Thus the \([72,66]+6\) horizon code is the local parity block inside the global genus staircase.

## Why this is sharper than the isolated 66 identity

The isolated identity was:

\[
72=66+q!.
\]

The staircase lift says this is one point in a tower:

\[
12,72,252,660,1056,\ldots
\]

The first differences are

\[
60,180,408,396,\ldots
\]

and the first ratio is

\[
180=3\cdot60=q\cdot60.
\]

So the \(n=12\) block is not a loose coincidence.  It is the first nontrivial correction horizon after the Császár torus step \(n=7\).

## Horizon row

At \(n=12\):

\[
T(12)=(12-3)(12-4)=72.
\]

Payload:

\[
\binom{12}{2}=66.
\]

Parity/check budget:

\[
72-66=6=q!.
\]

Rate:

\[
\frac{66}{72}=\frac{11}{12}.
\]

Redundancy:

\[
\frac{6}{72}=\frac{1}{12}.
\]

Genus:

\[
g(K_{12})=6=q!.
\]

So all four readings agree:

\[
\boxed{\text{payload}=66,\quad \text{parity}=6,\quad \text{total}=72,\quad \text{genus}=6.}
\]

## Relation to the next steps

At \(n=19\):

\[
g(K_{19})=21=\binom{7}{2}.
\]

So the next major integer-genus step has genus equal to the Császár complete-edge count.

Then

\[
T(19)=21\cdot12=252=Q(1).
\]

At \(n=28\):

\[
g(K_{28})=55=c_{even}.
\]

Then

\[
T(28)=55\cdot12=660.
\]

So the tower passes through:

\[
\boxed{k\rightarrow72\rightarrow Q(1)\rightarrow c_{even}k.}
\]

## The theorem

**Staircase Parity-Horizon Lift Theorem.** The local \([72,66]+6\) horizon at \(n=12\) is the second nonzero corrected numerator in the integer-genus staircase

\[
T(n)=g(K_n)k=(n-3)(n-4).
\]

It is preceded by

\[
T(7)=12=k,
\]

and followed by

\[
T(19)=252=Q(1),
\]

and

\[
T(28)=660=c_{even}k.
\]

Thus the 66/72 parity-code block is not isolated; it is the correction-horizon node of the global qutrit genus tower.

## Honesty boundary

These are exact finite arithmetic/topological identities.  The code interpretation remains a structural model until explicit parity-check and generator matrices are constructed.
