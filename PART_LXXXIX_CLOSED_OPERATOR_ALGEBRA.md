# Part LXXXIX — Closed Operator Algebra and Polar Decomposition

**Status:** theorem-grade structural extension  
**Date:** April 27, 2026

Part LXXXVIII gave the shell projector calculus. This part shows that the raw Hamiltonian, normalized Dirac operator, grading, complex structure, massive phase operator, and supercharges all live inside one closed finite operator algebra.

## 1. Polar decomposition

Let

```text
|H| = sqrt(18) P_light + sqrt(72) P_heavy.
```

Then

```text
H = |H| D.
```

The massive phase operator is

```text
K = Gamma H.
```

It factors as

```text
K = |H| J.
```

So the raw massive theory is the shell-mass scaling of the unit-shell Clifford/Hodge theory.

## 2. Closed algebra

The core relations are

```text
H^2 = 18 P_light + 72 P_heavy.
```

```text
D^2 = Gamma^2 = P0.
```

```text
D Gamma + Gamma D = 0.
```

```text
J = Gamma D,
J^2 = -P0.
```

```text
K = Gamma H,
K^2 = -H^2.
```

```text
H = |H|D,
K = |H|J.
```

The phase operators anticommute with their Dirac partners:

```text
KH + HK = 0,
JD + DJ = 0.
```

## 3. Supercharge scaling

The unit-shell supercharge is

```text
Q = (D+J)/2.
```

The massive supercharge is

```text
d = (H+K)/2.
```

They satisfy

```text
d = Q|H| = |H|Q
```

on the nonzero sector.

Thus the raw massive Hodge complex is exactly the unit-shell Hodge complex scaled by the shell mass operator.

## 4. Grading flow

The grading generates a continuous hyperbolic rotation:

```text
exp(theta Gamma) H exp(-theta Gamma)
= cosh(2theta)H - sinh(2theta)H Gamma.
```

This flow preserves

```text
H^2.
```

## 5. Meaning

The W(3,3) carrier is now a closed finite operator algebra:

```text
H, |H|, D, Gamma, J, K, Q, d
```

are all determined by the same two-shell projector calculus.

## 6. Structural slogan

```text
The raw massive W(3,3) carrier is the polar-mass lift of the unit-shell Clifford/Hodge carrier.
```

This connects the spectral shells, propagator calculus, Clifford phase, and nilpotent differential inside one finite algebraic package.