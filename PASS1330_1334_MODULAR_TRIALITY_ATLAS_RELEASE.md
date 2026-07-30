# Passes 1330--1334 exact release

This release closes five requested frontiers while preserving runtime boundaries.

1. **Pass 1330:** exact Jacobson radicals, semisimple quotients, central blocks,
   and Loewy layers of the literal 26-dimensional Hecke algebra in
   characteristics 2, 3, and 5.
2. **Pass 1331:** the literal four-class `S3_internal x S3_triality` scheme on
   the nine species-20 axes and its `H(2,3)` coordinate-swap fusion.
3. **Pass 1332:** literal length-7 and length-8 cycle stabilizers, plus the
   theorem that cycle symmetry breaking and multiplicity-copy selection are
   separate operations.
4. **Pass 1333:** a genuine GAP program using AtlasRep, CTblLib, TomLib, and
   Repsn; this replaces the earlier coordinate-only scaffold. Local GAP was
   unavailable, so execution is delegated to a dedicated CI job.
5. **Pass 1334:** a compile-ready theorem insert, idempotent integration into
   both main manuscripts, local insert compilation, and full repository build
   jobs.

The authoritative machine-readable result is
`data/w33_pass1330_1334_modular_triality_cycle_atlas.json`.
