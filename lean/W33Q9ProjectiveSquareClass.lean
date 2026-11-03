/-
Formal finite GF(9) arithmetic and multiplicative square-class gates.
Represent x=a+b*i over F3, i*i=-1; x is encoded a+3*b.
Finite exhaustive proofs use Lean's kernel, no sorry, no axioms.
This is an independent prerequisite for the q9 projective triple classifier;
Witt extension/transitivity and orbit-average transfer are not proved here.
-/
import Std

namespace W33Q9Field

abbrev F9 := Fin 9

def enc (a b : Nat) : F9 :=
  ⟨(a % 3 + 3 * (b % 3)) % 9, Nat.mod_lt _ (by decide)⟩

def add (x y : F9) : F9 :=
  enc (x.val % 3 + y.val % 3) (x.val / 3 + y.val / 3)

def neg (x : F9) : F9 :=
  enc (3 - x.val % 3) (3 - x.val / 3)

def mul (x y : F9) : F9 :=
  enc (x.val % 3 * (y.val % 3) + 2 * (x.val / 3) * (y.val / 3))
    (x.val % 3 * (y.val / 3) + x.val / 3 * (y.val % 3))

theorem i_squared_minus_one : mul (3 : F9) (3 : F9) = (2 : F9) := by decide
theorem one_times : ∀ x : F9, mul (1 : F9) x = x := by decide
theorem mul_comm : ∀ x y : F9, mul x y = mul y x := by decide
theorem mul_assoc : ∀ x y z : F9, mul (mul x y) z = mul x (mul y z) := by decide
theorem add_assoc : ∀ x y z : F9, add (add x y) z = add x (add y z) := by decide
theorem add_comm : ∀ x y : F9, add x y = add y x := by decide
theorem add_zero : ∀ x : F9, add x (0 : F9) = x := by decide
theorem add_neg : ∀ x : F9, add x (neg x) = (0 : F9) := by decide
theorem distrib : ∀ x y z : F9,
    mul x (add y z) = add (mul x y) (mul x z) := by decide
theorem nonzero_has_inverse :
    ∀ x : F9, x ≠ (0 : F9) → ∃ y : F9, mul x y = (1 : F9) := by decide

-- Completely explicit bounded finite enumeration of nonzero squares.
def sqb (x : F9) : Bool :=
  ((mul 1 1) == x) || ((mul 2 2) == x) ||
  ((mul 3 3) == x) || ((mul 4 4) == x) ||
  ((mul 5 5) == x) || ((mul 6 6) == x) ||
  ((mul 7 7) == x) || ((mul 8 8) == x)

theorem four_nonzero_squares :
    ∀ x : F9, sqb x = true ↔
      (x = (1 : F9) ∨ x = (2 : F9) ∨ x = (3 : F9) ∨ x = (6 : F9)) := by decide

theorem projective_square_class_well_defined :
    ∀ x r : F9, r ≠ (0 : F9) →
      sqb x = sqb (mul (mul r r) x) := by decide

-- Triple-product scale invariance follows from this square-class lemma and
-- commutativity, distributivity and associativity proved above.

end W33Q9Field
