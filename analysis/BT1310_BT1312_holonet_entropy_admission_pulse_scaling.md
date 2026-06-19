# BT1310-BT1312: Holonet Entropy, Admission, and Recursive Pulse Scaling

BT1307-BT1309 exposed the runtime problem: global utilization alone cannot
guarantee low latency.  A balanced `540`-packet atlas burst finishes in one
epoch, while the same `540` packets aimed at one chart require `135` epochs.

This packet adds the missing network-control layer:

1. a deterministic entropy-preserving router that repairs hot spots;
2. an exact admission-control boundary at `2160` packets per W33 instance;
3. a recursive pulse-scaling law showing that shell growth preserves the
   balanced control vector.

## BT1310 - Entropy-Preserving Mirror Router

The mirror atlas has

```text
540 charts * 4 mirror slots per chart = 2160 slots.
```

BT1310 routes a burst by a simple cyclic rule:

```text
For each requested chart c, place the packet in the first chart c+d
whose local load is still below 4.
```

The rule has two important properties.

First, it preserves already-balanced traffic exactly:

```text
balanced atlas:       540 packets, zero displacement, max load 1
q per chart:         1620 packets, zero displacement, max load 3
saturated q+1:       2160 packets, zero displacement, max load 4
```

Second, it repairs the BT1308 adversarial hot spot:

```text
all-to-one 540-packet burst:
  before BT1310: one chart overloaded, 135 epochs
  after BT1310:  135 charts at load 4, one epoch
```

The router is therefore entropy preserving in the precise operational sense:
if the input already carries chart entropy, it does not disturb it; if the
input collapses onto a hot chart, it injects the minimum cyclic spread needed
to stay under the four-slot service law.

The capacity boundary remains honest:

```text
5 packets per chart = 2700 requests
2160 admitted, 540 rejected
```

The router never claims to fit more than the physical mirror-slot count.

## BT1311 - Mirror Admission Control

BT1311 promotes the BT1310 capacity into an admission controller:

```text
admitted_per_epoch = min(backlog + arrivals, 2160)
spill              = max(0, backlog + arrivals - 2160)
epochs_needed      = ceil(total_packets / 2160)
```

For one W33 instance the key cases are:

```text
540 packets   -> 1/4 utilization, no spill
1620 packets  -> 3/4 utilization, no spill
2160 packets  -> full epoch, no spill
2700 packets  -> full epoch, 540-packet spill
4321 packets  -> three epochs, final epoch has one packet
```

BT1311 also separates two different scaling questions that should not be
confused.

If all depth-6 instances were serialized through one bus, the one-packet-per
chart shell wave would contain

```text
I_6 * 540 = 105025641 * 540 = 56713846140 packets,
```

which would require

```text
ceil(56713846140 / 2160) = 26256411
```

epochs on a single bus.

But the recursive holonet is not a single bus.  With `I_n` W33 instances the
parallel capacity is

```text
2160 I_n packets per epoch.
```

So the same one-packet-per-chart wave at depth 6 uses

```text
(540 I_6) / (2160 I_6) = 1/4
```

of the parallel shell capacity and is admitted in one epoch.  That distinction
is the architecture: recursion multiplies both demand and service, instead of
forcing all shells through one bottleneck.

## BT1312 - Recursive Pulse-Energy Scaling

BT1309 proved the full atlas active pulse vector is balanced:

```text
qutrit-axis pulses = 1620
delay-hop pulses   = 1620
```

BT1312 proves this is a recursive ABI.  With

```text
I_n = (40^n - 1) / 39
```

W33 instances at depth `n`, the active pulse vector is

```text
(1620 I_n, 1620 I_n).
```

The reserved and idle windows scale with the same instance count:

```text
active pulses   = 3240 I_n
idle windows    = 1080 I_n
reserved windows= 4320 I_n
```

Therefore every depth keeps the same utilization law:

```text
active/reserved = 3/4
idle/reserved   = 1/4
qutrit/delay    = 1/1
```

At depth 6 the verified row is:

```text
I_6                 = 105025641
qutrit-axis pulses  = 170141538420
delay-hop pulses    = 170141538420
active pulses       = 340283076840
idle windows        = 113427692280
reserved windows    = 453710769120
```

## Architecture Reading

BT1310-BT1312 turn the holonet from a route compiler into a network computer.

The architecture now has three finite control laws:

- routing law: preserve chart entropy and repair hot spots by cyclic spreading;
- admission law: accept at most `2160` packets per W33 instance per epoch;
- scaling law: multiply the balanced pulse vector by `I_n` without changing
  the `3/4` compute and `1/4` transport split.

This is the clean network-engineering meaning of the fractal holonet.  Each
W33 cell is a deterministic router-computer with a four-slot mirror output
port.  Larger shells are not faster because they ignore the boundary; they are
faster because the boundary is copied at every cell, so capacity scales with
geometry.

The honesty boundary is also explicit.  These results count exact symbolic
slots, queue epochs, and control pulses.  They do not claim a physical optical
loss budget, thermal budget, stochastic traffic QoS policy, or measured device
clock rate.
