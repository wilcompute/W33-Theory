# Part CCCCXXIII: A(7) Representation Theory and Csaszar K7 CSS Toric Code

**Status:** verified representation-theory and local toric-code refinement of the 7-mode photonic harmonic TQC algebra.

## Result

Part CCCCXXII built the 7-mode photonic harmonic algebra:

```text
A(7) = Span{ a_i, a_i^dagger : i = 0..6 }
```

CCCCXXIII resolves two deeper layers.

## 1. Representation-Theory Layer

The 7 modes carry the standard finite algebra dimensions:

```text
dim U(7)  = 49 = Phi6^2
dim SU(7) = 48 = Phi6^2 - 1
dim G2    = 14 = 2*Phi6
```

The K7 hopping shell has:

```text
eigenvalues: 6 (x1), -1 (x6)
spectral gap: 7 = Phi6
det adjacency: 6 = Phi6 - 1
ground energy: -6
```

The 21 K7 bond operators branch as:

```text
21 = 14 + 7 = G2_adj + G2_fund
```

The Fano cubic interaction has 7 triple operators, each mode occurs in exactly `q=3` Fano cubics, and creation plus annihilation gives:

```text
2*7 = 14 = dim G2
```

## 2. Csaszar K7 CSS Toric Code

The Csaszar torus has:

```text
V = 7
E = 21
F = 14
chi = 0
genus = 1
```

Over `GF(2)`, its chain complex gives:

```text
rank H_Z = 6
rank H_X = 13
H_Z H_X^T = 0
k = 21 - 6 - 13 = 2
```

So the local toric code is:

```text
[[21,2,>=3]]
```

with ground-state degeneracy:

```text
2^2 = 4 = mu
```

## Boundary

The distance statement is a lower-bound/local toric-code statement on the Csaszar K7 triangulation. It does not replace the protected W33 Steane/Phi6 layer `[[82320,81,>=81]]`, and it does not upgrade the Q4 packet layer beyond `[[1296,81,4]]`.

Artifacts:

- Script: `exploration/PART_CCCCXXIII_A7_REPRESENTATION_CSS_TORIC.py`
- Results: `PART_CCCCXXIII_a7_representation_css_toric_results.json`
- Tests: `tests/test_a7_representation_css_toric_ccccxxiii.py`
