# BT1236 -- Clifford Word-Metric Paper Integration Manifest

## What landed

BT1236 adds a paper-ready insert:

```text
analysis/BT1236_minimal_clifford_tomography_insert.tex
```

and an idempotent integrator:

```text
tools/integrate_bt1236_insert.py
```

The integrator copies the insert to:

```text
paper/sections/sec_bt1236_minimal_clifford_word_metric.tex
```

and inserts:

```tex
\input{sections/sec_bt1236_minimal_clifford_word_metric}
```

into `paper/w33_preprint.tex` exactly once.

## Section content

The section records:

\[
|Sp(4,3)|=51840,
\]

BT1231's exact projective-transvection minimality theorem:

\[
3^{40},\qquad 9^{240}+24^{540},\qquad 24^{360}+27^{160}+72^{2160}+648^{7200},
\]

and BT1233's word-metric fingerprint:

\[
\operatorname{diam}=14,
\]

\[
1,8,36,126,363,916,2052,4096,7396,12170,16916,7247,476,36,1.
\]

## Run command

```bash
python tools/integrate_bt1236_insert.py
```

## Boundary

The direct `paper/sections` write path was blocked by the connector, so the repo follows the established safe pattern: paper insert plus narrow idempotent integration helper.
