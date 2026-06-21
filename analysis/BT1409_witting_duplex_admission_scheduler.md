# BT1409 Witting Duplex Admission Scheduler

BT1408 established the Witting communication bridge:

```text
1 same ray + 12 compatible orthogonal rays + 27 incompatible rays = 40
```

so a state-query round accepts at `13/40`.

BT1409 adds the missing scheduler distinction.  A Witting ray lives in exactly
four tetrads.  Therefore a basis-query round has a smaller witness aperture:

```text
4 witness bases / 40 bases = 1/10
```

The complement is:

```text
36 rejected bases / 40 bases = 36/40
```

This is the useful reconciliation: `13/40` is communication throughput, while
`1/10` is the contextual witness aperture.  The `36/40` basis shadow matches
the corrected BT823 noncontextual ceiling.

## Two Clocks

For each selected Witting ray:

```text
state clock: 13 compatible states, 27 incompatible states
basis clock: 4 witness tetrads, 36 retry-shadow tetrads
incidence clock: 16 compatible incidences out of 160 = 1/10
```

The same selected ray has multiplicity four in the accepted basis incidences:
it appears once in each of its four tetrads.  The other twelve compatible
states appear once each.

## Frame Reading

If every compatible state is served as a BT1407 frame, one selected-ray state
census uses:

```text
13 * 72 = 936 frame ticks
```

If only the four basis witness apertures are audited, the contextual tamper
audit uses:

```text
4 * 72 = 288 frame ticks
```

Rejected choices need not consume BT1407 frames.  They are retry-shadow or
matter-shell classifications unless an implementation chooses to log them.

## Boundary

BT1409 is a finite scheduler/count certificate.  It does not prove
cryptographic security, channel loss tolerance, detector calibration, or a
physical Witting-ququart implementation.

## Verification

```bash
python tools/bt1409_witting_duplex_admission_scheduler.py
python tests/test_bt1409_witting_duplex_admission_scheduler.py
python -m py_compile tools/bt1409_witting_duplex_admission_scheduler.py tests/test_bt1409_witting_duplex_admission_scheduler.py
python -m json.tool data/bt1409_witting_duplex_admission_scheduler.json
```
