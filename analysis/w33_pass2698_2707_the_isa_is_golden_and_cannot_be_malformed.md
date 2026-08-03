## Passes 2698–2707 — the ISA is golden, cannot be malformed, and my controller is on the wrong side

---

## Pass 2698 — **the ISA's braid instruction is defined over the golden field**

The paper's §"Exact braid words": in the anyonic Fibonacci representation
`σ₁ = diag(ζ⁴, −ζ²)` with `ζ = e^{iπ/5}`, one has *exactly* `σ₁⁵ = Z` and `σ₁¹⁰ = I`,
verified in `ℤ[ζ₁₀]`. Confirmed symbolically:

```text
sigma^5  = diag(1, -1) = Z     exact
sigma^10 = diag(1,  1) = I     exact
```

Now the field. `ℚ(ζ₁₀) = ℚ(ζ₅)`, and

```text
2 cos(pi/5) = (1 + sqrt5)/2 = phi        exact
```

> **`φ` is an algebraic integer in `ℤ[ζ₁₀]` — the very ring the paper says the braid is
> exact in.** The ISA's braid instruction is written over the golden field, and `φ` is
> the Fibonacci anyon's quantum dimension.

This is the **fourth** `φ` in the project, and it is the only one that is not a
coincidence to reject:

| # | where | status |
|---|---|---|
| 1 | `ℚ(ζ₁₀)` of the `σ⁵ = Z` instruction | **canonical — the anyon model's defining constant** |
| 2 | icosian golden quaternions in `E₈` | manuscripts, established |
| 3 | the Golden `D₄`/Weyl shell | manuscripts, established |
| 4 | spectral radius of `R₄²U₆` in `SL₃(ℤ)` | mine, Pass 2439, unrelated to the others |

Passes 2083 and 2439 spent a lot of effort asking where `φ` comes from and concluding it
was absent from the finite geometry. **It was in the instruction set the whole time**, for
the most ordinary reason: the machine's braid gate is a Fibonacci anyon gate, and
Fibonacci anyons have quantum dimension `φ` by definition.

---

## Pass 2700 — the instruction, built and proved

`rtl/w33_pass2700_braid_instruction.sv` — a `σ`-counter mod 10 emitting a `Z` on the
addressed bit every fifth application.

```text
SAT: 199 variables, 534 clauses ... SUCCESS
     sigma^5 flips exactly the target bit;  sigma^10 restores the register

ICESTORM_LC 21/5280    SB_IO 14/96    98.42 MHz
```

> **The first of the eight `I_holo` instructions to exist as hardware.** 21 logic cells —
> a counter and one XOR, because the exactness lives in the algebra, not the circuit.

---

## Pass 2701 — **a complete prefix code means the machine has no illegal opcodes**

The Kraft equality of Pass 2682 holds *exactly*, so the code tree has no unused branch.
The consequence nobody has stated:

```text
20,000 RANDOM bit strings decoded through the router:
    failed to parse      : 0
    truncated final word : 8570   (framing, never an invalid opcode)
    instructions emitted : 232,491
```

> **The instruction stream cannot be malformed.** Noise on the wire decodes to a valid —
> if wrong — program. For a machine whose thesis is that *routing is computation*, a
> corrupted packet is still a legal computation.

The engineering consequence is sharp: **the error model has no decode-error term, only a
wrong-result term.** There is nothing to trap, no illegal-instruction exception, and no
parser to harden. Every fault is semantic, never syntactic.

That is a direct consequence of Kraft holding with equality rather than `≤ 1`, which the
paper obtains from *group orbit sizes* rather than from traffic statistics. A Huffman code
fitted to measured probabilities would generally give `< 1` and therefore illegal words.

---

## Pass 2702 — my phase controller is on the **wrong side** of the 2160 split

The paper: the cyclic `C₁₂` side is the selector's phase **clock**; the dihedral `D₁₂`
side is the mirror **transport bus**; *"equal cardinality is the red herring; different
stabilizer structure is the theorem."*

My `μ₄`/`μ₆` controller, checked:

```text
R4^4 = I : true     U6^6 = I : true
COMMUTE  : FALSE    commutator order 4
```

> **Non-abelian, so it belongs on the dihedral / transport side. But Pass 2457 built it
> as a phase accumulator — cyclic clock behaviour.**

The circuit is internally consistent and its SAT proofs stand; what is wrong is the
architectural role I assigned it. A `D₁₂` object driving an accumulator is a mirror bus
being used as a clock. **Pass 2457's identification is withdrawn**; the RTL remains valid
as a period-2-plus-Fibonacci datapath, which is what its proofs actually establish.

---

## Pass 2703 — what `χ(H)` is for: **not the routing fabric**

Pass 2692 established the paper's chart web is 6-regular on the 540 charts while the frame
graph `H` is 32-regular on the same set. So the chromatic question is not about routing.

What it *is* about: `χ(H) = 9` is equivalent to the 540 frames partitioning into 9 exact
covers, i.e. to a **resolution** of the 240-edge design. That is a statement about
scheduling all 240 edge-constraints in 9 conflict-free rounds — a **timetabling** result,
not a routing one.

> **`χ(H)` is the minimum number of parallel rounds in which every edge constraint can be
> serviced exactly once.** The parallel track's `10 ≤ χ(H) ≤ 11` therefore says the
> machine needs at least ten rounds, not nine.

Stated because three batches of chromatic work never named what the number means for the
machine, and "it isn't the routing bound" is only half an answer.

---

## Pass 2704 — the two not built

- **Transceiver RTL** — maths verified at Pass 2684; scaling by 10 makes it integer.
- **Data-plane RTL** — `SRG(40,12,2,4)` still nothing.

---

## Pass 2705 — ledger

| claim | status |
|---|---|
| `σ⁵ = Z`, `σ¹⁰ = I` exact | **verified symbolically and by SAT** |
| `φ = 2cos(π/5) ∈ ℤ[ζ₁₀]` | **proved — the ISA is over the golden field** |
| this is the canonical `φ` of the four | argued, not a count match |
| braid instruction placed, 21 LC, 98.42 MHz | measured |
| the instruction stream can be malformed | **refuted — 0/20,000** |
| error model has a decode-error term | **no — only wrong-result** |
| `μ₄/μ₆` controller is the `C₁₂` clock | **withdrawn — it is non-abelian** |
| `χ(H)` is a routing quantity | **no — it is a timetabling round count** |

---

## Prior art

- `photonic_holonet_body.tex` §"Exact braid words", §"The middleware", §"The parabolic
  router" — own the braid identity, the two 2160 worlds, and the Kraft orbits.
- Fibonacci anyons having quantum dimension `φ` — classical.

## Still open

- Transceiver and data-plane RTL; six more ISA instructions.
- Whether the four `φ`s connect, now that one of them is canonical.
- Lines 1220–2400 and the physics half.
