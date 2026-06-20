# BT1399--BT1401 -- PDF Rebuild, Erasure Noise, Runtime Release Extension

## BT1399 -- Claim master PDF rebuild

Added:

```text
data/bt1399_claim_master_pdf_rebuild_manifest.json
```

The BT1398-patched claim-stratified master paper was compiled locally with two pdflatex passes and rendered for inspection.

```text
pages = 6
rendered pages inspected = 1, 4, 5, 6
```

The local artifacts are:

```text
w33_q4_claim_stratified_master_bt1399.pdf
w33_q4_claim_stratified_master_bt1399.tex
```

## BT1400 -- Qutrit erasure readout noise sensitivity

Added:

```text
tools/bt1400_qutrit_erasure_noise_sensitivity.py
data/bt1400_qutrit_erasure_noise_sensitivity.json
```

The parametric model uses:

```text
gamma = visibility * (1 - distinguishability) * exp(-sigma_phi^2)
```

Baseline:

```text
gamma = 0.92919
port0 = 0.95280
```

Conservative:

```text
gamma = 0.79298
port0 = 0.86199
```

Bad distinguishability and bad phase cases degrade or fail as expected.

## BT1401 -- Runtime release extension

Updated:

```text
tools/bt1389_run_runtime_frontier_release_lock.sh
```

Added:

```text
data/bt1401_runtime_release_lock_extension.json
```

The runtime release lock now protects BT1393--BT1400.

## Regression

Added:

```text
tests/test_bt1399_bt1401_pdf_noise_release.py
```
