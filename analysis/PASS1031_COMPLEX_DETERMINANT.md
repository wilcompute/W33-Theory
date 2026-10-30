# Pass 1031 — the complex determinant detects the phase and is blind to the sign

**Certificate:** `analysis/w33_pass1031_complex_determinant_phase_detector.g` →
`data/w33_pass1031_complex_determinant_phase_detector.json` (10/10, deterministic)

---

## The result

Pass 1023 split the section obstruction into a 2-primary (sign) and a 3-primary
(phase) half. Passes 1028 and 1030 raised firewalls against merging either with
corpus objects. None of them supplied an *invariant* separating the halves. This does.

| character | domain | image | detects sign | detects phase |
|---|---|---|---|---|
| `det_ℝ` | the ω-normaliser, order 311040 | trivial | no | no |
| `det_ℂ` | the centraliser `C = ℤ₃ × Sp(4,3)` | `μ₃` | no | **yes** |

`Sp(4,3)` is perfect, so `det_ℂ` kills it; `C^ab = ℤ₃`, so `det_ℂ` is onto `μ₃`
with kernel **exactly** `Sp(4,3)`; and `det_ℂ(−I₄) = (−1)⁴ = +1` puts the antipodal
map inside that kernel. Verified: `ω` lies outside the kernel and generates the
image; the antipodal map lies inside and has trivial image.

Sharpest form: `⟨c⁵⟩ ∩ ker(det_ℂ)` has order 2 and contains the antipodal map, so

> **`det_ℂ` restricted to the ℤ₆ fibre is precisely the projection `ℤ₆ → ℤ₃`.**

The phase half *is* a determinant. The sign half is not a determinant of anything.

## Why the group-theoretic computation is `det_ℂ`, not an analogy

`det_ℂ` is a homomorphism from a finite group to `ℂ*`, so it kills every commutator
and factors through `C^ab`. Here `C^ab = ℤ₃` and `det_ℂ` is onto `μ₃`, so `det_ℂ`
**is** the abelianisation map up to an isomorphism of `ℤ₃`, and
`ker(det_ℂ) = [C,C] = Sp(4,3)`. Membership is then decidable purely
group-theoretically, which is what the certificate computes.

## What this can and cannot test — read before applying it

This section exists because the obvious next move is a type error, and the same
type error has already cost this corpus real work twice (`Sp(4,3) ≅ W(E6)`, and a
proposed identification of the ℤ₆ fibre with the Standard Model's ℤ₆ quotient).

**It CAN test:** whether an element or subgroup **of `C`** lies in `ker(det_ℂ)`.
That is a decidable membership question with a one-line answer.

**It CANNOT test:** whether a corpus "phase-sheet" or "golden-selector" object is
the 3-primary class. Those objects are not subgroups of `C`. They are actions on
W(3,3) structures — quadrangles, sheets, cochains — living on the *base*, whereas
`det_ℂ` is a character of the *total-space* symmetry group. Feeding one to the
other compares a subgroup to a groupoid action and produces a sentence that reads
like a theorem and is not one.

**`det_ℂ(J)` is also not the section criterion.** `ker(det_ℂ) = Sp(4,3)` is the
whole total-space group, and Pass 1023 shows `Sp(4,3)` does **not** admit a phase
section. So `det_ℂ(J) = 1` does not imply `J` is phase-clean. The two invariants
answer different questions: `det_ℂ` says *which class is a determinant*, the Pass
1023 criterion says *which subgroups can section it*.

**What would make the comparison legitimate:** an explicit homomorphism from the
selector's symmetry group into `C` that transports the point/line block system —
exactly the transport Pass 1030's firewall says any genuine bridge must construct.
Until such a map is named, the right statement is that the comparison is not yet
type-correct, and no amount of matching integers changes that.

## Scope

Separation invariant only. It identifies neither primary class with any named
corpus obstruction, and says nothing about conjugate-linear elements, on which
`det_ℂ` is not a homomorphism to `μ₃`.

## Prior art — cited, not reclaimed

Pass 1029 (`det_ℝ` trivial on the normaliser, and the antipodal map's real
determinant), Pass 1023 (the primary split and the subgroup criterion), Pass
1021/1020 (`C = ℤ₃ × Sp(4,3)`, `K = C'`, the fibration), Passes 1028 and 1030 on
the other track (the syndrome decoder and the carrier firewalls — this supplies
the invariant those firewalls were separating the halves without).
