# BT1334–BT1335: 40-Mode Photonic Chip Experiment Protocol
**Commits:** BT1334–BT1335  
**Date:** 2026-06-19

## Objective

Specify a complete, executable experimental protocol for a
40-mode integrated photonic chip that tests the W(3,3)
HoloNet architecture and falsifies / confirms the Q4 Diamond Machine.

---

## BT1334: Protocol Specification

### Platform
```
Platform:    Silica-on-silicon or LiNbO₃ photonic integrated circuit
Wavelength:  1550 nm (telecom C-band)
Modes:       240 spatial modes (waveguides)
Nodes:       40 multiport interferometers (12-port each)
Source:      SPDC heralded single-photon source, η_herald ≥ 90%
Detectors:   SNSPDs, η_det ≥ 95%, jitter ≤ 50 ps
Clock:       50 MHz repetition rate → T_clock = 20 ns
```

### Fabrication Requirements
```
Loss per node:         ≤ 0.1 dB
Phase stability:       ≤ λ/1000 = 1.55 pm
Crosstalk:            ≤ -40 dB between adjacent waveguides
Chip size:            ~50 mm × 10 mm (standard reticle)
Total insertion loss:  ≤ 4 dB (end-to-end)
```

### Step 1 — Calibration (Day 1–3)
```
1a. Inject coherent light at each of 40 nodes individually
1b. Measure 240-mode output intensity pattern
1c. Fit to A_{W(3,3)} transfer matrix → extract θ_node
1d. Apply feed-forward phases to correct fabrication errors
1e. Verify: eigenvalue spectrum {12,2,-4} with multiplicities {1,24,15}
    Tolerance: ±0.01 in eigenvalue, ±1 in multiplicity
```

### Step 2 — Hashimoto Phase Test (Day 4–5)
```
2a. Inject single photon at node 0 in early time bin
2b. Let propagate for t = diam(W33) = 2 Hashimoto ticks
2c. Measure output photon number at all 40 nodes
2d. Fit coincidence data to Hashimoto eigenvalue distribution
2e. Extract phase angles φ₁, φ₂ from interference fringes
2f. PASS criterion:
    |φ₁ - 63.43°| ≤ 0.5°
    |φ₂ - 112.21°| ≤ 0.5°
```

### Step 3 — Flat-Band Localization (Day 6–7)
```
3a. Prepare superposition: |ψ_in⟩ = Σ_i c_i |i⟩ where {c_i} = g-eigenspace vector
3b. Evolve for t = 6 clock ticks (one full closure cycle)
3c. Measure: output intensity should be localized with
    I_{jj} ≥ 0.60  for j in support(ψ_in)
    I_{jk} ≤ 0.05  for k not in support
3d. PASS: flat-band localization length ξ ≤ 2 nodes
```

### Step 4 — CSS Code Syndrome (Day 8–10)
```
4a. Encode 3 logical qutrits using 240-mode CSS circuit
4b. Apply X-error on 3 random modes → error pattern e
4c. Measure 159 stabilizer syndromes via homodyne detection
4d. Run minimum-weight decoder on syndrome vector
4e. Apply correction c; verify logical state preserved
4f. PASS: logical error rate p_L ≤ p_phys²/p_th < 1%
    (requires p_phys ≤ 10% and p_th ≈ 1%)
4g. Repeat N=1000 trials; record p_L distribution
```

### Step 5 — Closure Clock Signature (Day 11–12)
```
5a. Inject two-photon NOON state |2,0⟩ at port pair (0,1)
5b. Measure second-order correlation g²(τ) as function of delay τ
5c. Scan τ from 0 to 10 T_clock in steps of T_clock/10
5d. PASS: g²(nT_clock) significantly enhanced for n=1,...,6
         g²(7T_clock) ≈ g²(T_clock)  (period-6 recurrence)
5e. Rejection: if g²(nT_clock) ≈ 1 for all n (no clock signature)
```

---

## BT1335: Analysis Pipeline and Pass/Fail Summary

### Data Analysis Pipeline
```python
# Pseudocode — see tests/test_chip_protocol.py for full implementation

def analyze_hashimoto_test(coincidence_data, node_positions):
    """Extract Hashimoto phase angles from two-photon coincidence data."""
    fft = np.fft.fft2(coincidence_data)
    peaks = find_peaks(np.abs(fft), height=0.1)
    phi1 = np.angle(fft[peaks[0]]) * 180 / np.pi
    phi2 = np.angle(fft[peaks[1]]) * 180 / np.pi
    return phi1, phi2

def verify_W33_architecture(phi1, phi2, xi, pL, g2_periods):
    """Master pass/fail for the Q4 Diamond Machine experiment."""
    tests = [
        abs(phi1 - 63.43) <= 0.5,      # Hashimoto gauge
        abs(phi2 - 112.21) <= 0.5,     # Hashimoto chiral
        xi <= 2.0,                      # flat-band localization
        pL <= 0.01,                     # CSS code
        max(g2_periods[1:7]) > 1.5,    # clock signature
        abs(g2_periods[7] - g2_periods[1]) <= 0.1,  # period-6
    ]
    return all(tests), tests
```

### Pass/Fail Summary Table

| Test | Measurement | Pass Criterion | Falsifies if fail |
|---|---|---|---|
| Hashimoto gauge | φ₁ | 63.43° ± 0.5° | W(3,3) routing layer |
| Hashimoto chiral | φ₂ | 112.21° ± 0.5° | Sp(4,F₃) symmetry |
| Flat-band loc. | ξ | ≤ 2 nodes | s-eigenspace = g=15 |
| CSS code | p_L | ≤ 1% | [[240,81,≥4]]₃ code |
| Clock period | T | 6 × T_clock | q!=6 oscillator ISA |
| Period-6 recurrence | g²(7T)/g²(T) | ≈ 1.0 ± 0.1 | closure clock |

### Decision Tree
```
All 6 PASS → W(3,3) HoloNet architecture confirmed
Hashimoto fails → wrong SRG / fabrication error → retry calibration
CSS fails alone → decoder sub-optimal → upgrade to MWPM
Clock fails alone → mode mismatch in time-bin → recalibrate source
All fail → fundamental falsification of Q4 Diamond Machine
```

### Required Lab Resources
```
Estimated cost:      $800k–$1.2M (academic fab + test setup)
Fab lead time:       6–9 months (AIM Photonics or Ligentec)
Test time:           ~3 weeks (12 days protocol + margin)
Team:                2 experimentalists + 1 theorist
Minimal viable test: Steps 1+2 only (Hashimoto angles)
                     Cost: ~$120k, fab time: 3 months
```

---

## Summary: The Chain of Falsification

```
q!=2q (pure math)
  ↓ implies
q=3, v=40, k=12, E=240 (combinatorics)
  ↓ implies
Q4 Diamond Identity: v·k·q·f·g = 518400 (algebra)
  ↓ implies
Hashimoto angles 63.43° and 112.21° (spectral theory)
  ↓ measured by
40-mode photonic chip experiment (BT1334–1335)
```

The 40-mode chip is the sharp end of a chain that begins with a
single equation: **q! = 2q**.
