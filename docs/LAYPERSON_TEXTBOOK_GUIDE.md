# W33 Beginner Textbook

Full beginner curriculum for understanding this repository with zero physics background.

If you want the shortest possible version first, read `docs/LAYPERSON_ONE_PAGE_MAP.md`, then return here.

---

## Table of Contents

1. What You Are Looking At
2. How To Use This Textbook
3. The Main Idea In Plain Language
4. What Is Actually Being Claimed
5. What Is Not Being Claimed
6. The Core Objects (No Prerequisites)
7. The Repository Method: Claim -> Script -> Artifact -> Test
8. Confidence Levels: From Facts To Speculation
9. Your First Reproducibility Lab
10. How To Read Dense Research Docs Efficiently
11. Common Failure Modes For New Readers
12. Practical Glossary
13. 7-Day Learning Plan
14. How To Contribute As A Non-Expert
15. Final Orientation

---

## 1. What You Are Looking At

This repository is a computational research workspace that combines:

- math objects (finite geometry and symmetry groups)
- scripts that compute properties of those objects
- tests that check those computations
- writeups that interpret the results

Think of it as a hybrid:

- textbook (explains ideas)
- lab manual (tells you what to run)
- audit trail (stores outputs and checks)

### One-sentence summary

The repo asks whether a very specific finite geometry can reproduce structural patterns that also appear in exceptional Lie algebra frameworks used in high-energy physics mathematics.

---

## 2. How To Use This Textbook

Choose one mode.

### Mode A: 10-minute orientation

1. Read Sections 1, 3, 4, 5, and 7.
2. Run one script and one test from Section 9.
3. Stop and summarize in your own words.

### Mode B: 60-minute structured pass

1. Read Sections 1 through 10.
2. Run the full mini-lab in Section 9.
3. Use Section 8 to classify claim confidence.

### Mode C: Full beginner track

1. Read the whole guide.
2. Follow the 7-day plan in Section 13.
3. Add your own evidence notes file.

---

## 3. The Main Idea In Plain Language

Imagine a puzzle board with strict rules.

- It has fixed points and fixed connections.
- It has symmetry moves that keep the board structure unchanged.
- When you compute many properties of this board, certain number patterns appear.

This project asks:

- Do those computed patterns line up with known algebraic structures (`E6`, `E7`, `E8`) that are important in mathematical physics?

The repo does not rely on hand-wavy storytelling. It emphasizes executable checks.

---

## 4. What Is Actually Being Claimed

At a high level, the repository claims that:

1. The finite geometry `W(3,3)` (and its point graph `W33`) has rich symmetry/combinatorial structure.
2. Several computed invariants from that structure align with specific exceptional-algebra decompositions and counts.
3. These alignments can be generated and tested via scripts in this repo.

At an operational level, each major claim should be attached to:

- a script path
- a test path
- an artifact or report path

If you cannot find those three, treat the claim as narrative or in-progress.

---

## 5. What Is Not Being Claimed

This repo does not, by itself, provide:

- direct experimental confirmation in nature
- mainstream-consensus acceptance
- a final settled "physics is solved" conclusion

Important distinction:

- "computationally verified in this code model" is not identical to "experimentally validated by particle experiments."

This distinction is a strength, not a weakness. It keeps reasoning honest.

---

## 6. The Core Objects (No Prerequisites)

### 6.1 Graph

A graph is just:

- nodes (points)
- edges (connections)

`W33` is a graph derived from the finite geometry `W(3,3)`.

### 6.2 Symmetry

A symmetry operation changes labeling/placement but preserves structure.

If the object "looks the same" after the move, that move is a symmetry.

### 6.3 Automorphism group

All structure-preserving symmetries collected together form an automorphism group.

This repo tracks where those groups match known algebraic group orders.

### 6.4 Homology

Homology is a method to count hole-like structure in a combinatorial space.

You do not need full algebraic topology to begin. For beginners:

- homology gives structural counts with rigorous algebra behind them
- those counts are compared against algebraic decomposition dimensions

### 6.5 Artifacts

Artifacts are machine-generated outputs (JSON/MD/etc.) from scripts.

They are the evidence trail between code execution and documentation claims.

---

## 7. The Repository Method: Claim -> Script -> Artifact -> Test

This is the core discipline used in this project.

### 7.1 Why this matters

Without this chain, research text is hard to audit.

With this chain, anyone can do:

- rerun
- compare
- challenge

### 7.2 Canonical example pattern

1. Claim appears in a doc.
2. Script computes relevant quantity.
3. Artifact stores computed output.
4. Test checks consistency/constraints.

### 7.3 Beginner rule

When reading any claim, immediately ask:

- "Where is the script?"
- "Where is the test?"
- "Where is the output?"

If you can answer all three, you are reading this repo correctly.

---

## 8. Confidence Levels: From Facts To Speculation

