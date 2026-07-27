import Mathlib

namespace W33.Pass533

/-!
Reality of the characteristic polynomial of a Hermitian matrix.

Pass 491 proved that `det D` lies in the real subring `ℤ[ζ_p]⁺`, from `D` being
Hermitian, and formalised that case.  Pass 533 derived the Hermitian property
itself from inverse closure `c (-v) = -c v`, and Passes 531–532 observed that
the *same* hypothesis gives every coefficient of the characteristic polynomial,
not only the top one.  This file records the general step.

The mathematical content is small and worth stating plainly: a self-adjoint
matrix has self-adjoint principal minors, and the elementary symmetric
functions of its eigenvalues are sums of those minors.  So every coefficient of
the characteristic polynomial is fixed by `star`.  Over `ℤ[ζ_p]` with `star` the
Galois element `σ₋₁`, "fixed by star" is exactly "lies in `ℤ[ζ_p]⁺`", and at
`p = 3` — where the real subring has degree `(p-1)/2 = 1` over `ℚ` — that reads
"is a rational integer", which is the integrality observed at `q = 3`.

Two lemmas are proved here outright.  The passage from minors to the
characteristic polynomial is stated with the sum-of-principal-minors expansion
as an explicit hypothesis, in the same style as the other modules of this arc:
the arithmetic is checked exactly by the Python witnesses, and what is
formalised is the manipulation that carries it.
-/

open Matrix

variable {n m R : Type*} [Fintype n] [DecidableEq n] [CommRing R] [StarRing R]

/-- **The determinant of a Hermitian matrix is self-adjoint.**  This is Pass
491's statement, re-proved from the Hermitian hypothesis alone. -/
theorem det_isSelfAdjoint_of_isHermitian {M : Matrix n n R} (h : M.IsHermitian) :
    star M.det = M.det := by
  rw [← Matrix.det_conjTranspose, h]

omit [Fintype n] [DecidableEq n] in
/-- **A principal submatrix of a Hermitian matrix is Hermitian.**  Taking the
same index map on rows and columns is what makes this work; a general submatrix
of a Hermitian matrix need not be Hermitian. -/
theorem isHermitian_submatrix {M : Matrix n n R} (h : M.IsHermitian)
    [Fintype m] [DecidableEq m] (f : m → n) :
    (M.submatrix f f).IsHermitian := by
  unfold Matrix.IsHermitian at *
  rw [Matrix.conjTranspose_submatrix, h]

omit [Fintype n] [DecidableEq n] in
/-- Hence every principal minor of a Hermitian matrix is self-adjoint. -/
theorem principal_minor_isSelfAdjoint {M : Matrix n n R} (h : M.IsHermitian)
    [Fintype m] [DecidableEq m] (f : m → n) :
    star (M.submatrix f f).det = (M.submatrix f f).det :=
  det_isSelfAdjoint_of_isHermitian (isHermitian_submatrix h f)

omit [Fintype n] [DecidableEq n] in
/-- **The characteristic polynomial is self-adjoint coefficientwise.**  Given
the expansion of a coefficient as a sum of principal minors — supplied here as
the hypothesis `hexp`, since that expansion is the arithmetic input — every
coefficient of a Hermitian matrix's characteristic polynomial is fixed by
`star`. -/
theorem coeff_isSelfAdjoint_of_isHermitian
    {M : Matrix n n R} (h : M.IsHermitian)
    [Fintype m] [DecidableEq m]
    (s : Finset m) (f : m → m → n) (c : R)
    (hexp : c = ∑ i ∈ s, (M.submatrix (f i) (f i)).det) :
    star c = c := by
  subst hexp
  rw [star_sum]
  exact Finset.sum_congr rfl fun i _ =>
    principal_minor_isSelfAdjoint h (f i)

/-!
### Scope

`hexp` — that the coefficient is a sum of principal minors — is assumed, not
derived; it is the standard expansion of the elementary symmetric functions and
is the arithmetic input here.  Everything else is proved: self-adjointness of
determinants of Hermitian matrices, the fact that principal submatrices inherit
the Hermitian property, and the passage through a finite sum.

The Hermitian hypothesis itself is not free.  It is derived in
`analysis/w33_pass533_hermitian_derived.py` from inverse closure, via the entry
formula `D[i][j] = ∑_b d_{(a,b)} ζ^{2jb+ab}` with `a = i - j` and the identity
`2b(j - i + a) = 0`; and the reality of the coefficients is measured there and
in Pass 531 across 72 sections at `p = 3, 5, 7`.
-/

end W33.Pass533
