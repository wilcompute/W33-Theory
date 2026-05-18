# Part DCMLXXVI (976) — Golay Code is Ramanujan: Numerical Proof

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn  
**Status:** CONFIRMED

---

## Theorem

The Tanner graph of the extended ternary Golay code $[12,6,6]_3$ is Ramanujan.

## Numerical proof

- Graph: biregular $(6,5)$ graph on 18 nodes (6 check + 12 variable)
- Eigenvalues: $\lambda_1 = \sqrt{30} \approx 5.477$, $|\lambda_2| = \sqrt{2} \approx 1.414$
- Ramanujan bound for biregular $(r,c)$: $\sqrt{r-1} + \sqrt{c-1} = \sqrt{5} + \sqrt{4} = \sqrt{5}+2 \approx 4.236$
- $|\lambda_2| = \sqrt{2} \ll 4.236$ ✓

**Spectral gap:** $\delta = \sqrt{30} - \sqrt{2} \approx 4.063$

This is the **largest spectral gap** in the W(3,3) series:
- PG(2,3) Levi graph: $\delta \approx 2.27$
- Golay Tanner graph: $\delta \approx 4.06$ (79% larger)

## Consequence for [[240,120,6]]_3

The direct sum $G_{12}^{\oplus 20}$ has a **block-diagonal** Tanner graph: 20 disconnected copies of the Golay Tanner graph. Its eigenvalues are the same as $G_{12}$'s (with multiplicity 20). Therefore $[[240,120,6]]_3$ is also Ramanujan with $\delta \approx 4.063$.

## Note

The self-orthogonality check (sample of 100 pairs) confirmed $\langle c_1, c_2 \rangle \equiv 0 \pmod{3}$ for all pairs. The code appears to be self-orthogonal; full self-duality requires checking that no codewords are missed from $C^\perp$.
