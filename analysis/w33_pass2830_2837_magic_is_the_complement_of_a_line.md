## Passes 2830–2837 — magic is the complement of a line, and a readout costs 8/3 bits

---

## Pass 2835 (outside the programme) — `M₃₆` is `W(3,3)` **minus one line**

The 36 magic rays have been treated throughout as an external resource the substrate
happens to supply. But the substrate's address space is the 40 points of `W(3,3)`, and
`40 − 36 = 4`, and a **line of `W(3,3)` has exactly 4 points.**

Adjoin the four coordinate axes `e₁…e₄` to the 36 rays and compute the orthogonality
graph on all 40:

```text
orthogonality degrees : {12: 40}
lambda values         : [2]        mu values : [4]

ORTHOGONALITY GRAPH IS SRG(40, 12, 2, 4)
W(3,3) collinearity graph is SRG(40, 12, 2, 4) : True

the four axes are mutually orthogonal (a 4-clique = a LINE) : True
each magic ray is orthogonal to exactly one axis            : True  ({1: 36})
points per axis (the GQ 'nearest point' partition)          : {0:9, 1:9, 2:9, 3:9}
```

In a generalised quadrangle of order `(3,3)` the lines are exactly the 4-cliques of the
collinearity graph, and the defining axiom is that every point off a line is collinear
with **exactly one** point of it. Both hold.

> **`M₃₆` is the complement of a single line in `W(3,3)`.**
>
> The machine's address space is 40 points. Four of them — one line — are the
> computational basis, which is exactly the stabilizer part. **The other thirty-six are
> all magic.** Magic is not a resource bolted onto the substrate; it is the *generic
> condition* of the substrate's own address space, and the stabilizer states are the one
> distinguished line you delete to remove it.

The four families `A/B/C/D` of nine that the ray construction produces are not a
notational artefact either: they are the GQ *nearest-point* partition, one family per
point of the deleted line.

**And the group cuts across the geometry.** The Clifford classes are `4+8+12+12`
(Pass 2797); the geometric families are `9+9+9+9`. Neither refines the other.

---

## Pass 2836 (outside the programme) — one support readout erases **exactly 8/3 bits**

The support map sends `(x_p, z_p, x_f, z_f) ∈ F₃⁴` to the 4-bit mask of which
coordinates are nonzero. A mask of weight `k` has exactly `2ᵏ` preimages and there are
`C(4,k)` of them:

```text
weight 0: 1 x 1   weight 1: 4 x 2   weight 2: 6 x 4
weight 3: 4 x 8   weight 4: 1 x 16       total 81 = 3^4
```

```text
H(state | support) = 216/81 = 8/3 bits EXACTLY = 2.666666667
H(state)           = log2 81                   = 6.339850003
H(support)                                     = 3.673183336
support channel efficiency = 3.673183 / 4      = 91.830 %
```

> **A support readout destroys exactly `8/3` bits.** Landauer: `E ≥ (8/3) k_B T ln2 =
> 7.656 × 10⁻²¹ J = 47.78 meV` at 300 K, or `7.66 pW` of unavoidable dissipation at a
> 1 GHz readout rate.

### The closed form, and why `q = 2` is the tell

```text
H(state|support) = 4 (q-1) log2(q-1) / q      verified exactly at q = 2,3,4,5,7,8,9,11
```

At `q = 2` it is **exactly zero** — over `F₂` the support *is* the state, so a support
readout destroys nothing.

> Every one of the `8/3` bits is the price of the third field element. That is the
> thermodynamic statement of *support for readout, phase for execution*: **the phase is
> precisely the part you pay to look at.**

### A bound that lands on the other track's observer

Their Pass 2827 proves no **seven** support taps suffice to reconstruct the frame and
that exactly **48 eight-tap** selectors do. The information-theoretic floor is
`⌈log₂ 81⌉ = 7` bits.

> **Their observer sits exactly one bit above the counting floor, and their exhaustive
> search proves that bit is necessary rather than slack.** Two independent arguments —
> one from counting, one from search — meeting at 7 and 8.

---

## Pass 2830 — nothing an overlap can see separates the two 12-ray classes

