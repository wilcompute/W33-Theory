## Passes 2880–2886 — the choice is not free, and two negative results worth having

---

## Pass 2882 — the six minimal triples do **not** cost the same

Pass 2789 found six minimal generating triples and Pass 2866 measured one at diameter 19.
The natural inference — six valid choices, so pick the cheapest in silicon and the decision
is free — is **wrong**.

```text
triple                        diameter   mean    shell at diameter
F_p + CX_pf + CX_fp              19     14.176      188
F_f + CX_pf + CX_fp              20     15.216       60
F_p + F_f + CX_fp                22     16.078       20
F_p + S_f + CX_pf                22     16.119        2
F_f + S_p + CX_fp                22     15.897        2
F_p + F_f + CX_pf                23     17.076        2
```

> **Worst-case program length varies from 19 to 23 — a 21 % spread on a choice that looks
> free.** Build the triple with two entanglers.

The pattern is legible: the best triple contains **both** directions of the coupling
instruction; the worst contains neither. What shortens programs is the ability to move
information both ways between past and future — the machine's own central metaphor,
rewarded by its compiler.

*(The parallel track's Pass 2820 had already selected `{F_p, CX_pf, CX_fp}` for the
micro-ISA. This is independent confirmation that the selection was the right one, with the
margin quantified.)*

---

## Pass 2885 (outside the programme) — the 188 hardest elements are **not** an orbit

Only 188 of `4,199,040` sit at distance exactly 19 — `0.0045 %`. A set that rare invites
the hypothesis that it is one conjugacy class, one coset, something nameable.

```text
distinct linear parts among them : 54
distinct translations           : 58
element orders                  : {4:4, 5:6, 6:2, 8:10, 9:2, 10:4, 12:22, 18:4}
traces mod 3                    : {0:16, 1:20, 2:18}   -- all three classes
```

> **The hypothesis is refuted.** There is no single "hardest instruction" to name.
>
> What survives is the useful half: **188 is small enough to enumerate exactly**, so a
> compiler regression suite can contain *every* worst-case input rather than sampling for
> them. A negative structural result and a positive engineering one from the same run.

**Method note.** The first run of this asked about `TRIPLES[0]` and found a 2-element
shell at distance 23 — correct for that triple, and the wrong triple to ask about. Fixed to
the shortest one. Recorded because the number was plausible and would not have looked
wrong.

---

## Pass 2884 (outside the programme) — the 240 wires as a budget

Recomputing the Hodge Laplacian on 1-chains of `W(3,3)` independently:

```text
points 40   edges 240   triangles 160
Hodge L1 spectrum: {0: 81, 4: 120, 10: 24, 16: 15}
multiplicities sum to 240 = the edge count: True
```

> `240 = 81 + 120 + 24 + 15`. The harmonic sector is `81` — the frame register file, and
> the logical dimension of the substrate's own qutrit code `[240, 81, d_Z=4]`.

### What is tempting here, and what is not claimed

Two of the other three are already architectural quantities in this project: `15` is the
support-shell dimension (parallel track, Pass 2808) and `24 = |SL(2,3)|` is the
single-qutrit Clifford group modulo phase (Pass 2708). It is very tempting to read this as
*"the machine's wiring decomposes into its own subsystems."*

> **No map is exhibited in either case. These are equal integers.** This project's second
> most expensive failure mode is an over-read of a count match — and Pass 2883, in this
> same batch, is a worked example of exactly such a coincidence turning out to be nothing.
> Recorded as an open question, not a decomposition.

---

## Pass 2883 — the two `81`s are **not** the same module

`H₁(W(3,3); ℤ) = ℤ⁸¹` and `|F₃⁴| = 81`. The blueprint stated the counts agree and declined
to claim more. The sharper question has an answer.

```text
fixed frames of the order-3 linear opcode S_p : 27
homology character on order-3 classes         : 0    (index.html, GAP Pass 213)
characters disagree                           : True
```

A permutation module's character counts fixed points; the homology character vanishes on
every order-three class while the frame space has 27 fixed points there.

