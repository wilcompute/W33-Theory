# Passes 1330--1334: Modular radicals, triality grid, cycles, AtlasRep, and manuscripts

## Pass 1330 -- exact modular Jacobson radicals

The literal 26-dimensional Hecke multiplication tensor was reconstructed from all
Pass-1321 rational matrix units.  Its `int16` SHA-256 is

`3c41297ebbdd709f2bec32d25edde1b6b94d545d99ff50acdb4c376c639148e5`,

identical to the independently frozen Pass-1315 tensor.

The exact reductions are:

| characteristic | central blocks | dim radical | Loewy powers | semisimple quotient |
|---|---:|---:|---|---|
| 2 | 4 + 22 | 21 | 21,17,13,7,2,0 | `M2(F2) + F2` |
| 3 | 1 + 25 | 22 | 22,16,10,4,0 | `F3^4` |
| 5 | 1+1+1+1+4+9+9 | 6 | 6,2,0 | `M3(F5) + M2(F5) + F5^7` |

The reduced-center dimensions are 2, 2, and 7.  This is the full
finite-dimensional algebra classification requested at the three bad primes,
not merely a rank-drop calculation.

## Pass 1331 -- literal nine-axis triality scheme

The three internal species-20 axes on each of three triality carriers form
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

## Pass 1332 -- symmetry-breaking cycle selector classification

Deterministic literal simple cycles give:

- length 7: cycle `[0,1,2,3,22,4,13]`, stabilizer 2, orbit 25920;
- length 8: cycle `[0,1,2,3,22,4,7,14]`, stabilizer 1, orbit 51840.

A correction is essential: an unaveraged Y-side cycle breaks `W(E6)`, but it
still acts as `C tensor I3` on the three transported species-20 coordinates.
It does **not** choose a copy by itself.  A primitive copy idempotent, whose
internal-S3 stabilizer has order 2, must be supplied.  The combined
`W(E6) x S3` cycle-plus-copy orbit sizes are 77760 and 155520.

## Pass 1333 -- genuine GAP/AtlasRep attempt

`analysis/w33_pass1333_atlasrep_species20.g` loads AtlasRep, CTblLib, TomLib,
and Repsn; constructs `AtlasGroup("U4(2).2")`; builds all three degree-20
affording representations; and uses tables of marks to test the degree-20
multiplicities in index-432 and index-480 coset characters.  This is a real
runtime program rather than generic 3-by-3 coordinate swaps.

GAP is absent from the local execution container.  The script is CI-wired and
no local GAP result is claimed.

## Pass 1334 -- manuscript integration

The compile-ready insert is integrated idempotently into both
`w33_paper.tex` and `photonic_holonet.tex` by
`tools/integrate_pass1330_1334.py`.  The release workflow runs the integrator,
checks idempotence, and compiles both manuscripts.  A local minimal-document
compile checks the insert independently of the repository's historical TeX
surface.
