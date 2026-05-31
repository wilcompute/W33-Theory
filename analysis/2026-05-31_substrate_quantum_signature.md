# W(3,3) Substrate Quantum Signature

Date: 2026-05-31

This is a NEW result, derived by explicit simulation rather than
identity-matching.

## Setup

Build W(3,3) directly from the symplectic polar space PG(3, F_3):

```text
vertices = 40 projective points of PG(3, F_3)
edges    = pairs [u], [v] with omega(u, v) = 0 (mod 3) and [u] != [v]
omega(u, v) = u_0 v_2 - u_2 v_0 + u_1 v_3 - u_3 v_1
```

The construction reproduces SRG(40, 12, 2, 4) with adjacency spectrum
{12 (mult 1), 2 (mult 24), -4 (mult 15)} exactly.

## Run quantum walk

Define the substrate Hamiltonian H = A (the adjacency operator).
Evolve a state localized at vertex i:

```text
|psi(t)> = exp(-i A t) |e_i>
```

Compute the return probability

```text
P_return(t) = |<e_i | psi(t)>|^2
```

## Result 1: Universal period pi

The W(3,3) quantum walk is PERFECTLY PERIODIC with period pi:

```text
P_return(pi) = 1
P_return(k * pi) = 1 for all integer k.
```

This is because the adjacency eigenvalues {12, 2, -4} are all even, so
the GCD of the eigenvalue DIFFERENCES is exactly 2 = lambda, giving

```text
revival period = 2*pi / GCD = 2*pi / 2 = pi.
```

The substrate has a UNIVERSAL CLOCK with period pi.

## Result 2: Substrate-clean fractional revivals

At fractional times t = pi * p / q for small p / q, the return
probability takes CLOSED-FORM substrate-arithmetic values:

```text
P_return(0)       = 1
P_return(pi/6)    = Phi_6 * Phi_3 / v^2    = 91 / 1600    (0.0569)
P_return(pi/4)    = Phi_3 / F_5^2          = 13 / 25      (0.5200)
P_return(pi/3)    = (v^2 - q^2 * Phi_3) / v^2  = 1483 / 1600  (0.9269)
P_return(pi/2)    = 1 / F_5^2              = 1 / 25       (0.0400)
P_return(2*pi/3)  = (v^2 - q^2 * Phi_3) / v^2  = 1483 / 1600
P_return(3*pi/4)  = Phi_3 / F_5^2          = 13 / 25
P_return(5*pi/6)  = Phi_6 * Phi_3 / v^2    = 91 / 1600
P_return(pi)      = 1
```

These are NEW substrate identities, not previously catalogued.

## Why this is the substrate quantum SIGNATURE

The autocorrelation function at any vertex is:

```text
C(t) = (1/v)[exp(-i k t) + f * exp(-i r t) + g * exp(-i s t)]
     = (1/40)[exp(-12it) + 24 * exp(-2it) + 15 * exp(4it)]
```

Because W(3,3) is vertex-transitive under Sp(4, F_3), C(t) is INDEPENDENT
of which vertex i we start at.

So P_return(t) = |C(t)|^2 is a SUBSTRATE-INTRINSIC FUNCTION -- it
characterizes the W(3,3) substrate purely by its (v, k, lambda, mu)
parameters.

The function

```text
F: Q -> [0, 1],  F(p/q) := P_return(pi * p/q)
```

is the substrate's QUANTUM FINGERPRINT.  Its values at small rationals
are themselves rationals factoring through (v, f, g, k) = (40, 24, 15, 12).

## Substrate-clean denominators come in two families

At the t/pi values examined, two denominator families appear:

```text
FAMILY A: F_5^2 = (mu + 1)^2 = 25 denominator
  -- appears at t/pi = 1/2 and 1/4
  -- numerators: 1 and Phi_3 = 13
  -- meaning: BINARY revivals (involving 2nd and 4th roots of unity)

FAMILY B: v^2 = 1600 denominator
  -- appears at t/pi = 1/6, 1/3
  -- numerators: Phi_6*Phi_3 = 91 and v^2 - q^2*Phi_3 = 1483
  -- meaning: TERNARY revivals (involving 3rd and 6th roots of unity)
```

This is sharper than just "substrate-clean": there is a structural
DICHOTOMY between binary (Z_2-graded) and ternary (Z_3-graded)
fractional revivals.

## Why this matters

This is the first time the W(3,3) substrate has been studied as a
DYNAMICAL system rather than as a static counting object.

The fractional revival values F(1/2), F(1/4), F(1/3), F(1/6) are
EMPIRICAL substrate observables.  Any physical realization of the
substrate -- be it a photonic time-bin interferometer, a qutrit Pauli
phase space, or a hypothetical "substrate field theory" -- MUST produce
these revival amplitudes at the corresponding fractional times.

This gives a PROTOCOL for experimentally distinguishing W(3,3)
substrate models from alternatives.

## Compressed theorem

```text
The W(3,3) substrate has a universal quantum walk period pi (in adjacency
time units), set by the GCD = lambda = 2 of its spectral differences.
Fractional revivals at t = pi*p/q give substrate-clean rational return
probabilities, with denominators splitting into a BINARY family F_5^2 = 25
(quartic, half) and a TERNARY family v^2 = 1600 (sixth, third).  These
constitute the W(3,3) QUANTUM SIGNATURE -- a new dynamical fingerprint of
the substrate, derivable from (v, k, lambda, mu, r, s, f, g) alone.
```

## Honest boundary

The substrate quantum signature is derived from the bare adjacency
operator A; whether higher-derivative observables (e.g., commutator
spreading, OTOC, entanglement growth) give similarly clean values is
the next computational frontier.
