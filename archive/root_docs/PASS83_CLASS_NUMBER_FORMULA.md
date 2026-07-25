# Pass 83 — The graph analytic class number formula: W(3,3) as an F₁-curve

**Status: PASS** — witness `w33_pass83_class_number_formula.py` (7/7 checks incl. a sympy symbolic
verification), test `tests/test_pass83_class_number_formula.py` (5/5). Self-contained.

A synthesis pass: it fuses three separately-established results into one arithmetic-geometry
dictionary via the **graph analytic class number formula**.

## The formula
Write the reciprocal Ihara zeta in Bass form,
`1/ζ_G(u) = (1−u²)^{m−n} · det(I − Au + qu²)`, with q = k−1 = 11, m = 240, n = 40.

- **Order of vanishing at u=1 = the first Betti number** β = m − n + 1 = **201** (the cycle rank —
  the graph's "genus"). Verified symbolically in sympy (order 201).
- **Special value (leading coefficient) = a class number formula:**
  `lim_{u→1} 1/ζ_G(u)/(1−u)²⁰¹ = 2^{m−n}·(1−q)·n·κ(G) = −2²⁸⁵·5²⁵`, and the topology-free reduced
  form `lim_{u→1} det(I−Au+qu²)/(1−u) = −(q−1)·n·κ(G) = −400·κ = −2⁸⁵·5²⁵`,
  where **κ(G) = #spanning trees = 2⁸¹·5²³ = |critical group K(W)|** (Pass 82).

## The F₁ arithmetic dictionary
| number-field / curve side | W(3,3) graph side |
|---|---|
| Dedekind / Selberg zeta | Ihara zeta ζ_G(u) (Pass 73/74) |
| Riemann Hypothesis | Ramanujan: poles on \|u\|=1/√11 (Pass 73) |
| functional equation | u ↦ 1/(11u) pole involution (Pass 74) |
| genus / rank (order of vanishing at u=1) | first Betti number β = 201 |
| class number h | #spanning trees κ = 2⁸¹·5²³ (Pass 74) |
| ideal class group / Jacobian | **critical group K(W) = (ℤ/10)⁸⊕ℤ/40⊕(ℤ/160)¹⁴ (Pass 82)** |
| analytic class number formula | lim det(I−Au+qu²)/(1−u) = −(q−1)·n·κ |

## Why it matters
Pass 73–74 gave W(3,3) a zeta with a Riemann Hypothesis (Ramanujan) and a functional equation;
Pass 82 gave it a class group (the critical group). This pass supplies the **class number formula**
that binds them: the Ihara zeta's special value at u=1 is exactly (−(q−1)·n) times the order of the
critical group, and the order of vanishing is the graph's genus (β=201). W(3,3) thereby carries a
complete, internally-consistent "curve over F₁" arithmetic — zeta, RH, functional equation, genus,
class number, and class group, all verified.

## Files
- `w33_pass83_class_number_formula.py`, `.json` — witness + certificate (exact integer + sympy).
- `tests/test_pass83_class_number_formula.py` — 5 assertions.
