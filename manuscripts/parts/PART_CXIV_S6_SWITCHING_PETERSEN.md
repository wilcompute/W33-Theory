# Part CXIV — S6 Switching Automorphism and Outer Petersen Stabilizer

Status: theorem-grade structural extension  
Date: April 28, 2026

Part CXIII identified the odd kernel of the hidden oriented-triple cover as a Petersen Seidel matrix.

This part identifies its symmetry mechanism:

```text
ordinary graph symmetry = S5,
```

but

```text
Seidel switching symmetry = S6.
```

So Petersen is the unsigned shadow of a larger S6-symmetric switching object.

## Signed S6 action

The six-letter group S6 acts on:

```text
20 oriented triples,
10 bisections,
the odd anti-complement quotient.
```

Choosing one oriented triple representative over each bisection requires a sign convention. Therefore the S6 action on the odd quotient is signed.

The resulting signed monomial matrices M satisfy

```text
M^T S M = S.
```

The script verifies exactly

```text
720
```

such signed matrices.

Thus the full switching automorphism group is

```text
S6.
```

## Ordinary Petersen shadow

Forgetting signs, only

```text
120
```

permutations preserve the actual Petersen graph.

This is the ordinary Petersen automorphism group:

```text
Aut(Petersen) ≅ S5.
```

In the canonical orientation used here, this S5 is the stabilizer of one distinguished letter.

Therefore

```text
S6/S5
```

has

```text
6
```

cosets, matching the six possible distinguished letters.

## Six switching patterns

The S6 action produces exactly

```text
6
```

distinct sign-switching patterns.

These are precisely indexed by the six letters.

So changing the distinguished letter changes the Petersen representative inside the same Seidel switching class.

## Meaning

The odd 5+5 sector is not merely Petersen.

It is Petersen plus the missing S6 switching symmetry:

```text
Petersen graph S5 -> Petersen-Seidel switching class S6.
```

## Local rank context

The local split remains

```text
B29 = 1 + 2*9 + 5 + 5.
```

The 5+5 is governed by the Petersen-Seidel odd sector.

## Structural slogan

```text
Petersen is the S5 shadow of an S6 Seidel switching kernel.
```
