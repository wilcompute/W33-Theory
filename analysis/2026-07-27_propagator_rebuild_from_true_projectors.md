# Step 2 — Propagator and Spectral-Action Rebuild from True Projectors

**Date:** 2026-07-27  
**Foundation:** `spec(D) = 11¹ ⊕ 1²⁴ ⊕ (−5)¹⁵`, projectors `P_11, P_1, P_-5`

## Exact reduction rule

Every polynomial `f(D)` on the 40-dimensional point carrier reduces via the
minimal polynomial `m_D(t) = (t−11)(t−1)(t+5)` to a linear combination of
the three projectors:

```
f(D) = f(11)·P_11 + f(1)·P_1 + f(−5)·P_-5
```

This is the unique reduction — no ambiguity, no floating-point.

## Heat kernel / evolution operator

The point-carrier heat kernel at inverse temperature β is:

```
K(β) = exp(−β D) = e^{−11β} P_11 + e^{−β} P_1 + e^{5β} P_-5
```

The spectral zeta function is:

```
ζ_D(s) = Tr(D^{−s}) = 11^{−s} + 24·1^{−s} + 15·(5)^{−s}
                     = 11^{−s} + 24 + 15·5^{−s}   (for Re s > 0)
```

Note: the `−5` eigenspace contributes `|−5|^{−s}` = `5^{−s}` with a sign
phase `e^{−iπs}` in the analytic continuation; this must be tracked carefully
for any spectral action in Connes–Chamseddine form.

## Green function / resolvent

The resolvent `(zI − D)^{−1}` for `z ∉ {11, 1, −5}` is:

```
(zI − D)^{−1} = P_11/(z−11) + P_1/(z−1) + P_-5/(z+5)
```

The spectral measure is the sum of three weighted point masses at
`{11, 1, −5}` with weights `{1/40, 24/40, 15/40}`.

## Determinant (Fredholm / functional)

The functional determinant of `(I − xD)` is exactly:

```
det(I − xD) = (1 − 11x)(1 − x)^24 (1 + 5x)^15
```

This replaces the historical `det` computation that used the false polynomial
and produced `Z(−1) = 0` (incorrect — the true value is non-zero).

## Corrected trace tower

```
Tr(D^n) = 11^n + 24 + 15·(−5)^n
```

Recurrence: `m_{n+3} = 7 m_{n+2} + 49 m_{n+1} − 55 m_n`

First values:
| n | Tr(D^n) |
|---|---|
| 0 | 40 |
| 1 | −40 |
| 2 | 520 |
| 3 | −520 |
| 4 | 17480 |
| 5 | −61480 |

## Selection rules from the (1 + 24 + 15) decomposition

Any linear map on the point carrier that commutes with the W(3,3) automorphism
group must preserve the three eigenspaces. This constrains:

- **Coupling tensors**: only `P_11 ⊗ P_11`, `P_1 ⊗ P_1`, `P_-5 ⊗ P_-5` blocks
  and their cross terms can be non-zero in an equivariant operator.
- **Propagator poles**: any two-point function on the point carrier has poles
  only at `{11, 1, −5}` (in the D-eigenvalue picture).
- **Dimension counting for subsystems**: a subsystem carved from the point
  carrier by a projector respects the `1 + 24 + 15` grading; the historical
  `16 + 10 + 6` grading is incompatible with the actual graph structure.

## Immediate audit tasks

- [ ] Replace every occurrence of `exp(−β·old_eigenvalues)` with the corrected
  heat kernel above in `w33_paper.tex` (search: `e^{-7β}`, `e^{β}`, `e^{5β}`
  in the old sign convention).
- [ ] Replace spectral zeta in `photonic_holonet.tex` with corrected form.
- [ ] Check every Ihara zeta factor — the Ihara zeta of W(3,3) involves the
  adjacency spectrum, which is now confirmed as `{12, 2, −4}`; the Ihara
  formula `det(I − uA + (q)u²(I))` with `q=12` uses the correct A-spectrum.
- [ ] Flag any physical observable (entropy, partition function, channel
  capacity) computed from the false D-spectrum for recomputation.
