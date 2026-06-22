# BT1413-BT1415: toroidal Q4 compiler, dual port, and syndrome ledger

BT1412 gave the boundary count

```text
24 Q4 plaquettes, 4/24 = 1/6 oscillator aperture, 24 - 3 = 21 toroidal edges.
```

BT1413 through BT1415 turn that boundary into an addressable front-end architecture.

## BT1413 - Q4 plaquette to tomotope/Q6 flag compiler

BT1363 already proves the antipodal quotient of Q4 face-edge incidence is the
tomotope/Reye medial layer.  BT1371 already proves a bijective 192-row
tomotope-flag to Q6-edge table.  BT1413 composes them:

```text
24 Q4 plaquettes
  * 4 edge incidences
  / 2 antipodal lifts
  = 48 tomotope middle blocks

48 middle blocks * 4 flag residues = 192 tomotope/Q6 flags.
```

The generated compiler verifies:

- all 24 Q4 plaquettes are used;
- the 96 lifted face-edge incidences quotient to 48 middle blocks;
- every middle block has exactly two Q4 lifts;
- the three BT1363 ternary sheets have 64 flags each;
- each sheet hits all 16 tomotope face labels exactly once at block level;
- the 192 tomotope flags map bijectively to 192 Q6 edges, each a one-bit Q6 edge.

So the Q4 plaquette shell is no longer just a count.  It is an explicit flag bus.

## BT1414 - Csaszar/Szilassi dual physical port

BT1317 already split the tomotope packet as

```text
192 = 168 active toroidal slots + 24 ground slots.
```

BT1414 explains the active part as the physical dual port:

```text
21 shared toroidal edge channels
  * 2 orientations
  * 4 flag residues
  = 168 active slots.
```

The two analyzer modes use the same 21 edge channels:

- Csaszar mode: maximal vertex adjacency, seven vertex analyzers, each seeing six
  edge channels;
- Szilassi mode: maximal dual face adjacency, seven face analyzers, each seeing
  six edge channels.

Every edge channel appears in exactly two Csaszar analyzers and exactly two
Szilassi analyzers.  The BT1318 metric-axis records give the current fixed
axes: Csaszar fixes vertex 6, Szilassi fixes face 4, and the crossed calibration
channel is edge {4,6}.  The remaining 24 flags are not waste: they become the Q4
plaquette guard band.

## BT1415 - even Q4 projection as Steinberg/CSS syndrome ledger

BT1412's every-other clock projection is the eight-word even-parity layer

```text
0, 6, 3, 5, 9, 15, 10, 12.
```

It is a distance-2 binary front-end code: every allowed word has parity zero,
and every one-bit Q4 clock fault toggles the parity syndrome.  BT1375 supplies
the memory clock: the central C3 action on the Steinberg register has 27
three-cycles and nilpotent rank profile

```text
54, 27, 0.
```

The new ledger identity is

```text
27 Steinberg central cycles * 8 even Q4 states = 216 syndrome rows
216 syndrome rows + 24 Q4 plaquette guard rows = 240 CSS edge rows.
```

This exactly fills the existing W33 CSS edge ledger from BT1375, whose
chain-complex edge count is 240 and whose memory dimension is 81.  The field
boundary is important: the parity check is binary clock-side logic over F2; the
protected Steinberg/CSS register remains the existing F3 object.

## External Golden Quartic / Moebius-ball audit

Hans H. Otto's *Golden Quartic Polynomial and Moebius-Ball Electron* proposes a
golden-ratio/quartic and icosahedral/Moebius-ball electron geometry.  Newer
related material around the same program includes the 2025 ResearchGate preprint
*Can Artificial Intelligence Help to Verify the Most Probable Electron Structure
Model*, and the 2025 review *Critical Review of Zitterbewegung Electron Models*
frames extended electron models as Zitterbewegung/field-dynamics hypotheses.

The useful architecture lesson is not "use this as evidence."  The useful
lesson is separation of concerns:

- topology/chirality lives in the closed-loop/toroidal routing layer;
- scale normalization must be kept separate from topological adjacency;
- quartic algebra should enter through an exact gate/magic frontier, not through
  a visual electron-shape analogy.

The repo's exact quartic frontier remains the two independent D4 quartic atoms
in `scripts/w33_standard_model_minimal_magic_audit.py`.  BT1415 records the
Moebius-ball paper only as a heuristic external audit; no electron mass, spin,
or optical embedding claim depends on it.

## Breakthrough

The new architectural object is the first complete local front end:

```text
Q4 plaquettes -> tomotope/Q6 flags -> Csaszar/Szilassi dual port
               -> even-parity Q4 syndrome -> Steinberg/CSS 240-edge ledger.
```

This is the physical-computation bridge BT1412 pointed toward.  The toroidal Q4
clock supplies packet motion, the tomotope/Q6 flag table supplies addressable
edges, the Csaszar/Szilassi port supplies dual boundary analyzers, and the
Steinberg/CSS ledger supplies the memory-side check surface.

Boundary: this is a finite ABI/check certificate.  It is not yet a continuous
waveguide layout, a detector calibration, a new CSS stabilizer proof, or a
physical electron model.
