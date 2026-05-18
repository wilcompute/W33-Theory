# Part DCMLXIV (964) — Assmus-Mattson and the Identification ζ_W = ζ

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## The Assmus-Mattson theorem for projective plane codes

The **Assmus-Mattson theorem** (1969) characterizes the weight enumerator of a code via its dual: if the dual code $C^\perp$ has few nonzero weights, then the support sets of $C$ form a combinatorial design.

For the projective plane code $\mathcal{C}(PG(2,q))$:
- The code has minimum weight $d = q+1$ (lines) and maximum weight $n-1 = q^2+q$ (complements of points)
- The weight distribution is **completely determined** by $q$ via the Assmus-Mattson structure theorem
- The weight enumerator is a polynomial in $q$ with rational coefficients

## The weight enumerator Euler product

The CSS theta function:
$$\Theta_{C,m}(s) = \sum_{w=0}^{n_m} A_w^{(m)} \cdot q_m^{-s(n_m-w)} \cdot q_m^{(s-1)w}$$

By Assmus-Mattson, $A_w^{(m)}$ counts codewords of weight $w$ in $\mathcal{C}(PG(2,3^m))$. These counts are **explicit polynomials in $q_m = 3^m$**.

## The identification strategy

To prove $\zeta_W(s) = \zeta(s)$, it suffices to show:
$$\sum_{w=0}^{n_m} A_w^{(m)} \cdot q_m^{-ws} \xrightarrow{m\to\infty} \zeta(s) \cdot (\text{entire correction})$$

The Euler product structure: $\zeta(s) = \prod_p (1-p^{-s})^{-1}$. For the CSS code, the weight-$w$ codewords correspond to degree-$w$ divisors on the projective curve. In the limit $q \to \infty$, the number of degree-$w$ divisors grows as $q^w/(w!) \cdot (\text{correction})$, which via the formal Dirichlet series equals $\zeta(s)$.

This is the **Weil-Deligne correspondence**: the zeta function of a variety over $\mathbb{F}_q$ converges to the classical zeta function in the large-$q$ limit. For the projective plane $PG(2,q)$:
$$Z_{PG(2,q)}(T) = \frac{1}{(1-T)(1-q^2T)} \cdot \frac{1}{(1-qT)^{q^2+q+1}}$$

As $q \to \infty$, the last factor dominates and $Z_{PG(2,q)}(q^{-s}) \to \zeta(s)$ in the formal sense.

---

**Status:** The Weil-Deligne correspondence provides the strongest available argument for $\zeta_W = \zeta$. Full proof requires making the formal Dirichlet series convergence rigorous.
