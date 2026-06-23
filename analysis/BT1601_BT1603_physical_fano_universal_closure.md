# BT1601-BT1603 Physical Fano Universal Closure

BT1601 compiles the full Witting transaction cycle into one single-photon
physical automaton.  The automaton has `1600` states and `115200` ticks.  Every
state carries an explicit switch bank, delay placeholder, detector handoff,
symbolic loss channel, and dark-reference placeholder.

BT1602 attacks the `168` active detector-bin clue directly:

```text
168 = 7 Fano lines * 3 point slots * 8 D4 states = 7*24
40 Witting sources = 5 witness gates * 8 D4 states
27 fuel targets = 3 point slots * 9 Hesse/OAM residues
12 compatible controls = 2 reserve lines * 3 point slots * 2 parities
```

The five Witting witness gates occupy five Fano lines for contextual fuel.  The
two remaining Fano lines carry compatible controls.  The same-ray controls
anchor one gate-line bin per source.  Across all `1600` frames, every one of the
`168` active detector bins is used; `80` bins are used `9` times and `88` bins
are used `10` times.

BT1603 packages the closure as a theorem-level ABI statement: accepted Witting
frames carry Clifford transport, rejected Witting frames carry contextual fuel,
BT1594 supplies the Hesse/T non-Clifford port, and BT1486/BT1493 provide the
retwined CSS syndrome handoff.  The theorem is intentionally finite and
interface-level.  It does not claim a hardware threshold, calibrated loss,
detector efficiency, or magic-state yield.
