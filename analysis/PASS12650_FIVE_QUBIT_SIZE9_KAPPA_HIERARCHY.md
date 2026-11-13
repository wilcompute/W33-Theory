# Pass 12650: five-qubit maximal Pauli MUB sets of size 9 exist (minimum 8 or 9); κ ≤ 3 resists the SOS hierarchy; the genuine four-qubit optimum to 45 digits; a scope correction (Grassl et al. 2017)

Claude track. Follows Pass 12649. **Not a theory of everything.** The parallel assistant continues on rotor thresholds; a replay request has been added to the handoff.

## 0. Scope correction (prior art)

Grassl, McNulty, Mišta and Paterek (*Small sets of complementary observables*, PRA 95, 012118 (2017); arXiv:1611.08962) give strongly unextendible sets of only **three (non-Pauli) MUBs** in many dimensions, d = 16 included, verified by computer-aided algebra.
- Every statement in Passes 12636–12650 concerns **Pauli-class** MUB sets.
- The phrase "five bases are strongly unextendible in d = 16" (Pass 12647 and the paper draft) is now qualified "Pauli-class", and the paper cites this work.

## 1. Five qubits: size 9 exists; the minimum is 8 or 9 (`w33_rank_code_greedy_sizes.py`, `w33_five_qubit_local_search.py`, `w33_five_qubit_size9_verify.py`)

- **Greedy rank codes (n = 5).** Random greedy gives sizes {10: 8, 11: 598, 12: 1537, 13: 713, 14: 93, 15: 22, 17: 25, 33: 4} over 3,000 runs. The coverage-biased variant gives {**9: 2265**, 10: 473, 11: 253, 12: 9}.
- **Local search.** Annealing found size 9 at once. For size 8: 362 restarts in 1,500 s, best state still had 24 extendible matrices, **not found**.
- **Control (n = 4).** Annealing finds size 5 (in 17 s); random greedy also hits 5 (4 of 2,000 runs).
- **Independent verification of the size-9 set** (own GF(2) rank, no lookup table): all 7 matrices nonsingular; pairwise sums nonsingular; every graph isotropic; none of the 13,888 nonsingular T extends it.

> **W(9,2) has a maximal partial spread of size 9, and none of size ≤ 7 (Pass 12649). The five-qubit minimum is 8 or 9.** Size 8 is not ruled out; an exhaustive search would need roughly 100× the size-7 effort.

**A pattern (conjecture, four data points):** min = 2^{⌈n/2⌉} + 1, i.e. 3, 5, 5, and 9 if size 8 is excluded. For even n this is Grassl's q^{n/2} + 1. Kantor's Remark 4.7 (arXiv:1601.04194) says that for even q there "appears to be a maximal symplectic partial spread of size 2^i + 1 whenever q^{n/2} + 1 ≤ 2^i + 1 ≤ q^n + 1". At n = 5 that predicts sizes 9, 17 and 33, which match the greedy sizes. **Prior art:** Grassl's computer tables (cited by Kantor) may already list these minima. Not claimed new.

## 2. κ ≤ 3: numerically certain, not certifiable at low levels (`w33_kappa_alternating.py`, `w33_kappa_hierarchy.py`)

- **Alternating maximisation** from 2,000 random starts: every run converges to κ = 3.0000000000000036 (worst local value 2.999997).
- **A(y) is not a scaled projector:** for random y the top eigenvalue of A(y) = Σ_j M_j y y† M_j† is about 2.6–2.86, so 3 is reached only at special y.
- **Certificate hierarchy** for |x|^{2(a−1)}|y|^{2(b−1)}(3|x|²|y|² − Σ_j |x†M_j y|²), with optional partial-transpose blocks:

| level (a, b) | blocks | basis size | margin |
|---|---|---|---|
| (1, 2), constant 4 (control) | plain | 40 | **+1.0** (feasible) |
| (1, 2) | plain + PT_y | 40 | −1.82 |
| (2, 1) | plain + PT_x | 40 | −1.82 |
| (2, 2) | plain | 100 | −5.05 |
| (2, 2) | plain + PT_y | 100 | −1.94 |
| (2, 2) | plain + PT_x + PT_y | 100 | −1.29 |

So κ ≤ 3 is a tight biquadratic inequality on C⁴ × C⁴ that **no low level of the SOS/PPT hierarchy certifies**.

**Exact reformulation.** The six R_j are Hilbert–Schmidt-orthogonal Paulis, so

> **κ = max over unit c ∈ C⁶ of ‖Σ_j c_j R_j‖²_op** (R₁ = I, R₂…R₆ with pentagon anticommutation C₅).

Hence κ ≤ 3 says that every combination of I and the five pentagon Paulis has operator norm² ≤ 3|c|². A group-theoretic proof looks like the natural route. **Open.**

## 3. The genuine four-qubit optimum (`w33_genuine_optimum_highprec.py`)

Newton's method in mpmath (dps 80, gauge v₀ = 1), started from the double-precision optimum, converges quadratically (gradient 10⁻¹⁵ → 10⁻²⁷ → 10⁻⁴⁵, plateau about 6×10⁻⁴⁷):

**f* = 0.052362560756684733704581146700071134403665100…** (about 45 reliable digits).

**No algebraic relation** of degree ≤ 4 with |coefficients| ≤ 10⁴ (residual threshold 10⁻⁴⁵), nor of degree 5–8 with |coefficients| ≤ 10⁵ (threshold 10⁻⁴⁰). With the Hessian result of Pass 12649 (isolated optimum), the value is an isolated algebraic number of higher complexity, or not of low degree. **No closed form claimed.**

## 4. Paper draft

Updated with:
- the Pauli-class scope and the Grassl et al. citation;
- the five-qubit statement: size ≤ 7 impossible, size 9 exists;
- the analytic reduction with the κ reformulation.

## Open

- Size 8 at five qubits, which needs an exhaustive search.
- κ ≤ 3, via the operator-norm form and the pentagon.
- A closed form for f*.
