import Mathlib.Algebra.Ring.Defs

namespace W33.Pass7316

/-!
The scalar identity behind the Pass 7313--7316 `PSp`/`PCSp` scope repair.

If `N` has multiplier `mu` for a bilinear form and both arguments are
rescaled by `c`, the multiplier becomes `c*c*mu`.  In particular, an
antisymplectic map (multiplier `-1`) becomes symplectic precisely when the
chosen scalar satisfies `c^2 = -1`.  Over `F_q`, the existence of such a
scalar is the square-class boundary used by the exact GAP certificate.

The statement is deliberately carrier-agnostic.  `scale` and `form` are
required only to obey the displayed bilinear scaling law; no finite-field or
matrix implementation is smuggled into the theorem.
-/

variable {R V : Type*} [CommRing R]

/-- Rescaling both inputs of a similitude multiplies its form multiplier by
`c^2`. -/
theorem rescaled_multiplier
    (form : V → V → R) (scale : R → V → V) (N : V → V)
    (hscale : ∀ a b x y, form (scale a x) (scale b y) = (a * b) * form x y)
    (mu c : R) (hmul : ∀ x y, form (N x) (N y) = mu * form x y)
    (x y : V) :
    form (scale c (N x)) (scale c (N y)) = ((c * c) * mu) * form x y := by
  rw [hscale, hmul]
  exact (mul_assoc _ _ _).symm

/-- An antisymplectic map can be rescaled to a symplectic one when `-1` is a
square.  This is the exact algebraic distinction between the q=7 and q=9
projective-similitude witnesses in Pass 7313--7316. -/
theorem antisymplectic_rescale
    (form : V → V → R) (scale : R → V → V) (N : V → V)
    (hscale : ∀ a b x y, form (scale a x) (scale b y) = (a * b) * form x y)
    (c : R) (hc : c * c = -1)
    (hanti : ∀ x y, form (N x) (N y) = -form x y)
    (x y : V) :
    form (scale c (N x)) (scale c (N y)) = form x y := by
  rw [rescaled_multiplier form scale N hscale (-1) c (fun u v => by simpa using hanti u v)]
  rw [hc]
  simp

end W33.Pass7316
