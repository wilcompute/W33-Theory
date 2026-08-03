# Passes 2640–2649 — a node whose network has the shape of the node

**The brief:** minimal hardware that replicates itself, so the machine, the program and
the network are one object — self-similar inward and outward.

The interesting part is that the substrate answers it, rather than the designer choosing
a topology.

---

## Pass 2640 — the branching rule is already in the tower

The corpus names the GKP tower `A₂ < D₄ < E₈`. `E₈` has a maximal subalgebra `A₂ ⊕ E₆`,
and the adjoint branches as

```text
248 = (8,1) + (1,78) + (3,27) + (3bar,27bar)        8 + 78 + 81 + 81 = 248
```

Read as architecture:

| piece | is |
|---|---|
| `(1,78)` | one `E₆` machine core |
| `(8,1)` | the `A₂` qutrit **phase bus** (8 = adjoint of `su(3)`) |
| `(3,27)` | **three** copies of the 27-register, indexed by a qutrit |

> **One `E₈` node is three `E₆` nodes tied by an `A₂` bus. The branching factor is 3
> because `q = 3`.** The self-similarity is not a design choice — it is the branching rule
> of the tower the corpus already names.

And it meets existing work: `analysis/2026-07-15_pass79_fractal_tqc_scaling.md` gives the
fractal CSS family `[[2q^{2t}, 2, q^t]]`, whose tier-2 instance has **`n = 162`** physical
qudits — exactly the `(3,27)+(3̄,27̄) = 81 + 81` branching dimension.

*(A third 162 appears as an isotypic dimension of the 540-frame permutation character,
Pass 2535. Flagged, not claimed — three 162s across different objects is the count-match
shape this project rejects without a named map.)*

---

## Pass 2642 — built: `w33_holonet_node #(DEPTH)`

A recursive module. A node of depth `d`:

- holds `9 · 3^d` trits (depth 0 = one 27, a `3×3` matrix over `F₃`)
- instantiates **three** nodes of depth `d−1`
- emits **one trit** of phase, the `F₃` sum of its children's phases

The leaf is the Pass 2632 `E₆` cubic — `det` over `F₃`, already verified on all `3⁹`
inputs. So the fractal is built from a gate that is proved correct.

> **The register widens by 3 per level; the phase interface is IDENTICAL at every depth.**
> A depth-`d` assembly presents exactly the port signature of a depth-0 leaf. That is the
> precise sense in which the network of nodes is a node: same shape, different scale.

---

## Pass 2643 — the scaling law, measured and closed-form

Synthesised and placed on iCE40 UP5K at each depth:

```text
depth   leaves   trits   cells   Fmax
  0        1        9      73    126.26 MHz
  1        3       27     223
  2        9       81     673
  3       27      243    2023
```

```text
recurrence  : LC(d) = 3 * LC(d-1) + 4          (the +4 is the A2 bus: two F3 adders)
closed form : LC(d) = 75 * 3^d - 2             exact at all four measured depths
trits(d)    = 9 * 3^d = 3^(d+2)
```

### Where the chip ends and the network begins — and it is the same port

```text
depth 3 :  2023 cells,  243 trits   fits one UP5K (5280)
depth 4 :  6073 cells,  729 trits   EXCEEDS one chip
```

> **Depth 3 is the last that fits a single part. Depth 4 must cross a chip boundary — and
> the link it crosses is the same one-trit phase port that ties levels together inside the
> chip.**

That is the answer to "the computer is the network and the network is the computer",
stated as a netlist fact rather than an analogy: **the internal bus and the external link
are the same interface, so where the recursion stops being on-die is a packaging
decision, not an architectural one.** Nodes replicate inward until the fabric is full and
outward after that, by the same rule, with branching 3 throughout.

---

## Pass 2644 — what this is, and is not

**Is:** a self-similar classical datapath with an exactly verified leaf, an exact
closed-form resource law, and a single interface that serves as both intra-die bus and
inter-die link. Depths 0–3 place and route.

**Is not:** a quantum processor, a virtual-machine hypervisor, or a demonstration of
Lloyd–Braunstein universality. The "creates copies of itself as VMs" reading maps onto the
`DEPTH > 0` case — the same module image instantiated three times — but nothing here
executes software or migrates state, and no network protocol exists. The corpus's own
"universality boundary before any full braiding claim" is untouched.

**Also not claimed:** that the `E₈ ⊃ A₂ ⊕ E₆` branching is *why* a physical holonet would
be built this way. It is a branching rule that happens to have the right shape and the
right factor. That it agrees with Pass 79's `q^t` tier scaling is evidence; it is not a
derivation.

---

## Pass 2645 — the five items, honestly

The previous batch's five were **not reached**: relating my cubic to their `Cov₃`
covariants, comparing the GKP `E₈` lattice basis to `4 + 4bar`, per-lane SAT for the
involution, reading the 1821–1843 family, and pipelining the mixer.

This batch went entirely to the architecture question, which was the larger ask. Recorded
plainly rather than partially attempted.

---

## Pass 2646 — ledger

| claim | discharged by | status |
|---|---|---|
| `248 = 8 + 78 + 81 + 81` under `A₂ ⊕ E₆` | branching arithmetic | classical, cited |
| branching factor is 3 | the `(3,27)` | proved |
| recursive node builds and places | yosys + nextpnr, depths 0–3 | **measured** |
| `LC(d) = 75·3^d − 2` | exact at 4 depths | **measured** |
| phase interface identical at all depths | port signature | by construction |
| depth 4 crosses a chip boundary | 6073 > 5280 | measured |
| this is a quantum machine | — | **explicitly not claimed** |
| the three 162s are one object | — | **count match, rejected** |
| the previous five items | — | **not reached** |

---

## Prior art

- The GKP tower `A₂ < D₄ < E₈` and Lloyd–Braunstein universality — pre-existing corpus.
- `2026-07-15_pass79_fractal_tqc_scaling.md` — **owns** the fractal `[[2q^{2t},2,q^t]]`
  family this agrees with.
- Pass 2632 (mine) — the exhaustively verified `E₆` cubic leaf.
- `E₈ ⊃ A₂ ⊕ E₆` and its branching — classical Lie theory.

## Still open

- Everything in Pass 2645.
- Whether the depth-`d` assembly computes anything *useful* — the resource law and the
  interface are established; the semantics of the aggregate phase are not.
