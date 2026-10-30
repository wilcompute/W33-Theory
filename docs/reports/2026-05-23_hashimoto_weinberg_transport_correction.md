# 2026-05-23 - Hashimoto Transport Derivation of the Weinberg alpha-over-11 Correction

## Purpose

The previous Eq. 52 rewrite separated the weak-mixing story into:

```text
GUT normalization:          sin^2(theta_W) = 3/8
finite-geometric generator: x0 = 3/13
leading Z-pole correction:  alpha_hat(MZ)/(k-1)
```

The remaining question was why the denominator of the leading correction should be `k-1 = 11`.

## Hashimoto carrier

The new verifier reconstructs W33 from the symplectic form on PG(3,F3), then builds the Hashimoto non-backtracking operator on directed edges.

Verified facts:

```text
W33 vertices:          40
undirected edges:      240
directed edges:        480
regular degree k:      12
nonbacktracking degree: k-1 = 11
```

The 480 x 480 Hashimoto matrix B has:

```text
row sum = 11 for every directed edge
column sum = 11 for every directed edge
```

Therefore

```text
P = B/11
```

is a row-stochastic normalized transport operator.

## Ihara meaning

The same 11 is not merely a branching count.  It is also the quadratic coefficient in the Ihara-Bass vertex determinant:

```text
det(I - uB) = (1-u^2)^(E-V) det(I - uA + 11 u^2 I).
```

So 11 is the canonical W33 transport denominator.

## First-order correction rule

An isotropic first-order radiative insertion of strength alpha_hat on the directed-edge carrier is branch-averaged over the 11 legal non-backtracking continuations.

Thus the scalar first-order contribution is

```text
alpha_hat / 11.
```

The refined weak-mixing expression is therefore

```text
sin^2(theta_eff)(MZ)
  = 3/13 + alpha_hat(MZ)/11 + higher W33 transport terms.
```

Using alpha_hat(MZ)^(-1)=127.930 gives

```text
3/13 + 1/(11*127.930) = 0.23147985...
```

## Meaning

The denominator 11 is not tuned from the observed weak mixing angle.  It is the exact Hashimoto/Ihara non-backtracking branching number of W33.

This makes the Eq. 52 defense stronger:

```text
3/13 is the finite-geometric tree generator;
alpha_hat/11 is the leading transport correction;
11 is forced by the W33 Hashimoto carrier.
```

## Boundary

This proves the transport denominator and the natural first-order branch-averaging rule.  A full field-theoretic derivation still needs to derive alpha_hat and the higher-order terms from the W33 Ihara effective action.

## New code

- `analysis/w33_hashimoto_weinberg_transport_correction.py`

When run, it writes:

- `data/w33_hashimoto_weinberg_transport_correction.json`
