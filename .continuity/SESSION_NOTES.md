# Session Notes - 2026-08-08

> **Collaborative workspace for you and AI**

## 🎯 Session Goals
- 2026-08-08 current goal: finish and validate the Passes 4324-4334 chamber Hecke and audited-corrections packet while preserving exact theorem, retraction, and open-boundary language.


## 💡 Key Decisions Made
<!-- Important choices during this session -->

## 🚧 Blockers & Challenges
<!-- What's preventing progress? -->

## 🔍 Attempted Approaches
<!-- What did we try that didn't work? -->

## ✅ Next Steps
<!-- What should we do next? -->
- Auto-saved at 2026-08-15T04:28:55.910Z (reason: threshold-commits)
- Recent commits:
  - fb8b83c91 Merge remote-tracking branch 'origin/master'
  - bad265ea3 Pass 5340-5347: a tight coclique IS a regular simplex, and -1/q^2 was wrong one day later
  - e02ea9440 Reserve Pass5356-5363 PSL2 fiber/mod2 footprint lane

## 📝 Open Questions
<!-- What do we still need to figure out? -->

### 2026-08-15 — Track A (Passes 5340-5347)

- **Pass5341-5343**: the eigenspace noncollinear inner product is **-1/(Hoffman-1)**, NOT -1/q^2 as
  Pass5279 published one day earlier. Only GQ(q,q) carriers had been tested, where Hoffman = q^2+1
  makes the two forms identical. H(3,9) separates them and measures -1/27; Q(5,3), a completely
  different SRG(112,30,2,10) with the same Hoffman 28, gives the same value -- so it depends on the
  BOUND alone, not the graph. Consequence: a Hoffman-tight coclique IS a rigid regular
  (H-1)-simplex, which is exactly why the bound cannot see existence.
- **Pass5340/5344**: BT818 repaired. `alpha_exact=7` was always correct; only its prose said 9. The
  `correction` string now interpolates the computed value so the two halves cannot drift again.
  alpha=9 matches no nearby graph (the real values are 7 and 10), so it is a typo, not a
  coordinate artefact.
- **Pass5346-5347 (NEGATIVE)**: certificate self-contradiction resists mechanical detection.
  75% -> 9% flag rate after requiring a relational operator; 1-in-10 precision by hand triage,
  independently confirmed by stem-frequency triage (61% of 388 findings from the 12 commonest
  stems). Docstring extension catches 1 of BT818's 3 faults at a 47% flag rate and is NOT
  registered. Tightening to kill the noise also kills the signal, because prose does not use
  field names.
- **Open**: alpha(W(3,9)) MILP running at 820 vertices (Hoffman 82) -- the third deficit point.
