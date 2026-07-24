# BT796 — Global 2160 Chart-Transversal Fibration

A local slot is:

```text
(skew chart, common isotropic transversal)
```

Since W33 has 540 skew charts and BT794 proves four common transversals per
chart:

```text
540 * 4 = 2160 slots
```

The PSp(4,3) action is transitive on this slot set.  The stabilizer of one slot
has order 12 and order profile:

```text
{1:1, 2:7, 3:2, 6:2}
```

So orbit-stabilizer gives:

```text
25920 = 2160 * 12
```

Line multiplicity is also uniform:

```text
each W33 line appears as a transversal in 54 slots
40 * 54 = 2160
```

This proves that the 2160 chart-transversal slots form a real G-set/fibration
object, not just a count.  It can now be compared objectwise against the other
2160 spaces in the repo, especially rectangle, antipode, and Witting holonomy
slots.
