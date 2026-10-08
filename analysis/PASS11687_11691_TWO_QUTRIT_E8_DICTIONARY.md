# Passes 11687–11691 — the two-qutrit E₈ dictionary: centralisers, triality, the magic gate, chirality as C × T, and the Witting intertwiner

Producer: `analysis/w33_pass11687_11691_two_qutrit_e8_dictionary.py`
Certificate: `data/w33_pass11687_11691_two_qutrit_e8_dictionary.json`
Regression: `tests/test_w33_pass11687_11696.py`

**Starting point.** Everything here lives in the explicit e₈ = sl(9) ⊕ Λ³C⁹ ⊕ Λ³C⁹\* of two qutrits (Pass 11681).
* It is graded by Pauli charge v ∈ F₃⁴: E₈₀ is the Pauli-singlet Cartan h, and dim E₈_v = 3 for v ≠ 0.
* For a subgroup S of Pauli charges the centraliser is h ⊕ ⨁_{v ∈ S^⊥} E₈_v (symplectic complement).
* So **the symplectic subspace lattice of F₃⁴ (W(3,3) geometry) maps onto regular subalgebras of E₈ containing h.**

## 11687 — centralisers and triality

| Pauli subgroup S | roots (on S^⊥) | centraliser |
|---|---|---|
| a point p (one Pauli and its square) | 78 | **E₆ ⊕ A₂** (dim 86). Prior art: BT7175/7181, the 1 + 12 + 27 shell |
| the hyperplane p^⊥ | 6 | **A₂**, the point's own SU(3) |
| a Lagrangian line L (L^⊥ = L) | 24 | **A₂⁴**, one SU(3) per point of the W(3,3) line, mutually orthogonal |
| one qutrit's Paulis H (a tensor factor) | 24 | **D₄**, on the other qutrit's 8 charges; H and H^⊥ give a dual pair D₄ × D₄ |

**Triality.** Take the standard factorisation.
* **The cosets.** The 192 roots at the 64 mixed charges fall into exactly **three cosets of E₈/(D₄ ⊕ D₄)**, of 64 each: (8_v,8_v) + (8_s,8_s) + (8_c,8_c).
* **Each charge.** Every mixed charge has its three roots in three different cosets (64/64).
* **The rotation.** The Eisenstein rotation, i.e. the Z₃ grading sl(9) / Λ³ / Λ³\*, cycles the three cosets.

> **D₄ triality is the Z₃ grading of the two-qutrit E₈.** It cycles the three faces of each Pauli charge: operator, three-fermion and three-hole.

E₈ ⊃ D₄ × D₄ with triality is classical. New here is its two-qutrit form: each D₄ is the centraliser of one qutrit's Pauli group, and the 45 tensor factorisations are 45 such dual pairs.

## 11688 — the magic gate is the E₈ |3|-grading element

| element | fixed subalgebra | eigenphase multiplicities (units of 2π/9) | fixed roots |
|---|---|---|---|
| Z ⊗ I | dim 86 | 0: 86, 3: 81, 6: 81 | E₆ (72) + A₂ (6) |
| **T ⊗ I**, T = diag(1, ζ₉, ζ₉⁻¹) | **dim 82** | 0: 82, ±1: 54, ±2: 27, ±3: 2 | **E₆ (72) + A₁ (2)**, plus a U(1) |

**The T gate.**
* It is exp(2πi·Y/9) with Y = diag(1, 1, −2) in the A₂ of its cube, since T³ = Z.
* It keeps E₆ and breaks SU(3)_p to SU(2) × U(1), so (27,3) → (27,2) ⊕ (27,1).
* The grading 82 + 54 + 27 + 2 is the E₈ |3|-grading already in PASS20260925 (Hesse striation clocks) and in Kraft–Regeta–Zimmermann.
* New here: the qutrit magic gate is that grading element, and its cube is the E₆ × A₂ element.

## 11689 — chirality is C × T

**The character.** Fix a point p and its matter shell (27,3)_p, the ω-eigenspace of Ad P. Take an extended-Clifford element g with g(p) = εp, and set τ = +1 if g is unitary and −1 if antiunitary.

| g | ε | τ | (27,3)_p |
|---|---|---|---|
| identity | +1 | unitary | preserved |
| F² on qutrit 1 (Pauli inversion) | −1 | unitary | **swapped** with (27̄,3̄) |
| complex conjugation K | −1 | antiunitary | preserved |
| F²K | +1 | antiunitary | **swapped** |

> **The chirality character is ε·τ.** Pauli inversion (C-like) and antiunitarity (T-like) each flip the matter chirality, and their product preserves it. This is the finite analogue of P = CT.

**Consequence for Pass 346.** Pass 346 found chirality "unselectable from inside" because the antiunitary controller swaps the two Weil halves. The structure is sharper:
* A Clifford-invariant time arrow (τ-odd, ε-even), such as h₆ of Passes 11419/11649, transforms by τ alone, so it **cannot** select chirality while C-type Cliffords are unbroken.
* Once a point p is chosen, the lowest-degree selector transforming as ε·τ is **Im⟨P⟩**: the population imbalance between the ω and ω² eigenspaces of that point's Pauli.

## 11690 — the Witting intertwiner

* **Codex's rays.** With symmetric Weyl operators D_v = τ^{x·z}XˣZᶻ, Codex's zero-character projectors (Pass 11663) have odd rank 1 and form a Witting configuration (overlaps {0, 1/3}).
* **The intertwiner.** The Clifford-equivariant intertwiner from that odd sector to the trivector Cartan is **antilinear**: no linear one exists. It is unique up to scale and unitary.
* **The result.** It maps **all 40 Codex rays exactly onto the 40 E₈ root rays**, relabelling points by the anti-symplectic swap (x, z) ↦ (z, x).
* **Consequence.** Codex's quartic Maschke-to-Burkhardt normal map has the **E₈ root directions** as its base locus.
* **Correction.** This corrects Pass 11681's "16/40", which used non-symmetric Paulis.

## 11691 — why two qutrits

**Closure.** sl(V) ⊕ Λ³V ⊕ Λ³V\* closes into a Z₃-graded Lie algebra only if the bracket Λ³V × Λ³V → Λ⁶V ≅ Λ^{n−6}V\* lands in Λ³V\*. That forces **n = 9: two qutrits.**

**Two independent singling-outs.** Together with Pass 11658 (tensor factorisations act as reflections of the Hesse space only at n = 2), two qutrits are singled out twice:
* once for the fermionic (E₈) side;
* once for the bosonic (Burkhardt) side.

## Prior art and scope

**Classical.**
* E₈ ⊃ sl(9), E₆ × A₂, A₂⁴, D₄ × D₄ with triality.
* The E₈ |3|-grading (Kraft–Regeta–Zimmermann).
* The Witting/Maschke/Burkhardt geometry.

**In the repo.** The 1 + 12 + 27 / E₆ × A₂ fibre picture (BT7175/7181), the Hesse-clock |3|-grading (PASS20260925), and Pass 346.

**New here.** All of the following on one explicit two-qutrit object, with exact checks:
* the centraliser dictionary;
* triality as the operator / three-fermion / three-hole grading;
* the T gate as the grading element;
* chirality as ε·τ and its order parameter Im⟨P⟩;
* the antilinear intertwiner with exact 40/40 match.

**Tested non-result.** The guess that the 8 cosets of a line's charge group are the 8 trifundamental 27s of A₂⁴ is false: the A₂⁴-irreducibles cut across the cosets. Only "line ↦ A₂⁴" is claimed.
