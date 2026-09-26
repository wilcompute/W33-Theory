# Pass 10959 — one Albert 16 cannot carry the full clock; the minimal completion is 32

Producer: `analysis/w33_pass10959_albert_clock_extension_obstruction.py`

GAP cross-check: `analysis/w33_pass10959_gl23_character_restriction.g`

Certificates:

- `data/w33_pass10959_albert_clock_extension_obstruction.json`
- `data/w33_pass10959_doubled_albert_gl23_intertwiner.json`

Regression: `tests/test_w33_pass10959_albert_clock_extension_obstruction.py`

## 1. The question after Pass 10958

Pass 10958 embedded the missing two-mode clock module
[
A_2=operatorname{diag}(i,-i)
]
exactly into the Albert Peirce 16, and proved the full Peirce 16 is eight copies of that (C_4) module.

The next question is stricter: can one choose a (mu_8) phase for the exact Albert half-turn (U) so that it becomes the frozen order-eight generator (g) of a full complex (GL(2,3)) representation?
The required clock relations are
[
g^4=-I,qquad g^8=I.
]
Since (U^2=-I), the admissible phase lifts are odd eighth-root multiples of (U). Up to conjugation there are only two distinct C8 spectra:
```text
zeta8^-1 U : k={1,5}, each multiplicity 8,
zeta8    U : k={3,7}, each multiplicity 8.
```

## 2. Exact GL(2,3) character restriction

GAP computes all eight irreducible complex characters of (GL(2,3)), with degrees
```text
1,1,2,2,2,3,3,4.
```

Exactly three have the central element (-I) acting as scalar (-1). Their restrictions to the frozen (C_8=langle gangle) have Fourier exponents
```text
2D : {1,3}
2D : {5,7}
4D : {1,3,5,7}.
```
Therefore **every** complex representation on which the center acts as (-I) satisfies the restriction law
[
m_1=m_3,qquad m_5=m_7,
]
where (m_k) is the multiplicity of the (C_8) character (gmapstozeta_8^k).

This is a representation-ring statement, not an approximation.

## 3. The 16-dimensional extension is impossible

The producer exhausts all 25 central-odd degree-16 combinations of those three irreducibles.

The two Albert phase-lift spectra are
[
(8,0,8,0)
]
and
[
(0,8,0,8)
]
on exponents (1,3,5,7), respectively.

Both violate the exact equalities (m_1=m_3) and (m_5=m_7).

Hence:

> There is no complex-linear 16-dimensional representation of (GL(2,3)) that sends the central (-I) to (-I_{16}) and sends the frozen clock generator to any admissible (mu_8) phase lift of the exact Albert half-turn.
This is a genuine no-go for the single Peirce-16 carrier under those conditions.

## 4. The minimal completion is forced to 32 dimensions

To repair either Albert spectrum, the missing crossed characters must be added:
```text
{1,5}^8 requires {3,7}^8,
{3,7}^8 requires {1,5}^8.
```

The resulting 32-dimensional spectrum has
[
m_1=m_3=m_5=m_7=8.
]

An exhaustive degree search proves 32 is minimal.

This spectrum is exactly the restriction of eight copies of the faithful four-dimensional signed (D_4) representation constructed in Pass 10955.

Thus the minimal full-clock carrier is
[
16oplus16,
]
with the two Albert copies carrying conjugate (mu_8) phase lifts.
## 5. Explicit 32-dimensional GL(2,3) action

Let
[
G_A=operatorname{diag}(zeta_8^{-1}U,;zeta_8U)
]
on the doubled Albert carrier.

Let (R_4) be the faithful Pass-10955 signed (D_4) representation of (GL(2,3)), and let
[
R_{32}=R_4^{oplus8}.
]

The producer constructs exact C8 eigenbases on both sides over
[
mathbb Q(zeta_8)=mathbb Q(i,sqrt2)
]
and obtains an invertible (32	imes32) matrix (J) satisfying
[
G_AJ=J,R_{32}(g).
]

Its rank is 32, and the frozen certificate stores the complete exact matrix plus SHA-256 digest.
Transport the full group action by
[
ho_A(h)=J,R_{32}(h),J^{-1}.
]

Because (R_{32}) is already a faithful objectwise representation, this gives an exact faithful (GL(2,3)) representation on the doubled Albert vector space. The center acts as (-I_{32}).

This closes the finite complex-representation problem: **one Albert 16 cannot extend; two conjugate Albert 16s can, and 32 is minimal.**

## 6. Relation to the familiar 32 = 16 + 16 pattern

Standard Spin(10) representation theory also has a 32-dimensional Dirac spinor decomposing into two 16-dimensional Weyl spinors. That makes the forced (16+16) completion structurally suggestive.

It is **not** an identification made by this pass. The new 32D action is obtained by transporting a finite (GL(2,3)) representation. We have not proved that it lies inside Spin(10), inside Spin(9), preserves an Albert/Clifford product, or identifies the two 16s with physical particle/antiparticle or left/right sectors.

The resemblance is now a sharp target for a future intertwiner test rather than a numerical coincidence to promote by inspection.
## Boundary

This is an exact finite complex-representation theorem. The 16D no-go assumes:

- the central clock sign acts as (-I);
- the frozen generator is represented by an admissible (mu_8) phase lift of the exact Albert half-turn;
- the representation is complex-linear.

The theorem does not exclude larger, projective, semilinear, realified, or different physical clock realizations. The transported 32D representation is not yet shown to be a subgroup action inside Spin(9) or Spin(10), nor to preserve the Albert Jordan product.
