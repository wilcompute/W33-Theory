# BT1881-BT1883 summary

Executed BT1881-BT1883.

BT1881 adds a repeated-syndrome decoder for the `[[66,13,3]]_3` parent code.  It corrects persistent single-error histories and flags ambiguous distance-3 relation shadows rather than claiming generic weight-2 correction.

BT1882 adds a payload-path reuse architecture for the five-round optical schedule.  Reusing the 66 payload paths and counting 76 active loss units gives survival `0.8588264426049117`, erasure `0.1411735573950883`, and unconditional error-or-erasure bound `0.17372822406175498`.

BT1883 updates `tools/apply_bt1857_holonet_patch.py` so it inserts both `BT1857_holonet_k12_compiler_patch.tex` and `BT1880_holonet_finite_css_theorem_patch.tex` before the discussion/open-questions section and writes `papers/BT1347_photonic_holonet_journal_with_BT1857_BT1880.tex`.

Boundary: decoder policy, architecture model, and splice automation only; no threshold, remote build, or physical implementation is claimed.
