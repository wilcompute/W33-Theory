# Passes 2632–2639 — the degree-3 gate exists, and the whole universal set fits on one FPGA

---

## Pass 2632 — why the cubic cannot be a single-qutrit gate

Over `F₃`, Fermat gives `x³ = x` for every `x`:

```text
x^3 mod 3 for x in F3 : [0, 1, 2]        x^3 == x for all x : True
```

> **A cubic map on one trit is the identity.** That is why the architecture names the
> degree-3 `E₆` cubic on the **27**, not on a qutrit.

And `27 = 3³ = ` the `3×3` matrices over `F₃`, on which the `E₆` cubic invariant restricts
to the **determinant**. That is the object to build.

---

## Pass 2633 — built, and verified **exhaustively**

`rtl/w33_pass2632_e6_cubic_gate.sv`: nine trits in (2 bits each, row-major), `det(X) mod 3`
out, usable directly as a `μ₃` phase increment. Built from `F₃` add and multiply
primitives so the arithmetic is exact rather than a truncation of integer arithmetic.

```text
Pass 2632 E6 cubic: 19683 matrices checked, 0 errors
PASS  det over F3 correct on ALL 3^9 inputs
```

> **Every one of the `3⁹ = 19,683` possible inputs was checked against an independent
> determinant computation. This is a complete verification, not a sample.**

Given the Pass 2618 lesson — a bench that never drove a negative lane passed a broken
core — exhaustive was the right standard here, and the input space is small enough to
afford it.

---

## Pass 2634 — routed, and packed

```text
w33_e6_cubic         ICESTORM_LC   67/5280    SB_IO 20/96    (combinational)
w33_cubic_phase_gate ICESTORM_LC   73/5280    SB_IO 23/96    116.52 MHz
bitstream            104,090 bytes            sha256 837cda584c30fc000b7fb396...
```

### The whole gate set now fits on one part

| architecture layer | logic cells | Fmax |
|---|---:|---|
| degree-2 symplectic interconnect (36-lane mixer) | 4048 | 19.65 MHz |
| `μ₄`/`μ₆` phase controller | 73 | 93.40 MHz |
| chirality / fibre controllers `C₆`, `S₃` | 9 + 8 + 4 | — |
| **degree-3 `E₆` cubic** | **73** | **116.52 MHz** |
| **total** | **4215 / 5280 = 80%** | |

> **The complete Lloyd–Braunstein universal set — degree-2 symplectic plus degree-3
> cubic — now places and routes on a single iCE40 UP5K, with 20% of the fabric left.**

Before this pass the project had the Clifford half only, and the mixer could not even be
placed (Pass 2612).

**Scope, and it is the important part.** This is a *classical* digital realisation of the
gate set's combinatorial structure: exact `F₃` arithmetic and an exact cubic form, routed
on an FPGA. It is **not** a quantum processor, and nothing here demonstrates
Lloyd–Braunstein universality physically — that argument is about operations on quantum
states, and the corpus's own "universality boundary before any full braiding claim" still
stands. What is new is that the degree-3 object, which had **no** implementation of any
kind in this project, now has one that is exhaustively verified and routable.

*(The cubic phase gate happens to use 73 logic cells, as the chirality modulator does.
Coincidence — cell counts depend on the tool and the parameters, and Pass 2464 already
flagged and rejected the same number.)*

---

## Pass 2635 — the involution SAT: **timed out**, not failed

```text
Solving problem with 233,483 variables and 668,351 clauses..
ERROR: Called with -verify and proof did time out!
```

Distinct from the pre-fix run, which **found a model** quickly. After the fix the solver
finds no counterexample within budget but does not prove the property either.

> **Inconclusive.** The evidence for the fixed core is the Pass 2626 simulation —
> 14,076 signed lane checks, 0 errors, against 12,780 errors pre-fix — not the SAT.

Recorded rather than glossed: a timeout is not a pass.

---

## Pass 2636 — the GKP `E₈` question

The corpus states the GKP tower `A₂ < D₄ < E₈` as the code layer, and Pass 2444 identified
the `E₈` carrier as the **central** doubling `Sp(4,3) = 2.U₄(2)`. Whether those are the
same `E₈` was the question.

**Not answered.** The corpus text found — *"GKP tower `A₂<D₄<E₈` IS the…"*, *"the `E₈`
lattice or in the 8-dimensional space `E₈ ⊗ ℝ`"* — is about the `E₈` **lattice** as a code,
while Pass 2444's is about the 8-dimensional **faithful representation** `4 + 4bar` of
`2.U₄(2)`. Those can coincide (the lattice's automorphism group contains such
representations) but the identification needs the actual lattice basis compared against
the representation, which was not done.

Left as a well-posed question rather than a claimed link — the two objects share a name
and a dimension, which is exactly the count-match shape this project rejects by default.

---

## Pass 2637 — not reached

The 1821–1843 family read, and ranks 10–14 (third attempt). Both deferred to the cubic
gate, which was the larger deliverable.

---

## Pass 2638 — ledger

| claim | discharged by | status |
|---|---|---|
| single-qutrit cubic is the identity | `x³ = x` on `F₃` | proved |
| `E₆` cubic on the 27 is the `3×3` determinant | classical | cited |
| the gate computes it correctly | **all 19,683 inputs**, 0 errors | **exhaustively verified** |
| routes at 116.52 MHz, 73 LC | nextpnr | measured |
| full gate set fits one UP5K | 4215/5280 = 80% | measured |
| this demonstrates quantum universality | — | **explicitly not claimed** |
| involution SAT after the fix | timeout | **inconclusive** |
| GKP `E₈` = chiral `E₈` | — | **open; name-and-dimension match only** |

---

## Prior art

- The GKP tower, Lloyd–Braunstein universality and the qutrit Clifford scaffold are
  pre-existing corpus results.
- Pass 2554 (parallel track) — the four cubic `5:8` covariants that motivated looking for
  a degree-3 object. **This gate is not one of theirs**: it is the `E₆` cubic on the 27,
  built from the architecture's own description, and the relationship between the two is
  untested.
- Pass 2303/2308 (parallel track) — the mixer whose interface Pass 2612 made routable.

## Still open

- Whether this cubic and their `Cov₃` covariants are related.
- The involution property, still only simulation-backed.
- GKP `E₈` versus the chiral `E₈`.
- Ranks 10–14, `χ(H) ∈ {10,11}`, the 1821–1843 family.
