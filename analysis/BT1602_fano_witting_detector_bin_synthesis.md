# BT1602 Fano/Witting Detector-Bin Synthesis

BT1602 identifies the `168` active detector bins with a Fano/Witting runtime bus:

```text
168 = 7 Fano lines * 3 point slots * 8 D4 states = 7*24
40 Witting sources = 5 witness gates * 8 D4 states
27 fuel targets = 3 point slots * 9 Hesse/OAM residues
12 compatible controls = 2 reserve lines * 3 point slots * 2 parities
```

All `168` bins are used.  The total usage profile is `80` bins used `9` times and `88` bins used `10` times across the `1600` frames.
