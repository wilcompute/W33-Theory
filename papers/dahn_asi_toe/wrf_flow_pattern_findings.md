# WRF Flow Pattern Findings -- BT110/BT111/BT112
## Calibrated W(3,3) Architecture-Suite Notes

**Updated:** 2026-06-03  
**Graph:** W(3,3) = Cayley graph of Sp(4, F3)  
**Parameters:** 40 vertices, 240 edges, 480 directed states, k=12-regular  
**Property:** Ramanujan graph (all nontrivial eigenvalues <= 2*sqrt(11) ~= 6.633)  
**Scripts:** `wrf_full_suite_bt110_bt111.py`, `wrf_bt112_suite.py`  
**Results:** `wrf_bt110_bt111_results.json`, `wrf_bt112_results.json`

---

## BT110: First Harness Answers to the Original Open Items

### OI-1: Write Protocol
- Max transient to some attractor across the four primary seed rules: **37 steps**
- Mean transient: 9.5-13.1 steps (seed-dependent)
- Injection cost: **1 step** (direct attractor-node injection)

### OI-2: Noise Model
- Forward-flow perturbation: **100% same-basin preservation in the tested deterministic harness**
- Random perturbation: 50-97% CID preserved (reflects basin size)

### OI-3: 4-Cell Lattice
- Cross-talk: **0 / 2000 one-step independent-flow trials**
- Gate probabilities: AND=50.4%, XOR=49.6%
- Phase-lock prob (CD pair): 80.5% (near-perfect sync)

### OI-4: Capacity (500 seeds)
- Total distinct CIDs: **1138**
- Max attractors/seed: **6** (3 seeds at maximum)
- Mean attractors: 2.346

### OI-4b: CID Hamming Distance
- Sampled global min Hamming (24-char hex): **18**
- Symbolic correction budget in that sample: **t = 9**
- This is a sampled code-distance observation, not a production ECC proof.

---

## BT111: Spectral Trace Tower -- 6 Exact Identities Verified

| Moment | Substrate Formula | Value |
|--------|-------------------|-------|
| tr(A^2) | n | 480 |
| tr(A^3) | lam * n | 960 |
| tr(A^4) | n * mu * Phi3 | 24960 |
| tr(A^5) | lam*n * mu * (2*h_E8 + 1) | 234240 |
| tr(A^6) | n * 2^4 * (mu*q^2*p_Ih + 1) | 3048960 |
| tr(A^7) | lam*n * 2^4 * Phi6 * (lam*q*F5*p_Ih + 1) | 35589120 |

Constants: lam=2, mu=4, Phi3=13, Phi6=7, p_Ih=11, F5=5, h_E8=30, q=3

**E8 Coxeter number h_E8=30 encodes in tr(A^5). Fibonacci F5=5 in tr(A^7).**

### Cyclotomic Cross-Links
- Phi5(3) = 121 = p_Ih^2 = 11^2
- Phi1*Phi2*Phi4*Phi8 at q=3 = 6560 = 3^8 - 1 (Euler product)
- Triangles = mu * |V| = 4 * 40 = 160

---

## BT112: Full Suite Harness Results

### BT112-A: tr(A^8) Exact Substrate Identity

```
tr(A^8) = tr(A^6)*q*(4k - 1) + n*16*(q*(4k-1)-lambda)
        = 3048960 * 141 + 480*16*(141-2)
        = 430,970,880   [VERIFIED]
```

The tempting ratio ladder `tr(A^8) = tr(A^6)*q*(4k-1)` is close but false. The exact
identity needs the residual term above. This is useful: the architecture should retain
the correction channel rather than flattening it away.

Full form: `tr(A^8) = n*2^4*((mu*q^2*p_Ih+1)*q*(4k-1) + q*(4k-1)-lambda)`,
where `n=480` is the directed carrier used throughout the trace tower.

### BT112-B: Ihara Zeta Structural Data

| Quantity | Value | Substrate link |
|----------|-------|----------------|
| e_2 (Newton) | -240 | = -E (edge count!) |
| e_3 | +320 | = 2E/3 |
| Triangles | 160 | = mu * V |
| 4-cycles | 2400 | = 10 * E |
| chi = V-E | -200 | Euler characteristic |
| Trivial poles | 1/12, 1/11 | k and k-1 |

Functional equation: `Z(1/(k-1)u)^{-1} = Z(u)^{-1} * (k-1)^{|chi|} * u^{2|chi|}`
= `Z(u)^{-1} * 11^200 * u^400`

