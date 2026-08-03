## Passes 2789–2795 — three magic grades, a two-bit ISA, and the transpose closed

---

## Pass 2790 — the 36 magic rays are mutually identical, and the grading is external

The parallel track's Pass 2784 (PR #206) proves an exact **two-copy no-go**: over all
`5355` binary `[[4,2]]` stabilizer codes × 4 syndromes, no branch that closes back onto
the `M₃₆` orbit improves fidelity anywhere in its witness interval. Their next step is to
search three-copy, catalytic and non-identical schemes.

That search is enormous, and its size is set by **how many inequivalent magic states
there are**. So before searching harder, ask the cheaper question.

### The rays cannot tell each other apart

Exact integer arithmetic in `ℤ[ω]`, no floating point. Only **two** overlap values occur:

```text
9|<i|j>|^2 = 0   ->  |<i|j>|^2 = 0     396 ordered pairs
9|<i|j>|^2 = 3   ->  |<i|j>|^2 = 1/3   864 ordered pairs

distinct Gram profiles: 1
  all 36 rays: 11 orthogonal partners, 24 partners at overlap 1/3
```

> **Every one of the 36 rays has the identical Gram profile.** The configuration is
> internally homogeneous — no unitary symmetry can distinguish the rays by how they sit
> relative to *each other*. So the `8+24+4` grading, if real, must be **external**:
> visible only relative to the stabilizer polytope, invisible from inside `M₃₆`.

(The orthogonality graph is 11-regular on 36 vertices but **not** strongly regular —
`λ ∈ {1,2}`, `μ ∈ {3,4}`. Recorded because the near-miss is the sort of thing that
invites a wrong claim.)

### And it is real: the grading is exactly the stabilizer-fidelity spectrum

Generating all `60` two-qubit stabilizer states and taking
`F_stab(ψ) = max_s |⟨s|ψ⟩|²`:

| `F_stab` | closed form | rays | grade |
|---:|---|---:|---|
| `0.750000` | `9/12` | **4** | shallow |
| `0.705342` | `(5 + 2√3)/12` | **24** | mid |
| `0.622008` | `(4 + 2√3)/12` | **8** | deep |

> **`8 + 24 + 4` is the stabilizer-fidelity spectrum.** Stabilizer fidelity is a Clifford
> invariant, so the grading is genuine, not a basis artifact — an independent
> confirmation of the parallel track's census by a completely different route.

### The three quoted thresholds are one formula

For `ρ_p = (1−p)|m⟩⟨m| + p·I/4` the target overlap is `1 − 3p/4`, so the witness
certifies non-stabilizerness exactly while `1 − 3p/4 > F_stab`:

```text
                      p  <  4 (1 - F_stab) / 3

shallow:  derived 0.333333333333   quoted 1/3            equal
mid    :  derived 0.392877598318   quoted (7-2sqrt3)/9   equal
deep   :  derived 0.503988709429   quoted (8-2sqrt3)/9   equal
```

> **All three of Pass 2767's separately-stated thresholds are one formula evaluated at
> the three stabilizer fidelities.** Agreement to `1e-12`.

**Consequence for the open search:** a Clifford-invariant protocol cannot distinguish
rays within a grade, so **the distillation search needs three representatives, not
thirty-six** — a 12× reduction of the parallel track's next-step space, and the three
representatives are exactly the three fidelity levels.

---

## Pass 2789 — the frame ISA fits in **two** opcode bits

Pass 2778 showed one translation opcode is redundant. The sharper question is the
smallest generating subset. Because `F₃⁴ ⋊ H = ASp(4,3)` iff `H = Sp(4,3)` and at least
one translation is present, the search reduces to the six linear opcodes:

```text
subsets of size 1 generating Sp(4,3): 0
subsets of size 2 generating Sp(4,3): 0
subsets of size 3 generating Sp(4,3): 6
    F_p + F_f + CX_pf        F_p + F_f + CX_fp
    F_p + S_f + CX_pf        F_p + CX_pf + CX_fp
    F_f + S_p + CX_fp        F_f + CX_pf + CX_fp
```

> **Three Clifford opcodes plus one translation generate everything.** Four frame
> instructions — a **2-bit opcode field** instead of 3. `S_p`, `S_f`, one `CX`
> direction, and the second `Z` register-select are all convenience, not necessity.

Six different minimal triples exist, so there is real freedom to pick the cheapest in
silicon. Every triple contains at least one `F` and at least one `CX`: **no set of
phase gates and one Fourier gate suffices** — the entangler is irreplaceable.

---

## Pass 2791 — odd register widths need a **cube**, not a ninth power

Pass 2779 found the two-qutrit sensor exponent is `9 = dim`, phase group `μ₁₂`. For `n`
qutrits `d = 3ⁿ`, so the minimal exponent is the least `e ≡ 3ⁿ (mod 12)`.

The `n = 1` group is small enough to settle by **exact enumeration** rather than
sampling:

```text
|<F, S, X>| on one qutrit, enumerated : 2592
scalar subgroup                       : mu_12
mu_12 * |ASp(2,3)| = 12 * 216         = 2592   consistent
```

So `μ₁₂` is not an artifact of the two-qutrit case. And `3ⁿ mod 12` cycles `3, 9, 3, 9`:

