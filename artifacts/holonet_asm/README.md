# Holonet Assembly Exports

Pass 49 exports the W(3,3) symplectic router into three deterministic
retro machine listings plus golden traces for the same sample route.

- `router_4004_style.asm`: 4-bit listing with primitive `MUL` and `MOD3`.
- `router_6502_style.asm`: 6502-style accumulator listing with synthesized arithmetic.
- `router_z80_style.asm`: Z80-style accumulator listing with synthesized arithmetic.
- `golden_trace_*_style.json`: sample execution traces for `1000 -> 0100`.

These are canonical Holonet target listings, not vendor-assembler promises.
