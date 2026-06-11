# BT789 - Toroidal Genus Phase Bridge

The cube/tomotope exchange has the exact order identity:

```text
cube:     C2^3:S3, order 8*6  = 48
tomotope: C2^4:C3, order 16*3 = 48
```

The important point is that the groups have the same order but different
structure:

```text
C2^3 = 1 + 2
C2^4 = 2 + 2
```

BT789 connects the `3` and `4` in that replacement to the classical toroidal
polyhedron genus laws.

## Toroidal Unit

For the neighborly Csaszar torus:

```text
g(n) = (n-3)(n-4)/12
```

For the complete-face Szilassi dual:

```text
h(f) = (f-4)(f-3)/12
```

At the first positive toroidal value `n=f=7`:

```text
1 = (7-3)(7-4)/12 = 4*3/12.
```

The allowed residue classes are exactly:

```text
0, 3, 4, 7 mod 12
```

So the minimal torus is literally a normalized `4 x 3` event.

## Module Reading

The cube side has a fixed diagonal bit:

```text
C2^3 nonzero C3 orbit profile = {1:1, 3:2}
```

Kill the diagonal:

```text
C2^3/<111> = one F4 plane
```

Then add the missing phase plane:

```text
F4 + F4 = C2^4
```

The tomotope side has no fixed nonidentity bit:

```text
C2^4 nonzero C3 orbit profile = {3:5}
```

Thus the toroidal unit

```text
4*3/12
```

is the same structure as:

```text
|F4 plane| * |C3 phase clock| / 12.
```

## GAP Witness

The verifier also asks GAP for the group fingerprint:

```text
C2 wr S3       = SmallGroup(48,48), center size 2
C2^4:C3 model = SmallGroup(48,50), center size 1
```

They are not isomorphic.  The fixed diagonal bit is real group structure, not
notation.

## Validation

Run:

```bash
python3 analysis/bt789_toroidal_genus_phase_bridge.py
```