| `n` | `d = 3ⁿ` | minimal `e` |
|---:|---:|---:|
| 1 | 3 | **3** |
| 2 | 9 | 9 |
| 3 | 27 | **3** |
| 4 | 81 | 9 |

> **For odd `n` the sensor needs only `Tr(U^k)³/det(U^k)`, not a ninth power.** Verified
> directly on `3×3` unitaries: `e = 3` is invariant, `e ∈ {2,4,9}` are not. The parallel
> track's Pass 2785 budgets `118,316` events for the `n = 2` sensor; the odd-width
> variants are a strictly cheaper measurement.

---

## Pass 2792 — the transpose, built and checked at eight primes

Pass 2750's scope caveat is closed. The involution
`T : (x_p, z_p, x_f, z_f) ↦ (x_f, −z_f, x_p, −z_p)` built over `F_q`:

```text
   q   T^2 = I   T^T J T = -J   -1 square   q mod 4  time reversal is
   3      True           True       False         3  OUTER (physical)
   5      True           True        True         1  INNER (gauge)
   7      True           True       False         3  OUTER (physical)
  11      True           True       False         3  OUTER (physical)
  13      True           True        True         1  INNER (gauge)
  17      True           True        True         1  INNER (gauge)
  19      True           True       False         3  OUTER (physical)
  23      True           True       False         3  OUTER (physical)
```

The construction is valid at every `q` tested and the congruence law holds at every one.

---

## Pass 2793 — the unparseable mixer is deprecated in place

`rtl/w33_spread_mixer36.sv` now carries a deprecation banner naming its replacement, the
two frontend errors verbatim, and the measured reason the parallel build does not fit an
iCE40. The file bytes are kept as the historical record; nothing is deleted, because it
is another track's file and it compiles nowhere anyway.

---

## Pass 2794 — a namespace hazard in PR #206, flagged while it is still cheap to fix

PR #206 is honest about its own numbering — `data/PART_BT2784_BT2788_PROVISIONAL_ID_MAP.json`
documents the remap and says the canonical range is `2784–2788`. But the **filenames**
retain the provisional IDs:

```text
.github/workflows/w33_pass2777_2781_five_frontiers.yml
analysis/BT2777_BT2781_five_frontiers.md      analysis/bt2777_m36_stabilizer_code_census.py
analysis/bt2778_metaplectic_interferometer.py analysis/bt2779_structured_cx_compiler.py
data/PART_BT2777_M36_4_2_STABILIZER_CENSUS_summary.json   ... and four more
```

`2777–2783` are already on `master` as this track's passes (commit `368d6fb2f`, reserved
`e44cea6b9`…`9e113a5be`). After a merge, `grep 2777` returns **two unrelated packets**.

> Given that this repo's documented worst failure mode is rediscovery, and that its
> stated remedy is *search by result*, a namespace where one number means two things is
> a real hazard rather than a cosmetic one. **PR #206 has not merged, so renaming the
> files to `2784–2788` is still a rename rather than a history rewrite.**

Recorded as a suggestion, not a block — the mapping file means nothing is *hidden*.

---

## Pass 2795 — ledger

| claim | status |
|---|---|
| 36 rays have one Gram profile (11 orthogonal, 24 at 1/3) | **exact**, `ℤ[ω]` arithmetic |
| orthogonality graph is 11-regular but **not** strongly regular | exact |
| `8+24+4` is the stabilizer-fidelity spectrum | **computed**, 60 stabilizer states |
| `F_stab ∈ {9, 5+2√3, 4+2√3}/12` | closed form, exact on 4/24/8 rays |
| all three witness thresholds `= 4(1−F_stab)/3` | **derived**, agrees to 1e-12 |
| distillation search needs 3 representatives, not 36 | follows |
| minimal Clifford generating subset has size **3** | **proved**, sizes 1 and 2 give none |
| frame ISA fits a **2-bit** opcode field | follows |
| every minimal triple contains an `F` and a `CX` | observed over all six |
| `μ₁₂` at `n = 1` by exact enumeration (2592 = 12·216) | **proved** |
| minimal sensor exponent `= 3ⁿ mod 12`: 3 odd, 9 even | derived |
| transpose construction valid at `q ≤ 23` | **proved**, closes Pass 2750's caveat |
| first `n=1` enumeration gave `156327` | **failed run** — `complex64` rounding split equal matrices; not a group order |

---

## Prior art

- **PR #206 / Passes 2784–2788 (parallel track)** — **own** the `M₃₆` two-copy no-go, the
  physical interferometer, the structured 480-coset compiler, the certificate repair and
  the repeater model. Pass 2790 confirms their grading and thresholds independently and
  reduces their stated next-step search space; it does not duplicate the no-go.
- Parallel track Pass 2767 / BT822 — **own** the `8+24+4` census and the three quoted
  thresholds.
- `rtl/w33_pass2762_holonet_isa.sv` — owns the eight-opcode contract.

## Still open

- Whether a **three-copy or catalytic** protocol beats the two-copy no-go — now with
  three representatives instead of thirty-six.
- Whether the `μ₁₂` phase group is `n`-independent for all `n` (proved `n = 1`, sampled
  `n = 2`).
- Physical power in watts; end-to-end fault-tolerance threshold.
