# October 22, 2026 — q8 ten-point hyperovals fill all 120 hidden line-check dimensions

**Exact repository-level finite-geometry result.** The general theory of hyperovals, projective incidence codes and Hamada ranks is published prior art. The frozen q8 complementary-basis witness is a new-to-repo explicit calculation, not a claim of first discovery. Classical RH unproved.

## Previous mathematical checks

1. The prime-power symplectic noncollinearity code C_B has B²=0 in characteristic p, rank(B)=binomial(p+2,3)^t and an exact q+1 CSS distance. See analysis/w33_20261022_allq_pascal_CSS_exact_distance.py.
2. The classical dual dim of C_B at q8 is 585−64=521. The independently reconstructed 4745 ambient PG(3,8) projective-line checks have rank 401, matching published Hamada point-line rank transfer. See analysis/w33_20261022_hamada_golden_hidden_checks.py.
3. The q4 eight-hyperoval completion already fills rank 61→69. See analysis/w33_20261022_q4_hyperoval_dual_completion.py.
4. Even-type sets and hyperovals are standard projective coding theory, including Adriaensen (2023), https://doi.org/10.1137/23M1556277.

## Exact q8 witness

Represent F8 as F2[z]/(z³+z+1). Its standard projective plane x3=0 contains the hyperoval formed by the ten points

    [1,a,a²,0] for a in F8,
    [0,0,1,0], and [0,1,0,0].

This is an ordinary plane conic (nine points) plus its nucleus. Any invertible projective linear transformation preserves the hyperoval property.

Construct all 585 canonical PG(3,8) projective points and all 4745 projective lines using reduced-row-echelon 2D subspaces. The line incidence masks have binary rank exactly 401.

Beginning with the ten-point hyperoval, use the deterministic seed 20261022 and successive nontrivial GL4(F8) elementary shears. Reduce each resulting ten-point indicator modulo the current line-plus-hyperoval binary span and keep it if independent. The producer reaches rank 521 after **120 independent hyperovals in exactly 128 shear steps**.

Every witness passes the exact binary orthogonality check against all 585 noncollinearity rows B. Those rows each have q³=512 entries. The frozen witness support sequence has SHA256:

    a5a43a18acc15681c9976d1666f35a5687e7caf0293ec961c868966a0e946113

The first and last selected supports, in canonical projective-point ordering, are:

    (0,72,160,232,304,376,400,472,512,576)
    (81,84,163,164,282,283,441,446,490,494).

By the known rank(B)=64, ker(B) has dimension 521; the 401-dimensional line span plus these 120 new independent hyperoval rows is therefore the **entire** classical dual code.

## Engineering distinction

The resulting classical linear parity-check family uses 4745 checks of weight 9 and 120 extra checks of weight 10, with 521 independent constraints. This is a sparse classical-check architecture for the 64-dimensional binary code C_B.

The associated CSS code is [[585,457,9]]_2, but **line and hyperoval checks belong to C_B^perp and are not automatically elements of its stabilizer space C_B**. Do not confuse classical parity-check completeness with a low-weight quantum stabilizer extraction scheme, or claim a hardware fault-tolerance threshold. The program proves no classical RH result.

## Code

- analysis/w33_20261022_q8_hyperoval_dual_completion.py
- tests/test_w33_20261022_q8_hyperoval_dual_completion.py
- workflow .github/workflows/w33-pascal-CSS-hamada-hidden-checks.yml
- CI-produced data/w33_20261022_q8_hyperoval_dual_completion.json

## Five independent follow-ups

1. Derive a rigorous general hyperoval-generation completeness criterion for PG(3,2^t), or find a counterexample at q16 using incidence module methods rather than huge matrices.
2. Explicitly decompose the missing check quotient under Sp(4,4) and Sp(4,8), finding natural irreducible modules and geometric stabilizers of the hyperovals.
3. Engineer real syndrome measurements using only valid self-orthogonal CSS checks (or a gauge-subsystem construction) and test depth, weight, correlated noise and decoder threshold.
4. Connect the golden Hamada Fibonacci transfer to the modular representation decomposition without mistaking its unequal-absolute-value eigenvalues for Weil-pure Frobenius spectra.
5. Refocus the classical RH search on high-precision arithmetic spectral triples and interval-certified completed Weil positivity, independently of finite projective-code achievements.
