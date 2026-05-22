# 2026-05-22 - Minimal Support Geometry Theorem

## Short version

The May 18 minimal-logical invariants are not just enumerated code data. They have a direct finite-geometric support model inside the collinearity graph of `W(3,3)`.

```text
X_min supports = isotropic line-stars
Z_min supports = ordinary quadrangles
```

This turns the prior minimal logical surface into a clean geometry:

```text
160 = 40 isotropic K4 lines * 4 point-stars per line
1620 = ordinary quadrangles of SRG(40,12,2,4)
```

## Theorem

Let the W33 collinearity graph be the strongly regular graph `SRG(40,12,2,4)` built from the symplectic form on projective points of `F_3^4`.

1. Each projective minimal `X` support is a **line-star**: choose a totally isotropic line `L ~= K4` and a point `p in L`; take the three graph edges from `p` to the other three points of `L`. There are `40*4 = 160` such supports.
2. Each projective minimal `Z` support is an **ordinary quadrangle**: choose a noncollinear pair `{a,b}` and two of its four common neighbours `c,d`; take the 4-cycle `a-c-b-d-a`. There are `(540*C(4,2))/2 = 1620` such supports.
3. With the natural `F_3` coefficients on line-stars and quadrangles, the pairing matrix reproduces the full previous invariant stack:
   - support biregularity: `160*81 = 1620*8 = 12960`;
   - unsigned X-overlaps: `1^6480, 3^4320, 9^1440, 27^480`;
   - signed phase frame: `Spec(A A^T) = 160^81 + 0^79`.

## Why this matters

Before this pass, the theorem stack said:

```text
forget phase -> |W(E6)| = 51840
retain phase -> rank(A) = 81
```

Now we can say what the supports actually are.

```text
minimal X = local star defects inside isotropic K4 lines
minimal Z = global quadrangle exchange loops
```

That is a stronger bridge between the three TeX narratives:

- `w33_paper.tex` gives the full W33 finite-physics spine;
- `W33_FOR_EVERYONE.tex` insists on separating exact finite theorems from bridges/interpretation;
- `single_photon_universal_computation.tex` treats W33 as the qutrit/photonic gate geometry.

This result belongs in the exact finite theorem tier. The photonic interpretation is then natural but secondary: line-stars are local three-edge qutrit defects inside a four-point isotropic optical context, while quadrangles are four-step exchange loops between noncollinear states.

## Machine certificate

Added:

- `analysis/w33_minimal_support_geometry.py`
- `data/w33_minimal_support_geometry.json`

The script reconstructs the geometry from scratch and checks every identity above.
