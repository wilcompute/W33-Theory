# BT1865-BT1868 summary

Executed BT1865-BT1867 and continued one layer deeper to BT1868 after the CSS commutation obstruction revealed a cleaner subsystem route.

## Repo/paper searches

Searched across:

```text
CSS commutation / HX HZ mod 3
qutrit Pauli / GF3 stabilizer language
global clock sum / distance rows / C12 winding
Rule 110 / glider / domain wall / cellular automaton diagnostics
Holonet TeX splice / REVTeX integration
```

No prior Rule-110/glider diagnostic layer existed, and no existing CSS K12/F12 commutation result was found.  The closest structural anchors remain BT1348 for GF(3) qutrit QEC language and BT1827 for C12 cyclic residue/winding protection.

## BT1865 — CSS commutation matrix

The naive CSS split was tested:

```text
HX = 44 face-current rows
HZ = 6 cyclic-distance rows
field = GF(3)
```

Result:

```text
shape(HX HZ^T) = 44 x 6
rank(HX HZ^T) = 5
nonzero entries = 116
zero face rows = 1
nonzero face rows = 43
```

Row support profile:

```text
0 nonzero columns: 1 face
2 nonzero columns: 13 faces
3 nonzero columns: 30 faces
```

Right kernel:

```text
span{(1,1,1,1,1,1)}
```

Verdict: the naive six-row CSS split fails, but the all-distance/global clock-sum row commutes with all face rows.

## BT1866 — TeX splice runner

Added:

```text
tools/run_bt1863_tex_splice_and_check.sh
```

The runner executes the BT1863 splice script, verifies the integrated output file, checks for the K12/F12 compiler label, checks for the raw-distance boundary, rejects `enumerate[nosep]`, and compiles if `latexmk` or `pdflatex` is available.

Connector boundary: the remote GitHub connector cannot execute shell scripts in a checkout, so this is a committed reproducible local runner, not a claimed remote PDF build.

## BT1867 — Rule-110 glider diagnostics

Diagnosed the 120-step BT1864 orbit.

```text
length = 30
steps = 120
ones_min = 9
ones_max = 24
entropy_min = 0.7219280948873623
entropy_max = 1.0
cyclic_transitions_min = 6
cyclic_transitions_max = 24
```

All eight Rule-110 neighborhoods occur.  Diagonal persistence appears at several velocities:

```text
v=-3,-2,-1,+3 all reach length 12
v=0 reaches length 18
```

Verdict: nontrivial domain-wall and diagonal persistence is present, but no isolated long-lived glider family is proven in the 30-cell periodic box.

## BT1868 — global-clock CSS skeleton

BT1868 follows the BT1865 obstruction.

Do not use all six distance rows as Z stabilizers.  Instead:

```text
Z stabilizer = H1 + H2 + H3 + H4 + H5 + H6
five distance-class contrasts = gauge/defect rows
```

Payload skeleton:

```text
physical qutrits = 66
X rank = 42
Z rank = 1
commuting = true
candidate k = 23
distance = unknown
```

Full 72-symbol skeleton before gauge fixing:

```text
physical symbols = 72
X rank = 42
Z rank = 1
candidate k before gauge fixing = 29
parity/gauge degrees = 6
```

Breakthrough: the first clean CSS-compatible object is not the full six-distance-row code.  It is the face-check layer plus one global clock stabilizer, with the five distance contrasts demoted to gauge or requiring a dual face system.

## Boundary

BT1865 and BT1868 are exact GF(3) commutation/skeleton analyses, BT1866 is a reproducible local integration runner, and BT1867 is a finite orbit diagnostic.  No quantum distance theorem, PDF build, full Rule-110 universality proof, or physical implementation is claimed.
