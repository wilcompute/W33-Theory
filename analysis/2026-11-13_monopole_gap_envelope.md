# A continuous W33 adjoint scattering bound from the nonlinear checkpoints

The continuous coefficient interpolant of the W33 adjoint reflection loop has winding +3. A weighted multiple-shooting bound excludes outgoing zero-energy solutions between the nonlinear checkpoints and remains valid with a pointwise generator perturbation of 0.02 in the specified norm. This construction uses the finite-radius operator with the vacuum imposed at radius five. [Nonlinear phase checkpoints](2026-11-13_monopole_nonlinear_phase.md)

## Coefficient family

The exact constant fermion rephasing takes the explicit coupling to one and gives `R(φ)=exp(iφ) R_reduced(φ)`. In that reduced frame, the angular and mass terms are represented by the radial cubic spline coefficients constructed from the frozen profiles. The family contains the reference profile, all ten positive-phase profiles, and their conjugates. At every radius it allows the convex hull of these generators. In particular it allows linear interpolation in phase between consecutive profiles. At π the endpoint and its conjugate are averaged exactly to close the loop. The stored imaginary scalar entries at that endpoint have magnitude below 2×10⁻¹⁷. The additional perturbation must preserve the self-adjoint flux structure, the regular singular part, and the common vacuum exterior. [Fixed-profile rephasing](2026-11-13_monopole_adjoint_phase.md)

For vectors use the largest component norm, with each complex component measured by the sum of the absolute real and imaginary parts. The corresponding row-sum bound on a matrix is submultiplicative. The nominal generator is a real-form average of the zero and π endpoint generators. Negative-phase conjugation acts by complex conjugation and diagonal signs on this generator, which preserve the norm.

## The singular origin and the outgoing boundary

Near zero write the generator as `D/r+B(r)`, where D has four +1 and four −1 entries. Let C bound the norm of B on `[0,a]`. After dividing the unknown by r, its positive components u satisfy an ordinary integral equation run backward from u(a). Its negative components satisfy

```text
v(r) = r^(-2) integral_0^r s^2 [B(s)(u(s),v(s))]_negative ds.
```

The combined integral map has Lipschitz constant at most aC in the sup norm. For aC<1 it defines the unique regular space as a graph and gives `||v(a)|| ≤ aC/[3(1−aC)] ||u(a)||`. The code uses this graph bound in the first four rows of the matching problem.

At radius five the outgoing space consists of the three decaying heavy modes and the outgoing light mode. Its annihilator is computed by exact rational complex spectral projectors for the growing exterior modes, together with the incoming light projector. A localized zero mode lies in the outgoing space. Invertibility of the outgoing problem also gives the unique scattering solution for each specified incoming amplitude.

## Weighted multiple shooting

On interval i use a coordinate t from zero to one, logarithmic in the inner region and linear farther out. Let A_i(t) be the nominal generator in that coordinate, M_i bound its norm, and δ_i bound the deviation from it. Let T_i approximate the nominal transfer from t=0 to t=1 with defect τ_i. For any homogeneous outgoing solution define X as the maximum over intervals of `exp(−M_i t)||ψ(t)||`. Variation of constants gives

```text
||ψ(i+1) − T_i ψ(i)|| ≤ (exp(M_i) δ_i + τ_i) X
X ≤ max_i ||ψ(i)|| + max_i δ_i X.
```

Join the transfer rows and the eight boundary rows into a matrix B. Put the local bounds on their right-hand sides into a positive diagonal matrix W. If an approximate inverse X₀ satisfies

```text
ρ = ||W^(-1) B X₀ − I|| < 1,
q = ||X₀||/(1−ρ) + max_i δ_i < 1,
```

then the inverse residual bounds the nodal values and gives `X ≤ q X`. Thus the outgoing homogeneous problem has only the zero solution. The sparse factorization supplies the candidate X₀. The result depends on the checked residual rather than the factorization's conditioning estimate.

The code bounds the generator throughout each interval by polynomial translation and absolute coefficient sums. On logarithmic intervals it uses the atanh series with a geometric remainder. The reference transfers use 32 subintervals per cell, bounded constant-generator approximations, and degree-16 matrix exponential polynomials. The transfer error includes the Duhamel defect and the exponential remainder. Spline coefficients and candidate matrices are interpreted as stored binary64 numbers. The checker includes arithmetic allowances for the polynomial operations, matrix products and inverse residual sums. [Numerical gap lemma](https://arxiv.org/abs/0904.0268)

With the 0.02 allowance the following bounds hold over 931 radial cells.

| Representative channel | Inverse residual bound | Contraction bound |
| --- | ---: | ---: |
| Color | 2.59×10⁻⁷ | 0.88562 |
| Weak | 1.09×10⁻⁷ | 0.36951 |

The arithmetic allowances use the binary64 round-to-nearest model. Polynomial translation has degree at most four and uses absolute term majorants for both the candidate and nominal coefficients. The transfer polynomial and the 32-factor product are padded by 10⁻¹⁰ times their norm scale. The complex row-sum convention uses real additions and absolute values. The sparse inverse residual multiplies rows with at most nine entries and adds a bound of 256 machine epsilons times the corresponding absolute product before summation. The final sum padding also covers the accumulation over the roughly 7,500 columns.

## Winding consequence

The straight-line homotopy of reduced generators to the constant nominal profile stays in the certified bounds. Its reflection is continuous and unitary throughout, so its reduced winding is zero. Restoring the explicit coupling gives winding +1 in each of the two color partners and the weak channel. This yields total adjoint winding +3 for the continuous coefficient interpolant. A continuous nonlinear stationary branch inherits this conclusion once its between-checkpoint generators are shown to satisfy the envelope. The stationary branch validation and the infinite-domain tail remain separate calculations.

An independent nonlinear solve at φ=1.875 was kept outside the input hull. Its scaled stationarity residual is 2.64×10⁻⁷. Its radial generator lies within 0.002058 of the affine chord between 1.65 and 2.1 in the color block and within 0.000516 in the weak block. These bounds hold over the complete radius, including the origin cells, and both fit within the 0.02 allowance. Direct shooting on that profile gives matching singular values 0.550105 and 0.583652. This verifies one stationary between-checkpoint profile against the continuous scattering bound.

Run `python analysis/toe_20261113_monopole_gap_envelope.py --holdout`. To regenerate the midpoint, use the arithmetic mean of the packed nodal states at 1.65 and 2.1 as a same-grid seed for the nonlinear solver with `--elements 60 --angles 1.875 --seed-branch <seed-path>`. [Weighted bound fixture](../data/toe_20261113_monopole_gap_envelope.json) · [Independent midpoint profile](../data/toe_20261113_monopole_gap_holdout.json)
