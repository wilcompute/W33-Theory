# BT1070 — Off-diagonal lift scoring

BT1070 scores the BT1067 non-sector-preserving lift templates, now incorporating the BT1069 result

```text
Q64 = P0 + P16
```

as the clean 96-dimensional spectral support on the 240-chain carrier.

## Criteria

Each template is scored by:

```text
1. spectral gap economy
2. includes the E4 gauge/boundary sector
3. compatibility with the 96-support clue
4. nonzero commutator strength
5. construction readiness
6. preservation of the 1+3+8 local gauge profile
```

## Scores

| template | gap economy | gauge active | 96 support | nonzero comm | ready | gauge profile | total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| nearest-sector ladder `E0<->E4<->E10<->E16` | 2 | 2 | 1 | 2 | 2 | 1 | 10 |
| physical/complement mixing `P96<->P66` on 162 slots | 1 | 1 | 2 | 2 | 1 | 1 | 8 |
| boundary-heavy mixing `E4<->E10`, `E4<->E16` | 1 | 2 | 0 | 2 | 2 | 2 | 9 |
| endpoint physical spectral mixing `E0<->E16` | 0 | 0 | 2 | 2 | 2 | 0 | 6 |
| BT1069 support/complement mixing `(E0+E16)<->(E4+E10)` | 1 | 2 | 2 | 2 | 1 | 1 | 9 |

## Current leader

The best immediate lift template is the nearest-sector ladder:

```text
E0 <-> E4 <-> E10 <-> E16.
```

It keeps gaps small, activates the E4 gauge/boundary sector, and is easy to define from the known spectral decomposition.

## Best physical target

The best physical target is the BT1069 support/complement split:

```text
(E0 + E16) <-> (E4 + E10).
```

This aligns with the 96-dimensional support `E0+E16`, but it needs a derived off-diagonal operator before it can outrank the ladder template.

## Boundary

BT1070 scores templates. It does not construct the off-diagonal matrices. The next computation is to build the nearest-sector ladder operator and verify the predicted commutator gaps explicitly.
