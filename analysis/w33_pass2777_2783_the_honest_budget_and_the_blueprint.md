## Passes 2777–2783 — the honest budget, the group, the exponent, and a blueprint

---

## Pass 2778 — the eight opcodes generate `ASp(4,3)` exactly, and one of them is redundant

Pass 2774 showed the frame space is *reachable*. Reachability is much weaker than
*expressible*, so the real question is what group the ISA generates.

```text
linear part from the six Clifford opcodes : 51840   = |Sp(4,3)|, nothing missing
translations from Z_p ALONE               : 81 of 81
translations from Z_p and Z_f             : 81 of 81
affine group, one translation             : 4199040
|ASp(4,3)| = 81 * 51840                   : 4199040
orbit of one nonzero vector               : 80
```

> **The eight opcodes generate the full affine symplectic group `ASp(4,3) = F₃⁴ ⋊
> Sp(4,3)`, order `4,199,040`, exactly.**
>
> **And one translation generator suffices.** `Sp(4,3)` is transitive on the 80 nonzero
> frame vectors, so the orbit of a single translation already spans `F₃⁴`. The second
> `Z` register-select is provably redundant and can be removed from the ISA.

---

## Pass 2779 — why the sensor exponent is 9, and it is minimal

The parallel track's Pass 2768 sensor is `Θ_k(g) = Tr(U_g^k)⁹ / det(U_g^k)`, with the
ninth power stated as a fact. It has a reason, and the reason bounds how cheap the sensor
can be.

Under `U → λU` on a `d`-dimensional representation, `Tr(U^k)^e → λ^{ke} Tr(U^k)^e` and
`det(U^k) → λ^{kd} det(U^k)`, so the quotient is invariant for **all** `λ` exactly when
`e = d`. Here `d = 9` — the two-qutrit state space, which is `dim End(ℂ³)`. Verified:
`e ∈ {3, 8, 10}` fail, `e = 9` holds.

If the phase ambiguity were a finite `μ_m`, any `e ≡ 9 (mod m)` would do, possibly
smaller. So the scalar subgroup of the generated matrix group had to be computed:

```text
scalar subgroup: order 12   (the 12th roots of unity)
quadratic Gauss sum  sum_j omega^(j^2) = 1.732051i     -- IMAGINARY
det(F_3)                                = -i,  order 4
order of omega                          = 3
lcm(4,3) -> mu_12
```

> **`μ₁₂ = μ₄ × μ₃`. The `μ₃` is `ω`, the qutrit alphabet. The `μ₄` is the quadratic
> Gauss sum `Σ_j ω^{j²} = i√3` — imaginary precisely because `3 ≡ 3 (mod 4)`, the same
> congruence that makes time reversal outer (Pass 2750).**

Since `9 ≢ 0 (mod 12)` the determinant is genuinely required, and `9` is the **smallest**
exponent that works. **Their sensor is minimal, not over-engineered** — confirmed, with a
derivation they did not give.

---

## Pass 2777 — the honest cell budget

Every ISA cell count before Pass 2753 was measured on a module with no load port. Pass
2774 says why that is fatal: Clifford opcodes are symplectic, symplectic maps are linear,
linear maps fix the origin, so the register is provably constant and synthesis deletes
it.

`rtl/w33_pass2777_isa_frame_unit.sv` — loadable, all six frame opcodes, parameterised by
an enable mask so each instruction is measured in one harness:

| build | LC | Fmax | old (folded) figure |
|---|---:|---:|---|
| `F` only | 16 | 230.84 | — |
| `F_p + F_f` | 19 | 230.84 | — |
| `F` and `S`, 4 opcodes | 40 | 86.60 | **13** |
| `CX` only | 33 | 72.40 | **8** |
| `σ⁵ = Z` only | **20** | 144.07 | **21** |
| all Clifford, no `Z` | 65 | 60.80 | — |
| **full frame unit** | **72** | **60.80** | **42 claimed for 4 of 8** |

> **The theory predicted exactly which number would survive.** `σ⁵ = Z` re-measures at 20
> against an old 21 — essentially unchanged — because it is the one opcode that is a
> *translation* and so the one that could always move the state. Every linear opcode's
> figure roughly tripled.

---

## Pass 2780 — synthesis in RTL CI

