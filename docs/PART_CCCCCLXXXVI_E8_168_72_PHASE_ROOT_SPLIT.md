# Part CCCCCLXXXVI — E8 168+72 Phase/Root Split

Part CCCCCLXXXV found the full coupled phase-superperiod:

```text
period = lcm(4,6,7)=84,
Euler drift = -168.
```

This part connects that phase drift to the 240-dimensional W33/E8 carrier.

## 1. The 240 carrier

The core carrier has size

```text
|E(W33)| = 240,
|Roots(E8)| = 240.
```

The full phase closure contributes the Fano automorphism-order magnitude

```text
168 = |GL(3,2)| = |PSL(2,7)|.
```

The complement in the 240 carrier is

```text
240 - 168 = 72.
```

But `72` is exactly the number of nonzero roots in the E6 root system:

```text
E6 roots = 72,
dim E6 = 72 + 6 = 78.
```

Thus the full carrier admits the arithmetic split

```text
240 = 168 + 72.
```

## 2. Mod-12 form

The same identity is even sharper in the local 12-clock:

```text
168 = 14 * 12,
72  =  6 * 12,
240 = 20 * 12.
```

So the E8/W33 carrier decomposes into

```text
14 local phase-clock sheets + 6 E6-root sheets.
```

This is not a representation-theoretic theorem yet.  It is a strong arithmetic target:

```text
Fano phase curvature sector: 168,
E6 residual root sector:     72.
```

## 3. Interpretation

The phase-superperiod says one full genus clock closure accumulates Euler drift magnitude `168`.

The W33/E8 carrier has 240 edge/root states.  Removing the phase-curvature sector leaves exactly an E6 root shell:

```text
E8 roots = Fano phase-curvature shell + E6 residual roots.
```

This gives a possible bridge between:

```text
Fano / PSL(2,7) phase symmetry,
E6 firewall/root algebra,
E8 240-root carrier,
W33 240-edge carrier.
```

## 4. Relation to previous layers

Previous exact numbers now align:

```text
84  = full phase period,
168 = full Euler drift magnitude and Fano automorphism order,
72  = E6 roots,
240 = W33 edges / E8 roots.
```

The local 12-clock form is

```text
7*12 = 84,
14*12 = 168,
6*12 = 72,
20*12 = 240.
```

So the full phase closure has one 7-color Fano period over the 12-clock, its Euler drift doubles to 14 clock sheets, and the remaining 6 clock sheets match the E6 Cartan rank/root-shell decomposition scale.

## 5. Next executable target

Search the existing edge-to-E8-root artifacts for a 168/72 partition:

1. build or load an edge/root labeling,
2. mark the 168 phase-curvature states by a Fano/phase criterion,
3. test whether the remaining 72 states close under E6 root inner products,
4. check whether the 72 residual states have Cartan rank 6,
5. compare the residual shell to existing E6/firewall artifacts.

The current result is therefore a concrete hypothesis:

```text
The 84/168 genus phase-superperiod may carve the E8/W33 240 carrier into a 168-state Fano phase shell and a 72-root E6 residual shell.
```
