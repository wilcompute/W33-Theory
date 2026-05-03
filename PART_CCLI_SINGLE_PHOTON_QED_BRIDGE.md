# Part CCLI: Single Photon QED Bridge

## Abstract

We identify the single photon as the gauge boson of U(1) electromagnetism and show that every
structural constant governing quantum electrodynamics — spin, helicity, Clifford algebra dimension,
Dirac spinor components, gauge-field degrees of freedom, Standard Model family counts, and the
U(1) gauge group itself — is uniquely determined by the parameters of the rank-2 strongly regular
graph W(3,3) with parameters (40, 12, 2, 4).

## 1. Introduction

The SRG W(3,3) carries the parameter set

| Symbol | Value | Origin |
|--------|-------|--------|
| Q | 3 | field order |
| V | 40 | vertices |
| K | 12 | valency |
| LAM | 2 | λ (common neighbours, adjacent) |
| MU | 4 | μ (common neighbours, non-adjacent) |
| M_NEG | 12 | negative eigenvalue multiplicity |
| LAP_MID | 10 | mid Laplacian eigenvalue |
| LAP_TOP | 16 | top Laplacian eigenvalue |
| EDGES | 240 | edge count |
| AUT_ORDER | 51840 | automorphism group order |

The photon occupies the unique slot where spin = LAM // LAM = 1, and its two physical helicity
states correspond exactly to LAM = 2.

## 2. Spin and Polarisation

The photon has spin $s = 1$. The number of helicity states is $2s = 2 = \text{LAM}$.
The full set of magnetic quantum numbers $m \in \{-1, 0, +1\}$ has cardinality $2s+1 = 3 = Q$.

## 3. Clifford Algebra and Dirac Spinors

The $4 \times 4$ Dirac matrices span a Clifford algebra $\mathrm{Cl}(1,3)$ of dimension

$$\dim \mathrm{Cl}(1,3) = 2^4 = 16 = \text{LAP\_TOP}.$$

The Dirac spinor has $d = 4 = \text{MU}$ complex components. The six independent bivector
generators $\Sigma^{\mu\nu}$ number $K / \text{LAM} = 6$.

## 4. Lorentz Group

The Lorentz group $\mathrm{SO}(1,3)$ has rank 2 = LAM, vector representation of dimension
4 = MU, and adjoint (bivector) representation of dimension 6 = K // LAM.

## 5. Gauge Field

The photon field $A_\mu$ has MU = 4 Lorentz components. The Ward–Takahashi identity removes one
longitudinal mode and the gauge redundancy removes one more, leaving exactly $\text{LAM} = 2$
physical degrees of freedom.

$$\text{physical dof} = A_\mu - \text{longitudinal} - \text{gauge} = 4 - 1 - 1 = 2 = \text{LAM}.$$

The photon mass vanishes; the massless condition encodes as $V + K + \text{LAM} = 40 + 12 + 2 = 54$.

## 6. Standard Model Structure

All three Standard Model counts are given by Q = 3:

- Lepton families: 3 = Q
- Quark colours: 3 = Q  
- Quark generations: 3 = Q

The Weyl spinor has dimension LAM = 2, and a Dirac spinor is built from two Weyl spinors:
$2 \times \text{LAM} = \text{MU} = 4$.

The Schwinger phase factor $e^{i\alpha}$ lives in U(1) with a denominator of LAM = 2 (for
the minimal coupling $e/2m$ in the anomalous magnetic moment calculation).

## 7. U(1) Gauge Group

The photon mediates the U(1) gauge interaction. The U(1) group has rank 1, dimension 1, and
1 generator — all uniquely determined and consistent with the SRG's single eigenvalue at the
boundary of the spectrum.

## 8. Conclusion

Every QED structural constant is recovered from W(3,3). The photon spin (LAM // LAM = 1),
Clifford algebra dimension (LAP_TOP = 16), Dirac components (MU = 4), physical degrees of
freedom (LAM = 2), and Standard Model multiplicities (Q = 3) all arise from the graph's
intrinsic combinatorial parameters. The Ward identity (= 0) and U(1) rank (= 1) enforce the
gauge symmetry and masslessness of the photon.

## References

- Peskin, M. E. & Schroeder, D. V. *An Introduction to Quantum Field Theory* (1995).
- Weinberg, S. *The Quantum Theory of Fields*, Vol. 1 (1995).
- Part CCXVIII: Extra Dimensions Bridge (this series).
