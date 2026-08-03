## Passes 2796–2802 — four magic classes not three, and the minimal engine measured

---

## Pass 2797 — correction: the distillation search needs **four** representatives, not three

Pass 2790 established that the 36 Witting rays carry exactly three stabilizer fidelities,
`{9, 5+2√3, 4+2√3}/12` on `4/24/8` rays, and I wrote there that *"the distillation search
needs three representatives, not thirty-six."*

**That was one step too far.** Equal `F_stab` does not imply Clifford equivalence. Under
the full two-qubit Clifford group (`92160` matrices, `11520` classes × 8 phases), matching
images by **fidelity** rather than by a rounded hash key:

```text
Clifford equivalence classes on the 36 rays : 4, sizes [4, 8, 12, 12]
every class lies inside one grade           : True
CLASSES == GRADES                           : False

   F_stab = 0.750000000  ( 4 rays)  ->  1 class,  size [4]
   F_stab = 0.705341801  (24 rays)  ->  2 classes, sizes [12, 12]     <-- splits
   F_stab = 0.622008468  ( 8 rays)  ->  1 class,  size [8]
```

> **`F_stab` is a genuine invariant but not a complete one.** It is constant on classes —
> so the grading is real — but the 24-ray middle grade is **two** Clifford-inequivalent
> families of 12. Grade is necessary, not sufficient. The correct count is **four**.

### Independently corroborated from the other track, by a different method

The parallel track's Pass 2821 reports: *"Shallow and **both middle** M36 grades have zero
improving branches."* They found two middle grades by exhaustive distillation search over
`5355` projectors × 4 syndromes × `11520` decoders. I found them by Clifford orbits on the
rays. **Two completely different computations, same splitting.**

**Method note.** The first version of this matched images with a rounded hash key and
would have been fragile in precisely the dangerous direction: a single missed match
*splits* an orbit and manufactures a false inequivalence. Matching by
`|⟨r_j | g r_i⟩|² > 0.999` is safe because the only overlaps in this configuration are `0`
and `1/3` (Pass 2790) — the threshold has a gap of `2/3` to the nearest competing value.

---

## Pass 2798 — the two-copy no-go was never information-theoretic

`D_min(ρ) = −log₂ F_stab(ρ)` is a magic monotone (Bravyi–Browne–Calpin–Campbell–Gosset–
Howard 2019): **no** stabilizer operation can increase it, including measurement,
post-selection and feed-forward. So computing `F_stab` on two copies — over all `36,720`
four-qubit stabilizer states — bounds *every* two-copy protocol at once, not one code
family.

| grade | `F_stab(ψ)` | `F_stab(ψ⊗ψ)` | `F_stab(ψ)²` | `D_min(ψ)` | `D_min(ψ⊗ψ)` |
|---|---|---|---|---|---|
| shallow | 0.750000000 | 0.562500000 | 0.562500000 | 0.415037 | 0.830075 |
| mid | 0.705341801 | 0.497507057 | 0.497507057 | 0.503606 | 1.007211 |
| deep | 0.622008468 | 0.386894534 | 0.386894534 | 0.684994 | 1.369988 |

`F_stab` is **exactly multiplicative** on two copies for every grade, so
`D_min(ψ⊗ψ) = 2 D_min(ψ) > D_min(ψ)`.

> **The monotone never obstructs.** Two copies always carry more than enough magic to
> make one, for every grade. **Any two-copy no-go in this system is therefore structural,
> not information-theoretic** — a statement about the protocol family searched, and the
> right response is to widen the family.

### And that is exactly what happened

The parallel track's Pass 2821 widened the search from an arbitrary decoder to **all
11,520 logical Clifford decoders** and found **48 improving branches** on the deep grade,
with an explicit protocol improving fidelity for `0 < p < 2/3` — superseding their own
earlier no-go. The monotone analysis says why that had to be possible: nothing in the
resource accounting was ever in the way.

---

## Pass 2796 — the minimal engine, measured (the evidence Pass 2820 refused to assume)

Pass 2820 said the right thing about my Pass 2789 minimality proof:

> *"The measured `72 LC / 60.80 MHz` result belongs to the loadable public full-frame
> unit. It is not silently reassigned to the four-operation minimal engine; that engine
> requires its own synthesis and place-and-route evidence."*

Correct — a group-theoretic minimality proof says nothing about area, and removing decode
cases can even *cost* cells if what was removed was being shared. Here is the evidence.
`rtl/w33_pass2796_minimal_frame_engine.sv`, two-bit opcode, four operations
`{F_p, CX_{p→f}, CX_{f→p}, Z_p}`, loadable, measured in the same harness as the public
unit:

