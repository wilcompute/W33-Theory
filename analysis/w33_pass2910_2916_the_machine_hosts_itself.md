## Passes 2910–2916 — the machine hosts itself, and the last opcode is built

---

## Pass 2912 (outside the programme) — the exact cost of a virtual machine

The frame is two qutrits. A **one**-qutrit machine is a strictly smaller machine of the
same kind, so this processor can host one — and the question a hypervisor author actually
needs is the emulation overhead, exactly.

That is a shortest-word length in the host's Cayley graph, and Pass 2866 already computed
every one of those.

```text
host  : F_p, CX_pf, CX_fp, Z_p        (two qutrits, 4 ops, 2-bit opcode)
guest : F, S, Z on the past register  (one qutrit)

guest instruction   host instructions
  F_guest                 1
  S_guest                 8
  Z_guest                 1

VIRTUALISATION OVERHEAD: worst 8x, mean 3.33x
```

> **The whole cost is `S`.** `F` and `Z` are free — one host instruction each — and the
> guest's phase gate costs eight, because Pass 2789's minimal triple *dropped* `S`.

So the minimality that saves 40 % of the logic cells costs **8× on one guest opcode**.
That is a real, previously unnamed hardware/hypervisor trade, and it is exact rather than
estimated.

### And the isolation is structural

Two guests fit on disjoint register pairs. The only opcodes coupling the halves are the
two `CX` directions.

> **A hypervisor that never issues `CX` to a guest cannot leak between guests** — no MMU,
> no tagging, no permission check. The isolation is a consequence of the algebra, not of
> an enforcement mechanism, which is an unusually strong guarantee to get for free.

---

## Pass 2914 — the hypervisor, measured

`rtl/w33_pass2914_d12_mirror_and_hypervisor.sv`, HX8K CT256, one physical datapath and
`N` guest contexts:

| `N` | shared | replicated (`43N`) | area saved | per-guest throughput |
|---:|---:|---:|---:|---|
| 1 | 42 LC @ 175.1 MHz | 43 | — | 175.1 MHz |
| 2 | 74 LC @ 134.9 | 86 | 14 % | 67.5 MHz |
| 4 | 118 LC @ 128.5 | 172 | 31 % | 32.1 MHz |
| 8 | 180 LC @ 113.4 | 344 | **48 %** | 14.2 MHz |
| 16 | 339 LC @ 91.1 | 688 | **51 %** | 5.7 MHz |

> Sharing wins on area at every `N ≥ 2` and converges to about **half** — because half the
> cost is the shared datapath and half is per-context storage, and only the first half is
> shareable.
>
> The price is throughput: `N` guests time-share one datapath, so per-guest speed falls as
> `F_max/N`. At `N = 8` that is **48 % of the area for 1/15 of the per-guest speed**.

Both numbers are measured in the same harness, so the crossover is a real design curve
rather than an argument.

---

## Pass 2914 — `D₁₂`-mirror: the last unbuilt opcode is built

It sat in the blueprint's *not built* list with the honest note that it has no register
semantics. True, and not a reason not to build it.

An earlier attempt was withdrawn because it was built as a **phase accumulator**: `R₄` and
`U₆` do not commute (their commutator has order 4), so the object is dihedral `D₁₂`, not
cyclic `C₁₂`. A counter is the wrong circuit. The right one is a rotation register plus a
reflection bit — which is what a dihedral group *is*:

```text
D_12 = <r, s | r^6 = s^2 = 1, s r s = r^-1>,  order 12
21 ICESTORM_LC, 255.56 MHz on HX8K CT256
SAT: 115 variables, 308 clauses, SUCCESS -- s r s = r^-1 holds
```

> The relation `s r s = r⁻¹` is asserted **in the netlist**, because a phase accumulator
> satisfies every other property of this module and fails exactly that one. The circuit
> that was withdrawn would fail this proof.

Advancing while reflected runs the rotation backwards. That single line is the entire
difference between the dihedral group and a twelve-state counter.

---

## Pass 2910 — three copies: an exhaustive sub-family result, honestly scoped

