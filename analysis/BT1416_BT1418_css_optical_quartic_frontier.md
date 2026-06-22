# BT1416-BT1418: CSS Matrix, Optical Primitive, D4-Quartic Injection Frontier

This packet executes the three open follow-ons from BT1413-BT1415:

1. make the `240`-row BT1415 ledger into actual sparse CSS/intertwiner
   matrices;
2. turn the Csaszar/Szilassi dual port into objectwise linear-optical
   primitives;
3. attach the exact two-atom D4 quartic magic frontier to the guard band.

The main constraint is field discipline.  The Q4 front end is binary clock
logic over `F2`.  The W33 protected memory remains the canonical edge-chain
CSS code over `F3`.  BT1416 therefore uses a typed row/edge interwiner instead
of pretending the binary parity bits are qutrit stabilizer coefficients.

## BT1416: sparse CSS interwiner

BT1416 rebuilds the canonical W33 chain complex directly:

```text
points     = 40
edges      = 240
triangles  = 160
HX = d1    : 40 x 240
HZ = d2^T  : 160 x 240
```

The generated certificate checks:

```text
rank(HX) = 39
rank(HZ) = 120
HX HZ^T = 0 over F3
k = 240 - 39 - 120 = 81
```

So the carrier is still the exact `[[240,81,3]]_3` edge-chain CSS code.  The
new ingredient is a sparse `240 x 240` ledger interwiner:

```text
ledger row i -> W33 edge column i
```

Rows `0..215` are typed as `F2` front-end parity checks.  Rows `216..239` are
typed as the guard tail that addresses the same `F3` edge carrier.  The binary
front-end matrix has shape `216 x 4`, rank `1`, and kernel equal to the eight
even Q4 words of minimum distance `2`.

The point is precise: BT1416 proves compatibility by shared indexing and CSS
commutation, not by coercing fields.

## BT1417: objectwise optical primitive synthesis

BT1417 takes the BT1414 identity

```text
21 shared K7 edge channels * 2 orientations * 4 residues + 24 guards = 192
```

and turns it into a primitive inventory:

```text
21  edge-channel balanced couplers
42  oriented phase latches
168 active residue detector bins
24  Q4 guard apertures
```

The analyzer matrices are the exact `7 x 21` K7 star-incidence matrices.  Their
Gram law is:

```text
diagonal     = 6
off-diagonal = 1
```

That is the object-level statement that every Csaszar vertex analyzer and every
Szilassi face analyzer sees six channels, and any two analyzers overlap in one
shared channel.  The same channel set is used in both modes; only the
interpretation changes from maximal vertex adjacency to maximal face adjacency.

This is not a foundry layout.  It is a primitive checklist: coupler, orientation
latch, four-residue demux, detector bin, with the 24 guard apertures physically
separated from the active mesh.

## BT1418: finite D4-quartic magic injection

The previous Golden Quartic/Moebius-ball audit stayed heuristic-only.  BT1418
instead uses the repo's exact finite quartic frontier: the Standard Model
minimal-magic audit has two independent irreducible D4 quartic atoms, with no
shared quadratic subfield and splitting field `D4 x D4`.

Those two atoms fit the BT1415/BT1416 guard band exactly:

```text
2 quartic atoms * 4 algebraic branches * 3 qutrit phases = 24 guard apertures
```

Then the D4 orientation torsor expands each guard aperture:

```text
24 guard apertures * 8 D4 orientations = 192 tomotope orientation tokens
```

This gives a finite replacement for the continuum analogy:

```text
4 branches * 27 Steinberg cycles * 8 D4 orientations = 864 per atom
```

The right-hand side is exactly the repo's Golden D4/Weyl shell.  With two
independent atoms the shell doubles to `1728`, but the atoms remain distinct;
BT1418 does not collapse them into one field.

## What changed architecturally

The local holonet front end now has a full finite stack:

```text
Q4 plaquettes
  -> tomotope/Q6 flag ABI
  -> Csaszar/Szilassi dual port
  -> binary even-Q4 syndrome front end
  -> typed 240-edge F3 CSS carrier
  -> objectwise optical primitive mesh
  -> D4 quartic non-Clifford guard injection
```

The guard band is no longer just unused slack.  It is the exact aperture where
non-Clifford quartic resources can enter without contaminating the binary
front-end syndrome rows or the F3 CSS commutation proof.

## Boundary

BT1416-BT1418 are finite certificates.  They do not calibrate optical loss,
detector efficiency, waveguide geometry, electron structure, or a continuum
Moebius-ball model.  The external Golden Quartic paper remains a heuristic
topology prompt only; the exact content here is the repo-local D4/Weyl and
W33 CSS algebra.
