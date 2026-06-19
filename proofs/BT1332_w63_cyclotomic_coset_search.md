# BT1332 — W63 Cyclotomic Coset Search Protocol

**Date:** 2026-06-19  
**Series:** Post-HoloNet Validation  
**Predecessor:** BT1327 (W63 Construction Blueprint)

---

## 1. Setup

Length $n=63 = 2^6 - 1$. We work over $\mathbb{F}_2$. Let $\alpha$ be a primitive element of $\mathbb{F}_{2^6}$. The cyclotomic cosets modulo 63 partition $\{0,1,\ldots,62\}$ into orbits under multiplication by 2.

---

## 2. Cyclotomic Cosets mod 63

The cosets and their sizes:

| Coset representative | Orbit size | Members |
|---------------------|-----------|--------|
| 0 | 1 | {0} |
| 1 | 6 | {1,2,4,8,16,32} |
| 3 | 6 | {3,6,12,24,48,33} |
| 5 | 6 | {5,10,20,40,17,34} |
| 7 | 6 | {7,14,28,56,49,35} |
| 9 | 6 | {9,18,36,9,...} |
| 11 | 6 | {11,22,44,25,50,37} |
| 13 | 6 | {13,26,52,41,19,38} |
| 15 | 6 | {15,30,60,57,51,39} |
| 21 | 6 | {21,42,21,...} |
| 63 is $7 \times 9$ | 3 | {21,42,0\pmod{3},...} |

**Key structural fact:** $63 = 7 \times 9$. The cosets split into those inherited from $\mathbb{F}_{2^3}$ (order dividing 7) and those from $\mathbb{F}_{2^2}$ (order dividing 9). Specifically:
- Cosets of **7-smooth** elements: minimal polynomials over $\mathbb{F}_{2^3}$, orbit size $\leq 3$.
- Cosets of **generic** elements: orbit size 6.

The full factorization:
$$
x^{63} - 1 = \prod_{d \mid 63} \Phi_d(x) = \Phi_1 \Phi_3 \Phi_7 \Phi_9 \Phi_{21} \Phi_{63}.
$$

---

## 3. BCH Code Defining Set Strategy

For designed distance $\delta = 11$, the BCH code $\mathcal{C}(63,\delta)$ has defining set
$$
T_{\delta} = C_1 \cup C_2 \cup \cdots \cup C_{\delta-1} = C_1 \cup \cdots \cup C_{10}
$$
(union of cyclotomic cosets containing $\alpha^1, \ldots, \alpha^{10}$).

The redundancy (co-dimension) is $|T_\delta|$. We need $|T_\delta| = 31$ to get $\dim = 32$ for the $k=1$ CSS construction.

### Coset union sizing

Cosets $C_1, C_3, C_5, C_7, C_9$ each have size 6, $C_0$ has size 1. The union $C_1 \cup C_3 \cup C_5$ already yields $18$ positions. Adding $C_7, C_9$ brings total to 30. One more element from $C_{11}$ (or a 3-element coset from the 7-smooth part) completes $|T| = 31$.

---

## 4. CSS Orthogonality Alignment

For the CSS construction we need two codes $C_X, C_Z$ such that $C_Z^\perp \subseteq C_X$. In the cyclic code setting, this means the defining set $T_Z^\perp = \{63 - j \pmod{63} : j \in T_Z\}$ must satisfy $T_Z^\perp \subseteq T_X$.

**Search condition:** Find a pair of defining sets $(T_X, T_Z)$ such that:
1. $|T_X| = |T_Z| = 31$ (balanced CSS)
2. $T_Z^\perp \subseteq T_X$
3. Minimum distance of $C_X / C_Z^\perp \geq 11$
4. Minimum distance of $C_Z / C_X^\perp \geq 11$

Condition (2) is equivalent to $T_X \cup T_Z^\perp = T_X$ i.e. $T_Z = 63 - T_X \pmod{63}$ (negacyclic dual). This is satisfied automatically for BCH codes with **complementary shift**: set $T_Z = \{63 - j \pmod{63}: j \in T_X\}$.

---

## 5. Search Algorithm

```
INPUT: n=63, target k=1, target d≥11
FOR each candidate defining set T of size 31 built from cyclotomic cosets:
  Compute C_X = BCH(63, T)
  Compute T_Z_perp = {63-j mod 63 : j in T}
  IF T_Z_perp ⊆ T:
    Compute d_X = mindist(C_X \ C_Z_perp)
    Compute d_Z = mindist(C_Z \ C_X_perp)
    IF d_X >= 11 AND d_Z >= 11:
      RECORD (T, d_X, d_Z) as W63 candidate
```

The outer loop iterates over at most $2^{10} = 1024$ choices of which 10 cosets to include (from the ~10 distinct cosets covering positions 1–30), making this computationally tractable.

---

## 6. Sector Permutation Test

For each W63 candidate $(T, d_X, d_Z)$:
1. Obtain the generator matrix $G_X \in \mathbb{F}_2^{32 \times 63}$.
2. Search for a permutation $\sigma \in S_{63}$ such that columns decompose into 7 blocks of 9 with the Fano incidence pattern on cross-block supports.
3. This is a **group-theoretic coset enumeration** over the automorphism group $\mathrm{Aut}(\mathcal{C})$.

The cyclic code automorphism group contains the cyclic shift $x \mapsto x+1 \pmod{63}$ and the Frobenius $x \mapsto 2x \pmod{63}$. Together they generate a group of order at least $63 \times 6 = 378$, which is large enough to make the sector test tractable.

---

## 7. Expected Outcome

Based on the structure of length-63 BCH codes and the $63 = 7 \times 9$ factorisation, it is plausible that:

- At least one defining-set pair $(T_X, T_Z)$ satisfies the orthogonality condition.
- The resulting code achieves distance exactly 11 or 13.
- The cyclic automorphism group facilitates the 7-sector decomposition.

**Falsification criterion:** If the exhaustive search finds no candidate with $d \geq 11$, the W63 conjecture fails and an alternative construction (e.g. twisted product codes over $\mathbb{F}_3$) is required.

---

**Next:** BT1333 — W33 Exact Syndrome Simulator Specification.
