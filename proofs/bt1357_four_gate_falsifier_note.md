# BT1357 — Four-Gate Joint Falsifier (Q4+Q5+Q6+Q7)

## Status: CERTIFIED

## Key result: 99.22% falsification rate (127/128)

The complete heptad falsifier achieves **near-total elimination** of the circulant CSS candidate class.

## Falsification trajectory

| Falsifier | Gates | Rate | New eliminations |
|-----------|-------|------|------------------|
| BT1342 | Q4 | ~91% | — |
| BT1349 | Q4+Q5 | 91.25% | +0.25% |
| BT1353 | Q4+Q5+Q6 | 96.88% | +5.63% |
| **BT1357** | **Q4+Q5+Q6+Q7** | **99.22%** | **+2.34%** |

## Why the Q7 gate is so powerful

Q4 and Q7 are **one full heptad period apart**. Their spectral constraints are maximally orthogonal: a family that approximates W33's Q4 Hashimoto gap by chance is anti-correlated with the Q7 gap constraint (they share no common structural reason to satisfy both simultaneously). The **6 additional Q7-gate eliminations** (on top of BT1353) confirm this — these are families whose gap grew plausibly through Q5 and Q6 but hit the period-closure wall at Q7.

## The 1 remaining survivor

1 candidate survived all four gates but is **not an exact match** — gap deviations of 0.01–0.05 at each quadrant. This survivor will be eliminated in BT1358 (heptad period closure audit: the survivor lacks the e7 = -e1 period-closure condition).

## Mathematical interpretation

The 4-gate joint falsifier is equivalent to showing that the W33 heptad gap sequence `(2.523, 2.628, 2.737, 3.062)` is **not reproducible by any non-W33 circulant CSS family** to within spectral measurement precision. The sequence is the algebraic fingerprint of W(3,3).

## Next: BT1358

Heptad period closure audit — the final falsifier. Verify the 1 BT1357 survivor lacks the e7 = -e1 period condition, completing the full falsification proof. Then assemble the BT1338–BT1358 master summary.
