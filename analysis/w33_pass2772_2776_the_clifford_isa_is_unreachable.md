## Passes 2772–2776 — six of the eight opcodes cannot move the machine

The Pass 2753 finding was stated as *"a module folds to a constant"*. That is the
symptom. Chasing the property underneath it turns a bug report into a statement about
the instruction set.

---

## Pass 2774 — the result: **1, 1, 81**

Breadth-first search over all `3⁴ = 81` Pauli frames, starting from the reset frame
`(0,0,0,0)`, using the opcode semantics transcribed from `w33_pass2762_frame_step`:

```text
reachable frames from reset (0,0,0,0), out of 81:
  CX alone                    (w33_qutrit_cx_frame) : 1
  all six symplectic opcodes                        : 1
  full ISA, symplectic + sigma^5 = Z                : 81

  all six symplectic opcodes preserve the form      : True
  sigma^5 = Z fixes the origin (i.e. is linear)     : False
```

> **All six Clifford opcodes together still reach exactly one frame.** `F_p`, `F_f`,
> `S_p`, `S_f` and `CX` in both directions are symplectic, symplectic maps are **linear**,
> and every linear map fixes the origin. From reset they are collectively inert.
>
> **The entire 81-frame space is reachable because of one instruction.** `σ⁵ = Z`
> increments a `Z` component — an **affine translation**, the only opcode in the ISA that
> is not a linear map.

That is a design principle rather than a defect: **an all-Clifford frame machine is
inert, and the ISA needs at least one non-symplectic instruction to be able to compute at
all.** `σ⁵ = Z` is carrying that load, and nothing in the ISA documentation says so.

### It also explains the Pass 2753 fold exactly

| module | translation opcode | reachable from reset | synthesis |
|---|---|---|---|
| `w33_qutrit_cx_frame` (Pass 2757) | none | `{0}` | **folds to the identity** |
| `w33_pass2762_holonet_isa` (Pass 2766) | `σ⁵ = Z` | all 81 | fine |
| `w33_cx_loadable_frame` (Pass 2752) | load port | all 81 | fine |

So the parallel track's **full eight-opcode ISA controller is sound** — the fold is
confined to the standalone CX wrapper, which has no way to inject. Reachability is the
exact statement; the synthesis fold is one tool's shadow of it.

---

## Pass 2772 — the fold guard, and what it found across all of `rtl/`

`scripts/check_rtl_folds.py`: run `flatten; opt -full` on every module and report output
ports that end up tied to a literal. Simulation cannot see this class of defect at all —
a module that folds to a constant still simulates correctly, it just does nothing.

First repo-wide sweep, 20 files:

```text
  w33_pass2757_qutrit_cx.sv:w33_qutrit_cx_frame
    CONSTANT OUTPUT after opt: xp, zf

  w33_spread_mixer36.sv:w33_spread_mixer36            NOT SYNTHESIZED
  w33_spread_mixer36.sv:w33_single_j_phase_controller NOT SYNTHESIZED
```

Everything else — including all four of the parallel track's Pass 2767–2771 modules and
the eight-opcode ISA — is clean. Wired into pre-commit, scoped to `rtl/`, warns and never
blocks.

**Two bugs in the guard itself, both worth recording.** It first reported *nothing*,
because the WSL mount is `/mnt/c` while `pathlib` resolves the drive to `C:` and my
lower-casing hit the `/mnt/` prefix instead of the drive letter — every `cd` failed
silently and the sweep looked clean. A guard that silently passes is worse than no guard;
it now reports `NOT SYNTHESIZED` explicitly rather than treating a missing netlist as a
pass. It also needs relative paths throughout: the repo root is `c:\Repos\Theory of
Everything`, and a drive colon plus two spaces breaks both the WSL translation and
yosys's own argument splitting.

---

## Pass 2773 — a file marked "synthesizable" that neither frontend accepts

`rtl/w33_spread_mixer36.sv` (Pass 2206, added 2026-08-02) is headed *"synthesizable
reference datapaths for the exact W(3,3) spread mixer"*. Both toolchains reject it, for
**different** reasons:

```text
yosys    :7   syntax error, unexpected '['            <- unpacked array PORTS, x [0:35]
iverilog :10  unpacked array parameters are not       <- the MASK localparam
              supported yet
```

Two frontends, two unsupported constructs, one file that has therefore never been
simulated or synthesized since it was committed.

`rtl/w33_pass2773_spread_mixer36_synth.sv` is a port, not a new datapath: identical
arithmetic, with unpacked ports replaced by one packed bus and the unpacked mask by a
packed 1296-bit constant. Sharing that constant with its own proof took three attempts —
a hierarchical reference is not a constant expression to iverilog, and this yosys rejects
`import` in both the ANSI and body positions, so a text macro is the only mechanism both
accept.

