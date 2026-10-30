# Passes 1907–1911 release

## Status

`PASS_WITH_GLOBAL_U6_RUNTIME_BOUNDARY`

Frozen verification: **48/48** assertions.

Aggregate SHA-256:

`7d2ddba245bf2cf9912b33f3cb1e67751c50b5dda06c9fa88af255dc130f1111`

## Delivered

- **1907:** executed an exact `2,190,670`-error U6 chart shard, obtaining `1,830,866` syndrome groups and `1,349,896` nonlower shard singletons. The complete chart is exactly `6,230,484,547` records, requiring a `99,687,752,752`-byte sort stream and `778,810,569`-byte external bitmap. Global `U6` remains open.
- **1908:** completed all 156 residual-orbit contractions. The exact `20+180+40` enumerator has `2^45` words and `7,355` nonzero bins, reproduces all 91 ordinary coefficients, and contains a literal `C2 x C2` complement subcode.
- **1909:** classified all 56 subgroup classes of exceptional `S6`: phase counts `(24,90,114)=(26,22,12)`. The `PSp` and paired-`S6` complex structures generate `so(3)` on three `A6` copies, not a quaternionic pair.
- **1910:** proved unsigned `KG(6,2)` minimal-line incidence is phase-blind and derived exact conjugation-odd linear cuts on the `C4`-oriented 60-vector lift. The false `K10 <= 5` bound is excluded.
- **1911:** reconstructed stabilizer-weighted primitive holonomy and separated the shared `36`-dimensional `V9` channel from the `54`-dimensional Hashimoto complement.

## Provenance and parallel integration

Passes 353/355 already own the general Weil-chirality and Frobenius–Schur frame through Gow (1985) and Vinroot (2010). Pass 1909 newly contributes the complete 56-class exceptional-S6 phase poset and the A6 `so(3)` reconciliation.

At q=3 the outer `W(E6)/PSp(4,3)` involution is complex conjugation on complex-type irreducibles; q=5 refutes a general-q extrapolation. The phase also requires the signed oriented-edge module. `sigma_S` is an outer symplectic similitude, not a symplectic element. The spread value `5` is only the exact average `45/9`; `13` is attained and the `>=14` decision remains `UNKNOWN`.

## Boundaries

- No global sixth-order BSC coefficient is claimed.
- Applying the oriented Gaussian cuts requires the literal chart-to-solver transport.
- Holonomy and phase statements are finite representation/graph invariants, not physical evolution laws.
