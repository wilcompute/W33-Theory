# BT927 — Reconciliation of the E8 lift artifacts

BT927 cross-indexes the current E8 witnesses and prevents an equivalence overclaim.

## Artifact roles

| artifact | role | status |
|---|---|---|
| BT924 SNF shadow | integral invariant-factor location | rank and 2-adic sector pinned, no Gram chosen |
| BT925 mod-2 form | canonical H bilinear form | symplectic E8/2E8, no definiteness |
| BT926 vertex E8 | positive-definite Cartan witness | definite E8, not canonically linked to chain H |
| MCCCLXXXVIII tetracode E8 | 240-root metric witness | full root system, bridge to chain H not canonical |
| MCCCLXXXIX E8 to E6 x A2 | coordinate branching | useful for map search, not a chain lift by itself |

## Reconciliation

The witnesses are compatible but not yet proved identical as one canonical lift.

```text
chain shadow (BT924/925)  !=[not yet proved]  vertex/tetracode metric E8.
```

## Exact next target

Construct an explicit symplectic basis of H, lift it into either the BT926 vertex Gram or the MCCCLXXXVIII tetracode coordinates, and certify integral even-unimodular positivity.

## Witness

```text
analysis/bt927_e8_lift_artifact_reconciliation.py
data/bt927_e8_lift_artifact_reconciliation.json
```
