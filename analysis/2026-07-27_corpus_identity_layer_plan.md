# Step 5 — Corpus Identity Layer: Executed

**Date:** 2026-07-27  
**Status:** ACTIVE AND ENFORCED

## The two 540-object sets

There are two distinct 540-element sets because both the point and line
collinearity graphs have 40 vertices of non-neighbor degree 27:

- `{540:point-nonedge}`: `40*27/2=540` unordered noncollinear point pairs;
- `{540:line-nonedge}`: `40*27/2=540` unordered disjoint/skew line pairs.

The identity `51840=540*96` applies to both and identifies neither. An explicit
`{540:both}` tag declares that a local passage deliberately compares them.

## Occurrence-level classifier

`scripts/tag_540_disambiguation.py` classifies each literal occurrence rather than
assigning one majority label to an entire file. It:

1. ignores the `540` embedded inside the tag syntax itself;
2. uses line-local explicit tags and vocabulary;
3. reports files containing both objects as `mixed-explicit`;
4. exits nonzero in strict mode for a new unresolved occurrence.

The line / point / mixed regression fixture passes with zero ambiguity. GitHub
Actions runs the classifier over the complete live corpus and writes
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
retracted cubic packet, the two distinct 540 objects, the S5 stabilizer class, the
45-support image `1+20+24`, and the complete 2195-dimensional kernel.

## Enforcement

Pre-commit now fails on:

- a new unregistered descendant of the false shifted-adjacency cubic;
- a changed file with an ambiguous 540 occurrence;
- the known incorrect `S_min` formula.

Legacy full-corpus ambiguity remains visible in the generated report but does not
block unrelated changes; changed files are held to the strict rule.
