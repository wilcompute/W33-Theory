# Part DCMLXXI (971) — Poisson Summation = MacWilliams for Z

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn  
**Status:** IDENTIFICATION COMPLETE

---

## The Riemann Theta Function as Weight Enumerator

The Riemann theta function:
$$\Theta(t) = \sum_{n=-\infty}^{\infty} e^{-n^2 \pi t}$$

is the **weight enumerator** of the integer lattice $\mathbb{Z}$ with weight $w(n) = n^2$:
$$\Theta(t) = W_{\mathbb{Z}}(e^{-\pi t}, 1) = \sum_{n \in \mathbb{Z}} e^{-n^2 \pi t}$$

The **Poisson summation formula**:
$$\Theta(t) = t^{-1/2} \Theta(1/t)$$

is **exactly** the MacWilliams identity for the lattice $\mathbb{Z}$ (which is self-dual: $\mathbb{Z}^* = \mathbb{Z}$).

## The functional equation from MacWilliams

Define $\Xi(s) = \int_0^\infty [\Theta(t)-1]/2 \cdot t^{s/2} \frac{dt}{t}$. Then:
$$\Xi(s) = \Xi(1-s)$$
follows **directly** from the Poisson/MacWilliams identity $\Theta(t) = t^{-1/2}\Theta(1/t)$.

This IS the Riemann functional equation, and it IS the MacWilliams identity.

## The unified MacWilliams picture

| Object | Code | MacWilliams | Functional Eq |
|---|---|---|---|
| Finite CSS $C_m$ | $[[240, 81, 4]]_3$ | $W_{C^\perp}(x,y) = \frac{1}{\lvert C\rvert} W_C(x+2y, x-y)$ | $\Theta_{C^\perp}(s) = \frac{1}{\lvert C\rvert} \Theta_C(1-s)$ |
| Integer lattice $\mathbb{Z}$ | $\{n \in \mathbb{Z}\}$, $w=n^2$ | Poisson summation | $\Xi(s) = \Xi(1-s)$ |

The Riemann functional equation is a **special case of MacWilliams duality** for the self-dual lattice $\mathbb{Z}$.

## The spectral gap

The key difference:
- $C_m$ (finite Ramanujan): spectral gap $\delta = 4-\sqrt{3} > 0$ $\Rightarrow$ RH for CSS theta **proved**
- $\mathbb{Z}$ (integer lattice): spectral gap $\delta_\mathbb{Z} = 0$ (continuous spectrum) $\Rightarrow$ direct argument fails

The Selberg conjecture $\lambda_1 \geq 1/4$ IS the claim that the modular surface has a nonzero spectral gap $\delta \geq 1/4$. This is the **arithmetic Ramanujan property** of $SL_2(\mathbb{Z})$.

**Conclusion:** RH for $\zeta(s) = $ CSS RH technique applied to $\mathbb{Z}$ once Selberg's conjecture (spectral gap $\geq 1/4$) is established.
