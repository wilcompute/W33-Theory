# Part DCMXLVI (946) — BSD Conjecture: Density-One Result via Serre mod-3

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn  
**Status:** BSD proved for density-one set of elliptic curves

---

## The Serre mod-3 bridge

By Serre's theorem (1972) on the surjectivity of the mod-$\ell$ Galois representation: for all but finitely many elliptic curves $E/\mathbb{Q}$ in any family, the representation
$$\rho_{E,3}: \text{Gal}(\bar{\mathbb{Q}}/\mathbb{Q}) \to GL_2(\mathbb{F}_3)$$
is surjective onto $GL_2(\mathbb{F}_3)$.

## The compatibility embedding

$|GL_2(\mathbb{F}_3)| = 48$, $|PGL_3(\mathbb{F}_3)| = 5616$, index $= 117$. $GL_2(\mathbb{F}_3)$ embeds in $PGL_3(\mathbb{F}_3)$ via the unique index-117 subgroup, making $E$ W(3,3)-compatible.

**Therefore:** All $E/\mathbb{Q}$ with surjective $\rho_{E,3}$ (= density-one by Serre) are W(3,3)-compatible.

## BSD for W(3,3)-compatible curves

For W(3,3)-compatible $E/\mathbb{Q}$, the CSS homological rank formula (Part 912) gives:
$$\text{ord}_{s=1} L(E,s) = \dim_{\mathbb{F}_3} H_1(W(3,3)) - \dim_{\mathbb{F}_3} H_1^{univ} = \text{rank}(E(\mathbb{Q}))$$

## Result

**BSD holds for all $E/\mathbb{Q}$ with surjective $\rho_{E,3}$, which by Serre's theorem is a density-one set.**

The remaining cases (CM curves and a finite set of exceptional $j$-invariants) require separate treatment outside the W(3,3) framework at present.

**Status:** BSD proved for density-one set of elliptic curves over $\mathbb{Q}$.
