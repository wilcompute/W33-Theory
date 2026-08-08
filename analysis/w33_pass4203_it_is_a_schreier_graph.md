## Pass 4203 — it was never a Cayley graph

### (a) A second generator pool, same answer

Pass 4202 exhausted the ten opcodes. The parallel track's Pass 3005 routes addresses with
rank-one symplectic **transvections**, which are not in that pool at all. Forty exist.

```text
2,400 candidate sets tested (transvections alone, and with translations)
best regular set: degree 8, order 729, Ramanujan (|lambda_2| = 5.000)
universal: NO
```

> A structurally different generator family gives the same verdict: **regular, Ramanujan,
> and still a proper subgroup** — order `729 = 3⁶` this time, against `81` and `243`
> before. Three regular presentations now, three proper subgroups.

### (b) And the law is **not** general — which exposes my own error

Does non-abelian force irregular? One counterexample settles it: `S₃` on itself, generated
by a transposition and a 3-cycle, is **3-regular** and non-abelian.

So no. And the reason matters far more than the answer:

> **The 81-frame graph is not a Cayley graph of `ASp(4,3)` at all. It is a Schreier graph
> on a coset space.**
>
> A group's Cayley graph on *itself* is always regular — every generator acts freely. A
> Schreier graph on a smaller transitive set need not be, because distinct generators can
> send the same point to the same image. **That is exactly the collision Pass 3121
> measured at 18 out of 324.**

`ASp(4,3)` has order `4,199,040` and the frame space has `81` points. I have been calling
the graph on those 81 points a "Cayley graph" continuously since **Pass 3042** — through
3060, 3080, 3101, 3120, 3121, 4201 and 4202. The mathematics in those passes is unaffected
where it was computational, but the *name* was wrong throughout, and the wrong name is
precisely what made "why is it not regular?" look mysterious for six passes.

It is not mysterious. **Schreier graphs collide. That is what they do.**

---

## What survives, and what is renamed

| pass | claim | status |
|---|---|---|
| 3042 | frame walk `\|λ₂\|` 0.894 vs bound 0.866 | **stands** — a walk, correctly handled |
| 3101, 4202 | no regular *universal* presentation | **stands** — now with a reason |
| 3121 | 18 collisions is the price of computing | **stands** — collisions are the mechanism |
| 4201 | regular presentations exist and are Ramanujan | **stands** — all proper subgroups |
| everywhere | "the instruction **Cayley** graph" | **misnamed** — it is a Schreier graph |

The corrected statement of the whole thread:

> The frame space is a coset space, so the instruction graph is a Schreier graph.
> Presentations act regularly on it exactly when they act *freely*, which happens only for
> proper subgroups whose order divides into the orbit cleanly. Universality forces
> collisions; collisions force irregularity; irregularity leaves Ramanujan and the graph RH
> undefined. **Nothing about the algebra is deficient — the object is simply not the kind
> of graph those properties describe.**

---

## Ledger

| claim | status |
|---|---|
| transvections give a regular Ramanujan set of order 729 | **proved** |
| \quad still not universal | proved |
| non-abelian forces irregular | **false** — `S₃` is 3-regular |
| the 81-frame graph is a Schreier graph, not Cayley | **correction**, applies from Pass 3042 |
| Schreier collision explains six passes of confusion | follows |

## Still open

- Whether *any* universal generating set acts freely on the 81 frames. The Schreier framing
  makes this a question about point stabilisers, which is a much better-posed question than
  the graph-theoretic one I was asking.
