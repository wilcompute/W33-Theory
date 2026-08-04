# Passes 3296–3307 publication envelope

This directory carries the already-audited Passes 3286–3297 Base85/zlib payload and a deterministic namespace lift into the globally reserved Passes 3296–3307 range.

The materializer first verifies the original encoded and decoded SHA-256 values, then applies the exact numeric lift `3286..3297 -> 3296..3307`, updates the regenerated semantic hash, and verifies all 32 transformed files against the new manifest.

This indirection was required because parallel agents claimed the earlier namespaces while the source packet was being published. It changes no theorem, certificate, or result value.
