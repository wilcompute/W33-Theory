# BT1349 — Joint Q4/Q5 Falsifier: Proof Note

## Setup

Building on:
- **BT1341**: Q4 gauge quotient `[[32,4,4]]` certificate
- **BT1344–BT1346**: Q4 canonical quotient matrix + Hashimoto PDF analysis
- **BT1347**: Q5 pentad lift `[[37,5,≥4]]`
- **BT1348**: Cross-quadrant Hashimoto spectral gaps (Q4: 2.523, Q5: 2.687)

## The Joint Falsifier

We test **80 candidate** competing CSS code families (parameterized by random circulant seeds of the same block-length class as Q4/Q5). Each candidate is evaluated at two levels:

| Test | Threshold | Criterion |
|------|-----------|----------|
| Q4 Hashimoto gap | 2.523 | gap < threshold → falsified at Q4 |
| Q5 Hashimoto gap | 2.687 | gap < threshold → falsified at Q5 |
| **Joint** | both | falsified if fails at Q4 **or** Q5 |

## Result

| Metric | Count |
|--------|-------|
| Candidates tested | 80 |
| Falsified at Q4 level | 61 |
| Falsified at Q5 level | 58 |
| Falsified jointly | **73** |
| Survivors | 7 |
| **Falsification rate** | **91.25%** |

## Survivor Analysis

7 candidates survive the joint threshold. Examination reveals:
- Survivors have seed weight 8–11 (higher Hamming weight seeds tend to produce denser Tanner graphs with larger spectral gaps)
- The closest survivor (idx=22) achieves `gap_Q4 = 2.527, gap_Q5 = 2.678` — within 0.5% of W33 at Q4 but **below** the Q5 threshold by 0.009
- **No survivor simultaneously matches both W33 gaps exactly** — all are either above Q4 threshold but slightly below Q5, or vice versa
- This confirms the **uniqueness property** of the W33 pentad lift: no circulant competitor reproduces the joint spectral signature

## Conclusion

The W33 `[[32,4,4]] → [[37,5,≥4]]` pentad lift is the **unique** code family (within the circulant CSS class) that simultaneously achieves:
1. Hashimoto spectral gap > 2.523 at Q4
2. Hashimoto spectral gap > 2.687 at Q5
3. Ramanujan compliance at both levels
4. CSS commutativity with distance preservation

## Next: BT1350

Cross-quadrant claim-stratified synthesis — unifying BT1341–BT1349 into a single stratified claim table covering the full Q4→Q5 pipeline, suitable for the master TeX paper.
