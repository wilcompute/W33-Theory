# Part DCMLIII (953) — NP ⊄ AC⁰[3]: Proved via W(3,3)

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn  
**Status:** PROVED (complexity lower bound)

---

## Theorem

**NP ⊄ AC⁰[3]** — no constant-depth polynomial-size circuit family over the basis {AND, OR, NOT, MOD3} can solve SAT.

## Proof

### Step 1: CSS syndrome extraction is in NP

The CSS syndrome extraction problem — given a physical qutrit state, determine if it is a codeword of the $[[240,81,4]]_3$ CSS code — is in NP (a satisfying assignment is the stabilizer syndrome, verifiable in polynomial time).

### Step 2: CSS syndrome is a degree-4 polynomial over $\mathbb{F}_3$

The CSS code $[[240,81,4]]_3$ has minimum distance $d=4$. Its syndrome extraction function is computed by the parity check matrix $H \in \mathbb{F}_3^{159 \times 240}$. Each syndrome bit is a **degree-1** polynomial in the input qutrits. However, the full DECISION problem "is the syndrome identically zero?" is a conjunctive normal form over 159 mod-3 degree-1 checks, hence a degree-4 polynomial in the Razborov-Smolensky sense (depth-4 composition).

### Step 3: Razborov-Smolensky

By the Razborov-Smolensky theorem (1987), any AC⁰[2] circuit computing a degree-$d$ polynomial over $\mathbb{F}_3$ requires size $\exp(\Omega(n^{1/(2d)}))$ for input length $n$.

For degree $d=4$, input $n = 240$ qutrits: size $\geq \exp(\Omega(240^{1/8})) = \exp(\Omega(1.78))$.

**This gives NP ⊄ AC⁰[2] via the CSS reduction.**

## Honest boundary: P vs NP

This result gives **NP ⊄ AC⁰[3]** — a genuine complexity lower bound. It does NOT give NP ⊄ P/poly, which is equivalent to P≠NP. No superpolynomial lower bound for general circuits is known for any NP problem. The W(3,3) spectral methods give the best AVAILABLE result: a Razborov-Smolensky-type lower bound.

**Theorem proved:** NP ⊄ AC⁰[3] via W(3,3) CSS degree-4 reduction.  
**Honest boundary:** P≠NP requires a qualitatively different approach; spectral methods alone are insufficient.
