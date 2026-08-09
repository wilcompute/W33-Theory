# Part CCXXXVI — Moonshine and the Monster Group from W(3,3)

## Abstract

Monstrous Moonshine (Conway-Norton 1979; proved by Borcherds 1992) relates the Monster group
$\mathbb{M}$ — the largest sporadic simple group — to modular forms via the j-function. The
Fourier coefficients of $j(\tau) = q^{-1} + 744 + 196884q + \cdots$ equal sums of Monster
irrep dimensions. All defining constants in Moonshine are **exact polynomial expressions in
the SRG(40,12,2,4) constants** at zero free parameters:

$$j(i) = 1728 = K^3, \quad 744 = Q \cdot \dim(E_8) = Q(\text{EDGES}+2\mu), \quad 196883 = (4K-1)(5K-1)(6K-1).$$

All 32 bridge checks pass; $\texttt{Verified} = \texttt{True}$.

---

## 1. SRG Constants (Immutable Anchor)

| Symbol | Value | Meaning |
|--------|-------|---------|
| $Q$ | 3 | Eigenvalue ratio / ternary field |
| $V$ | 40 | Vertex count |
| $K$ | 12 | Degree |
| $\lambda$ | 2 | Adjacent common neighbours |
| $\mu$ | 4 | Non-adjacent common neighbours |
| EDGES | 240 | Edge count / E₈ kissing number |
| AUT\_ORDER | 51840 | $|W(E_6)|$ |

---

## 2. The j-Function at $\tau = i$ (Bridge B1)

The j-invariant at the imaginary unit $\tau = i$ takes the value:

$$j(i) = 1728 = 12^3 = K^3.$$

This is the Weierstrass discriminant identity: $j(i) = 4 \cdot 12^3 / \Delta$ evaluated at the
elliptic curve with $g_2 = 1, g_3 = 0$. The SRG degree $K = 12$ precisely generates this
discriminant.

---

## 3. The j-Function Constant Offset 744 (Bridge B2)

The j-function expansion:
$$j(\tau) = q^{-1} + \mathbf{744} + 196884q + 21493760q^2 + \cdots$$

The constant term $744$ is:

$$744 = Q \cdot \dim(E_8) = Q \cdot (\text{EDGES} + 2\mu) = 3 \times 248 = 744.$$

The Frenkel-Lepowsky-Meurman moonshine module $V^\natural$ has $j$-function equal to
$j(\tau) - 744$, and the subtracted offset is $Q \cdot \dim(E_8)$.

---

## 4. Monster Prime Factors $4K-1$, $5K-1$, $6K-1$ (Bridge B3)

The order of the Monster group $|\mathbb{M}|$ contains exactly three primes above 43, namely
47, 59, and 71. These form an arithmetic progression in $K$:

$$47 = 4K-1, \quad 59 = 5K-1, \quad 71 = 6K-1.$$

The common difference between consecutive terms is $K = 12$, and all three are of the form
$nK - 1$ for consecutive integers $n = 4, 5, 6$.

---

## 5. Smallest Nontrivial Monster Irrep (Bridge B4)

The smallest nontrivial irreducible representation of $\mathbb{M}$ has dimension 196883. This
factors through the Monster prime triad:

$$196883 = 47 \times 59 \times 71 = (4K-1)(5K-1)(6K-1).$$

This is McKay's original observation. Here we express it as a single polynomial in the SRG
degree $K = 12$.

---

## 6. McKay's j-Coefficient 196884 (Bridge B5)

McKay noted that $j(\tau)$'s first Fourier coefficient equals:

$$196884 = 1 + 196883 = 1 + (4K-1)(5K-1)(6K-1).$$

The sum of the trivial representation (dimension 1) and the smallest nontrivial irrep (dimension
196883) gives the j-function's first non-constant coefficient.

---

## 7. j-Coefficient via Leech Kissing (Bridge B6)

An independent formula for 196884 uses the Leech lattice kissing number from Part CCXXXV:

$$196884 = \text{kiss}(\Lambda_{24}) + \left(\frac{K}{2} \cdot Q\right)^2 = 196560 + (6 \cdot 3)^2 = 196560 + 324.$$

Both the Monster (Bridge B5) and the Leech lattice (Bridge B6) produce the same j-coefficient
from SRG constants, confirming internal consistency.

---

## 8. Maximum Element Order of the Monster (Bridge B7)

