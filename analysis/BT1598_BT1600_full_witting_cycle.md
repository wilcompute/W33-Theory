# BT1598-BT1600: Full Witting Cycle Compiler

BT1598 compiles the accepted `13/40` Witting rail into concrete control frames.
A perfect matching selects one same-ray basis for each Witting ray, and therefore
each Witting basis carries exactly `13` accepted controls:

```text
40 bases * 13 controls = 520 accepted frames
520 * 72 = 37440 ticks
```

BT1599 explains the basis-local surplus.  The physical Witting table has `160`
same-ray apertures, but BT1598 uses only `40` of them as logical controls.  The
remaining `120` records are exactly the BT1365 selector phase sheets:

```text
160 - 40 = 120 = 3 local tomotope sheets * 40 W33/Witting lines
```

BT1600 compiles the full Witting ordered-pair desk:

```text
40 source rays * 40 target rays = 1600 frames
1600 * 72 = 115200 ticks
520 accepted control frames + 1080 contextual fuel frames
```

The Witting desk is now a complete finite transaction cycle: accepted pairs run
the analyzer/mirror control rail, rejected pairs run the OAM/Hesse fuel rail, and
same-ray surplus contexts become the qutrit phase-sheet sidecar.