The full **stabilizer overlap spectrum** — the multiset of `|⟨s|ψ⟩|²` over all 60
two-qubit stabilizer states — is a Clifford invariant, and every stabilizer Rényi
entropy and overlap moment is a function of it. In exact ninths:

```text
class 0 ( 4 rays): 0/36 x4, 3/36 x18, 6/36 x12, 12/36 x9, 15/36 x12, 24/36 x3, 27/36 x2
class 1 ( 8 rays): 0/36 x3, 2/36 x9,  6/36 x27, 12/36 x9, 18/36 x3,  22/36 x9
class 2 (12 rays): 0/36 x2, 1/36 x4, 2/36 x2, 3/36 x8, 5/36 x2, 6/36 x14, ... 25/36 x2
class 3 (12 rays): 0/36 x2, 1/36 x4, 2/36 x2, 3/36 x8, 5/36 x2, 6/36 x14, ... 25/36 x2
```

> **The two 12-ray classes have the identical spectrum.** No stabilizer-overlap statistic
> separates them — not `F_stab`, not any Rényi entropy, not any moment. They differ
> **only** in the group action.

Distinct spectra across all four classes: **3**. So the entire 60-value distribution has
exactly the same resolving power as its single largest entry.

**Engineering consequence.** A protocol that depends on its input only through overlap
statistics *must* treat the two classes alike. The split can matter only to a protocol
that uses the ray's Clifford orbit — one that fixes a frame and cares which
representative it was handed.

---

## Pass 2831 — the yield, and the number that decides whether any of this is usable

The parallel track's PR #210 gives the accepted-round recurrence and its fixed points
`0, 2/3, 1` with `2/3` repelling — reproduced here exactly (`|dp′/dp| = 1.2` at `2/3`).
Convergence is half an engineering answer. Cost is the other half.

Each round consumes **two** inputs and succeeds with probability `P_succ`, so the raw
cost multiplies by `2/P_succ` per round.

```text
raw states consumed to reach a target output infidelity
 start p        1e-3              1e-6                1e-9
   0.10     2.3e7  (r=12)     4.0e17 (r=29)      6.9e27 (r=46)
   0.20     5.6e8  (r=14)     9.7e18 (r=31)      1.7e29 (r=48)
   0.30     1.5e10 (r=16)     2.6e20 (r=33)      4.5e30 (r=50)
   0.50     1.1e14 (r=21)     1.9e24 (r=38)      3.2e34 (r=55)
```

### Why the numbers are that large

```text
dp'/dp at p = 0 : 0.666667   (exactly 2/3)
P_succ at p = 0 : 0.500000   (exactly 1/2)
```

> **The map is *linearly* convergent with rate `2/3`: each accepted round multiplies the
> noise by two thirds; it does not square it.** Standard distillation is quadratic or
> cubic — the 15-to-1 Reed–Muller routine gives `p′ ≈ 35p³` — and that difference is the
> whole game, because a linear map needs a number of rounds *logarithmic* in the target
> while every round doubles the raw cost.

**So the deep-grade branch is a genuine fidelity-improving map, a genuine refutation of
the earlier no-go, and not by itself a usable distillation routine.** What it establishes
is that the resource is not inert. Making it practical needs a branch with super-linear
convergence, or a portfolio composing several of the 48 — which is exactly the parallel
track's own stated next step, now with a quantified reason.

---

## Pass 2832 — three copies: an honest negative

`F_stab` is exactly multiplicative on two copies (Pass 2798). Three copies live in six
qubits, where the `315,057,600` stabilizer states cannot be enumerated — but the question
has a **one-sided** rigorous answer: exhibiting one stabilizer state with overlap above
`F³` *proves* super-multiplicativity.

`40,000` random 24-gate Clifford words per grade found **no witness**; the best sampled
overlap equalled `F³` exactly in all three cases.

> This is **not** a proof of multiplicativity at three copies — the sampled fraction is
> negligible. What it establishes is that the obvious product constructions do not beat
> `F³`, so if three-copy protocols outperform two-copy ones here, the advantage does not
> come from a super-multiplicative stabilizer fidelity.

---

## Pass 2834 — the readout is a **diode**, proved at the gate level

