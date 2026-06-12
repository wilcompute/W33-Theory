# BT779 Metadata Lift Certificate

Verifier added: `analysis/bt779_51840_metadata_lift.py`.

Core count:

51840 = 540 * 2 * 48.

Rule:

- first id: stored W33 nonedge id
- parity bit: parity of the ordered opposite tetrad
- second id: selector index times 12 plus parity rank

Checks encoded in the verifier:

- total rows are 51840
- 540 ids each occur 96 times
- two parity classes each occur 25920 times
- 48 ids each occur 1080 times
- every triple occurs exactly once
- 45 packets each lift to 1152 rows
- 240 charts each lift to 216 rows

Boundary: this proves a deterministic metadata lift over the BT776 scaffold. It
is still a candidate shape, not the unavailable external row table.