| design | LC | pins | `F_max` |
|---|---:|---:|---:|
| minimal, 4 ops, 2-bit opcode | **43** | 22 | **72.40 MHz** |
| public, 6 ops, 3-bit opcode | 72 | 26 | 60.80 MHz |

> **40 % fewer logic cells and 19 % faster.** The minimality theorem cashes out in
> silicon, and now it is measured rather than assumed.

Also checked, because both are cheap and both have bitten this project:

```text
SAT: 4100 variables, 11278 clauses ... SUCCESS
     the linear part is symplectic on frame DIFFERENCES, all four opcodes at once
fold audit: outputs tied to a constant after `flatten; opt -full` = 0
```

The difference formulation is the neat part: a translation cancels in a difference, so
one assertion covers the three linear opcodes *and* the affine one — which is the same
reason a single translation makes the frame space reachable without breaking the form
(Passes 2774, 2778).

Every one of the four encodings is legal, so the engine has **no illegal-opcode trap** —
the same completeness property the Kraft-equality routing code has one level up.

---

## Pass 2799 — the phase group is `μ₁₂` for every `n`, with a proof

Pass 2791 had `μ₁₂` at `n = 1` by exact enumeration and sampled it at `n = 2`. The general
statement is four lines:

1. Every generator entry lies in `ℚ(ζ₁₂)`: `S` gives `ω = ζ₁₂⁴`, `X` and `CX` give `0, 1`,
   and `F₃` gives `ω^{jk}/√3` — where the only non-obvious step is `1/√3 ∈ ℚ(ζ₁₂)`.
2. `ℚ(ζ₁₂)` is a field and tensoring multiplies entries, so **every** element of the
   `n`-qutrit Clifford group has entries in it, for every `n`.
3. A scalar `λI` in a finite matrix group has `λ` a root of unity, lying in `ℚ(ζ₁₂)`.
4. For even `m` the roots of unity in `ℚ(ζ_m)` are exactly `μ_m`, and `12` is even.

Step 1's non-obvious part, checked as explicit identities:

```text
zeta_12 + conj(zeta_12) = sqrt3           residual 2.22e-16
zeta_12^4 = omega                          residual 2.48e-16
zeta_12^3 = i                              residual 2.78e-16
1/sqrt3 = (zeta_12 + conj(zeta_12))/3      residual 1.11e-16
```

> **The phase group is `μ₁₂` for every `n`, so the minimal sensor exponent is the least
> `e ≡ 3ⁿ (mod 12)` — `3` for odd `n`, `9` for even.** No longer a pattern; a theorem.

An earlier version of this check used a least-squares fit against `{1, ζ, ζ², ζ³}`, which
is underdetermined over `ℝ²` and reported `False` even for the permutation matrix `X`. A
direct identity has no such failure mode. Recorded because a *check* that fails on a
trivially true case is worse than no check.

---

## Pass 2800 — ledger

| claim | status |
|---|---|
| 4 Clifford classes on the 36 rays, sizes `[4,8,12,12]` | **proved**, fidelity matching |
| the 24-ray mid grade splits into `12+12` | proved; corroborated by Pass 2821 |
| Pass 2790's "three representatives" | **corrected to four** |
| `F_stab` constant on classes (necessary, not sufficient) | proved |
| `F_stab` exactly multiplicative on two copies | measured, all three grades |
| the monotone never forbids two-copy distillation | **proved** — no-go was structural |
| minimal engine: **43 LC, 72.40 MHz** | **measured** |
| public unit: 72 LC, 60.80 MHz | measured (Pass 2777) |
| minimal engine symplectic on differences | **SAT**, 4100 vars / 11278 clauses |
| minimal engine does not fold | fold audit clean |
| phase group `= μ₁₂` for all `n` | **proved** |
| earlier `ℚ(ζ₁₂)` least-squares check | **broken** — replaced by identities |

---

## Prior art

- **Parallel track Pass 2821** — **owns** the deep-grade distillation result: 48 improving
  branches, explicit protocol with `P_succ = (p²−2p+2)/4` improving on `0 < p < 2/3`, and
  the "both middle grades" observation this pass corroborates independently.
- **Parallel track Pass 2820** — **owns** the correct refusal to reassign the 72 LC figure;
  this pass supplies the measurement it asked for.
- **Parallel track Pass 2822** — **owns** the support-refinement chain `16 → 40 → 78 → 81`
  and the *support for readout, phase for execution* theorem.
- Bravyi et al. (2019) — the stabilizer-fidelity magic monotone.

## Still open

- Whether the two 12-ray middle classes differ by any *operationally* meaningful quantity,
  or only by Clifford class.
- Fault-tolerant injection threshold and asymptotic yield — the deep-grade result is a
  state-fidelity theorem, not either of those.
- Physical power in watts.
