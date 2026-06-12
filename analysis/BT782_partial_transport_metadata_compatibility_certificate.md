# BT782 — Partial Transport / Metadata Compatibility Certificate

Verifier added: `analysis/bt782_partial_transport_metadata_compatibility.py`.

Existing partial artifact:

`data/bt760_root_torsor_to_q43_transport.partial.json`

The partial block has 48 rows:

- root id: 0
- chirality bit: 0
- inner coordinate: 0 through 47

BT782 embeds that partial block into the BT779 metadata shape by the rule:

- root id maps to the 540-way id
- chirality maps to the parity bit
- inner coordinate maps to the 48-way id

Verified checks:

- partial rows: 48
- unique row ids: 48
- the block embeds as `(0, 0, id48)` for all 48 values of `id48`
- the partner involution agrees with the inner-coordinate rule
- Q(4,3) target fields remain unresolved

Boundary: this is source/local metadata compatibility only. It does not resolve
Q(4,3) target apartments or promote a full transport table.
