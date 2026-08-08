## Pass 4200 — independent verification of Pass 4191's Ihara factorisation

The parallel track's Pass 4191 states, for the degree-four Levi graph with spectrum
`4¹, (−4)¹, (√6)²⁴, (−√6)²⁴, 0³⁰`:

```
ζ⁻¹(u) = (1−u²)⁸¹ (1−9u²) (1+9u⁴)²⁴ (1+3u²)³⁰
```

Recomputed symbolically from Bass's determinant relation
`ζ⁻¹(u) = (1−u²)^(E−V) · det(I − Au + (k−1)u²I)`:

```text
V 80   E 160   E-V 80
Bass reproduces their closed form: True
```

**Confirmed exactly.** The pieces:

- `λ = ±4` contribute `(1−u)(1−3u)(1+u)(1+3u) = (1−u²)(1−9u²)` — this is where the
  **81st** power comes from: 80 from the prefactor plus one from inside the determinant.
- `λ = ±√6` pair as `(1−√6u+3u²)(1+√6u+3u²) = (1+3u²)² − 6u² = 1+9u⁴`, giving `(1+9u⁴)²⁴`.
- `λ = 0` gives `(1+3u²)³⁰` directly.

---

## Why this matters to *this* track

Passes 3060 and 3080 tried the same question on the instruction graph and failed twice:
3060 applied a `k`-regular formula to a graph with degrees 2–8; 3080's replacement
returned 0 % of poles in band and was withdrawn as a symptom.

> **Two differences in their approach, both of which I should adopt.** Their graph is
> genuinely `4`-regular, so the regular formula applies — mine was not, which is exactly
> what broke 3060. And they used Bass to obtain a **factored polynomial** rather than
> chasing numerical pole radii, which makes the pole structure readable instead of
> something you measure and then have to trust.

This also gives my implementation a **second reference** beyond `K₄` — and a much better
one, since it is a large graph with a non-trivial closed form. The `(1−u²)^(E−V)` prefactor
interacting with a `(1−u²)` factor *inside* the determinant is precisely the kind of
bookkeeping a small reference cannot exercise.

## Ledger

| claim | status |
|---|---|
| Pass 4191's factorisation | **verified independently**, symbolic |
| the 81st power's origin (`80 + 1`) | explained |
| my Bass logic against a second reference | validated |
| the factored-polynomial method | adopted for the next attempt |

## Prior art

- **Parallel track Pass 4191** — owns the factorisation, the spectrum, the bipartite
  Ramanujan property, and the Hashimoto radius 3 / zeta radius 1/3.
