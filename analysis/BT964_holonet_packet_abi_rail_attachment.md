# BT964 — Holonet packet ABI rail attachment

BT964 attaches the final selector rails to the Holonet prefix table.

## Assignment rule

Sort rails by BT963 phase score, then support sum, then xor mask. Assign to prefixes:

```text
[0, 10, 110, 111]
```

## Lane table

```text
prefix 0   -> mirror   -> rail 1 -> pair [4,42]    -> score 16
prefix 10  -> schedule -> rail 0 -> pair [3,68]    -> score 16
prefix 110 -> cache_A  -> rail 2 -> pair [38,65]   -> score 19
prefix 111 -> cache_B  -> rail 3 -> pair [90,144]  -> score 27
```

## Reading

The final E8 selector supplies concrete rail lanes for the Holonet packet prefix table: the two light rails feed mirror/schedule, and the heavier rails feed the two cache slots.

## Boundary

This is a selector-backed ABI attachment convention. It is not yet a proof that all packet operations preserve the assigned lanes.

## Witness

```text
data/bt964_holonet_packet_abi_rail_attachment.json
```
