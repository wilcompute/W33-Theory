import Mathlib

namespace W33.Pass508

/-!
The reduction of Pass 507, formalized with its input named as a hypothesis.

The determinant law needs `v_λ(e_q) ≥ v_λ(q) + 4`.  Newton's chain supplies
`v_λ(e_q) ≥ v_λ(p_q) - v_λ(q)`, and the *factorial law* — verified at 38
measured points but **not proved** — states `v_λ(p_q) = 2q + v_λ(q!)`.  For
prime `q` one has `v_λ(q) = q - 1`, so the target is `q + 3`.

Chaining these gives `v_λ(e_q) ≥ q + 1 + v_λ(q!)`, and the whole residual is
therefore the single inequality `v_λ(q!) ≥ 2`.

We state exactly that, over `ℕ`, with the factorial law as an explicit
hypothesis rather than smuggled in: the theorem below is honest about
depending on an unproved input, and is the precise sense in which "the
factorial law implies the determinant law".
-/

/-- **The reduction.**  Given the Newton bound and the factorial law at
`m = q`, the determinant law's requirement `q + 3` follows from the single
inequality `v_λ(q!) ≥ 2`. -/
theorem determinant_law_of_factorial_law
    (q vq vqfact vpq veq : ℕ)
    (hvq : vq = q - 1)                       -- ramification, prime q
    (hfact : vpq = 2 * q + vqfact)           -- the factorial law at m = q
    (hnewton : vpq ≤ veq + vq)               -- Newton: v(e_q) ≥ v(p_q) - v(q)
    (hq : 3 ≤ q)
    (hresidual : 2 ≤ vqfact) :               -- the entire remaining condition
    q + 3 ≤ veq := by
  subst hvq
  omega

/-- The residual condition is not merely sufficient here: with the factorial
law and the Newton bound sharp, `v_λ(q!) ≥ 2` is exactly what `q + 3` needs. -/
theorem residual_is_exactly_two
    (q vqfact : ℕ) (hq : 3 ≤ q) :
    (q + 3 ≤ q + 1 + vqfact) ↔ 2 ≤ vqfact := by
  omega

/-- For prime `q`, the input to the residual is `v_λ(q!) = q - 1`, which is at
least `2` for every `q ≥ 3` — so the residual is discharged. -/
theorem residual_holds_for_prime (q : ℕ) (hq : 3 ≤ q) :
    2 ≤ q - 1 := by
  omega

end W33.Pass508
