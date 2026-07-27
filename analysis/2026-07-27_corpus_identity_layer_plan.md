# Step 5 — Corpus Identity Layer: Executed

**Date:** 2026-07-27  
**Status:** ACTIVE AND ENFORCED

## The five degree-540 object species

Pass 1139 supersedes the original two-object inventory. A transitive
`PSp(4,3)`-set of degree 540 <!-- {540:mixed} --> has an order-48 stabilizer, and the `U4(2)` table
of marks has exactly five conjugacy classes of those subgroups:

- `{540:point-nonedge}`: TOM 77, rank 25, unordered noncollinear point pairs;
- `{540:double-six-nonincident}`: TOM 78, rank 28, `36*15` cubic
  nonincidence flags;
- `{540:gq42-arc}`: TOM 79, rank 27, `45*12` ordered support-geometry arcs;
- `{540:outer-4c}`: TOM 80, rank 21, restricted `W(E6)` class `4C`;
- `{540:line-nonedge}`: TOM 81, rank 32, unordered disjoint/skew line pairs.

The identity `51840=540*96` applies to several of these and identifies none.
Even the abstract stabilizer `C2 x S4` occurs twice, at ranks 28 and 32. The
compatibility tags `{540:both}` and `{540:mixed}` are reserved for a genuinely
mixed single occurrence.

## Occurrence-level classifier

`scripts/tag_540_disambiguation.py` classifies each literal occurrence rather than
assigning one majority label to an entire file. It:

1. ignores the `540` embedded inside the tag syntax itself;
2. binds a tag to one nearest numeric occurrence on the same line;
3. recognizes all five TOM species and reports multi-species files as
   `mixed-explicit`;
4. prunes repository metadata, caches, environments, and build trees;
5. exits nonzero in strict mode for a new unresolved occurrence.

The same-line multi-occurrence and five-species regression fixtures pass with
zero ambiguity. GitHub Actions runs the classifier over the complete live
corpus and writes
`data/BT1634_540_audit_results.json`.

## Namespace registry

`data/w33_pass_namespace_registry_v2.json` establishes:

- Passes 1120–1124: canonical merged glue track;
- Passes 1125–1128: canonical merged filter/carrier track;
- Passes 1132–1136: this exact execution release.

Draft PR #162's branch-local 1120/1121 labels are provisional and noncanonical.
Its exact class-algebra and cubic-incidence content is imported into Pass 1135
without importing the collided numbers.

## Alias registry

`data/ALIAS_REGISTRY.json` now records the corrected three eigenspaces, the
retracted cubic packet, all five degree-540 objects with their TOM positions and
ranks, the S5 stabilizer class, the 45-support image `1+20+24`, and the complete
2195-dimensional kernel.

## Enforcement

Pre-commit now fails on:

- a new unregistered descendant of the false shifted-adjacency cubic;
- a changed file with an ambiguous 540 occurrence;
- the known incorrect `S_min` formula.

Legacy full-corpus ambiguity remains visible in the generated report but does not
block unrelated changes; changed files are held to the strict rule.
