# H27 SIC vacua, SU(3) baryon minors, and Hesse-line alignment

**Date:** 2026-11-19. **Status:** exact finite-dimensional calculation plus an explicit bosonic gauge-invariant *candidate* potential. No holomorphic SUSY F-term or physical TOE is claimed. Follows `2026-11-19_H27_SIC_SU3_moment_map_completion_boundary.md`.

## 1. Nonnegative gauge-invariant potential whose zeros are D-flat SIC frames

Let the nine scalar species be `Q_j in C^3` in the SU(3) fundamental. Let `r>0` and `mu,kappa>0`. Define
\[
V_{\rm align}=\mu\sum_j(Q_j^\dagger Q_j-r)^2+
\kappa\sum_{j<k}\left(4|Q_j^\dagger Q_k|^2-r^2\right)^2.
\]
Every summand is SU(3)-gauge invariant and nonnegative. Its global zeros consist of nine equally normalized equiangular qutrit SIC vectors (including, not uniquely selecting, the projective H27 plus and minus orbits). The D-flat condition follows *without independently imposing it*. With `S=sum_j Q_j Q_j^dag` the SIC constraints imply
\[
\operatorname{tr}S=9r,\quad
\operatorname{tr}S^2=9r^2+72r^2/4=27r^2=(\operatorname{tr}S)^2/3.
\]
Equality in the eigenvalue Cauchy inequality forces `S=3r I_3`, so `Tr(T_a S)=0` for all eight SU(3) generators. This is a finite-dimensional moment-map reduction mechanism. No metric or chiral gauge theory is inferred.

The potential has quartic norm penalties and eighth-order pairwise penalties in elementary fields. It is a **nonholomorphic bosonic alignment potential**, not an N=1 gauge-invariant superpotential; flat species phases and SIC-family deformations remain.

## 2. SU(3)-invariant Plucker/baryonic distinguishing invariants

For each triple of nine species define `B_ijk=epsilon_abc Q_i^a Q_j^b Q_k^c=det(Q_i,Q_j,Q_k)`. The quantity `|B_ijk|^2` is SU(3)-gauge invariant. For unnormalized H27 orbits of `(1,1,0)` and `(1,-1,0)`, both with each `||Q_j||²=2`, exact enumeration over all 84 triples gives:

| `|B|²` | plus SIC `(1,1,0)` | minus SIC `(1,-1,0)` |
|---:|---:|---:|
| 0 | 3 | 12 |
| 1 | 18 | 0 |
| 3 | 54 | 72 |
| 4 | 9 | 0 |

The difference between **three** dependent triples in generic qutrit SICs and **twelve** in the special Hesse SIC is known in SIC literature. This computation gives a concrete SU(3) baryonic invariant implementation in the H27 vacuum proposal.

The first two permutation-invariant moments coincide:
\[
M_1=\sum_{i<j<k}|B_{ijk}|^2=216,\qquad
M_2=\sum_{i<j<k}|B_{ijk}|^4=648.
\]
The first equality is the Cauchy--Binet identity `M1=det(S)=det(6I)=216`; consequently it cannot select one SIC family over the other. The third moment distinguishes:
\[
M_3^{+}=2052,\qquad M_3^{-}=1944,\qquad \Delta M_3=108.
\]
All calculations use exact sympy expressions in the Eisenstein field.

## 3. A lower-degree H27-invariant separator

Label the nine species by the affine qutrit phase plane `(a,b) in F3²`, index `3*b+a`. The **12 affine lines** are preserved by the H27 translation action. Define
\[
J_{\rm Hesse}(Q)=\sum_{\ell\in AG(2,3)\,\mathrm{lines}}
|\det(Q_i,Q_j,Q_k)|^2,\quad\ell=\{i,j,k\}.
\]
This is continuous-SU(3) gauge invariant and discrete-H27-translation invariant. Exact line-multiset census:
- plus SIC: `0^3, 4^9`, hence `J_Hesse=36`;
- minus SIC: `0^12`, hence `J_Hesse=0`.

Therefore a **sextic baryonic operator** separates these *two explicit* F-flat SIC configurations, even though the all-triples first and second moments do not. A suitable scalar potential coupling could prefer one branch, but global vacuum selection, stability, all other stationary branches, continuous phase moduli, and SU(3) UV gauge invariance have not been solved. In particular this construction does NOT supply a supersymmetric E8 flavon.

### Prior-art boundary

The plus/minus SIC variants and the three-versus-twelve dependent-triple distinction have already been discussed in qutrit SIC literature; see Planat and Gedik, *Magic informationally complete POVMs with permutations* (2017), https://pmc.ncbi.nlm.nih.gov/articles/PMC5627088/, and earlier dissertation treatments of generic versus Hesse qutrit SICs. The classification itself is not claimed as new. What is new in this project packet is the explicit **gauge-invariant Plucker-moment and Hesse-line interaction as a concrete dynamical candidate**, not the SIC classification itself.

### Reproduction
`python analysis/toe_20261119_sic_baryon_plucker_alignment.py`, certificate `data/toe_20261119_sic_baryon_plucker_alignment.json`.

The next physical proof obligation is a gauge-invariant supersymmetric UV field content and superpotential whose combined F/D-flat moduli admit an isolated acceptable SIC/H27 orbit and whose anomaly/fermion spectrum is viable.
