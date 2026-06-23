# BT1592-BT1594: Lab Tomography, LG Mode Alphabet, and Hesse/T Witness Loop

BT1592 adds the synthetic lab-facing harness for the OAM holonet front end.  It
records a `9x9` sector confusion fixture, radial-shell tomography rows, exact
lane replay acceptance checks, and a CSV ingest path that can be replaced by
real bench measurements.

BT1593 fixes the recenter sector alphabet:

```text
sector_id = 3*x_shift + z_shift
ell       = sector_id - 4
p         = (x_shift + 2*z_shift) mod 3
address   = sector_id*24 + word_index
```

The nine OAM charges are symmetric, `ell=-4..4`, and the radial shells are
balanced three-per-shell.  The existing 24-word centered selector remains a
separate handoff, so the ABI uses `9` physical sector modes plus `24` centered
selector words rather than `216` raw OAM channels.

BT1594 overlays the Hesse/T port directly on the witness loop.  Every BT1590
witness segment is `72` ticks, and every BT1404 Hesse/T microframe is also
`9*8=72` ticks.  Therefore:

```text
1080 witness segments * 72 ticks
= 1080 Hesse/T microframes
= 77760 total ticks.
```

The non-Clifford port is now tested inside the same leakage/covariance witness
loop.  This proves ABI and schedule compatibility, not physical Hesse optics or
a magic-state yield.
