import Mathlib

namespace W33.Pass481

/-!
The algebraic heart of Pass 481's first-order determinant law
`v_λ(T₁) = (q-1) + v_λ(S) ≥ q+1`.  The `(q-1)` is the ramification of `q` in
`ℤ[ζ_q]` (a standard Mathlib fact about cyclotomic fields); the `+2` is the
inverse-closure pairing identity formalized here: for any root of unity `ζ`
and any element `w = ζ^{tc}`, the paired contribution
`w + w⁻¹ - 2` factors as `-(1 - w)(1 - w⁻¹)`, a product of two elements each
divisible by `λ = 1 - ζ`, hence of `λ`-valuation `≥ 2`.

We prove the ring identity generically in any commutative ring for a unit `w`
(so `w⁻¹` makes sense), which is exactly the shape used at `w = ζ^{tc}`.
-/

variable {R : Type*} [CommRing R]

/-- The inverse-closure pairing identity: `w + w⁻¹ - 2 = -(1-w)(1-w⁻¹)`.
Stated for a unit `w` via its inverse `wi` with `w * wi = 1`. -/
theorem pairing_factor (w wi : R) (h : w * wi = 1) :
    w + wi - 2 = -((1 - w) * (1 - wi)) := by
  have : (1 - w) * (1 - wi) = 1 - w - wi + w * wi := by ring
  rw [this, h]; ring

/-- Each factor `1 - w` and `1 - wi` is a multiple of `λ = 1 - ζ` when `w`
is a power of `ζ`; abstractly, if `λ ∣ (1 - w)` and `λ ∣ (1 - wi)` then
`λ^2 ∣ (w + wi - 2)`.  This is the "+2" order of vanishing. -/
theorem pairing_lambda_sq (lam w wi : R) (h : w * wi = 1)
    (hw : lam ∣ (1 - w)) (hwi : lam ∣ (1 - wi)) :
    lam ^ 2 ∣ (w + wi - 2) := by
  rw [pairing_factor w wi h]
  obtain ⟨a, ha⟩ := hw
  obtain ⟨b, hb⟩ := hwi
  refine ⟨-(a * b), ?_⟩
  rw [ha, hb]; ring

end W33.Pass481
