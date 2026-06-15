# BT1067 — Non-sector-preserving lift templates

BT1067 tests how to get nonzero scalar/gauge commutators after BT1062.

## Setup

For the chain-native operator

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

A sector-preserving lift commutes with `Q`. Therefore a physically informative lift must include off-diagonal maps between eigensectors.

## General rule

Let `X_{lambda,mu}` map `E_lambda` to `E_mu`. Then

```text
[Q, X_{lambda,mu}] = (mu/4 - lambda/4) X_{lambda,mu}.
```

So the commutator is controlled exactly by the spectral gap.

## Gap table

| map | gap |
| --- | ---: |
| E0 <-> E4 | 1 |
| E4 <-> E10 | 3/2 |
| E10 <-> E16 | 3/2 |
| E0 <-> E10 | 5/2 |
| E4 <-> E16 | 3 |
| E0 <-> E16 | 4 |

## Candidate lift templates

1. **Nearest-sector ladder**

```text
E0 <-> E4 <-> E10 <-> E16
```

This minimizes spectral jumps and gives gaps `1, 3/2, 3/2`.

2. **Physical/complement mixing**

```text
P96 <-> P66
```

This directly targets the BT1065 physical/complement split once `P96` is constructed.

3. **Boundary-heavy mixing**

```text
E4 <-> E10 and E4 <-> E16
```

This keeps the local-boundary gauge carrier active while coupling to heavy correction sectors.

## Reading

BT1062's sector-preserving lift was gauge-neutral for `Q=Delta_1/4`. BT1067 shows the exact mechanism for making commutators nonzero: introduce controlled off-diagonal sector maps. The commutator magnitude is then not arbitrary; it is fixed by the W33 spectral gaps.

## Boundary

BT1067 supplies lift templates and commutator laws. It does not choose the physical off-diagonal matrices. Those must be derived from the W33 centralizer, generation/fiber data, or the future 96-projector.
