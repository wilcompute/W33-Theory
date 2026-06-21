# BT1407 Microframe Transaction Composer

BT1406 fills the first 48 tomotope-body ticks with the continuous Q6 stress
walk.  BT1407 closes the full oscillator frame by identifying the remaining
BT1300 local-lift epilogue as one route branch of the BT1404 Hesse return
alphabet.

The frame identity is:

```text
48 Q6 body pulse ticks + 3 Hesse return words * 8 ticks = 72 ticks
```

So the 72-tick oscillator frame is no longer just a budget.  It is a complete
transaction:

```text
ticks  0..47  tomotope body: BT1406 Q6 edge pulses
ticks 48..55  Hesse h=3 return word, (r,p)=(1,0), X^1 Z^0
ticks 56..63  Hesse h=4 return word, (r,p)=(1,1), X^1 Z^1
ticks 64..71  Hesse h=5 return word, (r,p)=(1,2), X^1 Z^2
```

## Stress Route Selection

The six-digit stress route ends at target digit `4`.  The Hesse route branch is
therefore

```text
r = 4 mod 3 = 1
```

and the epilogue carries exactly the three phase outcomes on that branch:

```text
h = 3*r + p = 3, 4, 5
```

All three words reuse the BT1404 return-word shape:

```text
ERASE, ROUTE, PHASE, X-CORR, Z-CORR, T-BIT, RESTORE, NEXT
```

For this branch the shared branch label is `Z Omega`; the phase trits
`p=0,1,2` select `X^1 Z^0`, `X^1 Z^1`, and `X^1 Z^2`.

## Reading

BT1404 showed that the Hesse port has an 8-tick return word for every outcome.
BT1406 showed that the continuous stress route exactly fills the 48-tick
tomotope body.  BT1407 composes them into the full frame:

```text
body carrier path -> selected Hesse branch -> Clifford ABI restore
```

The single-photon runtime now has a frame-level ABI transaction for the stress
route, rather than a body-only timing schedule plus a separate epilogue budget.

## Boundary

BT1407 composes existing ABI schedules.  It does not certify physical SIC
optics, detector electronics, calibrated optical pulse widths, jitter,
dispersion, crosstalk, or waveguide loss.

## Verification

```bash
python tools/bt1407_microframe_transaction_composer.py
python tests/test_bt1407_microframe_transaction_composer.py
python -m py_compile tools/bt1407_microframe_transaction_composer.py tests/test_bt1407_microframe_transaction_composer.py
python -m json.tool data/bt1407_microframe_transaction_composer.json
```
