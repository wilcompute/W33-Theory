# BT1376 -- Radius-3 Local Optimum Certificate for the S3 Gauge

## Summary

BT1373 improved the BT1370 spanning-tree gauge:

```text
spanning-tree gauge: 160 identity edges, 380 corrections
BT1373 S3 gauge:     210 identity edges, 330 corrections
```

BT1376 strengthens the optimization certificate around that witness.  It keeps
the same root-fixed convention, line `0` labelled by the identity permutation,
and exhaustively checks every relabeling of one, two, or three non-root W33
lines.

## Result

The BT1373 witness is a strict local optimum through radius `3`.

```text
radius 1:     195 candidates checked, best delta -5
radius 2:  25,935 candidates checked, best delta -5
radius 3: 1,964,885 candidates checked, best delta -5
total:    1,991,015 candidates checked
```

So every tested root-fixed local move lowers the identity-edge score from
`210` to at most `205`.  Equivalently, every tested move raises the correction
count from `330` to at least `335`.

## Boundary

This is not a proof that `330` is the global minimum over all `6^39`
root-fixed gauges.  It is a finite local certificate: no one-line, two-line, or
three-line relabeling of the concrete BT1373 witness improves the gauge.

The global problem remains a Max-2CSP over the W33 skew-line graph with six
labels per line and `540` S3 transport constraints.

## Verification

```bash
python3 analysis/bt1376_s3_gauge_radius3_local_optimum_certificate.py
python3 tests/test_bt1376_s3_gauge_radius3_local_optimum_certificate.py
python3 -m py_compile analysis/bt1376_s3_gauge_radius3_local_optimum_certificate.py tests/test_bt1376_s3_gauge_radius3_local_optimum_certificate.py
python3 -m json.tool data/bt1376_s3_gauge_radius3_local_optimum_certificate.json
```
