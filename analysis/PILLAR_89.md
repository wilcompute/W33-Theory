# Pillar 89: 270‑Edge Transport Analysis

The 270‑edge transport bundle encodes the action of the five generators on the
27‑point Heisenberg quotient together with affine stabiliser data.  This pillar
collects a few structural observations which will be used repeatedly in the
subsequent tomotope investigations.

## Results

- **Heisenberg coordinates.**  There are exactly 27 distinct triples
  \((x,y,z)\) appearing in the CSV edges; the analysis script records the
  bijection to qids.
- **Affine matrices.**  Only three stabiliser matrices occur in the whole
  transport: the identity, the flip with off‑diagonal 2 and the scalar 2·I.
  Their multiplicities are 108, 54 and 108 respectively.
- **Z‑shift behaviour.**  Generators `g2,g3,g5` have zero shift on both
  coordinates, while `g8` and `g9` shift everything by 2.  These counts are
  summarised per generator for later consistency checks.
- **q_xy consistency.**  A brute‑force scan of the `q_xy` maps exposes six
  mismatches involving generator `g9` acting on the first three qids; the
  script records them for reference.
- **Block guesses.**  The forty‑eight block guesses appearing in the file are
  all listed, with a histogram of occurrences.

The companion script `THEORY_PART_CXCV_270_TRANSPORT.py` performs all
computations and writes a human‑readable report plus a JSON summary.  Utility
tests verify that the summary is JSON‑serialisable and that the basic
distributions have the expected sizes.

The analysis bundle `TOE_270_transport_analysis_v01_20260228_bundle.zip`
contains the original transport bundle along with the summary, report and any
intermediate files.
