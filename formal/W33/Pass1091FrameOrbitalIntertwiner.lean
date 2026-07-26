import Mathlib.Data.Fin.VecNotation
import Mathlib.LinearAlgebra.Matrix

/-!
# Pass 1091: frame-orbital transpose and intertwiner regression lock

The finite maps below are copied from the exact Pass-1082 certificate. The
`native_decide` theorems lock the corrected pairing counts. The generic matrix
lemmas record the algebraic meaning of the Pass-1083/1087 identities.
-/

namespace W33.Pass1091

def innerTranspose : Fin 32 → Fin 32 :=
  ![0, 1, 3, 2, 4, 5, 7, 6, 8, 9, 15, 13, 12, 11, 14, 10,
    17, 16, 18, 19, 20, 22, 21, 25, 26, 23, 24, 28, 27, 30, 29, 31]

def outerFusion : Fin 32 → Fin 32 :=
  ![0, 1, 3, 2, 4, 5, 7, 6, 8, 9, 11, 10, 14, 15, 12, 13,
    16, 17, 19, 18, 20, 22, 21, 23, 28, 25, 27, 26, 24, 30, 29, 31]

def outerTranspose : Fin 22 → Fin 22 :=
  ![0, 1, 2, 3, 4, 5, 6, 7, 10, 9, 8, 12, 11, 13, 14, 15,
    18, 19, 16, 17, 20, 21]

def innerSelfPaired : Finset (Fin 32) :=
  Finset.univ.filter fun i => innerTranspose i = i

def innerNonSelfPaired : Finset (Fin 32) :=
  Finset.univ.filter fun i => innerTranspose i ≠ i

def outerSelfPaired : Finset (Fin 22) :=
  Finset.univ.filter fun i => outerTranspose i = i

def fusionFixed : Finset (Fin 32) :=
  Finset.univ.filter fun i => outerFusion i = i

theorem innerTranspose_involutive : Function.Involutive innerTranspose := by
  native_decide

theorem innerSelfPaired_card : innerSelfPaired.card = 12 := by
  native_decide

theorem innerNonSelfPaired_card : innerNonSelfPaired.card = 20 := by
  native_decide

theorem innerTransposePair_card : innerNonSelfPaired.card / 2 = 10 := by
  native_decide

theorem outerFusion_involutive : Function.Involutive outerFusion := by
  native_decide

theorem outerFusionOrbit_card : fusionFixed.card + (32 - fusionFixed.card) / 2 = 22 := by
  native_decide

theorem outerTranspose_involutive : Function.Involutive outerTranspose := by
  native_decide

theorem outerSelfPaired_card : outerSelfPaired.card = 14 := by
  native_decide

/-- A column of `T` belongs to the left kernel of `B` whenever `B*T=0`. -/
theorem column_mem_leftKernel
    {m n k : Nat}
    (B : Matrix (Fin m) (Fin n) ℤ)
    (T : Matrix (Fin n) (Fin k) ℤ)
    (h : B * T = 0) (j : Fin k) :
    B.mulVec (fun i => T i j) = 0 := by
  funext i
  have hij := congrArg (fun M => M i j) h
  simpa [Matrix.mul_apply, Matrix.mulVec] using hij

/-- The projector relation `T*K=cT` is valid on every matrix entry. -/
theorem cycleEigen_entry
    {n k : Nat}
    (T : Matrix (Fin n) (Fin k) ℤ)
    (K : Matrix (Fin k) (Fin k) ℤ)
    (c : ℤ) (h : T * K = c • T) (i : Fin n) (j : Fin k) :
    (T * K) i j = c * T i j := by
  have hij := congrArg (fun M => M i j) h
  simpa using hij

def plusTensorSha256 : String :=
  "1455f33e219d8464a7fac74ca693f31dfa1cf01548c205c7fa246a4802132213"

def minusTensorSha256 : String :=
  "66476d71e75e52b3e06c3ed4b5594e63a095681d14cd3847d88f334fe225b052"

end W33.Pass1091
