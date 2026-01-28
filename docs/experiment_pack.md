# Witting/W33 Experiment Pack

## 1. Objective
Deliver a **lab‑ready** experimental plan that tests two falsifiable signatures:

1. **State‑independent contextuality** via the 24‑basis KS inequality.
2. **Discrete Pancharatnam phase** via triangle loops (quantized at **±π/6, ±π/2**).

---

## 2. KS Inequality (24‑Basis)

- Noncontextual bound: **23 / 24**
- Quantum prediction: **24 / 24**

Docs:
- `docs/witting_24basis_inequality.md`
- `docs/witting_24basis_runsheet.md`
- `docs/witting_24basis_labscript.md`

Noise robustness:
- `docs/witting_24basis_noise_threshold.md`

---

## 3. State Preparation and Settings

**Unitary definitions:**
- `docs/witting_24basis_unitaries.json`

**Optical decompositions:**
- MZI schedule: `docs/witting_24basis_mzi_schedule.md`
- Waveplates (rad): `docs/witting_24basis_waveplates.md`
- Waveplates (deg): `docs/witting_24basis_waveplates_deg.md`

**Ray amplitudes/phases:**
- `docs/witting_ray_amplitude_phase.csv`

---

## 4. Pancharatnam Phase Test (π/6, π/2)

**Key signature:** phase quantization in **{±π/6, ±π/2}**.

Docs:
- Protocol: `docs/witting_pancharatnam_protocol.md`
- Examples: `docs/witting_pancharatnam_examples.md`
- Run‑sheet: `docs/witting_pancharatnam_runsheet.md`
- Noise robustness: `docs/witting_pancharatnam_noise_threshold.md`

---

## 5. Experimental Checklist

1. Calibrate phase reference across all interferometric measurements.
2. Verify basis orthonormality (unitary columns).
3. Run KS bases in order and compute score S.
4. Measure Pancharatnam triangles and verify π/6, π/2 phase clustering.

---

## 6. Expected Outcomes

- **KS violation:** S = 24 (noncontextual bound 23).
- **Pancharatnam phase:** Φ ∈ {±π/6, ±π/2} with robust clustering.

Any failure falsifies the Witting/W33 photonic realization.
