# Pass 12715: an explicit SO(10)-invariant superpotential realises the pseudo-Goldstone Q + U (30 zero modes, 18 uneaten), with a "Goldstone quality" requirement that SO(10)-violating operators of dimension ≤ 10 be absent; hybrid and B′ separate at 2.3–6.5σ in the (M_VL, y′) plane; a signed-digit ternary multiplier needs 6 carry-free levels vs 8 + CPA for binary; ternary networks win below 0.073 pJ/bit of memory energy

Claude track. **Not a theory of everything.**
- Script: `explore_pass12715_round.py` (≈1 min).
- Certificate: `data/explore_pass12715_round.json`.
- Tests: `tests/test_toe_pass12715.py`, 4 tests passing.

## (1) An explicit superpotential for the pseudo-Goldstone Q + U
- **Model:** W = (m/2) tr Σ² + (λ/4M) tr Σ⁴ for a 45 (Σ). This is the generic SO(10)-invariant superpotential to quartic order, with only SU(5) gauged.
- **The vacuum exists.** The B−L vacuum Σ₀ = a·T_BL with a² = mM/λ solves F = 0 exactly; the eigenvalues of Σ₀ lie in {0, ±ia}.
- **Hessian of W on the 45 complex directions:**
  - **30 zero modes**, matching the 30 broken generators;
  - all other masses are 2m or 4m.
- **Zero modes by hypercharge:**
  - |Y| = 5/6: 12 states. This is the (3,2)₋₅/₆ pair, which the SU(5) gauge multiplets eat.
  - |Y| = 1/6: 12 states.
  - |Y| = 2/3: 6 states.
  - **So 18 chiral multiplets remain: Q + Q̄ + U + Ū.**
- **Explicit breaking:** an SU(5)-only perturbation of size ε lifts the would-be Goldstones linearly in ε (median 4.2ε·m, checked over three decades of ε).
- **Goldstone quality.**
  - **Requirement:** an SO(10)-violating operator Σⁿ/M_Pl^{n−3} gives the Goldstones m ~ a(a/M_Pl)^{n−3}, with a ≈ M_GUT. Keeping m ≤ 1.74 TeV requires **all such operators with n ≤ 10 to be absent** (n = 11 gives 265 GeV).
  - **Same structure as the axion quality problem.** The accidental SO(10) must be protected by a discrete or gauge symmetry that forbids violation up to dimension 10.
  - **Where the TeV mass then comes from:** the fermion masses come from SUSY breaking, ≈ M_SS²/M_GUT (Pass 12714).

## (2) E₆ (partial)
- **What a global E₆ would give:** under SO(10) × U(1), 78 = 45 + 16 + 16̄ + 1. A global E₆ broken to SO(10) × U(1) would add 16 + 16̄ Goldstones, which contain e^c, L, d^c and ν^c.
- **Consequence:** the clean Q + U result needs the accidental symmetry to be **SO(10) acting on a 45**, not E₆. If the hybrid's gauge E₆ is broken at the GUT scale by other fields, the 45 can be an E₆-singlet sector's field with its own accidental SO(10). The embedding is open.

## (3) Hybrid vs B′ in the (M_VL, y′) plane
- **Hybrid:** pseudo-Goldstone, with M_SS = √(M_VL·M_GUT/c) and c ∈ [0.3, 3].
- **B′:** flat R ∈ [0.009, 0.2] μm, including the mediator's gauge shift.

| M_VL | hybrid y′ | B′ y′ | band gap | separation (σ_meas = 0.005 / 0.002, ⊕ 0.0036 parametric) |
|---|---|---|---|---|
| 1.74 TeV | 0.465–0.480 | 0.494–0.510 | +0.014 | 2.3 / 3.4σ |
| 3.0 TeV | 0.445–0.462 | 0.481–0.499 | +0.019 | 3.1 / 4.6σ |
| 6.0 TeV | 0.421–0.440 | 0.467–0.488 | +0.027 | 4.3 / 6.5σ |

- **The bands never overlap**, and they diverge with M_VL: the hybrid's y′ falls faster.
- **A heavier partner makes them easier to tell apart.** With the partner at 3–6 TeV, FCC-hh distinguishes them at 3–6.5σ even after the uncertainty in c.

## (4) A signed-digit ternary multiplier
- **No digit multiplier is needed:** in balanced ternary, digit products are just signs.
- **Closure checked exhaustively:** redundant {−2..2} + {−2..2} addition is carry-free; u ∈ [−1, 1] and the sum digit stays in [−2, 2].
- **Verified:** 200 random 41-trit products, checked exactly.

| | rows | reduction levels | final carry-propagate |
|---|---|---|---|
| balanced ternary, 41 trits (≈ 64 bits) | 41 | **6** (2:1, carry-free) | one conversion |
| binary 64 bits, radix-4 Booth + Wallace 3:2 | 33 | 8 | one CPA |

Ternary saves 2 levels and the Booth recoding stage. Each level, however, is a 5-level-digit adder; the energy penalty of multi-level logic (Pass 12712) still applies.

## (5) Ternary network energy including arithmetic
- **Cost per weight:** bits × E_mem + E_op × (1 − zero fraction).
  - E_op = 0.1 pJ (32-bit add) for binary and ternary, 0.15 for 2-bit, 0.33 for int8.
  - Ternary has 44% zeros.
- **Crossover:** ternary beats binary per weight when **E_mem < 0.073 pJ/bit**. This is the weight-stationary and compute-in-memory regime (~0.01–0.05 pJ/bit), not SRAM (0.16) or DRAM (30).

| E_mem | Pareto front (re-scored, Pass 12714 accuracies) | ternary share |
|---|---|---|
| 30 (DRAM) | binary³ → ternary/binary/binary → 2-bit/binary/binary | 11% |
| 0.16 (SRAM) | same | 11% |
| **0.02 (in-memory)** | **ternary³** → ternary/ternary/2-bit → 2-bit/ternary/2-bit → 2-bit/binary/ternary → 2-bit/binary/binary | **47%** |

**When moving weights is cheap and arithmetic dominates, ternary takes over the front**, an all-ternary network included. This is the regime targeted by in-memory computing.

## Status
- **Hybrid:**
  - It has an explicit vacuum with exactly-light Q + U.
  - It needs an accidental SO(10) protected up to dimension 10.
  - It predicts a falling y′(M_VL), distinguishable from B′ at 2.3–6.5σ.
- **Ternary:**
  - it is optimal in in-memory neural-network inference and in links (PAM3);
  - it reduces multiplier depth;
  - it loses in conventional logic and memory-bound settings.