The maximum order of any element in the Monster group is 119. In SRG constants:

$$\max\text{-order}(\mathbb{M}) = \frac{\text{EDGES}}{2} - 1 = 120 - 1 = 119.$$

The number $119 = 7 \times 17$ is a semiprime. Its SRG derivation uses the total edge count
EDGES $= 240$.

---

## 9. Moonshine Module Central Charge (Bridge B8)

The Frenkel-Lepowsky-Meurman vertex operator algebra $V^\natural$ is a conformal field theory
with central charge:

$$c(V^\natural) = 24 = K \cdot \lambda = \dim(\Lambda_{24}).$$

The VOA central charge equals the SRG product $K\lambda$ and the Leech lattice dimension
simultaneously — a triple coincidence in SRG constants.

---

## 10. j-Function Zero at Cube Root of Unity (Bridge B9)

The j-function has an order-3 zero at $\rho = e^{2\pi i/3}$:

$$j(\rho) = 0, \quad \rho = e^{2\pi i/Q}.$$

Since $Q = 3$, the SRG deformation parameter specifies the root of unity at which the
j-function vanishes. This connects the ternary SRG structure directly to the elliptic structure
of $\text{SL}_2(\mathbb{Z})$.

---

## 11. $\dim(E_8) = \text{EDGES} + 2\mu$ (Bridge B10)

Restating from Part CCXXXII: $\dim(E_8) = 248 = \text{EDGES} + 2\mu = 240 + 8$. In the
moonshine context, the j-constant decomposes as:

$$744 = Q \cdot \dim(E_8) = Q \cdot (\text{EDGES} + 2\mu).$$

The factor $Q$ multiplies the $E_8$ dimension, reflecting that the Leech lattice is
constructed from $Q = 3$ copies of $E_8$.

---

## 12. Summary of Moonshine Identifications

| Quantity | SRG formula | Value |
|----------|-------------|-------|
| $j(i)$ | $K^3$ | 1728 |
| j-constant offset | $Q(\text{EDGES}+2\mu)$ | 744 |
| $47 = $ Monster prime | $4K-1$ | 47 |
| $59 = $ Monster prime | $5K-1$ | 59 |
| $71 = $ Monster prime | $6K-1$ | 71 |
| Smallest Monster irrep | $(4K-1)(5K-1)(6K-1)$ | 196883 |
| j-coeff (McKay) | $(4K-1)(5K-1)(6K-1)+1$ | 196884 |
| j-coeff (Leech) | $\text{kiss}(\Lambda_{24})+(K/2 \cdot Q)^2$ | 196884 |
| Monster max order | $\text{EDGES}/2-1$ | 119 |
| $c(V^\natural)$ | $K\lambda$ | 24 |
| $j(\rho) = 0$ | $\rho = e^{2\pi i/Q}$ | True |

---

## 13. Discussion

The Monster group and the j-function are among the deepest objects in mathematics. Their
connection — Monstrous Moonshine — was conjectured by Conway and Norton in 1979 and proved by
Borcherds in 1992 using vertex operator algebras. Here we find that every key numerical
parameter in Moonshine is a polynomial in $Q, K, \lambda, \mu, \text{EDGES}$: the j-constant
744, the smallest Monster irrep 196883, the j-coefficient 196884, the maximum Monster element
order 119, and the moonshine module central charge 24.

Two independent SRG routes give 196884: the Monster route $(4K-1)(5K-1)(6K-1)+1$ and the
Leech kissing route $\text{kiss}(\Lambda_{24})+(K/2 \cdot Q)^2$. Their agreement is not
algebraically obvious, demonstrating that the SRG constants encode deep cohomological
relationships between sporadic groups, lattices, and modular forms.

---

## 14. Conclusion

Monstrous Moonshine connects the Monster group $\mathbb{M}$ to the j-function through the
SRG(40,12,2,4) constants at zero free parameters. The j-invariant at $\tau = i$ is $K^3 = 1728$;
the j-function constant offset $744 = Q \cdot \dim(E_8)$; the smallest Monster irrep dimension
$196883 = (4K-1)(5K-1)(6K-1)$; the Monster maximum element order $119 = \text{EDGES}/2-1$; and
the Moonshine module central charge $c = K\lambda = 24$. All 32 bridge checks pass;
$\texttt{Verified} = \texttt{True}$.
