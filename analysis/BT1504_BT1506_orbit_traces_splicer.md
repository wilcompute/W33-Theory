# BT1504--BT1506: skew-line orbit map, native route traces, and release splicer

## BT1504 -- skew-line residual quotient map

BT1504 replaces the BT1501 edge-index placeholder with a map derived from actual skew-line data:

- BT1367 actual skew-line endpoints;
- BT1373 improved-gauge S3 residuals;
- 540 skew residuals;
- 210 identity edges and 330 corrections.

The resulting map covers all 7 point classes, all 21 flag classes, and all 3 fiber classes, then emits a 2397-clause WCNF scaffold.  This remains a scaffold: it is data-derived and reproducible, but not yet a canonical Aut(W33)-orbit theorem or a solved 330-frontier certificate.

## BT1505 -- native D4 generator route traces

BT1505 gives each of the eight native D4 classes a representative 72-tick symbolic route trace carrying detector slot, mirror residue, Hesse lane, row slot, qutrit value, and CSS column metadata.

The ledger still has 576 total native ticks:

8 generators * 72 ticks = 576.

These traces are for calibration planning, not measured optical losses or timings.

## BT1506 -- release-lock splicer

BT1506 adds an idempotent splicer for the transaction/scheduler packet:

- BT1495--BT1497 insert;
- BT1498--BT1500 insert;
- BT1501--BT1503 insert.

The splicer targets photonic_holonet.tex before the fuel section.  The connector commit adds the splicer and manifest; it does not rewrite the large paper source here.

## Current synthesis

Actual skew-residual data now drives the SAT scaffold, native D4 traces are concrete enough for calibration planning, and the next paper splice has an idempotent checkout tool.
