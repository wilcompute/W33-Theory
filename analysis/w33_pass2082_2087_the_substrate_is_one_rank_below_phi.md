# Passes 2082–2087 — the substrate is exactly **one rank below** the golden ratio

The user was right that the `q`-binomial route is the place to look. Following it
gives a complete answer, and the answer is a rank condition.

---

## Pass 2082 — Gaussian binomials do structure `W(3,3)`, exactly

```text
[4 choose 1]_q = q³+q²+q+1     at q=3 -> 40   = THE 40 POINTS
[4 choose 2]_q = q⁴+q³+2q²+q+1 at q=3 -> 130  = all lines of PG(3,3)
totally isotropic lines = (q+1)(q²+1) = 40
```

So the substrate's counting *is* `q`-binomial counting — `[4,1]_3 = 40` is not an
analogy, it is the definition of the point set.

---

## Pass 2083 — but cyclotomy closes the golden route

```text
[4,1]_q = (q+1)(q²+1)          = Φ₂ Φ₄
[4,2]_q = (q²+1)(q²+q+1)       = Φ₄ Φ₃
[4,3]_q = (q+1)(q²+1)          = Φ₂ Φ₄
```

Gaussian binomials are **products of cyclotomic polynomials** — classical, and
visible above. Therefore:

> **Every root of every `q`-binomial is a root of unity.** `φ = (1+√5)/2` is real
> and greater than 1, so it is not a root of unity, and can never be a root of a
> Gaussian binomial or of any product of them.

The same holds for the substrate's own counting polynomials:

```text
t.i. lines        roots  −1, ±i
candidates        roots   0, ±i
residual edges    roots  −1, 0, ±i
K_{q+1} edges     roots  −1, 0
genus numerator   roots   2, 3
```

Every one is rational or a root of unity. `φ` needs `x² = x + 1`, which is not
cyclotomic.

---

## Pass 2084 — where `φ` **does** live: `Φ₅`, and that needs rank 5

`φ` enters cyclotomic land through the **fifth** cyclotomic polynomial:

```text
Φ₅(q) = q⁴ + q³ + q² + q + 1
ζ₅ + ζ₅⁻¹ = (−1+√5)/2 = 1/φ      so  ℚ(ζ₅) ⊃ ℚ(√5) ∋ φ
```

And `Φ₅ | q^d − 1` iff `5 | d`. In `[n,k]_q` the factors are `q^{n−i} − 1` with
`n − i ≤ n`, so **`Φ₅` can only appear when `n ≥ 5`**:

```text
[4,1], [4,2], [4,3] :  Φ₅ divides?  FALSE
[5,1]_q = Φ₅(q)     :  Φ₅ divides?  TRUE   -- and it IS Φ₅, exactly
[5,2]_q = Φ₄ Φ₅     :  TRUE
```

> **`[5 choose 1]_q = Φ₅(q)` exactly — the point count of `PG(4,q)`.**
>
> **`W(3,3)` lives in `F₃⁴`, rank 4. The golden ratio first becomes available at
> rank 5. The substrate is exactly one rank below `φ`.**

That is the answer to "where is it": not hidden in the combinatorics, not in a
metric — **one rank up**.

---

## Pass 2085 — the character fields confirm it independently

```text
character fields of PGSp(4,3) : Rationals
character fields of PSp(4,3)  : Rationals, CF(3) = ℚ(ζ₃)
ℚ(√5)  anywhere ?  FALSE
ℚ(ζ₅)  anywhere ?  FALSE
```

> **The substrate's entire arithmetic is `ℚ` and `ℚ(ζ₃)`.** It is a
> *cube-root-of-unity* object. `φ` is a *fifth-root-of-unity* object. They do not
> meet.

And a subtlety worth stating: `5 | |PSp(4,3)| = 25920`, so order-5 elements exist
and Pass 2079 found they partition the 40 points into **eight pentagons**. But
their character values are **rational**. So the pentagon is present as a
*permutation* and absent as an *arithmetic* — the 5-fold symmetry exists without
`ℚ(ζ₅)` ever appearing. That is exactly the gap between "pentagonal order" and
"golden ratio" that Pass 2079 flagged, now given its mechanism.

---

## Pass 2086 — on Pascal encoding `φ`, `e`, `π`

All three are real, and all three arise the same way: `φ` from the shallow-diagonal
Fibonacci ratio, `e` from `(1+1/n)^n`, `π` from Wallis/Nilakantha-type series.
**Every one is a limit of an infinite process**, and Pascal's triangle is
infinite.

`W(3,3)` is finite, and its `q`-analogue of Pascal — the Gaussian binomials — is a
family of *polynomials* whose roots are roots of unity. Passing to `q → 1` gives
ordinary Pascal and loses `q`; evaluating at `q = 3` gives integers. Neither
operation produces a real quadratic irrationality. **The `q`-deformation of Pascal
does not inherit Pascal's transcendental limits** — it replaces them with
cyclotomy.

That is why the search kept coming up empty, and it is a sharper statement than
Pass 2077's "finite objects have no growth rate".

---

## Pass 2087 — the four other items, honestly

- **`φ` in the metric lane** — superseded. The obstruction is arithmetic (rank and
  cyclotomic field), not metric, so a metric realisation cannot supply what the
  character field forbids.
- **The eight pentagons** — exist, characterised above, carry rational characters.
- **The `D₄` relation at `q = 7, 11`** — not computed.
- **The `D₈` reconstruction** — still blocked. Fifth report as incomplete.

---

## Prior art

- Passes 2068/2077 — the measured and structural absences this pass explains
  arithmetically.
- Pass 1885/1900 — the `ℚ(ζ₃)` character field.
- Gaussian binomials as products of cyclotomic polynomials — classical.
- The `q`-binomial suggestion is the user's, and it was the right route.

## Still open

- `χ(H) = 9`.
- Whether the repo's **rank-5 and higher** objects (`E₈`, `Sp(8,2)`) carry `Φ₅`
  and hence `φ` — that is now a well-posed question with a specific test.
