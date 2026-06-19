# BT1307-BT1309: Holonet Latency, Collision, and Pulse Budget

This packet takes the BT1304-BT1306 runtime contract one layer closer to an
engineering architecture.  It proves three facts:

1. the full atlas has five exact latency classes and a dual utilization law;
2. global bus utilization is not enough to guarantee low latency;
3. the active photonic pulse budget balances qutrit-axis and delay-hop controls.

## BT1307 - Latency Classes

Every BT1301 atlas route is an 8-tick word.  The completion tick is the final
active tick plus one.  Across all `540` chart routes, the completion profile is

```text
4 tau : 108 routes
5 tau : 108 routes
6 tau : 108 routes
7 tau : 108 routes
8 tau : 108 routes
```

The mean completion time is therefore `6 tau`.  Total active route ticks are

```text
108(4+5+6+7+8) = 3240,
```

inside a reserved word budget of

```text
540 * 8 = 4320.
```

So the full-atlas route word is `3240/4320 = 3/4` active and `1/4` idle.

BT1304 proved that the same burst uses only `540/2160 = 1/4` of the mirror
transport bus.  Therefore the runtime has a dual utilization identity:

```text
3/4 compute + 1/4 mirror = 1.
```

The architecture is compute-dense locally and transport-sparse globally.

## BT1308 - Collision Stress

BT1305's queue law is local:

```text
service capacity = 4 packets per chart per mirror epoch.
```

BT1308 stress-tests this with adversarial traffic.  The important negative
result is that global utilization does not determine latency.

Two bursts can both contain `540` packets, so both use `1/4` of the global bus:

```text
balanced atlas:  1 packet on each of 540 charts -> 1 epoch
all-to-one:      540 packets on one chart       -> 135 epochs
```

Even a tiny hot spot matters.  A burst with one packet on every chart plus four
extra packets aimed at a single chart has only

```text
544 / 2160 = 34/135
```

global utilization, still barely above one quarter, but it already creates
backlog because one chart receives five packets.

The design rule is therefore exact: the holonet must preserve chart entropy.
Balanced address spread is not cosmetic symmetry; it is the condition that
keeps the mirror bus low-latency.

## BT1309 - Photonic Pulse Budget

BT1306 lowered one route digit to a symbolic hardware word:

```text
3 qutrit-axis windows + 5 delay-hop windows = 8 ticks.
```

That is the scheduled word shape.  But the full atlas activates the two
physical control families in exact balance:

```text
qutrit-axis pulses = 540 * 3 = 1620,
delay-hop pulses   = 108(1+2+3+4+5) = 1620.
```

The active pulse ratio is therefore

```text
1620 : 1620 = 1 : 1.
```

This happens because the balanced atlas makes the mean apartment-hop count
equal to `q=3`, exactly matching the three qutrit axes.

The scheduled hierarchy remains:

```text
word                 3 + 5       = 8
tomotope body        18 + 30     = 48
parity epilogue      9 + 15      = 24
microframe           27 + 45     = 72
mirror epoch         810 + 1350  = 2160
Clifford supercycle  19440+32400 = 51840
```

The six parity lanes use one qutrit-axis window and five delay-hop windows.

## Architecture Reading

BT1307-BT1309 sharpen the holonet as a practical network computer:

- local route execution is dense: `3/4` of reserved route ticks are active;
- global mirror transport is sparse: `1/4` of mirror capacity is used by a full atlas;
- low latency depends on chart-entropy preservation, not global packet averages;
- the physical control burden balances across qutrit-axis and delay-hop families.

This is not yet a photonic device budget in seconds, decibels, or loss per
component.  It is the finite, deterministic pulse-count and queueing contract
that the optical hardware must realize.
