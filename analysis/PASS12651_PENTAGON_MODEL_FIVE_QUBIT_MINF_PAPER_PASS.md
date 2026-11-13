# Pass 12651: an explicit pentagon model for κ; the five-qubit size-9 set has min F = 1/32; a six-qubit test; an overclaim pass on the paper

Claude track. Follows Pass 12650. **Not a theory of everything.**

## 1. κ in an explicit model (`w33_kappa_pentagon_model.py`)

κ = max over unit c ∈ C⁶ of ‖Σ_j c_j R_j‖²_op (Pass 12650). An explicit two-qubit model:

**{II, XI, ZI, XZ, IX, ZY}**: consecutive members of the pentagon (XI, ZI, XZ, IX, ZY) anticommute; non-consecutive members commute.

- **Same structure as the data:** commutation degrees [4, 4, 4, 4, 4, 6] in both.
- **Same value:** κ_model = κ_data = 3.000000000000005.
- **Block form.** The six split into three commuting pairs {II, IX}, {XI, XZ}, {ZI, ZY}, so
  M = I⊗B₀ + X⊗B₁ + Z⊗B₂, with B₀ ∈ span{I, X}, B₁ ∈ span{I, Z}, B₂ ∈ span{I, Y}, and
  M†M = I⊗S + X⊗T₁ + Z⊗T₂ + Y⊗T₃, where S = Σ_k B_k†B_k, T₁ = B₀†B₁ + B₁†B₀, T₂ = B₀†B₂ + B₂†B₀, T₃ = −i(B₁†B₂ − B₂†B₁).
- **Maximisers:** two coefficients of modulus exactly 1/√3, with the remaining weight 1/3 distributed differently in the model and the data. The maximum is attained on a family.

κ ≤ 3 is now a largest-eigenvalue bound for a 2×2-block Pauli expansion with 2×2 Hermitian coefficients. **A hand proof is still open.**

## 2. Five-qubit size-9 set: min F = 1/32 (`w33_five_qubit_size9_minF.py`)

279 covered Paulis (X-type, Z-type and seven graphs); 150 L-BFGS starts. **min F = 0.03125000004 = 1/32 = 1/d**, the stabiliser value (the five lowest runs all agree). So the set is **strongly unextendible numerically**, with min F = 1/d, like the three-qubit sets and the four-qubit nine-sets. An exact certificate would need ϑ = α = 30 for the 744-vertex uncovered graph; not attempted.

## 3. Five-qubit size 8: longer search (`w33_five_qubit_size8_anneal2.py`)

Annealing with single and double replacements, 1,087 restarts in 2,400 s: **no size-8 set**. Every restart gets stuck at exactly 24 extendible matrices (the same best cost as in Pass 12650). The size-9 control is found in 1.6 s. This is **evidence, not proof**, that the five-qubit minimum is 9. The robust floor of 24 is a structural hint worth explaining.

## 4. Six qubits (`w33_six_qubit_greedy.py`)

Greedy rank codes over the 2²¹ symmetric 6×6 matrices (about 880k nonsingular):
- coverage-biased: sizes {**9**: 1, 10: 5, 11: 54, 12: 28, 13: 12, 14: 3} over 103 runs;
- random: {16: 33, 17: 157, 18: 97, 19: 13} over 300 runs.

**The smallest found is 9**, matching the predicted 2^{⌈6/2⌉} + 1 = 9, which is Grassl's q^{n/2} + 1, known to exist for even n. Nothing smaller was found, which does not rule smaller sizes out.

**Independent verification** (`w33_six_qubit_size9_verify.py`; own GF(2) rank, no lookup table): the matrices are nonsingular with nonsingular pairwise sums, and none of the **888,832** nonsingular symmetric 6×6 matrices extends the set. **A six-qubit maximal Pauli MUB set of size 9 exists.**

## 5. Overclaim pass on the paper (`papers/strongly_unextendible_pauli_mubs.tex`)

- **Theorem 1:** "every three-set" is now justified. Exactly one three-set passes through a fixed complementary pair (exhaustive), so by Witt they form one orbit.
- **Theorem 3(ii):** the lift statement is now stated for a **representative** of each invariant type. Types are defined by invariants, and orbit-uniqueness within a type was not checked.
- **Abstract:** "below every stabiliser value" became "below its stabiliser value 1/16"; the five-qubit result was added.
- **Proposition (five qubits):** now includes min F = 1/32 for the size-9 set; the summary table gained a d = 32 row.
- **TeX corruption fixed:** an earlier scripted edit had turned `\rceil` into a carriage-return byte. Fixed at the byte level; a scan finds no other control characters or tabs. *(Lesson: never edit TeX through Python strings in a Bash heredoc; use the Edit tool or a byte-level script.)*
- **Scope:** Pauli-class only, citing Grassl–McNulty–Mišta–Paterek (Pass 12650).

## Open

- A hand proof of κ ≤ 3 (block form above).
- Five-qubit size 8.
- The six-qubit minimum.
- Exact certificates for the five-qubit size-9 set.
