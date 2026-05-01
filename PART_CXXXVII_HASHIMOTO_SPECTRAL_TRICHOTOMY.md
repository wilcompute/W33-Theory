# Part CXXXVII — Hashimoto Spectral Trichotomy of W(3,3)

## Statement

Let `B` be the 480 × 480 Hashimoto (non-backtracking) operator on the directed
edge set of W(3,3) — equivalently the strongly regular graph SRG(40, 12, 2, 4).
Let `n = |V| = 40`, `m = |E| = 240`, `k = 12`, `q = k − 1 = 11`. The full
spectrum of `B` decomposes into exactly three magnitude classes:

| layer            | magnitude        | multiplicity | source                                  |
|------------------|------------------|--------------|-----------------------------------------|
| Perron           | `\|μ\| = 11`     | 1            | adjacency root λ = 12                   |
| Ramanujan        | `\|μ\| = √11`    | 78           | adjacency roots λ ∈ {2, −4} (24+15 each, doubled) |
| Trivial / mate   | `\|μ\| = 1`      | 401          | Bass trivial 2(m−n) = 400 plus Perron-mate μ = 1 |
| **total**        |                  | **480**      | = 2m                                    |

## Proof

By Bass (1992), for any (q+1)-regular graph the determinantal identity

\[
\det(I - uB) \;=\; (1 - u^2)^{m-n}\,\det\!\bigl(I - uA + qu^2 I\bigr)
\]

implies that every Hashimoto eigenvalue `μ` is either:

1. a root of `μ² − λμ + q = 0` for some adjacency eigenvalue `λ` of `A`, or
2. a "Bass trivial" eigenvalue ±1 with combined multiplicity `2(m − n)`.

For W(3,3) the adjacency spectrum is closed-form
`{12 (×1), 2 (×24), −4 (×15)}` (SRG parameters give λ = (k+θ_2+θ_3) and
multiplicities f, g; here θ_2 = 2, θ_3 = −4, f = 24, g = 15).

* **Perron λ = 12.** Roots of `μ² − 12μ + 11 = 0` are `μ ∈ {11, 1}`. The 11
  is the unique Perron eigenvalue; its mate at 1 lands in the |μ|=1 layer.
* **λ = 2.** Discriminant `4 − 44 = −40 < 0`, complex roots
  `μ = 1 ± i√10`, magnitude `√(1+10) = √11`. Multiplicity 24, doubled = 48.
* **λ = −4.** Discriminant `16 − 44 = −28 < 0`, complex roots
  `μ = −2 ± i√7`, magnitude `√(4+7) = √11`. Multiplicity 15, doubled = 30.
* **Bass trivial.** `2(m − n) = 2 · 200 = 400` copies of ±1 (200 each).

Adding: 1 (Perron) + (48 + 30) (Ramanujan) + (1 Perron-mate + 400 Bass) =
**1 + 78 + 401 = 480 = 2m**. ∎

## Corollary (Ihara–GRH for W(3,3))

All 78 nontrivial Hashimoto eigenvalues satisfy `|μ| = √q = √11` exactly. Via
the substitution `u = 1/μ`, the nontrivial zeros of the Ihara zeta

\[
Z_{W(3,3)}(u) \;=\; \frac{1}{\det(I - uB)}
\]

lie precisely on the critical circle `|u| = 1/√11 = 1/√(k−1)`. W(3,3) is a
**Ramanujan graph**.

## Identities

* `1 + 78 + 401 = 480 = 2m`
* `78 = 2(f + g) = 2(24 + 15) = 2 · 39`
* `401 = 2(m − n) + 1 = 2 · 200 + 1`
* `λ = 12 ⇒ μ² − 12μ + 11 = 0 ⇒ μ ∈ {11, 1}`
* `λ ∈ {2, −4} ⇒ |μ|² = (λ/2)² + (4q − λ²)/4 = q = 11`

## Why this matters for the W(3,3) ToE

The operator `B` is the *generation transport* on edges (Part CXXXIV‑CXXXVI):
its Perron projector encodes the asymptotic Doob bridge measure with bridge
entropy `log(11)`. The spectral trichotomy tells you exactly which sectors
contribute at every time scale:

* **Hadronic / fast** (`n ≤ 3`): all 480 modes contribute; bridge entropy
  `log 2`.
* **Mid** (`4 ≤ n ≤ 6`): trivial and Ramanujan layers decay together at
  geometric rate `1/√11`; only the Perron mass survives.
* **Asymptotic** (`n ≥ 7`): only the unique `μ = 11` mode dominates; bridge
  entropy `log 11`, ratio `11/480` per Theorem CXXXVI.

The `√11` cutoff is the spectral gap of the Ihara zeta and equivalently the
diffusion barrier between the three generations encoded by `(f, g, 1)`.

## Files

| file | role |
|------|------|
| `PART_CXXXVII_HASHIMOTO_SPECTRAL_TRICHOTOMY.py` | runnable derivation + JSON report |
| `tests/test_hashimoto_spectral_trichotomy_cxxxvii.py` | 13 regression identities (Bass + direct diagonalisation) |
| `PART_CXXXVII_hashimoto_spectral_trichotomy_results.json` | machine-readable summary |

## Status

Theorem-grade: Bass-formula prediction matches direct numerical
diagonalisation of `B` to machine precision. Both certify the
trichotomy `{1, 78, 401}` and the Ramanujan property `|μ_nontriv| = √11`.
