import W33.Pass1063SignedLiftObstruction
import Mathlib.Tactic

/-!
# Pass 1074: normalized cocycles and the Schur central extension

A normalized `ZMod 2`-valued cocycle defines multiplication on `G × ZMod 2`.
The cocycle law is the associativity condition, the second factor is a central
kernel, and a multiplicative section is equivalent to a coboundary gauge.
-/

namespace W33.Pass1074

variable (G : Type*) [Group G]

structure NormalizedCocycle where
  c : G → G → ZMod 2
  one_left : ∀ g, c 1 g = 0
  one_right : ∀ g, c g 1 = 0
  cocycle : ∀ g h k, c g h + c (g * h) k = c h k + c g (h * k)

abbrev Extension := G × ZMod 2

def extensionMul (c : NormalizedCocycle G)
    (x y : Extension G) : Extension G :=
  (x.1 * y.1, x.2 + y.2 + c.c x.1 y.1)

theorem extensionMul_assoc (c : NormalizedCocycle G)
    (x y z : Extension G) :
    extensionMul G c (extensionMul G c x y) z =
      extensionMul G c x (extensionMul G c y z) := by
  rcases x with ⟨g, a⟩
  rcases y with ⟨h, b⟩
  rcases z with ⟨k, d⟩
  apply Prod.ext
  · simp [extensionMul, mul_assoc]
  · simp only [extensionMul, Prod.fst, Prod.snd]
    rw [c.cocycle g h k]
    abel

theorem extensionMul_one (c : NormalizedCocycle G) (x : Extension G) :
    extensionMul G c x (1, 0) = x := by
  rcases x with ⟨g, a⟩
  simp [extensionMul, c.one_right]

theorem one_extensionMul (c : NormalizedCocycle G) (x : Extension G) :
    extensionMul G c (1, 0) x = x := by
  rcases x with ⟨g, a⟩
  simp [extensionMul, c.one_left]

def kernel (a : ZMod 2) : Extension G := (1, a)

theorem kernel_central (c : NormalizedCocycle G)
    (a : ZMod 2) (x : Extension G) :
    extensionMul G c (kernel G a) x = extensionMul G c x (kernel G a) := by
  rcases x with ⟨g, b⟩
  simp [extensionMul, kernel, c.one_left, c.one_right, add_comm]

theorem projection_mul (c : NormalizedCocycle G)
    (x y : Extension G) :
    (extensionMul G c x y).1 = x.1 * y.1 := rfl

def section (b : G → ZMod 2) (g : G) : Extension G := (g, b g)

theorem section_mul_iff (c : NormalizedCocycle G) (b : G → ZMod 2)
    (g h : G) :
    extensionMul G c (section G b g) (section G b h) = section G b (g * h) ↔
      b g + b h + c.c g h = b (g * h) := by
  simp [extensionMul, section]

theorem w33SignedSectionObstruction
    (s0 s1 s48 s49 s50 s60 : ZMod 2)
    (h1 : s0 + s1 + s49 + s50 = 0)
    (h2 : s0 + s1 + s48 + s50 = 0)
    (h3 : s0 + s49 + s50 + s60 = 1)
    (h4 : s0 + s48 + s50 + s60 = 0) : False :=
  W33.Pass1063.signedLiftFourRowObstruction s0 s1 s48 s49 s50 s60 h1 h2 h3 h4

end W33.Pass1074
