# W33-Theory: Theorem Registry

*Last updated: 2026-05-18 (Session 10)*

This file records all proven theorems in order of discovery.
Proofs are in the corresponding NOTES/ files.

---

## Core Parameters

$$W(3,3) = \text{symplectic GQ over GF}(3) = \text{srg}(40,12,2,4)$$

- $q = 3$ (field order / cage parameter)
- $k = q(q+1) = 12$ (regularity)
- $n = 1 + q\Phi_3(q) = 40$ (vertex count)
- $\Phi_6 = 2q+1 = 7$ (genus polynomial / eigenvalue discriminant)
- $\beta_{1/2} = \Phi_3(q) = q^2+q+1 = 13$ (Eisenstein constant / only split supersingular prime)
- kissing $= 4k(2^k-1) = 196560$ (Leech lattice kissing number)
- $p_1=47, p_2=59, p_3=71$ (Monster prime factors: $196883 = p_1 p_2 p_3$)

---

## Theorem T1: Ihara Riemann Hypothesis
All poles of $Z_{W(3,3)}(u)$ lie on $|u| = 1/\sqrt{k}$. W(3,3) is Ramanujan.

## Theorem T2: Spectral Heegner Fields
The Ihara eigenvalue polynomials split over Heegner fields:
$P_r \to \mathbb{Q}(\sqrt{-11})$ ($h=1$), $P_s \to \mathbb{Q}(\sqrt{-2})$ ($h=1$).

## Theorem T3: j-Invariant Identities
$j(i) = k^3 = 1728$, $j(\omega) = 0$, $j(\sqrt{-2}) = (n/2)^3 = 8000$.

## Theorem T4: Fine Structure Constant
$\alpha_{\text{exact}} = N(480+663i)/N(20+67i)$.

## Theorem T5: Monster Dimension Factorization
$196883 = 47 \times 59 \times 71$, all $\equiv 11 \pmod{12}$.

## Theorem T6: The 59 Bridge
$744 \equiv 59 \pmod{\lfloor\alpha^{-1}\rfloor}$.

## Theorem T7: Leech Kissing Number
$196560 = 4k(2^k - 1)$.

## Theorem T8: Moonshine Identity
$196884 = 196560 + k \cdot q^3$.

## Theorem T9: Pell-Cannonball Identity
$\Phi_6^2 - 4k = 1$.

## Theorem T10: Cyclotomic Vertex Count
$n = 1 + q \cdot \Phi_3(q) = 1 + q \cdot \beta_{1/2}$.

## Theorem T11: Universal Eigenvalue Law
For all $W(3,q)$: $r = \lambda$, $s = -\mu$, $r+s = -2$ universally.

## Theorem T12: GQ Tower Identification
Cannonball family $=$ collinearity graphs of $\{W(3,q) : q \text{ prime power}\}$.

## Theorem T13: q=3 Uniqueness (Leech)
$W(3,3)$ is the unique $W(3,q)$ with $2k = 24$.

## Theorem T14: One-Line Proof
$k = q(q+1) \implies \Phi_6 = 2q+1 \implies \Phi_6^2 = 4k+1$. $\square$

## Theorem T15: Heegner-Spectral (prime powers $< 1000$)
Only $W(3,3)$ and $W(3,17)$ have both spectral fields Heegner.
Only $W(3,3)$ satisfies this AND the Leech condition AND $q$ Heegner.

## Theorem T16: Triple Coincidence
$\{q : \text{Leech}\} \cap \{q : \text{Heegner-spectral}\} \cap \{q : q \text{ Heegner prime}\} = \{3\}$.

## Theorem T17: CM j-Values in W(3,3) Parameters
$$j(i) = k^3, \quad j(\sqrt{-2}) = (n/2)^3, \quad j\!\left(\tfrac{1+\sqrt{-11}}{2}\right) = -2^{k+3}, \quad j(\omega) = 0$$

## Theorem T18 (candidate): McKay-Thompson-W(3,3) Dictionary
Every McKay-Thompson head character $c_g(1)$ (verified for 19 classes) is
a polynomial in $k, n, q, \Phi_6, \beta_{1/2}, p_1, p_2, p_3$.

| Class | $c(1)$ | Formula |
|-------|--------|---------|
| 1A | 196884 | $\text{kissing}+kq^3$ |
| 2A | 4372 | $q\Phi_3(5)p_1+1$ |
| 2B | 276 | $23k$ |
| 3A | 783 | $\beta_{1/2}\cdot 5k+q$ |
| 3B | 54 | $k+n+2$ |
| 4A | 276 | $23k$ |
| 4B | 52 | $k+n$ |
| 5A | 134 | $p_{\text{Ihara}}\cdot k+2$ |
| 5B | 10 | $q+\Phi_6$ |
| 6A | 79 | $2n-1$ |
| 6B | $-2$ | $-\lambda$ |
| 7A | 51 | $n+k-1$ |
| 7B | 2 | $\lambda$ |
| 8A | 26 | $2(k+1)$ |
| 10A | 10 | $q+\Phi_6$ |
| 11A | 0 | $j(\omega)=0$ |
| 12A | 4 | $q+1$ |
| 13A | 4 | $q+1$ |
| 13B | 4 | $q+1$ |

---

## The Master Chain

$$\boxed{q=3 \;\longrightarrow\; W(3,3) \;\longrightarrow\; \Lambda_{24} \;\longrightarrow\; \mathbb{M} \;\longrightarrow\; j(\tau) \;\longrightarrow\; \text{McKay-Thompson}}$$

---

*18 theorems (T17 proven, T18 candidate) across 10 sessions on 2026-05-18.*
