# BT1894 Witting Transaction Automaton Verifier

BT1894 reconstructs the Witting delayed-query table from the uploaded Holonet TeX.

Source anchors in the uploaded TeX:

```text
logical ordered-pair table: lines 4116-4127
physical frame table:      lines 4128-4143
packet slot and 72 ticks:  lines 4145-4158
four aperture audit:       lines 4091-4095
```

## Logical table

```text
40 * 40 = 1600 rows
same-ray pairs            = 40
compatible distinct pairs = 480
retry-shadow pairs        = 1080
```

Checks:

```text
40 + 480 + 1080 = 1600
40 + 480 = 520 accepted rows
520 / 1600 = 13 / 40
```

## Physical frame table

```text
40 Witting tetrads * 4 Alice slots * 4 Bob slots = 640 records
diagonal witness records  = 160
off-diagonal data records = 480
160 + 480 = 640
640 - 520 = 120 contextual aperture overhead
```

## Tick counts

```text
ticks per frame = 72
1600 * 72 = 115200
520 * 72  = 37440
640 * 72  = 46080
4 * 72    = 288
```

## Source absence note

I did not find an exact `2048 = 1600 + 448` line in the uploaded TeX used for this pass.  BT1894 therefore verifies the 1600-row / 640-frame / 72-tick automaton only.

Boundary: finite scheduler/accounting verifier only.