`.github/workflows/w33_rtl_synthesis_gate.yml`. Three stages: **parse** with both
frontends (fails the job — a file no frontend accepts is not RTL), **fold audit** (warns),
**place and route** with the budget uploaded as an artifact.

Every RTL job in this repo previously ran `iverilog` and stopped. That is the step that
cannot see the Pass 2753 defect at all: a module that folds to a constant still simulates
correctly.

---

## Pass 2781 — the implicit-novelty guard, and four measured calibration failures

`scripts/check_implicit_novelty.py`. The signature of implicit novelty is not a phrase,
it is **a position plus an absence**: a distinctive token in an emphasized span
(heading, bold, blockquote) that the encyclopedia carries, in a file that never cites
*that* source.

The calibration is the work, and every step was a real mistake:

| flagged | step | what the noise was |
|---:|---|---|
| 9/122 | presence of any token | **all nine were pass numbers in titles** |
| 0/122 | + skip files saying "Prior art" | **vacuous** — every pass file has that section |
| 51/122 | + cite the *right* source per token | `W(3,3)` 21×: the repo's own subject |
| 27/122 | + rarity ≤ 12 and non-round integers | what ships |

> **The second row is the one worth remembering: a guard that passes everything looks
> exactly like a guard that finds nothing wrong.** It cleared all 122 files including the
> known Pass 2735 failure. Only a deliberate self-test against that specific failure
> exposed it.

Self-test now passes: it flags `PGSp(4,3)` emphasized in
`w33_pass2732_2741_...md` against `index.html` (10 occurrences — rare enough to be a
result), uncited.

---

## Pass 2782 — the blueprint

`holonet_machine_blueprint.tex` → `holonet_machine_blueprint.pdf`, 13 sections, 16 TikZ
figures, compiled clean with **zero overfull boxes**.

Written to be read two ways at once: cream boxes explain every idea from scratch with no
assumed background, blue boxes carry the specification, and a third box type — there are
eleven — records what this project believed, published, and withdrew, with the
measurement that overturned it.

It contains the full ISA semantics, the datapath diagram, the measured cell budget, the
reachability theorem, the `ASp(4,3)` order, the exponent-9 derivation, the fractal network
and Kraft tree, the photonic layer with its evidence boundary, the five guards, a complete
claim ledger with status for every assertion, and a reproduction command for each figure.

Engine: `C:\Users\wiljd\tools\tectonic\tectonic.exe` — **not** the `%LOCALAPPDATA%\Temp`
path recorded in older notes.

---

## Pass 2783 — ledger

| claim | status |
|---|---|
| Clifford opcodes generate `Sp(4,3)`, order 51840 | **proved** |
| full ISA generates `ASp(4,3)`, order 4199040 | **proved** |
| one translation generator suffices; orbit 80 | **proved** — second `Z` is redundant |
| sensor exponent `e = d = 9` | **derived** |
| phase group is `μ₁₂ = μ₄ × μ₃` | **computed** (collision sampling) |
| `μ₄` is the imaginary Gauss sum | **computed**, `det(F₃) = −i` |
| 9 is the minimal exponent | **proved** — the sensor is minimal |
| full frame unit: 72 LC, 60.80 MHz | **measured** |
| `σ⁵ = Z`: 20 LC (was 21) | measured — the predicted survivor |
| synthesis wired into CI | done |
| implicit-novelty guard | built, self-tests, 27/122 |
| blueprint PDF | compiled clean |
| a first enumeration gave "799690" | **meaningless** — a truncation point, recorded so it is not mistaken for a group order |

---

## Prior art

- `analysis/BT2767_BT2771_five_frontiers.md` — **owns** the `Θ_k` sensor and the 34-class
  census; this pass derives its exponent and confirms minimality.
- `rtl/w33_pass2762_holonet_isa.sv` — **owns** the eight-opcode contract transcribed here.
- `docs/index.html` Pillars 128–130 — the Master Dictionary.
- Imany et al., *npj QI* **5**, 59 (2019) — the measured photonic qutrit `SUM`.

## Still open

- `M₃₆` magic-state injection threshold — refused in RTL until a proved protocol exists.
- End-to-end fault-tolerance threshold; physical power in watts.
- The transpose construction at `q > 3`.
- `rtl/w33_spread_mixer36.sv` (the unparseable original) should be retired.
