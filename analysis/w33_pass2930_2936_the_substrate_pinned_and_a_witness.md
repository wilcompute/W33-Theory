## Passes 2930–2936 — the substrate pinned down, and a three-copy witness

---

## Pass 2936 — the blueprint's substrate section, rewritten to the canonical definition

The blueprint described `W(3,3)` by its *statistics*. `docs/index.html`,
`photonic_holonet.tex` and `w33_paper.tex` all pin it down by its *construction*, and the
blueprint now does the same. What was added:

- **The definition proper.** `W(3,3)` is the symplectic polar space `W(3, F₃)`: points are
  the 40 projective 1-spaces of `GF(3)⁴` (every 1-space is automatically isotropic, so
  none are excluded), and adjacency is the single congruence
  `v ~ w ⟺ vᵀ J w ≡ 0 (mod 3)`. **That one line generates every number in the document.**
- **Lines properly distinguished from edges.** The 240 edges pair into 40 *totally
  isotropic projective lines*; a **non**-edge spans an ordinary *hyperbolic* line. The two
  kinds of pair are different geometric objects, not merely present-or-absent.
- **Eigenvalues `12, 2, −4`; diameter 2; Ramanujan** — with both translated for a
  non-specialist: diameter 2 means no packet is ever more than one relay from its
  destination within a node, and Ramanujan means **you cannot build a better-mixing
  network on 40 nodes with 12 links each**. The fabric is extremal, not merely adequate.
- **The two order-51840 groups**, in an errata box: `Aut = PGSp(4,3) ≅ W(E₆)` with normal
  inner `PSp(4,3)` of order 25920, against `Sp(4,3) = 2.U₄(2)` which has centre `C₂` and is
  **not** that extension. Both appear here for good reasons and the document now says
  which is meant at every occurrence.
- **What the shape already contains**: `H₁ = ℤ⁸¹` and the `E₈ = g₀(86) ⊕ g₁(81) ⊕ g₂(81)`
  grading with `g₀ = E₆ ⊕ A₂`; the Hodge spectrum `{0:81, 4:120, 10:24, 16:15}` with the
  exact gap `Δ = 4` **and the explicit statement that it is not a mass and not a
  Yang–Mills gap**; the clique complex as the `[240, 81, d_Z=4]` qutrit CSS code with check
  ranks 39 and 120; both Euler characteristics (`−40` truncated, `−80` full).
- **The `240`-to-`E₈` temptation, as an errata box.** `240 = 40×3×2`, `E₈` has 240 roots,
  the branching `3×(24+2+27+27)` matches, and an `E₈` Dynkin subgraph sits in the adjacency
  graph at `[7,1,0,13,24,28,37,16]` with `det(2I − A_sub) = 1`. **And there is no
  equivariant bijection** — `PSp(4,3)` is edge-transitive, the correspondence is
  representation-theoretic. This project spent several passes on the stronger reading.

17 sections, clean compile, zero overfull boxes.

---

## Pass 2933 — a three-copy **witness**, and why it is not yet a protocol

Pass 2910's negative used the *factor-wise* family. The stronger reduction: a stabilizer
projector annihilates all nine singles iff its **range** lies in their orthogonal
complement — and that range is a stabilizer **code**, which contains stabilizer **states**.
So search states, not projectors.

```text
stabilizer states sampled : 200,000
best max-overlap with the nine singles : 0.000000
states orthogonal to all nine AND overlapping |mmm> : 36
```

> **36 witnesses.** The first-order condition **is** satisfiable at three copies. Pass
> 2910's negative was an artefact of the family it searched, not a fact about three copies.

### And it is not a protocol

A rank-one stabilizer projector `|σ⟩⟨σ|` has a stabilizer state as its *entire* range, and
a stabilizer state carries **no magic**. Such a branch suppresses the first-order error
perfectly and outputs something useless.

> So the question sharpens rather than closing, and it is well posed for the first time:
>
> **is there a stabilizer code of rank ≥ 2 inside `(span singles)^⊥` whose range contains
> a magic state?**
>
> Rank one is proved possible and proved useless. Rank two or more is what a real
> three-copy protocol needs, and nothing here rules it out — a much better position than
> the three negatives that preceded it.