> **There is no equivariant isomorphism.** Both are `3⁴` because the geometry is
> four-dimensional over `F₃` — the shared reason is real — but the spaces differ as
> modules. The blueprint's refusal to claim a map was correct, and the question is now
> **closed negatively** rather than left open.

Open questions that stay open too long start to be cited as though they were answered.

---

## Pass 2881 — three copies: the condition, and no witness

Pass 2861 proved no **two**-copy stabilizer projection on `M₃₆` can be super-linear. The
same necessary-and-sufficient test applies verbatim at three copies: nine single-error
vectors, six-qubit projectors.

```text
clean vector |mmm> in dimension 64;  single-error vectors: 9
max |<single | mmm>| = 2.6e-16      -- orthogonal, as at two copies
available syndrome ranks 32,16,8,4,2,1; a 9-dim kernel caps rank at 55
  -> RANK IS NOT THE OBSTRUCTION, same as at two copies
30,000 sampled stabilizer groups on 6 qubits: 0 witnesses
```

> **Not a proof** — the six-qubit stabilizer space is far too large to enumerate. What it
> establishes is that three copies do not make the condition *easy*: an exhaustive search
> at two copies returned zero and a large random search at three returns zero too.

The open problem is now stated exactly, which is the deliverable: *does any stabilizer
protocol on three or more copies annihilate every single-error input while keeping the
clean one?* What is missing is an exhaustive search over a chosen code family rather than
a random one.

---

## Pass 2886 — blueprint: gaps closed out, and a hedge audit

The **"What is not built"** section is restructured into two halves — *Still open* and
*Closed, and when* — because a struck-through item in a list of gaps is a worse record than
a table row saying what closed it.

Three items remain open, each sharpened:
- the two non-frame opcodes (the `M₃₆` refusal is now **typed**: `p < (8−2√3)/9` is a
  comparison the controller can make, not a blanket refusal);
- the universality gap, now a **single well-posed question** with four bullets of
  narrowing;
- the power figure, now **modelled not absent** — `0.502 pJ/op` from two measured inputs
  and two assumed constants, with the two assumptions named as the whole gap.

Seven closed, with what closed each. **Two closed negatively** (the homology is not the
frame space; the six triples are not equivalent) — as valuable as the positive ones,
because each removed a plausible assumption that would otherwise have been relied on
quietly.

**Hedge audit** over every absolute word in the document: `the unique` (1), `no other` (1),
`uniquely` (2) — all four backed by exhaustive computation (Passes 2862, 2861, and the
`q=3` algebra checked at six values). `every` (35), `never` (16), `cannot` (12),
`exactly one` (8), `always` (8) reviewed by category; no unsupported instance found.

---

## Pass 2880 — ledger

| claim | status |
|---|---|
| six triples, diameters `19,20,22,22,22,23` | **proved** — the choice is not free |
| best triple contains both `CX` directions | observed across all six |
| the 188 hardest are not one orbit or coset | **proved** — 54 linear parts, all traces |
| 188 is enumerable as a regression suite | follows |
| `240 = 81+120+24+15` | **proved**, recomputed |
| `15` and `24` match other quantities | **count match only** — no map |
| `H₁` is not the frame space as a module | **proved** — characters disagree |
| three-copy super-linear condition | **open** — 0 witnesses in 30,000 samples |
| rank is not the obstruction at three copies | proved |
| first run of Pass 2885 used the wrong triple | **corrected** |

## Prior art

- `docs/index.html` — owns the Hodge spectrum `{0:81, 4:120, 10:24, 16:15}`, the
  `[240,81,d_Z=4]` code, and the order-three character fact used in Pass 2883.
- Parallel track Pass 2820 — selected `{F_p, CX_pf, CX_fp}`; Pass 2882 quantifies why.
- Parallel track Pass 2808 — owns the 15-dimensional support shell.

## Still open

- An exhaustive three-copy search over a chosen code family.
- Whether `15` or `24` in the Hodge budget is carried by a natural map.
- `D₁₂`-mirror RTL; a measured (not modelled) power figure.
