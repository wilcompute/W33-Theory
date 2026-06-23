# BT1650 Fano Guard-Page Calibration Closure

BT1650 assigns every one of the `448 = 7*64` time-bin guard addresses:

```text
per Fano point: 24 dark-reference guards
              + 24 loss-probe guards
              + 16 parity-overflow guards
```

The dark and loss guard sets each cover all `168` active detector bins once. The parity guards supply `7*16=112` CSS/jitter overflow slots.
