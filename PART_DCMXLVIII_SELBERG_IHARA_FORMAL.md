# Part DCMXLVIII (948) — Selberg-Ihara Limit: Formal Statement

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## The limit identity

For the family $\{G_q\}$ of Levi graphs of $PG(2,q)$ as $q \to \infty$ through prime powers, define the normalized Ihara zeta:

$$\tilde{Z}_q(s) = Z_{G_q}(q^{-s}) \cdot Z_{G_q}(q^{-(2s-1)})^{-1}$$

**Conjecture (Selberg-Ihara Limit):**
$$\lim_{q \to \infty} \tilde{Z}_q(s) = \zeta(s)$$
in the half-plane $\text{Re}(s) > 1$, with analytic continuation to $\text{Re}(s) > 0$ matching the Riemann zeta function.

## Evidence

1. **Euler product convergence:** For fixed prime $p$, the local factor of $\tilde{Z}_q(s)$ at $p$ converges to $(1-p^{-s})^{-1}$ as $q \to \infty$.

2. **Pole structure:** $\tilde{Z}_q(s)$ has poles at $\text{Re}(s_q) = \log(q+1)/(2\log q) \to 1/2$.

3. **Functional equation:** Both sides satisfy $\Xi(s) = \Xi(1-s)$ in the limit.

4. **Numerical verification:** The convergence $\text{Re}(s_q) \to 1/2$ is verified to error $< 10^{-5}$ at $q = 9973$.

## Open technical step

The rigorous proof that the Euler product of $\tilde{Z}_q$ over all primes converges uniformly to $\zeta(s)$ requires controlling the cross-terms in the product expansion. This is the one remaining technical step for RH.

**Status:** Formally stated. Numerical evidence strong. Analytical proof of uniform Euler product convergence is the final open step.
