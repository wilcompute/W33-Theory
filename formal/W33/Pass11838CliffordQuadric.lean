import Mathlib

namespace W33.Pass11838

/-!
Pass 11838: the Clifford quadric of two qutrits (Passes 11831-11833).

The Pauli phase space `V = F₃⁴` carries `ω(u,v) = uᵀ Ω v` with `Ω = [[0, I], [-I, 0]]`.  An `ω`-traceless bivector is
`(a, b, c, d, e)`; its operator `J = Ω⁻¹B` is the matrix `J a b c d e` below, and

* `J² = Q · 1` with `Q = a e + b² + c d` (Clifford relation), polarised to `J x J y + J y J x = (Q(x+y) - Q x - Q y) · 1`;
* `J` is `ω`-self-adjoint, `Jᵀ Ω = Ω J`, hence `Jᵀ Ω J = Q · Ω`: for `Q = 1` it is a symplectic involution (a tensor
  factorisation), for `Q = -1` an anti-symplectic map with `J² = -1` (a Kramers time reversal), for `Q = 0` nilpotent
  (a Lagrangian measurement context);
* over `ZMod 3` the `242` nonzero bivectors split `80 + 90 + 72` by `Q = 0, 1, 2`, i.e. `40 + 45 + 36` projective
  points: contexts, splits and Kramers reversals.

All identities hold over every commutative ring.
-/

variable {R : Type*} [CommRing R]

/-- `Ω = [[0, I], [-I, 0]]`. -/
def Ω : Matrix (Fin 4) (Fin 4) R :=
  !![0, 0, 1, 0; 0, 0, 0, 1; -1, 0, 0, 0; 0, -1, 0, 0]

/-- The `ω`-self-adjoint operator of the traceless bivector `(a, b, c, d, e)`. -/
def J (a b c d e : R) : Matrix (Fin 4) (Fin 4) R :=
  !![b, d, 0, -e; c, -b, e, 0; 0, a, b, c; -a, 0, d, -b]

/-- The quadratic form of the five-dimensional bivector space. -/
def Q (a b c d e : R) : R := a * e + b ^ 2 + c * d

theorem J_trace (a b c d e : R) : (J a b c d e).trace = 0 := by
  simp [J, Matrix.trace, Fin.sum_univ_four]

/-- Clifford relation: `J² = Q · 1`. -/
theorem J_sq (a b c d e : R) :
    J a b c d e * J a b c d e = Q a b c d e • (1 : Matrix (Fin 4) (Fin 4) R) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [J, Q, Matrix.mul_apply, Fin.sum_univ_four] <;> ring

/-- Polarised Clifford relation: orthogonal bivectors give anticommuting operators. -/
theorem J_anticomm (a b c d e a' b' c' d' e' : R) :
    J a b c d e * J a' b' c' d' e' + J a' b' c' d' e' * J a b c d e =
      (Q (a + a') (b + b') (c + c') (d + d') (e + e') - Q a b c d e - Q a' b' c' d' e') •
        (1 : Matrix (Fin 4) (Fin 4) R) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [J, Q] <;> ring

/-- `J` is self-adjoint for `ω`. -/
theorem J_selfadjoint (a b c d e : R) : (J a b c d e).transpose * Ω = Ω * J a b c d e := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [J, Ω, Matrix.mul_apply, Fin.sum_univ_four, Matrix.transpose_apply]

/-- `Jᵀ Ω J = Q Ω`: symplectic for `Q = 1`, anti-symplectic for `Q = -1`. -/
theorem J_similitude (a b c d e : R) :
    (J a b c d e).transpose * Ω * J a b c d e = Q a b c d e • (Ω : Matrix (Fin 4) (Fin 4) R) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [J, Q, Ω, Matrix.mul_apply, Fin.sum_univ_four, Matrix.transpose_apply] <;> ring

/-- A Kramers point (`Q = -1`) gives an anti-symplectic `J` with `J² = -1`. -/
theorem kramers (a b c d e : R) (h : Q a b c d e = -1) :
    J a b c d e * J a b c d e = -1 ∧
      (J a b c d e).transpose * Ω * J a b c d e = -(Ω : Matrix (Fin 4) (Fin 4) R) := by
  refine ⟨?_, ?_⟩
  · rw [J_sq, h, neg_one_smul]
  · rw [J_similitude, h, neg_one_smul]

/-- The quadric over `ZMod 3`, on the five coordinates. -/
def Q3 (v : ZMod 3 × ZMod 3 × ZMod 3 × ZMod 3 × ZMod 3) : ZMod 3 :=
  Q v.1 v.2.1 v.2.2.1 v.2.2.2.1 v.2.2.2.2

/-- `242 = 80 + 90 + 72` nonzero bivectors by `Q = 0, 1, 2`: `40` contexts, `45` splits, `36` Kramers reversals. -/
theorem counts :
    (Finset.univ.filter (fun v => v ≠ 0 ∧ Q3 v = 0)).card = 80 ∧
      (Finset.univ.filter (fun v => Q3 v = 1)).card = 90 ∧
      (Finset.univ.filter (fun v => Q3 v = 2)).card = 72 := by
  decide

theorem projective_counts : 80 / 2 = 40 ∧ 90 / 2 = 45 ∧ 72 / 2 = 36 ∧ 40 + 45 + 36 = 121 := by
  decide

end W33.Pass11838
