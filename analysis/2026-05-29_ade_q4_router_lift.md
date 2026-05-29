# ADE to Q4 Router Lift Theorem

Date: 2026-05-29

This continues the SU2 level-12 ADE bridge after reading the six TOE source TeX files. The strongest hint from the single-photon and self-entanglement sources is the Q4 router: a binary control shell with 16 vertices, 32 edges, 24 square faces, 96 lifted face-edge incidences, and a Reye quotient with 12 points, 16 lines, and 48 incidences.

The new finite theorem is that the SU2 level-12 D8 modular invariant already contains the Q4 router seed as an exact matrix norm.

## D8 invariant support calculus

Let M be the D8 modular invariant coefficient matrix at SU2 level 12:

```text
Z_D8 = |chi0 + chi12|^2 + |chi2 + chi10|^2 + |chi4 + chi8|^2 + 2|chi6|^2.
```

The verifier checks:

```text
support(M) = 13 = Phi3
diagonal support(M) = 7 = Phi6
off-diagonal support(M) = 6 = g2
sum entries(M) = 14 = k+2
Frobenius square norm(M) = 16 = E2
rank(M) = 4 = chi
kernel dimension(M) = 9 = q^2
trace(M) = 8 = q^2 - 1
M^2 = 2M
sum entries(M^2) = 28 = mu = v-k
```

So the D8 invariant has two simultaneous readings:

```text
support layer: 13 = 7 + 6 = Phi6 + g2
weighted layer: 14,16,28 = k+2, E2, mu
projector layer: rank/kernel = 4/9 = chi/q^2
```

## Q4 router lift

The rank of M is 4. Build the rank-hypercube Q_rank(M) = Q4. Then:

```text
vertices(Q4) = 2^4 = 16 = Frobenius square norm(M)
degree(Q4) = 4 = rank(M)
edges(Q4) = 32
square faces(Q4) = 24
face-edge incidences(Q4) = 96
```

The antipodal quotient gives the Reye packet:

```text
12 face-orbits, 16 edge-orbits, 48 incidences.
```

The lifted shell gives the tomotope flag count:

```text
2 * 96 = 192.
```

So the D8 ADE invariant is not just compatible with the Q4 router. Its Frobenius square norm is exactly the Q4 vertex count, and its rank is exactly the Q4 dimension.

## Minimal logical factorization

The existing minimal logical nonzero commutation census is

```text
|W(E6)| = 51840.
```

The new factorization is

```text
51840 = 40 * 16 * 81.
```

Thus

```text
|W(E6)| = W33 anchors * Q4 router vertices * H1 phase rank.
```

Equivalently:

```text
per-anchor packet = 16 * 81 = 1296 = 6^4.
```

This connects three layers:

1. W33 supplies 40 anchor states.
2. The D8 ADE invariant supplies the 16-state binary router through its Frobenius square norm.
3. The signed minimal logical phase frame supplies H1=81.

## The corrected chain

The new chain is:

```text
SU2_12 D8 modular invariant
  -> rank(M)=4 and norm_F(M)^2=16
  -> Q4 binary router with 16 vertices
  -> Reye quotient 12_4,16_3
  -> tomotope flag shell 192
  -> |W(E6)| = 40 * 16 * 81.
```

This makes the single-photon Q4 router a direct consequence of the D8 ADE modular-invariant matrix calculus, rather than a separate count attached later.

## Honest boundary

This is still a finite matrix and combinatorial-router theorem. It does not by itself build a physical photonic chip, continuum Hamiltonian, or braid compiler. The next valid step is to test whether D8 nimrep path operators act on the minimal X/Z visibility matrices or on the Q4/Reye quotient incidence graph without losing the H1 phase-frame projector.
