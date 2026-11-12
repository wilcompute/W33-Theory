# Two exact W33 thresholds generate the missing mixed cubic

Two tree-level chiral thresholds reproduce the rank-two mixed superpotential at the canonical W33 flat vacuum. A pair of family-neutral E6 adjoints preserves the family beta coefficient and costs 24 units of E6 Dynkin index. A vectorlike bifundamental pair costs 18 units of E6 index and 27 units of family index. Both retain the canonical light holomorphic Hessian and its massless character after the tree-level matching. Their induced Kähler terms affect the normalized massive spectrum. [Canonical flat vacuum and spectrum](2026-11-09_canonical_sm_flatness.md) · [Why direct running cannot supply the missing rank](2026-11-12_mixed_rank_relevance.md)

## Adjoint threshold

Use zero-based species labels. Retain the rank-one coupling `Z1 A (X0+X1)` and target the missing term `Z0 A X2`. Write J for the E6-adjoint projection of the family-contracted matrix `X2 Z0`, normalized by the trace pairing on the 27, so that `⟨A,J⟩=Z0 A X2`. Add adjoint chirals B and C with the threshold superpotential

```text
W_threshold = M⟨B,C⟩ − m⟨A,C⟩ + η⟨B,J⟩.
```

The heavy stationary solutions are `B=(m/M)A` and `C=−(η/M)J`. Substitution gives exactly `(ηm/M)⟨A,J⟩`. The inverse heavy mass block has zero diagonal, so there is no J² self-exchange. For `M:m=4:3`, the normalized light field at the unbroken quadratic threshold is represented by `A=(4/5)A_can` and `B=(3/5)A_can`. Choosing η=5/3 gives the unit canonical coefficient. The two massive singular values in this quadratic threshold sector are five in units where M is four. The full massive spectrum also depends on the original superpotential and the chosen threshold scale. [Integrating out heavy chiral superfields](https://arxiv.org/abs/0904.0370)

At the original vacuum, X2 and Z0 have disjoint family supports, hence J=0. The lifted fields are `A=(4/5)6Y`, `B=(3/5)6Y` and C=0. Both adjoint VEVs are Hermitian and contribute zero to the moment map. The inherited superpotential is written using `(5/4)A` everywhere the matched field A_can appears, with the target term omitted before adding the mediators. The heavy F terms vanish by construction. The light F terms equal the derivatives of the matched canonical superpotential and vanish there as well.

## Bifundamental threshold

Add U in the X representation and D in the Z representation, with

```text
W_threshold = M D U − m D X2 + η Z0 A U.
```

The heavy solutions are `U=(m/M)X2` and `D=−(η/M)Z0 A`. This produces the same target coefficient, using the same masses and cubic input and replacing X2 in the inherited terms by `(5/4)X2`. At the canonical vacuum A annihilates Z0, so D=0. The X2 and U VEVs carry 4/5 and 3/5 of the original X2 VEV. Their two moment-map contributions add to the original one because their squared coefficients sum to one. The other moment maps and the inherited F equations agree with the canonical result.

For either construction the Schur complement of the invertible heavy block of the holomorphic Hessian equals the Hessian of the matched superpotential. The lifted gauge orbit has the same dimension by equivariance of the heavy solutions. Thus the massless chiral character after quotienting by the broken gauge directions is the same 49-component character as before. The canonical light Kähler metric is matched at the origin after the linear normalization. Eliminating the heavy partners adds a positive Kähler term proportional to `||J||²` or `||Z0 A||²`, respectively. Its derivatives can shift normalized masses at the Higgs vacuum.

## Minimal cost at fixed family running

Consider tree-level elimination of massive family-neutral chiral fields with renormalizable heavy interactions, at a parent-gauge-invariant reference point. Generating the missing cubic requires quadratic heavy-light mixing followed by a cubic source. Family neutrality requires the mixing to be with A, hence at least one heavy adjoint. With just one adjoint the elimination produces a nonzero J² quartic for every nonzero adjoint current coefficient. This includes the most general singlet assistance. To see it, isolate any nonzero species pair and a common family coordinate. Set its internal X and Z to `e0+e17` and `e0*−e17*`. The singlet contraction vanishes. The exact root matrices have no entries linking those two internal coordinates, and the Cartan projection gives `⟨J,J⟩=2/3` for unit source coefficient. Any number of singlet exchanges therefore vanish on this witness and cannot cancel the adjoint quartic.

The only family-neutral E6 representations with a source from XZ are 1, 78 and 650. Two X fields or two Z fields have no family singlet. A 650 alone costs 150 units of E6 index, as follows from the product `27⊗27̄` and its singlet and adjoint summands. With fewer than 24 units of added index the only possible source representations are singlets and one adjoint, already excluded. The two-adjoint construction attains 24. This minimality concerns matching the mixed cubic without a residual XZ quartic in this tree-level class. [E6 tensor products](https://cds.cern.ch/record/134739/files/198109187.pdf)

In the convention `β(g)=−b0 g³/(16π²)+…`, the canonical coefficients `(−21,−66)` become `(−45,−66)` with the adjoints or `(−39,−93)` with the bifundamentals. The matching therefore comes with a calculable worsening of weak ultraviolet running. It supplies the mixed cubic, while the canonical higher-degree interactions remain input.

## A conditional ultraviolet obstruction for the adjoint threshold

Set the threshold masses to zero at a candidate fixed point with both gauge factors active. Keep the two separate mixed cubics and either choice of the alternating cubic. The third adjoint C has no active superpotential coupling. Let a, b, c be the scalar R charges of A, B, C and Σ the sum over the five bifundamental scalars. Gauge anomaly cancellation gives `3Σ+4(a+b+c)=23` and `9Σ+5R(S)=48`. Vary the relative splittings of the two coupled pairs, preserving the active cubic charges. Positivity of their flavor currents implies `a+b>0` when the alternating cubic is present, and `a>0` and `b>0` when it is absent.

The anomaly-free flavor variation of c at fixed a, b and pair splittings gives a microscopic trace

```text
Tr R F_c² = (6/25)[w(a+b)+101c+27],
w = 226 with the alternating cubic, 376 without it.
```

Negative trace requires `c<−27/101`. The degree-five E6 Casimir of C is nonzero in the classical chiral ring, where all other fields can be set to zero and C taken in the Cartan. If it survives as a quantum chiral primary, its trial charge 5c is below 2/3 and the ordinary free-field correction adds `25(2/3−5c)` to this trace. The corrected result is strictly positive for `a+b>0` and c<0. Further free corrections have nonnegative sign and cannot repair the contradiction. This excludes both cubic choices for the stated active gauge and superpotential support under the quantum-Casimir assumption. A new interacting accidental sector, a superpotential involving C, or the bifundamental threshold requires a separate test. [Flavor-current positivity](https://arxiv.org/abs/hep-th/0304128) · [Free-field correction](https://arxiv.org/abs/hep-th/0308071)

Run `python analysis/toe_20261113_mixed_mediator_threshold.py` from the repository root. [Exact output](../data/toe_20261113_mixed_mediator_threshold.json)
