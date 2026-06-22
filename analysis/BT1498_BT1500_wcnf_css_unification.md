# BT1498--BT1500: full quotient scaffold, transaction CSS replay, and scheduler/pulse unification

## BT1498 -- full Fano quotient WCNF generator

BT1498 upgrades BT1496 from a compact scaffold into a full WCNF generator for the BT1373 330-correction frontier.  The generated instance has:

- 540 soft identity-edge clauses;
- 22 hard clauses for one Fano point anchor;
- 211 hard clauses for one Fano flag anchor;
- 4 hard clauses for one local fiber block;
- 777 total generated clauses over 571 variables.

This is still not a global optimum proof.  It is the quotient scaffold on which orbit-compatibility clauses and imported MaxSAT certificates can be layered.

## BT1499 -- transaction-word CSS replay

BT1499 replays the 24 transaction words from BT1495 through the BT1486 retwined CSS row classes.  Each word contains 72 ticks:

- 24 active ticks;
- 48 guard ticks.

Across all 24 words, this gives:

- 1728 total ticks;
- 576 active ticks;
- 1152 guard ticks.

All replay ticks inherit X/Z syndrome legality from the ABI v2 CSS layer.  This is a symbolic CSS replay, not a physical optical-noise simulation.

## BT1500 -- scheduler/pulse unification table

BT1500 aligns the finite symmetry, pulse, CSS, and scheduler layers in one table:

- Fano bus 168 = 7*24 = 21*8;
- S4 shared fiber 24;
- native D4 subgroup 8;
- C3 x D4 scheduler lift 24;
- 72-tick transaction word;
- 1728 physical row-pulse packet;
- 576 native D4 square-pulse ticks;
- Steinberg scheduler carrier 81;
- retwined CSS ABI row sector 72.

## Current synthesis

Fano 168 -> fiber 24 -> D4 8 -> 72-tick words -> 1728 pulses -> retwined CSS legality -> Steinberg 81 scheduler carrier.
