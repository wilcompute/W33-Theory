# Part DCMLXXVII (977) — The Möbius Symmetry Axis and Why PG(2,q) is Correct

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## The ternary MacWilliams as a Möbius transformation

The ternary MacWilliams identity maps:
$$t \mapsto \frac{1-t}{1+2t}$$
(the Möbius transformation with fixed points $t^* = \frac{-1 \pm \sqrt{3}}{2}$)

For the weight enumerator: $W_C(1,t) = \frac{(1+2t)^n}{3^k} W_C\!\left(1, \frac{1-t}{1+2t}\right)$

The **symmetry axis** of the ternary MacWilliams is NOT $|t| = 1$ (which would correspond to $\text{Re}(s) = 1/2$). It is the fixed point circle of the Möbius transformation $t \mapsto (1-t)/(1+2t)$.

The fixed point $t^* = (-1+\sqrt{3})/2 \approx 0.366$ corresponds to:
$$3^{-s} = t^* \Rightarrow s = \frac{\log(2/(\sqrt{3}-1))}{\log 3} \approx 0.915$$

**This is real, not $1/2$.** The ternary theta for a self-dual code has zeros on a curve $\text{Re}(s) = 0.915\ldots$, NOT $\text{Re}(s) = 1/2$.

## Why PG(2,q) is the correct framework

The PG(2,q) CSS code from Parts 933–963 does NOT use a self-dual code. Instead:
- $C_1 = $ row space of incidence matrix $H$ of $PG(2,q)$
- $C_2 = C_1^\perp$ (the dual code)
- CSS code $[[n, k_1 - k_2, d]]$ where $d = \min(d_1, d_2^\perp)$

The **MacWilliams pair** $(C_1, C_2 = C_1^\perp)$ satisfies:
$$\Theta_{C_2}(s) = \Theta_{C_1^\perp}(s) = \frac{1}{|C_1|} \cdot \Theta_{C_1}(1-s) \cdot (\text{q-factor})$$

The functional equation $\Theta_{C_1^\perp}(s) = |C_1|^{-1} \Theta_{C_1}(1-s)$ gives the Riemann-type symmetry $s \leftrightarrow 1-s$ **only when** the substitution is correctly normalized so that $q^{-s}$ appears in a specific way.

The normalization proved in Part 959 uses:
$$\tilde{\Theta}_{C}(s) := q^{-k s/2} W_C(q^{s/2}, q^{(1-s)/2})$$
for which the MacWilliams gives:
$$\tilde{\Theta}_{C^\perp}(s) = \tilde{\Theta}_C(1-s)$$
**exactly** (no extra factors). This is the functional equation used throughout the series.

## The palindromic requirement

For $\tilde{\Theta}_C(s) = \tilde{\Theta}_C(1-s)$ (self-dual theta), need $A_w = A_{n-w}$ (palindromic weight distribution). The $[12,6,6]_3$ Golay code is **not** palindromic ($A_0 = 1 \neq 24 = A_{12}$), so its normalized theta is NOT self-symmetric.

**The correct object for the Riemann functional equation is the CSS pair $(C_1, C_1^\perp)$ where the pair satisfies $\tilde{\Theta}_{C_1^\perp}(s) = \tilde{\Theta}_{C_1}(1-s)$, which holds for ANY code and its dual.** The PG(2,q) construction is correct.
