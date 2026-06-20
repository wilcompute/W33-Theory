# BT1384--BT1386 -- MaxSAT Export, Hesse-SIC/T ABI, and Paper Splice

## BT1384 -- Exact S3 gauge MaxSAT export

Added:

```text
tools/bt1384_export_s3_gauge_maxsat.py
data/bt1384_s3_gauge_maxsat_manifest.json
proofs/BT1384_s3_gauge_maxsat_export.md
```

The exporter emits a weighted partial MaxSAT WCNF instance for the BT1379 S3 gauge problem:

```text
variables = 780
hard clauses = 20086
soft clauses = 540
total clauses = 20626
BT1373 witness score = 210
```

## BT1385 -- Concrete Hesse-SIC/T port ABI

Added:

```text
tools/bt1385_hesse_sic_t_port_abi.py
data/bt1385_hesse_sic_t_port_abi.json
```

The concrete Hesse-SIC/T token is qutrit-dimensional and has nine SIC outcomes. It defines injection timing, measurement signature, feed-forward, acceptance, and four failure modes.

## BT1386 -- Claim-stratified paper splice and PDF rebuild

Updated:

```text
paper/w33_q4_claim_stratified_master.tex
tex/bt1380_post_1377_claim_table.tex
```

Added:

```text
data/bt1386_claim_master_pdf_manifest.json
```

The paper now directly inputs:

```text
tex/bt1380_post_1377_claim_table.tex
tex/bt1381_bt1383_runtime_frontier_insert.tex
```

and includes the Hesse-SIC/T Non-Clifford Port section.

The PDF was compiled locally with two pdflatex passes, rendered, and inspected. It is five pages. The BT1380 table was compacted to avoid horizontal clipping.

## Regression

Added:

```text
tests/test_bt1384_bt1386_maxsat_port_paper.py
```
