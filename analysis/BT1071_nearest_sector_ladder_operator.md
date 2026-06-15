# BT1071 — Nearest-sector ladder operator

BT1071 constructs the abstract nearest-sector ladder from BT1070 and verifies the predicted commutator gaps.

## Sector data

For

```text
Q = Delta_1 / 4,
```

the sector values are

```text
E0  -> 0
E4  -> 1
E10 -> 5/2
E16 -> 4.
```

## Ladder template

Define the nearest-sector ladder

```text
L = X04 + X40 + X4,10 + X10,4 + X10,16 + X16,10
```

where `Xab` maps `Ea` to `Eb`.

## Commutator rule

For a block map `X_lambda,mu`,

```text
[Q, X_lambda,mu] = (mu/4 - lambda/4) X_lambda,mu.
```

Therefore the ladder gaps are

```text
E0  -> E4   :  1
E4  -> E0   : -1
E4  -> E10  :  3/2
E10 -> E4   : -3/2
E10 -> E16 :  3/2
E16 -> E10 : -3/2
```

## Norm reading

If every block is normalized to operator norm one, then

```text
||[Q,L]|| blockwise max = 3/2.
```

If squared Hilbert-Schmidt gap weight is used, the unsigned gap-square sum over the six oriented nearest blocks is

```text
2*(1^2) + 4*(3/2)^2 = 11.
```

## Boundary

BT1071 constructs the abstract block ladder and verifies its gap law. It does not choose concrete matrices inside the rectangular maps between eigenspaces. Those must come from W33 incidence, centralizer, or projector data.
