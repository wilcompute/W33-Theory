## Passes 2708–2715 — three of eight instructions, and all four `φ`s are one field

---

## Pass 2708 — `F` and `S`, built and proved

What hardware tracks for a Clifford gate is not the state but the **Pauli frame**: a
two-trit label `(a,b)` meaning `XᵃZᵇ`. Clifford gates act on it by symplectic matrices
over `𝔽₃`, and the two the paper names generate everything:

```text
F  (tritter / qutrit Fourier)  : (a,b) -> ( -b,  a )    order 4
S  (quadratic phase plate)     : (a,b) -> (  a, a+b )   order 3

|<F,S>| = 24,  all determinants 1   =   SL(2,3)
                                    =   single-qutrit Clifford mod Pauli
```

The closure was checked before the circuit was trusted. Then:

```text
SAT: 437 variables, 1177 clauses ... SUCCESS      F^4 = I  and  S^3 = I
ICESTORM_LC 13/5280    SB_IO 8/96    89.15 MHz
```

> **Three of the eight `I_holo` instructions now exist as hardware** — `F`, `S`, and
> `σ⁵ = Z` — for a combined **34 logic cells**.

That the whole Clifford frame tracker is 13 cells is the paper's own point made concrete:
*"The Clifford part normalizes Pauli frames and is efficiently classically trackable; it
is not universal by itself."* The expensive part is the `E₆` cubic (473 cells, Pass 2660)
and the magic injection, neither of which is a frame update.

**ISA status:**

| instruction | built | cells |
|---|---|---|
| `F_p`, `F_f`, `S_p`, `S_f` | **yes** | 13 |
| `σ⁵ = Z` | **yes** | 21 |
| `CX_{p→f}` | no | — |
| `D₁₂`-mirror | no | — |
| `M₃₆`-magic | no | — |

---

## Pass 2710 — all four `φ`s are **one field**, and my dichotomy was half wrong

```text
Z[zeta_10] anyon braid   ->  Q(zeta_10)^+ = Q(sqrt5)
icosian quaternions      ->  Q(sqrt5)
Golden D4 / Weyl shell   ->  Q(sqrt5)
SL3(Z) growth rate       ->  Q(sqrt5)      (Pass 2440)
```

And the number itself sits on both sides of the distinction I drew:

```text
phi = 2 cos(pi/5)          a real CYCLOTOMIC integer in Z[zeta_10]
phi * (phi - 1) = 1        and a UNIT
```

> **Pass 2571 separated `φ`-appearances into "roots of unity" versus "units". For `φ` that
> separation does not exist** — it is simultaneously a real cyclotomic integer and a unit,
> and all four appearances live in the same field `ℚ(√5)`.

**What survives** is the element statement, not the field statement: the anyon braid `σ`
has **finite order 10**; the `SL₃(ℤ)` word has **infinite order**. Same algebraic number,
same field, different group-theoretic role. **Pass 2571 stands as a statement about
elements and fails as a statement about fields**, and I wrote it as the latter.

So the honest position on `φ` after this session: it appears four times, in one field,
canonically as the Fibonacci anyon's quantum dimension in the ISA (Pass 2698), and the
`SL₃(ℤ)` appearance remains the odd one out only because its element is hyperbolic — not
because its arithmetic differs.

---

## Pass 2712 — the three not done

- **Re-homing the `μ₄/μ₆` circuit** — Pass 2702 established it is a `D₁₂`-side object
  built with `C₁₂` clock semantics. Not corrected; it needs either transport-bus drive
  logic or a rename, and neither was written.
- **Transceiver RTL** — maths verified at Pass 2684, still unbuilt.
- **Lines 1220–2400** — unread. Every prior block cost a claim; this is the largest
  remaining unexamined region before the physics half.

---

## Pass 2713 — ledger

| claim | status |
|---|---|
| `⟨F,S⟩ = SL(2,3)`, order 24, all det 1 | **verified** |
| `F⁴ = I`, `S³ = I` in the netlist | **SAT-proved** |
| frame tracker is 13 cells at 89.15 MHz | measured |
| three of eight ISA instructions exist | 34 cells total |
| all four `φ`s share `ℚ(√5)` | **proved** |
| `φ` is a cyclotomic integer **and** a unit | **proved** |
| Pass 2571's dichotomy as a field statement | **withdrawn** |
| Pass 2571's dichotomy as an element statement | stands |
| `μ₄/μ₆` re-homed | no |
| transceiver, reading | no |

---

## Prior art

- `photonic_holonet_body.tex` §"Instruction set architecture" — owns `I_holo`.
- Fibonacci anyon quantum dimension `= φ` — classical.
- Pass 2440 (mine) — the `ℚ(√5)` identification for the `SL₃(ℤ)` words.

## Still open

- Five ISA instructions; `CX_{p→f}` is the natural next and the first two-register one.
- Transceiver and data-plane RTL.
- The `μ₄/μ₆` circuit's correct architectural home.
- Lines 1220–2400 and the physics half.
