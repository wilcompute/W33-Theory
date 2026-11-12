# Pass 12649: smallest maximal Pauli MUB sets as symmetric-matrix rank codes (five qubits: no size ≤ 6); an analytic reduction of the three-qubit 1/8 to one 4⊗4 inequality

Claude track. Follows Pass 12648. **Not a theory of everything.** The parallel assistant refreshed `RESULTS_INDEX.md` with our Pauli MUB results (cb251b986) and works on rotor thresholds (a8b5ae286, b43aca67a); there is no overlap.

## 1. Rank-code form (`w33_symmetric_rank_code_spreads.py`)

Fix L₀ = the X-type and L₁ = the Z-type Lagrangian; by Witt, any maximal partial spread of size ≥ 2 contains a complementary pair.
- A Lagrangian disjoint from L₁ is a graph {(x, Sx)} with S symmetric over F₂. It is also disjoint from L₀ iff S is **nonsingular**.
- graph(S) and graph(T) are disjoint iff **S + T is nonsingular**.

> A maximal partial spread {L₀, L₁, graph(S₁), …, graph(S_k)} is the same thing as a set of nonsingular symmetric matrices with pairwise nonsingular differences, such that every nonsingular symmetric T has T + S_i singular for some i.

Every sum is symmetric, so one singularity table over all 2^{n(n+1)/2} symmetric matrices answers each test with an XOR and a lookup.
- S₁ runs over congruence classes: one class, I, for odd n; I and the alternating form for even n.
- The number of sets through the pair is Σ_classes |class|·c_class/k.

| n | nonsingular symmetric | size 3 | size 4 | size 5 through the pair | size 6 | size 7 |
|---|---|---|---|---|---|---|
| 3 | 28 | none | none | **56** (= Pass 12648) | none | none |
| 4 | 448 | none | none | **896** (= Pass 12648) | — | — |
| **5** | **13,888** | **none** | **none** | **none** | **none** (`w33_five_qubit_size6.py`; S₂ reduced mod O(5) of order 720, 8 orbits) | pending (time-limited search; see addendum) |

**Two independent methods agree.** Pass 12648 used an explicit Lagrangian enumeration; this method uses only symmetric matrices. They give identical counts at n = 3 and n = 4.

> **Five qubits: W(9,2) has no maximal partial spread of size ≤ 6.** Every weakly unextendible five-qubit Pauli MUB set has at least 7 bases. Grassl's conjecture q^{n/2} + 1 concerns even n only. Kantor's survey notes that small cases have counterexamples; for n = 5 nothing is claimed beyond this lower bound.

## 2. The genuine four-qubit optimum is isolated (`w33_optimum_hessian_nullity.py`)

Null directions of the Hessian on the sphere, beyond the global phase:

| optimum | min F | nullity | reading |
|---|---|---|---|
| three-qubit size 5 (control) | 0.125 | **2** | continuum (as found in Pass 12647) |
| two-qutrit pentad | 0.14711 | 0 | isolated |
| four-qubit genuine size 5 | 0.0523626 | **0** (smallest tangent eigenvalue 0.051, 4-fold) | **isolated** |

So the 15 profiles of Pass 12648 are distinct isolated optima, not a family. An exact algebraic value is plausible but unidentified.

## 3. Three qubits: min F = 1/8 reduces to one 4⊗4 inequality (`w33_threequbit_conditioning_profile.py`, `w33_threequbit_analytic_one_eighth.py`, `w33_kappa_structure.py`)

Condition on the distinguished uncovered Pauli P₀ (the singleton class of Pass 12643). Write ψ = cψ₊ + sψ₋ with t = ⟨P₀⟩ = c² − s², and let A (12) and B (15) be the uncovered Paulis anticommuting and commuting with P₀.

**Numerical profile:** max Σ_U ⟨P⟩² at fixed t is **6 − 2t²** exactly, with Σ_B = 3 and Σ_A = 3(1 − t²).

**Lemma A (exact).** B maps **bijectively** onto the 15 points of p₀^⊥/⟨p₀⟩ ≅ W(3,2) (verified). On each eigenspace the B operators are, up to sign, the 15 two-qubit Paulis, so the purity identity gives Σ ≤ 3. B commutes with P₀, so convexity gives Σ_B ⟨P⟩² ≤ 3.

**Lemma B (exact).** A consists of 6 pairs {a, a + p₀} (verified). The Hermitian Pauli of a + p₀ is ±i·aP₀, so a pair contributes (1 − t²)|⟨ψ₊|a|ψ₋⟩|² *exactly*. Hence Σ_A = (1 − t²)·Σ_{j=1}^{6} |⟨ψ₊|a_j|ψ₋⟩|² ≤ (1 − t²)·κ.

**Conclusion.** If **κ := max over unit x ∈ V₊, y ∈ V₋ of Σ_j |⟨x|M_j|y⟩|² ≤ 3**, then Σ_U ≤ t² + 3(1 − t²) + 3 = 6 − 2t² ≤ 6, i.e. **min F = 1/8 exactly** for all 24,192 sets.

**Status of κ ≤ 3.**
- Numerically κ = 3.0000000000 (the maximiser has four contributing terms: 1, 1, 0.622, 0.378).
- A decomposable certificate (PSD + partial-transpose PSD) is **infeasible** (margin −2), so the inequality is not provable that way.
- Structure: the six 4×4 unitaries are I and five two-qubit Paulis whose **anticommutation graph is the pentagon C₅** (Lovász number √5).
- **Open:** an exact proof of κ ≤ 3, perhaps from the pentagon structure or a degree-higher (symmetric-extension) certificate. This is a 16-variable problem, against the 8-dimensional degree-6 SOS it replaces.

**An earlier slip in this pass.** My first write-up of Lemma B carried a spurious factor 2 and asked for κ ≤ 3/2. The corrected statement is above; the 3/2 SDP was infeasible for that reason.

## 4. Paper draft

`papers/strongly_unextendible_pauli_mubs.tex` now covers the lifted/genuine split (Pass 12648) and the five-qubit lower bound (this pass).

## Open

- An exact proof of κ ≤ 3 (and hence 1/8).
- Five qubits: the size-7 search (see the table) and the true minimum.
- A closed form for the isolated genuine four-qubit optimum.