Use this classification while reading.

### Level 0: Definitions

- naming conventions
- object definitions
- canonical counts in standardization files

### Level 1: Computed facts

- script output reproduces a number/structure
- test confirms expected property in code model

### Level 2: Structured correspondences

- repeatable matches between independently computed structures
- stable under rerun/tests

### Level 3: Physical interpretation

- mapping mathematical structure to physics language
- may be insightful but is conceptually stronger than Level 1

### Level 4: Broad theory conclusion

- high-level synthesis claims
- should be treated cautiously unless independently validated beyond code checks

This layered reading method prevents confusion and overclaiming.

---

## 9. Your First Reproducibility Lab

This lab is designed to be beginner-safe and fast.

## 9.1 Setup

```bash
python -m venv .venv
# PowerShell
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements-dev.txt
```

## 9.2 Run one core script

```bash
python scripts/w33_e8_correspondence_theorem.py
```

What to look for:

- successful completion
- structural counts reported
- no silent crash

## 9.3 Run one core test

```bash
python -m pytest tests/test_e8_embedding.py -q
```

What to look for:

- pass/fail status
- deterministic behavior on rerun

## 9.4 Run one bridge path

```bash
python scripts/w33_heisenberg_qutrit.py
python -m pytest tests/test_heisenberg_qutrit_structure.py -q
```

What to look for:

- script and test both succeed
- docs describing this path can be traced in `docs/reports/auto_ingest/`

## 9.5 Interpretation checklist

After running, write answers:

1. Which claims were directly tested?
2. Which were only narrated?
3. What evidence files were produced or referenced?

This separates understanding from impression.

---

## 10. How To Read Dense Research Docs Efficiently

Use this scan pattern for any long file.

1. Read first paragraph and section headings only.
2. Mark all script paths.
3. Mark all test paths.
4. Mark all artifact paths.
5. Only then read proof narrative.

For this repository, prioritize:

1. `README.md`
2. `STANDARDIZATION.md`
3. `docs/INDEX.md`
4. claim-specific docs listed under the relevant track

This avoids drowning in volume.

---

## 11. Common Failure Modes For New Readers

### Failure mode 1: Reading everything linearly

Fix:

- follow entry points, not chronological file names

### Failure mode 2: Confusing script success with physical truth

Fix:

- classify confidence using Section 8

### Failure mode 3: Treating all docs as equal quality signal

Fix:

- weight docs higher when they include direct run/test links

### Failure mode 4: Ignoring canonical definitions

Fix:

- always anchor terminology with `STANDARDIZATION.md`

---

## 12. Practical Glossary

- `W(3,3)`: symplectic generalized quadrangle object used as starting structure.
- `W33`: point graph associated with `W(3,3)`.
- `SRG`: strongly regular graph.
- `Automorphism`: structure-preserving symmetry map.
- `E6`, `E7`, `E8`: exceptional Lie algebras.
- `Homology`: algebraic structure-counting framework.
- `Artifact`: generated evidence file from script execution.
- `Smoke test`: minimal quick-check test.
- `Reproducibility`: same commands produce consistent outputs.
- `Invariant`: quantity/property unchanged under allowed transformations.
- `Certificate`: compact witness showing why a claim holds or fails in a finite search space.
- `UNSAT core`: minimal set of constraints that cannot be satisfied simultaneously.

---

## 13. 7-Day Learning Plan

### Day 1

- Read `README.md`
- Read `STANDARDIZATION.md`
- Skim `docs/INDEX.md`

### Day 2

- Run Section 9 setup
- Execute one script + one test

### Day 3

- Read `docs/STATUS_AND_GAPS.md`
- Classify statements by confidence level (Section 8)

### Day 4

- Read one deep claim doc (for example `docs/NOVEL_CONNECTIONS_2026_02_10.md`)
- Extract its claim->script->test chain

### Day 5

- Inspect one artifact JSON and map keys to script logic

### Day 6

- Run a second pipeline (for example qutrit/Heisenberg path)

### Day 7

- Write a one-page summary:
  - strongest reproducible claims
  - weakest evidence points
  - next checks you would request

If you can do Day 7, you have practical mastery of this repository's structure.

---

## 14. How To Contribute As A Non-Expert

You can help even without advanced physics.

High-value contributions:

- improve docs clarity and navigation
- add run instructions and expected outputs
- tighten test coverage for claim paths
- add script argument validation and helpful errors
- improve artifact schema consistency

Contributor starting point:

- `CONTRIBUTING.md`

When proposing changes, keep the core discipline:

- every new claim should point to script/test/artifact.

---

## 15. Final Orientation

The healthiest mindset for this repo is:

- curious
- skeptical
- evidence-first

You do not need to accept every conclusion.
You need to follow the computational evidence chain and reason precisely.

That is exactly what this repository is built to support.
