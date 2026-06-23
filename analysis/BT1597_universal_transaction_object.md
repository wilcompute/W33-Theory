# BT1597 Universal Transaction Object

BT1597 packages the current architecture as one finite transaction object:

```text
40 Witting rays * 40 queried rays * 72 ticks = 115200 ticks
520 accepted pairs * 72 ticks = 37440 communication/control ticks
1080 rejected pairs * 72 ticks = 77760 contextual-fuel ticks
1080 = 5*9*24 = 40*27
```

The rejected rail is exactly the OAM/Hesse witness loop, and the Hesse/T overlay supplies the explicit non-Clifford port required by BT1377.
