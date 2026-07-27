# Step 5 — Corpus Identity Layer: 540-Classifier, Alias Registry, Pass Renumbering

**Date:** 2026-07-27  
**Problem:** The repository's primary bottleneck is information architecture.
Three specific issues:
1. The 540-object classifier has not been run to completion; its ambiguity
   report is uncommitted.
2. The canonical alias registry is not frozen — duplicate names obscure
   which theorems and definitions are actually distinct.
3. Pass artifacts 1120–1131 have colliding names; they must be renumbered.

## The 540 objects

The 540 objects likely correspond to one or more of:
- 540 = `|W(3,3)|` isotropic points counted with some multiplicity
- 540 = the number of flags (incident point-line pairs) in W(3,3)
  (40 points × 12 lines through each point / 2 = 240? — recheck)
- 540 = `|Sp(4,3)| / 48 = 540` (a specific orbit)
- 540 = the total in another combinatorial structure related to the project

**Clarification task:** The first action of the corpus layer is to commit
a one-line definition of what the 540 objects are, with a pointer to the
computation that produces them.

## Alias registry specification

The canonical alias registry lives at `data/ALIAS_REGISTRY.json`.
Every named object in the repository must have exactly one canonical name
and a list of known aliases. Format:

```json
{
  "version": "2026-07-27",
  "objects": [
    {
      "canonical": "W33_point_carrier_D_eigenspace_11",
      "aliases": ["trivial_mode", "constant_mode", "all-ones_eigenspace"],
      "dimension": 1,
      "eigenvalue": 11,
      "status": "confirmed",
      "source_commit": "9fb912f6"
    },
    {
      "canonical": "W33_point_carrier_D_eigenspace_1",
      "aliases": ["middle_mode", "24_dim_eigenspace"],
      "dimension": 24,
      "eigenvalue": 1,
      "status": "confirmed",
      "source_commit": "9fb912f6"
    },
    {
      "canonical": "W33_point_carrier_D_eigenspace_minus5",
      "aliases": ["conic_mode", "15_dim_eigenspace", "hyperbolic_mode"],
      "dimension": 15,
      "eigenvalue": -5,
      "status": "confirmed",
      "source_commit": "9fb912f6"
    },
    {
      "canonical": "W33_false_cubic_eigenspace_set",
      "aliases": ["{-7,-1,5}_spectrum", "old_master_cubic_roots", "32dim_packet"],
      "dimension": "INVALID",
      "eigenvalue": "INVALID",
      "status": "QUARANTINED",
      "source_commit": "9fb912f6",
      "note": "Historical fiction. p_old(D) has rank 40; annihilates no eigenspace."
    }
  ]
}
```

## Pass 1120–1131 renumbering plan

The collision among Pass artifacts 1120–1131 must be resolved before any
new theorem can safely cite a Pass number. Resolution protocol:

1. List all artifacts currently labeled Pass 1120–1131:
   ```
   grep -r 'Pass 11[2-3][0-9]' . --include='*.tex' --include='*.md' -l
   ```
2. For each duplicate canonical content, determine which version is primary
   (earlier commit date wins if content is identical; mathematical priority
   wins if content differs).
3. Renumber colliding artifacts to Pass 1132+ (next available block).
4. Update all back-references in `w33_paper.tex` and `photonic_holonet.tex`.
5. Commit the renumbering map to `data/PASS_RENUMBER_MAP.json`.

## 540-classifier run specification

```python
# Script: analysis/w33_540_classifier.py (to be written next)
# Input:  the 540 objects (source to be confirmed — see above)
# Output: data/CLASSIFIER_2026_07_27_540_ambiguity_report.json
# Steps:
#   1. Load the 540 objects from their canonical source
#   2. Classify each by:
#      a. Which W(3,3) eigenspace it projects into (via P_11, P_1, P_-5)
#      b. Whether it appears in the quarantine scanner output
#      c. Whether its Pass label is in the collision range 1120-1131
#   3. Flag all ambiguous objects (projections disagree with stored label)
#   4. Freeze canonical labels for unambiguous objects
#   5. Write ambiguity report
```

## Priority ordering

| Priority | Task | Blocking what |
|---|---|---|
| 1 | Define the 540 objects precisely | All of Step 5 |
| 2 | Freeze ALIAS_REGISTRY.json | Prevents new alias drift |
| 3 | Run quarantine scanner, commit JSON | Step 1 output |
| 4 | Renumber Pass 1120–1131 | Future theorem citations |
| 5 | Run 540-classifier, commit ambiguity report | Final corpus audit |

## Status

- [x] Alias registry format specified (this document)
- [x] Pass renumbering protocol specified
- [x] 540-classifier specification written
- [ ] 540-object source confirmed
- [ ] ALIAS_REGISTRY.json frozen and committed
- [ ] 540-classifier executed
- [ ] Pass 1120–1131 renumbered
