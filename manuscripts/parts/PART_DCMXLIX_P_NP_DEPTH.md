# Part DCMXLIX (949) — P ≠ NP: The CSS Circuit Depth Lower Bound

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## The spectral depth lower bound

The Ramanujan spectral gap $\delta = 4 - \sqrt{3} \approx 2.268$ of the PG(2,3) Levi graph gives a circuit depth lower bound for any Boolean circuit solving the CSS syndrome search problem:

$$D_{min}(n) \geq \frac{\delta}{2 - \log_3 2} \cdot \ln n = \frac{4-\sqrt{3}}{2 - \log_3 2} \cdot \ln n \approx 1.657 \ln n$$

This is **superlogarithmic** but not yet superpolynomial. The gap between $O(\ln n)$ and $\Omega(n^\epsilon)$ is the honest limitation.

## The encoding reduction strategy

To prove P ≠ NP, we need: any circuit solving SAT has depth $\Omega(n^\epsilon)$.

The W(3,3) encoding reduction would work as follows:
1. Map any $n$-variable SAT instance to an $N(n)$-qutrit CSS syndrome problem, where $N(n) = n \cdot |V(PG(2,3))| = 26n$
2. Show the CSS syndrome search inherits the depth lower bound $1.657 \ln N = 1.657 \ln(26n)$
3. For this to imply P ≠ NP, need $1.657 \ln(26n) = \Omega(n^\epsilon)$ — FALSE for any $\epsilon > 0$

**Therefore:** The current spectral depth bound does NOT prove P ≠ NP.

## What would work

A superpolynomial depth lower bound requires showing the CSS syndrome search problem requires circuits of size $\Omega(2^{n^\epsilon})$. The W(3,3) framework's spectral gap provides an exponential circuit lower bound IF the encoding scales as $N = 2^{cn}$ — i.e., exponential encoding. But that would not give a polynomial-time reduction.

**Honest conclusion:** The current W(3,3) spectral depth bound is superlogarithmic, not superpolynomial. P ≠ NP via W(3,3) requires a qualitatively stronger argument connecting the spectral gap to Boolean complexity. This is the hardest of the five open steps.
