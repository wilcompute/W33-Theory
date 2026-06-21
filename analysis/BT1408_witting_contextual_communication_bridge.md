# BT1408 Witting Contextual Communication Bridge

BT1408 imports the useful part of Vlasov's Witting-polytope communication
scheme into the holonet ABI.

The external scheme uses the Witting configuration as a 40-card ququart
communication desk: 40 rays and 40 orthogonal tetrads.  The holonet reading is
sharper than a generic QKD analogy.  Around any selected ray, the other side of
the protocol splits as:

```text
1 same ray + 12 compatible orthogonal rays + 27 incompatible rays = 40
```

Thus a delayed-query agreement round accepts with probability:

```text
(1 + 12) / 40 = 13/40
```

and rejects with probability:

```text
27/40
```

This is the Bell-line shell in protocol form: self, compatible gauge shell, and
incompatible matter shell.

## Correction Boundary

The Vlasov paper reports an illustrative classical one-mark ceiling of `34/40`.
The repo must not re-import that value as a theorem.  BT823 already proved the
exact Witting noncontextual ceiling:

```text
36/40, deficit 4, contextual fraction 1/10
```

So BT1408 uses the paper for the communication architecture and keeps BT823 as
the local contextuality certificate.

## ABI Bridge

An accepted Witting round selects a common tetrad.  A tetrad has four outcome
slots:

```text
slot 0, slot 1, slot 2, slot 3
```

Those are not a new bus.  They are exactly the four local BT1374 residues:

```text
tomotope_flag = 4 * tomotope_block + (mirror_slot mod 4)
```

After basis agreement, the ququart outcome slot can be read as
`mirror_slot mod 4`, enter the Q6/tomotope packet ABI, and then run through the
BT1407 full frame:

```text
48 Q6 body pulse ticks + 3 Hesse return words * 8 ticks = 72 ticks
```

## Reading

BT1408 makes the outside communication paper part of the machine architecture:

```text
Witting query pair -> common tetrad -> mirror slot -> Q6 body -> Hesse epilogue
```

The accepted sector is `13/40`.  The rejected sector is `27/40`, the same
`q^q` matter shell already used by the holonet as contextual fuel.  The
tamper-evidence audit remains the corrected BT823 `36/40` KS budget.

## Boundary

This is a finite communication/ABI certificate.  It is not a proof of
cryptographic security, detector calibration, loss tolerance, or a physical
ququart implementation.

## Verification

```bash
python tools/bt1408_witting_contextual_communication_bridge.py
python tests/test_bt1408_witting_contextual_communication_bridge.py
python -m py_compile tools/bt1408_witting_contextual_communication_bridge.py tests/test_bt1408_witting_contextual_communication_bridge.py
python -m json.tool data/bt1408_witting_contextual_communication_bridge.json
```
