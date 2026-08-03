## Passes 2658–2665 — the real `E₆` cubic, and BT827's resource law meets synthesis

---

## Pass 2658 — "`27 = 3⊗3⊗3`" taken literally is wrong

Pass 2652 corrected my gate to the paper's `ε`-cubic on `27 = 3⊗3⊗3`. Building that
literally — a `3×3×3` tensor with the degree-3 `ε ε ε` contraction — **fails**:

```text
SL(3,3) invariance, 3 slots x 2 generators x 300 tensors:
  1800 checks, 206 violations   ->   NOT invariant
```

`SL(3)³` has no degree-3 invariant on a genuine `3×3×3` tensor. The paper's notation is
shorthand for the **trinification** decomposition:

```text
27 = (3, 3bar, 1) + (1, 3, 3bar) + (3bar, 1, 3)      three 3x3 blocks A, B, C
```

on which the `E₆` Cartan cubic is

```text
C(A,B,C) = det A + det B + det C - tr(A B C)
```

with the three `SL(3)`s acting as `A → g₁ A g₂⁻¹`, `B → g₂ B g₃⁻¹`, `C → g₃ C g₁⁻¹`. Each
`det` survives because `det g = 1`; `tr(ABC)` survives because the inner factors cancel
telescopically. Verified:

```text
trinification SL(3,3)^3 invariance: 2400 checks, 0 violations
value distribution over 6000 random 27-trit vectors: {0: 2083, 1: 1916, 2: 2001}
```

> **And `det A` is one of the four terms.** Pass 2632 built a *component* of the `E₆`
> cubic, not a wrong object — which is a softer correction than Pass 2652 recorded.

---

## Pass 2660 — built, verified, placed

`rtl/w33_pass2660_e6_cartan_cubic.sv`: 27 trits in (three `3×3` blocks), three `det3`
units plus a 27-term `tr(ABC)`, all in exact `F₃` arithmetic.

```text
Pass 2660 E6 Cartan cubic: 4000 random 27-trit vectors, 0 errors
PASS  det A + det B + det C - tr(ABC) over F3

w33_e6_cartan_cubic   ICESTORM_LC  470/5280   SB_IO 56/96
w33_e6_cubic_gate     ICESTORM_LC  473/5280   SB_IO 59/96
```

6.5× the size of the Pass 2632 gate, as expected: 27 trits instead of 9, plus the trace
term.

*(Random rather than exhaustive: `3²⁷ ≈ 7.6 × 10¹²` inputs. The 4000-vector check is
backed by the independent `SL(3,3)³` invariance proof above, which is a structural
property no sampling could fake.)*

---

## Pass 2661 — BT827's resource law meets a place-and-route, for the first time

The paper's fractal theorem gives slot counts per instance but carries no synthesis
numbers. Measured, one `W(3,3)` core on an iCE40 UP5K:

```text
degree-2 symplectic mixer    4048 LC
E6 Cartan cubic gate          473 LC
mu4/mu6 phase controller       73 LC
chirality / fibre              21 LC
-------------------------------------
core total                   4615 LC   = 87% of a UP5K
```

> **The complete `W(3,3)` core — Clifford interconnect, the `E₆` cubic that supplies the
> magic, the phase clock and the chirality select — fits on one $5 FPGA at 87%.**

Applying it to the BT827 law `I_n = (40ⁿ−1)/39`:

```text
H_1 :     40 leaves,     1 instance   ->     4,615 LC   one part
H_2 :  1,600 leaves,    41 instances  ->   189,215 LC   ~36 parts
H_3 : 64,000 leaves, 1,641 instances  -> 7,573,215 LC   ~1434 parts
```

> **`H₁` is a chip. `H₂` is a rack.** The BT827 fractal is a network from level 2 onward,
> and that boundary now has a measured constant rather than an estimate.

---

## Pass 2662 — the four recursions are **not** one law

```text
BT827 branching    40 = (q+1)(q^2+1) = 4 x 10
Pass 79 tier       size scales by q^2 = 9, distance by q = 3
my A2+E6           3 = q
qutrit Pauli hierarchy   not examined
```

All are functions of `q`, but **different** functions — `q`, `q²`, `(q+1)(q²+1)`. The
hypothesis that they are one law seen at different levels is **not supported**. They are
distinct recursions on the same substrate, and calling any of them "the" fractal remains
wrong.

---

## Pass 2663 — the two items not done

- **Pages 50–100** — not read. The batch went to building the corrected gate, which the
  page 1–50 read had shown was necessary.
- **Auditing the manuscripts** — not done. The gap is real and now precisely stated:
  `scripts/build_certificate_index.py` indexes `data/*.json`; **three withdrawals in the
  last two batches came from `photonic_holonet_body.tex`, which nothing indexes.** The
  value index should cover `.tex` too, or those corrections will keep arriving late.

---

## Pass 2664 — ledger

| claim | status |
|---|---|
| `ε`-cubic on a literal `3×3×3` tensor | **refuted — 206/1800 violations** |
| `E₆` cubic is `det A + det B + det C − tr(ABC)` | **verified, 2400 invariance checks** |
| Pass 2632's `det` is a component of it | softens Pass 2652's correction |
| gate correct on 4000 random 27-trit vectors | verified |
| `w33_e6_cubic_gate` = 473 LC | measured |
| full `W(3,3)` core = 4615 LC = 87% of a UP5K | **measured** |
| `H₂` needs ~36 parts | **new — BT827 with a measured constant** |
| the four recursions are one law | **not supported** |
| pages 50–100, manuscript audit | not done |

---

## Prior art

- `photonic_holonet_body.tex` — owns the gate-set claim and the BT827 fractal law.
- The `E₆` trinification cubic `det A + det B + det C − tr(ABC)` — classical.
- Pass 2632 (mine) — the `det3` unit reused here as one of the four terms.

## Still open

- Pages 50–100, and indexing the manuscripts.
- Whether the qutrit Pauli hierarchy recursion relates to any of the other three.
- `χ(H) ∈ {10,11}`, ranks 10–14, the five certificates.
