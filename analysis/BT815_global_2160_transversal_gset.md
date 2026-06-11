# BT815 — Global 2160 Chart-Transversal G-Set

BT801 counted:

```text
540 skew-line charts * 4 common transversals = 2160 slots.
```

BT815 identifies the actual G-set.  The map

```text
(chart, common transversal line)
  -> (chart, base antipode pair cut out by that transversal)
```

is a `PSp(4,3)`-equivariant bijection from the chart-transversal slots to the
BT778 antipode-slot space.

## Stabilizer

For a base slot, the stabilizer has order `12` and element-order profile:

```text
{1: 1, 2: 7, 3: 2, 6: 2}
```

GAP identifies the stabilizer as:

```text
D12
```

and confirms it is not cyclic `C12`.  Therefore the `2160` chart-transversal
space is the mirror/antipode `2160` space, not the cyclic rectangle-clock
`2160` space.

## Consequences

The same carrier now has four equivalent readings:

```text
2160 = 540 * 4   chart-transversal slots
2160 = 40 * 54   each W33 line appears in 54 slots
2160 = 240 * 9   BT778 antipode slots
2160 = 45 * 48   polar-pair geography times chart group order
```

So BT801’s global repair atlas is tied to the completed BT810-BT813 Schlaefli
geography: it sits below the chart `O_h` group and lands on the D12 antipode
side of the `2160` boundary.

## Boundary

The existing Witting packet audit also records `2160` transposition holonomies.
BT815 records this as a matching cardinal layer, but does not assert a Witting
G-set isomorphism without a shared stabilizer/transport map.

## Validation

Run:

```bash
python3 analysis/bt815_global_2160_transversal_gset.py
```
