# Pass 12656: the E6 cubic is Tr X³ over 27 three-qubit Paulis; every pure three-qubit state has charge vector with |Z|² = 3 and N(Z) = 1; Θ(W(3,3)) ≥ √60

Claude track. Follows Pass 12655. **Not a theory of everything.**

## 1. The E6(6) cubic from three-qubit Paulis (`w33_e6_cubic_from_three_qubit_paulis.py`)

Take Q₀(v) = x·z (parity of the number of Y's) and an antisymmetric Pauli a (here Y⊗I⊗I). Then Q(v) = Q₀(v) + ω(v, a) is an elliptic quadric Q⁻(5,2) in the three-qubit symplectic space:
- it has **27** singular points;
- its 45 totally singular lines are the commuting triples {u, v, u+v}; this is GQ(2,4).

For x ∈ R²⁷ put X = Σ_{Q(v)=0} x_v P_v, a traceless Hermitian 8×8 matrix. Checked:
- **Tr X³ / 48 = Σ over the 45 lines of s_uvw x_u x_v x_w**, with s = Tr(P_uP_vP_w)/8 = ±1 (32 plus, 13 minus);
- this signed cubic satisfies the adjoint identity and has a **78-dimensional stabiliser**; with all signs dropped, the adjoint identity fails (control);
- by Pass 12655 (uniqueness of the E6 sign class) it is therefore the repository's cubic up to relabelling and coordinate signs.

**Prior art.**
- Lévay–Saniga–Vrana–Pracna, Phys. Rev. D 79, 084036 (2009), label GQ(2,4) by three-qubit Paulis for the D = 5 entropy formula; their 40 nine-charge truncations are the 40 grids (the 40 trinification frames, W(3,3) lines).
- Ferrara–Günaydin write the cubic as Tr(ΩZ)³ in the USp(8) basis.
- The other track built a numerical 28×27 usp(8) intertwiner (89d6878ec).

What this pass adds is the closed formula in the repository's conventions with an executable check, and §2.

## 2. A state-independent sum rule: every pure state is a unit charge

The 27 quadric Paulis are exactly the non-identity Paulis that commute with the antiunitary J = P_a K (J² = −1, a quaternionic structure). The other 36 anticommute with it. For a pure state ψ:

(ρ + JρJ⁻¹)/2 = (I + X_ψ)/8, with X_ψ = Σ_{27} ⟨P_v⟩ P_v.

Since ⟨ψ|Jψ⟩ = 0, the operator ρ + JρJ⁻¹ is a rank-2 projector Π. So **X_ψ = 4Π − I**, with eigenvalues 3 (twice) and −1 (six times). Hence, for **every** pure three-qubit state:

- **Σ over the 27 quadric Paulis of ⟨P_v⟩² = 3** (from Tr X² = 24);
- **N(Z_ψ) = 1** for the charge vector Z_ψ = (⟨P_v⟩) (from Tr X³ = 48);
- the other 36 Paulis carry Σ ⟨P⟩² = 4.

Numerically, the minimum and maximum over pure states are 3.000000 for |Z|² and 1.000000 for N. All 1,080 stabiliser states have Z supported on exactly one line of the quadric (a triad) with N = +1.

**Reading.**
- The map ψ ↦ Z_ψ is the quaternionic Hopf (twistor) fibration CP⁷ → HP³ written in Paulis.
- Its image is one compact orbit USp(8)/(USp(2) × USp(6)) inside the N = 1 hypersurface of the 27.
- There are 28 such maps, one per antisymmetric Pauli.
- In the 5D black-hole dictionary every pure three-qubit state is a rank-3 charge with unit cubic invariant. That is a statement about this map, not about gravity.

**General n** (same argument): for each antisymmetric a, Σ_{b∈E_a} ⟨P_b⟩² = d/2 − 1 over the elliptic quadric E_a = {b ≠ 0 : Q₀(b) = ω(a, b)}.

## 3. The purity relations are exactly the quadric sum rules (`w33_transpose_lp_bound.py`)

- The antiunitary relations t_a = (1/d) Σ_b (−1)^{Q₀(b)+ω(a,b)} m_b = |⟨ψ|P_a|ψ*⟩|² were verified on random states (n = 2, 3, 4). They vanish for antisymmetric a.
- **They are not new constraints.** Adding them to the self-duality system of Pass 12653 leaves the rank unchanged at 6, 28, 120 for n = 2, 3, 4, which is exactly the number of antisymmetric Paulis 2^{n−1}(2^n − 1).
- So the Fourier self-duality of pure-state Pauli spectra **is** the family of elliptic-quadric sum rules.
- The LP with both families still returns the trivial d − 1 in all four test cases (three-qubit five-set, both four-qubit types, five-qubit 9-set). **Sixth failed relaxation** for the exact 1/32.

## 4. Negative: the MUB uncovered set is not "a point plus the 27 lines" (`w33_umub_uncovered_is_e6_cubic.py`)

Lemmas A and B of Pass 12649 have the same local counts as an elliptic quadric seen from a point (15 cosets with one member each, 6 pairs). But for the three-qubit five-set:
- no quadratic form vanishes exactly on U∖{p} for any p ∈ U;
- neither U nor C is a quadric;
- control: 0 of 200 random 27-sets are quadrics.

The conjecture is false. (The script stops at its first assertion by design and is kept as the record.)

## 5. Shannon capacity: Θ(W(3,3)) ≥ √60 (`w33_shannon_symmetric_codes.py`, `w33_shannon_symmetric_codes_conj.py`)

- Codes in G⊠G invariant under ⟨(g, g^a)⟩ for g of order 5 (no fixed points) reach **size 60**, proved optimal within that symmetry class for every twist a (CP-SAT OPTIMAL). C₅ control: 5.
- The 60-code was **independently verified** on a separately built W(3) (GQ axiom, VF2 isomorphism): 0 conflicts.
- Other classes: order 3 gives 58; order 4 gives 56; order 2 gives 56; with the coordinate swap at most 55.
- Conjugate twists ⟨(g, c g^a c⁻¹)⟩ for 25 random c per class have not beaten 60 (orders 5, 6, 9 and the order-3 class with 4 fixed points done; the order-3 class with 13 fixed points was still running at commit).
- **√60 ≈ 7.746 ≤ Θ(W(3,3)) ≤ 10.**

## Cross-track

- The other track's `2026-11-13_e6_tits_coordinates.md` (84a62035d, 24d7141f0) constructs the explicit Chevalley/Tits lift that Pass 12655 left open, citing it. Agreed.
- Their a4593c961 (15:44) proves "each four-coordinate overlap determines both sections". `w33_sections_levi_overlap.py` (Pass 12655 addendum A, computed independently, committed here) finds the same counts: 1,080 pairs, 15 per sixer, 5 per fiver. **They committed first; this pass cites it** and adds only the stabiliser orders 720/240.

## Open

- A structural description of the 60-code (12 orbits of Z₅; 30 distinct points per coordinate with multiplicities 1, 2, 3).
- The exact five-qubit 1/32: six relaxations are now ruled out.
- Whether the 28 quaternionic maps CP⁷ → HP³ organise the three-qubit MUB problem.
