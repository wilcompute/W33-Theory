# BT1519 Full Fixture CSV Materializer

BT1519 materializes the full native D4 calibration fixture CSV in checkout.

The generated fixture has 576 rows: 8 native generators times 72 ticks. Measurement columns are blank placeholders.

The connector blocked committing the literal generated CSV sample, so the executable materializer and manifest are the committed source of truth.
