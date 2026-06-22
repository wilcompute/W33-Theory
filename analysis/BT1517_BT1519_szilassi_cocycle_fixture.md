# BT1517--BT1519: concrete Szilassi map, decorated cocycle runner, and full fixture materializer

## Repo checks performed

This packet explicitly checks prior repo work before extending it:

- BT1444 fixed Szilassi face extractor;
- Toroidal-Polyhedra-Realizations data;
- BT1514 toroidal incidence model;
- BT1515 residual cocycle law;
- BT1511/BT1516 calibration fixture path.

## BT1517

The 7/21/3 incidence model is anchored to the actual Szilassi fixed hexagon from BT1444.  The concrete anchor is face index 4 with boundary vertices [11, 9, 12, 10, 8, 13] and boundary shift 3.

This gives the 3 a sharper reading: the fixed hexagon splits into three opposite two-edge sectors under the boundary shift.  The remaining six face classes still need full face-list import for a complete realization theorem.

## BT1518

The decorated cocycle runner combines the BT1510 orbit firewall and BT1515 residual law.  Representative line/gauge moves reach all six S3 residual keys and show that BT1504 classes are not automatically canonical orbit-unions under the scaffold.

## BT1519

The fixture materializer emits the full 576-row native D4 calibration CSV in checkout.  Measurement fields remain blank placeholders.  The connector blocked committing the literal sample CSV, so the executable materializer is the source of truth.

## Current synthesis

The toroidal bridge is now anchored to the actual Szilassi fixed hexagon, the residual cocycle has a representative decorated runner, and the calibration fixture has a full materializer path.
