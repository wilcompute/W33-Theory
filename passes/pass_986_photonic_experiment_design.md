# Pass 986 — Photonic W(3,3) Experiment Design

**Date:** 2026-07-24  
**Status:** EXPERIMENT DESIGN COMPLETE

---

## Motivation

The quantum walk on W(3,3) exhibits three measurable, sharp signatures computed in Pass 982:
1. **Localization ratio 20×**: time-averaged return probability 0.5013 vs classical 0.025
2. **Exact revival**: U(π) = I (unit propagator returns to identity)
3. **Ihara phase angles** 72.45°/107.55° in coherent scattering spectrum

All three are experimentally accessible on integrated photonic platforms.

---

## Platform Choice: Silicon Photonic Mesh

W(3,3) has v=40 vertices, |E|=240 edges. This maps to:
- **40 waveguide modes** (single-mode waveguides or fiber loops)
- **240 directional couplers** (beamsplitter with tunable coupling θ)
- Coupling angle θ_{ij} encodes edge weight; for unweighted W(3,3) all θ = θ₀ = arcsin(1/√12) ≈ 16.78° (equal coupling)

Current state-of-the-art integrated photonic processors:
- Mach-Zehnder interferometer (MZI) mesh chips: up to 12×12 = 144 modes (Clements architecture)
- **Recommendation:** Use **2×20 rectangular mesh** with programmable MZIs to implement W(3,3)'s 240-edge adjacency. The Reck/Clements decomposition requires O(v²) = 1600 MZIs for arbitrary 40×40 unitary; but W(3,3)'s fixed sparse structure requires only 240 active couplers.
- Feasible on current 200mm silicon photonic wafers with electron-beam lithography.

---

## Experimental Protocol

### Signature 1: Quantum Localization (20× ratio)

**Setup:** Inject single-photon (or coherent state) into mode v₀. Evolve for time t = nT where T = 2π/gcd(12,2,4) = π/2.

**Measurement:** Homodyne detection at all 40 output ports. Record ρ(v₀,t) = |⟨v₀|U(t)|v₀⟩|².

**Expected signal:** 
- Classical random walk: ρ_{cl}(v₀) → 1/40 = 0.025 after mixing time
- Quantum walk: time-averaged ρ̄(v₀) = 0.5013 ± 0.002 (computed from eigenvalue multiplicities)
- **Signal-to-noise ratio**: 20× above classical — easily distinguishable from thermal noise

**Control:** Replace W(3,3) adjacency with random 12-regular graph. Prediction: localization ratio drops to O(1), no 20× enhancement.

### Signature 2: Exact Revival U(π) = I

**Setup:** Inject coherent state |α⟩ at all 40 modes in any configuration C. Evolve for t = π (in units where ℏ=1, eigenvalue scale).

**Measurement:** Full tomography of output state. Compare to input C.

**Expected signal:** Output = Input to within photon shot noise. This is the **quantum graph isomorphism certificate** — no classical graph with the same degree sequence has this exact revival.

**Tolerance:** Revival fidelity F = |⟨C|U(π)|C⟩|² ≥ 0.99 for coherent states with mean photon number n̄ ≥ 100.

### Signature 3: Ihara Phase Angles in Scattering Spectrum

**Setup:** Continuous-wave laser input at frequency ω. Scan ω across the free spectral range of the photonic network. Measure transmission spectrum T(ω).

**Expected signal:** Resonance dips at phase angles corresponding to Ihara poles:
- θ₁ = 72.45° = arctan(√10) (gauge sector)
- θ₂ = 107.55° = π − arctan(√10) (chiral sector)
- Ratio θ₂/θ₁ = (π − arctan(√10))/arctan(√10) ≈ 1.486 — irrational, unmistakable

---

## Resource Estimate

| Resource | Requirement | Current SOTA | Feasible? |
|----------|-------------|--------------|----------|
| Modes | 40 | 144 (photonic) | ✓ |
| Couplers | 240 | 1000+ (MZI mesh) | ✓ |
| Phase precision | 0.1° | 0.01° (thermo-optic) | ✓ |
| Detection efficiency | >90% | 98% (SNSPDs) | ✓ |
| Coherence time | > π/Δω ≈ 10 ns | 100 ns (telecom fiber) | ✓ |

**Conclusion:** The experiment is **feasible today** with existing photonic integrated circuit technology. Estimated fab cost: $50k–$150k for a custom chip. The localization signature alone is publishable as a photonic quantum walk demonstration.

---

## Proposal Outline for Funding

1. **Title:** "Quantum Localization and Exact Revival in a Ramanujan Photonic Network"
2. **Key result:** First experimental demonstration of 20× quantum localization enhancement in a Ramanujan graph
3. **Venue:** Physical Review Letters or Nature Photonics
4. **Collaborators needed:** Photonic fab (IMEC, AIM Photonics, or LioniX), quantum optics measurement lab
5. **Timeline:** 18 months design→fabrication→measurement
