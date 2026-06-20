# BT1402 -- Photonic Manuscript Runtime-Frontier Handoff

BT1402 updates the manuscript layer after the BT1378--BT1401 runtime-frontier
batch.  The mathematical and executable frontier already exists; this packet
checks that the live writeups now expose it consistently.

## Contract

The post-BT1401 architecture has four explicit facts:

```text
1. The deterministic kernel is the 51840-window Clifford/Sp(4,3) runtime.
2. The reduced single-photon demonstrator has Bell-qutrit signatures
   V(I)=1, V(F3)=1/3, V(X)=0, V(Z)=0.
3. Route coherence is not visible after tracing out the Bell legs; it is
   recovered by a quantum-erasure readout with success probability 1/3 and
   l1 coherence 2.
4. The Hesse-SIC/T port is a concrete nine-outcome ABI, but the physical
   resource factory and global S3 MaxSAT optimum remain open gates.
```

The important honesty boundary is that this is not a new threshold claim.  The
BT1400 noise model is parametric, the Hesse-SIC/T factory is still not certified,
and the S3 gauge frontier remains witness-only at score 210 until a
solver-generated upper-bound certificate is imported.

## Verification

```bash
python tools/bt1402_photonic_manuscript_runtime_frontier.py
python tests/test_bt1402_photonic_manuscript_runtime_frontier.py
python -m py_compile tools/bt1402_photonic_manuscript_runtime_frontier.py tests/test_bt1402_photonic_manuscript_runtime_frontier.py
python -m json.tool data/bt1402_photonic_manuscript_runtime_frontier.json
```
