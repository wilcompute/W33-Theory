# BT1301-BT1303 - Holonet Architecture Stack

## Summary

BT1300 made the oscillator microframe executable:

```text
72 = 48 + 18 + 6
```

BT1301-BT1303 push that into a real computer/network architecture:

```text
BT1301  full 540-chart atlas compiles into the 8-tick word
BT1302  six parity epilogue lanes become a live reroute protocol
BT1303  the holonet becomes a finite stack machine
```

The result is not only a collection of compatible counts.  It is a packet
machine with a route word, packet body, parity trailer, bus epoch, supercycle,
and fractal scaling law.

## BT1301: Full Chart-Atlas ISA Compiler

For every chart in the 540-chart atlas, there are five canonical ingress
candidates:

```text
target digits = 7, 15, 23, 31, 39.
```

Each has the same low three-bit mask:

```text
111
```

so every atlas route activates all three ternary XOR axes.  The five candidates
carry apartment-hop costs:

```text
1, 2, 3, 4, 5.
```

This is true chart-by-chart, not only in aggregate.  Choosing candidate
`chart mod 5` gives a balanced full-atlas schedule:

```text
540 chart routes
all 540 target charts covered exactly once
all routes activate XOR axes [0,1,2]
active tick counts 4,5,6,7,8 occur 108 times each
apartment-hop counts 1,2,3,4,5 occur 108 times each
target digits 7,15,23,31,39 occur 108 times each
```

So the 8-tick word is not a sample-program artifact.  It compiles the complete
chart atlas while exercising the whole micro-op budget.

## BT1302: Parity Epilogue Reroute Protocol

The six parity lanes in BT1300 are exactly the six column pairs of the 4-column
CSS sheet:

```text
01, 02, 03, 12, 13, 23.
```

BT1302 uses those six lanes as active syndrome controls.  For each chart and
each failed column-pair syndrome, it chooses a route whose own column-pair
carrier avoids that failed pair:

```text
540 charts * 6 parity lanes = 3240 recovery actions.
```

The recovery rule is simple:

```text
if the base route does not use the failed pair:
    keep the packet
else:
    switch to the lowest-cost all-XOR candidate for the same chart
    whose carrier uses a different column pair
```

Every recovery action fits inside one 8-tick word.  Exactly one failed lane per
chart forces a route change, so there are:

```text
540 changed recovery actions
2700 keep-route actions
```

This converts the final six parity lanes from passive checks into a live,
deterministic self-healing route selector.

## BT1303: Holonet Stack Contract

The complete stack is:

```text
L0  carrier              1      one self-entangled qutrit photon
L1  micro-op word         8      3 ternary XOR + 5 apartment-hop ticks
L2  atlas ingress       540      one compiled ingress word per chart
L3  tomotope body        48      6 route words
L4  parity epilogue      24      18 residual payload + 6 parity lanes
L5  microframe           72      [72,66]_3 instruction frame
L6  mirror bus         2160      30 frames = 540 charts * 4 slots
L7  Clifford cycle    51840      24 mirror epochs = 720 frames
L8  fractal shell      40^n      route bound 8n
```

The exact handoffs are:

```text
8      = 2^q
48     = q! * 2^q
24     = q  * 2^q = 18 + 6
72     = q^2 * 2^q = 48 + 24
2160   = 30 * 72 = 540 * 4
51840  = 24 * 2160 = 720 * 72
```

Fractal routing locks to the same stack:

```text
level n route bound = 8n
level 6 fills the 48-tick tomotope body
level 9 fills the 72-tick oscillator microframe
```

## Architectural Reading

The holonet is now a stack machine.

The single carrier executes 8-tick route words.  Six words form the tomotope
packet body.  Three more words close the local-lift parity epilogue.  Thirty
frames form the D12 mirror-bus epoch.  Twenty-four bus epochs form the full
two-qutrit Clifford supercycle.  Recursive W33 shells scale routing as `8n`.

In computer-engineering language:

```text
carrier      = physical layer
8-tick word  = instruction layer
48 body      = packet layer
24 epilogue  = recovery/trailer layer
2160 bus     = switching fabric
51840 cycle  = universal control plane
40^n shell   = fractal network layer
```

The same object is simultaneously a computer and a network.

## Verification

```text
python3 analysis/bt1301_full_chart_atlas_isa_compiler.py
python3 analysis/bt1302_parity_epilogue_reroute_protocol.py
python3 analysis/bt1303_holonet_stack_contract.py
python3 tests/test_bt1301_bt1303_holonet_architecture_stack.py
python3 -m py_compile analysis/bt1301_full_chart_atlas_isa_compiler.py analysis/bt1302_parity_epilogue_reroute_protocol.py analysis/bt1303_holonet_stack_contract.py tests/test_bt1301_bt1303_holonet_architecture_stack.py
python3 -m json.tool data/bt1301_full_chart_atlas_isa_compiler.json
python3 -m json.tool data/bt1302_parity_epilogue_reroute_protocol.json
python3 -m json.tool data/bt1303_holonet_stack_contract.json
```

## Boundary

BT1301-BT1303 prove deterministic finite routing and stack contracts.  They do
not yet model simultaneous traffic contention, stochastic noise, finite-squeeze
GKP errors, hardware loss, or queueing under many concurrent packets.
