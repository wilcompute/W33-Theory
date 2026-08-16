import Mathlib.Tactic

/-!
# The cosine sequence of a strongly regular graph (arithmetic layer)

This file formalizes ONLY the arithmetic of the cosine sequence used in Passes
5278–5419.  It does not define a graph, an adjacency matrix, an eigenspace, or a
Gram matrix: the geometric content is a separate, machine-verified statement (see
`analysis/w33_pass5412_5415_the_cosine_sequence_was_always_classical.py`).  What IS
formalized here is the three-term recurrence, its closed form at `i = 1`, and the
specialization that collapses it on a generalized quadrangle.

Following every other module in `formal/W33`, the scope is stated in the negative and
the geometry remains an external input.

The mathematics is classical (Brouwer–Cohen–Neumaier, Godsil); Pass 5412 established
that the repository had re-derived it.  Nothing here is claimed as new.
-/

namespace W33.CosineSequence

/-- Parameters of a strongly regular graph, as rationals, with the positivity we
actually use.  `k` is the valency, `lam` and `mu` the usual intersection numbers, and
`s` the least eigenvalue (negative). -/
structure Params where
  k : ℚ
  lam : ℚ
  mu : ℚ
  s : ℚ
  k_pos : 0 < k
  s_neg : s < 0
  one_add_s_ne : 1 + s ≠ 0
  b1_ne : k - lam - 1 ≠ 0

variable (P : Params)

/-- `w₁ = θ/k`, the first cosine, for an eigenvalue `θ`. -/
noncomputable def w1 (θ : ℚ) : ℚ := θ / P.k

/-- `w₂` from the three-term recurrence `θ·w₁ = c₁·w₀ + a₁·w₁ + b₁·w₂` with
`w₀ = 1`, `c₁ = 1`, `a₁ = lam`, `b₁ = k - lam - 1`. -/
noncomputable def w2 (θ : ℚ) : ℚ := (θ ^ 2 - P.k - P.lam * θ) / (P.k * (P.k - P.lam - 1))

/-- The recurrence is satisfied by construction: this is the statement that `w2` is
the unique solution of `θ·w₁ = 1 + lam·w₁ + (k - lam - 1)·w₂`. -/
theorem recurrence (θ : ℚ) :
    θ * w1 P θ = 1 + P.lam * w1 P θ + (P.k - P.lam - 1) * w2 P θ := by
  have hk : P.k ≠ 0 := ne_of_gt P.k_pos
  have hb : P.k - P.lam - 1 ≠ 0 := P.b1_ne
  unfold w1 w2
  field_simp
  ring

/-- The alternative closed form `μ / (k(1+s))` agrees with the recurrence value at the
eigenvalue `θ`, given the two strongly regular identities relating `μ`, `lam`, `θ` and `s`.

Stated over bare rationals rather than through `Params`: `subst` cannot act on a structure
projection like `P.lam`, and the arithmetic is what is being formalized, not the packaging.
This is the content behind Pass 5374's `mu/(k(1+s))` — which Pass 5412 then established is
the classical cosine sequence, so nothing here is new. -/
theorem mu_form (k lam mu θ s : ℚ) (hk : k ≠ 0) (hs : 1 + s ≠ 0)
    (hb : k - lam - 1 ≠ 0)
    (hmu : mu = k + θ * s) (hlam : lam = mu + θ + s) :
    (θ ^ 2 - k - lam * θ) / (k * (k - lam - 1)) = mu / (k * (1 + s)) := by
  subst hlam
  subst hmu
  rw [div_eq_div_iff (by simpa using mul_ne_zero hk hb) (mul_ne_zero hk hs)]
  ring

/-- The `Params`-level corollary, for callers that carry the structure. -/
theorem w2_eq_mu_form (θ : ℚ)
    (hmu : P.mu = P.k + θ * P.s) (hlam : P.lam = P.mu + θ + P.s) :
    w2 P θ = P.mu / (P.k * (1 + P.s)) :=
  mu_form P.k P.lam P.mu θ P.s (ne_of_gt P.k_pos) P.one_add_s_ne P.b1_ne hmu hlam

/-- On a generalized quadrangle of order `(a, t)` the least eigenvalue is `s = -(t+1)`,
the valency is `k = a(t+1)` and `μ = t+1`, so the second cosine collapses to `-1/(a·t)`.
Since the Hoffman bound of such a quadrangle is `a·t + 1`, this is `-1/(H-1)`.

This is the specialization that made `-1/q²` (on `a = t = q`) and `-1/(H-1)` look like
general laws when they are properties of this family. -/
theorem gq_collapse (a t : ℚ) (ha : 0 < a) (ht : 0 < t) :
    (t + 1) / (a * (t + 1) * (1 + -(t + 1))) = -1 / (a * t) := by
  have ha' : a ≠ 0 := ne_of_gt ha
  have ht' : t ≠ 0 := ne_of_gt ht
  have h1 : t + 1 ≠ 0 := by positivity
  rw [show (1 : ℚ) + -(t + 1) = -t by ring]
  rw [div_eq_div_iff (by simp [ha', ht', h1]) (by simp [ha', ht'])]
  ring

/-- And on `W(3,q)`, where `a = t = q`, the same expression is `-1/q²`. -/
theorem w3q_collapse (q : ℚ) :
    (-1 : ℚ) / (q * q) = -1 / q ^ 2 := by
  ring

end W33.CosineSequence
