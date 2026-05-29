# Index-Guided Dirac / Local-Shell Bridge

Date: 2026-05-29

This note records the finite-count bridge extracted from the live GitHub Pages index surface.

The live page states that the exact theorem spine begins with

```text
W(3,3) = SRG(40,12,2,4)
```

as the projective commutation geometry of the 40 non-identity two-qutrit Pauli observables. Around each vertex, the 12 neighbours split into four qutrit MUB triangles, while the 27 non-neighbours form an F3^3 Heisenberg shell whose derived graph is the Schlaefli graph.

It also points to the exact projective-affine shell audit:

```text
PG(2,3) + AG(3,3)
```

as the tangent-hyperplane / affine-complement split behind the local

```text
13 + 27
```

qutrit shell, and to the symplectic spread frame audit for the exact

```text
36 = 4 * 9
```

spread/MUB layer.

## Local shell

The local anchor shell is

```text
40 = 13 + 27.
```

The refined split is

```text
13 = 1 + 4*3
27 = 9*3
```

so

```text
40 = (1 + 4*3) + 9*3.
```

Interpretation:

```text
1 = anchor
4*3 = four qutrit memory/MUB triangles in the tangent hyperplane
9*3 = nine qutrit affine fibers in the AG(3,3) complement
```

## Spread square

The spread audit gives

```text
36 = 4 * 9.
```

The previous router/phase factorization gave

```text
16 * 81.
```

But

```text
16 * 81 = 4^2 * 9^2 = (4*9)^2 = 36^2.
```

Also

```text
36^2 = 48 * 27.
```

because

```text
48 = 16 * 3.
```

So the same transport packet can be read as either

```text
Q4 router states * F3^4 phase states
```

or

```text
ternary Q4 clock * local H27 affine shell
```

or

```text
ordered spread-frame source/target pair.
```

## Chain shell

The finite chain dimensions are

```text
(C0,C1,C2,C3) = (40,240,160,40).
```

Their total is

```text
480 = 40 * 12.
```

Normalizing per anchor gives

```text
(1,6,4,1),
```

whose sum is

```text
1 + 6 + 4 + 1 = 12.
```

This is the local 12-flag codec denominator appearing in the genus and flag-codec stack.

## Finite D^2 shell

The finite Dirac-square multiplicities split as

```text
82 + 320 + 48 + 30 = 480.
```

The index-guided decomposition is

```text
82  = 1 + 81
320 = 40 * 8
48  = 16 * 3
30  = 10 * 3
```

So the 480-dimensional shell decomposes as:

```text
zero/phase sector:      1 + 81
Cartan-anchor sector:   40 * 8
ternary Q4 clock:       16 * 3
spread-direction shell: 10 * 3
```

This gives an exact count-level dictionary between the local qutrit shell, Q4 router clock, symplectic spread layer, and finite internal Dirac shell.

## Global factorization

The prior factorization

```text
51840 = 40 * 16 * 81
```

becomes

```text
51840 = 40 * 36^2.
```

Thus:

```text
anchor * router * phase = anchor * ordered spread-frame pair.
```

## Compressed theorem

```text
The live index surface suggests that the 13+27 local shell, 36 spread/MUB frames, Q4 router, H27 affine shell, and finite Dirac multiplicities are one dictionary. The exact bridge is:

40 = (1+4*3)+9*3,
36 = 4*9,
16*81 = 36^2 = 48*27,
40+240+160+40 = 480 = 40*12,
82+320+48+30 = 480,
51840 = 40*36^2 = 40*16*81.
```

## Honest boundary

This is an exact finite-count bridge, not a new continuum derivation. The next hard test is to import the actual finite Dirac operator used in the current theorem stack and verify that its eigenspaces decompose canonically into the four subpackets listed here rather than only matching the multiplicities.
