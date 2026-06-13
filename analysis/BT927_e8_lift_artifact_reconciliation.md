# BT927 — Reconciliation of the \(E_8\) lift artifacts

BT927 cross-indexes the current \(E_8\) witnesses and prevents an equivalence overclaim.

## Artifact roles

| artifact | role | status |
|---|---|---|
| BT924 SNF shadow | integral invariant-factor location | rank and 2-adic sector pinned, no Gram chosen |
| BT925 mod-2 form | canonical \(H\) bilinear form | symplectic \(E_8/2E_8\), no definiteness |
| BT926 vertex \(E_8\) | positive-definite Cartan witness | definite \(E_8\), not canonically linked to chain \(H\) |
| MCCCLXXXVIII tetracode \(E_8\) | 240-root metric witness | full root system, bridge to chain \(H\) not canonical |
| MCCCLXXXIX \(E_8	o E_6	imes A_2\) | coordinate branching | useful for map search, not a chain lift by itself |

## Reconciliation

The witnesses are compatible but not yet proved identical as one canonical lift.

\[
oxed{	ext{chain shadow }(BT924/925)\quad
eq_{m not\ yet\ proven}\quad	ext{vertex/tetracode metric }E_8.}
\]

## Exact next target

Construct an explicit symplectic basis of \(H\), lift it into either the BT926 vertex Gram or the MCCCLXXXVIII tetracode coordinates, and certify integral even-unimodular positivity.

## Witness

```text
analysis/bt927_e8_lift_artifact_reconciliation.py
data/bt927_e8_lift_artifact_reconciliation.json
```
