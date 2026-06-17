# BT1285 -- Recovery Packet Landing Snippet

## Purpose

BT1285 adds a compact landing page for the finite Clifford recovery packet.

## New page

```text
docs/recovery_packet_landing.md
```

## Landing pointers

The landing page points to:

1. Human guide.
2. Machine index.
3. Strict certificate.
4. Certificate verifier.
5. Single-candidate scorer.
6. Batch scorer.
7. Paper sections.

## Expected outputs

```text
verified = true
pass = 1
review = 1
fail = 2
```

## Boundary

This creates a standalone docs landing page. No top-level README update was made in this pass, because the safe path was to add a dedicated docs page without risking edits to a large existing landing file.
