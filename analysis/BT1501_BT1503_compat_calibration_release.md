# BT1501--BT1503: quotient compatibility, native D4 calibration, and release splice lock v3

## BT1501 -- quotient compatibility WCNF

BT1501 adds the first real compatibility layer to the BT1498 quotient scaffold.
The generated WCNF has:

- 540 soft identity-edge clauses;
- 237 one-hot hard clauses for Fano point, flag, and fiber choices;
- 1620 hard compatibility clauses tying each selected edge to point, flag, and fiber classes;
- 2397 generated clauses over 571 variables.

This is not a solved MaxSAT certificate. The quotient map is still a deterministic scaffold map, and the next step is to replace it with the true skew-line orbit map.

## BT1502 -- native D4 pulse calibration ledger

BT1502 splits the 576 native square-pulse ticks into eight D4 calibration classes:

- identity: 1 action, 72 ticks;
- quarter turns: 2 actions, 144 ticks;
- half turn: 1 action, 72 ticks;
- reflections: 4 actions, 288 ticks.

Each native generator contributes one 72-tick word with 24 active and 48 guard ticks. This is a finite calibration ledger, not a measured optical error model.

## BT1503 -- release splice lock v3

BT1503 promotes BT1495--BT1502 to the preferred exact finite transaction/scheduler packet for the next Holonet release splice. The splice order is:

1. BT1495--BT1497 transaction/scheduler insert;
2. BT1498--BT1500 quotient/CSS/unification insert;
3. BT1500 scheduler-pulse table;
4. BT1502 native D4 calibration ledger.

## Current synthesis

Fano quotient constraints now touch edge variables; native D4 pulses have calibration classes; and the next paper release has an explicit splice lock before PDF rebuild.
