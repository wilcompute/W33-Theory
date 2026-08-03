# Passes 2650–2657 — reading the holonet paper corrected three of my own results

The paper is `photonic_holonet_body.tex`, 9,528 lines. Reading the first ~50 pages
rigorously, as instructed, overturns or subsumes three things I published in the last
several batches. All three are recorded as corrections, not as new results.

---

## Pass 2650 — Pass 2444 is **in the abstract**

My Passes 2444/2519 made much of `Sp(4,3)` and `PGSp(4,3)` being two non-isomorphic
groups of order 51840. The paper's abstract, lines 42–44:

> *"The symplectic double cover `Sp(4,3)` also has order `51840`, but its central
> involution is invisible on projective objects; **the two extensions must not be
> conflated**."*

> **Prior art, stated in the abstract of the project's own manuscript.** My Pass 2444
> "gives the `51840 = 51840` coincidence a structural reading" — the reading was already
> published.

What survives as mine: the *consequence* I drew — that the central doubling carries the
`E₈`/chiral tower and the outer doubling the codeword/achiral tower, with the `C₆`/`S₃`
fibre split. The paper states the group distinction; it does not attach the two towers to
it. But the headline was not new and should not have been written as one.

---

## Pass 2651 — Pass 2642's fractal is **not the holonet's fractal**

The paper has `\section{Fractal scaling: the computer is the network}` — literally the
phrase from the brief — with a theorem and a witness:

```text
BT827 holonet scaling law
  leaves          N_n = 40^n
  W(3,3) instances I_n = (40^n - 1)/39
  edge-qutrit slots 240 I_n     directed transport 480 I_n
  chart routers     540 I_n     apartment links   1620 I_n
  mirror slots     2160 I_n     Clifford atoms   51840 I_n
  routing diameter  8n = 8 log_40 N,  where 8 = 3 + 5
                    (in-chart hypercube diameter + chart-web apartment diameter)
  durable commit clock  T(g) = 4(7^g - 1)
  witness: bt827_holonet_fractal_architecture.py
```

The recursion is **40-ary**: replace each of the 40 substrate *points* with a child
holonet.

My Pass 2642 built a **3-ary** recursion from the `E₈ ⊃ A₂ ⊕ E₆` branching and presented
it as "the substrate answering the architecture question". **The substrate had already
answered, with a different branching factor, a full resource law, a routing bound and a
witness script.**

> **Pass 2642's framing is withdrawn.** What it built is a real self-similar datapath with
> an exact law `LC(d) = 75·3^d − 2`, but it is the Lie-algebra recursion, not the
> holonet's, and it should not have been offered as the architecture's own.

### What is still worth having from it — and it is an engineering fact

The paper's fractal is 40-ary, so level 2 needs `I_2 = 41` `W(3,3)` instances. The mixer
alone is 4048 logic cells (Pass 2612), so one instance is already most of a UP5K and 41
of them are on the order of 10⁵ cells.

> **The holonet fractal crosses the chip boundary at level 2, not at some deep level.**
> `H_1` is one core and plausibly one part; `H_2` is 41 cores and is unavoidably a
> network. The paper's recursion is a *network-level* construction from its second rung
> onward, and the measured mixer cost is what pins that down.

That is a contribution the paper does not make, because it does not carry synthesis
numbers.

---

## Pass 2652 — Pass 2632's cubic is on the **wrong space**

The paper, §"The universal gate set is degree two plus degree three":

> *"the **degree-3** `E₆` Cartan cubic on the matter `27 = 3⊗3⊗3`, the `ε`-cubic
> preserved by `sl(3,𝔽₃)³`"*

```text
3x3 matrices over F3 : dimension  9,  elements 3^9  = 19,683
3 (x) 3 (x) 3        : dimension 27,  elements 3^27 = 7,625,597,484,987
```

