# Pass 12652: κ ≤ 3 is proved by a two-moment eigenvalue bound, so min F = 1/8 exactly for every three-qubit five-set; the five-qubit floor of 24 explained; six qubits at 1/64

Claude track. Follows Pass 12651. **Not a theory of everything.**

## 1. κ ≤ 3, proof (`w33_kappa_moment_proof.py`)

κ = max over unit x, y ∈ C⁴ of Σ_{j=1}^{6} |⟨x|M_j y⟩|². The M_j are the unitary 4×4 restrictions V₋ → V₊ of the six representatives a_j of the uncovered Paulis that anticommute with P₀ (Lemma B, Pass 12649).

**Setup.** Fix a unit y and put W = [M₁y, …, M₆y]. Then max_x Σ_j |⟨x|M_j y⟩|² = λ_max(WW*). The 4×4 matrix WW* has:
- Tr WW* = 6, since each M_j is unitary;
- Tr (WW*)² = Σ_{j,k} |⟨y|M_j*M_k|y⟩|².

**Key fact (checked in exact Gaussian-integer arithmetic).** The 15 products M_j*M_k (j < k), together with I, are pairwise Hilbert–Schmidt orthogonal unitaries. So up to phase they are the 15 non-identity two-qubit Paulis on V₋.
- Purity of y then gives Σ_{j<k} |⟨y|M_j*M_k|y⟩|² = 4 − 1 = 3.
- Bessel's inequality would already give ≤ 3.
- So **Tr (WW*)² = 6 + 2·3 = 12 for every y**.

**Moment bound.** Let λ₁ ≥ … ≥ λ₄ ≥ 0 be the eigenvalues of WW*. Cauchy–Schwarz on λ₂, λ₃, λ₄ gives
(6 − λ₁)² ≤ 3(12 − λ₁²), i.e. 4λ₁(λ₁ − 3) ≤ 0, i.e. **λ₁ ≤ 3**.
This is the trace bound of Wolkowicz–Styan (LAA 29, 1980). Equality forces the spectrum (3, 1, 1, 1). The numerical maximiser has exactly (3, 1, 1, 1, 0, 0) for W*W.

With Lemmas A and B (Pass 12649) and the single Sp(6,2)-orbit (Pass 12643):

> **Theorem.** For every five-element three-qubit Pauli MUB set (all 24,192) and every v ∈ C⁸, F(v) ≥ |v|⁴/8, with equality at stabiliser states. **min F = 1/8 exactly.**

This replaces the interval [1/8 − 10⁻⁶, 1/8] (Pass 12647).
- The inequality κ ≤ 3 had resisted decomposable certificates and the SOS/PPT hierarchy at levels (1,2), (2,1) and (2,2) (Passes 12649–12650). It is a positive but non-decomposable map on M₄, and the moment argument goes around that obstruction.
- **Combinatorics.** {a_j + a₁} mod p₀ is a six-subset of F₂⁴ containing 0 whose 15 pairwise sums are all the non-zero vectors. A pentagon anticommutation graph forces this: the Gram matrix of C₅ over F₂ has kernel ⟨(1,1,1,1,1)⟩, so the only linear relation is Σ = 0.
- **The pentagon model of Pass 12651 needs no cases.** For {II, XI, ZI, XZ, IX, ZY}, Tr G = 6 and Tr G² = 12 identically, and the commuting triple {I, XI, XZ} attains 3 (`tests/test_w33_pass12652.py`).

**General form.** For unitaries R₁…R_k on C^d whose pairwise quotients R_j*R_k (j < k) are HS-orthogonal to each other and to I:

max Σ_j |⟨x|R_j y⟩|² ≤ (k + √((r−1)(r(k + 2(d−1)) − k²)))/r, with r = min(d, k).

## 2. Five qubits, size 8

**CP-SAT is not the tool** (`w33_five_qubit_size8_cpsat.py`).
- The model fixes S₁ = I and S₂ to one of the 8 O(5)-orbit representatives, with conflict and coverage clauses (about 1.6M binary clauses per orbit).
- n = 3 controls pass: size 5 is feasible and verified; size 6 is infeasible.
- At n = 5, size 7, CP-SAT returned UNKNOWN after 600 s on the first orbit (8 workers). The rank-code DFS of Pass 12649 settles all of size 7 in 2,695 s.
- The size-8 runs were stopped. **No new size-8 result.**

**The floor of 24 explained** (`w33_five_qubit_floor24.py`). Ten annealed six-matrix states, each with |E| = 24 extendible T, were analysed:
- **In every state, E contains an isolated vertex T\*** (compatible with no other member of E), and **adding T\* gives a verified maximal set of size 9**. The cost-24 states are 9-sets with one matrix deleted.
- Deleting a matrix frees itself plus a private region of 23 matrices that only it blocked.
- Two types appear:
  - (8 states) compatibility graph on E with degrees {0¹, 6⁹, 8¹⁰, 10³, 12¹}, clique number 4;
  - (2 states) four isolated vertices and a 7-clique. Adding the 7-clique gives a maximal set of size 15.
- Every pair sum T + S_i over E is nonsingular (rank 5), as it must be.

So the landscape is dominated by 9-sets, and the annealing floor measures the smallest private region of a member (24 = 1 + 23). It is **evidence, not proof**, that the five-qubit minimum is 9.

## 3. Five-qubit size-9 set: towards an exact 1/32 (`w33_five_qubit_size9_theta.py`)

The anticommutation graph on the 744 uncovered Paulis is **368-regular**, and greedy finds α = 30.
- Spectrum: 368¹, 16²²⁵, −16²⁴⁸, and 270 simple eigenvalues in between.
- Hoffman bound = 744·16/384 = **31 = d − 1**: trivial (F ≥ 0).
- ϑ (SDP): still running when this was committed; see the addendum

## 4. Six qubits (`w33_six_qubit_size9_minF_size8.py`)

- The verified size-9 set (Pass 12651) has **min F = 1/64 = 1/d** numerically: 60 L-BFGS starts, five lowest all 0.015625000.
- This continues 1/8, 1/16, 1/32: every 2^⌈n/2⌉+1-type set tested has min F = 1/d.
- Size-8 annealing: still running when this was committed; see the addendum

## Open

- An exact 1/32 at five qubits (needs ϑ = 30, or a conditioning argument like §1).
- Five-qubit size 8 (exhaustive, needs a better search than CP-SAT).
- The six-qubit minimum.
- Whether §1's conditioning plus moment method gives the four-qubit lifted type exactly (1/16).
