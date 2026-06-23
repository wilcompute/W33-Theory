# BT1649 Time-Bin Qudit Envelope

BT1649 embeds the `1600` Witting transaction frames into an `11`-bit single-photon time-bin envelope:

```text
2^11 = 2048 time bins
2048 - 1600 = 448 = 7*64 guard bins
per Fano point: 24 dark references + 24 loss probes + 16 parity overflow
```
