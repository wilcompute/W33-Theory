# Part DCLXXVI — Holonomy Scattering Boundary Bridge

## Why this part exists

`Part DCLXXV` collapsed the non-stationary holonomy future to one exact quadratic transfer function.

The next deeper question is whether this already fixes the all-frequency boundary signature of any host realization.

This part proves the stronger statement:

> the holonomy generator has an exact Cayley scattering law whose stationary mode is transmitted unchanged and whose two dynamical sectors are pure phase channels.

## Exact boundary law

Let `G` be the self-adjoint generator from `Part DCLXXII`.

Define the imaginary-frequency boundary response by the Cayley transform

$$
S(i\omega) = (i\omega I - G)(i\omega I + G)^{-1}.
$$

The verifier proves that this is exactly

$$
S(i\omega)
=
P_0
+ \frac{i\omega-\log(4)}{i\omega+\log(4)} P_+
+ \frac{i\omega-\log(5/2)}{i\omega+\log(5/2)} P_-.
$$

So the boundary response is completely fixed by the same two rates that already controlled the recurrence, semigroup, and transfer function pictures.

## Unitary phase split

For every real frequency `\omega > 0`, both dynamical factors have unit modulus:

$$
\left|\frac{i\omega-\log(4)}{i\omega+\log(4)}\right|=1,
\qquad
\left|\frac{i\omega-\log(5/2)}{i\omega+\log(5/2)}\right|=1.
$$

So the rank-`24` and rank-`15` sectors do not dissipate at the boundary. They only acquire frequency-dependent phase shifts.

The stationary mode is transmitted exactly:

$$
S(i\omega) P_0 = P_0.
$$

## Low- and high-frequency limits

The verifier checks the exact limits

$$
\lim_{\omega\to 0^+} S(i\omega) = P_0 - P_+ - P_- = \frac{J}{20} - I,
$$

and

$$
\lim_{\omega\to \infty} S(i\omega) = I.
$$

So low frequency sees the full dynamic complement as a sign-flipped reflection, while high frequency becomes transparent.

## Why this is a breakthrough

This is the first layer in the chain that directly looks like a host boundary signature.

- `DCLXXV` gave the exact transfer function.
- `DCLXXVI` converts it into the exact scattering law.

So the finite holonomy object no longer only determines time evolution.

It also determines the exact all-frequency boundary response that any mixed-plane host realization would have to match.

## Executable artifact

Verifier:

```text
verify_dclxxvi_holonomy_scattering_boundary_bridge.py
```

Tests:

```text
tests/test_dclxxvi_holonomy_scattering_boundary_bridge.py
```

Generated summary:

```text
data/dclxxvi_holonomy_scattering_boundary_bridge.json
```

---
*W33-Theory | Part DCLXXVI | the holonomy generator has one exact two-phase Cayley boundary law, fixing the all-frequency scattering signature of the finite witness object.*
