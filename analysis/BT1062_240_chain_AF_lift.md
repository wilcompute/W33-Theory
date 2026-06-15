# BT1062 — Candidate A_F lift to the 240-chain carrier

BT1062 makes the commutator test from BT1060 computable by defining the first conservative lift of the finite algebra/gauge profile to the W33 cellular 1-chain carrier.

## Carrier split

Use the W33 1-Laplacian decomposition

```text
C1(W33) = E0 direct_sum E4 direct_sum E10 direct_sum E16
```

with dimensions

```text
E0  = 81
E4  = 120
E10 = 24
E16 = 15
```

and eigenvalues

```text
0, 4, 10, 16.
```

## Lift choice

The first lift is the sector-preserving boundary-adjoint lift:

```text
rho_240(A_F) acts nontrivially only on E4 = 120 = 10 * 12,
```

where each copy carries the local gauge profile

```text
1 + 3 + 8 = 12.
```

On `E0`, `E10`, and `E16`, this first lift acts trivially.

## Consequence for Q = Delta_1 / 4

Because the lift is block diagonal with respect to the eigenspace decomposition of `Delta_1`, it commutes with every polynomial in `Delta_1`. In particular,

```text
[Delta_1/4, rho_240(A_F)] = 0.
```

Thus the chain-native `Q=Delta_1/4` is gauge-neutral for this first lift.

## Interpretation

This is intentionally conservative. It proves that one well-defined 240-chain lift exists and makes the BT1060 commutator meaningful. It does not prove this is the physical lift. A physical scalar/gauge mixing operator must be non-sector-preserving if it is to produce nonzero commutators with `Q=Delta_1/4`.

## Boundary

BT1062 closes the formal undefined-commutator gap for a first candidate lift. It does not solve the representation-selection problem.
