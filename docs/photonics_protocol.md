# Witting/W33 Photonics Protocol

## 1. Objective
This protocol tests two **falsifiable signatures** of the Witting/W33 structure:

1. **State‑independent contextuality** via the 24‑basis KS inequality (bound 23 vs quantum 24).
2. **Discrete Pancharatnam phase** via Berry‑phase loops on explicit Witting‑ray triangles (quantized at **±π/6, ±π/2**).

## 2. KS Inequality (24‑Basis Subset)

- **Noncontextual bound:** 23 / 24
- **Quantum prediction:** 24 / 24 (state‑independent)

Docs:
- `docs/witting_24basis_inequality.md`
- `docs/witting_24basis_runsheet.md`

**Noise threshold (depolarizing):**
- Visibility **v ≥ 0.944444** (noise p ≤ 0.055556)
- `docs/witting_24basis_noise_threshold.md`

## 3. State Preparation

Two equivalent paths:

**(A) Direct unitary preparation**
- `docs/witting_24basis_unitaries.json`

**(B) Optical decomposition**
- MZI schedule: `docs/witting_24basis_mzi_schedule.md`
- Waveplates (rad): `docs/witting_24basis_waveplates.md`
- Waveplates (deg): `docs/witting_24basis_waveplates_deg.md`

## 4. KS Measurement Run‑Sheet

Use the basis order and ray definitions in:
- `docs/witting_24basis_runsheet.md`

Each basis uses four orthogonal rays. The score S is the number of bases
with exactly one designated outcome.

## 5. Pancharatnam Phase Test (π/6, π/2)

**Signature:** phases clustered at **±π/6** and **±π/2**.

- Example triangles: `docs/witting_pancharatnam_examples.md`
- Full run‑sheet: `docs/witting_pancharatnam_runsheet.md`
- Measurement protocol: `docs/witting_pancharatnam_protocol.md`

## 6. Implementation Checklist

- Calibrate phase reference across all interferometric measurements.
- Verify orthonormality of each basis (unitary columns).
- Collect counts for all 24 bases → compute KS score.
- Measure triangle phases for the π/6, π/2 signature.

## 7. Summary of Expected Outcomes

- KS violation: **S = 24**, bound **S ≤ 23**.
- Pancharatnam phase quantization: **Φ ∈ {±π/6, ±π/2}**.

If either fails, the Witting/W33 photonic realization is falsified.
