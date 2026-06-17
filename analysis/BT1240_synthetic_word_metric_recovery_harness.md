# BT1240 -- Synthetic Word-Metric Recovery Harness

## Purpose

BT1240 turns the BT1237 recovery bands into an executable synthetic harness.  Instead of only defining thresholds, it generates finite recovered gate cases and scores them against the exact BT1233 word-metric fingerprint.

## Reference target

The reference target is

\[
|G|=51840,
\qquad
\operatorname{diam}=14,
\]

with sphere histogram

\[
1,8,36,126,363,916,2052,4096,7396,12170,16916,7247,476,36,1,
\]

and checkpoint balls

\[
|B_4|=534,
\quad
|B_8|=14994,
\quad
|B_{12}|=51803,
\quad
|B_{14}|=51840.
\]

## Synthetic cases

The harness evaluates four cases:

1. `exact`: the BT1228 / BT1231 four-transvection set.
2. `drop_last`: only the first three transvections.
3. `swap_last`: replace the fourth transvection by another transvection.
4. `identity_last`: replace the fourth transvection by identity.

## Results

The exact case passes.  The dropped-generator case collapses to order \(648\).  The swapped-generator case still reaches order \(51840\), but has diameter \(10\) and fails the word-metric fingerprint.  The identity replacement fails the local order-three law and also collapses to order \(648\).

## Boundary

This is synthetic finite recovery.  It is not experimental tomography, but it is the next harness layer needed before feeding in real or simulated noisy gate data.

## Files

- Code: `analysis/bt1240_synthetic_word_metric_recovery_harness.py`
- Result: `data/bt1240_synthetic_word_metric_recovery_harness_summary.json`
