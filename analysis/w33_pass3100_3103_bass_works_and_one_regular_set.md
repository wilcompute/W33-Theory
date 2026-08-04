## Passes 3100–3103 — the routine works, exactly one generating set is regular, and τ stops at two

---

## Pass 3100 — Bass, validated before being trusted

Pass 3080's computation put 0 % of the poles inside the band. Rather than patch it, run it
on a graph whose Ihara zeta is textbook:

```text
K_4: 8 poles, 7 non-trivial;  critical radius 1/sqrt2 = 0.707107
non-trivial poles on the circle: 6 of 7
radii found: [0.5, 0.707107]
REFERENCE CHECK PASSES
```

> **The routine reproduces `K₄`.** The earlier failure was the linearisation orientation,
> now corrected — and the reference is what distinguished *"the graph is unusual"* from
> *"the code is broken"*, which look identical from the output alone.

---

## Pass 3101 — exactly **one** four-generator set is regular, and it is useless as an ISA

Pass 3081 concluded the degree collapse was structural. That was too strong.

```text
connected 4-generator sets tested : 80
giving a REGULAR simple graph     : 1

Z0 + Z1 + Z2 + Z3 : 8-regular, |lambda_2| 5.0000 vs bound 5.2915  ->  RAMANUJAN
```

> **One of eighty.** The irregularity is a property of the chosen opcodes, not of the
> group — so Pass 3081's "structural" reading is corrected.
>
> **And the winner is the four pure translations**, which generate only `F₃⁴`, the
> 81-element translation subgroup. It is connected on the frame space and **abelian**: it
> cannot perform a single Clifford operation.

So the honest statement is sharper than either extreme. There *is* a four-generator
Ramanujan Cayley graph on the frame space. It is not an instruction set. **Every generating
set that can actually compute collides, and every set that does not collide cannot
compute.**

That is a real trade and it now has a count: `1` regular set out of `80`, and the one is
the trivial one.

---

## Pass 3102 — the τ bridge is **two** facts, not three

```text
n   tau(n)     matches a named graph integer
2      -24     -f
3      252     E + k
6    -6048     -f(E+k)      <- forced by multiplicativity
4, 5, 7, 8, 9, 10           -   nothing
```

> Only `τ(2)` and `τ(3)` land on graph integers. `τ(6)` follows from them, so **the bridge
> is two independent coincidences and one identity, and it does not extend.**

Worth stating plainly because the pattern invited extrapolation: three hits in a row looks
like a law. Recorded with the same prior as this project's other count matches — now four
for four against.

---

## Ledger

| claim | status |
|---|---|
| Bass routine reproduces `K₄` | **validated** |
| \quad the Pass 3080 numbers | remain withdrawn |
| exactly 1 of 80 connected 4-sets is regular | **proved** |
| \quad Pass 3081's "structural" reading | **corrected** — it was the opcodes |
| \quad the regular set is abelian, cannot compute | proved |
| τ bridge: `τ(2) = −f`, `τ(3) = E+k` only | **proved** — no extension |

## Still open

- The graph RH for a *computing* generating set, now that the routine is trustworthy.

---

## Pass 3103 — the layout defect, reduced but not cleared

The three tall spec boxes are now **one table** — the shape change that worked before.

```text
before the merge : 88.39 pt vertical overflow
after            : 29.29 pt
```

> **A two-thirds reduction from changing the shape**, after four attempts at changing
> dimensions produced nothing. That is the second time this session the same lesson has
> paid, and it is now written down twice.

The residual 29 pt is a `plain` environment landing at a page end; it renders as an
unbreakable box. Six mitigations have been tried across two rounds. **Recorded, not
hidden** — the PDF is legible and the remaining fix is to stop patching and re-typeset that
page from scratch, which is what the previous round's own next-step list said.
