# BT1333--BT1335 -- Paper, Threshold Gate, and Layout Gate

## BT1333 -- Repo-native paper

Added:

```text
paper/w33_q4_diamond_machine_audited_synthesis.tex
.github/workflows/q4-diamond-paper.yml
```

The paper source is now repository-native and has a dedicated CI workflow that compiles it with `pdflatex` and uploads the PDF artifact.

## BT1334 -- Gottesman-Knill threshold capacity gate

Added:

```text
tools/bt1334_gk_threshold_capacity_gate.py
data/bt1334_gk_threshold_capacity_gate.json
proofs/BT1334_gottesman_knill_threshold_capacity_gate.md
```

Result: under independent photon loss treated as a quantum erasure channel, a Gottesman-Knill stabilizer decoder cannot push the threshold above 50 percent. The correct target is to improve toward 50 percent from below and compare against the 14.4 percent ML-loss baseline.

## BT1335 -- Foundry layout feasibility gate

Added:

```text
tools/bt1335_foundry_layout_feasibility_gate.py
data/bt1335_foundry_layout_feasibility_gate.json
proofs/BT1335_foundry_layout_feasibility_gate.md
```

Result: the 4320 base-channel claim is area-plausible on a 5mm by 5mm die under explicit chart-cell assumptions. The 70.8M concatenated-mode claim is not a single-die claim and requires hierarchy, time multiplexing, fiber/memory multiplexing, or multi-die architecture.

## Regression

Added:

```text
tests/test_bt1333_bt1335_paper_threshold_layout.py
```

The tests protect the repo-native paper/workflow, threshold capacity gate, and foundry feasibility gate.
