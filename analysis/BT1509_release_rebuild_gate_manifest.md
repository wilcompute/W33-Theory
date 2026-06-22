# BT1509 Release Rebuild Gate Manifest

Status: command sequence prepared, not executed here.

## Commands

1. `python tools/bt1506_release_lock_splicer.py`
2. `python tools/bt1504_skew_line_orbit_map.py`
3. `python tools/bt1505_native_d4_generator_route_traces.py`
4. `python tools/bt1508_route_trace_css_syndrome_replay.py`
5. `python -m json.tool data/bt1504_skew_line_orbit_map.json > /tmp/bt1504.json`
6. `python -m json.tool data/bt1508_route_trace_css_syndrome_replay.json > /tmp/bt1508.json`
7. `latexmk -pdf -interaction=nonstopmode photonic_holonet.tex`
8. `python -m pytest --noconftest -q tests/test_bt1492_bt1494_canonical_pulse_release_lock.py`
9. `python scripts/run_focused_bridge_tests.py photonic-qec`

## Visual checks

- `photonic_holonet.pdf` pages `new insertion neighborhood before fuel section`: BT1495-BT1503 inserts render without overfull table rupture.
- `photonic_holonet.pdf` pages `scheduler/pulse table page`: BT1500 count table remains readable.
- `photonic_holonet.pdf` pages `native D4 calibration page`: BT1502 ledger renders as finite calibration, not noise model.

Honesty boundary: this manifest does not claim the PDF was rebuilt or tests were run in this connector turn.