*Support for readout, phase for execution* is a theorem about the mathematics. It
constrains no netlist: an engineer can wire the cheap 4-bit mask back into the datapath,
and the result passes simulation almost always — support *is* preserved by most
operations — and drifts the first time a translation fires on a register holding a `2`.
Same failure shape as Pass 2753's folded registers: correct in simulation, wrong in
silicon, invisible to the testbench.

`scripts/check_information_flow.py` flattens the design to gates, builds the driver
graph, and computes reachability in both directions:

```text
top w33_support_readout_diode: 59 cells after flatten+opt
reverse: support_mask,tamper_mask reaches none of xp_o, zp_o, xf_o, zf_o
forward: every frame register reaches the mask
PASS: the readout is a diode -- state reaches the mask, the mask reaches no state.
```

**Self-tested against a negative control**, because a guard that can only pass is not a
guard (Pass 2781): rewiring the tamper input into the load enable makes it report
`VIOLATION` on all four registers.

The non-congruence witness is also asserted in the netlist itself and SAT-proved
(`228` variables, `600` clauses): `(0,1,0,0)` and `(0,2,0,0)` share a mask, and after
`Z_p` they do not.

> This is what *typed* should mean in hardware: not a naming convention, a reachability
> proof over the synthesised gate graph. An information-flow violation is the one thing
> this repo's guards **fail** on rather than warn about — unlike a rediscovery collision,
> a backward edge has no benign reading.

---

## Pass 2833 — the same designs on the part the other track targets

| design | HX8K CT256 | | UP5K SG48 | |
|---|---:|---:|---:|---:|
| | LC | `F_max` | LC | `F_max` |
| minimal engine, 4 ops | 43 | **208.86 MHz** | 43 | 72.40 MHz |
| public unit, 6 opcodes | 72 | 175.72 MHz | 72 | 60.80 MHz |
| engine + support readout | 48 | 207.64 MHz | 48 | 72.05 MHz |

Two things fall out. **The UP5K figures in the blueprint understate speed by about
2.9×** — same cells, different silicon. And **the support readout costs 5 logic cells and
0.6 % of `F_max`**: the cheap layer really is cheap, and now it is cheap *and* provably a
diode.

---

## Pass 2837 — ledger

| claim | status |
|---|---|
| `M₃₆ = W(3,3)` minus one line | **proved** — SRG(40,12,2,4), axes are a 4-clique |
| every magic ray meets that line exactly once | proved (the GQ axiom) |
| families `9+9+9+9` are the nearest-point partition | proved |
| Clifford classes `4+8+12+12` do not refine it | observed |
| support readout erases exactly `8/3` bits | **proved** |
| `H = 4(q−1)log₂(q−1)/q`, zero at `q=2` | proved at 8 field sizes |
| Landauer `47.78` meV at 300 K | derived |
| observer is one bit above the counting floor | derived + their search |
| the two 12-ray classes share the full overlap spectrum | **proved** |
| spectrum resolves 3 of 4 classes | proved |
| deep-grade map is **linearly** convergent, rate `2/3` | **proved** |
| `~10²⁷` raw states for `10⁻⁹` infidelity | computed |
| three-copy super-multiplicativity | **no witness** — not a proof either way |
| readout diode, gate-level | **proved**, with negative control |
| HX8K: 43 LC @ 208.86 MHz | **measured** |

---

## Prior art

- **Parallel track PR #210 / Pass 2821** — **owns** the deep-grade distillation
  recurrence, its fixed points, and the 48 improving branches. This pass adds the yield
  and the convergence rate.
- **Parallel track Pass 2822** — **owns** *support for readout, phase for execution* and
  the `16→40→78→81` refinement. This pass adds the gate-level enforcement and the
  thermodynamic cost.
- **Parallel track Passes 2825–2828** — **own** the finite-delay support observer, the
  eight-tap minimum and the distance-four telemetry code.
- `docs/index.html` P1021 — owns the `6:1` fibration `240 E₈ roots → 40 W(3,3) points`,
  which is why the Witting diagonals are the address space in the first place.

## Still open

- A super-linearly convergent branch among the 48, or a portfolio that composes them.
- Whether the two 12-ray classes differ under *any* operational figure of merit.
- Three-copy `F_stab`: no enumeration, no witness, no proof.
