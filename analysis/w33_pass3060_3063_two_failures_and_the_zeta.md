## Passes 3060–3063 — two of my own results failed before publication

---

## Pass 3060 — **invalid as constructed**, and the reason matters

The plan was to sharpen Pass 3042's "3.23 % above the Ramanujan bound" into a statement
about where the Ihara zeta poles sit — the graph-theoretic Riemann Hypothesis, which
`docs/index.html` establishes that `W(3,3)` **satisfies**: every non-trivial pole lies
exactly on `|u| = 1/√11`, 48 from `r = 2` and 30 from `s = −4`, for `78 = dim(E₆)` complex
poles.

The computation returned:

```text
frame graph: 81 vertices, 261 edges, degree [2, 4, 6, 7, 8], regular False
```

> **The graph is not regular, so the `k`-regular pole formula does not apply and the
> result is void.**

**Why.** I built the undirected graph by symmetrising the opcode action — adding both
`A[i,j]` and `A[j,i]` and clamping. The opcodes are **not involutions** and their inverses
are not in the generating set, so distinct opcodes can land on the same neighbour and the
underlying simple graph has degrees from 2 to 8. The Cayley graph is 4-out-regular as a
*directed* graph and not regular as an undirected one.

The Ihara zeta of a non-regular graph needs the general Bass determinant formula, not
`(k−1)u² − λu + 1`, and "the critical circle" is not even defined the way I used it.

**What survives.** Pass 3042 stands: it used the *walk transition matrix*, which is
genuinely 4-regular by construction because it is stochastic on out-edges, and its
`|λ₂| = 0.894` against a bound of `0.866` is a valid comparison. The conclusion
— **the geometry is extremal and the instruction layer is not** — is unaffected. Only this
attempt to say *where* the poles are is withdrawn.

---

## Pass 3061 — the 324 coincidence is **false**

I expected `2E = 324` for the frame graph, matching the Delsarte absolute bound
`f(f+3)/2 = 24·27/2 = 324` for `W(3,3)`.

```text
total Ihara zeros of the frame graph = 2E = 522
Delsarte absolute bound              =      324
equal: False
```

> **Killed by arithmetic before it was written down.** I had assumed 162 edges; there are
> 261, for the same non-regularity reason as above.

This is the fourth coincidence of this shape the project has tested — after `81`, `15` and
`24`, all refuted — and the first to fail on the count itself rather than on a character.
The prior is now four for four: **in this substrate a matching integer is not evidence, and
half the time it is not even a matching integer.**

---

## Pass 3062 — the eight-dimensional code, at full budget

250,000 samples. The result is recorded in the certificate; the code test ran this time
rather than being starved of pairs as at Pass 3040.

---

## What goes into the paper from this round

Not my two failures — those go in the errata index. What goes in is the **prior art on
`W(3,3)`'s own zeta function**, which is solid and which the blueprint's substrate section
did not carry:

- `W(3,3)` is Ramanujan: `|r| = 2` and `|s| = 4`, both far below `2√11 ≈ 6.63`. It is not
  marginally Ramanujan — it is **maximally** so, with a spectral gap of `10`.
- Its Ihara zeta satisfies the graph-theoretic **Riemann Hypothesis**: all non-trivial
  poles on `|u| = 1/√11`, `48 + 30 = 78 = dim(E₆)` of them.
- The clique complex has `χ = 40 − 240 + 160 = −40 = −v`, and embedded genus
  `21 = 3 × 7 = C(7,2)`.
- Pole discriminants: `|disc r| = 40 = v`, `|disc s| = 28 = v − k = dim(SO(8))`, and their
  difference is `k = 12`.

That is a considerably stronger statement than "diameter 2 and well connected", which is
what the substrate section said, and it belongs there.

---

## Ledger

| claim | status |
|---|---|
| frame graph is 4-regular undirected | **false** — degrees 2–8 |
| Pass 3060 pole analysis | **withdrawn** — wrong formula for a non-regular graph |
| Pass 3042 Ramanujan comparison | **stands** — used the stochastic walk, which is regular |
| `2E = 324` matching the Delsarte bound | **false** — `2E = 522` |
| `W(3,3)` is maximally Ramanujan | **prior art**, `docs/index.html` |
| its Ihara zeta satisfies the graph RH | **prior art** |
| `78 = dim(E₆)` complex poles | prior art |

## Prior art

- `docs/index.html` — owns the Ramanujan property, the Ihara zeta and its pole structure,
  the `78 = dim(E₆)` count, the discriminant identities, and the genus.
