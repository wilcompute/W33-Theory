# Passes 1330--1334: Modular radicals, triality grid, cycles, AtlasRep, and manuscripts

## Pass 1330 -- exact modular Jacobson radicals

The literal 26-dimensional Hecke multiplication tensor was reconstructed from all
Pass-1321 rational matrix units.  Its `int16` SHA-256 is

`3c41297ebbdd709f2bec32d25edde1b6b94d545d99ff50acdb4c376c639148e5`.

The tensor is reconstructed from Pass-1321 matrix units. Pass 1315 owns the
rational Wedderburn decomposition, not an independent copy of this hash.

The exact reductions are:

| characteristic | central blocks | dim radical | Loewy powers | semisimple quotient |
|---|---:|---:|---|---|
| 2 | 4 + 22 | 21 | 21,17,13,7,2,0 | `M2(F2) + F2` |
| 3 | 1 + 25 | 22 | 22,16,10,4,0 | `F3^4` |
| 5 | 1+1+1+1+4+9+9 | 6 | 6,2,0 | `M3(F5) + M2(F5) + F5^7` |

The reduced-center dimensions are 2, 2, and 7. The producer now enumerates
every central idempotent and ranks every primitive central block rather than
copying those dimensions from the quotient-map input. The exact scope is the
radical, semisimple quotient, Loewy powers, center, and central-block profile;
no general quiver-with-relations classification is claimed here.

## Pass 1331 -- spectral completion of the Pass-1327 nine-axis grid

Pass 1327 already owns the literal three-by-three species-20 gauge grid. On
the abstract coordinate model, the three internal axes on each triality carrier form
`{0,1,2} x {0,1,2}`.  The coherent `S3 x S3` action has four orbitals with
valencies `1,2,2,4`, primitive ranks `1,2,2,4`, and eigenmatrix

```
1  2  2  4
1 -1  2 -2
1  2 -1 -2
1 -1 -1  1
```

It is the tensor product of two rank-2 complete-graph schemes.  Adding the
coordinate swap fuses the two middle relations to the rank-3 Hamming scheme
`H(2,3)` with valencies `1,4,4`.

## Pass 1332 -- two selected symmetry-breaking cycle representatives

The deterministic search selects two literal simple cyclic words:

- length 7: cycle `[0,1,2,3,22,4,13]`, ordered/dihedral stabilizer 2,
  orbit 25920; its support stabilizer is 12 and it has five chords;
- length 8: cycle `[0,1,2,3,22,4,7,14]`, ordered/dihedral stabilizer 1,
  orbit 51840.

These values describe the selected cyclic orders, not invariants of all
length-7 or length-8 cycles.

A correction is essential: Pass 1328 proves that an invariant Y-side operator
acts as `C tensor I3` on the three transported species-20 coordinates.
It does **not** choose a copy by itself.  A primitive copy idempotent, whose
internal-S3 stabilizer has order 2, must be supplied.  The combined
`W(E6) x S3` cycle-plus-copy orbit sizes are 77760 and 155520.

## Pass 1333 -- genuine GAP/AtlasRep validation

`analysis/w33_pass1333_atlasrep_species20.g` loads AtlasRep, CTblLib, TomLib,
and Repsn; constructs `AtlasGroup("U4(2).2")`; builds all three degree-20
affording representations; and uses tables of marks to test the degree-20
multiplicities in index-432 and index-480 coset characters.  This is a real
runtime program rather than generic 3-by-3 coordinate swaps.

The complete script passed under GAP 4.12.1 with Repsn 3.1.2. All three
degree-20 representations have faithful image order 51840; the TOM data
include a 432 action with multiplicities `[0,3,0]` and a 480 action with a
single degree-20 copy. The script emits
`data/w33_pass1333_atlasrep_species20.json`; CI requires its explicit
`PASS 1333 COMPLETE` marker because a bare GAP error can otherwise exit zero.

## Pass 1334 -- manuscript integration

The compile-ready insert occurs exactly once in both
`w33_paper.tex` and `photonic_holonet.tex` by
`tools/integrate_pass1330_1334.py`. The release workflow runs the integrator,
checks idempotence, and compiles both manuscripts. No local TeX engine is
installed, so full PDF compilation is an explicit CI boundary rather than a
claimed local pass.
