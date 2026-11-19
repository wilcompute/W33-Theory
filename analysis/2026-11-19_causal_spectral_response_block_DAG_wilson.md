# Causal DAG spectral response: a sharp boundary between vacuum determinant and gauge-sensitive propagation

**Date:** 2026-11-19. **Status:** independently checked finite linear algebra; **not** an emergent quantum field theory or a Theory of Everything.

## Provenance and novelty check

This follows the latest repo's `f73c83e853` eight-gate packet and especially `analysis/toe_20261119_causal_diamond_gauge_interference.py`, which already proves graph-blind determinants and observable gauge-invariant U(1) two-path interference. It also complements `analysis/toe_20261119_causal_gauge_optics_entropy_flavor_info_v10.py`, which checks the scalar DAG determinant. Those are **prior in-repo results**, not new findings of this pass.

This pass extends that boundary in three ways: (1) a general matrix-valued local-site theorem valid for arbitrary noncommuting gauge transports and nonidentical local blocks; (2) the inverse singular-value trace and positive spectral regularizer as explicit gauge-sensitive quantities even though the plain Hermitianized determinant remains exactly blind; (3) SU(3) two-holonomy comparison proving the first trace moment need not determine higher spectral response.

Relevant literature anchors: causal-set Green functions and mesoscopic d'Alembertians (Surya, Living Reviews 2019, https://doi.org/10.1007/s41114-019-0023-1); Wilson line and loop transport concepts (review https://onlinelibrary.wiley.com/doi/10.1002/prop.70156). Reflection positivity is a **separate gate**, especially after Lu and Shao (submitted 2026-11-15, https://arxiv.org/abs/2611.20084): the overlap Weyl fermion is not finite-lattice reflection-positive in 2D/4D. We do not claim any such positivity test here.

## Theorems

**General block-triangular blindness.** Let the causal graph have vertices topologically ordered so every edge points from smaller to larger index. Assign arbitrary invertible q x q site blocks M_i, not necessarily commuting, and arbitrary edge transport matrices U_e. Then
```
D_ii = M_i,       D_ij = -alpha U_ij for forward edges,
D_ij = 0 for backward edges.
```
Block triangularity implies `det(zI-D)=prod_i det(zI-M_i)`, `det D=prod_i det M_i`, and `det(D^dagger D)=prod_i |det M_i|^2`. Thus no bare eigenvalue/determinant information detects the forward graph. Local upper-triangular transport can nonetheless change non-normality, singular values, and resolvents.

**Diamond Wilson response.** On four events with edges 0→1→3 and 0→2→3, take all site blocks mI and length-two path transports P and Q. For G=D^{-1}, `G_03=(alpha^2/m^3)(P+Q)`. The relative Wilson matrix W=P Q^dagger transforms by conjugation under endpoint gauge transformations. Put K=D^dagger D. Directly expanding the finite nilpotent Neumann series yields

```
Tr K^{-1} = 4q/m^2 + 4q alpha^2/m^4
          + alpha^4/m^6 [2q + 2 Re Tr W].
```

Consequently the positive, explicitly **modified** spectral determinant `Z(mu)=det(K+mu I)` has `(d/dmu) log Z|_{mu=0}=Tr K^{-1}`, which varies with gauge holonomy. `det K` itself is constant: adding `mu I` changes the operator.

An independent positive **source-to-detector response** is `Z_probe(lambda)=det[I_q + lambda G_03 G_03^dagger]`. This is an observable generating function, not the original vacuum fermion determinant. It is invariant under arbitrary local U(q) gauge-frame changes and equals 1 at perfect two-path cancellation.

**Higher non-Abelian information.** Even for SU(3), the real fundamental Wilson trace does not by itself determine all coefficients of the regulated spectral determinant. Fix two diagonal SU(3) holonomies with exactly equal `Re Tr W=0.664457775189137`: one has `Im Tr W=0`, the other `Im Tr W=0.773644542790111`. They have the same first `log det` derivative (8.809925450816268) but different second derivatives (-9.30830922268564 vs -9.307446238765024) and different normalized determinants at mu=0.1 (2.31194972935 vs 2.31195540663). Hence a spectral response can resolve gauge conjugacy data beyond the first moment.

## Exact-control and numerical summary

The code checks 32 random block DAGs (q=2 and 3), 24 random U(3) frame transformations, and four SU(2) diamond phases. Maximum frame residual < 9e-15. Parameters: m=1.3, alpha=0.6, lambda=2, mu=0.1.

| SU(2) phase | det D | det(K+mu I)/det K | endpoint Z_probe |
|---|---:|---:|---:|
| 0 | 8.15730721 | 1.759528357226 | 1.475739758187 |
| pi/3 | 8.15730721 | 1.752412401238 | 1.348153724830 |
| pi/2 | 8.15730721 | 1.745310863740 | 1.226335087346 |
| pi | 8.15730721 | 1.731151044212 | 1.000000000000 |

Reproduction: `python analysis/toe_20261119_causal_spectral_response_v1.py` writes `data/toe_20261119_causal_spectral_response_v1.json`. The regression command is `python -m unittest tests/test_toe_20261119_causal_spectral_response_v1.py` (or unittest discover with pattern).

## Physical limits and next falsification

None of these determinants is a derived Lorentzian Dirac path integral. The positive regulator `mu` is an additional tunable coupling; its presence may violate fundamental symmetries unless derived from a physical operator. Choosing a source and detector changes the operational question and does not automatically define a vacuum weighting of spacetime. The first trace slope depends on supplied `m`, `alpha`, and `U_e`; it does not determine those constants. We have shown no continuum 3+1 dimension, local Lorentz invariance, reflection positivity, fermionic anomaly cancellation, unitarity, or Einstein field equations.

The next genuinely hard gate is to find a regulator or influence functional derived from a causal, unitary, anomaly-free microscopic action. It must retain this Wilson sensitivity and select physically appropriate four-dimensional manifoldlike histories under a **normalized** sum over graphs; a hand-inserted positive determinant is not enough.
