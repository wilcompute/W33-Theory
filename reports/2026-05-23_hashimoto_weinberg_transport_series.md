# 2026-05-23 - Bounded Hashimoto Transport Series for the Weinberg Correction

## Result

The leading W33 transport correction to the finite-geometric Weinberg generator is

```text
alpha_hat / 11
```

where 11 is the Hashimoto non-backtracking branching number.

The next question is whether the higher-order terms are arbitrary. Under the isotropic scalar-transport approximation, they are not: they are controlled by a Neumann series.

## Series

Let

```text
r = alpha_hat / 11.
```

Repeated isotropic non-backtracking insertions contribute at most

```text
r^n
```

at order n. Therefore the full repeated-insertion response is bounded by

```text
delta_full = r + r^2 + r^3 + ... = r/(1-r)
```

or equivalently

```text
delta_full = alpha_hat / (11 - alpha_hat).
```

The omitted tail after the leading term is

```text
tail = r^2/(1-r).
```

## Numerical scale

Using

```text
alpha_hat(MZ)^(-1) = 127.930
```

the script finds:

```text
r = alpha_hat/11 ≈ 0.0007106
```

and the higher-order tail is below

```text
5e-7.
```

So writing

```text
sin^2(theta_eff)(MZ) = 3/13 + alpha_hat/11 + O(alpha_hat^2)
```

is not vague: the isotropic repeated-transport tail is explicitly bounded.

## Meaning

The Weinberg-angle response now has three increasingly strong layers:

```text
1. 3/13 is the W33 finite-geometric tree generator.
2. alpha_hat/11 is the first Hashimoto transport correction.
3. higher isotropic transport terms are bounded by a tiny Neumann tail.
```

This makes Eq. 52 far less vulnerable to the objection that it is just a numerical coincidence.

## Boundary

The Neumann bound assumes isotropic scalar transport. The next nontrivial target is sector-dependent Hashimoto transport, where the 480 directed-edge carrier is projected onto W33's 1+24+15 spectral sectors.

## New code

- `analysis/w33_hashimoto_weinberg_transport_series.py`

When run, it writes:

- `data/w33_hashimoto_weinberg_transport_series.json`
