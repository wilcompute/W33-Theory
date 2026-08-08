## Pass 4201 — the instruction layer *can* be Ramanujan, at five generators

Three attempts failed on this question (Passes 3060, 3080, 3120) because the four-opcode
Cayley graph is not regular — degrees 2 to 8 — and every tool for it assumes regularity.
Pass 3101 found exactly one regular four-generator set and it was abelian.

**Pass 3101 only searched size four.** Searching larger sets:

```text
size 4: regular, connected, containing a Clifford op = 0
size 5: regular, connected, containing a Clifford op = 2

FOUND: S_f + Z0 + Z1 + Z2 + Z3
V 81   E 324   degree 8   (E - V = 243)
spectrum: 8^1, 5^8, 2^24, (-1)^32, (-4)^16          (sums to 81)
|lambda_2| 5.000000  vs Ramanujan bound 5.291503  ->  RAMANUJAN
```

> **A regular presentation containing a Clifford operation exists, and it is Ramanujan.**
> The zeta then factors in the Pass 4191 form exactly:
> `ζ⁻¹(u) = (1−u²)²⁴³ ∏(1 − λu + 7u²)`.

---

## The caveat, which is most of the result

`⟨S_f, Z0, Z1, Z2, Z3⟩` has order **243 = 3⁵**, not `4,199,040`. It is
`F₃⁴ ⋊ ⟨S_f⟩` — it acts transitively on the 81 frames, which is why the graph is
connected, but **it does not generate `ASp(4,3)`**. It contains a Clifford operation
without being a universal instruction set.

So the honest statement is layered, and the layers matter:

| presentation | regular? | Ramanujan? | generates `ASp(4,3)`? |
|---|---|---|---|
| 4 opcodes (the ISA) | **no** — degrees 2–8 | ill-posed | **yes** |
| 4 translations | yes, 8-regular | **yes** | no (abelian, 81) |
| `S_f` + 4 translations | yes, 8-regular | **yes** | no (order 243) |

> **Every presentation that is regular fails to generate the group, and the presentation
> that generates the group is not regular.** Three data points now, all pointing the same
> way: the question "is the instruction layer Ramanujan" cannot be asked of a universal
> ISA in this family.

---

## What this corrects

Passes 3042 and 3120 concluded *"the geometry is extremal and the algebra is merely very
good"*, on the strength of the frame **walk**'s `|λ₂| = 0.894` against a bound of `0.866`.

That comparison stands for the walk. But the broader reading — that the algebra is
*inherently* less extremal than the geometry — is **not supported**, because two regular
presentations of parts of the same algebra *are* Ramanujan. What is actually true is
narrower and more interesting:

> **Extremality and universality are in tension here.** The presentations that are
> spectrally optimal are exactly the ones that cannot compute, and vice versa. That is the
> same shape as Pass 3121's collision result (`18` collisions is the price of computing)
> and Pass 3122's routing/compute split, arrived at by a third independent route.

---

## Ledger

| claim | status |
|---|---|
| a regular presentation with a Clifford op exists at size 5 | **proved** |
| it is Ramanujan (`5.000` vs `5.2915`) | **proved** |
| its zeta factors in the Pass 4191 form | follows |
| it generates only order `243`, not `ASp(4,3)` | **proved** |
| "the algebra is inherently less extremal" | **not supported** — corrected |
| extremality and universality are in tension | three independent routes |

## Prior art

- **Parallel track Pass 4191** — owns the factored-zeta method this uses, verified
  independently at Pass 4200.

## Still open

- Does *any* generating set of the full `ASp(4,3)` give a regular simple Cayley graph, at
  any size? Sizes 4 and 5 are now searched.
