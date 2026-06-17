# BT1272 -- Schema Candidate CLI

## Purpose

BT1272 completes the BT1269/BT1266 bridge: a schema-shaped external candidate JSON can now be scored directly from the command line.

## CLI

```text
tools/bt1272_score_candidate.py <candidate.json> [--out result.json]
```

## Gate vector

```text
closure51840
diameter14
polar_path_P4P4
unique_all_channel_endpoint
labelled_nonzero_spread
```

## Band rule

```text
5/5 -> pass
full closure plus at least one additional gate -> review
otherwise -> fail
```

## Fixtures

The CLI is intended for the fixtures added in BT1271 and future external candidate files matching the BT1269 schema.

## Files

- CLI: `tools/bt1272_score_candidate.py`
- Summary: `data/bt1272_candidate_cli_summary.json`