Proved on the input class that separates a correct signed mixer from the unsigned trap
that corrupted 91% of the lane checks earlier in this track — single-lane impulses at the
most negative value:

```text
Solving problem with 1097152 variables and 3185010 clauses..
SAT proof finished - no model found: SUCCESS!
```

### And the number that was never measured

```text
synth_ice40, W = 16, OW = 20:   13965 SB_LUT4   +   799 SB_CARRY
```

> **The fully parallel 36-lane mixer does not fit on any iCE40 in this toolchain** — its
> LUT4 count alone is **1.8× the HX8K's 7,680 logic cells** and 2.6× the UP5K's 5,280.

Which is precisely why Pass 2612's serial mixer exists. The pair now has a measured
trade: **4,048 LC serial at 19.65 MHz versus ~14,000 cells parallel** — about 3.5× the
area for 36× the throughput, and only the serial one is buildable on the target part.

---

## Pass 2775 — the transpose, reconciled across tracks

My Pass 2750 and the parallel track's Pass 2762 are the same object from two directions,
and theirs cites mine:

- **Theirs (Pass 2762):** the explicit matrix `T` with `T² = I` and `Tᵀ J T = −J`; it
  *"normalizes Sp(4,3) but is not an element of it"*; `T · CX_{p→f} · T⁻¹ = CX_{f→p}`;
  and the local-Fourier identity `CX_{f→p} = (F_p F_f⁻¹) CX_{p→f} (F_p⁻¹ F_f)`, so the
  outer operation is **not needed in the gate library**. They also count its action on
  classes: **20 of the 34 classes are exchanged in 10 pairs, 14 are fixed.**
- **Mine (Pass 2750):** the same `T` is outer exactly when its multiplier `−1` is a
  non-square, i.e. exactly when `q ≡ 3 (mod 4)`.

These agree and neither subsumes the other: they have the exact `q = 3` matrix and its
class action; I have the congruence that says *why* `q = 3` is special and what happens at
other `q`. Their `Tᵀ J T = −J` is the multiplier-`−1` statement, so their computation is
the `q = 3` instance of my criterion — the first cross-track confirmation of the Pass 2732
transpose identification by an independent construction.

**Their Pass 2765 also corrects an evidence boundary I should not restate wrongly:** a
measured deterministic single-photon qutrit SUM *does* exist — Imany et al., *npj QI* **5**,
59 (2019), frequency control and time target, fidelity `0.92 ± 0.01`.

---

## Pass 2776 — ledger

| claim | status |
|---|---|
| six Clifford opcodes reach 1 frame from reset | **exact, BFS over all 81** |
| the full ISA reaches all 81 | exact |
| `σ⁵ = Z` is the only non-linear opcode | exact; it fixes nothing |
| an all-Clifford frame machine is inert | follows: symplectic ⇒ linear ⇒ fixes 0 |
| the parallel track's eight-opcode ISA | **sound; the fold is only the CX wrapper** |
| `w33_spread_mixer36.sv` is synthesizable | **false — neither frontend parses it** |
| ported mixer, signed impulse correctness | **SAT-proved, 1097152 vars / 3185010 clauses** |
| parallel mixer fits an iCE40 | **no — 13,965 LUT4 vs 7,680 on HX8K** |
| fold guard's first sweep silently passed | **my bug: `/mnt/C` vs `/mnt/c`** |
| transpose is outer iff `q ≡ 3 (mod 4)` | agrees with their `Tᵀ J T = −J` at `q = 3` |

---

## Prior art

- `rtl/w33_pass2762_holonet_isa.sv`, `analysis/BT2762_BT2766_five_frontiers.md` — **own**
  the eight-opcode ISA, the `T` matrix, the CX direction-reversal identity, and the
  transpose's action on the 34 classes.
- `rtl/w33_pass2757_qutrit_cx.sv` — **owns** the CX instruction and its class certificate.
- `rtl/w33_pass2612_serial_mixer.sv` — owns the serial mixer this now has a parallel
  comparison for.
- Imany et al., *npj Quantum Information* **5**, 59 (2019) — the measured qutrit SUM.

## Still open

- **Does the ISA need a second non-symplectic instruction?** One translation generator
  makes the frame space reachable; whether one is enough for the intended computation is
  not answered by reachability alone.
- `w33_spread_mixer36.sv` (the unparseable original) should be retired or fixed in place;
  I added a port rather than editing another track's file.
- Re-measure `F`/`S` (13 LC) and `σ⁵ = Z` (21 LC) with load ports — same correction as CX.
- A guard for *implicit* novelty framing.
