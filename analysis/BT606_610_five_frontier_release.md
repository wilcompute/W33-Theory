# Passes 606–610: complete torsion, flatness, symmetry, hardware, and inference

This release executes the five non-sequential directions following Pass 605. Each result has a deterministic script, immutable JSON certificate, and focused regression.

## Pass 606 — complete integral Smith normal form

A reproducible GitHub Actions PARI/GP run factors the residual 62-digit determinant cofactor as

- `587147981829636393642873223241`,
- `75144583858746017876203917172673`.

PARI reports both factors prime with exponent one and verifies their product. Combining this with the exact elementary-divisor profiles from Passes 597 and 601 produces the complete 280-entry Smith diagonal: 233 unit entries followed by 47 nontrivial invariant factors. The script verifies the divisibility chain and reconstructs the exact 325-digit determinant.

## Pass 607 — nonabelian flat-sector closure

The clique complex of `J(8,3)` has 56 vertices, 420 edges, and 840 triangle 2-cells. A spanning-tree presentation starts with 365 free generators. A deterministic sequence of 365 elementary Tietze eliminations removes every generator and every relator, proving

`pi_1(Cl(J(8,3))) = 1`.

Therefore every triangle-flat connection with values in any discrete group is gauge equivalent to the trivial connection. The curved Pass-594 connection is not affected by this theorem.

## Pass 608 — torsion symmetry boundary

For the exceptional degree-six `S5` action, its `A5` restriction, and the outer-`S6` six-point action, the augmentation commutant has dimension one over `Q`, `F2`, and `F3`. The fixed twisted torsion object consequently has only scalar parallel symmetries. Treating fibre holonomy as a non-scalar global action on the fixed cokernel would require extra equivariant connection data.

The exact filtration dimensions are

- `2`-primary: `47,15,8,3,2,1`,
- `3`-primary: `40,16,3,1,1,1,1`.

## Pass 609 — tetrahedral hardware gauge

The four antipodal yellow-face pairs of the certified snub coloring become four control rails. The six Hamming-weight-two rail words are identified with the six Pass-596 exterior rank-pairs and reproduce the Wilson multiset

`{-168,-84,-84,56,56,112}`.

An orientation bit distinguishes `(i,j)` from `(j,i)`, removes the residual `A4` stabilizer, and compiles `U` versus `U^{-1}`. The combinatorial mapping is exact; the proposed phase tags remain a device convention requiring calibration.

## Pass 610 — calibrated optimal Wilson inference

For the recorded response matrix, phase bias, and pilot covariance, the exact maximin photon fractions are

- `108965/129909` for `Tr(U)`,
- `20944/129909` for `Tr(U^2)`,
- `0` for `Tr(U^3)`.

An exact dual linear-program certificate proves optimality. With 100 photons the integer allocation is `84/16/0`, and the deterministic Gaussian maximum-likelihood confusion calculation gives worst-class correctness `0.996287624229`. The third trace remains valuable as a held-out model-falsification channel.

## Validation

The five scripts pass 46 of 46 internal checks, regenerate byte-identical certificates under `--check`, compile, and pass the focused regression.
