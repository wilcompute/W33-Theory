# BT1341--BT1343 -- Quotient, Falsifier, Claim-Stratified Master

## BT1341 -- Q4 gauge quotient [[32,4,4]]

Added:

```text
tools/bt1341_q4_gauge_quotient_3244.py
data/bt1341_q4_gauge_quotient_3244.json
proofs/BT1341_q4_gauge_quotient_3244.md
```

Result:

```text
n = 32
rank(H_X) = 15
rank(H_Z) = 13
k = 4
d_X = 4
d_Z = 4
```

The construction uses four global quotient/flux functionals on the 17-dimensional Q4 cycle space and takes the kernel as the Z-check space.

## BT1342 -- Hashimoto falsifier simulator

Added:

```text
tools/bt1342_hashimoto_falsifier_simulator.py
data/bt1342_hashimoto_falsifier_simulation.json
proofs/BT1342_hashimoto_falsifier_simulator.md
```

The simulator constructs W(3,3) from projective F3^4, verifies SRG(40,12,2,4), and generates a deterministic synthetic pass/fail packet for Hashimoto angles, flat-band localization, CSS proxy, and period-6 recurrence.

## BT1343 -- Claim-stratified master TeX

Added:

```text
paper/w33_q4_claim_stratified_master.tex
data/bt1343_claim_stratified_master_manifest.json
```

The merged paper uses the audited Q4 paper as the spine and imports the broader Q4 Diamond Machine synthesis under explicit claim labels:

```text
EXACT, CERT, STRUCT, SIM, ENG, SPEC
```

## Regression

Added:

```text
tests/test_bt1341_bt1343_quotient_falsifier_master.py
```

This protects the quotient certificate, falsifier simulator, and claim-stratified master paper.
