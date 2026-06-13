# BT906 — Clean-context BT905 Run

BT906 executed the one-command Holonet profile CI in a clean local workspace:

```bash
python tools/run_bt905_holonet_profile_ci.py --compile
```

## Result

Status: **passed**

The run produced a patched and compiled Holonet PDF.

- PDF pages rendered: 35
- PDF SHA256:

```text
e934160ca0742c4aaf012e3ad3dd3e789f7abc27531e9d732b49da9c3b7050b6
```

- Patched TeX SHA256:

```text
bb6f678632950e6d619085a8a9cd9683bf3d6863d37965cf2bf01187cb4fcae5
```

The PDF was rendered with the PDF skill renderer at 120 dpi and all 35 pages rendered successfully.

## Honest scope

This was a clean-context local simulation, not a network `git clone`. It copied only the needed root source and BT899/BT901/BT902/BT903/BT904/BT905 scripts into a fresh workspace, then ran the CI guard from there.

## Witness

```text
tools/simulate_bt906_clean_context.py
data/PART_BT906_CLEAN_CONTEXT_BT905_RUN_results.json
```
