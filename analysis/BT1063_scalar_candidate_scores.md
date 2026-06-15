# BT1063 — Scalar candidate scoring

BT1063 scores the BT1061 scalar-operator candidates after the BT1062 240-chain lift.

## Scoring scale

Each criterion is scored as:

```text
2 = strong / verified
1 = partial / pending construction
0 = fails or not applicable
```

Criteria:

```text
W33-native definition
Delta_1 compatibility
finite-algebra compatibility under BT1062
nonzero mixed trace
relation to generation/fiber data
physical identification status
```

## Candidate scores

| candidate | W33 native | Delta compat | AF compat | mixed trace | gen/fiber | physical status | total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `Q=Delta_1/4` | 2 | 2 | 2 | 2 | 0 | 0 | 8 |
| `Q=P0` | 2 | 2 | 2 | 0 | 1 | 0 | 7 |
| `Q=P4` | 2 | 2 | 2 | 2 | 0 | 1 | 9 |
| `Q=P10` | 2 | 2 | 2 | 2 | 0 | 0 | 8 |
| `Q=P16` | 2 | 2 | 2 | 2 | 0 | 0 | 8 |
| `Q=sum c_lam P_lam` | 2 | 2 | 2 | 2 | 1 | 1 | 10 |
| generation/fiber projector | 2 | 1 | 1 | 1 | 2 | 1 | 8 |
| centralizer projector | 2 | 1 | 1 | 1 | 1 | 2 | 8 |

## Current leader

The best current search family is

```text
Q = sum c_lam P_lam
```

because it remains W33-native and sector-computable while allowing generation/fiber or centralizer constraints to choose the coefficients.

## Reading

`Q=Delta_1/4` is the best baseline test object, but `Q=sum c_lam P_lam` is the best search family. The physical route likely requires choosing the coefficients from W33 representation data, not simply taking the Laplacian eigenvalue.

## Boundary

These scores are heuristic search scores, not proof of physical identification.
