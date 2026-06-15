# BT1060 — Chain-native Q sanity checks

BT1060 tests what the chain-native scalar-slot operator

```text
Q = Delta_1 / 4
```

can honestly say.

## Exact facts

Because `Q` is a polynomial in `Delta_1`, it commutes with

```text
Delta_1
P_0, P_4, P_10, P_16
```

where `P_lambda` are the spectral projectors of the W33 cellular 1-Laplacian.

Its sector eigenvalues are

```text
0, 1, 5/2, 4
```

on dimensions

```text
81, 120, 24, 15.
```

## Consequence for BT1054

The projection averages are immediate:

```text
A_lambda = lambda/4
```

so BT1056 is internally consistent.

## Gauge-block sanity boundary

The current BT1038 finite algebra blocks act on the 162 Hilbert-Schmidt carrier, while `Q=Delta_1/4` is defined on the 240 cellular chain carrier. Therefore the commutator

```text
[Q, rho(A_F)]
```

is not yet a well-defined single-space matrix computation.

## Possible outcomes once a 240-carrier algebra action is chosen

1. If `rho(A_F)` preserves every eigenspace of `Delta_1`, then `[Q,rho(A_F)] = 0` and Q is gauge-neutral.
2. If `rho(A_F)` mixes eigensectors, then `[Q,rho(A_F)]` measures exactly which sectors are coupled by the scalar slot.
3. Either case is useful, but neither can be asserted before the 240-carrier action is constructed.

## Verdict

`Q=Delta_1/4` is an excellent chain-native test operator and a valid BT1054 amplitude source. It is not yet a physical scalar operator and cannot be tested against finite algebra blocks until the algebra action is lifted to the 240-chain carrier.
