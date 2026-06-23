# BT1595-BT1597: Deep Witting Fuel Object

BT1595 identifies the full OAM/Hesse witness loop with the Witting incompatible
ordered-pair shell:

```text
40 Witting source rays * 27 incompatible targets = 1080 reject pairs
5 witness gates * 9 OAM sectors * 24 selector words = 1080 fuel segments
1080 * 72 ticks = 77760 ticks
```

Per gate, the identity refines to:

```text
9 * 24 = 216 = 8 Witting source rays * 27 incompatible targets.
```

BT1596 then writes the runtime economy:

```text
520 accepted Witting pairs * 72 ticks = 37440 communication/control ticks
1080 rejected Witting pairs * 72 ticks = 77760 contextual-fuel ticks
1600 total Witting pairs * 72 ticks = 115200 transaction-cycle ticks
accepted:fuel = 13:27
```

BT1597 packages the result as a universal transaction object.  Accepted Witting
pairs are the communication/control rail.  Rejected Witting pairs are exactly the
OAM/Hesse contextual-fuel rail.  The Hesse/T overlay supplies the required
non-Clifford boundary, so the current architecture is no longer just a local
witness loop: it is the fuel sector of the full Witting delayed-query desk.
