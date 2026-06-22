# BT1412 Toroidal Q4 Oscillator Boundary

BT1412 joins the older toroidal square, oscillator, and dual-polyhedron
threads into one local ABI theorem.

The already-verified inputs are:

```text
4x4 toroidal knight graph = Q4
tetrahedral oscillator marks = {0,3,4,7} mod 12
forbidden neighborly genus = h=q=3
Csaszar/Szilassi shared edge boundary = 21
```

## The Splice

The 4-cube has

```text
C(4,2) * 2^2 = 24
```

square faces.  The four oscillator marks therefore occupy exactly

```text
4 / 24 = 1 / 6
```

of the Q4 plaquette shell.  Removing the forbidden neighborly genus level
`q=3` leaves the toroidal dual edge channel:

```text
24 - 3 = 21
```

That `21` is the invariant preserved by the Csaszar/Szilassi dual pair:

```text
Csaszar:  V,E,F = 7,21,14
Szilassi: V,E,F = 14,21,7
```

Duality swaps vertices and faces while preserving the edges, and in both rows
`V+F=E=21`.

## Gray Clock Boundary

The closed toroidal knight tour is a 16-tick Gray Hamilton cycle on Q4.  It
alternates board parity and Q4 bit parity on every step.

This is not promoted to an induced snake-in-the-box code.  The full Hamilton
cycle uses 16 Q4 edges while Q4 has 32 edges, so there are 16 non-cycle chords.
The useful error-detecting layer is the every-other projection:

```text
0, 6, 3, 5, 9, 15, 10, 12
```

Those eight even-parity words have pairwise Hamming distance at least 2, and
the cyclic projection steps all have distance 2.

## Physical Reading

The local packet clock is a 16-state toroidal Q4 Gray clock.  Its 24 square
faces are the plaquette shell on which the tetrahedral oscillator's four
admissible mod-12 marks occupy exactly a `1/6` aperture.  Removing the
forbidden neighborly genus `h=q=3` leaves `21`, the edge channel preserved by
the Csaszar/Szilassi dual toroidal boundaries.

This makes the two toroidal polyhedra into boundary conditions around the
tetrahedral oscillator interface: Csaszar is maximal vertex adjacency, Szilassi
is maximal face adjacency, and duality keeps the edge channel intact.

## Boundary

BT1412 is a finite arithmetic and routing certificate.  It does not prove a
continuous optical embedding of the toroidal polyhedra, a new optimal
snake-in-the-box code, or a calibrated physical oscillator.  It supplies the
exact local ABI boundary tying Q4 plaquettes, mod-12 oscillator marks, and the
21-edge toroidal dual channel.

## Verification

```bash
python tools/bt1412_toroidal_q4_oscillator_boundary.py
python tests/test_bt1412_toroidal_q4_oscillator_boundary.py
python -m py_compile tools/bt1412_toroidal_q4_oscillator_boundary.py tests/test_bt1412_toroidal_q4_oscillator_boundary.py
python -m json.tool data/bt1412_toroidal_q4_oscillator_boundary.json
```
