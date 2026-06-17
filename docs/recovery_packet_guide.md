# Finite Clifford Recovery Packet Guide

This guide gives the short path through the external candidate protocol.

## 1. Create a candidate JSON

Use the schema:

```text
schema/bt1269_tomography_candidate.schema.json
```

Required fields:

```text
candidate_id
closure_order
word_diameter
edge_split
diameter_endpoint_first_set_histogram
labelled_channel_spread
```

The edge split contains:

```text
polar_graph
nonpolar_graph
```

## 2. Score one candidate

```bash
python tools/bt1272_score_candidate.py examples/bt1269_exact_polar_path_candidate.json
```

The scorer emits the gate vector, missing gates, score, and band.

## 3. Batch-score all bundled fixtures

```bash
python tools/bt1274_batch_score_candidates.py
```

The bundled fixture distribution is:

```text
pass = 1
review = 1
fail = 2
```

## 4. Inspect the strict recovery certificate

```text
data/bt1275_strict_polar_path_recovery_certificate.json
```

The strict target is:

```text
diam14_polar_path
```

It packages closure, word metric, edge geometry, labelled geodesic data, score vector, candidate schema fields, and validator result.

## 5. Paper sections

The recovery packet is explained by these sections:

```text
paper/sections/sec_bt1261_clifford_tomography_ladder.tex
paper/sections/sec_bt1267_tomography_score_vector.tex
paper/sections/sec_bt1276_external_candidate_protocol.tex
```

## 6. Index

The one-stop machine index is:

```text
data/bt1279_recovery_packet_index.json
```

It points to the schema, fixtures, tools, results, strict certificate, paper sections, CI materializers, and tests.
