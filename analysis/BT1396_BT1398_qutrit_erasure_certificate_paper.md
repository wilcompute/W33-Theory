# BT1396--BT1398 -- Qutrit Erasure Readout, Example Certificate, Paper Patch

## BT1396 -- Qutrit quantum-erasure readout

Added:

```text
tools/bt1396_qutrit_quantum_erasure_readout.py
data/bt1396_qutrit_quantum_erasure_readout.json
```

The route register is maximally mixed if the Bell legs are discarded, but a Bell-branch eraser measurement onto

```text
(|Omega> + |Z Omega> + |X Omega>)/sqrt(3)
```

restores a coherent route qutrit:

```text
success probability = 1/3
l1 coherence = 2
single route-interferometer output port
```

## BT1397 -- Example MaxSAT optimality certificate pathway

Added:

```text
examples/bt1397_example_s3_maxsat_optimality_certificate.json
tools/bt1397_verify_example_optimality_certificate.py
data/bt1397_example_optimality_certificate_verification.json
```

The example drives the BT1395 verifier into the `optimal_certified` path but is explicitly marked synthetic. Project status remains:

```text
not_solver_certified
```

## BT1398 -- Claim master patch

Updated:

```text
paper/w33_q4_claim_stratified_master.tex
```

Added:

```text
data/bt1398_claim_master_patch_manifest.json
```

The paper now includes:

```text
BT1393 ladder chronology correction
BT1394 reduced qutrit demonstrator
BT1396 quantum-erasure readout
BT1395/BT1397 MaxSAT certificate pathway and boundary
```

## Regression

Added:

```text
tests/test_bt1396_bt1398_erasure_certificate_paper.py
```
