# BT695 — Fibonacci Register Correction Theorem

## Purpose

BT686 correctly noticed a powerful local bridge:

\[
K_{3,3}\quad\leadsto\quad [9,4,4]\quad\leadsto\quad SU(2)_3\quad\leadsto\quad \text{Fibonacci anyons}.
\]

BT695 makes the bridge reviewer-safe by separating three different layers:

1. the classical `K33` cycle code,
2. a quantum register interpretation,
3. the Fibonacci anyon fusion representation.

## The exact classical layer

The graph `K33` has

\[
|V|=6,\qquad |E|=9.
\]

Therefore its cycle rank is

\[
\beta_1(K_{3,3})=9-6+1=4.
\]

The smallest nonzero cycle is a rectangle of length 4.  Hence the binary graph-cycle
code is exactly

\[
\boxed{[9,4,4].}
\]

This is the clean code-theoretic object directly supplied by the local chart.

## The quantum-code boundary

The notation

\[
[[9,4,4]]
\]

is not produced by the standard self hypergraph-product of the `K33` incidence
matrix without additional construction.  The direct verified object is

\[
[9,4,4],
\]

not automatically

\[
[[9,4,4]].
\]

So the correct statement is:

\[
\boxed{
K_{3,3}\text{ supplies a four-bit/four-cycle homology register, not by itself a standard }[[9,4,4]]\text{ stabilizer code.}
}
\]

## The Fibonacci layer

The Fibonacci theory is the `SU(2)_3` / Jones level with

\[
k+2=5.
\]

The four-Fibonacci-anyon fusion space with total charge fixed has dimension

\[
\boxed{2.}
\]

Thus it gives one qubit-like topological register, not four independent qubits.

The safe register dictionary is therefore:

\[
\boxed{
\text{one Fibonacci four-anyon register}\quad\leftrightarrow\quad\mathbb C^2.
}
\]

The local `K33` cycle code has

\[
2^4=16
\]

binary code states.  Therefore it can be organized as four qubit-like binary
cycle generators, or equivalently as four independent two-state registers, but a
single four-anyon Fibonacci fusion space accounts for only one two-state factor.

A compatible bookkeeping statement is:

\[
\boxed{
[9,4,4]\text{ cycle code}\cong (\mathbb F_2)^4
\quad\text{can host four two-state labels, while each Fibonacci four-anyon block contributes one }\mathbb C^2.
}
\]

So a full 16-state realization would require four such Fibonacci two-state
blocks, or a different Fibonacci fusion architecture whose total fusion space has
dimension 16.

## Corrected chain

Combining BT690--BT694, the corrected bridge is

\[
\boxed{
W(3,3)
\to
\text{local }K_{3,3}\text{ nonedge chart}
\to
[9,4,4]\text{ classical cycle code}
\to
\text{two-state Fibonacci fusion blocks}.
}
\]

The phrase `K33 is the physical implementation of Fibonacci TQC` is therefore too
strong unless a hardware/stabilizer/fusion encoding map is added.  The theorem we
can safely claim now is:

\[
\boxed{
K_{3,3}\text{ supplies the smallest }q=3\text{ local cycle register whose }4\text{-cycle geometry is compatible with Fibonacci two-state fusion blocks.}
}
\]

## Open connector

The missing functor is an explicit map

\[
\mathcal F:\;H_1(K_{3,3};\mathbb F_2)\longrightarrow
\bigotimes_i V^{\rm Fib}_i
\]

with either

\[
\dim\bigotimes_i V^{\rm Fib}_i=16
\]

for a full cycle-code state realization, or a specified quotient/projection onto
one or two Fibonacci registers.

That connector is the correct next target.
