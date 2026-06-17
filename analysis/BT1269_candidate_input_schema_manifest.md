# BT1269 -- Candidate Input Schema

## Purpose

BT1269 adds a stable JSON input shape for external Clifford tomography candidates.

## Schema file

```text
schema/bt1269_tomography_candidate.schema.json
```

## Required fields

```text
candidate_id
closure_order
word_diameter
edge_split
diameter_endpoint_first_set_histogram
labelled_channel_spread
```

The `edge_split` object contains two graph names: `polar_graph` and `nonpolar_graph`.

## Gate mapping

```text
closure_order -> closure gate
word_diameter -> diameter gate
edge_split -> polar path gate
diameter endpoint histogram -> all-channel endpoint gate
labelled_channel_spread -> labelled spread gate
```

## Boundary

The JSON schema file was pushed. A companion smoke-validator script was attempted, but the connector safety layer blocked the script creation in this turn. The executable pass/review/fail validator remains BT1266.
