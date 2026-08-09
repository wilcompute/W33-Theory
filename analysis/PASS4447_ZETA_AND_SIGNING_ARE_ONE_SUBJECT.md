# Pass 4447 — the zeta track and the signing track are the same subject

This file exists to be found by a grep that neither track would otherwise run. Per
`CLAUDE.md`, the structural cause of rediscovery here is that two agents work in parallel
and neither reads the other's filenames; the remedy is to write the **result**, not the
topic, somewhere both will hit.

## The identification

A ±1 signing `s` of a graph `X` is a character `χ: H₁(X) → {±1}`, and it defines a connected
double cover `X_s`. The Ihara zeta of the cover **factors**:

```
ζ_{X_s}(u)⁻¹ = ζ_X(u)⁻¹ · L(u, χ)⁻¹
L(u, χ)⁻¹    = det(I − A_s u + (d−1) u² I)
```

The zeros of `L` lie on the circle `|u| = 1/√(d−1)` **exactly when** every eigenvalue of the
signed adjacency matrix satisfies `|λ| ≤ 2√(d−1)`.

> **The Bilu–Linial conjecture is the Riemann Hypothesis for the Artin–Ihara L-function of
> the sign character.**

Verified numerically at Pass 4436: all 80 zeros on the circle to `5.6e-17` for a Ramanujan
signing of W(3,3); 78 of 80 for the trivial gauge field, the two stragglers being exactly
the pair from `λ = 12`.

## Why this needed writing down

Two long lines of work in this repository turn out to be one:

| track | passes | vocabulary |
|---|---|---|
| **zeta / non-backtracking** | Ihara ζ, Bass, Hashimoto `B`, graph RH, the 522×522 and 162×162 linearisations, `w33_pass4222–4244` | zeros, poles, primes, RH |
| **signings / gauge** | Bilu–Linial, ±1 signings, Z₂ gauge fields, magnetic flux, GOE→GUE, `w33_pass4403–4446` | spectral radius, frustration, holonomy |

Neither cites the other. They ask the same question in two languages, and every result in
one is a result in the other. Concretely:

- A **Ramanujan signing** (Passes 4409, 4418, 4426) is a **character whose L-function
  satisfies RH**.
- The **magnetic flux** of Passes 4403–4405 is the U(1) generalisation of the same
  character; the twisted zeta is its L-function.
- The **prime geodesic count** of Pass 4444 has an error term whose decay rate is measured
  at `−1.2388` against the RH prediction `−log(11)/2 = −1.1989`, because the largest
  non-trivial Hashimoto eigenvalue is `3.3166 = √11` exactly.
- **87% of random signings are Ramanujan** (Pass 4438) — i.e. RH for this L-function holds
  for most characters on this graph, which is a statement the zeta track never made because
  it never varied the character.

## Search terms, deliberately dense

Written out so a grep for the *result* finds this file regardless of which vocabulary the
searcher is using:

`Artin-Ihara L-function` · `Bilu-Linial` · `Ramanujan signing` · `sign character` ·
`double cover zeta factorisation` · `det(I - A_s u + (d-1)u^2 I)` · `|u| = 1/sqrt(d-1)` ·
`2*sqrt(d-1)` · `2*sqrt(11) = 6.6332` · `graph Riemann Hypothesis` · `Hashimoto
non-backtracking` · `prime geodesic` · `pi(m) ~ q^m/m` · `q = 11` · `sqrt(11) = 3.3166` ·
`Z2 gauge field on W(3,3)` · `magnetic flux W(3,3)` · `Marcus-Spielman-Srivastava` ·
`interlacing families` · `expander` · `80-vertex 12-regular Ramanujan cover`

## Evidence boundary

The factorisation and the RH equivalence are standard theory, verified numerically here and
claimed as neither new nor mine. What is new **to this corpus** is that the two tracks are
the same subject and should cite each other. No priority is claimed for anything in this
file.
