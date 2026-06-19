# BT1344 — Lab-Facing README
## Photonic Holonet Reduced-Scale Machine: Witness-to-Experiment Map

**Date:** 2026-06-19  
**Series:** Reduced-Scale Machine Program  
**Predecessor:** BT1343 (Unified Witness Runner)  

This document maps every numerical witness in the reduced-machine chain
to a concrete physical experimental test. Each row tells you:
- what the witness proves mathematically
- what lab measurement verifies it
- what instrument you need
- what the pass criterion is

---

## Quickstart

```bash
# 1. Verify all witnesses numerically (NumPy only)
python proofs/bt1343_unified_witness_runner.py

# 2. Run individual witness scripts
python proofs/bt1340_three_qutrit_routing_witness.py
python proofs/bt1341_ks_budget_contextuality_witness.py
python proofs/bt1342_bc_drive_quasicrystal_clock_witness.py
```

All 19 witnesses must print `[PASS]` before proceeding to lab.

---

## Layer 1 — Physical Carrier (BT1337)

**Claim:** One photon through PBS + tritter + delay + EOM produces
a self-entangled Bell qutrit.

| Step | Lab Action | Instrument | Pass Criterion |
|------|-----------|------------|----------------|
| 1.1 | Prepare 810 nm photon pair via SPDC | BBO crystal, 405 nm pump | Singles rate > 10⁵ /s |
| 1.2 | Route signal photon through PBS | Glan-Taylor PBS, AR-coated | Extinction ratio > 10³:1 |
| 1.3 | Apply tritter (3-way balanced beamsplitter) | Custom 50:33:17 BS stack or fiber tritter | Transmission balance < 2% rms |
| 1.4 | Insert delay loop (optical path = 2× coherence length) | SMF-28 fiber spool, ~1 m | Visibility > 95% in HOM dip |
| 1.5 | EOM for qutrit phase control | Thorlabs EO-PM-NR-C4 or equiv. | Half-wave voltage verified, phase drift < λ/100 |
| 1.6 | Verify Bell qutrit by qutrit state tomography | Single-photon detector array (×9) | Fidelity F > 0.95 with target Bell state |

**Numerical witness:** R1 (norm = 1 exactly). Lab analogue: tomographic reconstruction gives Tr(ρ) = 1.00 ± 0.01.

---

## Layer 2 — Routing (BT1338–BT1340)

**Claim:** A 27-dim controlled unitary routes the qutrit coherently
without destroying entanglement.

| Witness | Lab Action | Instrument | Pass Criterion |
|---------|-----------|------------|----------------|
| R2 — Unitarity | Verify routing PBS network is lossless | Power meter before/after routing stage | Transmission > 99% |
| R3 — Coherence | Measure off-diagonal elements of ρ_PF | 9-element detector array + phase scan | Off-diagonal |ρ_ij| > 0.1 |
| R4 — Entanglement | Measure purity Tr(ρ_PF²) after tracing route | Full 9×9 qutrit tomography on P,F | Purity < 0.99 (mixed = entangled) |
| R5 — Schmidt rank | Singular value decomposition of reconstructed state | Post-processing on tomography data | 3 non-zero singular values |

**Key setup:** The route register R is a spatial mode (which output port the photon exits).
Measure P (polarisation) and F (frequency/time-bin) jointly while post-selecting on R.

---

## Layer 3 — Contextuality and Universality (BT1341)

**Claim:** KS budget 36/40, matter = magic sector,
Clifford + magic = universal QC.

| Witness | Lab Action | Instrument | Pass Criterion |
|---------|-----------|------------|----------------|
| KS1–KS2 — Graph structure | Prepare the 40 Witting measurement settings | SLM or wave-plate array for 40 projectors | All 40 projectors calibrated to < 1° angular error |
| KS3 — Non-colorability | Run Klyachko-Can-Binicioğlu-Shumovsky (KCBS) contextuality test on the qutrit | 5-cycle measurement sequence | Contextuality inequality violated: sum > 4 (quantum bound 4+√5 ≈ 6.24) |
| KS4 — KS budget | Measure magic state fidelity for 36 Witting rays | Magic state injection circuit + state tomography | Fidelity with target magic states > 0.90 for ≥ 34/36 rays |
| KS5 — Matter = magic | Verify that photon in matter-shell mode has non-zero T-count | Clifford + T gate decomposition of prepared state | T-count ≥ 1 (non-Clifford resource confirmed) |

