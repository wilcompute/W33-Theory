# BT1839 — Runtime Audit Manifest

Run these checks in the repo environment:

1. `python analysis/bt1824_executable_packet_replay.py`
2. `python analysis/bt1825_aperture_shot_table_exporter.py`
3. `python analysis/bt1836_e8_selector_aperture_table.py`
4. `python analysis/bt1837_tetracode_quotient_hunt.py`
5. `python analysis/bt1832_tex_build_check.py`
6. `python -m pytest tests/test_bt1823_bt1827_runtime_stack.py tests/test_bt1818_bt1822_execution.py -q`

Expected generated outputs:

- `data/PART_BT1824_EXECUTABLE_PACKET_REPLAY_results.json`
- `data/PART_BT1825_APERTURE_SHOT_TABLE_summary.json`
- `data/PART_BT1836_E8_SELECTOR_APERTURE_TABLE_summary.json`
- `data/PART_BT1837_TETRACODE_QUOTIENT_HUNT_results.json`
- `data/PART_BT1832_TEX_BUILD_CHECK_results.json`

Pass condition: every command exits successfully and the expected JSON outputs exist.

Honest boundary: this is the reproducible audit manifest, not an executed CI log.
