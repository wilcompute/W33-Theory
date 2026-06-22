# BT1410 Witting Delayed-Query Frame Compiler

BT1408 imported the Witting communication shell and BT1409 separated its two
admission clocks.  BT1410 compiles the delayed-query step into a frame table.

## Logical Table

The ordered query-pair table has `40*40=1600` rows:

```text
same ray:                    40
compatible distinct rays:   480
incompatible retry shadow: 1080
accepted logical pairs:     520 = 13*40
```

Thus the logical acceptance rate remains `520/1600 = 13/40`.

## Physical Frame Table

The physical frame table is basis-local:

```text
40 tetrads * 4 Alice query slots * 4 Bob query slots = 640 records
```

Each tetrad contributes a `4x4` tile:

```text
4 diagonal witness apertures + 12 off-diagonal data handshakes
```

Across all tetrads this becomes:

```text
160 diagonal witness aperture records
480 off-diagonal data handshake records
```

The physical table exceeds the logical accepted-pair table by `120` records
because each same-ray query pair has four possible witness bases instead of one.
That is the BT1409 basis aperture, not duplicate communication throughput.

## Compiler Rule

For a pair of delayed query rays `(alice_ray, bob_ray)`:

```text
no common tetrad     -> retry shadow, no frame
one common tetrad    -> open that tetrad as the BT1407 frame basis
four common tetrads  -> same-ray case; use a two-bit aperture selector
```

After the common basis is selected, the actual measurement outcome is one of
the four basis slots.  That slot enters the packet ABI as:

```text
tomotope_flag = 4*tomotope_block + (mirror_slot mod 4)
```

So the Witting "40 quantum cards" desk becomes a packet admission ROM:
off-diagonal entries carry compatible communication pairs, while diagonal
entries are contextual audit apertures.

## Boundary

BT1410 is a compiler/count certificate.  It does not prove cryptographic
security, detector calibration, loss tolerance, or a physical Witting-ququart
implementation.

## Verification

```bash
python tools/bt1410_witting_delayed_query_frame_compiler.py
python tests/test_bt1410_witting_delayed_query_frame_compiler.py
python -m py_compile tools/bt1410_witting_delayed_query_frame_compiler.py tests/test_bt1410_witting_delayed_query_frame_compiler.py
python -m json.tool data/bt1410_witting_delayed_query_frame_compiler.json
```
