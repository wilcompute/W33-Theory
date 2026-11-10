# Pass 12645: min F = 1/16 exactly for a nine-element four-qubit Pauli MUB set (facial reduction); it has no mirror partner; the non-stabiliser optimisers have no Weyl symmetry

Claude track. Follows Passes 12643–12644. **Not a theory of everything.**

## 1. Exact tight four-qubit value (`w33_four_qubit_facial_reduction.py`, `data/w33_four_qubit_facial_reduction.json`)

Pass 12644 certified ϑ ≤ 14 + 1/2000 only: the optimal dual face is degenerate, so plain rounding failed. **Facial reduction fixes this.**
- A commuting set of 14 uncovered Paulis spans a maximal isotropic 4-space. Maximality makes that Lagrangian meet C, so the 14-sets are exactly the three Lagrangians meeting C in one point, minus that point.
- Each gives a primal optimum X_S = 1_S 1_Sᵀ/14. Complementary slackness forces (14I − Y)1_S = 0 for every optimal dual Y: **318 linear equations, of rank 315**.
- With these equalities the dual returns t = 14.00000004. Rounding the free multipliers to denominator **4** and solving the 315 pivot variables exactly from the reduced row echelon form makes the slackness equations hold exactly.
- **14I − J − T ⪰ 0 then passes an exact rational LDLᵀ check** (float min eigenvalue −6×10⁻¹⁵, i.e. exactly 0 on the kernel).

> **Theorem (exact, given de Gois–Hansenne–Gühne).** For the nine-element four-qubit Pauli MUB set with lines [53, 508, 753, 1027, 1092, 1602, 1876, 2024, 2095] (indexing in `w33_four_qubit_theta_exact.py`) and every v ∈ C¹⁶:
> Σ_e (|⟨e|v⟩|² − |v|²/16)² ≥ |v|⁴/16, **with equality** for the stabiliser states of the three Lagrangians meeting the covered set once.

**The qubit rungs, all exact:**

| d | set | min F | certificate |
|---|---|---|---|
| 4 | 3 bases (all) | 1/4 | ϑ = α = 2; also an elementary 2-class cover |
| 8 | 5 bases (all 24,192; one orbit) | 1/8 numerically; ≥ (3 − √5)/8 exact | ϑ ≤ 4 + √5 (Q(√5) dual); tight value open |
| 16 | 9 bases (one certified set) | **1/16 exact** | ϑ = α = 14, facially reduced dual over (1/4)Z |

**Reading.** Three qubits are the exception: ϑ > α there, so neither the Lovász bound nor any anticommuting cover can be tight. At d = 4 and d = 16 the Lovász number equals the stabiliser value. "d/2 + 1 sets attain 1/d" holds at d = 4, 8 (numerically) and 16.

## 2. No mirror partner at four qubits (`w33_four_qubit_mirror_partners.py`)

The covered set C (135 points) contains 17 Lagrangians but has **exactly one** partition into 9. So the certified d = 16 set has **no** mirror partner. By contrast, every two-qutrit pentad and every three-qubit 5-set has exactly one partner. Mirror pairing is therefore not a general feature of minimal sets. Only this one d = 16 set was examined.

## 3. The non-stabiliser optimisers (`w33_d25_optimiser_structure.py`)

- **Neither optimiser is an eigenstate of any Weyl operator** (no |⟨W_u⟩| = 1), so there is no shortcut through a stabiliser subspace.
- **Pentad:** two levels on covered vectors (×24, ×16) and two on uncovered (×24, ×16).
- **d = 25 single cover:** 144 Weyl expectations of modulus 0.166667, i.e. 1/6 to six digits (48 covered, 96 uncovered).
- The automatic 6-digit identifications of the other levels are **spurious** (the tolerance was too loose) and are not used.
- (207 − 19√57)/432 and 13/75 remain numerical identifications (Pass 12644).

## 4. Exact three-qubit 1/8: not attempted to completion

The same facial reduction applies in principle: the minimisers are the stabiliser states of lines meeting C once. But exact coefficient matching for a degree-6 SOS (Gram blocks 120 and 288 over Q(i)) means exact linear algebra in roughly 10⁵ unknowns, which is beyond Python fractions in one round. A symmetry reduction (the order-60 stabiliser together with Pauli invariance) should come first.

## 5. Replay request

`analysis/HANDOFF_CLAUDE_TO_CHAT_20261106.md` now lists, cheapest check first: the four-qubit denominator-4 certificate; the three-qubit Q(√5) dual; the orbit counts; and the two numerical identifications.

## Open

- Whether all nine-element four-qubit sets are equivalent (only two integer-program samples; both have ϑ = 14).
- The exact three-qubit 1/8.
- Closed forms of the non-stabiliser optimisers.
