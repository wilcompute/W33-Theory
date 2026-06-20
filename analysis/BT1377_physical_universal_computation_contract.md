# BT1377 -- Physical Universal-Computation Contract

## Summary

BT1377 assembles the recent runtime packets into one physical computation
contract:

```text
logical packet digit
  -> 8-tick optical word
  -> Q6/tomotope switch edge
  -> S3 phase synchronization
  -> central C3 Steinberg scheduler
  -> 720-frame / 51840-window Clifford supercycle
```

The result is a deterministic physical Clifford/`Sp(4,3)` runtime.  It is not
claimed to be universal by itself.  Universal quantum computation requires the
explicit non-Clifford port recorded by the older TQC artifact: Hesse-SIC/T
measurement or Fibonacci braiding.

## Physical Execution

The eight ISA ticks have direct hardware readings:

```text
ticks 0..2: tritter/EOM ternary-axis phase pulses
ticks 3..7: delay-line apartment-hop switch pulses
```

BT1374 then lowers each packet row through:

```text
tomotope_flag = 4 * tomotope_block + (mirror_slot mod 4)
```

so every packet address becomes a single-bit Q6 edge.  The six-digit stress
route uses six distinct Q6 switch edges inside the 48-tick tomotope body.

The physical timing ladder is:

```text
word:              8 tau
tomotope body:    48 tau
local epilogue:   24 tau
microframe:       72 tau
mirror bus:     2160 tau
Clifford cycle: 51840 tau
```

BT1376 supplies the current phase synchronization frontier: the `210`
identity-edge / `330` correction S3 gauge is strict under every root-fixed
one-, two-, and three-line relabeling checked.  BT1375 supplies the generation
clock: the scheduler is the concrete central `C3` action on Steinberg
cycle-vector witnesses, with `27` three-cycles and nilpotent ranks `54,27,0`.

## Universal Boundary

The deterministic kernel is a protected finite Clifford runtime:

```text
Sp(4,3) runtime order = 51840
720 oscillator frames = one Clifford supercycle
```

That is not universal quantum computation alone.  The universal architecture
requires a non-Clifford resource port:

```text
Hesse-SIC/T measurement, or Fibonacci braiding
```

So the honest architecture statement is:

```text
physical Clifford machine + explicit non-Clifford port = universal QC architecture
```

## Verification

```bash
python3 analysis/bt1377_physical_universal_computation_contract.py
python3 tests/test_bt1377_physical_universal_computation_contract.py
python3 -m py_compile analysis/bt1377_physical_universal_computation_contract.py tests/test_bt1377_physical_universal_computation_contract.py
python3 -m json.tool data/bt1377_physical_universal_computation_contract.json
```
