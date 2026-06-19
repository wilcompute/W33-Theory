# BT1301 -- Release Gate Layer

BT1301 protects the new v1 release gate layer.

Committed files in this layer:

```text
data/bt1298_v1_release_gate_matrix.json
tools/bt1299_run_v1_release_gates.sh
tools/bt1300_verify_paper_build_handshake.py
tests/test_bt1298_bt1300_release_gates.py
```

The gate matrix and shell runner cover the strict certificate, candidate batch, unified release verifier, readiness badge, paper-build handshake, and release pytest subset.

The paper handshake checks the paper workflow, the preprint path, and the PDF artifact path.
