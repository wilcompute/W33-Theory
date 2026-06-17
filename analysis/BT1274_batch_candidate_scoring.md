# BT1274 -- Batch Candidate Scoring

## Purpose

BT1274 scores every external candidate fixture matching:

```text
examples/bt1269_*candidate.json
```

## New CLI

```text
tools/bt1274_batch_score_candidates.py
```

It calls the BT1272 single-candidate scorer for each fixture and writes one aggregate JSON.

## Result

```text
candidate_count = 4
pass = 1
review = 1
fail = 2
```

The exact polar-path candidate passes. The diameter-12 candidate is review. The sparse full-closure and not-full-order candidates fail.

## Files

- CLI: `tools/bt1274_batch_score_candidates.py`
- Result: `data/bt1274_batch_candidate_scores_summary.json`
