# BT832-BT834 Holonet Runtime Extensions

## Summary

BT828-BT831 closed the first executable holonet runtime:

```text
address word -> packet route -> sentinel monitor -> durable tomotope commit
```

BT832-BT834 make the tomotope cover boundary operational rather than only
descriptive.

## BT832 - Cover-Indexed Durable Storage

The BT814 tomotope middle layer is the stable local ABI: 48 packet blocks and
192 flags.  The global regular cover is not unique, so durable storage must not
pretend that there is one canonical cover backend.

For cover index `k`, the storage fiber is:

```text
base ABI block in {0,...,47}
cover coordinate in Z_k^3
```

so the lifted durable packet space has `48*k^3` slots and kernel order
`k^6 = (k^3)^2` over the base ABI.  Tested indices `3, 5, 7, 11, 13` all
reduce exactly to the same base packet program.

## BT833 - Sentinel-Aware Packet Rerouting

BT829 gave an exact `g=15` sentinel projector.  BT833 uses it as a compiler
cost function.  Each digit route may insert up to two W33 waypoint points,
minimizing sentinel energy first and reversible move count second.

The extra moves are not charged to the fast BT827 route bound.  They are paid
inside the slower BT830 durable commit phase.  In the level-six stress program:

```text
direct route:   47 moves, sentinel energy 4
rerouted path:  58 moves, sentinel energy 2
commit window:  470592 ticks
```

The compiler can therefore spend commit-time slack to lower off-context fault
activation.

## BT834 - Desync Guard-Band Arithmetic

The full route-epoch sync condition is:

```text
8n | T(n) = 4(7^n - 1)
```

equivalently:

```text
2n | 7^n - 1
```

For odd prime powers `p^a | n`, `p != 7`, synchronization requires
`ord_{p^a}(7) | n`; if `7 | n`, sync is impossible.  The first failure is:

```text
n = 5
ord_5(7) = 4 does not divide 5
T(5) mod 40 = 24 = f
```

So `n=5` is the first true guard band: the durable tomotope clock and the full
route epoch separate by exactly the local runtime lift size `f=24`.

## Top 3 Next Moves

1. Interpret the `Z_k^3` cover coordinate as a three-axis durable-storage
   namespace: route epoch, mirror sheet, and tomotope face/edge parity.
2. Generalize BT833 from per-digit waypoints to a dynamic-programming route
   optimizer over the 540-chart apartment graph.
3. Lift BT834 from arithmetic levels to actual cover-family selection: decide
   which `k` families are operationally safe, guarded, or forbidden.
