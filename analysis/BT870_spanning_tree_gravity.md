# BT870 — Gravity From Spanning Trees: τ(W₃,₃) = 2⁸¹·5²³

**Status: PROVEN (exact integer Matrix-Tree, cross-checked by cofactor determinant, `analysis/bt870_spanning_tree_gravity.py`, data `data/bt870_spanning_tree_gravity.json`)**

Mined from W33_FOR_EVERYONE.tex §"Gravity from spanning trees": the finite
gravitational bridge is the discrete Matrix-Tree action
S = (M_P²/2)·ln τ(G), with τ the spanning-tree count. For the substrate
this is computable to the last digit — and the answer writes the
matter-sector dimension into the exponent.

## The exact partition functions

W(3,3) = SRG(40,12,2,4) has Laplacian spectrum {0, 10²⁴, 16¹⁵}
(0; k−r = 10 with mult f = 24; k−s = 16 with mult g = 15). By the
Matrix-Tree theorem,

```text
τ(W33) = 10²⁴ · 16¹⁵ / 40 = 2⁸¹ · 5²³
```

verified two independent ways (eigenvalue product and the reduced-Laplacian
cofactor determinant). The factorization is loaded with substrate meaning:

- **2-exponent = 81 = q⁴ = dim(matter sector) = dim(Steinberg module)** (BT861);
- **base 5 = F₅** — the tier-ladder prime (r = 27/80 = 3³/(2⁴·5));
- **5-exponent = 23 = f − 1** (one less than the r-eigenvalue multiplicity).

The complement Q = SRG(40,27,18,18) (the matter/non-collinearity graph,
Pillar 109) has Laplacian {0, 30²⁴, 24¹⁵} and

```text
τ(Q) = 30²⁴ · 24¹⁵ / 40 = 2⁶⁶ · 3³⁹ · 5²³
```

with **3-exponent = 39 = q·Φ₃ = dim(gauge sector) = rank(∂₀)**.

## Reading

The substrate's gravitational partition function is not a fitted number — it
is 2^(matter dim)·5^(F₅), and the dual matter graph adds 3^(gauge dim). The
Matrix-Tree action factors:

```text
S/(M_P²/2) = ln τ(W33) = 81 ln 2 + 23 ln 5 = 93.16…
```

So "gravity as the thermodynamics of the spanning-tree ensemble" has the
matter and gauge sector dimensions as its **literal logarithmic charges**:
the entropy of the discrete-gravity ensemble counts the matter register
(power of 2) and, on the complement, the gauge register (power of 3), with
the cosmological tier-prime 5 = F₅ common to both. The three Standard-Model
sector sizes — q⁴ = 81 matter, q·Φ₃ = 39 gauge, F₅ = 5 cosmological — are
exactly the prime-exponent data of the substrate's two spanning-tree counts.

## Open

- The line graph / dual gravity: τ of the 40-line incidence and the
  240-edge medial graph — does the Steinberg 81 reappear?
- M_P normalization: the W33_FOR_EVERYONE bridge claims the curved-refinement
  limit gives Einstein–Hilbert with the right coefficient; the exact ln τ
  here is the finite seed of that coefficient — pin the numerical match.
- 23 = f − 1 as a "leech-adjacent" prime (24 = f = Leech kissing dim / 24-cell);
  the common 5²³ across both graphs is the shared cosmological charge.