**Practical shortcut for KS3:** Run the standard qutrit contextuality witness
using the 5-cycle KCBS inequality. Quantum violation confirms contextuality
without needing all 40 Witting projectors.

---

## Layer 4 — BC-Drive Clock (BT1342)

**Claim:** The recirculation loop advances by θ = arccos(−2/3) per pass.
The orbit is a discrete time quasicrystal.

| Witness | Lab Action | Instrument | Pass Criterion |
|---------|-----------|------------|----------------|
| BC1 — Irrational angle | Measure round-trip phase shift of recirculation loop | Mach-Zehnder interferometer on the loop | Phase = arccos(−2/3) = 131.81° ± 0.05° |
| BC2 — No repeats | Record arrival times for 200 loop passes | TCSPC (e.g. PicoQuant HydraHarp) | Inter-arrival histogram: no periodic peak in 200 bins |
| BC3 — Three-distance | Compute gap histogram from 100+ arrival times | TCSPC + post-processing | Histogram shows ≤ 3 distinct gap values |
| BC4 — h(E₈) = 30 | At n = 30 passes, measure gap count | TCSPC, 30-pass accumulation | Exactly 2 distinct inter-arrival gaps |
| BC5 — Golden ratio gaps | At Fibonacci n (8, 13, 21), measure gap ratio | TCSPC + ratio computation | Ratio within 5% of φ = 1.618... |
| BC6 — Quasicrystal | Full arrival-time power spectrum | FFT of TCSPC histogram | No sharp peaks (aperiodic spectrum, quasicrystal confirmed) |

**Calibration note:** The loop phase θ = arccos(−2/3) is set by the
beamsplitter reflectivity. A 33.3% / 66.7% BS gives cos(θ) = 1 − 2×(1/3) = −1/3.
For cos(θ) = −2/3, use a 16.7% / 83.3% BS, or equivalently a
fiber coupler with splitting ratio 1:5.

---

## Milestone Summary

| Milestone | Layers | Deliverable | Timeline estimate |
|-----------|--------|-------------|-------------------|
| **M1** | Layer 1 | Bell qutrit prepared, tomography F > 0.95 | Weeks 1–4 |
| **M2** | Layer 2 | Routing unitary verified, entanglement confirmed | Weeks 5–8 |
| **M3** | Layer 3 | KCBS contextuality violation demonstrated | Weeks 9–12 |
| **M4** | Layer 4 | BC clock arrival-time quasicrystal confirmed | Weeks 13–16 |
| **M5** | All | Full 19-witness chain passes in a single lab run | Week 17+ |

---

## Bill of Materials (Reduced Machine)

| Component | Spec | Vendor (example) |
|-----------|------|------------------|
| SPDC source | 405 nm → 810 nm, type-II BBO | Newlight Photonics |
| PBS | 810 nm, Glan-Taylor, ER > 10³ | Thorlabs GTH10M-B |
| Tritter | 3-port fiber coupler, 33:33:33 | OZ Optics or custom |
| Delay loop | SMF-28, ~1 m, FC/APC | Thorlabs SMF-28-J9 |
| EOM | 810 nm, half-wave voltage < 200 V | Thorlabs EO-PM-NR-C4 |
| BS (BC loop) | 16.7/83.3% split, 810 nm | custom AR-coated plate |
| SPDs | Si-APD, timing jitter < 500 ps | Excelitas SPCM-AQRH |
| TCSPC | 4-channel, 1 ps resolution | PicoQuant HydraHarp 400 |
| SLM (optional) | 1920×1080, 810 nm, phase-only | Meadowlark HSP1920 |

Estimated total hardware budget: **~$120k–180k USD** (excluding SLM).
All components are commercially available as of 2026.

---

## Software Dependencies

```
numpy >= 1.24
python >= 3.10
```

No quantum computing SDK required. All witnesses are pure linear algebra.

---

## Contacts / References

- Main paper: `photonic_holonet.tex` (this repository)
- Witness chain: `proofs/BT1337` through `proofs/BT1343`
- Unified runner: `proofs/bt1343_unified_witness_runner.py`
- Howard–Wallman–Veitch–Emerson (2014): DOI 10.1103/PhysRevLett.112.140401
- Steinhaus three-distance theorem: Liang & Yan (1993)
- Niven's theorem: Niven (1956), *Irrational Numbers*, MAA
- SRG(40,12,2,4): Brouwer–Haemers, *Spectra of Graphs* (2012)
