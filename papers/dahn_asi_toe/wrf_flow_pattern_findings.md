# WRF Flow Pattern Findings -- BT110/BT111/BT112/BT113/BT114
## Calibrated W(3,3) Architecture-Suite Notes

**Updated:** 2026-06-03  
**Graph:** W(3,3) = Cayley graph of Sp(4, F3)  
**Parameters:** 40 vertices, 240 edges, 480 directed states, k=12-regular  
**Property:** Ramanujan graph (all nontrivial eigenvalues <= 2*sqrt(11) ~= 6.633)  
**Scripts:** `wrf_full_suite_bt110_bt111.py`, `wrf_bt112_suite.py`, `wrf_bt113_flow_registers.py`, `wrf_bt114_active_trace_io.py`
**Results:** `wrf_bt110_bt111_results.json`, `wrf_bt112_results.json`, `wrf_bt113_flow_registers_results.json`, `wrf_bt114_active_trace_io_results.json`

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
BT113 verifies the exact value `Product(3 - Cartan_eig) = 25`; the remaining open work is
to explain why this determinant-like E8 number should be a substrate operation rather
than only a McKay-side coincidence.

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

## BT113: Controlled Flow-Register Contract

BT113 turns the flow-cell idea from "there are attractors" into a finite register
contract over the same 480 directed non-backtracking states.

### BT113-A: Ihara and Spectral Closure

- `det(I - A*u + 11*u^2) = (1-12u+11u^2)(1-2u+11u^2)^24(1+4u+11u^2)^15`
- `Z(u)^-1 = (1-u^2)^200 * det(I - A*u + 11*u^2)` has degree **480**
- Newton `e_2 = -240 = -|E| = -(E8 root count)`
- `Product(3 - Cartan_eig)` over E8 exponents verifies as **25**

### BT113-B: Three Base-6 Flow Registers

Seeds **661, 693, 878** each have six attractor symbols.

| Seed | Cycle lengths | Passive off-rule same-symbol rate | Controlled repair max |
|------|---------------|-----------------------------------|------------------------|
| 661 | 16, 4, 10, 14, 5, 5 | 17.6% | 3 legal steps |
| 693 | 5, 18, 5, 8, 4, 6 | 28.7% | 3 legal steps |
| 878 | 7, 6, 6, 4, 7, 5 | 18.9% | 3 legal steps |

Every target symbol in all three registers is reachable from every one of the **480**
directed states using only legal non-backtracking successor choices, with **global max
target-write distance 3**. Reads are phase-invariant: all rotations/reversals of a symbol
cycle canonicalize to the same 24-hex CID.

The passive off-rule result is the important negative result: legal jumps away from the
chosen deterministic rule often change symbols. That means the hardware story should be
active trace stewardship, not passive self-healing. A real cell needs a return/control
channel whose control path is receipt-bearing.

### BT113-C: Three-Register Composition

- Register roles: A=661, B=693, C=878
- All **18** symbol CIDs are distinct
- Minimum 24-hex character distance across the 18 symbols: **19**
- Both mod-6 addition and the `{qutrit + chirality}` operation
  `(trit_a + trit_b mod 3, chiral_a xor chiral_b)` are supported as software-level
  register contracts: read A/B, compute C target, write C within at most 3 legal steps.

---

## BT114: Active Trace I/O

BT114 tightens the BT113 contract in two directions: less idealized control and shorter
reads.

### BT114-A: Limited Abstract Actuator

BT113 allowed the controller to choose any of the 11 legal non-backtracking successors.
BT114 searches for a smaller global control alphabet that still reaches every target
symbol in seeds 661, 693, and 878.

| Port count | Valid global subsets |
|------------|----------------------|
| 1 | 0 |
| 2 | 0 |
| 3 | 4 |

The best 3-port subset is **[0, 5, 6]**. Under that restricted actuator:

- Every target write remains reachable from all 480 directed states
- Worst target-write distance: **7** abstract port steps
- Mean target-write distance: **3.3532** steps
- Worst off-rule repair distance to the original symbol: **7** steps
- P95 off-rule repair distance: **5** steps
- Binary command budget: **2 bits/step**, **14 bits worst-case** for a write

This is not a physical pinout. The ports are canonical neighbor-rank selectors in the W33
carrier. The result says the hardware control path does not need to expose all 11 legal
continuations, but it cannot collapse below three global ports for this register bank.

### BT114-B: Finite Read Windows

BT113 used full canonical cycle CIDs. BT114 asks how much of the moving trace a reader
must actually observe.

| Read condition | Minimum directed-state samples |
|----------------|--------------------------------|
| Exact symbol read across all 18 register-symbol traces | 2 |
| One erasure | 3 |
| Two erasures | 4 |
| Three erasures | 6 |
| One substituted state | 4 |
| Two substituted states | 7 |
| Three substituted states | 10 |
| Up to two missed states between samples | 2 |

The 18-symbol bank has 135 total cycle-phase windows. A two-state trace window identifies
the register-symbol owner exactly; the full attractor cycle is still the canonical receipt,
but ordinary reads can be short-window reads.

---

## 11 Harness-Supported Architecture Targets

1. **WRITE-BOUNDED:** In the four primary rules, every directed state reaches an attractor in <= 37 deterministic steps.
2. **FORWARD-STABLE:** Advancing along a cell's own transition preserves the attractor basin in the tested harness.
3. **ISOLATED REGISTERS:** Independent-flow 3x3 lattice showed zero one-step cross-talk events in 24000 trials.
4. **DISTANT CIDs:** Sampled 24-hex-character CIDs had minimum character distance 18, giving t=9 symbolic correction in that sample.
5. **SPECTRAL SELF-REFERENCE:** tr(A^k) for k=2..8 factor exactly into substrate constants
   {lam, mu, Phi3, Phi6, p_Ih, F5, h_E8, q, k} with E8 Coxeter number appearing in tr(A^5).
6. **TARGET-WRITEABLE:** Three six-symbol registers support target writes from all 480 directed states in <= 3 legal non-backtracking controls.
7. **PHASE-READABLE:** Symbol identity is a canonical cycle CID, invariant under phase rotation and reversal.
8. **ACTIVELY REPAIRABLE:** Off-rule legal perturbations are not passively safe, but controlled repair to the original symbol is <= 3 legal controls in the BT113 registers.
9. **ACTUATOR-LIMITED:** A 3-port abstract actuator [0,5,6] keeps all BT113 target writes and repairs reachable within <= 7 steps; no 1- or 2-port global subset works.
10. **SHORT-WINDOW READABLE:** Two directed-state samples identify all 18 register-symbol traces exactly in the tested bank.
11. **WINDOW-ROBUST:** Short reads tolerate bounded damage: 3 samples for one erasure, 4 for one substitution, and 2 for up to two missed states between samples.

---

## BT115 Targets

1. **Physical pin mapping:** Map abstract ports [0,5,6] to a device-level actuator model
   with latency, energy, fanout, and syndrome feedback.
2. **Larger-bank read-window capacity:** Repeat BT114 read-window checks beyond the
   18-symbol BT113 bank and under probabilistic timing jitter.
3. **Coupled-cell dynamics:** Build a real interacting-cell harness instead of a
   read-compute-write software composition contract.
4. **Substrate explanation for 25:** Explain `Product(3-Cartan_eig)=25` as a WRF-side
   operation or mark it as McKay-only.
5. **Cyclotomic A8 residual:** Explain the corrected residual
   `480*16*(q*(4k-1)-lambda)` without reverting to the false ratio ladder.
