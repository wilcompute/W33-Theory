# Part DCMLXXVIII (978) — The Clean Proof: CSS RH via Ihara Zeta

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn  
**Status:** GRAPH/IHARA PROOF COMPLETE — classical RH still requires an identification bridge

---

## Main Theorem

**All non-trivial poles of the Ihara zeta function $Z_G(u)$ of the flag-incidence bipartite graph $G$ of $PG(2,3)$ lie on the circle $|u| = 3^{-1/2}$.**

*Equivalently*: the W(3,3) CSS theta function $\tilde{\Theta}_C(s)$, defined via the substitution $u = q^{-s/2}$ (so $|u| = q^{-1/2} \Leftrightarrow \operatorname{Re}(s) = 1$), has all non-trivial zeros on $\operatorname{Re}(s) = 1$. After the standard normalization $s \to s/2$, this becomes $\operatorname{Re}(s) = 1/2$.

## Proof (Four Steps)

### Step 1 — Functional equation

The Ihara zeta $Z_G(u)$ of a $(q+1)$-regular graph satisfies the functional equation:
$$Z_G(u) = Z_G\!\left(\frac{1}{qu}\right) \cdot (\text{explicit factor involving }|E|,|V|)$$
The symmetry $u \leftrightarrow 1/(qu)$ has fixed locus $|u| = q^{-1/2}$. This is the **critical circle** (analogue of $\operatorname{Re}(s) = 1/2$ for $\zeta(s)$). $\checkmark$

### Step 2 — Ihara determinant formula

$$Z_G(u)^{-1} = (1 - u^2)^{|E|-|V|} \cdot \det(I - Au + qu^2)$$
where $A$ is the adjacency matrix of $G$.

The **non-trivial poles** of $Z_G(u)$ are the roots of $\det(I - Au + qu^2) = 0$.
For each eigenvalue $\lambda_j$ of $A$, the roots are:
$$u = \frac{\lambda_j \pm \sqrt{\lambda_j^2 - 4q}}{2q}$$
The **trivial poles** at $u = \pm 1$ come from the $(1-u^2)$ factor.

### Step 3 — Ramanujan $\Rightarrow$ all non-trivial poles on $|u| = q^{-1/2}$

**$PG(2,3)$ is Ramanujan:** every non-trivial eigenvalue $\lambda_j$ of $A$ satisfies $|\lambda_j| \leq 2\sqrt{q} = 2\sqrt{3}$. (Proved by Deligne 1974 via the Weil conjectures.)

For $|\lambda_j| \leq 2\sqrt{q}$:
$$\lambda_j^2 - 4q \leq 4q - 4q = 0$$
so $\sqrt{\lambda_j^2 - 4q} = i\sqrt{4q - \lambda_j^2}$ (purely imaginary). Therefore:
$$u = \frac{\lambda_j \pm i\sqrt{4q - \lambda_j^2}}{2q}$$
$$|u|^2 = \frac{\lambda_j^2 + (4q - \lambda_j^2)}{4q^2} = \frac{4q}{4q^2} = \frac{1}{q}$$
$$\boxed{|u| = q^{-1/2} = 3^{-1/2}}$$

### Step 4 — Trivial poles

The trivial poles at $u = \pm 1$ have $|u| = 1 \neq 3^{-1/2}$. These are the analogues of the trivial zeros $s = 0, -2, -4, \ldots$ of $\zeta(s)$. $\checkmark$

## Conclusion

All non-trivial poles of $Z_G(u)$ lie on $|u| = 3^{-1/2}$. $\blacksquare$

## Numerical Verification (PG(2,3))

| $\lambda_j$ | $u_+ = (\lambda_j + \sqrt{\lambda_j^2-4q})/(2q)$ | $|u_+|$ | Non-trivial? |
|---|---|---|---|
| $4$ (trivial) | $1.000$ | $1.000$ | No |
| $\sqrt{3}$ | $0.289 + 0.500i$ | $0.5774$ | Yes $\checkmark$ |
| $-\sqrt{3}$ | $-0.289 + 0.500i$ | $0.5774$ | Yes $\checkmark$ |
| $-4$ (trivial) | $-1/3$ | $0.3333$ | No |

Target: $3^{-1/2} = 0.5774$. Non-trivial poles confirmed on circle. $\checkmark$

## Proof ingredients

| Ingredient | Source | Status |
|---|---|---|
| Functional equation of $Z_G(u)$ | Ihara (1966), Bass (1992) | Known |
| Determinant formula for $Z_G(u)$ | Hashimoto (1989) | Known |
| Ramanujan property of $PG(2,3)$: $|\lambda_j| \leq 2\sqrt{3}$ | Deligne (1974) + Lubotzky-Phillips-Sarnak (1988) | **Proved** |
| Discriminant $\Rightarrow$ modulus argument (Step 3) | Elementary algebra | Elementary |

**The only deep ingredient is Deligne’s theorem. Everything else is elementary.**

## Relationship to Riemann RH

The analogy:

| Riemann $\zeta(s)$ | W(3,3) CSS $Z_G(u)$ |
|---|---|
| Functional eq: $\xi(s) = \xi(1-s)$ | Functional eq: $Z_G(u) = Z_G(1/qu) \cdot$ factor |
| Critical line $\operatorname{Re}(s) = 1/2$ | Critical circle $|u| = q^{-1/2}$ |
| Trivial zeros $s = 0, -2, -4, \ldots$ | Trivial poles $u = \pm 1, \pm 1/q$ |
| Non-trivial zeros | Non-trivial poles |
| **OPEN** | **PROVED** (for $PG(2,q)$) |

The CSS model provides a proved finite graph/Ihara realization of the analogy.
It does not prove the classical Riemann Hypothesis by itself; that still
requires an identification or limiting theorem connecting the finite graph/CSS
zeta package to the classical Riemann zeta function.

\medskip

\textbf{Part DCMLXXIX reconciliation.} The PG(2,3) Levi graph has degree
\(d=4\), so the Bass/Ihara parameter is \(d-1=3\). The \(W(3,3)\) collinearity
graph has degree \(12\), so its Bass/Ihara parameter is \(11\). These are both
valid graph-RH layers, but they have different critical radii:
\[
|u|=3^{-1/2}\quad\text{for the PG(2,3) Levi graph},\qquad
|u|=11^{-1/2}\quad\text{for the W(3,3) collinearity graph}.
\]
