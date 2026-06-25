# BT1789--BT1791 holonet H27 execution

## Read order and correction

This packet was executed only after a straight-through read of `photonic_holonet.tex`. The relevant holonet claim is not merely that a 27 exists. It is two different 27s:

```text
H27 = 3^{1+2}_+  : curved state shell, point-parabolic, noncommuting qutrit phases
A27 = F_3^3      : flat program shell, Bell-line parabolic, commuting three-trit addresses
```

The later holonet passage states the sharper local dictionary: the 27 non-collinear **points** form a genuine Heisenberg torsor whose invariant relations recover the 27-zoo, including `GQ(2,4)=SRG(27,10,1,5)` and the Schlaefli graph `SRG(27,16,10,8)`, while the 27 disjoint **lines** form the flat `F_3^3` operational shell with no invariant SRG.

The live-index correction is essential. The raw second subconstituent of `W(3,3)=SRG(40,12,2,4)` is:

```text
1 anchor + 12 neighbours + 27 non-neighbours = 40
raw 27 shell: 27 vertices, 8-regular, 108 edges
```

So the raw 27 is not already the Schlaefli/GQ(2,4) object. It is the affine Heisenberg bulk. The Schlaefli/Witting bridge runs through a Payne/Heisenberg transform of that shell.

## BT1789: H27 Payne tuple extractor

Fix an anchor point of `W(3,3)`. The 27 non-neighbours can be coordinatized as

```text
(a,b,d) in F_3^3, represented by projective vector (a,b,1,d).
```

The raw shell adjacency inherited from `W(3,3)` has signature:

```text
27 vertices
108 edges
8-regular
```

Then Payne derivation supplies exactly the missing 9 triples:

```text
old W33 triples not through anchor: 36
new Heisenberg vertical fibres:     9
total lines:                       45
```

The new fibres are:

```text
for fixed (b,d), {(0,b,d), (1,b,d), (2,b,d)}.
```

With the 36 old triples plus these 9 vertical triples, NetworkX verifies:

```text
GQ(2,4) collinearity = SRG(27,10,1,5)
Schlaefli dual complement = SRG(27,16,10,8)
```

This resolves the proposed connection: yes, the H27 object is the 27-SRG layer, but it is not the raw dual of `W(3,3)` collinearity. It is the Payne-derived local shell; the Schlaefli graph is the complement/dual of that derived `GQ(2,4)` collinearity graph.

## BT1790: 27-frontier H27 sheaf solver

BT1788 exposed a `27` pair-frontier object:

```text
{RC,RD,CD} x F_3 x F_3 = 27.
```

BT1790 identifies this as the H27 boundary geometry:

```text
(layer,u,v) in F_3^3,
layer in {RC,RD,CD}.
```

The nine new Heisenberg fibres become exactly the same Hesse cell seen through the three pair projections:

```text
[(RC,u,v), (RD,u,v), (CD,u,v)]  for each (u,v) in F_3^2.
```

The resulting sheaf has:

```text
27 points
45 local triple patches = 36 old W33 shell triples + 9 new H27 vertical triples
line size 3
each point incident with exactly 5 patches = 4 old + 1 new
GQ point-line axiom checks: 1080/1080 pass
```

The practical solver lesson is that the next true tuple materializer should not treat the 18 ternary tables as opaque counts. It should project them onto this 27-point H27/Payne boundary and use the 45 line patches as the local sheaf chart family before quotienting global sections by plateau symmetries.

## BT1791: D5 x Hesse weld

BT1783 rephased eight Coxeter 5-cycles so the inversion is uniformly:

```text
q -> -q mod 5.
```

BT1790 gives exactly five local line patches through each H27 point:

```text
phase 0:      the unique new Heisenberg vertical fibre
phases 1..4: the four old W33 shell triples through that point
```

That is the local D5 pencil. Orienting each pencil line gives:

```text
27 H27 points * 5 D5 phases * 2 orientations = 270 oriented local flags.
```

Cross with the eight BT1783 rephased Coxeter cycles:

```text
8 * 270 = 2160 = 8 * 27 * 5 * 2.
```

So the D5 bus and the H27 sheaf meet exactly at the holonet mirror-bus count. This does not assert a global `D5^27` automorphism group of `GQ(2,4)`; it asserts the local phase-pencil ABI whose eight-cycle lift recovers the already verified `2160` mirror slots.

## Files

- `analysis/bt1789_h27_payne_tuple_extractor.py`
- `data/bt1789_h27_payne_tuple_extractor.json`
- `analysis/bt1790_h27_frontier_sheaf_solver.py`
- `data/bt1790_h27_frontier_sheaf_solver.json`
- `analysis/bt1791_d5_hesse_weld.py`
- `data/bt1791_d5_hesse_weld.json`
- `analysis/BT1789_BT1791_holonet_h27_execution.md`

## Bottom line

```text
raw W33 local 27 shell       = 8-regular affine Heisenberg bulk
Payne-derived H27 shell      = GQ(2,4) SRG(27,10,1,5)
Schlaefli graph              = complement SRG(27,16,10,8)
27 pair-frontier solver      = H27/Payne sheaf boundary
D5 x H27 x 8-cycle lift      = 2160 mirror bus
```
