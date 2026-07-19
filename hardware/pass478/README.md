# Pass 478 independent optical acquisition

This directory separates the laboratory operator from the analyst.

1. On a private machine, generate a fresh 32-byte random salt and run `prepare_private_blind_run.py --salt-hex <64-hex> --output-dir <private-dir>`.
2. Keep the private run plan and reveal offline until predictions are frozen.
3. Acquire 48 field and 48 ring samples in blinded order and record all sixteen phase counts in canonical phase order.
4. Publish only the commitments, measured manifest, measured transfer matrix, and label-free sealed observations.
5. Run the frozen Pass 467 classifier and commit `measured_predictions.json`.
6. Only then publish the reveal with `prediction_sha256` set to the committed prediction hash and score the balanced-accuracy endpoint.

No measured files are included here. The public repository cannot substitute for an independent laboratory operator or physical apparatus.
