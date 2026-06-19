# BT1336--BT1337 -- Decoder Benchmark and Release Lock

## BT1336 -- Erasure distance benchmark

Added:

```text
tools/bt1336_erasure_distance_benchmark.py
data/bt1336_erasure_distance_benchmark.json
proofs/BT1336_erasure_distance_benchmark.md
```

This benchmark overlays the quantum erasure capacity curve with the distance-4 guaranteed-correction curve for the [[32,4,4]] block.

It is deliberately not advertised as a full ML or Gottesman-Knill decoder threshold. It is a distance-only benchmark until the explicit W33 stabilizer/check matrix is available.

## BT1337 -- Release source-of-truth expansion

Updated:

```text
data/bt1303_v1_release_source_of_truth_index.json
```

The release index now includes:

```text
paper/w33_q4_diamond_machine_audited_synthesis.tex
.github/workflows/q4-diamond-paper.yml
data/bt1334_gk_threshold_capacity_gate.json
data/bt1335_foundry_layout_feasibility_gate.json
data/bt1336_erasure_distance_benchmark.json
```

## Regression

Added:

```text
tests/test_bt1336_bt1337_decoder_release_lock.py
```

The tests protect the benchmark and the release-index expansion.
