# BT1304-BT1306: Holonet Runtime Physicalization

This packet turns the BT1301-BT1303 holonet stack into a runtime engineering
contract.  The result is deliberately narrow: it proves deterministic
contention, queueing, and symbolic timing facts for the verified finite
architecture, while leaving analog photonic thresholds as separate hardware
work.

## BT1304 - Holonet Contention Model

BT1301 compiles one ingress packet for each of the `540` chart targets.  BT1304
classifies that full-atlas burst as network traffic.

The key distinction is:

- shared micro-op ticks are broadcast control load;
- repeated target charts are output-port contention.

For the verified atlas, every target chart is unique.  Therefore the full
540-chart burst has exactly zero output-port conflicts.  The mirror bus has
four local slots per chart, so the one-packet-per-chart atlas occupies

```text
540 / 2160 = 1/4
```

of the bus.  The remaining `3/4` is not rhetorical slack: it is exactly three
unused mirror slots per chart.

The verified load profile is:

```text
mirror phases:       0,1,2,3 each occur 135 times
active tick counts:  4,5,6,7,8 each occur 108 times
tick load:           540,540,540,540,432,324,216,108
output conflicts:    0
```

Thus the first four ticks are global broadcast ticks used by every chart, while
the later five ticks form the balanced apartment-hop staircase.

## BT1305 - Mirror-Bus Queueing Law

BT1305 promotes the four mirror slots per chart to a deterministic service law:

```text
B_{t+1} = max(0, B_t + arrivals_per_chart - 4).
```

Equivalently, each chart is a four-server queue per mirror epoch.  If `m`
packets target each chart in one epoch, the number of epochs required is
`ceil(m/4)`.

The substrate numbers appear as operating regimes:

```text
m = 1       utilization 1/4    full atlas, no queue
m = q = 3   utilization 3/4    ternary traffic, no queue
m = q+1=4   utilization 1      saturated, still no backlog
m = 5       utilization 5/4    first queueing boundary
m = q^2=9   utilization 9/4    three mirror epochs
```

The recursive scaling is exact.  For

```text
I_n = (40^n - 1) / 39
```

W33 instances, a one-packet-per-chart burst uses `540 I_n` packets against
`2160 I_n` service slots.  Utilization remains `1/4` at every recursive depth,
and the slack is always

```text
1620 per W33 instance.
```

This is the first clean engineering form of the fractal computer/network law:
demand and capacity scale by the same W33 instance count, so local utilization
is depth-invariant.

## BT1306 - Symbolic Physical Timing

BT1306 lowers the 8-tick ISA word into a symbolic optical control schedule.
Let `tau` be one implementation-dependent hardware tick.  Then:

```text
ticks 0..2  ternary XOR axes       tritter/EOM phase-address pulses
ticks 3..7  apartment hops         delay-line switch pulses
```

The frame durations are:

```text
word                 8 tau
tomotope body        48 tau = 6 words
parity epilogue      24 tau = 3 words
microframe           72 tau = 9 words
mirror-bus epoch     2160 tau = 30 frames
Clifford supercycle  51840 tau = 720 frames
```

The six parity windows are the final six frame ticks, lanes `66..71`, one for
each column-pair syndrome `01,02,03,12,13,23`.

## Architecture Reading

BT1304-BT1306 close the runtime layer between abstract W33 routing and physical
photonic control:

```text
chart packet
  -> 8-tick qutrit/apartment word
  -> 48-tick tomotope body
  -> 24-tick parity epilogue
  -> 72-tick oscillator microframe
  -> 2160-slot mirror bus
  -> 51840-tick Clifford supercycle
```

The computer and the network are the same object at different scales.  At one
W33 shell, the architecture routes 540 chart packets into a four-slot local
mirror bus with no output contention.  At recursive depth `n`, the same local
law repeats across `I_n` W33 instances.  The full machine therefore scales like
a fractal packet network whose utilization is an invariant of the local W33
ABI, not a parameter tuned at higher levels.

## Honesty Boundary

The packet does not claim an optical clock speed, a loss budget, a detector
jitter tolerance, a squeezing threshold, or an integrated-photonics fabrication
margin.  It supplies the finite deterministic runtime contract those hardware
numbers must instantiate.
