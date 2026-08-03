## Passes 2690–2697 — two different 36s, a different 540-graph, and the paper policing itself

Reading `photonic_holonet_body.tex` lines 800–1120 in full. Four findings, two of which
are traps I was one step from walking into.

---

## Pass 2690 — there are **two** 36s, and they are not the same 36

Line 1064: *"`M₃₆` denotes injection from the **thirty-six magic rays**"*, and line 1069:
*"the same thirty-six rays that appear as the matter shell are the non-Clifford fuel"*.
The abstract gives the mechanism: *"exact Kochen–Specker budget `36/40`"*.

Line 2783: *"the **36 timetables** form `SRG(36,15,6,6)`"* — the control-plane fabric,
which Pass 2668 identified as my mixer's object.

```text
36 magic rays     : 36 of the 40 POINTS (the KS budget 36/40)
36 timetables     : the 36 SPREADS, forming SRG(36,15,6,6)
```

> **Two different 36s on two different object types.** The magic sector is a subset of the
> 40 points; the control-plane fabric is the 36 spreads. Equal cardinality, unrelated
> objects.

I was about to write that my 36-lane mixer "is the magic sector interconnect" — a
stronger and more exciting identification than "control plane". **It would have been
wrong.** Recorded because the near-miss is the useful part: this is precisely the
count-match failure this project documents, and the only thing that caught it was reading
both passages instead of one.

---

## Pass 2691 — the paper states my own methodology, in one line

Lines 935–940, on the two 2160-element boundary worlds:

> *"The rectangle side is cyclic: its stabilizer is `C₁₂` and it supplies the selector's
> phase clock. The chart-transversal side is dihedral: its stabilizer is `D₁₂` and it
> supplies the mirror transport bus. **Equal cardinality is the red herring; different
> stabilizer structure is the theorem.**"*

That is the rule I have been applying all session under the name "a count match is not a
link", stated by the manuscript itself, with a worked instance. It also flags something
about my own hardware: the `μ₄`/`μ₆` phase controller (Pass 2457) has `lcm(4,6) = 12`, and
**which of the two order-12 worlds it belongs to — the `C₁₂` clock or the `D₁₂` mirror —
I have never checked.** The paper says that distinction is the whole theorem.

---

## Pass 2692 — the paper's 540-graph is **not** my 540-graph

Line 843:

> *"The chart-adjacency web (`540` nodes, two charts adjacent when one's axis is a
> disjoint transversal pair of the other) is **`6`-regular** with exactly `1620` edges,
> and these edges are in canonical bijection with the `1620` apartments of the Tits
> building. The web has **diameter `5`**."*

The frame graph `H` I have spent many passes on — the one whose chromatic number the
parallel track bounded at `10 ≤ χ(H) ≤ 11` — is **`32`-regular** on the same 540 objects,
with `540 × 32/2 = 8640` edges.

```text
paper's chart web : 540 nodes,  6-regular,  1620 edges, diameter 5, = apartments
my frame graph H  : 540 nodes, 32-regular,  8640 edges
```

> **Same vertex set, two entirely different adjacency relations.** `χ(H) = 9` is a
> question about the frame graph, **not** about the paper's routing fabric. Nothing in the
> chromatic work bears on the routing bound, and nothing in the routing bound bears on
> `χ(H)`.

I had not stated that, and the shared `540` makes it very easy to assume otherwise.

---

## Pass 2693 — the paper's universality boundary is stricter than mine

Lines 1101–1116 give a *Conditional universality criterion* and then an explicit
**Evidence boundary**:

> *"Contextuality is a resource diagnostic, not a compiled optical protocol. Promoting the
> conditional criterion to a hardware universality theorem requires an explicit state
> preparation, injection gadget, decoder, and noise threshold… later 'matter equals magic'
> and unit-premium statements are **architectural hypotheses unless they name those
> missing maps**; the exact finite results do not establish them."*

My Pass 2634 scope paragraph said the cubic gate "is not a quantum processor and nothing
here demonstrates Lloyd–Braunstein universality physically". **That was correct and is
weaker than the paper's own boundary**, which additionally names the four missing maps.
Nothing to withdraw; recorded because it is the one place this session's scoping was
already at the manuscript's standard.

---

## Pass 2694 — the instruction set, and what I have built of it

```text
I_holo = { F_p, F_f, S_p, S_f, CX_{p->f}, sigma^5 = Z, D_12-mirror, M_36-magic }
```

Eight instructions. Against my RTL:

| instruction | built |
|---|---|
| `F`, `S` (single-qutrit Clifford frame) | no |
| `CX_{p→f}` | no |
| `σ⁵ = Z` (exact five-letter braid word) | no |
| `D₁₂`-mirror | no |
| `M₃₆`-magic injection | no |
| — | the `E₆` cubic, the control-plane mixer, the Kraft router, the phase controller |

> **I have built none of the eight named instructions.** What exists is fabric — the
> control-plane interconnect, the route decoder, a cubic form, a phase accumulator — and
> the ISA sits above it, unimplemented.

That is not a criticism of the hardware; it is the honest map. The `σ⁵ = Z` braid word is
the most tractable next one: it is exact in `ℤ[ζ₁₀]`, five letters, and a register bit
flip.

---

## Pass 2695 — the two builds not done

- **Transceiver RTL** — the maths is verified (Pass 2684: rank 24, `TᵀT = 6E₂₄`, decoder
  exact to `6.75e-16`) but the datapath is not built. Scaling by 10 makes it integer
  throughout, which is the fixed-point decision the paper leaves open.
- **Data-plane RTL** — `SRG(40,12,2,4)` still has nothing.

---

## Pass 2696 — ledger

| claim | status |
|---|---|
| the 36 magic rays are the mixer's 36 | **wrong — caught before writing it** |
| 36 magic rays ⊂ 40 points; 36 timetables = 36 spreads | established |
| "equal cardinality is the red herring" is the paper's own rule | quoted |
| the `μ₄/μ₆` controller is `C₁₂` or `D₁₂` | **never checked** |
| the paper's chart web is my frame graph `H` | **no — 6-regular vs 32-regular** |
| `χ(H)` bears on the routing bound | **no** |
| Pass 2634's scoping met the paper's boundary | yes |
| any of the eight ISA instructions built | **none** |
| transceiver / data-plane RTL | not built |

---

## Prior art

- `photonic_holonet_body.tex` §"Hypercube networking", §"The middleware", §"The software"
  — own the chart web, the two 2160 worlds, the ISA and the universality boundary.

## Still open

- Which order-12 world the `μ₄/μ₆` controller lives in.
- Transceiver and data-plane RTL; any ISA instruction.
- Lines 1220–2400 and the whole physics half unread.
