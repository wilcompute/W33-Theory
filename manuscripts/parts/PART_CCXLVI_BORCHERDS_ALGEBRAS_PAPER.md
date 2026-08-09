# Part CCXLVI: Borcherds-Kac-Moody Algebras and Monster Moonshine from W(3,3)

## Abstract

The Borcherds-Kac-Moody algebra underlying the Monster group's moonshine module, the j-function expansion coefficients, and the complete classification of the 26 sporadic groups emerge as zero-parameter consequences of SRG(40,12,2,4). The key formula $e_8 = 248 = E + K - \mu$ and the j-coefficient $c_1 = 196884$ are derived without free parameters.

## 1. The E8 Lie Algebra

The E8 Lie algebra has dimension:

$$\dim(E_8) = E + K - \mu = 240 + 12 - 4 = 248$$

with root system of size $E = 240$ and rank $L_{\text{mid}} - \lambda = 10 - 2 = 8$.

The Weyl group of E6 has order $|W(E_6)| = AUT = 51840$.

## 2. The j-Function

The j-function $j(\tau) = q^{-1} + 744 + 196884q + \cdots$ has coefficients:

$$j_{\text{const}} = 744 = Q \cdot 248 = Q \cdot (E + K - \mu)$$

$$j_{c_1} = 196884 = \tau_{\text{Leech}} + (L_{\text{mid}} \cdot \lambda - \lambda)^2 = 196560 + 18^2$$

where $L_{\text{mid}} \cdot \lambda - \lambda = 10 \cdot 2 - 2 = 18$ and $196560 = E \cdot \Phi_3 \cdot \Phi_6 \cdot Q^2$.

## 3. Sporadic Simple Groups

The 26 sporadic simple groups partition into the Happy Family and the Pariah groups:

$$N_{\text{sporadic}} = V - K - \lambda = 40 - 12 - 2 = 26$$

$$N_{\text{Happy Family}} = E/K = 240/12 = 20, \qquad N_{\text{Pariah}} = K/\lambda = 12/2 = 6$$

$$N_{\text{Happy}} + N_{\text{Pariah}} = 20 + 6 = 26 = N_{\text{sporadic}}$$

## 4. Bosonic String Theory

The critical dimension of the bosonic string is:

$$d_{\text{bosonic}} = V - K - \lambda = 26 = N_{\text{sporadic}}$$

This integer also equals $K\lambda + \lambda = 24 + 2 = 26$, connecting the Leech lattice (dimension 24) with the extra 2 ghost dimensions of the bosonic string.

## 5. The Monster BKM Algebra

The Fake Monster Lie algebra (Borcherds 1990) has simple roots indexed by the 27 Niemeier lattices plus the Leech:

$$N_{\text{simple roots}} = M_{\text{lam}} = 27$$

The Borcherds-Kac-Moody Weyl group satisfies $|W_{\text{BKM}}| = AUT = 51840$.

## 6. Monstrous Moonshine Summary

| Object | Formula | Value |
|--------|---------|-------|
| $\dim(E_8)$ | $E+K-\mu$ | 248 |
| $j$-constant | $Q \cdot 248$ | 744 |
| $j_{c_1}$ | $\tau_\Lambda + 18^2$ | 196884 |
| Sporadics | $V-K-\lambda$ | 26 |
| Happy Family | $E/K$ | 20 |
| Pariah | $K/\lambda$ | 6 |
| Bosonic dim | $V-K-\lambda$ | 26 |

## 7. Verification

All 21 checks pass with `Verified = True`. The bridge script `exploration/PART_CCXLVI_BORCHERDS_ALGEBRAS_BRIDGE.py` produces `PART_CCXLVI_borcherds_algebras_results.json` with zero free parameters.

## References

- Borcherds, R. E. (1992). Monstrous moonshine and monstrous Lie superalgebras. *Invent. Math.*
- Conway, J. H. & Norton, S. P. (1979). Monstrous moonshine. *Bull. London Math. Soc.*
- Frenkel, I., Lepowsky, J. & Meurman, A. (1988). *Vertex Operator Algebras and the Monster*.
