# Pass 1023 — the section obstruction is two obstructions, and they are independent

**Certificate:** `analysis/w33_pass1023_chirality_and_phase_halves.g` →
`data/w33_pass1023_chirality_and_phase_halves.json` (11/11, deterministic, GAP 4.16.0)

---

## What Pass 1022 left on the table

The other track's Pass 1022 proved that `L ↠ C₆` is regular, so `240 → 40` admits
no `Sp(4,3)`-equivariant section, and gave an exact subgroup criterion with two
witnesses (`Z(G)` obstructed, Sylow-5 clean). Its stated Boundary: the obstruction
is *"not yet identified"* with anything.

Its structural handle is `C₆ = C₂ × C₃` — and Pass 1020's block sizes 2, 3, 6
supply **both** intermediate quotients, not just the one:

```text
240 --C₂--> 120 antipodal pairs     fibre ⟨−1⟩ = ⟨c¹⁵⟩   the SIGN
240 --C₃-->  80 Eisenstein triples  fibre ⟨ω⟩  = ⟨c¹⁰⟩   the PHASE
        both --> 40 points
```

## The theorem

> **Each half is separately and fully obstructed, a `C₆` section exists exactly
> when both halves admit one, and the two halves are independent.**

| half | tower | fibre | block stabiliser | monodromy | section |
|---|---|---|---|---|---|
| sign | `240 → 120` | `⟨−1⟩` | 432 | `C₂`, regular | **no** |
| phase | `240 → 80` | `⟨ω⟩` | 648 | `C₃`, regular | **no** |
| product | `240 → 40` | `⟨c⁵⟩` | 1296 | `C₆`, regular | **no** |

**Product law.** `full section ⟺ sign section ∧ phase section`, verified on every
subgroup tested — the eleven rows below, including all five maximal classes.

**Independence.** Both mixed types are realised, so neither half implies the other:

| subgroup | order | sign | phase | full |
|---|---|---|---|---|
| `Z(G) = C₂` | 2 | ✗ | **✓** | ✗ |
| Sylow 3 | 81 | **✓** | ✗ | ✗ |
| Sylow 2 | 128 | ✗ | **✓** | ✗ |
| Sylow 5 | 5 | ✓ | ✓ | **✓** |
| root stabiliser `H` | 216 | ✗ | ✗ | ✗ |
| `Sp(4,3)` | 51840 | ✗ | ✗ | ✗ |
| maximals (5 classes) | 1920, 1440, 1296, 1296, 1152 | ✗ | ✗ | ✗ |

`Z(G)` is **phase-clean and chirality-obstructed**; the Sylow 3-subgroup is
**chirality-clean and phase-obstructed**. They are opposite corners of a genuine
2×2, not two samples of one phenomenon.

Pass 1022's two witnesses turn out to be clean and dirty *for different reasons*:
Sylow-5 is clean because 5 ∤ 6 — it misses **both** halves — whereas `Z(G)` fails
in the 2-part only. A single `C₆` statement cannot see that difference.

## Why this matters for the corpus

The repo has, under many names, reported obstructions of two visibly different
kinds: **chirality** ones ("chirality cannot be selected internally", the `det = −1`
controller that swaps `S±`) and **ternary-phase** ones ("phase-sheet obstruction",
"golden-selector failures", the qutrit phase bundle). Pass 1022 offered a single
`C₆` class as a candidate common cause for all of them.

This pass says that merge would be **wrong**. There are two independent primary
parts, and a subgroup can be clean in one while dirty in the other. So:

- chirality claims belong to the **2-primary** part, `240 → 120`;
- ternary-phase claims belong to the **3-primary** part, `240 → 80`;
- and any claim that identifies one with the other needs a reason, because the
  centre of the group already separates them.

That converts Pass 1022's open Boundary from one unnamed target into **two named
targets**, which is the prerequisite for the identification it asks for.

## Cross-track verification

Before extending anything, this pass re-derives Pass 1022's results independently
(its criterion reimplemented from the statement, not copied) and reproduces all
four: `|H| = 216`, `|L| = 1296`, `C₆` regular monodromy, no equivariant section,
`Z(G)` obstructed, Sylow-5 clean. Their certificate also **runs and passes 25/25
here**, in 31 s.

One provenance nit, not a mathematical one: the committed
`data/w33_pass1022_equivariant_section_obstruction.json` contains a field
`verification.fixed_ci_issue` that the tracked `.g` script does not emit, so the
tracked artifact is not byte-reproducible from the tracked source. Every
mathematical value matches exactly. Worth fixing in a repo whose CI is explicitly
"fail closed on stale certificates".

## Scope

This identifies the 2-primary and 3-primary parts of the Pass 1022 class. It does
**not** prove that any particular earlier corpus obstruction equals either part —
that comparison now has two named targets instead of one, which is the
prerequisite, not the conclusion. The monodromy computation also carries a trap
worth recording: `ActionHomomorphism(stab, block)` returns permutations of
`[1..6]`, not of the block's own point labels, so testing transitivity on the
block silently fails and reads like a mathematical result. It cost a run here.

## Prior art — cited, not reclaimed

- **Pass 1022** (other track) — the `C₆` monodromy, the no-section theorem, the
  subgroup criterion, and both witnesses. All of that is theirs.
- **Pass 1021** — the fibration `240 → 40` and its fibre as the Eisenstein units.
- **Pass 1020** — `Sp(4,3)` transitive on the roots; the block sizes 2, 3, 6.
