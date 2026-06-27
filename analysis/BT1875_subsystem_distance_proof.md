# BT1875 — All-Weight Subsystem Distance Proof

BT1875 proves the subsystem distance claim left open in BT1873 for the chosen finite symplectic gauge-pair model.

## Parent

BT1872 gives the stabilizer parent:

```text
[[66,13,3]]_3
```

with primal triangular `X` checks and signed dual vertex-star `Z` checks.

## Subsystem candidate

BT1873 adds five canonical gauge pairs from the five distance-contrast directions:

```text
n = 66
parent k = 13
gauge qudits r = 5
logical k = 8
```

## Distance proof

For distance 3, it is enough to prove two statements:

```text
1. no dressed logical exists at weight 1 or 2
2. some dressed logical exists at weight 3
```

The BT1872 parent has no weight-1 or weight-2 logicals.  Adding gauge-pair commutation constraints shrinks the logical centralizer, so it cannot create a new lower-weight logical.

A surviving weight-3 dressed logical is:

```text
edge(0,1) + 2*edge(0,3) + edge(1,3)
```

It survives the five-gauge quotient and is not in the gauge group.

## Result

```text
[[66,8,3;5]]_3
```

in the finite symplectic matrix model.

## Boundary

This is an exact finite matrix-code statement for the chosen gauge-pair construction.  It is not yet an optical decoder, hardware threshold, or physical measurement proof.
