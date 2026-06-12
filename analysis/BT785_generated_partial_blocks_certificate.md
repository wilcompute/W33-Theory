# BT785 — Generated Partial Blocks Compatibility Certificate

Verifier added: `analysis/bt785_generated_partial_blocks_compatibility.py`.

BT782 embedded the existing 48-row partial block into the BT779 metadata shape.
BT785 generalizes that source-local contract to all generated metadata blocks:

51840 = 540 * 2 * 48.

Checks:

- total generated rows: 51840
- generated blocks: 1080
- each block has 48 rows
- every `(id540, bit, inner)` triple appears exactly once
- the partner map is an involution in every block
- every 540-way id appears 96 times
- each bit class appears 25920 times
- every inner id appears 1080 times

Boundary: target-side Q43 fields remain unresolved. This is a source-local
compatibility theorem, not a completed transport table.
