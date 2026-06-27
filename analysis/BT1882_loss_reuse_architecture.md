# BT1882 — Loss-Reuse Architecture

BT1882 rewrites the BT1876 measurement schedule to reuse the 66 payload paths across the five syndrome rounds.

## Goal

BT1879 showed the conservative 122-resource pass is loss-heavy:

```text
survival = 0.7832962313857886
erasure = 0.21670376861421137
```

The ancilla-only ideal is better:

```text
survival = 0.8939439964545421
erasure = 0.10605600354545786
```

BT1882 targets the middle: payload reuse plus explicit switching overhead.

## Architecture

```text
payload paths = 66, prepared once
check ancillas = 56
rounds = 5
edge/check touches = 264
switching layers = 5
memory delays = 4
```

Schedule:

```text
1. prepare 66 payload paths once
2. round X0: measure 16 Reye faces
3. rounds X1/X2: measure residual face halves
4. rounds Z0/Z1: measure even/odd vertex stars
5. reset check ancillas and switch fabric; reuse payload path phases
```

## Budget with switching overhead

Modeled active loss units:

```text
76 = 56 check ancillas + 20 switching/memory overhead units
```

Result:

```text
survival = 0.8588264426049117
erasure = 0.1411735573950883
unconditional error-or-erasure bound = 0.17372822406175498
```

Improvement against conservative BT1879:

```text
survival gain = 0.0755302112191231
erasure reduction = 0.07553021121912308
bound reduction = 0.07553021121912306
```

## Hardware priority

```text
1. low-loss switch fabric
2. phase-stable payload memory across five rounds
3. ancilla detector reset
4. shared F12 edge-address bus
```

Boundary: architecture/budget model only; not a calibrated threshold or detailed optical layout.
