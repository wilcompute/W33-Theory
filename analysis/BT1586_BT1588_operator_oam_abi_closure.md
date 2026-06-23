# BT1586-BT1588: Operator/OAM ABI Closure

## BT1586

The operator/OAM appendix is now spliced into `photonic_holonet.tex` by a bounded,
idempotent block before the bibliography.  The block imports BT1564-BT1576,
BT1580-BT1585, the BT1586-BT1588 synthesis insert, and subsequent operator/OAM
appendix inserts.

## BT1587

The 216 internal Clifford/OAM actions are nine affine recentering shifts over
the 24 centered BT1495 transaction words:

```text
216 = 9 * 24 = (1 + 2 + 2 + 4) * 24.
```

The class counts are `24,48,48,96` for centered, OAM-only, phase-only, and mixed
shifts.  One operation sweep costs `216*72=15552` ticks; the five-gate
`I,X,Z,F3,S` witness sweep costs `77760` ticks.

## BT1588

External OAM and time-bin papers are retained as literature motivation and
guardrails only.  The exact promoted claim is local: the finite recenter ABI and
claim ledger, not calibrated optical loss or measured leakage.