Reformulating the first-order condition as a **set cover**: each `(Pauli, sign)` factor
has a kill set — which of the nine single-error vectors it annihilates — and a stabilizer
projector's kill set is the union of its factors'.

```text
non-identity Paulis on 6 qubits          : 4095
usable factors (kill >=1 single, spare |mmm>) : 18
kill-set sizes                           : {1: 18}   -- every one kills exactly ONE
commuting family covering all nine       : NONE
```

> Over the **factor-wise family** the search is exhaustive and the answer is no.

**It is not a proof over all stabilizer projectors,** and a first draft of this pass said
it was. `P` annihilates `v` iff `v` has no component in the joint eigenspace, which can
happen without any single factor killing `v` — so the factor-wise family is strictly
smaller. The overclaim is withdrawn.

What stands: **two structurally different searches now return nothing** — this one
exhaustive over the natural sub-family, and Pass 2881's 30,000 general projectors — on top
of Pass 2861's exhaustive two-copy no-go. Strong evidence that the obstruction is not
about copy count. Evidence, not a theorem.

---

## Pass 2911 — the Hodge `15` is **not** the support shell

Pass 2884 found `240 = 81 + 120 + 24 + 15` and refused to identify the `15` with the
support shell on a count match. The same character test that settled the `81`s settles
this.

Acting with a genuine symmetry — the swap of the two qutrit blocks; a bare 4-cycle on
coordinates is *not* a symmetry, and the first draft crashed on exactly that:

```text
trace on the lambda = 16 eigenspace : 7/3 = 2.333333
fixed subsets of the support shell  : 3
characters agree                    : False
```

> **Refuted.** And more sharply than by inequality alone: the trace is `7/3`, which is
> **not an integer**, while a permutation module's character always is. The `λ=16`
> eigenspace cannot be a permutation module at all, and the support shell is one.

The count match at `15` is arithmetic, exactly as Pass 2884 suspected. Second coincidence
of that shape tested and killed in three passes.

---

## Pass 2915 — the power model, with measured topology

The Pass 2864 estimate assumed one unit of switched capacitance per logic cell. The real
netlist says otherwise:

```text
driven nets 52   total sinks 106   mean fanout 2.0385
fanout histogram {1:21, 2:20, 3:6, 4:1, 5:3, 8:1}
```

> **The flat model understates switched capacitance by `2.04×`.** Corrected:
> `0.502 pJ → ~1.02 pJ` per operation, and `0.105 mW → ~0.21 mW` at 208.86 MHz.

Still modelled — the per-unit capacitance is still assumed — but one of the two
assumptions in Pass 2864 has been replaced by a measurement of the actual topology. One
assumption left.

---

## Pass 2916 — ledger

| claim | status |
|---|---|
| VM overhead: worst `8×`, mean `3.33×` | **proved** (shortest words) |
| the entire cost is the guest's `S` gate | proved |
| guest isolation is structural, not enforced | follows from the ISA |
| hypervisor `N=1,2,4,8,16`: `42,74,118,180,339` LC | **measured**, HX8K |
| sharing saves up to `51 %` of area | measured |
| per-guest throughput falls as `F_max/N` | structural |
| `D₁₂`-mirror: `21` LC, `255.56` MHz | **measured** |
| `s r s = r⁻¹` holds in the netlist | **SAT**, 115 vars |
| three-copy factor-wise family | **exhaustive**, no witness |
| \quad over all stabilizer projectors | **not a proof** — overclaim withdrawn |
| Hodge `15` is not the support shell | **proved** — trace `7/3` is not an integer |
| mean fanout `2.0385` | **measured** |
| power `~1.02` pJ/op | **modelled**, one assumption left |

---

## Prior art

- Parallel track Passes 2847–2853 — own the affine-square feature encoder, the adaptive
  observer (worst-case depth 4), and the noisy `M₃₆` operating boundary
  `g_c = (7−3√5)/4`. The hypervisor here shares no code with them.
- `docs/index.html` — owns the Hodge spectrum used in Pass 2911.

## Still open

- Whether the `24` in the Hodge budget is a map (the `15` is now refuted).
- A three-copy proof over *all* stabilizer projectors, not just the factor-wise family.
- Per-unit capacitance: the last assumed constant in the power model.
