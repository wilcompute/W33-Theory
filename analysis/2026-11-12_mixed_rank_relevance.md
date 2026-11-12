# Flavor-current positivity blocks a direct ultraviolet increase of the W33 mixed-coupling rank

At a unitary four-dimensional N=1 fixed point with the canonical W33 fields and interacting E6 gauge dynamics, a rank-zero or rank-one mixed adjoint coupling cannot acquire the missing rank through a relevant perturbation by that same cubic tensor. This applies with the signed alternating cubic present or absent, and with the family gauge coupling active or zero. It complements the previous obstruction at rank two with both gauge factors active. The calculation assumes the stated superpotential support and allows the usual accidental symmetries from free chiral operators. An emergent interacting sector with extra R-current mixing requires a separate analysis. [Rank-two calculation](2026-11-12_canonical_uv_fixed_point.md)

## An exact inequality that survives free chiral fields

For any nonzero conserved flavor generator F, the positive two-point coefficient is proportional to `−Tr R F²`, with R the superconformal Weyl charge. In the elementary description the anomaly is `Σ dim(i)(R_i−1) F_i²`, with R_i the scalar charge. If a chiral operator O becomes free because its trial charge lies below 2/3, the correction to this anomaly is `(2/3−R_O) Tr_O F² ≥ 0`. Therefore every microscopic trace used below must itself be strictly negative. This necessary condition avoids a chiral-ring census. The currents in the table preserve the active cubic terms and have zero mixed anomaly with both gauge factors, so they are available even when the family factor is gauged. [Current positivity and a-maximization](https://arxiv.org/abs/hep-th/0304128) · [Free-field correction](https://arxiv.org/abs/hep-th/0308071)

Use one coupled pair `X_c,Z_c` in the rank-one case and write X_u and Z_u for uncoupled species. Let `r=R(A)`, `q=R(X_c)`, and `u=R(X_u)`. The unpaired X doublet has a common charge by its unbroken SU(2) symmetry. At rank zero write x and z for the common X and Z charges. The E6 gauge condition is `3Σ+4r=15`. The proposed rank-increasing operator is `Z_u A X_u`, with gap `δ=R(Z_u A X_u)−2`.

| Mixed rank | Alternating cubic | Microscopic current constraints | Gap δ |
| --- | --- | --- | --- |
| 1 | Present | `−81q<0`, `(27/4)(9q−16r)<0` | `q/2+2r/3>0` |
| 1 | Absent | `162(u−1)<0`, `−81r<0` | `1−u+2r/3>0` |
| 0 | Present | `27(3−4r)<0` | `1/6+r/3>5/12` |
| 0 | Absent | `162(x−1)<0`, `162(z−1)<0` | `5(1−x)/4+(1−z)/2>0` |

For rank one with the alternating cubic present, `u=1−q/2`, `R(Z_c)=2−r−q`, and `R(Z_u)=1−r/3+q`. The first constraint is from the unpaired X Cartan current. The second is from the derivative of these charges with respect to q, holding r fixed. When the alternating cubic is absent, the second current rotates the coupled X and Z with opposite phases. At rank zero the constraints are the Cartans of the full species symmetries. With the alternating cubic present x is 2/3, so the E6 condition fixes `z=3/2−2r/3`. These charges account for every component of the rank-increasing block. An operator in this block that survives as a chiral primary has dimension `3+3δ/2>3`. A component removed by a chiral-ring relation supplies no independent relevant superpotential deformation.

There is a uniform stronger bound for rank one with the alternating cubic and both gauge factors active. Take the flavor generator corresponding to `2∂r+3∂q` in the anomaly-free trial charge chart, including `R(S)=(3+12r)/5`. Its negative microscopic trace implies `(4149/4)q+(32676/25)r>22296/25`. Since q and r are positive, this gives `δ>14864/34575`, or operator dimension greater than `3+22296/34575`.

## Consequence for direct running

If the mixed superpotential matrix runs only by wavefunction renormalization, its beta function has the form `B_Z^T M + M B_X + b_A M`. Its finite-scale solution multiplies M by invertible matrices and a scalar, preserving rank. Near a rank-one fixed point, the rank-increasing block is represented by the Schur complement of the nonzero entry. That block has a homogeneous flow and its linear exponent toward high energy is `3δ/2>0`. At rank zero the same statement holds for the whole matrix. A nonzero rank-increasing block therefore cannot approach either lower-rank fixed point in the ultraviolet within this direct flow. This conclusion concerns the canonical cubic coupling itself. Flows through changed elementary fields, thresholds, or nonperturbatively generated superpotentials remain possible tests. [Supersymmetric Yukawa beta functions](https://arxiv.org/abs/hep-ph/9311340) · [Scope of superpotential nonrenormalization](https://arxiv.org/abs/hep-ph/9309335)

## Fixed-point tests when only the family factor is gauged

With the E6 gauge coupling zero, the family factor can still interact and E6 acts as a global symmetry. For rank zero with the alternating cubic, the X charge is 2/3 and the two Z fields have common charge z. The spectator charge is `6−18z/5` by the family gauge condition. The unbroken Z species SU(2) requires `z<1`. The independent anomaly-free flavor current `∂z`, which charges the two Z copies equally and S oppositely, has bare trace `486−7614z/25>0` throughout that range. This contradicts current positivity even with the usual free chiral corrections.

There is also a conditional test at rank two with either choice of alternating cubic. Let p be the charge of the uncoupled X and let r be the charge of the now family-gauge-singlet adjoint A. If A survives as a chiral primary, unitarity gives `r≥2/3`. The family gauge equation fixes `R(S)=(12+18r−9p)/5`. Use the conserved flavor current that varies p while preserving the active cubic charge constraints, keeping r and the paired X splitting fixed. Its bare trace is

```text
with alternating cubic       567 p/25 + 3807 r/50 − 891/25
without alternating cubic    567 p/25 + 2916 r/25 − 891/25
```

Negativity forces `p<−2/3` and `p<−13/7` respectively. Three fields from the uncoupled X can form a family baryon by using the family epsilon tensor and three distinct internal coordinates. Set the other X fields, all Z fields, A and S to zero. Every classical F-term vanishes. Taking the three columns of the remaining X to be orthonormal makes the family moment map zero and gives a baryon equal to one in that internal minor. Thus the baryon defines a classical chiral-ring class and this configuration completely Higgses the family group. Its trial charge is 3p and its charge under the flavor current is three. If even one such baryon component survives in the quantum ring, unitarity and free-field correction add `9(2/3−3p)` to the trace. The corrected traces are strictly positive over their respective allowed domains. Under these ring assumptions, the family-only rank-two fixed point is excluded for either cubic choice. The calculation leaves the quantum survival of the baryon open.

Run `python analysis/toe_20261112_mixed_rank_relevance.py` from the repository root. [Exact output](../data/toe_20261112_mixed_rank_relevance.json)
