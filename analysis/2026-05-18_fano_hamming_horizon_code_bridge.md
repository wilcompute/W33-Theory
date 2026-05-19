# Fano-Hamming Horizon Code Bridge

## Parallel hint used

The newest Fano-Hamming commit identifies the binary shadow:

\[
[7,4,3]_2=[\Phi_6,d_Z,d_X]_2.
\]

So the Hamming code parameters are exactly W33 substrate primitives:

\[
n=7=\Phi_6,
\]

\[
k=4=d_Z,
\]

\[
d=3=d_X=q.
\]

The Hamming parity rank is

\[
7-4=3=q.
\]

The dual simplex code has dimension 3, hence

\[
2^3=8
\]

syndrome/coset states.

## Bridge to the horizon code

Our explicit horizon code has parameters

\[
[72,66]_3
\]

with parity rank

\[
72-66=6.
\]

Now:

\[
72=q^2\cdot8=9\cdot8.
\]

Since the binary Hamming dual has 8 codewords/cosets,

\[
\boxed{72=q^2\cdot |[7,3,4]_2|.}
\]

The parity rank is

\[
6=2\cdot3=2q.
\]

So

\[
\boxed{\text{horizon parity rank}=2\times\text{Hamming parity rank}.}
\]

The dimension is

\[
66=72-6.
\]

But also

\[
66=q^2\Phi_6+q=9\cdot7+3=63+3.
\]

So the horizon payload is nine Fano sheets plus one qutrit line.

## Binary heptad closure

The metric moment bridge gave

\[
B_2=127=2^7-1.
\]

So

\[
B_2+1=128=2^7.
\]

This is the full Boolean closure of the Fano/heptad shell.

The Hamming bridge says this is not accidental: the seven toroidal/Fano points carry the classical binary Hamming shadow.

## Factorial check

The Fano automorphism group order is

\[
|\operatorname{Aut}(\text{Fano})|=168=f\Phi_6=24\cdot7.
\]

The E8 root carrier has

\[
|E|=240.
\]

Then

\[
168\cdot240=40320=8!.
\]

So:

\[
\boxed{|\operatorname{Aut}(\text{Fano})|\cdot|E_8\text{ roots}|=8!.}
\]

That binds Fano/Hamming, the W33 edge carrier, and tomotope/E8 rank 8.

## The theorem

**Fano-Hamming Horizon Code Bridge.** The \([72,66]_3\) horizon parity code is a qutrit lift of the binary Hamming \([7,4,3]_2\) syndrome quotient:

\[
[7,4,3]_2=[\Phi_6,d_Z,d_X]_2,
\]

\[
72=q^2\cdot2^q,
\]

\[
6=2q,
\]

\[
66=q^2\Phi_6+q.
\]

Thus the ternary horizon code is nine qutrit sheets over the 8-element binary Hamming syndrome/coset space, with doubled Hamming parity rank.

## Why this matters

This directly connects the binary-shadow code to the ternary horizon code:

\[
\boxed{[7,4,3]_2\longrightarrow[72,66]_3.}
\]

The length lift is

\[
7\mapsto 72=q^2(1+7),
\]

and the parity-rank lift is

\[
3\mapsto6=2\cdot3.
\]

So the horizon code is not floating.  It is the qutrit expansion of the Fano/Hamming heptad.

## Honesty boundary

This is an exact parameter bridge. A literal functor from the binary Hamming code to the ternary horizon code still requires an explicit map of check matrices and syndromes.
