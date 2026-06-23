# BT1648-BT1650 Fano Time-Bin Guard Closure

BT1648 exposes the charge law hidden inside the `80x9 + 88x10` detector usage
profile:

```text
80*9 + 40*(9+1) + 48*10 = 1600
5*(16*9 + 8*10) + 2*(24*10) = 1600
```

The `88` high-usage bins are exactly the `40` same-ray anchors plus the `48`
compatible-control reserve bins.

BT1649 embeds the `1600` active Witting frames in an `11`-bit single-photon
time-bin envelope:

```text
2^11 = 2048
2048 - 1600 = 448 = 7*64
```

The slack is not waste.  It is seven Fano guard pages.

BT1650 assigns every guard page as:

```text
24 dark-reference guards
24 loss-probe guards
16 parity-overflow guards
```

So every active detector bin gets one dark-reference guard and one loss-probe
guard, while the remaining `112` guards feed the CSS/jitter side of the fault
ABI.
