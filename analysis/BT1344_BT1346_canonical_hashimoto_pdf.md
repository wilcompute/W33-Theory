# BT1344--BT1346 -- Canonical Quotient, Matrix Falsifier, and Claim-Stratified PDF

## BT1344 -- Quotient canonicalization

Added:

```text
tools/bt1344_canonicalize_q4_quotient.py
data/bt1344_q4_quotient_canonicalization.json
proofs/BT1344_q4_quotient_canonicalization.md
```

Result:

```text
Q4 automorphism group order = 384
quotient orbit size = 384
stabilizer size = 1
```

The BT1341 quotient is valid but generic under full Q4 cube symmetry.

## BT1345 -- Matrix-derived Hashimoto falsifier

Added:

```text
tools/bt1345_hashimoto_matrix_falsifier.py
data/bt1345_hashimoto_matrix_summary.json
proofs/BT1345_hashimoto_matrix_falsifier.md
```

Result:

```text
standard Hashimoto phase clusters = 72.452 degrees and 127.087 degrees
protocol targets = 63.435 degrees and 112.208 degrees
```

The protocol targets do not match the standard non-backtracking Hashimoto matrix. The protocol must either define a nonstandard normalized observable or update the target angles.

## BT1346 -- Claim-stratified PDF build

Added:

```text
.github/workflows/q4-claim-stratified-paper.yml
data/bt1346_pdf_manifest.json
```

Local build:

```text
w33_q4_claim_stratified_master.pdf
4 pages
pdflatex, two passes
```

Regression:

```text
tests/test_bt1344_bt1346_canonical_hashimoto_pdf.py
```
