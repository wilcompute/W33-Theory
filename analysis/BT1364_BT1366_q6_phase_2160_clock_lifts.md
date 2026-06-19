# BT1364--BT1366 -- Q6, Qutrit Phase, and 2160 Clock Lifts

## Summary

BT1363 left three explicit next moves.  This packet executes all three:

1. lift the local `48`-block tomotope clock to the full `192`-flag/Q6 bus;
2. align the three local sheets with the existing qutrit phase bundle;
3. grade the global `2160` D12 atlas by the local clock.

The result is one factor chain:

```text
48 = 12 * 4 = 3 * 16
192 = 48 * 4
2160 = 45 * 48 = 45 * 12 * 4 = 45 * 3 * 16
```

## BT1364 -- Q6 Flag Bus

The Q6 edge count is

```text
|E(Q6)| = 6 * 2^5 = 192.
```

The tomotope flag carrier is

```text
192 = 48 middle blocks * 4 flag-fiber states.
```

BT1364 pairs the six binary Q6 directions into three direction pairs.  Each
direction pair carries one BT1363 ternary sheet:

```text
3 sheets * 16 middle blocks/sheet * 4 flag states/block = 192.
```

This is a finite bus assignment, not a claim that the full Q6 automorphism
group is the tomotope automorphism group.

## BT1365 -- Qutrit Phase Alignment

BT361 already proved:

```text
120 selector sheets = 40 W33 lines * 3 qutrit phases.
```

BT1363 gives three local tomotope sheets, and each sheet hits all 16 tomotope
face labels exactly once.  BT1365 aligns those three sheets with the qutrit
phase labels:

```text
3 local tomotope sheets * 40 W33 lines = 120 selector phase sheets.
```

The boundary remains honest: this aligns phase indices and incidence profiles;
it does not yet choose a global phase gauge for every skew-line transport
matching.

## BT1366 -- 2160 D12 Clock Grading

BT815 gives the global D12 mirror atlas:

```text
2160 = 540 charts * 4 slots/chart = 45 polar geographies * 48 local blocks.
```

BT1363 explains the 540:

```text
540 = 45 geographies * 12 local C4 cycles.
```

Then each C4 cycle supplies four ticks:

```text
2160 = 45 * 12 * 4.
```

Equivalently, the ternary-sheet reading gives:

```text
2160 = 45 * 3 * 16.
```

This grades the D12 atlas.  It does not replace the D12 mirror stabilizer by a
cyclic clock; BT815's D12-vs-C12 boundary is preserved.

## Verification

```bash
python3 analysis/bt1364_q6_tomotope_flag_bus_lift.py
python3 analysis/bt1365_qutrit_phase_sheet_alignment.py
python3 analysis/bt1366_global_2160_d12_clock_grading.py
python3 tests/test_bt1364_bt1366_clock_lifts.py
python3 -m py_compile analysis/bt1364_q6_tomotope_flag_bus_lift.py analysis/bt1365_qutrit_phase_sheet_alignment.py analysis/bt1366_global_2160_d12_clock_grading.py tests/test_bt1364_bt1366_clock_lifts.py
python3 -m json.tool data/bt1364_q6_tomotope_flag_bus_lift.json
python3 -m json.tool data/bt1365_qutrit_phase_sheet_alignment.json
python3 -m json.tool data/bt1366_global_2160_d12_clock_grading.json
```
