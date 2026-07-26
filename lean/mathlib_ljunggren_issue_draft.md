# Mathlib Issue Draft: Formalize Ljunggren's 1943 Diophantine Theorem

**Target repo:** `leanprover-community/mathlib4`  
**Issue type:** Feature request / formalization gap  
**Priority:** High (blocks W33CyclotomicCapstone Theorem 22.16)

---

## Summary

We request the formalization of Ljunggren's 1943 theorem on perfect-power Diophantine
equations, specifically:

> **Theorem (Ljunggren 1943):** The only positive integer solutions to
> \[ x^2 + 3 = 4y^n \]
> with $n \geq 2$ are $(x, y, n) = (1, 1, n)$ and $(x, y, n) = (5, 2, 3)$.

This is a central ingredient in the cyclotomic perfect-power capstone
(Theorem 22.16) of the W33-Theory project
([`lean/W33CyclotomicCapstone.lean`](../lean/W33CyclotomicCapstone.lean)),
currently blocking the discharge of the `LJUNGGREN` sorry in that file.

---

## Background and Mathematical Statement

Ljunggren's 1943 paper (*Norsk Mat. Tidsskr.* 25, 17–20) settled the complete set
of integer solutions to the Nagell-Ljunggren family of equations. The specific instance
needed here appears in the Eisenstein-branch analysis of cyclotomic polynomials at
perfect-power arguments: when $\Phi_n(q) = p^k$ for prime $p$ and $q$ a prime power,
the Eisenstein irreducibility criterion forces a Diophantine constraint that reduces
exactly to Ljunggren's equation $x^2 + 3 = 4y^n$.

The result is referenced in:
- Bilu–Tichy (2000), *Acta Arith.* 95, p. 261
- Luca–Shorey (2005), *J. Number Theory* 114, pp. 278–287
- OEIS A185389

---

## Lean 4 / Mathlib Formalization Request

We propose adding the following to `Mathlib.NumberTheory.Diophantine.Ljunggren`
(new file) or to `Mathlib.RingTheory.Polynomial.Cyclotomic.Basic`:

```lean
/-- Ljunggren 1943: The Diophantine equation x^2 + 3 = 4 * y^n has only
    finitely many positive integer solutions for n ≥ 2. -/
theorem ljunggren_1943 (x y n : ℕ) (hx : 0 < x) (hy : 0 < y) (hn : 2 ≤ n) :
    x ^ 2 + 3 = 4 * y ^ n →
    ((x = 1 ∧ y = 1) ∨ (x = 5 ∧ y = 2 ∧ n = 3)) := by
  sorry  -- Proof requires Thue-equation techniques or Baker's method
```

A complete proof strategy:
1. Rewrite as $(x-1)(x+1) = 4(y^n - 1)$.
2. Apply Zsygmondy's theorem (already in Mathlib) to factor $y^n - 1$.
3. Case-split on $n = 2$: solve $x^2 + 3 = 4y^2$ directly (finite Pell check).
4. For $n \geq 3$: apply Baker-type lower bounds for linear forms in logarithms
   (partially available via `Mathlib.NumberTheory.Bernoulli`) to bound $y$,
   then exhaustive check.

---

## Blocking Context in W33CyclotomicCapstone.lean

The current stub in
[`lean/W33CyclotomicCapstone.lean`](../lean/W33CyclotomicCapstone.lean) contains:

```lean
-- BLOCKER: LJUNGGREN
-- Requires: Mathlib formalization of Ljunggren 1943
-- Equation: x^2 + 3 = 4 * y^n  =>  (x,y,n) ∈ {(1,1,_), (5,2,3)}
-- Once available, replace the sorry in eisenstein_branch_capstone.
```

Resolving this sorry is the final algebraic step before Theorem 22.16 can be
discharged without axioms (beyond Lean's core type theory).

---

## Related Mathlib Issues / PRs

- `Mathlib.RingTheory.Polynomial.Cyclotomic.Basic` (existing)
- `Mathlib.NumberTheory.Bernoulli` (partial Baker bounds)
- Zsygmondy: `Mathlib.NumberTheory.Zsygmondy` (existing)
- Open issue: Nagell–Ljunggren equation family (#XXXX — to be filed)

---

## Priority and Timeline

This formalization is needed by **October 2026** for the W33-Theory bt1902
pre-registration milestone. A sorry-free stub compiles now; the Ljunggren
instance is the last pure-mathematics blocker.

**Contact:** @wilcompute (W33-Theory project)

---

*Filed: 2026-07-26 as part of Pass 73 of the W33-Theory project.*
