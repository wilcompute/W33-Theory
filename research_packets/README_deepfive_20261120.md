# 2026-11-20 deep-five independently executable research packet

**Purpose:** Reproduce the *constructive linear causal-switch witness* and four physical/operational consistency gates (optical, anomaly-index, calibration drift, and W33 Wilson coupling), plus a dimensional-scaling no-go.

**Primary research report:** [analysis/2026-11-20_deepfive_constructive_causal_witness_and_no_go.md](../analysis/2026-11-20_deepfive_constructive_causal_witness_and_no_go.md).

**Source archive:** [toe_20261120_deep_five_sources.tar.xz](toe_20261120_deep_five_sources.tar.xz).
SHA-256: `a1aa82a14aa88aa0cd4366c50f813b717352880937580ba35d776929f46c901e`.

The archive contains three **plain-text** files after extraction:

- `analysis/toe_20261120_causal_witness_constructive.py`
- `analysis/toe_20261120_five_independent_operational_gates.py`
- `tests/test_toe_20261120_deep_five.py`

### Replay against this repository

Extract at the repository root, preserving the contained paths:

```bash
tar -xJf research_packets/toe_20261120_deep_five_sources.tar.xz
python -m pip install numpy scipy networkx
python analysis/toe_20261120_causal_witness_constructive.py > /dev/null
python analysis/toe_20261120_five_independent_operational_gates.py > /dev/null
python -m unittest discover -s tests -p 'test_toe_20261120_deep_five.py' -v
python -m unittest discover -s tests -p 'test_toe_20261120_fivefront_plus_bridge.py' -v
```

**Tests:** 24 new focused test cases plus 16 existing prior five-front baseline cases = **40/40 passing** in the stated server Python environment.

**Generated certificates:** `data/toe_20261120_causal_witness_constructive.json` and `data/toe_20261120_five_operational_gates.json`. The new producer scripts recreate these deterministically. Each checks its own identity and numerical controls. A complete separately downloadable ZIP packet was also delivered in the same ChatGPT conversation.

**Scientific limits:** No physical photonic device was operated. The causal witness is for the ideal established quantum-switch process, with a weak >99.2% visibility requirement, and its Pauli expansion is not automatically an implementable laboratory measurement. No charged singular-G2 Dirac index, dynamical generation count, anomaly-inflow completion, or beyond-standard-QFT parameter-free observable was derived. The Wilson coupling calculation is a finite-Z3 gauge-theory underdetermination example, not a full dynamical W33 theory.

**Source orientation:** existing `analysis/toe_20261120_fivefront_plus_bridge.py` supplies the known 9-mode Weyl gates and 18-mode compiled switch. The new modules add noncentral controls, a mathematical causal witness, an anomaly-index polynomial, a calibrated drift falsifier, and an exact eight-cycle Wilson coupling model.