# BT1061 — Scalar operator search space

BT1061 enumerates a small W33-native search space for future scalar-slot operators `Q`.

## Candidate families

| family | candidate | strengths | boundary |
| --- | --- | --- | --- |
| Laplacian polynomial | `Q = p(Delta_1)` | chain-native, sector-diagonal, computable immediately | may be too central / gauge-neutral |
| Spectral projector | `Q = sum c_lambda P_lambda` | exact control of sector amplitudes | still needs physical coefficient derivation |
| Harmonic projector | `Q = P_0` | isolates matter zero modes | gives zero mixed `Delta_1 Q^2` |
| Boundary projector | `Q = P_4` | isolates 120 local-boundary carrier | may represent gauge/local sector rather than Higgs |
| Heavy projector | `Q = P_10` or `P_16` | probes heavy correction sectors | physical interpretation open |
| Generation/fiber projector | `Q = Q_gen/fiber` | can encode BT1047 invariants | needs explicit 240-chain lift |
| Centralizer projector | `Q = Q_C(R)` | tied to finite SM centralizer route | requires representation matrices on chain carrier |

## Scoring criteria

Each candidate should be scored by:

```text
1. W33-native definition
2. commutation with Delta_1
3. compatibility with the finite algebra action
4. first-order compatibility
5. nonzero Tr(Delta_1 Q^2)
6. symbolic trace simplicity
7. relation to generation/fiber invariants
8. absence of empirical parameter insertion
```

## Current baseline score

For `Q = Delta_1/4`:

```text
W33-native definition              yes
commutes with Delta_1              yes
sector amplitudes computable       yes
nonzero Tr(Delta_1 Q^2)            yes
physical scalar identification     no
finite-algebra compatibility       pending 240-action lift
```

## Next exact move

Construct the 240-chain action of the finite algebra or centralizer projectors. That is the missing prerequisite for scoring commutators and first-order compatibility beyond the sector-diagonal Laplacian family.
