# BT1344--BT1346 -- Canonical Quotient, Matrix Hashimoto, Claim-Stratified PDF

## BT1344 -- Q4 quotient canonicalization

Added:

```text
tools/bt1344_canonicalize_q4_quotient.py
data/bt1344_q4_quotient_canonicalization.json
proofs/BT1344_q4_quotient_canonicalization.md
```

Result:

```text
orbit size = 384
stabilizer size = 1
```

The BT1341 quotient is valid but generic under the full Q4 cube automorphism group.

## BT1345 -- Matrix-derived Hashimoto falsifier

Added:

```text
tools/bt1345_hashimoto_matrix_falsifier.py
data/bt1345_hashimoto_matrix_summary.json
proofs/BT1345_hashimoto_matrix_falsifier.md
```

The exact non-backtracking matrix on W(3,3) has phase clusters:

```text
72.452 degrees, multiplicity 48
127.087 degrees, multiplicity 30
```

These do not match the inherited synthetic protocol targets 63.435 and 112.208 degrees, so the protocol angles need correction or a nonstandard operator definition.

## BT1346 -- Claim-stratified master PDF

Updated:

```text
paper/w33_q4_claim_stratified_master.tex
```

Added:

```text
data/bt1346_claim_stratified_pdf_manifest.json
```

The paper was compiled locally with pdflatex into:

```text
w33_q4_claim_stratified_master_final.pdf
```

The PDF has 4 pages and was render-verified with pdftoppm/PIL.

The full workflow creation was blocked by the connector filter, so the manifest and regression tests record the build.

## Regression

Added:

```text
tests/test_bt1344_bt1346_canonical_matrix_paper.py
```
