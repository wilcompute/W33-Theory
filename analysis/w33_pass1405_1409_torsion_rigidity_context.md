# Passes 1405–1409 — the torsion is not the free part's analogue, covers are near-rigid, and a fourth noise class

Five results, continuing my own queue rather than the parallel track's. Two are
mathematics on the cross-matching, one is a measured tool defect, one is a
manuscript promotion, and one is a bound stated as a bound.

---

## Pass 1405 — the 2-torsion is *not* the free part's analogue

Pass 1397 proved the rational half: `coker(M) ⊗ Q` is irreducible of degree 15
and equals the `(−4)`-eigenspace. The natural expectation is that the
`(Z/2)³⁰` behaves similarly. It does not.

First, where the torsion comes from — exact ranks over three primes:

```text
rank_Q  = 225
rank_F2 = 195      drop 30      <- the entire torsion
rank_F3 = 225      drop  0
rank_F5 = 225      drop  0
```

**2 is the only bad prime.** That is exactly what the coalescence theorem
predicts: `spec(A) = {12, 2, −4}` collapses *completely* mod 2 (all three are
`0`), splits `{12},{2,−4}` mod 3, and `{12,2},{−4}` mod 5. Maximal coalescence at
2, and 2 is where the torsion sits.

Then the module structure, via MeatAxe:

```text
F2^240 composition factors   1^8, 6^6, 8^4, 14^6, 40^2
image submodule              dim 195
QUOTIENT                     dim 45
  composition factors        [1, 1, 1, 6, 8, 14, 14]        (sum 45)
  irreducible?               FALSE
```

So the mod-2 picture is genuinely different in kind. The degree-15 rational
irreducible **reduces to `1 + 14` modulo 2**, and the 30-dimensional torsion
carries the remaining factors `1, 1, 6, 8, 14` (sum 30).

**The honest statement: `coker(M) ⊗ Q` is irreducible, `coker(M) ⊗ F₂` is not.**
No integral analogue of Pass 1397's theorem holds, and the composition factors
say why — the reduction fragments.

---

## Pass 1406 — covers are near-rigid

Pass 1398 showed no exact cover is `G`-invariant, structurally: `G` is transitive
on the 540 frames, so the only invariant sets are `∅` and all 540, and a cover
uses 60. The remaining question is how much symmetry a cover *does* keep.

```text
cover 1..4   |Stab| = 4    orbit 6480    C4
cover 5      |Stab| = 8    orbit 3240    C4 x C2
cover 6      |Stab| = 4    orbit 6480    C2 x C2
```

**Out of `|G| = 25920`, a cover keeps a group of order 4 or 8.** The 60-block
resolution of the edge set is close to rigid: it is a genuinely non-symmetric
decomposition, not a `G`-orbit phenomenon in disguise. `25920/4 = 6480` and
`25920/8 = 3240` check.

That every sampled stabiliser contains a `C₄` or `C₂×C₂` is an observation on six
covers, not a theorem, and is recorded as such.

---

## Pass 1407 — a fourth noise class: `[n,k,d]` is not a code parameter

Pass 1399 removed three noise classes from corpus-wide collision detection.
Reading the surviving head found a fourth, and it is in the *token grammar*, not
the filters:

```text
rarest token in 2 files | 37 shared
   A: data/w33_packet_vm.json
   B: data/w33_python_bytecode_packet_lifter.json
   tokens: [102,103,104] [105,106,107] [108,109,110] [111,112,113] ...
```

Those are consecutive **array rows in a JSON file**, not code parameters. The
guard's `RE_LIN = \[\s*\d+,\s*\d+,\s*\d+\s*\]` matches *any* three-integer list,
and this corpus is full of them — coordinate triples, index blocks, orbit tables.
Pass 328 calibrated this class at 20% signal on **prose**; extending the index to
`.json` broke that calibration silently.

`[[n,k,d]]` stays unconditional — nothing else here is written with double
brackets. A single-bracket triple now counts only when the surrounding 60
characters carry code vocabulary (`code`, `CSS`, `stabilizer`, `distance`,
`BCH`, …), the same contextual rule already used for noun-number tokens:

```text
'{"rows": [[102,103,104],[105,106,107]]}'              ->  no tokens
'the exact CSS code is [137,1,21] with distance 21'    ->  ['[137,1,21]']
```

**A self-inflicted trap worth recording separately.** The first version of that
regex was written through a shell heredoc, and its `\b` word-boundary escapes
were consumed into literal **backspace bytes** (`\x08`), so `RE_CODEWORD` silently
matched nothing and the rule dropped *every* `[n,k,d]` including real ones. It
looked like a working filter. This is the same escaping failure recorded earlier
against GAP sources; the fix is the same — edit the file directly rather than
generating regexes through a shell.

---

## Pass 1408 — the 15-dimensional statement, written for the manuscript

`analysis/BT1408_frame_cross_matching_theorem_insert.tex` states the arc as
Lemma (faithful tetrahedral action) → Proposition (canonical cross-matching) →
Theorem (lands on edges, 9-to-1) → Theorem (cokernel, and the identification with
`ker(A+4I)`) → Remark (what is *not* claimed) → Proposition (resolutions).

It is a promotion candidate, not a promotion: it sits in `analysis/` until read.
Every numeric claim names its certificate, the uniqueness lemma names its Lean
module, and the remark carries Pass 1405's negative result so the rational
theorem cannot be mistaken for an integral one. No `E₈` reading of the 240
appears — Pass 1012 owns that obstruction and the 240 here is the edge set.

---

## Pass 1409 — the cover count is a bound, and stays one

Pass 1398 reported 6,579 distinct exact covers from a depth-first search that was
**time-capped at 780 s**. That is a lower bound produced by an enumeration order
that does not respect `G`-orbits, so it is not an estimate of the total either.

Pass 1406 now bounds it from below structurally instead: covers fall into
`G`-orbits of length 3240 or 6480, so **at least one full orbit of 6480 exists**
and the true count is a sum of such orbit lengths. The exact total remains
uncomputed and is stated that way rather than being extrapolated from 6,579.

## Prior art

- [Pass 1397](analysis/w33_pass1397_1401_cokernel_theorem_covers_collisions.md) — the rational theorem this pass shows has no integral analogue.
- [Pass 1398/1399](analysis/w33_pass1397_1401_cokernel_theorem_covers_collisions.md) — the covers and the first three noise classes.
- [Pass 1390/1392](analysis/w33_pass1390_1391_frame_cross_matching.md) — the cross-matching and its Smith form.
- [`pass828`](analysis/w33_pass828_coalescence_theorem.py) — **owns** the coalescence theorem invoked for the bad prime.
