# BT1823 quartet / W(E6) diagram spec

Purpose: render the fibre-law chain from the global Schlaefli symmetry down to the local oriented D4/GKP correction.

## Diagram layers

```text
W(E6) image stabilizer
  |
  v
10 stabilizer slices of Hesse hinges
  |
  v
observed size-6 slice
  |
  v
K4 edge set on {00,01,10,11}
  |
  v
oriented edge 00 -> 11
  |
  v
XZ diagonal / both-quadrature half-shift
  |
  v
T010:-2, T210:-2, T222:+2
  |
  v
F3 syndrome [0,2,1,1,1] + [0,1,2,2,2] = [0,0,0,0,0]
```

## Core counts

```text
816 all triples
54 Hesse hinges
10 W(E6) stabilizer slices
6 hinges in the observed slice = C(4,2)
4 hidden quartet states = F2^2
12 oriented quartet edges
1 observed oriented edge = 00 -> 11
```

## Mermaid sketch

```mermaid
flowchart TD
  A[W(E6) image stabilizer] --> B[10 stabilizer slices]
  B --> C[observed size-6 hinge slice]
  C --> D[K4 edge set: C(4,2)=6]
  D --> E[hidden quartet F2^2: 00,01,10,11]
  E --> F[observed oriented edge: 00 -> 11]
  F --> G[XZ diagonal / both-quadrature half-shift]
  G --> H[T010:-2, T210:-2, T222:+2]
  H --> I[F3 cancellation: [0,2,1,1,1]+[0,1,2,2,2]=0]
```

## Graphviz DOT sketch

```dot
digraph quartet_law {
  rankdir=LR;
  W_E6 [label="W(E6) image stabilizer"];
  slices [label="10 stabilizer slices"];
  hinge [label="observed 6-hinge slice"];
  k4 [label="K4 edge set, C(4,2)=6"];
  square [label="F2^2 quartet: 00,01,10,11"];
  edge [label="oriented edge 00 -> 11"];
  op [label="XZ diagonal / both-quadrature half-shift"];
  corr [label="T010:-2, T210:-2, T222:+2"];
  syn [label="F3 cancellation"];
  W_E6 -> slices -> hinge -> k4 -> square -> edge -> op -> corr -> syn;
}
```

## Caption

The global Schlaefli/W(E6) symmetry does not select a single table defect.  It selects a size-six Hesse-hinge slice.  That slice is the edge set of a hidden four-state D4/GKP quartet.  The observed table correction is one oriented diagonal edge, `00 -> 11`, corresponding to the local `XZ` half-shift.  The induced correction `T010:-2, T210:-2, T222:+2` preserves the binary Hesse split and cancels the ternary double-six syndrome.
