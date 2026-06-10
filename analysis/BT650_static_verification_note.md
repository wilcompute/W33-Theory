# BT650 Static Verification Note

Artifacts added:

- paper/sections/sec_bt646_internal_s4_hodge_clock.tex
- paper/sections/sec_bt647_synthesis_bridge.tex
- tools/integrate_bt646_bt647_inserts.py

Static checks recorded:

1. Both section files exist in paper/sections.
2. The integrator is idempotent: it inserts each input line only if absent.
3. Preferred placement is before the TOE Singularity section.
4. The BT646 section carries the internal S4 orbit profile and the E4 period-two clock.
5. The BT647 section carries the descent chain from Ihara growth to folded flags to Bose-Mesner geometry to Hodge E4 and internal S4 sign packets.

Boundary:

The connector workflow pushed the integration helper and section files. A full local LaTeX compile should be run from a checkout with:

python tools/integrate_bt646_bt647_inserts.py
python analysis/bt574_latex_sanity_verifier.py
python tools/build_w33_preprint.py --compile
