# Recovery Packet

The finite Clifford recovery protocol is packaged as a small reproducibility packet.

## Start here

```text
docs/recovery_packet_guide.md
```

## Machine index

```text
data/bt1279_recovery_packet_index.json
```

## Strict certificate

```text
data/bt1275_strict_polar_path_recovery_certificate.json
```

## Verify the certificate

```bash
python tools/bt1281_verify_recovery_certificate.py
```

Expected result:

```text
verified = true
```

## Score a candidate

```bash
python tools/bt1272_score_candidate.py examples/bt1269_exact_polar_path_candidate.json
```

## Batch-score bundled candidates

```bash
python tools/bt1274_batch_score_candidates.py
```

Expected bundled distribution:

```text
pass = 1
review = 1
fail = 2
```

## Paper sections

```text
paper/sections/sec_bt1261_clifford_tomography_ladder.tex
paper/sections/sec_bt1267_tomography_score_vector.tex
paper/sections/sec_bt1276_external_candidate_protocol.tex
paper/sections/sec_bt1282_recovery_packet_reproducibility.tex
```
