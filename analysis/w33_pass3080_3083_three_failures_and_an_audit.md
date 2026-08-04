## Passes 3080–3083 — three failures, one clean audit, and what went in the paper

---

## Pass 3081 — **my test was vacuous**, and the answer is still no

The hypothesis: adjoining the four opcode inverses would make the instruction Cayley graph
regular, so the Ramanujan question becomes well posed — a real ISA trade, eight opcodes for
a comparable spectrum.

```text
forward opcodes symmetrised : V 81  E 261  degrees 2..8  regular False
inverses adjoined           : V 81  E 261  degrees 2..8  regular False
```

**Identical.** And they had to be: my `build(False)` branch already applied
`A = max(A, Aᵀ)`, so both branches construct the same undirected graph. The test compared
a thing with itself.

> **But the underlying answer survives the broken test, and it is no.** The degree collapse
> is not caused by the generating set being asymmetric — it is caused by *different
> generators landing on the same neighbour*. Adjoining inverses cannot fix that, because
> collisions are a property of the action, not of the set's symmetry.

So the architectural trade I hoped to price does not exist in that form. Eight opcodes buy
a symmetric generating set and still not a regular simple graph.

---

## Pass 3080 — the Bass computation is **not trustworthy** and is not published

The Ihara–Bass identity has no regularity hypothesis, which is why it was the right tool
after Pass 3060 was withdrawn. The run returned:

```text
RH band |u| in [0.377964, 1.000000]
non-trivial poles 161, inside the band 0 (0.0%)
worst excursion 4.746873
```

**Zero per cent inside is not a result, it is a symptom.** Ihara poles are small; a
computation that puts none of them anywhere near the band has almost certainly inverted
the pencil — I take reciprocals of generalised eigenvalues of a linearisation that may
already be returning `u` rather than `1/u`.

> Published as a failed computation rather than as a finding. The question — how badly does
> the instruction layer violate the graph RH — remains open and now has two failed
> attempts against it.

---

## Pass 3082 — the regularity audit, which came out better than feared

Twice in one file is a habit, so every graph this track has built was checked:

| graph | regularity | verified where |
|---|---|---|
| `W(3,3)` collinearity | 12-regular | **Pass 2869** — degrees `{12:40}` printed |
| orthogonality on 40 rays | 12-regular | **Pass 2835** — printed |
| orthogonality on 36 rays | 11-regular | **Pass 2790** — printed |
| frame walk transition matrix | doubly stochastic | **Pass 2867** — checked explicitly |
| frame **Cayley** graph | **not regular** | assumed at 3060, refuted |

> **Four of five carried an explicit degree check in the pass that built them.** The habit
> is narrower than feared: one missing check, not a systematic assumption.

The rule is cheap and worth keeping: **print the degree sequence before using a `k`-regular
formula.**

---

## Pass 3083 — what went into the paper

Not the three failures — those are errata rows. What went in is prior art the substrate
section was missing:

- **`τ(2) = −24 = −f`.** Ramanujan's tau at 2 is the negative of the eigenvalue
  multiplicity. `τ(3) = 252 = E + k = 240 + 12`. `τ(6) = −6048 = τ(2)τ(3)` by
  multiplicativity, `= −f(E+k)`. The weight of `Δ` is `12 = k`, the degree of the graph.
- **`χ = 40 − 240 + 160 = −40 = −v`** for the clique complex, with embedded
  **genus `21 = 3 × 7 = C(7,2)`**.
- The `[240, 81, d_Z=4]` code and the Hodge sectors were already there; these sit beside
  them.

---

## Ledger

| claim | status |
|---|---|
| adjoining inverses makes the graph regular | **false** — collisions, not asymmetry |
| \quad and the test that showed it | **vacuous** — compared a thing with itself |
| Bass pole computation | **unreliable** — 0 % inside the band is a symptom |
| regularity audit: 4 of 5 verified at build time | **clean** |
| `τ(2) = −f`, `τ(3) = E + k`, `τ(6) = τ(2)τ(3)` | **prior art** |
| `χ = −v`, genus `21` | **prior art** |

## Still open

- The graph RH for the instruction layer, by a correct Bass computation.
- Whether *any* four-element generating set of `ASp(4,3)` gives a regular simple Cayley
  graph.

---

## Known defect in this build

One `88 pt` vertical overflow remains in the substrate section, where the three new spec
boxes (Ramanujan margin, Ihara zeta, tau) land together and one page runs long. Four
mitigations were tried — narrowing, re-wrapping the orphaned paragraph, splitting the
errata table, and forcing a page break. The PDF is legible; the box is recorded here rather
than left for a reader to find.

**Second time this session that a table or box resisted four fixes**, and last time the
answer was to change the *shape* rather than the dimensions. That is the thing to try next:
these three boxes probably want to be one table, not three environments.
