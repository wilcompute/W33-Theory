# Pass 10961 — exact Albert Cl(9), doubled Cl(10), and the clock grade obstruction

Producer: `analysis/w33_pass10961_albert_clifford10_doubled_clock.py`

Certificates:

- `data/w33_pass10961_albert_clifford10_doubled_clock.json`
- `data/w33_pass10961_albert_clifford9_gammas.json`

Regression: `tests/test_w33_pass10961_albert_clifford10_doubled_clock.py`

## 1. The nine Albert spatial multiplications are already Cl(9)

Pass 10950 constructed the Peirce decomposition of the executable Albert algebra at a primitive idempotent c:

```text
27 = 1 + 16 + 10.
```

Inside the Peirce-0 ten-space, remove the time direction u = e - c. The deterministic nine-vector basis used by Pass 10950 has exact determinant-form Gram matrix

```text
G_spatial = 2 I9.
```

Restrict Jordan multiplication by those nine spatial vectors to the Peirce 16. Denote the resulting rational 16×16 matrices by γ_i.

The producer checks all 81 anticommutators:

```text
γ_i γ_j + γ_j γ_i = 2 δ_ij I16.
```

No rescaling or imported gamma convention is required. The 36 products γ_i γ_j for i < j have exact linear-span dimension 36, matching the compact Spin(9) algebra already certified in Pass 10950.

Thus the same operators previously seen as the nine boost-type Jordan multiplications reconstruct the Euclidean Cl(9) spinor module objectwise.

## 2. The forced 32 = 16 + 16 carrier gives an explicit Cl(10)

On two copies of the Albert 16 define

```text
Γ_i  = [[0, γ_i],
        [γ_i, 0]]          for i=1,...,9

Γ_10 = diag(I16, -I16).
```

All 100 anticommutators close exactly:

```text
Γ_a Γ_b + Γ_b Γ_a = 2 δ_ab I32.
```

The ten grade-1 generators have rank 10 as a matrix subspace. Their 45 pairwise bivectors have rank 45, the dimension of so(10).

This is the first actual Cl(10) Dirac system in this pass sequence. It is stronger than older repository “Spin(10)-sized” or 10+6 spectral-packet observations, which did not construct the ten Clifford vectors.

## 3. The exact Spin(9) half-turn is a π rotation

Pass 10956 froze the rational half-turn U with

```text
U² = -I16.
```

Conjugating the nine γ_i by U produces an exact 9×9 matrix C9. The producer proves

```text
C9ᵀ C9 = I9
det(C9) = 1
C9² = I9
spectrum(C9) = (+1)^7 + (-1)^2.
```

So U is exactly a π rotation in one spatial two-plane, fixing the orthogonal seven-space.

## 4. The minimal doubled clock is not a Spin(10)/Pin(10) vector normalizer

Pass 10959's minimal full-clock carrier uses

```text
G = diag(ζ8^-1 U, ζ8 U),   ζ8 = exp(iπ/4).
```

The exact power ladder is

```text
G² = i Γ_10
G⁴ = -I32
G⁸ = +I32.
```

The crucial conjugation law is

```text
G Γ_i G^-1 = -i Γ_10 Σ_j C9[j,i] Γ_j     for i=1,...,9
G Γ_10 G^-1 = Γ_10.
```

Therefore one clock tick sends the nine spatial Clifford **vectors** into the nine mixed **bivectors** Γ_10 Γ_j.

The original ten-dimensional vector space and its one-tick image intersect only in span{Γ_10}. Equivalently,

```text
dim(V_Cliff + G V_Cliff G^-1) = 19.
```

So the frozen order-eight clock generator does not normalize the Clifford vector space. By the defining Clifford-group criterion, the full C8—and therefore the full transported GL(2,3) action containing it—cannot be identified with a Spin(10) or Pin(10) subgroup in this canonical Albert Cl(10) extension.

## 5. Two ticks return to the vector normalizer

The failure is sharply graded rather than arbitrary. The exact relation is `G² = i Γ_10`.

Hence:

```text
G² Γ_i G^-2 = -Γ_i        for i=1,...,9
G² Γ_10 G^-2 = Γ_10.
```

Thus two ticks normalize the grade-1 vector space, with induced orthogonal action diag(-I9,+1), whose determinant is -1. Four ticks are the central -I32 and act trivially by conjugation.

The clock therefore has an exact Clifford-grade ladder:

```text
0 ticks : Clifford vectors
1 tick  : nine spatial vectors map to nine mixed bivectors; Γ10 fixed
2 ticks : Clifford vectors again; reflection-type orthogonal action
3 ticks : mixed bivectors again
4 ticks : central -I32; trivial conjugation
```

This is a substantially sharper boundary than “32 has the Spin(10) Dirac dimension.” The carrier supports Cl(10), but the clock dynamics is grade-mixing at odd ticks.

## 6. Prior art and external anchor

The repository's earlier `exploration/w33_double_spin16_clifford_bridge.py` identified two 16-dimensional spectral/operator packets with a 10+6 grading. That is useful prior structure, but it does not construct gamma matrices or a Clifford-vector normalizer. Pass 10961 supplies those missing objectwise matrices.

Standard Clifford theory defines the Clifford group by the condition that conjugation preserve the underlying vector subspace, and in even dimension the spinor representation decomposes into two half-spin modules. Those are the standard facts used here to interpret the executable rank and normalization tests; the obstruction itself is proved directly by the committed matrices.

## Boundary

This is an exact Clifford/representation theorem for the canonical Cl(10) extension reconstructed from the executable Albert algebra. It rules out identifying the full doubled order-eight clock with a Spin(10) or Pin(10) vector normalizer **in this extension**.

It does not rule out a larger Clifford carrier, a grade-mixing automorphism of the full Clifford algebra, a projective or semilinear realization, or a different physical Spin(10) embedding. It also does not identify the two Albert 16s with observed fermion chiralities, particles/antiparticles, or a GUT.
