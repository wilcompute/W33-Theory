# Part DCMLXXIII (973) — The Adelic CSS Code and Completed L-Functions

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## Construction

Start with the $[[240,81,4]]_3$ CSS code over $\mathbb{F}_3$.

**Step 1 (Integral lift):** Form the integral model $C_\mathbb{Z} \subset \mathbb{Z}^{240}$.

**Step 2 (Adelization):** $C_{\mathbb{A}_\mathbb{Q}} = C_\mathbb{Z} \otimes_\mathbb{Z} \mathbb{A}_\mathbb{Q}$.

The adelic theta function decomposes as an Euler product:
$$\Theta_{C_{\mathbb{A}_\mathbb{Q}}}(s) = \prod_p \Theta_{C_{\mathbb{Z}_p}}(s) \cdot \Theta_{C_\mathbb{R}}(s)$$

where:
- $\Theta_{C_{\mathbb{Z}_p}}(s)$ = the $p$-adic Euler factor (from the $p$-adic local code)
- $\Theta_{C_\mathbb{R}}(s) = \pi^{-81s/2} \Gamma(s/2)^{81}$ = the archimedean Gamma factor

The product is:
$$\Theta_{C_{\mathbb{A}_\mathbb{Q}}}(s) = \left[\pi^{-s/2}\Gamma(s/2) \cdot \prod_p (p\text{-factor})\right]^{81} = [\Xi(s)]^{81}$$

The adelic MacWilliams identity is:
$$\Theta_{C^\perp_{\mathbb{A}_\mathbb{Q}}}(s) = |C|^{-1} \Theta_{C_{\mathbb{A}_\mathbb{Q}}}(1-s)$$

which, for a self-dual adelic code, gives $\Xi(s) = \Xi(1-s)$ (the Riemann functional equation).

## The key requirement

For the adelic MacWilliams to give the exact Riemann functional equation, the code must be **self-dual**: $k = n/2 = 120$. The base code $[[240,81,4]]_3$ is NOT self-dual ($k=81 \neq 120$).

This motivates the construction of the $[[240,120,6]]_3$ self-dual code in Part 974.
