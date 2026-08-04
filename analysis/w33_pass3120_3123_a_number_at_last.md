## Passes 3120–3123 — a number at last, and the price of non-commutativity

---

## Pass 3120 — the graph RH for the instruction layer, on the third attempt

Two failures preceded this: Pass 3060 applied a `k`-regular formula to a non-regular graph;
Pass 3080's replacement returned 0 % and was withdrawn as a symptom. Pass 3100 validated
the routine against `K₄`. Third attempt, first checked tool:

```text
V 81   E 261   degrees 2..8
RH band for a non-regular graph : |u| in [0.377964, 1.000000]
non-trivial poles 161, inside 156  (96.9%)
pole radii: min 0.174008   median 0.419446   max 0.869474
```

> **96.9 %.** The instruction layer's poles almost all lie in the band a non-regular graph
> can be held to — and the address layer has **100 %** of its poles on a *single circle*,
> satisfying the graph Riemann Hypothesis exactly.

The difference between attempts two and three was validating the routine, not improving it.

---

## Pass 3121 — the price of non-commutativity, measured

Pass 3101 showed every computing generating set collides. *How much?*

```text
connected 4-sets: 80   computing 79   abelian 1
minimum collisions over COMPUTING sets : 18   (CX_fp + Z0 + Z1 + Z2)
collisions for the abelian set          : 0
the ISA actually in use                 : 45
```

> **18 collisions out of 324 outgoing edges — 5.6 % — is the irreducible cost of being
> able to compute.** The abelian set wastes none. And the ISA in use wastes **45**, which
> is two and a half times the minimum.

That last number is the actionable one: a generating set exists that computes and collides
`18` times instead of `45`. Whether it is otherwise a good ISA is a separate question, but
the gap is real and was invisible until collisions were counted.

---

## Pass 3122 — the abelian graph is a routing layer, and that is not a consolation prize

```text
8-regular, |lambda_2| 5.0000 vs bound 5.2915  ->  RAMANUJAN
diameter 4
```

An 8-regular Ramanujan graph of diameter 4 on the 81 frames, abelian.

> **That is exactly the profile a routing layer wants and exactly the wrong one for a
> compute layer.** The machine already separates the two concerns — address transport by
> transvections, frame algebra by opcodes — and this says the separation is not a
> convenience: **the two jobs want structurally different graphs, and no single generating
> set is good at both.**

Which is the sharpest form yet of the thread running through the last several rounds. It
began as "the geometry is extremal and the algebra is not", which sounded like a criticism
of the algebra. It is not. **They are different jobs with different optima, and the machine
is right to use two graphs.**

---

## Ledger

| claim | status |
|---|---|
| instruction layer: 96.9 % of poles in band | **measured**, validated tool |
| address layer: 100 % on one circle | prior art |
| minimum collisions over computing sets: **18/324** | **proved** |
| the ISA in use collides **45** times | measured — 2.5× the minimum |
| abelian set: 8-regular, Ramanujan, diameter 4 | **proved** |
| routing and compute want different graphs | follows |

## Still open

- Is the 18-collision set (`CX_fp + Z0 + Z1 + Z2`) a usable ISA? It generates, but its
  diameter and cell cost are unmeasured.

---

## Pass 3123 — the layout defect: a seventh attempt, reverted

The plan was to re-typeset the page rather than patch it — turn the tall unbreakable `tikz`
box into ordinary prose, since six patches had failed and a `tikz` node cannot break across
pages by construction.

The edit removed a `\end{plain}` that turned out to belong to a *different*, legitimately
open environment 74 lines earlier. The document then failed to compile:

```text
LaTeX Error: \begin{tikzpicture} on input line 529 ended by \end{document}
```

**Reverted.** The build is back to the 29 pt state, which compiles and is legible.

> Seven attempts, and the seventh made it worse rather than better. The honest reading is
> that I have been editing this by pattern-matching on line content instead of parsing the
> environment structure, and that is why each fix has a fifty-fifty chance of hitting the
> wrong `\end`. The next attempt should build an environment map first, not another `sed`.

Recorded because a reverted attempt is still information: it narrows what the remaining
fix can be.
