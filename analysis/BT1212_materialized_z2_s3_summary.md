# BT1212 Materialized Z2/S3 Summary

The uploaded `W33-Theory-master` archive was unpacked and the pending BT1208--BT1210 scripts were run locally in the sandbox.

## BT1208 table

Raw Z2 vs packet-local S3 sign:

| raw Z2 | S3 sign 0 | S3 sign 1 |
|---:|---:|---:|
| 0 | 211 | 203 |
| 1 | 155 | 151 |

Canonical Z2 vs packet-local S3 sign:

| canonical Z2 | S3 sign 0 | S3 sign 1 |
|---:|---:|---:|
| 0 | 220 | 194 |
| 1 | 146 | 160 |

## BT1209 isomorphism sample

The 64-isomorphism run exceeded the sandbox timeout. A 16-isomorphism sample completed and produced 4 distinct table signatures, so the table is not invariant under sampled packet-to-centerquad graph isomorphisms.

## BT1210 schema

The half-fiber presentation-pair schema was materialized with 51840 expected rows, but the full objectwise table was not materialized. The original BT748 run completes quickly for aggregates; the full object table requires an optimized instrumented run to avoid the naive 540-by-51840 fixed-point scan.

## Verdict

The raw/canonical Z2 data and packet-local S3 sign live on isomorphic 720-edge carriers, but the comparison is not canonical until the graph isomorphism is geometrically fixed. The correct next target is a canonical packet-to-centerquad alignment, not a direct equality theorem.
