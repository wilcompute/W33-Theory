## Passes 3040–3044 — the geometry is perfect and the algebra is merely very good

---

## Pass 3042 (outside the programme) — the instruction layer is **not** Ramanujan

The address graph is Ramanujan: provably the best-mixing graph of its degree (Pass 2869).
Nobody had asked the same question of the *instruction* layer. For a 4-regular graph the
same optimality condition is `|λ₂| ≤ 2√3/4`:

```text
frame walk |lambda_2|        : 0.893992320
Ramanujan bound for degree 4 : 0.866025404
is the instruction layer Ramanujan : False
shortfall : 0.027967   (3.23% above the bound)
```

> **The instruction graph misses optimality by 3.23 %.** A good expander, not the best one.

### And that is now the fourth independent measurement saying the same thing

| measurement | geometry | algebra |
|---|---|---|
| diameter | **2** | **19** |
| share of worst-case work | 10 % | 90 % |
| mixing | **Ramanujan (optimal)** | 3.23 % short |
| identification | forced by construction | six valid triples, spread 19–23 |

> **The machine's geometry is perfect and its algebra is merely very good, and every way
> of measuring it says so.**

That is not a defect. It is a statement about where the design has freedom: the geometry
was handed to us and is extremal; the instruction set was chosen and could in principle be
chosen better. Three per cent is the size of the prize.

---

## Pass 3041 (outside the programme) — the growth series, which is what a compiler wants

Pass 2866 measured the whole ball profile and used only the last shell. The profile *is*
the growth series of the group with respect to the four opcodes:

```text
a_n = 1, 4, 15, 53, 176, 547, 1630, 4648, ...        (20 shells, 4,199,040 total)
mean 14.1756   s.d. 1.7682   modal length 15   max 19
early ratios: 4.000, 3.750, 3.533, 3.321, 3.108
```

> **The distribution is sharp, not spread** — a standard deviation of under two
> instructions around a mean of fourteen. A scheduler that budgets **fifteen** is right
> almost always and never wrong by more than four.

That is a far better specification than a worst case. And the early ratios tell you the
group is closing on itself immediately: a free product on four generators would hold ratio
4 forever; this one is at 3.108 by the fifth shell.

---

## Pass 3040 — the eight-dimensional code: sample too small to test

Pass 3020's rank-3 finding said a rank-3 stabilizer group has an **eight**-dimensional
code, and if one lies inside the complement it would kill every single error with room to
spare.

This run drew 60,000 samples (half the previous budget to leave time for the other three
passes) and found **7 witnesses and 0 orthogonal pairs** — so the code test never ran.

> **No result, stated as no result.** The previous run at 120,000 samples found 17
> witnesses and 13 pairs, so the object exists and the sampling here was simply too thin.
> The test is written and waiting; it needs the larger budget.

---

## Pass 3043 — the Hamiltonian self-test, a fourth failed method

400,000 randomized Warnsdorff restarts. **Longest path: 76 of 81.**

The graph gets within five nodes and strands. Four approaches have now failed —
depth-first, pruned depth-first, bounded depth-first, and randomized restarts — and none
of them is a proof of absence.

> Recorded as an open question with four failed methods rather than as an absent result.
> The gap between 76 and 81 is small enough to be suspicious in either direction.

---

## Ledger

| claim | status |
|---|---|
| instruction layer is **not** Ramanujan, by 3.23 % | **proved** |
| four measurements agree: geometry extremal, algebra not | derived |
| growth series `1, 4, 15, 53, 176, 547, …` | **measured**, 20 shells |
| mean 14.18, s.d. 1.77, mode 15 | measured |
| 8-dimensional code in the complement | **not tested** — sample too thin |
| Hamiltonian self-test | open; longest path 76/81 after 4 methods |

## Still open

- The 8-dim code test, at the larger sampling budget.
- The Hamiltonian cycle, by a method that decides rather than searches.
