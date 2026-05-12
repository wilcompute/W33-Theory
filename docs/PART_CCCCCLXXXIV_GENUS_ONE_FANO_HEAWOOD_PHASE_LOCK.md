# Part CCCCCLXXXIV — Genus-One Fano/Heawood Phase Lock

This part records a new arithmetic lock found by comparing the genus oscillator, Fano/Heawood torus structure, and the W33 mod-12 non-backtracking split.

## 1. Genus-one oscillator values

The genus oscillator gives

```text
v(h)=4+3h,
E(h)=6+15h,
F(h)=4+10h.
```

At genus one:

```text
(v,E,F) = (7,21,14).
```

This is not merely numerology.  It is exactly the natural toroidal/Fano/Heawood package:

```text
7  = Fano points / toroidal colors / K7 vertices,
21 = Fano incidences / K7 edges / 3*7,
14 = two oriented face polarities per color / 2*7.
```

The Csaszar torus realizes the K7 skeleton.  The Szilassi dual realizes maximal face adjacency.  Together they form the two maximum-adjacency polarizations of the genus-one shell.

## 2. Mod-12 decomposition

W33 has a local 12-clock through 12-regularity.  The non-backtracking turn split is

```text
11 = 2 triangle turns + 9 open turns.
```

The genus-one torus counts decompose around the same 12-clock:

```text
E(1)=21=12+9,
F(1)=14=12+2.
```

So the torus layer encodes the same local split as the W33 directed-edge dynamics:

```text
open-turn component      9  appears in E(1)-12,
triangle-turn component  2  appears in F(1)-12.
```

This is a new exact bridge:

```text
Csaszar/Szilassi genus-one arithmetic = W33 12-clock plus Hashimoto 9+2 turn split.
```

## 3. Fano/Heawood meaning

The torus has chromatic maximum 7 via the Heawood theorem, and the Csaszar polyhedron realizes a K7 graph on the torus.  The Fano plane also has:

```text
7 points,
7 lines,
3 points per line,
21 incidences.
```

Therefore the same triple appears three ways:

```text
K7 torus skeleton:       7 vertices, 21 edges,
Fano incidence algebra:  7 colors, 21 incidences,
genus oscillator h=1:   7 vertices, 21 edges, 14 faces.
```

The face count `14=2*7` is naturally read as two face/chirality/polarity sheets over the seven Fano colors.

## 4. Phase superperiod

Each handle advances the mod-12 vertex/edge phase by

```text
Delta v = 3,
Delta E = 15 == 3 mod 12.
```

Thus the local mod-12 transport phase has period

```text
12/gcd(12,3)=4.
```

If the genus-one toroidal color shell advances through 7 colors, the coupled phase period is

```text
4*7=28.
```

This number is structurally important:

```text
28 = dim so(8) = number of bivectors in 8 dimensions = edges of K8.
```

Over one such 28-step handle/color period, the Euler characteristic changes by

```text
28*(-2) = -56.
```

The pair

```text
28 / 56
```

is suggestive: `28` is the Spin(8)/bivector/triality scale and `56` is the canonical symplectic scale familiar from E7-style structures.  This should be treated as a target for further verification, not yet as a proven physical identification.

## 5. Main synthesis

The genus-one layer is the first place where the clocks lock simultaneously:

```text
7  = Fano/Heawood/toroidal color shell,
12 = W33 local incidence phase clock,
9+2 = Hashimoto open/triangle turn split,
21=12+9,
14=12+2.
```

This says the toroidal polyhedra are not just examples of genus-one topology.  They are the minimal surface realization of the same phase arithmetic already appearing in W33 non-backtracking dynamics.

## 6. Next executable check

The next script should verify and track:

```text
h=1: (v,E,F)=(7,21,14),
E-12=9,
F-12=2,
E=3*7,
F=2*7,
phase period = 4*7=28,
Euler drift over period = -56.
```

Then compare the 28/56 phase-superperiod against existing E7/E8 and Clifford/bivector artifacts in the repo.
