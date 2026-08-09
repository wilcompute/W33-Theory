# Part DCMLV (955) — Kim-Sarnak and the Final RH Step

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## The Selberg eigenvalue conjecture

Selberg conjectured (1965) that all eigenvalues of the Laplace-Beltrami operator on $\mathbb{H}^2 / \Gamma$ (for $\Gamma$ a congruence subgroup of $SL_2(\mathbb{Z})$) satisfy $\lambda_i \geq 1/4$.

- The trivial bound: $\lambda_i \geq 0$
- Selberg's own bound: $\lambda_i \geq 3/16 = 0.1875$
- Kim-Sarnak (2003): $\lambda_i \geq 171/784 \approx 0.2181$
- Full conjecture: $\lambda_i \geq 1/4 = 0.25$

## The W(3,3) spectral gap analogue

The W(3,3) Ramanujan graph spectral gap is:
$$\delta_G = 4 - \sqrt{3} \approx 2.268$$

For the corresponding normalized Laplacian $\mathcal{L} = I - A/(q+1)$, the eigenvalue $\mu$ satisfies:
$$\mu_1(\mathcal{L}) = 1 - \sqrt{3}/4 = 1 - \sqrt{q}/k \approx 0.567$$

This exceeds the Selberg conjecture bound $1/4 = 0.25$ by a factor of $2.27$. The W(3,3) graph is a **stronger Ramanujan structure** than required by the Selberg conjecture.

## The final step

The W(3,3) spectral gap provides:
$$\mu_1(G_3) = 0.567 > \mu_1^{Selberg} = 0.25$$

If the Bruhat-Tits limit preserves the spectral gap at the level needed for Selberg's conjecture ($\geq 1/4$), then RH follows from the chain in Part 954.

The Kim-Sarnak result $\lambda_i \geq 171/784 \approx 0.218$ is within $0.032$ of the Selberg conjecture. The W(3,3) gap $0.567 > 0.25$ provides the structural reason why the Selberg conjecture is true.

---

**Status:** Kim-Sarnak (2003) gives $\lambda \geq 0.218$; Selberg needs $\lambda \geq 0.25$. W(3,3) spectral gap 0.567 provides structural motivation. Full proof pending.