My Pass 2632 gate takes **9 trits** and computes `det` of a `3×3` matrix. I wrote
"`27 = 3³ =` the `3×3` matrices over `F₃`" — **conflating `3⁹` elements with dimension
27**. The paper's object is a `3×3×3` tensor: 27 trits, `sl(3)³`-invariant, an
`ε`-cubic, not a determinant.

> **The gate is correct as built — exhaustively verified on all `3⁹` inputs — but it is
> not the `E₆` cubic the architecture calls for.** Pass 2632's identification is
> withdrawn.

The correct target is `C(x) = Σ ε ε ε · x x x` on `3⊗3⊗3`, and there is already a witness
script for the universality claim: `analysis/w33_cv_universality_cubic.py`.

---

## Pass 2653 — what reading the paper *confirmed*

The same section supplies numbers that settle an earlier open question:

```text
|Aut(D4)| = |W(F4)| = 192 * 6 = 1152
[Sp(4,3) : Aut(D4)] = 51840 / 1152 = 45
```

> The transversal (code-preserving) Gaussian gates are `Aut(D₄) = W(F₄)`, **whose `S₃`
> factor is `D₄` triality — the three-generation structure** — and the remaining **45**
> logical Cliffords are teleported using the cubic resource.

That answers the previous batch's step 5 (*"does `D₄` belong at a half-level?"*): **yes,
explicitly**, and its triality `S₃` is named as the generation structure. It also explains
`1152`, which the Pass 2583 index lookup had returned without context.

And the routing bound decomposes as `8 = 3 + 5` — one in-chart hypercube diameter plus one
chart-web apartment diameter — which is the kind of structural detail a resource law alone
would not reveal.

---

## Pass 2654 — other fractal material in the repo

```text
analysis/2026-07-15_pass79_fractal_tqc_scaling.md        [[2q^{2t}, 2, q^t]] CSS family
analysis/2026-05-30_qutrit_pauli_hierarchy_recursion.md
analysis/2026-05-30_qutrit_projection_fiber_tower.md
analysis/2026-05-21_genus_percolation_information_hole.md
```

So there are **at least three distinct recursions** in this project — the holonet's 40-ary
substitution (BT827), the fractal CSS tier family `q^t` (Pass 79), and the qutrit Pauli
hierarchy — plus my `A₂⊕E₆` 3-ary one. **They are not the same recursion and should not be
spoken of as "the" fractal.** Whether any two coincide is unexamined.

---

## Pass 2655 — the five items

Not reached: the aggregate-phase semantics, the inter-chip link, pipelining the mixer,
relating the cubic to `Cov₃`, and the `D₄` half-level — the last of which the paper
answered directly (Pass 2653) rather than needing computation.

---

## Pass 2656 — ledger

| claim | status |
|---|---|
| Pass 2444 "two order-51840 groups" is new | **withdrawn — in the paper's abstract** |
| Pass 2642 branching-3 is the holonet's fractal | **withdrawn — the holonet is 40-ary** |
| Pass 2632 gate is the `E₆` cubic | **withdrawn — wrong space, 9 trits vs 27** |
| Pass 2632 gate is correct as built | stands — exhaustive on `3⁹` |
| Pass 2642 law `LC(d) = 75·3^d − 2` | stands — but for a different recursion |
| holonet fractal is a network from level 2 | **new** — from the measured mixer cost |
| `D₄` sits at a half-level, triality `S₃` = generations | **confirmed by the paper** |
| at least three distinct recursions exist here | observed |

---

## Prior art

- `photonic_holonet_body.tex` §"Fractal scaling: the computer is the network", Theorem
  *BT827 holonet scaling law*, witness `bt827_holonet_fractal_architecture.py` — **owns**
  the fractal architecture.
- Same, §"The universal gate set is degree two plus degree three", witness
  `w33_cv_universality_cubic.py` — **owns** the `ε`-cubic identification.
- Same, abstract — **owns** the `Sp(4,3)` / `W(E₆)` distinction.

## Still open

- Building the actual `ε`-cubic on `3⊗3⊗3`.
- Whether the four recursions in this repo are related.
- Everything in Pass 2655.
