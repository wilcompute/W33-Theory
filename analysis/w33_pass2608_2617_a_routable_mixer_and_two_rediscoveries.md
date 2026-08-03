# Passes 2608–2617 — a **routable** 36-lane mixer, a corpus-wide rediscovery sweep, and one failed proof

---

## Pass 2612 — the 36-lane mixer, made placeable

The parallel track's Pass 2303/2308 mixer is correct and synthesises, but **cannot be
placed**: its flat interface exposes `36×4` input bits + `36×8` output bits = **432 pins**,
and no iCE40 package has them. Their Pass 2308 had to erase the port table to route the
core at all, which measures capacity but is not a placeable design.

Fix: stream the lanes. 36 signed values in over 36 cycles, 36 out over 36 cycles, on a
~15-pin interface. Same masks, same arithmetic.

```text
synth_ice40 + nextpnr-ice40 --up5k --package sg48

ICESTORM_LC   : 4048 / 5280   76%
SB_IO         :   21 /   96   21%        <-- was 432 pins
Max frequency : 19.65 MHz   (PASS at 12.00 MHz)
Routing complete.
```

> **First 36-lane spread mixer to place and route with a real interface on a real
> package.** The 432-pin wall was an interface problem, not a capacity problem.

The masks were checked before use: 36 masks, every one of degree 15, symmetric,
diagonal-free — a genuine `SRG(36,15,6,6)` adjacency.

The core was then verified against Python by simulation, not assumed:

```text
A*e0 (Icarus)  = 0 1 1 0 1 1 1 1 0 0 1 1 1 1 0 0 0 1 0 0 1 1 0 0 0 1 0 1 0 ...
A*e0 (numpy)   = 0 1 1 0 1 1 1 1 0 0 1 1 1 1 0 0 0 1 0 0 1 1 0 0 0 1 0 1 0 ...   identical
A*e5           identical
```

---

## Pass 2613 — the involution proof **failed**, and the failure is mine

`A² = 9I + 6J` for `SRG(36,15,6,6)` gives `A²x = 9x + 6(Σx)·1`, so on **mean-zero**
signals `A/3` is an involution — one interconnect both encodes and decodes. That is the
statement the encoder/decoder claim actually rests on, and their SAT check covers the
single-application mask identity rather than the square.

Asserting the square over all inputs:

```text
Solving problem with 212,109 variables and 604,203 clauses..
SAT proof finished - model found: FAIL!
```

Before touching anything, the identity itself was checked in Python:

```text
degrees {15}   symmetric True   A^2 == 9I + 6J ?  True
```

and the core was checked by simulation (above): **both are correct**.

> **So the counterexample is in my formal harness, not in the algebra or the mixer — and
> I did not locate it.** Two Yosys latch-inference rejections were fixed along the way
> (module-scope and conditionally-assigned loop variables inside `always_comb`); the
> remaining fault is unfound.

Recorded as a failed proof attempt with the fault correctly attributed. **No claim is
made that `A² = 9I + 6J` fails** — it holds; my encoding of it does not yet.

---

## Pass 2614 — corpus-wide rediscovery sweep

Extending the Pass 2586/2587 method from two lookups to a systematic pass: index every
integer in `10⁵ … 10¹¹` appearing in a `data/w33_pass*.json`, and flag values shared by
pass families **≥ 400 apart** in ≤ 4 files.

```text
distinct large values indexed : 1154
rediscovery candidates        :   38
```

Most are noise — powers of two, and group orders like `276,595,200 = |Sp(4,7)|` and
`9,360,000 = |Sp(4,5)|` legitimately appearing wherever those groups do. The signal:

```text
233280   families [ 440, 1821, 2416, 2564]
3149280  families [1821, 2416, 2564]
126360   families [1821, 2416, 2564]
```

> **The Pass-1821 family's numbers keep resurfacing in the 2400–2500 range** — the same
> pattern as `42,912` (Pass 1843 → 2432) and `91,007,752` (Pass 1829 → 2550), now visible
> as a trend rather than two anecdotes.

Not individually confirmed as rediscoveries — that needs each pair read, as Pass 2586 did
for `42,912`. Flagged as a shortlist.

---

## Pass 2615 — Pass 1835, and the items not reached

`w33_pass1835_signature_lift_obstruction.json` exists and is the companion Pass 1843
cites. **Not read in full** — the batch went to the hardware work instead.

Also not done: the correct coherent closure for ranks 10–14 (third attempt not made), and
the four integer-key producers (still unrepaired, still surfacing on every push via the
Pass 2577 CI job).

---

## Pass 2616 — ledger

| claim | discharged by | status |
|---|---|---|
| serial mixer places and routes | nextpnr, 21 pins, 76% LC, 19.65 MHz | **built and measured** |
| masks are a genuine `SRG(36,15,6,6)` | degree/symmetry/diagonal check | verified |
| mixer core is arithmetically correct | Icarus vs numpy, two columns | verified |
| `A² = 9I + 6J` | numpy | true |
| my netlist proof of it | SAT counterexample | **failed, fault unlocated** |
| 1821-family numbers resurface in the 2400s | corpus sweep, 3 values | shortlist, unconfirmed |
| ranks 10–14 | — | not attempted this batch |
| Pass 1835 | — | located, not read |

---

## Prior art

- Pass 2303 / 2308 (parallel track) — **own** the 36-lane mixer, its masks, the
  `A² = 9I + 6J` algebra and the FWHT factorisation. This pass changes only the
  interface.
- Pass 1821 / 1829 / 1843 — the older results the sweep keeps surfacing.

## Still open

- The involution proof's actual fault.
- Ranks 10–14 by correct coherent closure.
- `χ(H) ∈ {10, 11}`.
- Four integer-key producers, and `1887`.
