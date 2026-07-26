# Pass 1059 amendment: late parallel Pass5 integration

A fifth parallel pass landed while Passes 1054--1059 were being committed. This amendment records the merged result and supersedes the earlier 71-check total.

## Retained correction

Parallel Pass5 correctly rebuilds the W33 spectrum as

\[
12^1,\qquad 2^{24},\qquad (-4)^{15},
\]

repairing the Pass3/4 multiplicities \(26,13\). The trace checks are exact:

\[
1+24+15=40,
\]
\[
12+2\cdot24-4\cdot15=0,
\]
\[
12^2+2^2\cdot24+(-4)^2\cdot15=480.
\]

## Remaining fail-closed boundaries

The late pass does not close the following gaps:

1. `analysis/pass5_step5_s4_coset_dictionary.py` sorts coordinate patterns under all raw coordinate permutations. It does not verify that those permutations preserve the chosen symplectic form, construct an \(S_4\) or \(S_4\times C_2\) subgroup inside \(PSp(4,3)\), or enumerate its 540 cosets. Thus \(540=25920/48\) remains an order/index identity until the order-48 subgroup and its geometric role are explicitly constructed.

2. The CF budget still uses \(N=120\) as the number of W33 contexts. The generalized quadrangle has 40 line contexts. The statistical and timing claims must be recomputed from a declared raw-shot protocol over those 40 contexts.

3. `analysis/pass5_step2_pass575_fix.lean` is a proposed snippet. It does not modify the actual formal module and no successful module or full-library build artifact accompanies the commit. The polynomial correction is useful; the Lean repair remains unverified.

4. The exact Ihara circle is retained. The asserted equality with a Weil zeta function still requires an explicit variety or stack, point counts over all finite extensions, and equality of Euler factors.

5. The CMB scripts still contain no data ingestion, covariance, transfer function, or likelihood evaluation, so the printed bounds are not a reproduced Planck/LiteBIRD analysis.

## Authoritative release

Pass 1059 v3 adds four exact audit checks for these late claims. The six-pass package now contains

\[
14+10+12+8+7+24=75
\]

passing checks. The authoritative compact ledger is `data/w33_pass1054_1059_release.json` schema `w33.pass1054_1059.release.v2`.