---

## Pass 2930 — the native/guest trade **does not exist**

| triple | diam | `F_g` | `S_g` | `Z_g` | worst |
|---|---:|---:|---:|---:|---:|
| **`F_p + CX_pf + CX_fp`** | **19** | 1 | 8 | 1 | **8** |
| `F_f + CX_pf + CX_fp` | 20 | 9 | 8 | 1 | 9 |
| `F_p + S_f + CX_pf` | 22 | 1 | 9 | 1 | 9 |
| `F_p + F_f + CX_fp` | 22 | 1 | 12 | 1 | 12 |
| `F_f + S_p + CX_fp` | 22 | 10 | **1** | 1 | 10 |
| `F_p + F_f + CX_pf` | 23 | 1 | 8 | 1 | 8 |

> **The hypothesis is refuted.** `F_p + CX_pf + CX_fp` has the shortest diameter *and*
> ties for the lowest guest overhead. No triple is better for guests than the one that is
> best natively, so the hardware choice needs no workload assumption after all.

The reason the alternative fails is legible in the table. `F_f + S_p + CX_fp` **keeps**
the guest's `S` gate, so `S_g` costs 1 instead of 8 — and `F_g` jumps from 1 to **10**.
**The cost does not disappear when you keep `S`; it moves to `F`, and lands higher.**

A hypothesis refuted by the same table that was built to quantify it.

---

## Pass 2932 — the Hodge `24` is refuted too

```text
lambda = 10 eigenspace dimension : 24
trace of the block swap on it    : 5.866667   -- not an integer
```

A group of order 24 acting on itself gives a permutation module, whose character is an
integer on every element. A non-integer trace refutes that outright.

> **Both count matches from Pass 2884 are now dead.** The `15` fell at Pass 2911, the `24`
> here. `240 = 81 + 120 + 24 + 15` is arithmetic — the sectors are real, the
> identifications were not.

Three coincidences of this shape have now been tested (`81`, `15`, `24`) and all three
died. That is worth stating as a prior: in this substrate, a matching integer is not
evidence.

---

## Pass 2935 (ludicrous) — no Hamiltonian self-test found

A Hamiltonian cycle in the frame graph would be a single 81-instruction word visiting
every frame exactly once — a built-in self-test with no scan chain, no test vectors and
one equality check.

**Not found** within a 4,000,000-node depth-first search. Honest negative: the search is
bounded, not exhaustive, so this neither exhibits one nor proves none exists.

**Method note.** The first attempt ran unbounded and was killed by a ten-minute budget,
reporting nothing at all. A node cap turns that into a result. *An unbounded search that
gets killed is strictly worse than a bounded one that says "not found within N".*

---

## Pass 2934 — ledger

| claim | status |
|---|---|
| substrate section pinned to the symplectic construction | done |
| three-copy first-order condition is satisfiable | **witnessed** — 36 states |
| \quad rank-one output carries no magic | proved — not a protocol |
| \quad rank ≥ 2 with magic in range | **open**, and now well posed |
| Pass 2910's three-copy negative | **artefact of the factor-wise family** |
| native/guest trade | **refuted** — one triple wins both |
| keeping `S` moves the cost to `F` (1→10) | measured |
| Hodge `24` is not a permutation module | **proved** — trace `5.8667` |
| all three count matches (`81`, `15`, `24`) dead | proved |
| Hamiltonian self-test | not found within 4M nodes |

## Prior art

- `docs/index.html` "The Theory" — **owns** the canonical `W(3,3)` definition, the Spence
  count, the Hodge spectrum, `H₁ = ℤ⁸¹`, the `E₈` grading, the `[240,81,d_Z=4]` code, the
  `E₈` Dynkin subgraph vertices, and the five `q = 3` selection criteria. The blueprint now
  transcribes rather than paraphrases.

## Still open

- A rank ≥ 2 stabilizer code in `(singles)^⊥` containing a magic state.
- A Hamiltonian cycle in the frame graph, or a proof there is none.
