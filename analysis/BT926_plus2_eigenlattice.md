# BT926 — The +2-eigenlattice is NOT the definite E₈ home (open frontier #5)

**Status: honest negative result — rules out the natural definite candidate.**
Script `analysis/bt926_plus2_eigenlattice.py`, data
`data/bt926_plus2_eigenlattice.json`.

BT925 proved the residual of the integral E₈ lift is purely *definiteness*.
The obvious place for a definite E₈ to live is the integer **+2-eigenlattice**
(the SRG eigenvalue r=2, multiplicity 24 = 8×3 — one E₈ per generation?),
because the canonical form `½A` restricted to a +2-eigenvector `v` (`Av=2v`)
is exactly the standard inner product `½vᵀAv = vᵀv`. BT926 extracts it and
tests the hypothesis.

## Construction

`L₂ = { x ∈ Z⁴⁰ : Ax = 2x }`, a primitive rank-24 sublattice of Z⁴⁰, obtained
via an integer Smith normal form with transforms `U(A−2I)V = D` (the 24
columns of `V` with `Dⱼⱼ=0` are a Z-basis; `AK=2K` verified). Its Gram under
the standard inner product is the canonical `½A` form.

## Result — `L₂` is even, definite, but not unimodular

```text
rank 24,  even,  positive-definite,
det(L₂) = 19 349 176 320 = 2¹⁶ · 3¹⁰ · 5,
SNF(Gram) = diag(1⁸, 2⁶, 6⁹, 30),
minimal norm = 6, with exactly 480 minimal vectors (exact Fincke–Pohst
enumeration in Pass 157).
```

Since `det ≠ 1`, `L₂` is **not unimodular**, hence **not E₈³** (det 1, 720
roots) and **not Leech** (det 1). With minimal norm 6 it has **no roots** at
all, so it is not a root lattice. The hypothesis "the three generations are
E₈³ in the +2-eigenlattice" is **false**.

## Reading

The natural definite candidate for the E₈ lift is ruled out: the integral E₈
does **not** sit in the +2-eigenlattice as E₈³ (or any root lattice). This
sharpens open frontier #5 — combined with BT925 (the residual is definiteness)
and BT924 (rank + 2-adic location pinned), we know the definite lift is **not**
the eigenlattice of A. Pass 157 replaces the former dimensional numerology by
the exact primary decomposition
`(Z/2)¹⁶ ⊕ (Z/3)¹⁰ ⊕ Z/5`: the exponents are the Gram-radical dimensions
`16,10,1` at `p=2,3,5`. In particular, the previously unexplained `3¹⁰` is
the image of the square-zero collision operator `(A+I)|1⊥` over `F₃`. The
same pass proves that the 480 minimal vectors are precisely the oriented
local line-pair selectors; their 240 projective rays are the local axis
endpoints used by Pass 123 for the signed E₈ lift.

## The #5 arc (BT924–926), honestly

| step | result |
| --- | --- |
| BT924 | E₈ rank 8 = #(invariant factors = 2); 2-adic location pinned; vertex E₈ certified; naive lift det `3⁴·5·7·179` ≠ ±1 |
| BT925 | canonical symplectic mod-2 form on H = E₈/2E₈; Wu class vanishes; residual proven to be purely definiteness |
| BT926 | the +2-eigenlattice (the natural definite candidate) is even/posdef but det `2¹⁶·3¹⁰·5`, rootless — **not** E₈³ |

**Still open:** a positive-definite even unimodular (E₈-carrying) integral lift
of the chain data — now known to live neither in the naive support-lift
(BT924) nor in the eigenlattices (BT926). This is a genuine research-level
residual; not forced.
