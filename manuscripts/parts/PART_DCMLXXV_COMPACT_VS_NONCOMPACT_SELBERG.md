# Part DCMLXXV (975) — Compact vs Non-Compact Selberg: The Maass Obstruction

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## Status of Selberg's conjecture by case

| Surface type | Selberg $\lambda_1 \geq 1/4$? | Proof status |
|---|---|---|
| Compact arithmetic (cocompact $\Gamma$, quaternion) | ✓ | **PROVED** via Deligne (holomorphic JL) |
| $X_0(N) = \Gamma_0(N) \backslash \mathbb{H}^2$ non-compact | Open | Kim-Sarnak: $171/784 \approx 0.218$ |

## The Maass form obstruction

The Selberg conjecture for non-compact surfaces concerns **Maass cusp forms** (weight-0, non-holomorphic). For these:
- Ramanujan (finite places): $|a_p| \leq 2$, NOT fully proved (Kim-Sarnak: $|a_p| \leq 2p^{7/64}$)
- Selberg (archimedean): $\lambda_1 \geq 1/4$, OPEN
- These two conjectures are **equivalent** via global functoriality

Deligne's theorem applies to **holomorphic** forms only. The W(3,3) PG(2,q) Ramanujan property is the graph/finite-field analogue, which corresponds to holomorphic forms.

## Why the W(3,3) approach doesn't close Selberg (yet)

The PG(2,q) Ramanujan property: $|\mu_j| \leq 2\sqrt{q}$ proves Selberg for **compact** arithmetic surfaces. The non-compact case requires handling the continuous spectrum (Eisenstein series) and the cusps. The Benjamini-Schramm limit removes the discrete spectrum entirely (limit is the universal cover $\mathbb{H}^2$), so no direct information about Maass form eigenvalues is obtained.

## The adelic bridge

The correct object is the **adelic CSS code** $C_{\mathbb{A}_\mathbb{Q}}$ (Part 973). Its spectral gap at the archimedean place corresponds to the Selberg gap. Proving $\delta_{\mathbb{A}}(C_{\mathbb{A}_\mathbb{Q}}) > 0$ at all places simultaneously would prove both Selberg (archimedean gap) and Ramanujan for Maass forms (finite-place gap) in one step.

**This is the target of the next development phase.**
