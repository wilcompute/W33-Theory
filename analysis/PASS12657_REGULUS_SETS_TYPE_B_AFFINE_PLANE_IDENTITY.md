# Pass 12657: the minimal qubit MUB sets are reguli over F_q; type B is the F₄ regulus; F is an explicit sum of squares on the affine plane AG(2,4); the size-8 cross-check agrees

Claude track. Follows Pass 12656. **Not a theory of everything.**

## 1. Regulus sets (`w33_regulus_mub_sets.py`)

Take q = 2^k and view n = 2k qubits as two F_q-"qudits". The symplectic space is F_q⁴ = {(x₁, x₂, z₁, z₂)} with ω = Tr(x·z′ + z·x′), and it carries the F_q-valued quadratic form Q = x₁z₁ + x₂z₂, a hyperbolic quadric Q⁺(3,q). One regulus of Q is

- L_∞ = {x = 0};
- L_t = {z₁ = t·x₂, z₂ = t·x₁} for t ∈ F_q.

These are q + 1 pairwise disjoint Lagrangians. This is the q^k + 1 family of Kantor (arXiv:1601.04194, Thm 5.2), written explicitly.
- In rank-code form: S_t = [[0, M_t], [M_t, 0]] with M_t[i][j] = Tr(t·b_i·b_j).
- The eigenbases are the computational basis and CZ_t·(F⊗F)|x₁, x₂⟩, where CZ_t = diag χ(t·x₁x₂): an explicit family of q + 1 bases of C^q ⊗ C^q.

**Verified:**

| q | qubits | size | maximal | covered set |
|---|---|---|---|---|
| 2 | 2 | 3 | yes (4 matrices) | = {Q = 0}, 9 points |
| 4 | 4 | 5 | yes (448) | = {Q = 0}, 75 points |
| 8 | 6 | 9 | yes (all 888,832) | = {Q = 0}, 567 points |

- **The covered Paulis are exactly the F_q-quadric {Q = 0}.** So F = (1/d)·Σ_{Q(v)=0} ⟨P_v⟩² is a quadric sum over F_q. For q = 2 this is the sum over symmetric Paulis, d(1 + c)/2 − 1 with c = |⟨ψ|ψ*⟩|², which is the whole proof of 1/4.
- **Type B is the F₄ regulus.** The q = 4 set has 10 Lagrangians inside its covered set and 2 partitions (the two reguli of the quadric). The census of Pass 12648 has (6, 1) for type A and (10, 2) for type B. The identification is by these two invariants, not by an explicit Sp(8,2) element.
- The six-qubit 9-set of Pass 12651, found by search, is **not** equivalent to the F₈ regulus (addendum).

## 2. An exact sum-of-squares identity for type B (`w33_typeB_affine_plane_inequality.py`)

Write the state as A: F₄² → C with Σ|A_p|² = 1.

**Index-of-coincidence formula** (checked to 10⁻¹⁶ for q = 2, 4, 8):

Σ_{t∈F_q} IC_t = (1/q)·[c + 2(1 − IC_∞) + R′], with
- c = |Σ_x A(x)²|²;
- G(σ, δ) = Σ_x A(x)·A(x+σ)·conj(A(x+δ)·A(x+σ+δ));
- R′ = Σ_{σ≠0} Σ_{λ≠0,1} G(σ, λσ).

It follows from summing the character χ(t·(…)) over t, which forces δ ∥ σ over F_q.

**For q = 4** the four points {x, x+σ, x+ωσ, x+ω²σ} are an affine F₄-line. The formula becomes an identity (residual 6×10⁻¹⁶ on random states):

> **F(A) + 5/16 = Σ_p |A_p|⁴ + ¼·|Σ_p A_p²|² + Σ over the 20 lines ℓ of AG(2,4) and the 3 pairings ab|cd of ℓ of |A_aA_b + A_cA_d|².**

So **min F = 1/16 for type B ⇔ the right side is ≥ 3/8 for unit A**.
- Numerically the minimum is 0.37500000 (60 starts).
- Basis states and the uniform state give 5/4.
- This replaces the coupled inequality of Pass 12652 addendum C by a statement about one function on the 16 points of an affine plane, with every term a square.

**Why it is not yet a proof.** As a Hermitian form on A⊗A the right side has a kernel (y_ab = −y_cd on each pairing), so the bound needs the rank-one relations A_aA_b·A_cA_d = A_aA_c·A_bA_d. Whether a PSD-plus-partial-transpose certificate reaches 3/8 is tested in `w33_typeB_decomposable_certificate.py`; see the addendum.

## 3. Five qubits: the size-8 cross-check agrees

The reversed-traversal run (Pass 12654 addendum) finds none on both S₃-class representatives: 54,001,206 and 53,942,707 nodes. Same code base, different search order. The paper now states the minimum 9 with that qualification.

## Open

- Prove the AG(2,4) inequality (exact 1/16 for type B).
- The analogous identity for q = 8 (six qubits; R′ has six λ-terms) and min F = 1/64.
- Is the five-qubit 9-set a quotient of the F₈ regulus at a non-singular point (Kantor Lemma 6.1)? (The Pass 12651 six-qubit set is not the F₈ regulus; see the addendum.)

## Addendum

**The first SOS level gives only the trivial bound** (`w33_typeB_decomposable_certificate.py`). The largest δ with LHS − δ·(Σ|A|²)² = ⟨A⊗A|M₂|A⊗A⟩ + ⟨A⊗Ā|M₁|A⊗Ā⟩, M₁, M₂ ⪰ 0, is **δ\* = 0.3125 = 5/16** (SCS, optimal; control with LHS = norm² returns 1.0000). That is exactly F ≥ 0. So the AG(2,4) inequality, like κ ≤ 3 at three qubits, has no decomposable certificate; a proof needs degree 6 or a structural argument.

**Two inequivalent six-qubit 9-sets.** The number of F₂-quadratic forms vanishing on the covered set is an Sp-invariant:

| set | covered points | vanishing quadrics |
|---|---|---|
| F₄ regulus (type B) | 75 | 2 |
| F₈ regulus | 567 | 3 |
| Pass 12651 six-qubit set (found by search) | 567 | 1 |
| five-qubit 9-set (Pass 12650) | 279 | 0 |

- The regulus values are k = log₂ q, the forms Tr(s·Q).
- The Pass 12651 set has only one, so **it is not equivalent to the F₈ regulus**: there are at least two inequivalent maximal 9-sets for six qubits. Its numerical min F = 1/64 (Pass 12652) therefore says nothing yet about the regulus set, and vice versa.