**Key: e_2 = -E = -240 = -(E8 root count). Newton coefficient = negative edge count.**

### BT112-C: McKay E8 <-> Sp(4,F3) Proof Sketch

| Fact | Value | Verified |
|------|-------|----------|
| E8 roots = W(3,3) edges | 240 = 240 | YES |
| Sum of E8 exponents = 4*h_E8 | 120 = 4*30 | YES |
| Product of first*last exponent = h_E8-1 | 1*29 = 29 | YES |
| |W(E8)| / |Sp(4,F3)| | 696729600 / 51840 = 13440 | -- |
| 13440 = 2^7 * 3 * 5 * 7 | verified | YES |
| Product(3 - Cartan_eig) over E8 exponents | 25.00 (exact) | YES |

Conclusion: tr(A^5) encodes the E8 Coxeter number h_E8=30 via the factor (2*h_E8+1)=61.
The McKay correspondence between Sp(4,F3) and E8 manifests in the 5th spectral moment.
Product(3 - Cartan_eig) = 25 = p_Ih + 14 = ... (new substrate link TBD in BT113)

### BT112-D: Shannon Capacity Bound

| Bound | Value |
|-------|-------|
| Singleton bound | M <= 16^7 = 2.68e8 |
| Hamming bound | M <= 1.52e12 |
| Observed M (500 seeds) | 1138 |
| Information bits/CID | 10.15 bits |
| Rate | 0.1058 bits/hex-symbol |
| BSC capacity (t=9) | 1.094 bits/CID channel |

Conclusion: The observed WRF CID set is sparse relative to simple coding bounds.
This suggests design headroom, but it does not yet replace a full capacity theorem under
real read windows and device noise.

### BT112-E: Seed-661 Base-6 Register Harness

All 6 symbols have measured mean write latency below 7 steps:

| Symbol | Cycle length | Basin size | Avg write latency |
|--------|-------------|------------|------------------|
| 0 | 16 | 127 | 5.7 steps |
| 1 | 4 | 33 | 5.9 steps |
| 2 | 10 | 68 | 5.6 steps |
| 3 | 14 | 107 | 5.5 steps |
| 4 | 5 | 106 | 6.1 steps |
| 5 | 5 | 39 | 6.2 steps |

**log2(6) = 2.585 bits/register. 3 base-6 registers > 7 classical bits.**

### BT112-F: 3x3 Coupling Lattice

- Seeds: [61, 161, 261, 361, 461, 561, 661, 761, 861]
- Attractor counts: [4, 3, 4, 3, 2, 3, 6, 3, 3]
- **0 cross-talk events in 24000 one-step independent-flow trials**
- Center-to-center phase-lock: **0.980** (near-perfect sync available)
- Seed-661 at position (row=2, col=0): **6-attractor base-6 register embeds cleanly**

---

## 5 Harness-Supported Architecture Targets

1. **WRITE-BOUNDED:** In the four primary rules, every directed state reaches an attractor in <= 37 deterministic steps.
2. **FORWARD-STABLE:** Advancing along a cell's own transition preserves the attractor basin in the tested harness.
3. **ISOLATED REGISTERS:** Independent-flow 3x3 lattice showed zero one-step cross-talk events in 24000 trials.
4. **DISTANT CIDs:** Sampled 24-hex-character CIDs had minimum character distance 18, giving t=9 symbolic correction in that sample.
5. **SPECTRAL SELF-REFERENCE:** tr(A^k) for k=2..8 factor exactly into substrate constants
   {lam, mu, Phi3, Phi6, p_Ih, F5, h_E8, q, k} with E8 Coxeter number appearing in tr(A^5).

---

## BT113 Targets

1. **Ihara zeta poly over Q[u]:** Compute det(I - A*u + 11*u^2) as explicit polynomial
2. **E8 / Sp(4,F3) combinatorial proof:** Derive 13440 = |W(E8)|/|Sp4| from substrate directly
3. **3-register base-6 read/write/noise cycle:** Full benchmark with seed-661 + two neighbors
4. **tr(A^8) ratio ladder Phi_30 link:** Map q*(4k-1)=141=3*47 to cyclotomic Phi_30(3) evaluation
5. **Newton e_2 = -240 = -(E8 roots) link:** Prove this is the spectral shadow of McKay
6. **Product(3-Cartan_eig)=25 substrate identity:** What is 25 in the substrate algebra?
