# Part LXXXVIII — Projector Calculus and Finite Propagator

**Status:** theorem-grade structural extension  
**Date:** April 27, 2026

Part LXXXVII collapsed the spectral action to two atoms. This part upgrades that collapse into a complete operator calculus.

Let

```text
X = H^2.
```

Then the three shell projectors are polynomials in X:

```text
P0 = (X - 18I)(X - 72I)/1296
```

```text
P_light = X(72I - X)/972
```

```text
P_heavy = X(X - 18I)/3888
```

Thus H alone determines the zero, light, and heavy shell projectors.

## 1. Functional calculus

For any polynomial or analytic function f,

```text
f(H^2) = f(0)P0 + f(18)P_light + f(72)P_heavy.
```

The normalized Dirac involution is the spectral sign of H:

```text
D = sign(H) = H(P_light/sqrt(18) + P_heavy/sqrt(72)).
```

So the unit-shell Dirac/Hodge complex is the polar/sign normalization of the raw two-shell Hamiltonian.

## 2. Finite propagators

The massive Green kernel is

```text
(H^2 + mu^2 I)^(-1)
= P0/mu^2 + P_light/(18+mu^2) + P_heavy/(72+mu^2).
```

The Dirac resolvent is

```text
(H - zI)^(-1)
= -P0/z + (H+zI)P_light/(18-z^2) + (H+zI)P_heavy/(72-z^2).
```

The heat kernel is

```text
exp(-tH^2)=P0 + exp(-18t)P_light + exp(-72t)P_heavy.
```

The unitary evolution is

```text
exp(itH)
= P0
+ cos(t sqrt(18))P_light
+ i sin(t sqrt(18)) H P_light / sqrt(18)
+ cos(t sqrt(72))P_heavy
+ i sin(t sqrt(72)) H P_heavy / sqrt(72).
```

## 3. Meaning

The completed W(3,3) triangle is now a symbolic finite propagator system. There is no hidden spectral computation left:

```text
H -> P0, P_light, P_heavy -> D, G, R, exp(-tH^2), exp(itH).
```

This turns the two-shell spectral action into an explicit finite Green/resolvent/evolution calculus.