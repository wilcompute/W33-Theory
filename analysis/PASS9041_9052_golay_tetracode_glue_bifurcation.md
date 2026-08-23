# Passes 9041–9052 — Golay/Tetracode Glue Bifurcation

## The exact common substrate

Passes 9029–9040 found that the 72 quotient-zero roots inside the `E6^4` carrier form a
full-rank `A2^12` root subsystem. That makes a comparison possible which is sharper than
comparing the two Niemeier root systems abstractly: both `N(E6^4)` and `N(A2^12)` can be
viewed as index `3^6=729` even unimodular overlattices of the **same root-lattice type**
`A2^12`.

The new verifier reconstructs the corresponding maximal isotropic ternary glue codes in
`(A2^*/A2)^12 ~= F_3^12`.

## The two self-dual [12,6] codes

For the `A2^12` Niemeier lattice the glue is the extended ternary Golay code:

`C_G : [12,6,6]_3`,

with exact weight enumerator

`W_G(y) = 1 + 264 y^6 + 440 y^9 + 24 y^12`.

There are no weight-three words. Since a nonzero `A2^*/A2` class has minimum norm `2/3`,
any nontrivial glue word has norm at least

`6 * (2/3) = 4 > 2`.

Thus Golay glue adds no roots and the root system stays `A2^12`, with 72 roots.

For `N(E6^4)`, relative to the quotient-zero `A2^12` subsystem selected in Passes
9029–9040, the verifier obtains a different self-dual code:

`C_E : [12,6,3]_3`,

with exact weight enumerator

`W_E(y) = 1 + 8 y^3 + 240 y^6 + 464 y^9 + 16 y^12`.

Its eight weight-three words are supported on exactly four disjoint triples:

`{0,1,2}`, `{3,4,5}`, `{6,7,8}`, `{9,10,11}`,

with two nonzero scalar multiples on each support.

## Local E6 extension plus global tetracode

The four projective weight-three directions span a dimension-four subcode `U` of size 81.
Each direction performs the local extension

`A2^3 -> E6`.

After quotienting by those four local extension lines, the remaining code has parameters

`[4,2,3]_3`,

is self-dual, has weight enumerator

`1 + 8 y^3`,

and is exactly the tetracode.

So the full six-dimensional `E6^4` glue decomposes structurally as

`4 local A2^3 -> E6 extension directions + 2 global tetracode directions`.

This is the code-theoretic version of the standard two-stage Niemeier construction: first the
four `E6` root components appear, then the tetracode glues their discriminant groups to make
the full rank-24 lattice unimodular.

## Why the E6 root counts are forced

A weight-three word in the `A2^12` discriminant code has three nonzero coordinates. Each
nonzero `A2` discriminant class has three minimal vectors of norm `2/3`, so each weight-three
glue coset contains

`3^3 = 27`

norm-two vectors.

There are eight such words. Hence

`72 + 8*27 = 72 + 216 = 288`,

which is exactly the `E6^4` root count.

The words occur as four `+/-` pairs. Each pair contributes

`2*27 = 54`

visible roots, exactly the multiplicity found over each of the four collinear W33 points in
Passes 9029–9040. Meanwhile the underlying `A2^3` block contributes 18 roots to the quotient
kernel.

Thus the W33 line shadow is now explained by the glue code itself:

- four disjoint weight-three support triples;
- four W33 line points;
- two signed words per point;
- 27 roots per signed word;
- 54 visible roots per point.

## What is new and what is not

The ternary Golay construction of `N(A2^12)`, the tetracode construction of `N(E6^4)`, and
the standard Niemeier classification are classical. The new repository result is the explicit
**comparison in the quotient-selected `A2^12` coordinates**, together with its identification
with the four-point W33 root shadow of the same order-nine carrier.

This also sharpens the cross-carrier relation from Passes 9029–9040: the third carrier is not
merely numerically reminiscent of the first carrier's kernel. Its root system is the common
rank-24 substrate on which the second and third Niemeier lattices are selected by two different
self-dual ternary codes.

## Evidence boundary

This is a finite lattice/code theorem. No continuum or particle-physics claim is inferred.
The equality `A2^12` refers to root-lattice type; `N(E6^4)` and `N(A2^12)` remain distinct
Niemeier lattices with different glue codes and different root systems.
