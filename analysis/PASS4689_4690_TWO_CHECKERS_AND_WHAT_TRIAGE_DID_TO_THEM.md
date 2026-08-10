# Passes 4689–4690 — two checkers, and the thing that only shows up after you triage them

Two rules that existed as prose are now executable. Both found something. One of them found
mostly noise first, and the noise is the more useful half of this note.

## 4689 — the unpowered null

`scripts/check_search_power.py`. Flags a sample count plus a null verdict with no
denominator nearby: no space size, no coverage percentage, no power, no "exhaustive".

Built because Pass 4680 found a sentence reporting "30,000 sampled … produced no witness"
that covered **0.0095%** of its space and had **0.95%** power against a hundred-witness set.
The hedge was there. The denominator was not, and the denominator is what decides whether a
null is evidence.

**Sweep of 5,302 files → 3 hits.** One of them is
`analysis/w33_pass2881_three_copy_first_order.py:154` — the exact pass Pass 4680 diagnosed
by hand. The checker was written from the *shape* of the fault, not from that file, and
re-found it independently. The other two are a 5,000-trial cocycle probe in `bt1749` and its
execution summary, both of which report a null with no coverage figure.

## 4690 — the may-claim table, enforced

`scripts/check_layer_conformance.py`. Part 0 of the blueprint ends with a table saying what
each layer may and may not claim, and asserts that most withdrawn claims in the project were
violations of it. That makes it a decision procedure, and a decision procedure that runs
only in a reader's head runs only on the pages a reader reaches.

| layer | may claim | may **not** |
|---|---|---|
| L0–L2 | necessity, exact counts | speed, area, power |
| L3 | gate counts, relative cost | minimality or uniqueness |
| L4 | energy floors, timing | that a floor was *achieved* |
| L5–L6 | behaviour, equivalence | anything about physics |

### First run: 15 violations. After triage: 1.

This is the part worth keeping.

| family | count | verdict |
|---|---:|---|
| table flattening | 8 | **false** — a `tabular` body has no sentences, so the splitter merged a geometry row and a MHz column into one "claim" |
| "minimal engine" | 6 | **false** — `minimal` there names the minimal *generating set*, an L2 theorem that **is** proved, not a cell count |
| L1 mixing time in ns | 1 | **real** |

The second family is the instructive one. One of those six hits was the blueprint's own
`gotwrong` box, which reads *"A minimality proof says nothing about area."* **The checker
flagged the passage that correctly draws the exact line the checker exists to enforce.** A
checker that penalises a document for warning about the confusion it detects is not strict —
it is measuring vocabulary and calling it judgement.

Both families are now excluded (tabular/spec environments skipped; `minimal
engine|generating set|instruction set|arithmetic core` recognised as the proved sense), with
both kept as regression cases in `--selftest`. Precision on this document went 1/15 → 1/1.

### The one real finding, and the fix

> A frame forgets its origin by 1/e in 9.4 instructions and is statistically gone after 15 —
> **71.8 ns** at the measured 208.86 MHz.

The instruction count is L1 and forced by the geometry — true on every conforming machine.
The nanoseconds are L4 and true only on an iCE40 at that clock. The headline bolded the
part that does not port. Rewritten so the forced quantity leads and the conversion is marked
part-specific.

## Both checkers ship with planted faults

Per failure mode 7. Each self-test pairs every planted violation with a **clean sentence at
the same layer using the same nouns**, differing only in the forbidden move — so a checker
that flagged both halves would be detecting the topic rather than the fault. 10/10 and 4/4.

## Boundary

Layer detection is **sentence-local**. A claim whose layer is set by the previous paragraph,
or split across a sentence boundary, is invisible — and both examples Part 0 itself gives (a
wattage from an assumed cadence, a cell count against a wrong baseline) are of that kind. The
power checker sees phrasings it was given; a null reported in a table or a variable name is
invisible to it. Planted-fault recall measures the families you have, never the ones you lack.
