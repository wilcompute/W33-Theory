# BT1313-BT1315: Holonet Optimality, Stability, and Physical Budget Interface

BT1310-BT1312 gave the holonet a deterministic network-control layer.  This
packet strengthens that layer in three directions:

1. BT1313 proves exact lower bounds that the entropy router saturates;
2. BT1314 stress-tests raw traffic versus routed traffic under a deterministic
   pseudo-random source;
3. BT1315 converts symbolic pulse counts into a parametric physical-resource
   ledger without inventing lab constants.

## BT1313 - Entropy-Router Optimality

The mirror bus has

```text
540 charts * 4 slots/chart = 2160 slots.
```

For a one-hot burst of `N` packets aimed at one chart, any one-epoch cyclic
nonnegative router must use at least

```text
ceil(N/4)
```

charts, because each chart carries at most four packets.  Therefore its maximum
cyclic displacement must be at least

```text
ceil(N/4) - 1.
```

The BT1310 cyclic router saturates those bounds.  For the hard BT1308 collapse:

```text
N = 540
minimum nonempty charts     = ceil(540/4) = 135
minimum max displacement    = 134
minimum mean displacement   = 67
BT1310 achieved             = 135 charts, max 134, mean 67
```

At the full one-hot capacity boundary:

```text
N = 2160
minimum nonempty charts  = 540
minimum max displacement = 539
minimum mean displacement= 539/2
```

The over-capacity case is also tight:

```text
2700 requests = 5 packets/chart
one-epoch capacity = 2160
minimum rejection = 540
BT1310 rejection  = 540
```

So the router is not just a working fix.  In the finite mirror-slot model, it
hits the exact chart-count, displacement-span, and admission lower bounds on
the certified hot-spot cases.

## BT1314 - Deterministic Traffic Stability

BT1314 uses a deterministic LCG source modulo `540` charts, with `60 = 540/9`
trials per case.  This is not a claim about real deployment traffic; it is a
reproducible stress harness.

The raw per-chart service law creates backlog even when global utilization is
low.  For `540` packets, only `1/4` global utilization, the raw harness has:

```text
mean backlog after one epoch = 2.716666...
max backlog after one epoch  = 9
mean hot charts              = 2.266666...
```

For `1620` packets, the ternary `3/4` load:

```text
mean backlog after one epoch = 168.5
max backlog after one epoch  = 187
mean hot charts              = 97.266666...
```

For full `2160`-packet utilization:

```text
mean backlog after one epoch = 420.5
max backlog after one epoch  = 457
mean hot charts              = 199.166666...
```

The BT1310 router removes this backlog completely for every admitted burst:

```text
540 packets   -> accepted 540, rejected 0, backlog 0
1620 packets  -> accepted 1620, rejected 0, backlog 0
2160 packets  -> accepted 2160, rejected 0, backlog 0
2700 packets  -> accepted 2160, rejected 540, backlog 0
```

This is the practical reason the entropy router is part of the architecture.
Global utilization is not enough.  The machine needs a layer that actively
turns address entropy into local service stability.

## BT1315 - Parametric Photonic Loss Budget

BT1309 and BT1312 fixed the pulse counts:

```text
qutrit-axis pulses = 1620 I_n
delay-hop pulses   = 1620 I_n
idle windows       = 1080 I_n
detector windows   = 540 I_n
mirror slots       = 2160 I_n
I_n                = (40^n - 1)/39
```

BT1315 keeps device physics honest by leaving the calibrated costs as
parameters:

```text
C_n = 1620 I_n e_q + 1620 I_n e_d + 1080 I_n e_idle.
```

Here `e_q` is the cost per qutrit-axis pulse, `e_d` is the cost per delay-hop
pulse, and `e_idle` is the cost per idle window.  The substrate fixes the
multiplicities; the lab supplies the constants.

Three exact scenario rows are verified:

```text
equal active pulse cost:
  C_1 = 3240, qutrit share = 1/2, delay share = 1/2

delay double cost:
  C_1 = 4860, qutrit share = 1/3, delay share = 2/3

equal active plus idle tenth:
  C_1 = 3348, qutrit share = 15/31, delay share = 15/31, idle share = 1/31
```

At depth 6:

```text
I_6                  = 105025641
detector windows     = 56713846140
mirror slots         = 226855384560
equal active cost    = 340283076840
```

The detector-to-mirror ratio remains

```text
540 I_n / 2160 I_n = 1/4
```

at every depth.

## Architecture Reading

BT1313-BT1315 close the first engineering loop:

- BT1313 gives the lower-bound certificate;
- BT1314 gives the stability reason the router is required;
- BT1315 gives the lab-facing cost interface.

The result is not merely a mathematical routing toy.  It is a finite
network-computer contract:

```text
exact slot capacity -> entropy router -> deterministic admission -> recursive ABI
                    -> parametric physical budget
```

The remaining physical work is now well-posed.  Measure or choose the actual
device constants `e_q`, `e_d`, `e_idle`, detector efficiency, optical loss, and
clock rate, then plug them into the substrate-fixed multiplicities.
